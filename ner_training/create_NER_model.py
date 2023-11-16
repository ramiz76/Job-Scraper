"""This module converts the json training files into .spacy files for model training."""
import random
import json
from spacy.tokens import DocBin
import spacy


def load_data(file):
    with open(file, "r", encoding="utf-8") as training_file:
        data = json.load(training_file)
    return data


def create_training(TRAINING_DATA):
    db = DocBin()
    for i in range(30):
        random.shuffle(TRAINING_DATA)
        for text, skills in (TRAINING_DATA):
            doc = nlp(text)
            ents = []
            for start, end, label in skills["entities"]:
                char_span = doc.char_span(start, end, label=label,
                                          alignment_mode="contract")
                if char_span is None:
                    print(f"{text} skipped")
                else:
                    ents.append(char_span)
            try:
                doc.ents = ents
                db.add(doc)
            except:
                print(doc)
    return db


if __name__ == "__main__":

    training_data = load_data('data/training_data.json')
    verifying_data = load_data('data/verifying_data.json')
    nlp = spacy.blank("en")

    skills_train = create_training(training_data)
    skills_train.to_disk("data/skills_train.spacy")

    skills_verify = create_training(verifying_data)
    skills_verify.to_disk("data/skills_verify.spacy")
