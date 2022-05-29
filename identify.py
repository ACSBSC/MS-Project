import fingerprint as fp
import pandas as pd
import os
import sys

cmdargs = sys.argv

df = pd.read_csv (cmdargs[2]+'.csv')
file_name = cmdargs[4]
file_path = "./"+file_name

print("Scanning Test samples...")

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(file_path):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

for sample in listOfFiles:
    song_analysed = sample 
    #print(song_analysed)

    hashes = fp.fingerprint(song_analysed)

    list_match=[]
    dict={} 
    name=""

    for (key, values) in hashes.items():
        name = values[1]
        for row in range(len(df)):
            if key == df.at[row,'fingerprint']:
                song_name=df.at[row,'song']
                time_diff=df.at[row,'time']-values[0]
                if song_name in dict:
                    list_=[]
                    value_ = dict[song_name]
                    if type(value_)==list:
                        value_[0].append(time_diff)
                        dict[song_name]=value_
                    else:
                        list_.append([value_,time_diff])
                        dict[song_name]=list_
                else:
                    dict[song_name]=time_diff
                
    possible_songs=[] 
    matches = []
    result = False       
    for (key, values) in dict.items():
        if type(values)==list:
            result = all(elem == values[0][0] for elem in values[0])
            if result:
                possible_songs.append(key)
                matches.append(len(values[0]))
        else:
            possible_songs.append(key)
            matches.append(1)
    
    '''ordered=False
    while not ordered:
        count = 0
        for i in range(len(matches)-1):
            if matches[i]<matches[i+1]:
                m = matches[i]
                matches[i]=matches[i+1]
                matches[i+1]=m
                
                s = possible_songs[i]
                possible_songs[i]=possible_songs[i+1]
                possible_songs[i+1]=s
                
                count+=1
        
        if count < 0:
            ordered=True'''
    
    print()    
    print("Sample: ", name)
    for index in range(len(possible_songs)):
        print("Song prediction: ", possible_songs[index], " - Number of matches: ", matches[index])


    

