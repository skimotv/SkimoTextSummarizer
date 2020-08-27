import spacy
import neuralcoref
from punctuator import Punctuator
# from deepsegment import DeepSegment
import re

nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp)


def fix_text(text_list):
    """
    Cleans, punctuates, neural coreferences, and sentencizes the transcript.
    :param text_list: A list of strings; an 'unclean' transcript
    :return: A list of tokenized sentences (every sentence is a Doc object)
    """
    fixed_text = ' '.join(text_list)  # convert the list into one string
    fixed_text.replace('  ', ' ')  # remove double spaces

    print('adding punctuation; please wait a few minutes...')
    punctuator = Punctuator('Demo-Europarl-EN.pcl')
    fixed_text = punctuator.punctuate(fixed_text)
    print('punctuation has been added.')

    # with open('fixed.txt', 'w') as fix:
    #     fix.write(fixed_text)

    print('removing interjections; please wait a few more minutes...')
    fixed_text_doc = remove_tokens_by_pos(nlp(fixed_text), 'INTJ')

    print('performing neural coreferencing; please wait for several more minutes...')
    fixed_text_doc = fixed_text_doc._.coref_resolved

    print('splitting the text into sentences; please keep waiting...')
    fixed_text_list = re.split('\\.|\\?|!', fixed_text_doc)
    # segmenter = DeepSegment('en')
    # fixed_text_list = segmenter.segment(fixed_text_doc)
    fixed_text_list = [nlp(sentence) for sentence in fixed_text_list]

    return fixed_text_list


# remove all tokens with the given part of speech from a doc object
# @returns A Doc object
def remove_tokens_by_pos(doc, pos):
    new_text = ''
    for token in doc:
        # this changes "model um, I understand" to "model, I understand" instead of "model , I understand"
        if token.i != (len(doc) - 1) and token.nbor().pos_ == pos and token.nbor(2).is_punct:
            new_text += token.text
            continue
        if token.pos_ != pos:
            new_text += token.text_with_ws

    return nlp(new_text)


# counts the number of named entities in a doc/span object
def count_ents(phrase_span):
    named_entities = list(phrase_span.ents)
    return len(named_entities)


# returns a span/doc object with its stop words removed
def remove_stopwords(sentence):
    stopless_sent = ''
    for token in sentence:
        if not token.is_stop:
            stopless_sent += token.text_with_ws
    return nlp(stopless_sent)


def filter_sentences(sent_dict_list):
    min_tokens = 10
    sent_dict_list = [sentence for sentence in sent_dict_list
                      if len(sentence) > min_tokens and count_ents(sentence) != 0]
    for sent_dict in sent_dict_list:
        sentence = sent_dict['original_sentence']
        if len(sentence) < min_tokens or count_ents(sentence) == 0:
            sent_dict_list.remove(sent_dict)
    return sent_dict_list
