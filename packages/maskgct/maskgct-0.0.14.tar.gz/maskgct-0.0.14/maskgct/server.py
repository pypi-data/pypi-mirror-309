"""
hosting a server for maskgct
same as OpenAI API.

users can request tts also with language and prompt wav input.

the output is target wav with that language.

This is helpful when do cross language cloning.
"""

import argparse
from contextlib import asynccontextmanager
from datetime import datetime
import io
from typing import Literal, Optional, TypedDict, Union
import fastapi
from fastapi import Depends, FastAPI, Request, Response, UploadFile, File
from fastapi.responses import StreamingResponse
import librosa
import numpy as np
from uvicorn.config import Config
from uvicorn import Server
import torch
from pydantic import BaseModel
import os
import logging
from scipy.io.wavfile import write
import soundfile as sf
from pydub import AudioSegment
from loguru import logger
from maskgct.tts_wrapper import TTSMaskGCT

# logging.disable(logging.INFO)
logger_librosa = logging.getLogger("librosa")
logger_librosa.setLevel(logging.CRITICAL)
logging.getLogger("numba").setLevel(logging.WARNING)


class SpeechCreateParams(BaseModel):
    input: str
    model: Union[str, Literal["tts-1", "tts-1-hd"]] = "tts-1"
    voice: str = "中文男"
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm", "hq"] = "mp3"
    speed: float = 1.0
    stream: bool = True
    language: str = "zh"
    length: Optional[float] = None
    prompt_text: Optional[str] = None
    prompt_language: Optional[str] = "zh"


async def startup():
    print("started up..")


async def shutdown():
    print("shutting down..")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)
os.makedirs("./temp", exist_ok=True)


async def parse_form(request: Request, prompt_wav: UploadFile = File(None)):
    form_data = await request.form()
    data = SpeechCreateParams(
        input=form_data.get("input"),
        model=form_data.get("model", "tts-1"),
        voice=form_data.get("voice", "中文男"),
        response_format=form_data.get("response_format", "mp3"),
        speed=float(form_data.get("speed", 1.0)),
        length = float(form_data.get("length")) if form_data.get("length") is not None else None,
        stream=form_data.get("stream", "true").lower() == "true",
        language=form_data.get("language", "zh"),
        prompt_text=form_data.get("prompt_text"),
        prompt_language=form_data.get("prompt_language", "zh"),
    )
    return data, prompt_wav


async def parse_json(request: Request, prompt_wav: UploadFile = File(None)):
    body = await request.json()
    data = SpeechCreateParams(**body)
    return data, prompt_wav


@app.post("/v1/audio/speech", response_model=SpeechCreateParams)
async def text_to_speech(
    request: Request,
    prompt_wav: UploadFile = File(None),
):
    content_type = request.headers.get("content-type")
    logger.info(f"content type: {content_type}")
    if "application/json" in content_type:
        data = await parse_json(request, prompt_wav)
    elif "multipart/form-data" in content_type:
        data = await parse_form(request, prompt_wav)
    request, prompt_wav = data
    # do tts how to return?
    global model, model_type
    response_format = request.response_format

    prompt_wav_data = None
    print(prompt_wav.filename)
    if prompt_wav:
        original_filename = prompt_wav.filename
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_wav_path = f"./temp/{current_time}_{original_filename}"
        prompt_wav_data = await prompt_wav.read()
        with open(prompt_wav_path, "wb") as f:
            f.write(prompt_wav_data)
        logger.info(f"prompt wav saved to {prompt_wav_path}")

    if "stream" in request.model:
        print("stream mode tts.")
        # maskgct not support streaming yet.
        res = model.tts_instruct(txt, request.voice, return_format="wav", stream=True)

        def audio_stream():
            for rr in res:
                rr = rr.cpu().numpy()[0]
                print(rr)
                # audio_chunk_resampled = librosa.resample(
                #     rr, orig_sr=24000, target_sr=16000
                # )
                # audio_int16 = (audio_chunk_resampled * 32767).astype(np.int16)
                rr = (rr * 32768).astype(np.int16)

                wav_buffer = io.BytesIO()
                sf.write(file=wav_buffer, data=rr, samplerate=22050, format="WAV")
                buffer = wav_buffer
                yield buffer.getvalue()

        return StreamingResponse(audio_stream(), media_type=f"audio/{response_format}")
    else:
        if model_type == "cosyvoice":
            res = model.tts_instruct(
                request.input, request.voice, return_format="wav", stream=False
            )
            print("non-stream mode tts")
            # print(res_f)
            res = next(res)
            res = res.cpu().numpy()[0]

            if response_format == "hq":
                res = (res * 32768).astype(np.int16)
                print(f"return format: {response_format}")
                y_stretch = res
                if request.speed != 1.0:
                    # to change rate
                    y_stretch = res
                wav_buffer = io.BytesIO()
                sf.write(
                    file=wav_buffer, data=y_stretch, samplerate=22050, format="WAV"
                )
                buffer = wav_buffer
                response_format = request.response_format
                # if response_format != 'wav':
                #     wav_audio = AudioSegment.from_wav(wav_buffer)
                #     wav_audio.frame_rate=22050
                #     buffer = io.BytesIO()
                #     wav_audio.export(buffer, format=response_format)
                # sf.write(file="s_res.wav", data=y_stretch, samplerate=22050, format="WAV")
                return Response(
                    content=buffer.getvalue(), media_type=f"audio/{response_format}"
                )
            else:
                # return is sr 16k int16 wav data, it can be directly played
                audio_chunk = librosa.resample(res, orig_sr=24000, target_sr=16000)
                audio_int16 = (audio_chunk * 32768).astype(np.int16)
                buffer = io.BytesIO()
                write(buffer, 16000, audio_int16)
                buffer.seek(0)
                return Response(
                    content=buffer.read(), media_type=f"audio/{response_format}"
                )
        else:
            logger.info("maskgct model.")
            prompt_text = request.prompt_text
            txt = request.input
            logger.info(
                f"prompt text: {prompt_text}, txt: {txt}, target_lan: {request.language}"
            )
            res = model.tts_instruct(
                target_text=txt,
                prompt_text=prompt_text,
                prompt_wav=prompt_wav_path,
                source_lang=request.prompt_language,
                target_lang=request.language,
                target_length=request.length,
                return_format="wav",
                stream=False,
            )
            with open(res, "rb") as f:
                audio_data = f.read()
            return Response(content=audio_data, media_type=f"audio/{response_format}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    parser.add_argument("--type", type=str, default="instruct")
    parser.add_argument("--model", type=str, default="maskgct")
    parser.add_argument("--model_path", type=str, default="checkpoints/MaskGCT")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    global model
    global model_type

    model_type = args.model

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if args.model == "maskgct":
        logger.info("create maskgct tts model...")
        logging.info(
            f"loading model from {args.model_path} [for maskgct you should manually download models, put into: {args.model_path}]"
        )
        model = TTSMaskGCT(checkpoint_dir=args.model_path)
        logger.info("maskgct tts model loaded.")
    else:
        from cosyvoice.api import CosyVoiceTTS
        model = CosyVoiceTTS(
            device=device,
            model_cache_dir=os.path.expanduser("~/cosyvoice_models/cosyvoice"),
            model_type="base",
        )

    import asyncio

    http_config = Config(app=app, host=args.ip, port=args.port, log_level="info")
    http_server = Server(config=http_config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(http_server.serve()))
