# Split the documents into sentences and divide the sentences into
# train, dev and test datasets

import codecs
import json
import os
import os.path
import re
import pandas as pd
import numpy as np
import nltk.data
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split


def main():
    num_sentences_dev = 3000
    num_sentences_test = 3000
    datadir = 'data'
    textdir = 'data/answers'
    outputdir = 'vkk'

    metadata = load_metadata(os.path.join(datadir, 'metadata.json'))
    ministries = get_ministry(metadata)
    tokenizer = load_sent_tokenizer()

    sentences = []
    ys = []
    for textfile in os.listdir(textdir):
        doc_id = textfile.split('.')[0]
        y = ministries[doc_id]
        assert y, f'Ministry missing on document {doc_id}'

        full_path = os.path.join(textdir, textfile)
        lines = codecs.open(full_path, encoding='utf-8').readlines()
        text = ' '.join(x.strip() for x in lines)
        doc_sentences = tokenize_sentences(tokenizer, text)

        sentences.extend(doc_sentences)
        ys.extend([y]*len(doc_sentences))

    all_sentences = pd.DataFrame({'sentence': sentences, 'ministry': ys})
    # drop a rare class
    all_sentences = all_sentences[all_sentences['ministry'] !=
                                  'Kulttuuri- ja asuntoministeri']
    all_sentences = all_sentences.drop_duplicates('sentence')

    temp, df_test = train_test_split(all_sentences, test_size=num_sentences_test,
                                     random_state=42)
    df_train, df_dev = train_test_split(temp, test_size=num_sentences_dev,
                                        random_state=43)

    token_counts = [len(word_tokenize(x)) for x in all_sentences['sentence']]
    median_num_tokens = np.median(token_counts)
    max_num_tokens = np.max(token_counts)

    print('Train data')
    print(summarize(df_train))
    print()
    print(f'Number of train sentences: {len(df_train)}')
    print()
    print('Dev data')
    print(summarize(df_dev))
    print()
    print(f'Number of dev sentences: {len(df_dev)}')
    print()
    print('Test data')
    print(summarize(df_test))
    print()
    print(f'Number of test sentences: {len(df_test)}')
    print()
    print(f'Median tokens per sentence: {median_num_tokens}')
    print(f'Max tokens per sentence: {max_num_tokens}')

    os.makedirs(outputdir, exist_ok=True)
    df_train.to_csv(os.path.join(outputdir, 'train.csv.bz2'), index=False)
    df_dev.to_csv(os.path.join(outputdir, 'dev.csv.bz2'), index=False)
    df_test.to_csv(os.path.join(outputdir, 'test.csv.bz2'), index=False)


def summarize(df):
    return (df.groupby('ministry')
     .size()
     .sort_values(ascending=False)
     .to_string())


def load_metadata(filename):
    return {x['id']: x for x in json.load(open(filename))}


def get_ministry(metadata):
    merged = {
        # Merge the ministries that were split during the Sipilä Cabinet
        'oikeusministeri': 'oikeus- ja työministeri',
        'työministeri': 'oikeus- ja työministeri',
        'asunto-, energia- ja ympäristöministeri': 'maatalous- ja ympäristöministeri',
        'maa- ja metsätalousministeri': 'maatalous- ja ympäristöministeri',
        'opetusministeri': 'opetus- ja kulttuuriministeri',

        # Aliases
        'ulkoasiainministeri': 'ulkoministeri',
    }
    return {k: merged.get(v['position'], v['position'])
            for (k, v) in metadata.items()}


def tokenize_sentences(tokenizer, text):
    return [
        ' '.join(word_tokenize(sent, 'finnish', True))
        for sent in tokenizer.tokenize(text, 'finnish')
    ]


def load_sent_tokenizer():
    # Add some common abbreviations that are missing form the nltk
    # Finnish PunctTokenizer (Apr 2019).
    abbrev = [
        'jälj', 'ko', 'ks', 'ml', 'mm', 'mrd', 'n', 'pl', 's', 'v', 'vs', 'ym'
    ]

    tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
    tokenizer._params.abbrev_types.update(abbrev)
    return tokenizer


if __name__ == '__main__':
    main()
