import glob
import os.path
import subprocess


def main():
    docdir = 'data/orig/'
    outdir = 'data/text/'

    os.makedirs(outdir, exist_ok=True)

    for f in glob.glob(docdir + '*.pdf'):
        doc_id = os.path.splitext(os.path.basename(f))[0]
        output_name = os.path.join(outdir, doc_id + '.txt')

        try:
            text = extract_text(f)
            with open(output_name, 'w') as f:
                f.write(text)
        except subprocess.CalledProcessError as ex:
            print(ex)


def extract_text(pdffile):
    p = subprocess.run(['pdftotext', pdffile, '-'], capture_output=True,
                       encoding='utf-8', check=True)
    return p.stdout


if __name__ == '__main__':
    main()
