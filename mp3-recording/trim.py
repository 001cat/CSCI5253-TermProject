import os,glob

matchTable = {}
with open('trueMatch.txt','r') as f:
     for l in f.readlines():
          matchTable[l[:80].strip()] = int(l[80:])


for rawFile in glob.glob('../mp3/*.mp3'):
     i = matchTable[os.path.basename(rawFile)]
     newFile = f'record-{i:02d}.mp3'

     os.system(f""" 
     ffmpeg -ss 00:01:00 -t 00:00:20 -i "{rawFile}" -acodec copy "{newFile}"
          """)