import glob
import os
import os.path
import subprocess
import tempfile
import sys


def main():
    docdir = 'data/orig/'
    outdir = 'data/text/'

    os.makedirs(outdir, exist_ok=True)

    for input_name in glob.glob(docdir + '*.pdf'):
        doc_id = os.path.splitext(os.path.basename(input_name))[0]
        output_name = os.path.join(outdir, doc_id + '.txt')

        if os.path.getsize(input_name) == 0:
            print(f'Skipping the empty file {input_name}')
            continue

        try:
            extract_text(input_name, output_name)

            if os.path.getsize(output_name) < 100:
                ocr_pdf(input_name, output_name)
        except subprocess.CalledProcessError as ex:
            print(ex)
        except FileNotFoundError as ex:
            print('A required external application missing?')
            print(ex)
            sys.exit(-1)


def extract_text(pdffile, outputfile):
    subprocess.run(['pdftotext', '-layout', pdffile, outputfile], check=True)


def ocr_pdf(pdffile, outputfile):
    f = tempfile.NamedTemporaryFile(suffix='.tiff', delete=False)
    try:
        f.close()

        subprocess.run(
            ['montage', '-density', '300', pdffile, '-mode', 'Concatenate',
             '-tile', '1x', '-depth', '8', f.name],
            check=True)

        assert outputfile.endswith('.txt')
        subprocess.run(
            ['tesseract', f.name, outputfile[:-len('.txt')], '-l', 'fin'],
            check=True)
    finally:
        os.remove(f.name)


if __name__ == '__main__':
    main()
