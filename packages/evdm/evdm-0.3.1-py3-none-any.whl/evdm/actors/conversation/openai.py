"""Actors related to OpenAI based conversation management."""

import asyncio

from evdm.core import BusType, Event, make_event, Actor, Emitter
import os
import json
from websockets.asyncio.client import connect
from loguru import logger
import soundfile as sf
import io
import numpy as np
import base64


async def decode_audio(data: str):
    """Decode base64 audio `data` that's in raw PCM_16 little endian format to
    samples and sampling rate.
    """

    # This is the default for the API
    sr = 24_000

    binary_data = base64.b64decode(data)

    def _read(buffer):
        with sf.SoundFile(buffer, "r", format="RAW", samplerate=sr, channels=1, subtype="PCM_16", endian="LITTLE") as fp:
            return fp.read()

    with io.BytesIO(binary_data) as buffer:
        loop = asyncio.get_event_loop()
        samples = await loop.run_in_executor(None, lambda: _read(buffer))

    samples = samples.astype(np.float32)
    return samples.reshape(len(samples), 1), sr


async def encode_audio(audio_samples, samplerate: int) -> str:
    """Encode audio to base64 encoded binary format that's acceptable via
    the API.
    """

    # HACK since they are allowing only this sampling rate right now
    assert samplerate == 24_000

    def _write(buffer, samples, sr: int):
        with sf.SoundFile(buffer, "w", format="RAW", samplerate=sr, channels=1, subtype="PCM_16", endian="LITTLE") as fp:
            fp.write(samples)

    with io.BytesIO() as buffer:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: _write(buffer, audio_samples, samplerate))

        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")


def build_diarized_transcript(data_items: list[dict]) -> str:
    """Take word level transcription events and return stitched text for LLM
    consumption while taking care of multi speaker transcripts.
    """

    # First we figure out if diarization is happening
    single_speaker = data_items[0]["speaker"] is None

    if single_speaker:
        return " ".join([it["text"] for it in data_items])

    last_speaker = data_items[0]["speaker"]
    lines = []
    accumulator = []

    for it in data_items:
        current_speaker = it["speaker"]
        if current_speaker == last_speaker:
            accumulator.append(it["text"])
        else:
            lines.append(f"speaker {last_speaker + 1}: {' '.join(accumulator)}")
            accumulator = [it["text"]]
            last_speaker = current_speaker

    lines.append(f"speaker {last_speaker + 1}: {' '.join(accumulator)}")

    return "\n".join(lines)


class OpenAIRealtimeBase(Actor, Emitter):
    """Base class handling the realtime API. You should extend this and make
    concrete versions.

    The mandatory methods to implement are: `session_update` and `act`.
    """

    def __init__(self, prompt: str) -> None:
        super().__init__()
        self.prompt = prompt

    async def connect(self):
        url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key is None:
            raise ValueError("OPENAI_API_KEY not set.")

        self.ws = await connect(url, additional_headers={
            "Authorization": "Bearer " + api_key,
            "OpenAI-Beta": "realtime=v1"
        })

        await self.session_update()
        asyncio.create_task(self.handle_server_events())

    async def session_update(self):
        raise NotImplementedError()

    async def act(self, event: Event):
        raise NotImplementedError()

    async def handle_error(self, message_data: dict):
        raise RuntimeError(f"Server error: {message_data}")

    async def handle_server_events(self):
        """Loop and listen to server events and then act accordingly. We ignore
        most of the events for now but we still 'handle' all to ensure that any
        upstream change doesn't blow up in our face.
        """

        async for message in self.ws:
            data = json.loads(message)

            match data["type"]:
                case "error":
                    await self.handle_error(data)
                case "session.created":
                    logger.debug("Session created.")
                case "session.updated":
                    pass
                case "conversation.created":
                    pass
                case "input_audio_buffer.committed":
                    pass
                case "input_audio_buffer.cleared":
                    pass
                case "input_audio_buffer.speech_started":
                    logger.debug("Input speech started")
                case "input_audio_buffer.speech_stopped":
                    logger.debug("Input speech stopped")
                case "conversation.item.created":
                    logger.debug("Conversation item created")
                case "conversation.item.input_audio_transcription.completed":
                    await self.handle_input_transcript(data)
                case "conversation.item.input_audio_transcription.failed":
                    pass
                case "conversation.item.truncated":
                    pass
                case "conversation.item.deleted":
                    pass
                case "response.created":
                    logger.debug(f"Response created")
                case "response.done":
                    logger.debug(f"Response done")
                case "response.output_item.added":
                    logger.debug(f"Response item added")
                case "response.output_item.done":
                    logger.debug(f"Response item done")
                case "response.content_part.added":
                    pass
                case "response.content_part.done":
                    pass
                case "response.text.delta":
                    pass
                case "response.text.done":
                    await self.handle_output_text(data)
                case "response.audio_transcript.delta":
                    pass
                case "response.audio_transcript.done":
                    await self.handle_output_transcript(data)
                case "response.audio.delta":
                    await self.handle_audio_delta(data)
                case "response.audio.done":
                    pass
                case "response.function_call_arguments.delta":
                    pass
                case "response.function_call_arguments.done":
                    pass
                case "rate_limits.updated":
                    pass

    async def handle_output_text(self, message_data: dict):
        await self.emit(make_event(BusType.Texts, {
            "source": "oai-realtime",
            "text": message_data["text"],
            "is_eou": True
        }))

    async def handle_output_transcript(self, message_data: dict):
        await self.emit(make_event(BusType.Texts, {
            "source": "oai-realtime-transcript",
            "text": message_data["transcript"],
            "is_eou": True
        }))

    async def handle_input_transcript(self, message_data: dict):
        await self.emit(make_event(BusType.Texts, {
            "source": "oai-input-asr",
            "text": message_data["transcript"],
            "is_eou": True
        }))

    async def handle_audio_delta(self, message_data: dict):
        samples, sr = await decode_audio(message_data["delta"])

        await self.emit(make_event(BusType.AudioSignals, {
            "source": "oai-realtime",
            "samples": samples,
            "sr": sr
        }))


class OpenAITexttoSpeechConvAgent(OpenAIRealtimeBase):
    """Agent that uses OpenAI Realtime API for multi-party conversations by
    sending text from user side and receiving audio from OpenAI.
    """

    def __init__(self, prompt: str, source: str = "asr") -> None:
        super().__init__(prompt)
        self.source = source
        self.accumulator = []

    async def session_update(self):
        await self.ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": self.prompt,
                "voice": "alloy",
                "output_audio_format": "pcm16",
                "tools": [],
                "tool_choice": "none",
                "temperature": 0.8
            }
        }))

    async def act(self, event: Event):
        if event.data["source"] != self.source:
            return

        if "signal" in event.data:
            if event.data["signal"] == "eou":
                transcript = build_diarized_transcript(self.accumulator)
                self.accumulator = []

                await self.ws.send(json.dumps({
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": transcript
                            }
                        ]
                    }
                }))

                await self.ws.send(json.dumps({
                    "type": "response.create"
                }))

        else:
            self.accumulator.append(event.data)


class OpenAISpeechtoSpeechConvAgent(OpenAIRealtimeBase):
    """Agent that uses OpenAI Realtime API for two-party conversations.

    This listens on Audio Signals bus (since we use server VAD mode from the
    API) and emits to Audio Signals (output audio) and Lexical Segments
    (transcripts) bus.
    """

    def __init__(self, prompt: str, source: str) -> None:
        super().__init__(prompt)
        self.source = source

    async def session_update(self):
        await self.ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": self.prompt,
                "voice": "alloy",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 200
                },
                "tools": [],
                "tool_choice": "none",
                "temperature": 0.8
            }
        }))

    async def act(self, event: Event):
        if event.data["source"] != self.source:
            return

        sr = event.data["sr"]
        samples = event.data["samples"]

        encoded_audio = await encode_audio(samples, sr)

        await self.ws.send(json.dumps({
            "type": "input_audio_buffer.append",
            "audio": encoded_audio
        }))
