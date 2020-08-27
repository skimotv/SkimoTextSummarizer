from detector import Detector
from segmenter import Segmenter
from utils import fix_text, filter_sentences
from operator import itemgetter

print('this program exists')

WORKING_DIR = '/Users/ishita/PycharmProjects/action-item-detection/'
VERBS_LOC = WORKING_DIR + 'data/action_verbs.txt'
TRANSCRIPT_LOC = WORKING_DIR + 'data/boe_transcript.txt'

transcript_list = open(TRANSCRIPT_LOC, 'r').readlines()
transcript_list = fix_text(transcript_list)

print('text has been fixed')

with open('fixed.txt', 'w') as fixed:
    for sentence in transcript_list:
        fixed.write(sentence.text + "\n")

verbs = open(VERBS_LOC, 'r').readlines()
verbs = [verb.lower().replace('\n', '') for verb in verbs]  # cleans list

segment = Segmenter(transcript_list)
segment.run_segmenter()
temporal_segments = segment.get_temporal_segments()
non_temporal_segments = segment.get_non_temporal_segments()

print('segmenter has segmented')

temporal_segments = filter_sentences(temporal_segments)
non_temporal_segments = filter_sentences(non_temporal_segments)

# detect = Detector(verbs, transcript_list)
# detect.run_detector()
# action_items = detect.get_action_items()
#
# print('detector has detected')



