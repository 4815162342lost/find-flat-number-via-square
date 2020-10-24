#!/usr/bin/python3
import requests
import time
import random
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--min_flat_number", type=str, required=True, help="minimum flat number")
parser.add_argument("-n", "--max_flat_number", type=str, required=True, help="maximiun flat number")
parser.add_argument("-n", "--max_flat_number_in_entrance", type=str, required=True, help="maximiun flat number in first entrance")
parser.add_argument("-s", "--floors_number", type=str, required=True, help="number of floors on house (9 or 17 on typical russian houses)")
parser.add_argument("-z", "--flats_in_floor", type=str, required=True, help="number of flats on floor (4 in 9th floors old houses)")
parser.add_argument("-c", "--main_kadastr_num", type=str, required=True, help="kadastr number without last 4 numbers")
parser.add_argument("-b", "--min_last_kadastr_num", type=str, required=True, help="minimum number of last 4 numbers in kadastr")
parser.add_argument("-n", "--max_last_kadastr_num", type=str, required=True, help="maximum number of last 4 numbers in kadastr")
parser.add_argument("-p", "--min_area", type=str, required=True, help="min area of apartments")
parser.add_argument("-o", "--max_area", type=str, required=True, help="max area of apartments")
parser.add_argument("-i", "--street_name", type=str, required=True, help="full street name")
args=parser.parse_args()

approved_flats=[]

while args.max_flat_number_in_entrance<=args.max_flat_number+1:
    for i in range(args.min_flat_number, args.max_flat_number_in_entrance+1):
        approved_flats.append(i)
    args.min_flat_number=args.min_flat_number+args.floors_number*args.flats_in_floor; args.max_flat_number_in_entrance=args.max_flat_number_in_entrance+args.min_flat_number+args.floors_number*args.flats_in_floor

logs=open('/tmp/1.log', 'a')

def check_flat(number, exception_count=0, e=None, json_e=None):
    try:
        if exception_count>1:
            print(f"Error with number {number}, exceprion: {e}, json: {json_e}")
            return 0
        r=requests.post("https://www.avito.ru/web/1/domoteka/previewReport", json={'key' : '16:50:110805:' + str(number)}, headers={"user-agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0"} )
        rj=json.loads(r.text)
        logs.write(str(rj)+"\n")
        logs.flush()
        if "Республика Татарстан, г Казань, пр-кт Ямашева, д 78" in rj['result']['address'] and 34>rj['result']['area']>32:
            for i in approved_flats:
                if rj['result']['address'].endswith("кв " + str(i)):
                    print(f"Address: {rj['result']['address']}; Area: {rj['result']['area']} м²")
    except Exception as e:
        exception_count+=1
        time.sleep(random.randint(8,15))
        check_flat(number,exception_count, e, rj)

for i in range(3011,3300):
    check_flat(i)
    time.sleep(random.randint(8,15))
