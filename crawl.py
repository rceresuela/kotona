#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup
import time
import json
import re
import house


url_part1 = "http://asunnot.oikotie.fi/apartment-rent/search/card?arpricerent%5Bmin%5D=&arpricerent%5Bmax%5D=&arsize%5Bmin%5D=&arsize%5Bmax%5D=&arsettings%5Bchanged%5D=0&arsettings%5Bcollapsed%5D=1&arbuildyear%5Bmin%5D=&arbuildyear%5Bmax%5D=&arpublished%5Bpublished%5D=1&offset="
url_part2 = "&limit="
url_part3 = "&sortby=published%20desc&format=json"

url_house = "http://asunnot.oikotie.fi/vuokrattavat-asunnot/"

def build_url(offset, limit):
   return url_part1 + str(offset) + url_part2 + str(limit) + url_part3

def get_ids(offset, limit):
   url = build_url(offset, limit)
   r = requests.get(url)
   data = json.loads(r.text)
   id_list = []

   while data['response']['docs']:
      for e in data['response']['docs']:
         id_list.append(e['card_id'])
   
      offset = offset + limit
      url = build_url(offset, limit)

      time.sleep(1)

      r = requests.get(url)
      data = json.loads(r.text)

   return id_list

def get_house_html(house_id):
   url = url_house + str(house_id)
   r = requests.get(url)
   r.encoding = 'utf-8'
   return r.text

def get_house(house_table):
   address = re.search("<th>\nSijainti\n</th>\n<td>\n(.*)</td>", str(house_table[0]))
   if address:
      address = address.group(1)

   size = re.search("<th>\nAsuinpinta-ala\n</th>\n<td>\n(.*)</td>", str(house_table[0]))
   if size:
      size = size.group(1)

   prize = re.search("<th>\nVuokra\n</th>\n<td>\n(.*)</td>", str(house_table[1]))
   if prize:
      prize = prize.group(1)

   rooms = re.search("<th>\nHuoneita\n</th>\n<td>\n(.*)</td>", str(house_table[0]))
   if rooms:
      rooms = rooms.group(1)

   room_configuration = re.search("<th>\nHuoneiston kokoonpano\n</th>\n<td>\n(.*)</td>", str(house_table[0]))
   if room_configuration:
      room_configuration = room_configuration.group(1)

   h = house.House(address, size, prize, rooms, room_configuration)
   return h


if __name__ == '__main__':
   start = time.time()
   offset = 0
   limit = 48
   
   id_list = []
   id_list = get_ids(offset, limit)
   failed_id_list = []
   i = 1

   for house_id in id_list:
      try:
         house_html = get_house_html(house_id)
         soup = BeautifulSoup(house_html, "lxml")
         house_table = soup.find_all("table")
         my_house = get_house(house_table)
         print i, "->", my_house.address
      except requests.exceptions.ConnectionError, e:
         failed_id_list.append(house_id)
      except UnicodeDecodeError, e:
         failed_id_list.append(house_id)
      except IndexError, e:
         failed_id_list.append(house_id)
      finally:
         i = i + 1
      
   end = time.time()
   print "total time:", str(end - start)
   print "failed:", len(failed_id_list)