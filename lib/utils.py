import spacy
import neuralcoref
from punctuator import Punctuator
import re

nlp = spacy.load('en_core_web_lg')


def fix_text(text_list, is_saved):
    """
    Cleans, punctuates, neural coreferences, and sentencizes the transcript.
    :param is_saved: True if a version of the fixed text is already saved in a file
    :param text_list: A list of strings; an 'unclean' transcript
    :return: A list of tokenized sentences (every sentence is a Doc object)
    """
    file_name = 'fixed.txt'

    if is_saved:
        with open(file_name, 'r') as fixed:
            fixed_text_list = fixed.readlines()
        fixed_text_list = [text.replace('\n', '') for text in fixed_text_list]
        fixed_text_list = [nlp(sentence) for sentence in fixed_text_list]
        return fixed_text_list

    else:
        fixed_text = ' '.join(text_list)  # convert the list into one string
        fixed_text.replace('  ', ' ')  # remove double spaces

        print('adding punctuation; please wait a few minutes...')
        punctuator = Punctuator('Demo-Europarl-EN.pcl')
        fixed_text = punctuator.punctuate(fixed_text)
        print('punctuation has been added.')

        print('removing interjections; please wait a few more minutes...')
        fixed_text_doc = remove_tokens_by_pos(nlp(fixed_text), 'INTJ')

        print('performing neural coreferencing; please wait for several more minutes...')
        neuralcoref.add_to_pipe(nlp)
        fixed_text_doc = fixed_text_doc._.coref_resolved

        print('splitting the text into sentences; please keep waiting...')
        fixed_text_list = re.split('\\.|\\?|!', fixed_text_doc)

        with open(file_name, 'w') as fixed:
            for sentence in fixed_text_list:
                fixed.write(sentence + "\n")
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
    new_list = []
    for sent_dict in sent_dict_list:
        sentence = sent_dict['original_sentence']
        if len(sentence) >= min_tokens and count_ents(sentence) != 0:
            new_list.append(sent_dict)
    return new_list


def stringify_segments(sent_dict_list, segment_type):
    max_segment = max(item[segment_type] for item in sent_dict_list)
    segments = []
    for counter in range(max_segment + 1):
        segment = stringify_segment(sent_dict_list, counter, segment_type)
        if len(segment) != 0:
            segments.append(segment)
    return segments


def stringify_segment(sent_dict_list, segment, segment_type):
    sentence_list = [item['original_sentence'].text for item in sent_dict_list if item[segment_type] == segment]
    stringified_segment = '. '.join(sentence_list)
    stringified_segment.replace('  ', ' ')
    return stringified_segment
