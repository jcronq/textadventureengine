import src.core.train as train
import json
from nltk.corpus import wordnet as wn

annotation_file = './.data/command.annotations'
hypernyms_file = './.data/command.hypernyms'
hyponyms_file = './.data/command.hyponyms'

try:
    with open(annotation_file, 'r') as f:
        previous_synsets = json.loads(f.read())
except:
    previous_synsets = {}
confirmed_hyponyms = {}
confirmed_hypernyms = {}

sentence = "take move attack use examine"
annotations = train.annotate_synsets(sentence, previous_synsets)

with open(annotation_file, 'w') as f:
    f.write(json.dumps(annotations))

for word in annotations:
    word_sense = wn.synset(annotations[word]['name'])
    confirmed_hypernyms[word] = train.confirm_hyponyms(word, word_sense,
                                                 do_hypernyms_instead = True)
    confirmed_hyponyms[word] = train.confirm_hyponyms(word, word_sense,
                                                 do_hypernyms_instead = False)

with open(hypernyms_file, 'w') as f:
    f.write(json.dumps(confirmed_hypernyms))

with open(hyponyms_file, 'w') as f:
    f.write(json.dumps(confirmed_hyponyms))
