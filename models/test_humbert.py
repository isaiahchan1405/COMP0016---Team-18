from transformers import pipeline

predictor = pipeline(
    "fill-mask",
    model="nlp-thedeep/humbert"
)

text = "The flood affected access to <mask> and sanitation services."

results = predictor(text)

for result in results:
    print(result["token_str"], result["score"])