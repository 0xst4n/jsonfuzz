# Simple single parameter JSON fuzzer
# example: python main.py -u http://127.0.0.1:5000/login -w rockyou-75.txt -d '{"username": "admin", "password" : "FUZZ"}'

import argparse, requests, json
from argparse import RawTextHelpFormatter
from os.path import exists

from colorama import init
from termcolor import colored

init(convert=True)

status_codes = [200, 301]

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description='JsonFuzz \n Fuzzing JSON API endpoints \n example: python main.py -u http://127.0.0.1:5000/login -w rockyou-75.txt -d \'{"username": "admin", "password" : "FUZZ"}\' -c 200,301')

# Required positional argument
parser.add_argument('-w', help='the wordlist to use', metavar='wordlist')
parser.add_argument('-u', help='the website to fuzz, for example: http://127.0.0.1:5000/login', metavar='url/host')
parser.add_argument('-d', help='the JSON data to fuzz', metavar='json data')
parser.add_argument('-c', help='status code filtering (default: 200,301)', metavar='status codes')

args = parser.parse_args()

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

if not args.w or not args.u or not args.d:
    parser.error("Required arguments: -w, -u, -d")
    quit()

if "http" not in args.u:
    parser.error("-u: must be an url to a website/API/endpoint") 
    quit()

if not exists(args.w):
    parser.error("-w: wordlist does not exist")

if not is_json(args.d):
    parser.error("-d: invalid JSON") 

if "FUZZ" not in args.d:
    parser.error("-d: input must contain FUZZ keyword")

if not args.c:
    print(f"No status codes selected, using defaults: {colored(','.join(str(x) for x in status_codes),  'green')}")
else:
    if ',' in args.c:
      status_codes = args.c.split(',')
    else:
      status_codes = args.c

    status_codes = [int(x) for x in status_codes]

    print(f"Using the following selected status codes: {colored(','.join(str(x) for x in status_codes),  'green')}")

url = args.u
wordlist_location = args.w
input_data = args.d
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

wordlist = open(wordlist_location, 'r')
lines = wordlist.readlines()

count = len(lines)
index = 0

for p in lines:
  p = p.strip()
  data = input_data.replace("FUZZ", p)
  r = requests.post(url, data=data, headers=headers)
  print(f'\r{index}/{count} requests', end='')
  index += 1
  if r.status_code in status_codes:
    print()
    print(f"RESPONSE: {r.text.strip()}")
    print(f"CODE: {colored(r.status_code,  'green')}")
    print(f"PAYLOAD: {colored(data, 'green')}")
    check = input("Continue? (y/n): ")
    if check.lower() != "y":
      break


