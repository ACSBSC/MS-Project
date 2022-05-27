
import fingerprint as fp
import pandas as pd
import os
import sys

cmdargs = sys.argv

folder = cmdargs[2]
folder = './'+folder

print("Scanning Songs...")

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(folder):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

hashes = {}
print("Obtaining Fingerprints...")
for file in listOfFiles:
    filename = file
    hashes_temp=fp.fingerprint(filename)
    hashes.update(hashes_temp)
    

df = pd.DataFrame.from_dict(hashes, orient='index', columns=['time', 'song'])
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'fingerprint'})

df.to_csv(str(cmdargs[4])+'.csv', index=False)

print("Fingerprint Database saved!")