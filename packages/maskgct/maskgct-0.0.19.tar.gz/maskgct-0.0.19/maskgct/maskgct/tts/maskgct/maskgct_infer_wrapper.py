# Copyright (c) 2024 Amphion.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import torch
from .maskgct_utils import *
from huggingface_hub import hf_hub_download
import safetensors
import soundfile as sf
from loguru import logger
from accelerate import load_checkpoint_and_dispatch


class MaskGCTInfer:

    def __init__(self, checkpoint_dir="checkpoints/") -> None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        cfg_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "maskgct.json"
        )
        cfg = load_config(cfg_path)

        # 1. build semantic model (w2v-bert-2.0)
        self.semantic_model, self.semantic_mean, self.semantic_std = (
            build_semantic_model(device)
        )
        # 2. build semantic codec
        self.semantic_codec = build_semantic_codec(cfg.model.semantic_codec, device)
        # 3. build acoustic codec
        self.codec_encoder, self.codec_decoder = build_acoustic_codec(
            cfg.model.acoustic_codec, device
        )
        # 4. build t2s model
        self.t2s_model = build_t2s_model(cfg.model.t2s_model, device)
        # 5. build s2a model
        self.s2a_model_1layer = build_s2a_model(cfg.model.s2a_model.s2a_1layer, device)
        self.s2a_model_full = build_s2a_model(cfg.model.s2a_model.s2a_full, device)

        # download checkpoint
        # download semantic codec ckpt
        semantic_code_ckpt = hf_hub_download(
            "amphion/MaskGCT",
            filename="semantic_codec/model.safetensors",
            local_dir=checkpoint_dir,
        )
        logger.info(f"semantic_code_ckpt got.")
        # download acoustic codec ckpt
        codec_encoder_ckpt = hf_hub_download(
            "amphion/MaskGCT",
            filename="acoustic_codec/model.safetensors",
            local_dir=checkpoint_dir,
        )
        codec_decoder_ckpt = hf_hub_download(
            "amphion/MaskGCT",
            filename="acoustic_codec/model_1.safetensors",
            local_dir=checkpoint_dir,
        )
        # download t2s model ckpt
        t2s_model_ckpt = hf_hub_download(
            "amphion/MaskGCT",
            filename="t2s_model/model.safetensors",
            local_dir=checkpoint_dir,
        )
        # download s2a model ckpt
        s2a_1layer_ckpt = hf_hub_download(
            "amphion/MaskGCT",
            filename="s2a_model/s2a_model_1layer/model.safetensors",
            local_dir=checkpoint_dir,
        )
        s2a_full_ckpt = hf_hub_download(
            "amphion/MaskGCT",
            filename="s2a_model/s2a_model_full/model.safetensors",
            local_dir=checkpoint_dir,
        )
        logger.info(f"loading safetensors...")
        device_map = {"": "cpu"}
        load_checkpoint_and_dispatch(
            self.semantic_codec, semantic_code_ckpt, device_map=device_map
        )
        load_checkpoint_and_dispatch(
            self.codec_encoder, codec_encoder_ckpt, device_map=device_map
        )
        load_checkpoint_and_dispatch(
            self.codec_decoder, codec_decoder_ckpt, device_map=device_map
        )

        load_checkpoint_and_dispatch(
            self.t2s_model, t2s_model_ckpt, device_map=device_map
        )
        load_checkpoint_and_dispatch(
            self.s2a_model_1layer, s2a_1layer_ckpt, device_map=device_map
        )
        load_checkpoint_and_dispatch(
            self.s2a_model_full, s2a_full_ckpt, device_map=device_map
        )

        self.maskgct_inference_pipeline = MaskGCT_Inference_Pipeline(
            self.semantic_model.to(self.device),
            self.semantic_codec.to(self.device),
            self.codec_encoder.to(self.device),
            self.codec_decoder.to(self.device),
            self.t2s_model.to(self.device),
            self.s2a_model_1layer.to(self.device),
            self.s2a_model_full.to(self.device),
            self.semantic_mean.to(self.device),
            self.semantic_std.to(self.device),
            self.device,
        )
        logger.info("MaskGCT Inference Pipeline Initialized")

    # inference
    def infer(
        self,
        prompt_wav_path,
        prompt_text,
        target_text,
        source_lang="en",
        target_lang="en",
        target_len=None,
        save_path=None,
    ):
        """
        if target_len is None, will use a simple way to predict duration
        """
        prompt_wav_path = prompt_wav_path

        recovered_audio = self.maskgct_inference_pipeline.maskgct_inference(
            prompt_wav_path,
            prompt_text,
            target_text,
            source_lang,
            target_lang,
            target_len=target_len,
        )
        if save_path is None:
            return recovered_audio
        else:
            sf.write(save_path, recovered_audio, 24000)
            return save_path
