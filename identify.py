import fingerprint as fp
import pandas as pd
import os
import sys

cmdargs = sys.argv

df = pd.read_csv (cmdargs[2]+'.csv')
file_name = cmdargs[4]
file_path = "./Test/clean_samples/01_Bourgade_samples/"+file_name+'.wav'

hashes=fp.fingerprint(file_path)

