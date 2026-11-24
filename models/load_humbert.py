from transformers import AutoTokenizer, AutoModelForMaskedLM

model_name = "nlp-thedeep/humbert"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)

model.eval()

print("HumBERT loaded successfully!")