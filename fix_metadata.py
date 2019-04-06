import json
import os.path


def main(metadata_filename, textdir):
    with open(metadata_filename) as f:
        metadata = json.load(f)

    metadata = fix_missing_position_metadata(metadata, textdir)

    with open('data/metadata.json', 'w') as f:
        json.dump(metadata, f)


def fix_missing_position_metadata(metadata, textdir):
    fixed_metadata = []
    for doc in metadata:
        if doc.get('position') is None:
            doc['position'] = get_ministry_from_text(textdir, doc['id'])

        fixed_metadata.append(doc)

    return fixed_metadata


def get_ministry_from_text(textdir, doc_id):
    with open(os.path.join(textdir, doc_id + '.txt')) as f:
        lines = [x.strip() for x in f.readlines()]
        ministry = extract_ministry(lines)
        assert ministry, f'Failed to extract ministry from doc {doc_id}'

        return ministry


def extract_ministry(lines):
    for line in reversed(lines[-5:]):
        i = line.find('ministeri')
        if i > 0:
            return line[:(i + len('ministeri'))].lower()

        i = line.find('mmisteri')
        if i > 0:
            return (line[:(i + len('mmisteri'))]
                    .lower()
                    .replace('mmisteri', 'ministeri'))

    return None


if __name__ == '__main__':
    main('data/metadata.json', 'data/text')
