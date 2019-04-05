import codecs
import os
import os.path
import re
from nltk.tokenize import sent_tokenize


def main():
    datadir = 'data'
    outputdir = 'data/answers'
    sentencedir = 'data/sentences'

    os.makedirs(outputdir, exist_ok=True)
    os.makedirs(sentencedir, exist_ok=True)
    
    textdir = os.path.join(datadir, 'text')
    for textfile in os.listdir(textdir):
        full_path = os.path.join(textdir, textfile)

        if os.path.getsize(full_path) > 100:
            lines = codecs.open(full_path, encoding='utf-8').readlines()
            if detect_language(lines) == 'fi':
                text = cleanup_vkk(lines)
                with open(os.path.join(outputdir, textfile), 'w') as f:
                    f.write(text)

                sentences = sent_tokenize(text.replace('\n', ' '), 'finnish')
                with open(os.path.join(sentencedir, textfile), 'w') as f:
                    f.write('\n'.join(sentences))
            else:
                print(f'WARNING: Document {textfile} not in Finnish')


def detect_language(lines):
    if (lines[0].startswith('Svar på skriftligt spörsmål') or
        lines[0].startswith('Svar pä skriffligt spörsmäl')):
        return 'sv'
    elif lines[0].startswith('Vastaus kirjalliseen kysymykseen'):
        return 'fi'
    else:
        return 'unk'


def cleanup_vkk(lines):
    lines = [x.strip() for x in lines]
    
    header = lines[0]
    assert header.startswith('Vastaus kirjalliseen kysymykseen')

    lines = strip_lines(lines)
    lines = remove_headers(lines, header)
    lines = lines[(find_start_of_the_answer(lines) + 1):]
    lines = remove_signature(lines)
    lines = dehyphenate(lines)

    return '\n'.join(lines)


def find_start_of_the_answer(lines):
    for i, line in enumerate(lines):
        if (line == 'Vastauksena kysymykseen esitän seuraavaa:' or
            line == 'Vastauksena kysymykseen esitän seuraavaa'):
            return i

    raise ValueError('The start of answer not found')


def strip_lines(lines):
    i = 0
    while i < len(lines) and not lines[i]:
        i += 1

    j = len(lines) - 1
    while j >= 0 and not lines[j]:
        j -= 1

    return lines[i:(j+1)]


def remove_headers(lines, header):
    while True:
        try:
            i = lines.index(header)
        except ValueError:
            break

        first = i-1
        while first >= 0 and not lines[first]:
            first -= 1

        last = i+1
        while last < len(lines) and not lines[last]:
            last += 1

        lines = lines[:(first+1)] + lines[last:]

    return lines


def remove_signature(lines):
    if any(lines[-1].startswith(x) for x in ('LVM', 'MMM', 'Dnro')):
        lines = strip_lines(lines[:-1])

    lines = remove_ocr_noise_postfix_lines(lines)

    if any(x in lines[-1] for x in ('ministeri', 'minisi', 'misteri')):
        lines = strip_lines(lines[:-1])

    lines = remove_ocr_noise_postfix_lines(lines)

    if re.search(r'\d{1,2}(\. ?| päivänä )(\d{1,2}\.|\w+kuuta) ?\d{4}', lines[-1]):
        lines = strip_lines(lines[:-1])

    return lines


def remove_ocr_noise_postfix_lines(lines):
    while (lines and
           ((len(lines[-1]) < 3) or
            (len(lines[-1]) < 15 and any(x in lines[-1] for x in '^/\\')))):
        lines = strip_lines(lines[:-1])

    return lines


def dehyphenate(lines):
    hyphen = False
    res = []
    for line, next_line in zip(lines, lines[1:] + ['']):
        line2 = line[:-1] if line.endswith('-') else line

        if hyphen:
            res[-1] = res[-1] + line2
        else:
            res.append(line2)

        hyphen = line.endswith('-') and next_line

    return res


if __name__ == '__main__':
    main()
