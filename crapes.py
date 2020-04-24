import re
import os
import time
import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Crapes():

    def __init__(self):
        self.session = requests.Session()
        self.result = []
        self.total = []
        with open('capres.csv') as f:
             self.records = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

    def save_to_csv(self, result):
        keys = result[0].keys()
        with open('new_capres.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(result)
    def scrape(self):
        for record in self.records:
            self.url = record["origurl"].strip()
            print(self.url)
            headers= {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
            response = self.session.get(self.url,headers=headers,timeout = 20)
            #print(self.url)
            soup = BeautifulSoup(response.content, "lxml")
            table = soup.find("table", {"class":"featured-grid"})
            all_tr = table.findAll("tr")
            data = {}
            for all_td in all_tr:
                All = all_td.findAll("td" )
                
                exempt_keys1 = All[0].text.strip() 
                exempt_values1 = All[1].text.strip()
                exempt_keys2 =  All[2].text.strip()
                exempt_values2 = All[3].text.strip()
                
                data[exempt_keys1] = exempt_values1

                data[exempt_keys2] = exempt_values2

            #print(data)
            try:
                date_time = soup.find("table", {"class":"property-timestamp"})
                items = date_time.findAll("tr")
                id_date = {}
                for item in items:
                    itms = item.findAll("td" )
                
                    key1  = itms[0].text.split(':')[0].strip()
                    value1 = itms[0].text.split(':')[1].strip()
                    id_date[key1] = value1

                    key2  = itms[1].text.split(':')[0].strip()
                    value2 = itms[1].text.split(':')[1].strip()
                    id_date[key2] = value2

                    key3  = itms[2].text.split(':')[0].strip()
                    value3 = itms[2].text.split(':')[1].strip()
                    id_date[key3] = value3
            except:
                date_time = soup.find("ul", {"class":"property-timestamp"})
                itms = date_time.findAll("li" )
                
                key1  = itms[0].text.split(':')[0].strip()
                value1 = itms[0].text.split(':')[1].strip()
                id_date[key1] = value1

                key2  = itms[1].text.split(':')[0].strip()
                value2 = itms[1].text.split(':')[1].strip()
                id_date[key2] = value2

                key3  = itms[2].text.split(':')[0].strip()
                value3 = itms[2].text.split(':')[1].strip()
                id_date[key3] = value3


            #print(id_date)

            div = soup.findAll("div", {"class":"column-12"})[18]
            descripion = div.text
            #print(descripion)

            tmp = {
                "origurl":self.url,
                "price":data.get("Price"),
                "commision_split":data.get("Commission Split"),
                "no_units":data.get("No. Units"),
                "gross_rent_multiplier":data.get("Gross Rent Multiplier"),
                "lot_size":data.get("Lot Size"),
                "occupancy":data.get("Occupancy"),
                "property_subtype":data.get("Property Subtype"),
                "additional_subtype":data.get("Additional Sub-types"),
                "property_use_type":data.get("Property Use Type"),
                "apn/parcel_id":data.get("APN / Parcel ID"),
                "year_built":data.get("Year Built"),
                "no_stories":data.get("No. Stories"),
                "parking_ratio":data.get("Parking Ratio"),
                "apartment_style":data.get("Apartment Style"),
                "listing_id":id_date.get("Listing ID"),
                "date_created":id_date.get("Date Created"),
                "last_updated":id_date.get("Last Updated"),
                "description":descripion
                }
            print(tmp)
            self.result.append(tmp)
            self.save_to_csv(self.result)

        return self.result
            

c = Crapes()
result = c.scrape()
print(result)
