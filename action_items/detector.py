from spacy.tokens import Span, Doc
from utils import count_ents


class Detector:
    def __init__(self, verbs, transcript_list):
        self.MIN_WORDS = 10
        self.action_items = []
        self.sents_with_dates = []
        self.transcript_list = transcript_list
        self.action_verbs = verbs

    def run_detector(self):
        self.__detect_action_items()
        self.__detect_dates()

    def get_action_items(self):
        return self.action_items

    def get_sents_with_dates(self):
        return self.sents_with_dates

    def __detect_action_items(self):
        acceptable_verb_tags = ['VB', 'VBP', 'VBZ']

        filtered_tokens = ['?', 'thank']  # list will be expanded
        self.__set_filtered_tokens_ext(filtered_tokens)

        for sentence in self.transcript_list:
            if len(sentence) < self.MIN_WORDS or sentence._.has_filtered_token:
                continue

            subtree_list = []
            token_list = []
            flag = False
            for token in sentence:
                if token.tag_ in acceptable_verb_tags and token.lemma_ in self.action_verbs:
                    token_list.append(token)
                    subtree_list.append(sentence[token.left_edge.i: token.right_edge.i + 1])  # gets the token's subtree
                    flag = True

                if flag is True and token.i == (len(sentence) - 1):
                    self.__generate_dict(token_list, subtree_list, sentence)

    # create a custom extension using a lambda to filter out sentences with a particular token
    def __set_filtered_tokens_ext(self, filtered_tokens):
        def token_getter(span):
            return any(token in span.text for token in filtered_tokens)

        Span.set_extension("has_filtered_token", getter=token_getter)
        Doc.set_extension("has_filtered_token", getter=token_getter)

    def __generate_dict(self, token_list, subtree_list, sentence):
        ent_count = count_ents(sentence)
        if ent_count != 0:
            self.action_items.append({'tokens': token_list,
                                      'subtrees': subtree_list,
                                      'sentence': sentence,
                                      'ent_count': ent_count})

    def __detect_dates(self):
        for sentence in self.transcript_list:
            sentence_ents = list(sentence.ents)
            for ent in sentence_ents:
                if ent.label_ == 'DATE' or ent.label_ == 'TIME':
                    self.sents_with_dates.append(sentence)

