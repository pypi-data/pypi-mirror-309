import sys
from phonemizer.backend.espeak.wrapper import EspeakWrapper
import os
from loguru import logger


def get_espeak_library():
    if sys.platform == "win32":
        paths = [
            r"C:\Program Files\eSpeak NG\libespeak-ng.dll",
            r"C:\Program Files (x86)\eSpeak NG\libespeak-ng.dll",
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    elif sys.platform == "darwin":  # macOS
        paths = [
            "/usr/local/lib/libespeak-ng.dylib",
            "/opt/homebrew/lib/libespeak-ng.dylib",
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    else:  # Linux
        paths = [
            "/usr/lib/libespeak-ng.so",
            "/usr/lib/x86_64-linux-gnu/libespeak-ng.so",
            "/usr/local/lib/libespeak-ng.so",
            "/usr/lib64/libespeak-ng.so",
            "/usr/lib64/libespeak-ng.so.1",
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    logger.info(
        """espeak-ng library not found, you may check yourself or ignore. install instructions:
brew install espeak-ng
apt install libespeak-ng-dev
yum install espeak-ng-devel
                """
    )
    return None


espeak_lib = get_espeak_library()
if espeak_lib:
    EspeakWrapper.set_library(espeak_lib)
