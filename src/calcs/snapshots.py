#!/usr/bin/python3

import numpy as np
import json
import random # Mersenne Twister
import matplotlib.pyplot as plt
from collections import OrderedDict
import argparse

parser = argparse.ArgumentParser(description='Process raw snapshot data for the second Hydra airdrop.')
parser.add_argument('round', metavar='n', type=int, choices=[1, 2],
                    help='The round of snapshots to process')

args = parser.parse_args()

if args.round == 1:
    # Input
    raw_files = ['../data/raw/snapshot_2017-12-25_00_02.dat',
                '../data/raw/snapshot_2017-12-26_00_08.dat',
                '../data/raw/snapshot_2017-12-27_00_00.dat',
                '../data/raw/snapshot_2017-12-28_00_00.dat',
                '../data/raw/snapshot_2017-12-29_00_59.dat',
                '../data/raw/snapshot_2017-12-30_00_06.dat',
                '../data/raw/snapshot_2017-12-31_00_00.dat']
    # Output
    balances_chonological_file = '../data/round1/all_balances_chronological.json'
    balances_sorted_file = '../data/round1/all_balances_sorted.json'
    balances_eligible_file = '../data/round1/balances_eligible.json'
    print("Processing first snapshot round...")
elif args.round == 2:
    # Input
    raw_files = ['../data/raw/snapshot_2017-12-25_00_02.dat',
                '../data/raw/snapshot_2017-12-26_00_08.dat',
                '../data/raw/snapshot_2017-12-27_00_00.dat',
                '../data/raw/snapshot_2017-12-28_00_00.dat',
                '../data/raw/snapshot_2017-12-29_00_59.dat',
                '../data/raw/snapshot_2017-12-30_00_06.dat',
                '../data/raw/snapshot_2017-12-31_00_00.dat']

    # Output
    balances_chonological_file = '../data/round2/all_balances_chronological.json'
    balances_sorted_file = '../data/round2/all_balances_sorted.json'
    balances_eligible_file = '../data/round2/balances_eligible.json'
    print("Processing second snapshot round...")






nSnaps = len(raw_files)


# Read all snapshots and make a list for each address, containing the balances
print("Reading raw snapshot data...")
snapshots= {}
for i in range(nSnaps):
    rawData = np.asarray( np.genfromtxt(raw_files[i], skip_header=6, dtype= None) )
    for x in rawData:
        address = x[2].decode("utf-8")
        if address in snapshots:
            snapshots[ address ][i] = x[0]
        else:
            snapshots[ address ] = np.zeros(nSnaps).tolist()
            snapshots[ address ][i] = x[0]


# Throw out all addresses that do not have any balance and sort the balances by amount
print("Cleaning and sorting snapshot data...")
balances_chronological = {}
balances_sorted = {}
for key, value in snapshots.items():
    if max(value) > 0 and key.startswith('p'): # exclude time locked tokens
        balances_chronological[ key ] = value
        balances_sorted[ key ] = sorted(value, reverse=True) # highest balance first


# Coins held for more than half of the snapshots are eligible to receive Hydras
print("Determining eligible balance for all addresses...")
minIOP = 1
minSnaps = int(nSnaps/2) + 1 # for 7, this is 4
balances_eligible = {}
for addr, balances in balances_sorted.items():
    eligible = balances[ minSnaps - 1] # array indices start at 0
    if eligible > minIOP: # need _more_ than 1 IOP to participate
        balances_eligible[ addr ] = eligible


print("Writing chronological balances to JSON... {}".format(balances_chonological_file))
with open(balances_chonological_file, 'w') as outfile:
    json.dump(balances_chronological, outfile, indent=2)
print("Writing sorted balances to JSON... {}".format(balances_sorted_file))
with open(balances_sorted_file, 'w') as outfile:
    json.dump(balances_sorted, outfile, indent=2)
print("Writing eligible balances to JSON... {}".format(balances_eligible_file))
with open(balances_eligible_file, 'w') as outfile:
    json.dump(balances_eligible, outfile, indent=2)
