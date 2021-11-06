import argparse, requests, json
from os.path import exists

parser = argparse.ArgumentParser(description='JsonFuzz')

# Required positional argument
parser.add_argument('-W', help='The wordlist to use')
parser.add_argument('-H', help='The website to fuzz, for example: http://127.0.0.1:5000/login')
parser.add_argument('-D', help='The JSON data to fuzz')

args = parser.parse_args()

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

if not args.W or not args.H or not args.D:
    parser.error("Required arguments: -W, -H, -D")
    quit()

if "http" not in args.H:
    parser.error("-H: must be an url to a website/API/endpoint") 
    quit()

if not exists(args.W):
    parser.error("-W: wordlist does not exist")

if not is_json(args.D):
    parser.error("-D: input valid JSON") 

if "FUZZ" not in args.D:
    parser.error("-D: input must contain FUZZ keyword")

url = args.H
wordlist_location = args.W
input_data = args.D
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

wordlist = open(wordlist_location, 'r')
lines = wordlist.readlines()

count = len(lines)
index = 0

for p in lines:
  p = p.strip()
  data = input_data.replace("FUZZ", p)
  r = requests.post(args.H, data=data, headers=headers)
  print(f'\r{index}/{count} requests', end='')
  index += 1
  if (r.status_code == 200):
    print()
    print(f"RESPONSE: {r.text.strip()}")
    print(f"CODE: {r.status_code}")
    print(f"PAYLOAD: {data}")
    check = input("Continue? (y/n): ")
    if check.lower() != "y":
      break


