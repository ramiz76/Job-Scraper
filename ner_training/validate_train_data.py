import json


def load_data(file):
    with open(file, "r", encoding="utf-8") as training_file:
        data = json.load(training_file)
    return data


def validate_training_data(data: list[list]):
    for example in data:
        text = example[0]
        entities = example[1]['entities']
        if entities:
            for entity in entities:
                print(text[entity[0]:entity[1]])


if __name__ == "__main__":
    training_data = load_data("data/testing_data.json")
    validate_training_data(training_data)
