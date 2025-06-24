import json
from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1, device=device)

with open("exports/summarized_articles.json", "r") as f:
    articles = json.load(f)

for article in articles:
    if 'summary' in article:
        emotion = classifier(article['summary'])[0][0]['label']
        article['emotion'] = emotion

with open("exports/tagged_articles.json", "w") as f:
    json.dump(articles, f, indent=2)
