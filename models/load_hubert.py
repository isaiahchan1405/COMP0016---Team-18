from pathlib import Path
from transformers import HubertModel, AutoFeatureExtractor

model_path = Path(__file__).resolve().parent / "hubert"

model = HubertModel.from_pretrained(model_path)
processor = AutoFeatureExtractor.from_pretrained(model_path)

model.eval()

print("HuBERT loaded successfully!")