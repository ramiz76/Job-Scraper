from spacy.tokens import DocBin
import spacy
import json
from tqdm import tqdm


def load_data(file):
    with open(file, "r", encoding="utf-8") as training_file:
        data = json.load(training_file)
    return data


def create_training(TRAINING_DATA):
    db = DocBin()
    for text, skills in tqdm(TRAINING_DATA):
        doc = nlp(text)
        ents = []
        for start, end, label in skills["entities"]:
            char_span = doc.char_span(start, end, label=label,
                                      alignment_mode="contract")
            if char_span is None:
                print("Entity skipped")
            else:
                ents.append(char_span)
        doc.ents = ents
        db.add(doc)
    return db


if __name__ == "__main__":

    training_data = load_data('training_data.json')
    verifying_data = load_data('verifying_data.json')
    nlp = spacy.blank("en")

    skills_train = create_training(training_data)
    skills_train.to_disk("skills_train.spacy")

    skills_verify = create_training(verifying_data)
    skills_verify.to_disk("skills_verify.spacy")
