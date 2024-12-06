import os
from pathlib import Path

import modal

from utils import GPU_IMAGE, MINUTES, NAME, VOLUME_CONFIG, _exec_subprocess

parent_path: Path = Path(__file__).parent.parent.parent
model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"


# container build-time fns
def download_model():
    from huggingface_hub import login, snapshot_download  # type: ignore

    login(token=os.getenv("HF_TOKEN"), new_session=False)
    snapshot_download(
        model_id,
        ignore_patterns=["*.pt", "*.bin"],
    )


# Modal
in_prod: bool = os.getenv("MODAL_ENVIRONMENT", "dev") == "main"
SECRETS = [modal.Secret.from_dotenv(path=parent_path, filename=".env" if in_prod else ".env.dev")]
IMAGE = (
    GPU_IMAGE.pip_install(  # add Python dependencies
        "bitsandbytes>=0.44.1",
        "datasets>=2.14.4",
        "matplotlib>=3.9.2",
        "torch>=2.5.0",
        "torchao>=0.6.1",
        "torchtune>=0.3.1",
        "torchvision>=0.20.0",
        "transformers>=4.45.2",
        "safetensors==0.4.5",
    )
    .run_function(
        download_model,
        secrets=SECRETS,
        volumes=VOLUME_CONFIG,
    )
    .copy_local_file(
        parent_path / "training" / "model.py",
        "/root/original/model.py",  # can't be /root/model.py since it's this file in the container
    )
)
TIMEOUT = 15 * MINUTES
GPU_TYPE = "H100"
GPU_COUNT = 1
GPU_SIZE = None  # options = None, "40GB", "80GB"
GPU_CONFIG = f"{GPU_TYPE}:{GPU_COUNT}"
if GPU_TYPE.lower() == "a100":
    GPU_CONFIG = modal.gpu.A100(count=GPU_COUNT, size=GPU_SIZE)

APP_NAME = f"{NAME}-model"
app = modal.App(name=APP_NAME)


@app.function(
    image=IMAGE,
    gpu=GPU_CONFIG,
    volumes=VOLUME_CONFIG,
    timeout=TIMEOUT,
)
def main():
    _exec_subprocess(["python", "/root/original/model.py"])


@app.local_entrypoint()
def local():
    main.remote()
