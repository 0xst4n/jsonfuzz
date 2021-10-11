import argparse
import urllib.request
import json
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

print(args.D)
if not is_json(args.D):
    parser.error("-D: input valid JSON") 

# TODO:
# add FUZZ to json
# do post request
# read wordlist 


