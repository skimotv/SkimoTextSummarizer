from utils import remove_stopwords
from spacy.attrs import ORTH


class Segmenter:
    def __init__(self, transcript_list):
        self.transcript_list = transcript_list
        self.segments = []
        self.MIN_SIMILARITY = 0.7

    def run_segmenter(self):
        """
        Driver function for the class. It calls all the other functions in order.
        """
        self.segments = self.__generate_dict_list()
        stopless_sentences = [sent['stopless_sentence'] for sent in self.segments]

        segment_indexes = self.__fetch_segment_indexes(stopless_sentences)
        self.__update_temporal_segments(segment_indexes)

        segments = self.__find_related_sentences(stopless_sentences)
        self.__update_non_temporal_segments(segments)

    def get_segments(self):
        return self.segments

    def __generate_dict_list(self):
        """
        Generates a list of dictionaries; each dict maps a sentence in the transcript
        to the sentence minus its stop words.
        :return: The generated dictionary list.
        """
        sent_dict_list = []
        for sentence in self.transcript_list:
            stopless_sentence = remove_stopwords(sentence)
            sent_dict_list.append({'original_sentence': sentence, 'stopless_sentence': stopless_sentence})
        return sent_dict_list

    def __find_related_sentences(self, stopless_sentences):
        """
        This method iterates over the stopword-less sentences. It finds the sentence with the max number of
        unique tokens. It then compares every other sentence to this sentence and puts all sentences similar to this
        sentence in one segment. Then it finds the sentence with the max number of unique tokens from the remaining
        sentences. It repeats the process, and this goes on until all sentences are segmented.
        :param stopless_sentences: the list of sentences to put in segments
        :return: a 2D list of segments; each segment is a list of sentences
        """
        segments = []
        while stopless_sentences:
            longest_sentence = self.__fetch_longest_sentence(stopless_sentences)
            segment = [longest_sentence]
            for sentence in stopless_sentences:
                if sentence.similarity(longest_sentence) >= self.MIN_SIMILARITY:
                    segment.append(sentence)
                    stopless_sentences.remove(sentence)
            segments.append(segment)
        return segments

    def __fetch_longest_sentence(self, sentences):
        """
        Fetches the sentence with the maximum number of UNIQUE tokens.
        :param sentences: the list of sentences to search through
        :return: The sentence (A Doc object) with the maximum number of unique tokens
        """
        sentence_lengths_unique = [len(sentence.count_by(ORTH).keys()) for sentence in sentences]
        longest_sent_index = sentence_lengths_unique.index(max(sentence_lengths_unique))
        return sentences[longest_sent_index]

    def __fetch_segment_indexes(self, stopless_sentences):
        """
        This method iterates over the stopword-less sentences. As soon as it hits a sentence that goes below
        the similarity threshold, it notes the index of the dissimilar sentence. These indexes segment the
        sentence into paragraphs.
        :param stopless_sentences: the list of stopword-less sentence Span objects
        :return: a list of list indexes at which to segment the text (the indexes that begin a new paragraph)
        """
        segment_indexes = []
        segment_index = 0
        for index in range(1, len(stopless_sentences)):
            if stopless_sentences[segment_index].similarity(stopless_sentences[index]) < self.MIN_SIMILARITY:
                segment_indexes.append(index)
                segment_index = index

        return segment_indexes

    def __update_temporal_segments(self, segment_indexes):
        """
        Adds a new key to the segments dictionary: the temporal segment number.
        :param segment_indexes: The indexes of the action items list to change segment numbers
        """
        segment_counter = 0
        sentence_counter = 0
        for item in self.segments:
            item.update({'temporal_segment': segment_counter})
            sentence_counter += 1
            if sentence_counter in segment_indexes:
                segment_counter += 1

    def __update_non_temporal_segments(self, segments):
        """
        Adds a new key to the segments dictionary: the non-temporal segment number.
        :param segments: The transcript, organised into segments.
        """
        for index in range(len(segments)):
            for sentence in segments[index]:
                next(item for item in self.segments if item['stopless_sentence'] == sentence)\
                    .update({'non_temporal_segment': index})
