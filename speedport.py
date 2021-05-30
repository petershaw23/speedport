#!/usr/bin/python3

import requests
import hashlib
import re
import sys
import json


#formatting and printing single call
def print_call_data(str1, str2):
    # when do we need newlines when printing?
    nwl = (str1 == "takencalls_duration") or (str1 == "dialedcalls_duration") or (str1 == "missedcalls_who")
    # write duration using minutes and seconds
    if (str1 == "takencalls_duration") or (str1 == "dialedcalls_duration"):
         str2_min = int(str2) // 60
         str2_sec = int(str2) % 60
         str2 = str(str2_min) + "' " + str(str2_sec) + "''"
    # remove useless entries (do this after newlines and recalculation!)
    clutter = ["takencalls_", "missedcalls_", "dialedcalls_", "date", "time", "who"]
    for s in clutter:
        str1 = re.sub(s, '', str1)
    str1 = re.sub('duration', 'Dauer', str1)
    str1 = re.sub('id', 'Nr', str1)
    # finally print
    if nwl:
         print(str1, str2)
    else:
        print(str1, str2, end=" ")
    return
   

#printing set of calls
def print_calls(i, str, denom, counter, no):
    if (i["varid"] == str):
        counter += 1
        if (counter == 1):
            print (denom)
        if (counter < no+1):
            for j in i["varvalue"]:
                print_call_data(j["varid"],j["varvalue"])
    return counter
   
def main():
    url_router = 'http://192.168.2.1'
    passwd_router = 'XXXXXXXX'
   
    no_printed_calls = 6 #how many calls shall be printed?
    counter_taken = 0 #three counters
    counter_missed = 0
    counter_dialed = 0
       
    with requests.Session() as s:
        page = s.post(url_router + '/data/Login.json', data={'password': hashlib.md5(bytes(passwd_router, 'utf-8')).hexdigest(), 'showpw': '0', 'httoken': ''})
        httoken = re.findall('_httoken = (\d*);', s.get(url_router + '/html/content/overview/index.html?lang=de').text)[0]
       
        #Telefonate
        page = s.get(url_router + '/data/PhoneCalls.json', params={"_tn": httoken}, headers={'Referer': url_router + '/html/content/overview/index.html?lang=de'})
        page_decoded = json.loads(page.content.decode('utf-8'))
       
        for i in page_decoded:
             counter_taken = print_calls(i, "addtakencalls", "--angenommen", counter_taken, no_printed_calls)         
             counter_missed = print_calls(i, "adddialedcalls", "--angerufen", counter_missed, no_printed_calls)         
             counter_dialed = print_calls(i, "addmissedcalls", "--verpasst", counter_dialed, no_printed_calls)         

if __name__ == '__main__':
    main()
   
