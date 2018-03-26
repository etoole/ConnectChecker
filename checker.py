import csv, requests, re
from bs4 import BeautifulSoup

CONNECTNY_URL = 'https://www.connectny.info/search~S0/'
isbd_grabber = re.compile('[0-9X]{10}')

#OPEN LIST, READ CSV AS DICTIONARY W/ "~" DELIMITER
with open('NoCirc_test.csv', 'r+') as data:
    no_circ = csv.DictReader(data, delimiter="~")
    with open('NoCirc_test_output.csv', 'w') as output:
        fieldnames = ['Record Number','Publication Info.','Call No.','Horizon checkouts','Old in-house uses','Checkout Date','Standard No.','Title','CNY']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

    #LOOP THROUGH EACH RECORD. DEFINE ISBD & 245 VARIABLE USING DICTIONARY KEYNAME(NAME OF COLUMN)
        for record in no_circ:
            # print(record)
            isbd = None
            marc245 = None
            library_name_list = []

            isbd = record['Standard No.']
            isbd_list = re.findall(isbd_grabber, isbd)

            marc245 = record['Title']
            # print(isbd)
            # print(marc245)

##BEGIN ISBD SEARCH
            for isbd in isbd_list:

                if isbd != "":
                    # print(isbd)

                    isbd_params = {
                                'searchtype': 'i',
                                'searcharg': isbd}

                    isbd_req = requests.get(CONNECTNY_URL, isbd_params)
                    # print(isbd_req)
                    # print(isbd_req.text)
                    # print(isbd_req.url)
                    isbd_soup = BeautifulSoup(isbd_req.text, 'html.parser')

                    #CHECK FOR NEGATIVE RESULT
                    isbd_no_matches_found = isbd_soup.body.find('tr', {'class':'msg'})
                    # print(isbd_no_matches_found)

                    #CHECK FOR INDIVIDUAL POSITIVE RESULT
                    if isbd_no_matches_found == None:
                        isbd_request_this_item = isbd_soup.body.find('a', id='__requestItem')
                        # print(isbd_request_this_item.text)
                        if isbd_request_this_item != None:
                            if isbd_request_this_item.text == 'REQUEST THIS ITEM':
                                # print(isbd_request_this_item.text)
                                isbd_lenders_table = isbd_soup.body.find('table', {'bgcolor':"#DDEEFF"})
                                isbd_lender_rows = isbd_lenders_table.findAll('tr')

                                #CREATE LIST OF LENDER NAMES OTHER THAN PRATT
                                for row in isbd_lender_rows:
                                    library = row.find('td')
                                    if library != None:
                                        library_name = library.get_text()
                                        # print(library_name)
                                        # print('\n')
                                        if library_name != 'Pratt':
                                            library_name_list.append(library_name)
                                # print(library_name_list)

                                #IF LENDERS OTHER THAN PRATT, ADD 'CNY': 'X' TO CSV
                                if len(library_name_list) > 0:
                                    # print(library_name_list[0])
                                    record['CNY'] = 'X'
                                elif len(library_name_list) == 0:
                                    record['CNY'] = 'ONLY PRATT'



                        #CHECK FOR MULTIPLE POSITIVE RESULT



##BEGIN MARC 245 SEARCH
            if record['CNY'] != 'X':
                marc245_params = {
                            'searchtype': 't',
                            'searcharg': marc245
                }

                marc_req = requests.get(CONNECTNY_URL, marc245_params)
                # print(marc_req)
                # print(marc_req.text)
                print(marc_req.url)
                marc_soup = BeautifulSoup(marc_req.text, 'html.parser')

                #CHECK FOR NEGATIVE RESULT
                marc_no_matches_found = marc_soup.body.find('tr', {'class':'msg'})
                # print(marc_no_matches_found)

                #CHECK FOR INDIVIDUAL POSITIVE RESULT
                if marc_no_matches_found == None:
                    marc_request_this_item = marc_soup.body.find('a', id='__requestItem')
                    # print(marc_request_this_item.text)
                    if marc_request_this_item != None:
                        if marc_request_this_item.text == 'REQUEST THIS ITEM':
                            # print(marc_request_this_item.text)
                            marc_lenders_table = marc_soup.body.find('table', {'bgcolor':"#DDEEFF"})
                            marc_lender_rows = marc_lenders_table.findAll('tr')

                            #CREATE LIST OF LENDER NAMES OTHER THAN PRATT
                            for row in marc_lender_rows:
                                library = row.find('td')
                                if library != None:
                                    library_name = library.get_text()
                                    # print(library_name)
                                    # print('\n')
                                    if library_name != 'Pratt':
                                        library_name_list.append(library_name)
                            # print(library_name_list)

                            #IF LENDERS OTHER THAN PRATT, ADD 'CNY': 'X' TO CSV
                            if len(library_name_list) > 0:
                                print(library_name_list[0])
                                record['CNY'] = 'X'
                            elif len(library_name_list) == 0:
                                record['CNY'] = 'ONLY PRATT'











            writer.writerow(record)


        #!! ADD 'CNY':'X'


                                # for row in isbd_lender_rows:
                                #     isbd_lender_name = row['td']
                                #     print(isbd_lender_name)
        #!! INSERT 'CNY': 'X'
                            # elif
