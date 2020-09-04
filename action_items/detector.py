from spacy.tokens import Span, Doc
from lib.utils import count_ents, fix_text


class Detector:
    def __init__(self, verbs, transcript_list):
        self.action_items = []
        self.sents_with_dates = []
        self.transcript_list = transcript_list
        self.action_verbs = verbs

    def run_detector(self):
        """
        Driver function for the Detector. Populates the Action Items list and the Dates list with relevant info.
        """
        self.__detect_action_items()
        self.__detect_dates()

    def get_action_items(self):
        return self.action_items

    def get_sents_with_dates(self):
        return self.sents_with_dates

    def __detect_action_items(self):
        """
        Identifies action verbs (from a given list of verbs) in a transcript (a list of sentences) and filters out
        sentences that do not contain an action verb.
        """
        acceptable_verb_tags = ['VB', 'VBP', 'VBZ']

        filtered_tokens = ['?', 'thank']  # list will be expanded
        self.__set_filtered_tokens_ext(filtered_tokens)

        for sentence in self.transcript_list:
            if sentence._.has_filtered_token:
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

    def __set_filtered_tokens_ext(self, filtered_tokens):
        """
        Creates a custom extension using a lambda to filter out sentences (Span/Doc objects) with a particular token
        :param filtered_tokens: The list of tokens to filter out
        """
        def token_getter(span):
            return any(token in span.text for token in filtered_tokens)

        Span.set_extension("has_filtered_token", getter=token_getter)
        Doc.set_extension("has_filtered_token", getter=token_getter)

    def __generate_dict(self, token_list, subtree_list, sentence):
        """
        Generates a dictionary entry and appends to the action items list: one entry per relevant sentence.
        :param token_list: the list of action verbs in the sentence
        :param subtree_list: the list subtrees associated with the tokens
        :param sentence: the sentence containing the action verbs
        """
        ent_count = count_ents(sentence)  # the number of named entities in the sentence
        if ent_count != 0:
            self.action_items.append({'tokens': token_list,
                                      'subtrees': subtree_list,
                                      'sentence': sentence,
                                      'ent_count': ent_count})

    def __detect_dates(self):
        """
        Detects the sentences with dates/times in the transcript and appends them to the sents with dates list.
        """
        for sentence in self.transcript_list:
            sentence_ents = list(sentence.ents)
            for ent in sentence_ents:
                if ent.label_ == 'DATE' or ent.label_ == 'TIME':
                    self.sents_with_dates.append(sentence)

# -------------------------------------------------------------------------------------------------------------------- #

WORKING_DIR = 'Enter your working directory here'
VERBS_LOC = WORKING_DIR + 'action_verbs.txt'
TRANSCRIPT_LOC = WORKING_DIR + 'boe_transcript.txt'

transcript_list = open(TRANSCRIPT_LOC, 'r').readlines()
transcript_list = fix_text(transcript_list, True)
print('text has been fixed')

verbs = open(VERBS_LOC, 'r').readlines()
verbs = [verb.lower().replace('\n', '') for verb in verbs]  # cleans list

detect = Detector(verbs, transcript_list)
detect.run_detector()
action_items = detect.get_action_items()
print('detector has detected')

for item in action_items:
    print(item)
