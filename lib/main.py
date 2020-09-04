from lib.segmenter import Segmenter
from lib.utils import fix_text, filter_sentences, stringify_segments
from operator import itemgetter

print('this program exists')

WORKING_DIR = 'Enter your working directory here'
TRANSCRIPT_LOC = WORKING_DIR + 'data/boe_transcript.txt'

transcript_list = open(TRANSCRIPT_LOC, 'r').readlines()
transcript_list = fix_text(transcript_list, True)
print('text has been fixed')

segment = Segmenter(transcript_list)
segment.run_segmenter()
segmented_dict = segment.get_segments()
print('segmenter has segmented')

segmented_dict = filter_sentences(segmented_dict)
non_temporal_sort = sorted(segmented_dict, key=itemgetter('non_temporal_segment'))
stringified = stringify_segments(segmented_dict, segment_type='non_temporal_segment')

segmented_dict = segment.renumber_segments('temporal_segment', segmented_dict)
segmented_dict = segment.renumber_segments('non_temporal_segment', segmented_dict)

for item in segmented_dict:
    print(item)
