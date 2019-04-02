# Download "Vastaus kirjalliseen kysymykseen" metadata from
# avoindata.eduskunta.fi

import json
import requests
import xml.etree.ElementTree as ET


avoin_data_host = 'http://avoindata.eduskunta.fi'


def get_documents():
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
    metadata = get_metadata(data.get('metadata_url'))
    return {**data, **metadata}


def get_metadata(url):
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

    xml_data = metadata.get('rowData', [])[0][1]
    return parse_xml_data(xml_data)

    
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
    print(json.dumps(get_documents()))
