#!/usr/bin/python
# vim:fileencoding=UTF-8

import argparse
import csv
import sys
import locale
import logging
import tempfile
from getpass import getpass

import eagate
import sdgvt

def fetch(args):
  logging.basicConfig(level = logging.DEBUG)

  kid, password = input("KONAMI ID: "), getpass("Password: ")

  with tempfile.NamedTemporaryFile() as tmp:
    eg = eagate.EaGate(tmp.name)
    eg.set_account(kid, password)
    logging.info('loginning...')
    if eg.login() == False:
        logging.error('Failed to login!')
        return
    logging.info(u'Fetching data...')
    music_info = eg.get_music_info()

  FIELDS = [
      'name', 'genre', 'artist', 'version', 'play_count_sp', 'play_count_dp',
      'clear_lamp_spn', 'dj_level_spn', 'ex_score_spn', 'pgreat_spn', 'great_spn', 'miss_count_spn',
      'clear_lamp_sph', 'dj_level_sph', 'ex_score_sph', 'pgreat_sph', 'great_sph', 'miss_count_sph',
      'clear_lamp_spa', 'dj_level_spa', 'ex_score_spa', 'pgreat_spa', 'great_spa', 'miss_count_spa',
      'clear_lamp_dpn', 'dj_level_dpn', 'ex_score_dpn', 'pgreat_dpn', 'great_dpn', 'miss_count_dpn',
      'clear_lamp_dph', 'dj_level_dph', 'ex_score_dph', 'pgreat_dph', 'great_dph', 'miss_count_dph',
      'clear_lamp_dpa', 'dj_level_dpa', 'ex_score_dpa', 'pgreat_dpa', 'great_dpa', 'miss_count_dpa',
  ]

  with open(args.savedest, 'w') as f:
    writer = csv.DictWriter(f, FIELDS, lineterminator = '\n')
    writer.writeheader()
    # エンコードして書き出す
    for row in music_info:
      row_encoded = {}
      for key, value in row.items():
        row_encoded[key] = value
      writer.writerow(row_encoded)
    logging.info("Saved to `{0}'.".format(f.name))

  return music_info

def sdgvt_upload(args):
  with tempfile.NamedTemporaryFile() as tmp:
    session = sdgvt.SDGVT(input('SDGVT Username: '), getpass('Password: '), tmp.name)
    session.login()
    session.upload(None)

argparser_root = argparse.ArgumentParser()
argparser_root.set_defaults(func = None)

subparser = argparser_root.add_subparsers()
parser_fetch = subparser.add_parser('fetch', help = 'to Fetch your DJ DATA from e-AMUSEMENT GATE.')
parser_fetch.set_defaults(func = fetch, savedest = 'music-info.csv')
parser_fetch.add_argument('--savedest')

parser_fetch = subparser.add_parser('sdgvt', help = 'to Upload your DJ DATA to IIDX SCORE DATA GRAPHICAL VIEW TOOL.')
parser_fetch.set_defaults(func = sdgvt_upload)
parser_fetch.add_argument('path_to_csv')

args = argparser_root.parse_args()
if args.func:
  args.func(args)
else:
  argparser_root.parse_args(["--help"])
