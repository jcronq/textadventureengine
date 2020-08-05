import json
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import text.textIO as text

prev_select_color = 'magenta'
number_color = 'yellow'
name_color = 'blue'
definition_color = 'white'

prompt_bg = 'green'
prompt_highlight = 'red'
block_size = 75

def annotate_synsets(sentence, previous_word_senses=None):
    cached_selections = {}
    if previous_word_senses is not None:
        word_senses = previous_word_senses
        for word, sense_obj in previous_word_senses.items():
            cached_selections[word] = sense_obj['selection']
    else:
        word_senses = {}

    words = word_tokenize(sentence)
    for word in words:
        synsets = wn.synsets(word)
        if len(synsets) != 0:
            selection = select_synset(sentence, word, synsets,
                                      cached_selections)
            if selection == 'quit':
                quit()
            if selection != None:
                cached_selections[word] = selection
                if selection < len(synsets):
                    s = synsets[selection]
                    word_senses[word] = {
                        'name':s.name(),
                        'selection': selection
                    }

    return word_senses

def select_synset(sentence, word, synsets, cached_selections):
    prompt = text.colorize('  '+sentence, prompt_bg, [
        {'word': word, 'color': prompt_highlight}
    ])

    options = []
    prev_selection = -1
    if word in cached_selections:
        prev_selection = cached_selections[word]

    for choice, s in enumerate(synsets):
        options.append(text.colorize(
            f"{s.name()}: {s.definition()}",
            definition_color if choice != prev_selection else prev_select_color,
            [
                {'word': f'{s.name()}:', 'color': name_color}
            ]))

    choice += 1
    options.append(text.colorize(
        f"None of the above.",
        definition_color if choice != prev_selection else prev_select_color,
        []))

    selection = text.getOption(
        prompt, options,
        default_selection = prev_selection,
        block_size = block_size,
        numeral_color = number_color)
    return selection

def confirm_hyponyms(word, synset, do_hypernyms_instead=False):
    prompt = word

    confirmed = []
    if do_hypernyms_instead:
        unconfirmed = synset.hypernyms()
    else:
        unconfirmed = synset.hyponyms()

    while len(unconfirmed) > 0:
        s = unconfirmed.pop(0)
        print(f"Is {s.name()} an appropriate substitute for {word}? (y/n)")
        print("It means:", s.definition())
        print("Synonyms are:", get_synonyms(s))
        if text.getYesNo():
            confirmed.append(s.name())
            if do_hypernyms_instead:
                unconfirmed.extend(s.hypernyms())
            else:
                unconfirmed.extend(s.hyponyms())

    return confirmed

def get_synonyms(word_sense):
    synonyms = []
    for lemma in word_sense.lemmas():
        synonym = lemma.name().replace('_', ' ')
        synonyms.append(synonym)
    return synonyms

