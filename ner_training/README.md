train_file_conversion.py was used to convert the training and verifying data json files into .spacy files that can be processed by the training model

run `python3 create_NER_model.py` to create the spacy files to train the model 
train/dev should be pointing to the correct file paths for both training data files
use `python3 -m spacy init fill-config base_config.cfg config.cfg` to fill in the remaining defaults of the base_config.cfg file
train model from data in config using `python3 -m spacy train config.cfg --output ./output`