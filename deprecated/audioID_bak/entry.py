import os
from audioID.get_database_stat import printSongs
from audioID.collect_fingerprints_of_songs import addAudio2DB

packageDir = os.path.dirname(os.path.realpath(__file__))

def reset():
    os.system(f'cd {packageDir} && find . -name \*.pyc -delete')
    os.system(f'cd {packageDir} && python reset-database.py')

def stats():
    return printSongs()

def addAudio(audio_path):
    return addAudio2DB(audio_path)

def recognizeFile():
    pass

# def recognizeMic():
#     pass

if __name__ == '__main__':
    # reset()
    # for mp3file in os.listdir('mp3'):
    #     addAudio('mp3/'+mp3file)
    print(stats())
    pass