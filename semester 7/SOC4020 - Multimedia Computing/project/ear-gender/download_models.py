"""Download everything the project needs (about 126 MB). Run once:

  python download_models.py

  models/haarcascade_mcs_leftear.xml, ..._rightear.xml   ear detectors (OpenCV 2.4 repo)
  models/mobilenetv2-12.onnx                             feature extractor (ONNX model zoo)
  data/EarVN1.0 dataset/                                 training data (Mendeley Data,
                                                         non-commercial use only)
"""
import hashlib
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
MODELS, DATA = HERE / "models", HERE / "data"

FILES = {
    MODELS / "haarcascade_mcs_leftear.xml":
        "https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_mcs_leftear.xml",
    MODELS / "haarcascade_mcs_rightear.xml":
        "https://raw.githubusercontent.com/opencv/opencv/2.4/data/haarcascades/haarcascade_mcs_rightear.xml",
    MODELS / "mobilenetv2-12.onnx":
        "https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx",
    DATA / "EarVN1.0.rar":
        "https://data.mendeley.com/public-files/datasets/yws3v3mwx3/files/"
        "e47d0c62-1d22-42a0-a70a-2013ede1373a/file_downloaded",
}
EARVN_SHA256 = "f1675a810edb6876366c56743a0d86d62417a2abc761f743550200b112cb01de"


def main():
    MODELS.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    for target, url in FILES.items():
        if target.exists() and target.stat().st_size > 0:
            print(f"already have {target.name}")
            continue
        print(f"downloading {target.name} ...")
        urllib.request.urlretrieve(url, target)
        print(f"  {target.stat().st_size / 1e6:.1f} MB")

    rar = DATA / "EarVN1.0.rar"
    if hashlib.sha256(rar.read_bytes()).hexdigest() != EARVN_SHA256:
        raise SystemExit("EarVN1.0.rar checksum mismatch - delete it and run again")
    if not (DATA / "EarVN1.0 dataset").exists():
        print("extracting EarVN1.0.rar ...")
        # Windows 10/11 ships bsdtar, which can read .rar archives.
        subprocess.run([r"C:\Windows\System32\tar.exe", "-xf", str(rar)], cwd=DATA, check=True)
    print("done")


if __name__ == "__main__":
    main()
