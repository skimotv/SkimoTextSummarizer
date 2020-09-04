import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

# helper to break up longer strings
def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

# helper fn to break up longer strings
def breaktext(text):
    if len(text) < 4000:
        return [text]
    else:
        return list(chunkstring(text, 4000))


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

    inputs = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")
    outputs = model.generate(inputs, max_length=250, do_sample=True, top_p=0.95, top_k=60)
    generated = tokenizer.decode(outputs[0])

    return generated

    '''
    # generate lists to be summarized
    chunks = breaktext(text)
    text_out = ''
    
    # Tokenize input, run model, decode output
    for c in chunks:
        inputs = tokenizer.encode(c, add_special_tokens=False, return_tensors="pt")
        outputs = model.generate(inputs, max_length=250, do_sample=True, top_p=0.95, top_k=60)
        generated = tokenizer.decode(outputs[0])
        text_out = text + c

    return text_out
    '''
