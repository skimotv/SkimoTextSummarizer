from detector import Detector
from segmenter import Segmenter
from utils import fix_text, filter_sentences, stringify_segments
from operator import itemgetter

print('this program exists')

WORKING_DIR = '/Users/ishita/PycharmProjects/action-item-detection/'
VERBS_LOC = WORKING_DIR + 'data/action_verbs.txt'
TRANSCRIPT_LOC = WORKING_DIR + 'data/boe_transcript.txt'

transcript_list = open(TRANSCRIPT_LOC, 'r').readlines()
transcript_list = fix_text(transcript_list, True)

print('text has been fixed')

# verbs = open(VERBS_LOC, 'r').readlines()
# verbs = [verb.lower().replace('\n', '') for verb in verbs]  # cleans list

segment = Segmenter(transcript_list)
segment.run_segmenter()
temporal_segments = segment.get_temporal_segments()
non_temporal_segments = segment.get_non_temporal_segments()

print('segmenter has segmented')

temporal_segments = filter_sentences(temporal_segments)
non_temporal_segments = filter_sentences(non_temporal_segments)
non_temporal_segments = sorted(non_temporal_segments, key=itemgetter('segment'))

segments = stringify_segments(non_temporal_segments)

for segment in segments:
    print(segment)

print('')
print('')
print('')

for segment in non_temporal_segments:
    print(segment)

# detect = Detector(verbs, transcript_list)
# detect.run_detector()
# action_items = detect.get_action_items()
#
# print('detector has detected')
