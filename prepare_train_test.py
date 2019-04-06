import codecs
import json
import os
import os.path
import re
import pandas as pd
from nltk.tokenize import sent_tokenize
from sklearn.model_selection import train_test_split


def main():
    datadir = 'data'
    textdir = 'data/answers'
    outputdir = 'vkk'

    metadata = load_metadata(os.path.join(datadir, 'metadata.json'))
    ministries = get_ministry(metadata)

    sentences = []
    ys = []
    for textfile in os.listdir(textdir):
        doc_id = textfile.split('.')[0]
        y = ministries[doc_id]
        assert y, f'Ministry missing on document {doc_id}'

        full_path = os.path.join(textdir, textfile)
        lines = codecs.open(full_path, encoding='utf-8').readlines()
        text = ' '.join(x.strip() for x in lines)
        doc_sentences = tokenize_sentences(text)

        sentences.extend(doc_sentences)
        ys.extend([y]*len(doc_sentences))

    X_temp, X_test, Y_temp, Y_test = train_test_split(
        sentences, ys, test_size=500, random_state=42)
    X_train, X_dev, Y_train, Y_dev = train_test_split(
        X_temp, Y_temp, test_size=500, random_state=42)

    df_train = pd.DataFrame({'sentence': X_train, 'ministry': Y_train})
    df_dev = pd.DataFrame({'sentence': X_dev, 'ministry': Y_dev})
    df_test = pd.DataFrame({'sentence': X_test, 'ministry': Y_test})

    print('Train data')
    print(summarize(df_train))
    print()
    print('Dev data')
    print(summarize(df_dev))
    print()
    print('Test data')
    print(summarize(df_test))

    os.makedirs(outputdir, exist_ok=True)
    df_train.to_csv(os.path.join(outputdir, 'train.csv'), index=False)
    df_dev.to_csv(os.path.join(outputdir, 'dev.csv'), index=False)
    df_test.to_csv(os.path.join(outputdir, 'test.csv'), index=False)


def summarize(df):
    return (df.groupby('ministry')
     .size()
     .sort_values(ascending=False)
     .to_string())


def load_metadata(filename):
    return {x['id']: x for x in json.load(open(filename))}


def get_ministry(metadata):
    merged = {
        # Merge the divided ministries
        'oikeusministeri': 'oikeus- ja työministeri',
        'työministeri': 'oikeus- ja työministeri',
        'asunto-, energia- ja ympäristöministeri': 'maatalous- ja ympäristöministeri',
        'maa- ja metsätalousministeri': 'maatalous- ja ympäristöministeri',
        'ulkoasiainministeri': 'ulkoministeri',
        'opetusministeri': 'opetus- ja kulttuuriministeri',

        # Merge smallest classes to the nearest sensible class
        'puolustusministeri': 'sisäministeri',
        'kunta- ja uudistusministeri': 'valtiovarainministeri',
    }
    return {k: merged.get(v['position'], v['position'])
            for (k, v) in metadata.items()}


def tokenize_sentences(text):
    return [
        ' '.join(x.strip() for x in re.split(r'\b', sent) if x.strip())
        for sent in sent_tokenize(text, 'finnish')
    ]


if __name__ == '__main__':
    main()
