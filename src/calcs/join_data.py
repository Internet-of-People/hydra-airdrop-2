#!/usr/bin/python3
import json
HYDRA_DECIMALS = 12
json.encoder.FLOAT_REPR = lambda o: format(o, '.12f')


# Input
shares_files = ['../data/round1/shares.json',
                '../data/round2/shares.json']
hydras_files = ['../data/round1/hydras.json',
                '../data/round2/hydras.json']

# Output
all_shares_file = '../data/combined/shares.json'
all_hydras_file = '../data/combined/hydras.json'
  

print("Reading share and token data from both rounds...")
with open(shares_files[0]) as data_file:    
    shares_round1 = json.load(data_file)
with open(shares_files[1]) as data_file:    
    shares_round2 = json.load(data_file)
with open(hydras_files[0]) as data_file:    
    hydras_round1 = json.load(data_file)
with open(hydras_files[1]) as data_file:    
    hydras_round2 = json.load(data_file)

all_addresses = set(shares_round1.keys()) | set(shares_round2.keys())

all_shares = {}
all_hydras = {}
for addr in all_addresses:
    all_shares[ addr ] = [ shares_round1.get(addr,0.0), shares_round2.get(addr,0.0) ]
    all_hydras[ addr ] = [ round(hydras_round1.get(addr,0.0),HYDRA_DECIMALS), round(hydras_round2.get(addr,0.0),HYDRA_DECIMALS) ]

print("Writing to disk...")
with open(all_shares_file, 'w') as outfile:
    json.dump(all_shares, outfile, indent=2)
with open(all_hydras_file, 'w') as outfile:
    json.dump(all_hydras, outfile, indent=2)
print("Done!")
