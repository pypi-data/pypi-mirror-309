from .tts.maskgct.maskgct_infer_wrapper import MaskGCTInfer
import os


class TTSMaskGCT:

    def __init__(self, checkpoint_dir="checkpoints/MaskGCT") -> None:
        self.model = MaskGCTInfer(checkpoint_dir=checkpoint_dir)

    def tts_instruct(
        self,
        target_text,
        prompt_text,
        prompt_wav,
        source_lang=None,
        target_lang=None,
        target_length=None,
        return_format="wav",
        stream=True,
    ):
        # target_text = """こんにちは、私は雷军です。私はXiaomi Technologyの創設者であり、夢を持った若者です。Xiaomi Technologyでの最初の数年間は、私はずっとハードウェアを作る人でしたが、今はソフトウェアを作りたいと思っています。私は誰もが使える携帯電話を作りたいと思っています。これが私の夢です。 今、私は誰もが車に乗れるようにしたいです。"""
        # inference
        os.makedirs("temp/output/", exist_ok=True)
        name, ext = os.path.splitext(os.path.basename(prompt_wav))
        save_path = os.path.join(
            "temp/output/",
            f"{source_lang}_{target_lang}_{name}_{target_text[:10].replace(' ', '')}.{ext}",
        )
        self.model.infer(
            prompt_wav_path=prompt_wav,
            prompt_text=prompt_text,
            target_text=target_text,
            source_lang=source_lang,
            # target_lang="zh",
            target_lang=target_lang,
            target_len=target_length,
            save_path=save_path,
        )
        return save_path
