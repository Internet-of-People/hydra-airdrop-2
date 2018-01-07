#!/usr/bin/python3

import numpy as np
import json
import matplotlib.pyplot as plt
from collections import OrderedDict
import argparse

TOTAL_HYDRAS = 500000
HYDRA_DECIMALS = 12
N_ROUNDS = 2
json.encoder.FLOAT_REPR = lambda o: format(o, '.12f')

parser = argparse.ArgumentParser(description='Calculate the distribution of HYD tokens for the second Hydra airdrop.')
parser.add_argument('round', metavar='n', type=int, choices=[1, 2],
                    help='The round of snapshots to process')

args = parser.parse_args()


if args.round == 1:
    # Input
    eligible_balances_file = '../data/round1/balances_eligible.json'

    # Output
    shares_file = '../data/round1/shares.json'
    hydras_file = '../data/round1/hydras.json'
else:
    # Input
    eligible_balances_file = '../data/round2/balances_eligible.json'

    # Output
    shares_file = '../data/round2/shares.json'
    hydras_file = '../data/round2/hydras.json'
    

print("Reading balance data for round {}...".format(args.round))
    
with open(eligible_balances_file) as data_file:    
    eligible_balances = json.load(data_file)

addresses, coins = zip(*eligible_balances.items()) # split dict into addresses and coins

print("Calculating shares...")
shares = np.power( 100 , np.arctan( (np.log10(coins)/2-1) * np.pi/2 ) + 1 )
total_shares = np.sum(shares)
print("Total Shares: {}".format(total_shares))
hydras = np.around(TOTAL_HYDRAS/N_ROUNDS * shares / total_shares, HYDRA_DECIMALS) 
shares_data = OrderedDict( sorted( dict( zip(addresses,shares) ).items(), key=lambda x: x[1] ) )
hydras_data = OrderedDict( sorted( dict( zip(addresses,hydras) ).items(), key=lambda x: x[1] ) )
print("Distributed a total of {} HYD".format(np.sum(hydras)))
print("Minimum amount was {} HYD".format(np.min(hydras)))
print("Maximum amount was {} HYD".format(np.max(hydras)))

print("Writing to disk...")
with open(shares_file, 'w') as outfile:
    json.dump(shares_data, outfile, indent=2)
with open(hydras_file, 'w') as outfile:
    json.dump(hydras_data, outfile, indent=2)
print("Done!")
