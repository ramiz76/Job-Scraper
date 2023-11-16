"""This module is used to create new training data from from the current outputs of the model (to be manually reviewed)."""
import json


def open_json(file):
    with open(file, 'r') as f:
        data = f.read()
    return json.loads(data)


def load_json(file, processed_data):
    current_data = open_json(file)
    current_data.extend(processed_data)
    with open(file, 'w') as f:
        json.dump(current_data, f, indent=4)


def create_training_data(input: list):
    for example in input:
        text = example[0]
        entities = example[1]["entities"]
        for i, entity in enumerate(entities):
            st_index = text.find(entity[0])
            en_index = st_index + len(entity[0])
            example[1]["entities"][i] = [st_index, en_index, entity[1]]
    return input


if __name__ == "__main__":
    raw_file = 'ner_training/train_model/raw_data.json'
    training_file = 'ner_training/train_model/verifying_data.json'
    raw_data = open_json(raw_file)
    processed_data = create_training_data(raw_data)
    load_json(training_file, processed_data)
