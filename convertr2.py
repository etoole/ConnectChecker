import csv, requests, re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

WORLDCAT_URL = 'http://www.worldcat.org/webservices/catalog/content/libraries/'
pratt_location_number = '43017'

non_pratt_cny_members_list = ['VJA','VVP','YSR','VVPCS','VKC','VVC','YHM','VFL','XMA','MEDCL','YJT','VZL','VZW','VZP','VZU','YRM','RVE','XLM',
'VKM','VZS','ZWU','NYUGC','ADW','VYM','YWM','VXW']

non_pratt_cny_members = {
'Adelphi University' : 'VJA',
'Bard College - Charles P. Stevenson Library' : 'VVP',
"Bard College at Simon's Rock Alumni Library" : 'YSR',
'Bard College - Center for Curatorial Studies Library and Archives' : 'VVPCS',
'Canisius College' : 'VKC',
'Colgate University' : 'VVC',
'Hamilton College' : 'YHM',
'Le Moyne College' : 'VFL',
'Marist College' : 'XMA',
'Medaille College - Rochester Accel Program' : 'MEDCL',
'Medaille College' : 'YJT',
'Pace University, Law Library' : 'VZL',
'Pace University - College of White Plains' : 'VZW',
'Pace University New York - Henry Birnbaum Library' : 'VZP',
'Pace University, Pleasantville - Edward & Doris Mortola Library' : 'VZU',
'Rensselaer Polytechnic Institute' : 'YRM',
'Rochester Institute of Technology' : 'RVE',
'St. Lawrence University' : 'XLM',
'Siena College' : 'VKM',
'Skidmore College' : 'VZS',
'Union College' : 'ZWU',
'Union Graduate College' : 'NYUGC',
'Adirondack Research Library of Union College' : 'ADW',
'United States Merchant Marine Academy': 'VYM',
'United States Military Academy' : 'YWM',
'Vassar College' : 'VXW'
}

with open('noCirc_oclcNumber', 'r+') as data:
    no_circ = csv.DictReader(data, delimiter="~")

    with open('NoCirc_output_worldcat.csv', 'w') as output:
        fieldnames = ['Record Number','Publication Info.','Call No.','Horizon checkouts','Old in-house uses','Checkout Date','Standard No.', 'OCLC Number','Title','CNY']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for record in no_circ:
            holders_list = []

            # print(record)
            # isbd = None
            # marc245 = None
            library_name_list = []

            oclc_number = record['OCLC Number']
            # print(isbd)
            # print(marc245)

            if oclc_number != "":
                worldcat_request = requests.get(WORLDCAT_URL + oclc_number + "?location=" + pratt_location_number + WSKEY)
                # print(worldcat_request.text)
                if worldcat_request.status_code != 200:
                    print(worldcat_request.text)
                    root = ET.fromstring(worldcat_request.text)
                    holding = root.findall('holding')
                    print(holding)
                    for holding_child in holding:
                        institution_id = holding_child.findall('institutionIdentifier')
                        for item in institution_id:
                            for value in item.findall('value'):
                                for cny_member in non_pratt_cny_members_list:
                                    if cny_member == value.text:
                                        holders_list.append(value.text)

                    print(holders_list)
