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

verbs = open(VERBS_LOC, 'r').readlines()
verbs = [verb.lower().replace('\n', '') for verb in verbs]  # cleans list

segment = Segmenter(transcript_list)
segment.run_segmenter()
segmented_dict = segment.get_segments()
print('segmenter has segmented')

segmented_dict = filter_sentences(segmented_dict)
non_temporal_sort = sorted(segmented_dict, key=itemgetter('non_temporal_segment'))
stringified = stringify_segments(segmented_dict, segment_type='non_temporal_segment')

for item in segmented_dict:
    print(item)

# create a function in segmenter to re-number the segments

# detect = Detector(verbs, transcript_list)
# detect.run_detector()
# action_items = detect.get_action_items()
# print('detector has detected')
#
# for item in action_items:
#     print(item)
