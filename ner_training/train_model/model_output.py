"""This module is used to create json files with the model output."""
import spacy
import json
from dotenv import load_dotenv
from pipeline.etl.transform import testing_model_, load_json


def load_data(file):
    with open(file, "r", encoding="utf-8") as training_file:
        data = json.load(training_file)
    return data


if __name__ == "__main__":
    load_dotenv()
    NLP_LG = spacy.load('en_core_web_lg')
    NLP_SKILLS = spacy.load("ner_training/output/model-best")
    # comp_salary = 'job101304099.html'
    # range_salary = 'job101290399.html'
    # fixed_salary = 'job101266908.html'
    # listing_data = get_listing_data("pipeline/etl", range_salary)
    skills = testing_model_('practise/data_use_this/london/listing')
    if skills:
        load_json(skills)
