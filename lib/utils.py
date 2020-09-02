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


def remove_tokens_by_pos(doc, pos):
    """
    NOTE: Can be made more efficient if Doc slicing is used
    Removes all tokens with the given Part of Speech (POS) from a Doc object.
    :param doc: The Doc object from which to remove tokens.
    :param pos: The POS for which to look.
    :return: A Doc object without the given Part of Speech
    """
    new_text = ''
    for token in doc:
        # this changes "model um, I understand" to "model, I understand" instead of "model , I understand"
        if token.i != (len(doc) - 1) and token.nbor().pos_ == pos and token.nbor(2).is_punct:
            new_text += token.text
            continue
        if token.pos_ != pos:
            new_text += token.text_with_ws

    return nlp(new_text)


def count_ents(phrase):
    """
    Counts the number of Named Entities in a spaCy Doc/Span object.
    :param phrase: the Doc/Span object from which to remove Named Entities.
    :return: The number of Named Entities identified in the input object.
    """
    named_entities = list(phrase.ents)
    return len(named_entities)


def remove_stopwords(sentence):
    """
    Removes the stop words (the most commonly used words in a language, such as 'the', 'hello', etc.) from
    the input sentence.
    :param sentence: The sentence from which to remove stop words.
    :return: The sentence minus the stop words.
    """
    stopless_sent = ''
    for token in sentence:
        if not token.is_stop:
            stopless_sent += token.text_with_ws
    return nlp(stopless_sent)


def filter_sentences(sent_dict_list):
    """
    Filters sentences (in dict objects) that do not meet the following conditions:
        1. Have more than a given threshold of tokens
        2. Have at least one Named Entity
    :param sent_dict_list: The dictionary list to filter
    :return: The dictionary list without the unneeded sentences
    """
    min_tokens = 10
    filtered_sents = []
    for sent_dict in sent_dict_list:
        sentence = sent_dict['original_sentence']
        if len(sentence) >= min_tokens and count_ents(sentence) != 0:
            filtered_sents.append(sent_dict)
    return filtered_sents


def stringify_segments(sent_dict_list, segment_type):
    """
    Converts a list of sentences (Doc objects) into strings based on their segment number, to pass to a model.
    :param sent_dict_list: The dictionary list containing the list of sentences.
    :param segment_type: The type of segment to convert (temporal_segment or non_temporal_segment)
    :return: A list of strings: one string per segment.
    """
    max_segment = max(item[segment_type] for item in sent_dict_list)
    segments = []
    for counter in range(max_segment + 1):
        sentence_list = [item['original_sentence'].text for item in sent_dict_list
                         if item[segment_type] == counter]
        segment = '. '.join(sentence_list)
        re.sub('\\s\\s+?', ' ', segment)
        if len(segment) != 0:
            segments.append(segment)
    return segments
