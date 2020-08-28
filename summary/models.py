import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

# Download a summarization model from Huggingface and summarize the text
def summarize(text, m):
    # Use a model from https://huggingface.co/models?filter=summarization&sort=modified
    models = ["sshleifer/distilbart-cnn-12-3", "sshleifer/distilbart-cnn-12-6",
          "sshleifer/distilbart-cnn-6-6", "sshleifer/distilbart-xsum-1-1",
          "sshleifer/distilbart-xsum-12-1", "sshleifer/distilbart-xsum-12-3",
          "sshleifer/distilbart-xsum-12-6", "sshleifer/distilbart-xsum-6-6",
          "sshleifer/distilbart-xsum-9-6", "google/pegasus-billsum"
          ]

    # Download tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(models[m])
    model = AutoModelWithLMHead.from_pretrained(models[m])
    
    # Tokenize input, run model, decode output
    inputs = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")
    outputs = model.generate(inputs, max_length=250, do_sample=True, top_p=0.95, top_k=60)
    generated = tokenizer.decode(outputs[0])
    return generated
