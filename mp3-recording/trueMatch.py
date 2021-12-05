import os,glob
import numpy as np

mp3files = [os.path.basename(f) for f in glob.glob('../mp3/*.mp3')]
mp3files.sort()
randIdx = np.random.permutation(len(mp3files))+1

# print(mp3files)

with open('trueMatch.txt','w+') as f:
    for idx,mp3file in zip(randIdx,mp3files):
        f.write(f'{mp3file:<80} {idx:02d}\n')
