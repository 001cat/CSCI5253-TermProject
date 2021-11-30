import os,glob

for f in glob.glob('../mp3/*.mp3'):
    os.system(f"python rest-client.py localhost add '{f}'")