from spacy.tokens import Span, Doc
from utils import count_ents


class Detector:
    def __init__(self, verbs, transcript_list):
        self.MIN_WORDS = 10
        self.action_items = []
        self.transcript = transcript_list
        self.action_verbs = verbs

    def run_detector(self):
        # bottom_half = transcript[len(transcript) / 2:].split(' ', 1)[1]

        self.__detect_action_items()

    def get_action_items(self):
        return self.action_items

    def __detect_action_items(self):
        acceptable_verb_tags = ['VB', 'VBP', 'VBZ']
        # create a custom extension using a lambda to filter out sentences with a particular token
        filtered_tokens = ['?', 'thank']  # list will be expanded

        def token_getter(span):
            return any(token in span.text for token in filtered_tokens)

        Span.set_extension("has_filtered_token", getter=token_getter)
        Doc.set_extension("has_filtered_token", getter=token_getter)

        for sentence in self.transcript:
            if len(sentence) < self.MIN_WORDS or sentence._.has_filtered_token:
                continue

            subtree_list = []
            token_list = []
            flag = False
            for token in sentence:
                if token.tag_ in acceptable_verb_tags and token.lemma_ in self.action_verbs:
                    token_list.append(token)
                    subtree_span = sentence[token.left_edge.i: token.right_edge.i + 1]
                    subtree_list.append(subtree_span)
                    flag = True

                if token.i == (len(sentence) - 1) and flag is True:
                    ent_count = count_ents(sentence)
                    if ent_count != 0:
                        self.action_items.append({'tokens': token_list,
                                                  'subtrees': subtree_list,
                                                  'sentence': sentence,
                                                  'ent_count': ent_count})

