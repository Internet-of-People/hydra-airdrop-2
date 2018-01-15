#!/usr/bin env python3

import json
import numpy as np
from collections import OrderedDict

original_file = '../data/registration_original.json'
clean_file = '../data/registration.json'
hydra_file = '../data/combined/hydras.json'
payout_file = '../data/payout.json'

print("Reading original registration data ... ")
with open(original_file) as data_file:    
    reg_data = json.load(data_file)


print("Writing file to disk cleanly...")
with open(clean_file, 'w') as outfile:
    json.dump(reg_data, outfile, indent=2)

print("Reading Hydra amount per IOP address")
with open(hydra_file) as data_file:    
    amounts = json.load(data_file)


payout = {}
for address, dic in reg_data.items():
    if dic['eth'] in payout:
        payout[ dic['eth'] ] += np.sum(amounts[ address ])
    else:
        payout[ dic['eth'] ] = np.sum(amounts[ address ])

payout_sorted = OrderedDict( sorted( payout.items(), key=lambda x: x[1] ) )


print("Total amount claimed: {} HYD".format(np.sum(list(payout_sorted.values()))))

print("Writing payouts to disk...")
with open(payout_file, 'w') as outfile:
    json.dump(payout_sorted, outfile, indent=2)

