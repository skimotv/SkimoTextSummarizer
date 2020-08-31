# SkimoTextSummarizer

**Data Set**:
* [AMI Corpus](http://groups.inf.ed.ac.uk/ami/corpus/)

**Package Requirements**: 
* [spaCy 2.1.0](https://pypi.org/project/spacy/2.1.0/) (not higher) 
* [neuralcoref](https://pypi.org/project/neuralcoref/)
* [punctuator](https://pypi.org/project/punctuator/)
* [torch](https://pypi.org/project/torch/)
* [transformers](latest version from https://github.com/huggingface/transformers.git)

**Additional Requirments**: 
* [en_core_web_lg](https://spacy.io/models/en#en_core_web_lg) (for spaCy)
* [Demo-Europarl-EN](https://drive.google.com/file/d/0B7BsN5f2F1fZd1Q0aXlrUDhDbnM/view?usp=sharing) (for punctuator)


This repo contains several useful functions related to text processing, including text 
summarization, action item extraction, keyword extraction, and others.

To use the summarization function, import summarization from ./summarization/models and call
it. The first argument is the text string. The second is the type of model you want to use. For example:

text = "Four score and seven years ago ..."
summarize(text, 1)

To extract key words, import TextRank4Keyword from ./concepts/extractor. instantiate the object and
call analyze to search the text and get_keywords to return a list of key words. i.e.

tr4w = TextRank4Keyword()
tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
tr4w.get_keywords(10)
