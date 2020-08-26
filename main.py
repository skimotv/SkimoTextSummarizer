from detector import Detector
from segmenter import Segmenter
from utils import fix_text
from operator import itemgetter

print('this program exists')

WORKING_DIR = '/Users/ishita/PycharmProjects/action-item-detection/'
VERBS_LOC = WORKING_DIR + 'data/action_verbs.txt'
TRANSCRIPT_LOC = WORKING_DIR + 'data/boe_transcript.txt'

transcript_list = open(TRANSCRIPT_LOC, 'r').readlines()
transcript = fix_text(transcript_list)

print('text has been fixed')

with open('fixed.txt', 'w') as fixed:
    for sentence in transcript:
        fixed.write(sentence.text + "\n")

verbs = open(VERBS_LOC, 'r').readlines()
verbs = [verb.lower().replace('\n', '') for verb in verbs]  # cleans list


detect = Detector(verbs, transcript)
detect.run_detector()
action_items = detect.get_action_items()

print('detector has detected')

segment = Segmenter(action_items)
segment.run_segmenter()
action_items = segment.get_action_items()

print('segmenter has segmented')

action_items = sorted(action_items, key=itemgetter('segment'))
for item in action_items:
    print(item['sentence'], item['segment'])

