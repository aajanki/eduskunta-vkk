import os
import os.path
import re

number_word_re = re.compile(r'(\b\d{2,})([^\d\s:/-]{3,})\b')


def main():
    datadir = 'data'
    outputdir = 'data/answers'

    os.makedirs(outputdir, exist_ok=True)

    textdir = os.path.join(datadir, 'text')
    for textfile in os.listdir(textdir):
        full_path = os.path.join(textdir, textfile)

        if os.path.getsize(full_path) > 100:
            lines = open(full_path, encoding='utf-8').readlines()
            lang, doctype = detect_language_and_doctype(lines)
            if lang == 'fi' and doctype == 'answer':
                try:
                    text = cleanup_vkk(lines)
                except Exception as ex:
                    print(f'Failed to cleanup {full_path}: {str(ex)}')
                with open(os.path.join(outputdir, textfile), 'w') as f:
                    f.write(text)
            elif lang == 'fi':
                print(f'Document {textfile} is not an answer')
            else:
                print(f'Document {textfile} not in Finnish')


def detect_language_and_doctype(lines):
    line = lines[0].strip()
    if (line.startswith('Svar på skriftligt spörsmål') or
        line.startswith('Svar pä skriffligt spörsmäl')):
        return ('sv', 'answer')
    elif line.startswith('Vastaus kirjalliseen kysymykseen'):
        return ('fi', 'answer')
    elif line.startswith('Kirjallinen kysymys'):
        return ('fi', 'question')
    else:
        return ('unk', 'unk')


def cleanup_vkk(lines):
    lines = [x.strip() for x in lines]
    
    header = lines[0]
    assert header.startswith('Vastaus kirjalliseen kysymykseen')

    lines = strip_lines(lines)
    lines = remove_headers(lines, header)
    lines = lines[(find_start_of_the_answer(lines) + 1):]
    lines = remove_signature(lines)
    lines = dehyphenate(lines)
    lines = [fix_number_word_separators(x) for x in lines]

    return '\n'.join(lines)


def find_start_of_the_answer(lines):
    for i, line in enumerate(lines):
        if (line == 'Vastauksena kysymykseen esitän seuraavaa:' or
            line == 'Vastauksena kysymykseen esitän seuraavaa'):
            return i

    # Can't recognize the start of the answer. Try to find the start
    # of the question instead.
    for i, line in enumerate(lines[:10]):
        if 'kirjallisen kysymyksen' in line:
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

        hyphen = (line.endswith('-') and
                  len(line) >= 2 and
                  not line[-2].isdigit() and
                  next_line)

    return res


def fix_number_word_separators(line):
    """Add space between numbers and string
    For example: 2020luvulle -> 2020 luvulle
    """
    return number_word_re.sub(r'\1 \2', line)


if __name__ == '__main__':
    main()
