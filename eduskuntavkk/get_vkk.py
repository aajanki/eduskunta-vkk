# Download "Vastaus kirjalliseen kysymykseen" metadata and documents
# from avoindata.eduskunta.fi

import json
import os
import os.path
import requests
import requests.exceptions
import shutil
import time
import xml.etree.ElementTree as ET
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


avoin_data_host = 'https://avoindata.eduskunta.fi'


def main():
    datadir = 'data'
    docdir = os.path.join(datadir, 'orig')
    metadata_filename = os.path.join(datadir, 'metadata.json')

    os.makedirs(docdir, exist_ok=True)

    metadata = get_metadata()
    json.dump(metadata, open(metadata_filename, 'w'))

    download_documents(metadata, docdir)


def download_documents(metadata, docdir):
    retry = Retry(total=3,
                  backoff_factor=0.5,
                  status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retry))
    session.mount('https://', HTTPAdapter(max_retries=retry))

    for i, x in enumerate(metadata):
        time.sleep(0.2)

        doc_id = x['id']
        destfile = os.path.join(docdir, doc_id + '.pdf')

        print(f'Downloading document {i+1}/{len(metadata)} {destfile}')
        try:
            save_as_file(x['url'], destfile, session)
        except requests.exceptions.RequestException as ex:
            print(ex)


def save_as_file(url, filename, session):
    with open(filename, 'wb') as f, \
         session.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        shutil.copyfileobj(r.raw, f)


def get_metadata():
    doc_type = 'Vastaus%20kirjalliseen%20kysymykseen'
    expected_columns = [
        'Id',
        'EduskuntaTunnus',
        'Päivämäärä',
        'NimekeTeksti',
        'AsiakirjatyyppiNimi',
        'Url',
        'Data',
        'Kielikoodi'
    ]
    page_num = 0
    has_more = True
    docs = []
    while has_more:
        print(f'Downloading metadata page {page_num + 1}')

        res = get_page(doc_type, page_num)
        page_num += 1 
        has_more = res.get('hasMore', False) == True

        assert res.get('columnNames', []) == expected_columns
        docs.extend(expand_metadata(parse_row(x)) for x in res.get('rowData', []))

    return docs


def get_page(doc_type, page_num):
    url = (f'{avoin_data_host}/api/v1/vaski/asiakirjatyyppinimi?'
           f'perPage=100&page={page_num}&filter={doc_type}&languageCode=fi')
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def parse_row(data):
    return {
        'id': data[0],
        'url': get_href(data[5]),
        'metadata_url': avoin_data_host + '/' + get_href(data[6]),
    }


def expand_metadata(data):
    metadata = get_document_metadata(data.get('metadata_url'))
    return {**data, **metadata}


def get_document_metadata(url):
    expected_columns = [
        'Id',
	'XmlData',
	'Status',
	'Created',
	'Eduskuntatunnus',
	'AttachmentGroupId',
	'Imported'
    ]
    
    r = requests.get(url)
    r.raise_for_status()
    metadata = r.json()
    assert metadata.get('columnNames', []) == expected_columns

    row_data = metadata.get('rowData')[0]
    data = parse_xml_data(row_data[1])
    data.update({'timestamp': row_data[3]})
    return data


def parse_xml_data(data):
    tag_path = (
        './/{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}'
        'AiheTeksti')
    position_path =(
        './/{http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15}'
        'AsemaTeksti')

    root = ET.fromstring(data)
    tags = [tag.text for tag in root.findall(tag_path)]
    position = [x.text for x in root.findall(position_path)][0]

    return {
        'position': position,
        'tags': tags,
    }


def get_href(atag):
    assert atag.startswith('<a href=')

    return atag[len('<a href='):].split('>', 1)[0].strip('"')


if __name__ == '__main__':
    main()
