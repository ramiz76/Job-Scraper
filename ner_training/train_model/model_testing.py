"""This module is used to create json files with the model output."""
import spacy
import json


def load_data(file):
    with open(file, "r", encoding="utf-8") as training_file:
        data = json.load(training_file)
    return data


if __name__ == "__main__":
    nlp = spacy.load("output/model-best")
    test_data = load_data("data/formal_test.json")
    text_doc = nlp(test_data[0][0])
    for ent in text_doc.ents:
        print(ent.text, ent.label_)
