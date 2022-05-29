import fingerprint as fp
import pandas as pd
import os
import sys
import metrics
import random

cmdargs = sys.argv

df = pd.read_csv (cmdargs[2]+'.csv')
file_name = cmdargs[4]
file_path = "./"+file_name

print()
print("Scanning Test sample...")

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(file_path):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

'''Total_files=0
TP = 0
FN = 0
FP = 0'''
random.shuffle(listOfFiles)
#for sample in listOfFiles:
song_analysed = sample 
#print(song_analysed)
'''if Total_files>15:
    break
Total_files+=1'''

hashes = fp.fingerprint(song_analysed)

list_match=[]
dict={} 
name=""

for (key, values) in hashes.items():
    name = values[1]
    for row in range(len(df)):
        if key == df.at[row,'fingerprint']:
            song_name=df.at[row,'song']
            #time_diff=df.at[row,'time']-values[0]
            if song_name not in dict:
                dict[song_name]=[]
            
            dict[song_name].append((key, values[0], df.at[row,'time']))
                

'''
We can calculate a histogram of the number of matches per offset. 
The height of the tallest peak in the histogram is the best score for that match. 
Songs with a lot of similar frequencies, but played at different times, 
will have a flat histogram with no clear tall peaks.

keep track of the specific hash which matched between the database and the user recording, 
as well as the time in the database that matched occured and the time it occured in the user sample
'''
# assign a score based on the largest peak in it's histogram.
scores = {}

for song_index, matches in dict.items():
    song_scores_by_offset = {}
    
    for hash, sample_time, source_time in matches:
        delta = source_time - sample_time
        
        if delta not in song_scores_by_offset:
            song_scores_by_offset[delta] = 0
            
        song_scores_by_offset[delta] += 1
        
    max = (0, 0)

    for offset, score in song_scores_by_offset.items():

        if score > max[1]:
            max = (offset, score)

    scores[song_index] = max
                
                
scores = list(sorted(scores.items(), key=lambda x: x[1][1], reverse=True))                 

scores = scores[:5]
if len(scores)>0:
    name_song=name.split("_")
    sn=name_song[1:len(name_song)-1]
    for song_id, score in scores:
        if sn[0] in song_id:
            TP+=1
    
        else:
            FP+=1
else:
    FN+=1
            
    
    
print() 
print(f"File name {name}:")                
for song_id, score in scores:
    print(f"{song_id}: Score of {score[1]}")               
                
'''print("Total files: ", Total_files)
print("TP: ", TP)
print("FP: ", FP)
print("FN: ", FN)'''