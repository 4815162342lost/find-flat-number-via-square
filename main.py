#!/usr/bin/python3
import requests
import time
import random
import json

approved_flats=[]

a=133; b=145
while b<=217:
    for i in range(a, b):
        approved_flats.append(i)
    a=a+36; b=b+36

logs=open('/tmp/1.log', 'a')

def check_flat(number, exception_count=0, e=None, json_e=None):
    try:
        if exception_count!=0:
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
