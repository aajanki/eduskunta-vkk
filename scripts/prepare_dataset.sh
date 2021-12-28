#!/bin/sh

# Download "vastaukset kirjallisiin kysymyksiin" dataset from
# avoindata.eduskunta.fi, extract the sentences and split them into
# train, dev and test datasets.
#
# The dataset will be saved in the subdirectroy vkk.
#
# Original documents and intermediate formats will be saved in the
# subdirectory data.

set -eu

python3 -m nltk.downloader punkt

python3 eduskuntavkk/get_vkk.py
python3 eduskuntavkk/extract_text.py
python3 eduskuntavkk/cleanup_vkk.py
python3 eduskuntavkk/fix_metadata.py
python3 eduskuntavkk/prepare_train_test.py
