
import fingerprint as fp
import pandas as pd
import os
import sys

cmdargs = sys.argv

listOfFiles = list()
print("Scanning Songs...")

#from the input folders, get every possible song location / path and store it in a list
for i in range(2, len(cmdargs)-2):
    folder = cmdargs[i]
    folder = './'+folder
    #print(folder)
    for (dirpath, dirnames, filenames) in os.walk(folder):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

hashes = {}
#obtain the fingerprints for each file
print("Obtaining Fingerprints...")
for file in listOfFiles:
    filename = file
    hashes_temp=fp.fingerprint(filename)
    hashes.update(hashes_temp)
    
#store the fingerprints in a dataframe and then save it as a csv file
df = pd.DataFrame.from_dict(hashes, orient='index', columns=['time', 'song'])
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'fingerprint'})

df.to_csv(str(cmdargs[len(cmdargs)-1])+'.csv', index=False)

print("Fingerprint Database saved!")