
import fingerprint as fp
import pandas as pd

filename = './library1/01. Bourgade.wav'

hashes=fp.fingerprint(filename)

df = pd.DataFrame.from_dict(hashes, orient='index', columns=['time', 'song'])
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'fingerprint'})
print(df.head())
