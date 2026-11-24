from pathlib import Path
from huggingface_hub import snapshot_download

model_path = Path(__file__).resolve().parent / "hubert"

snapshot_download(
    repo_id="facebook/hubert-base-ls960",
    local_dir=model_path,
    allow_patterns=[
        "config.json",
        "preprocessor_config.json",
        "pytorch_model.bin"
    ]
)

print("HuBERT downloaded successfully!")