import sys
import numpy as np
from audioID.libs.reader_file import FileReader
from audioID.libs.config import get_config
from audioID.libs.db_sqlite import SqliteDatabase
import audioID.libs.fingerprint as fingerprint
from termcolor import colored
from itertools import zip_longest

config = get_config()
db = SqliteDatabase()

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values in zip_longest(fillvalue=fillvalue, *args))

def find_matches(samples, Fs=fingerprint.DEFAULT_FS):
    hashes = fingerprint.fingerprint(samples, Fs=Fs)
    return return_matches(hashes)

def return_matches(hashes):
    mapper = {}
    for hash, offset in hashes:
        # print(offset)
        mapper[hash.upper()] = offset
    values = mapper.keys()

    for split_values in grouper(values, 1000):
        split_values = list(split_values)
        # @todo move to db related files
        query = """
            SELECT upper(hash), song_fk, offset
            FROM fingerprints
            WHERE upper(hash) IN (%s)
        """
        query = query % ', '.join('?' * len(split_values))

        x = db.executeAll(query, split_values)
        matches_found = len(x)

        if matches_found > 0:
            msg = '   ** found %d hash matches (step %d/%d)'
            print(colored(msg, 'green') % (
            matches_found,
            len(split_values),
            len(values)
            ))
        else:
            msg = '   ** not matches found (step %d/%d)'
            print(colored(msg, 'red') % (
            len(split_values),
            len(values)
            ))

        for hash, sid, offset in x:
            offset = int.from_bytes(offset,'little')
            # (sid, db_offset - song_sampled_offset)
            # print(sid, offset, mapper[hash], hashes) # debug Ayu
            yield (sid, offset - mapper[hash])

def align_matches(matches):
    diff_counter = {}
    largest = 0
    largest_count = 0
    song_id = -1

    for tup in matches:
        sid, diff = tup

        if diff not in diff_counter:
            diff_counter[diff] = {}

        if sid not in diff_counter[diff]:
            diff_counter[diff][sid] = 0

        diff_counter[diff][sid] += 1

        if diff_counter[diff][sid] > largest_count:
            largest = diff
            largest_count = diff_counter[diff][sid]
            song_id = sid

    songM = db.get_song_by_id(song_id)

    nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                     fingerprint.DEFAULT_WINDOW_SIZE *
                     fingerprint.DEFAULT_OVERLAP_RATIO, 5)

    return {
        "SONG_ID" : song_id,
        "SONG_NAME" : songM[1],
        "CONFIDENCE" : largest_count,
        "OFFSET" : int(largest),
        "OFFSET_SECS" : nseconds
    }

def recognize_file(filepath):
    # config = get_config()
    # db = SqliteDatabase()

    chunksize = 2**12
    L = 5

    reader = FileReader(filepath)
    audio = reader.parse_audio()

    data = []
    for c in audio['channels']:
        iStart = np.random.randint((len(c)-L*audio['Fs']))
        iEnd   = iStart + L*audio['Fs']
        data.append(c[iStart:iEnd])
    # data = audio['channels']
    Fs = fingerprint.DEFAULT_FS
    channel_amount = len(data)

    result = set()
    matches = []

    for channeln, channel in enumerate(data):
        # TODO: Remove prints or change them into optional logging.
        msg = '   fingerprinting channel %d/%d'
        print(colored(msg, attrs=['dark']) % (channeln+1, channel_amount))

        matches.extend(find_matches(channel))

        msg = '   finished channel %d/%d, got %d hashes'
        print(colored(msg, attrs=['dark']) % (
        channeln+1, channel_amount, len(matches)
        ))

    total_matches_found = len(matches)

    if total_matches_found > 0:
        msg = ' ** totally found %d hash matches'
        print(colored(msg, 'green') % total_matches_found)

        song = align_matches(matches)

        msg = ' => song: %s (id=%d)\n'
        msg += '    offset: %d (%d secs)\n'
        msg += '    confidence: %d'

        print(colored(msg, 'green') % (
        song['SONG_NAME'], song['SONG_ID'],
        song['OFFSET'], song['OFFSET_SECS'],
        song['CONFIDENCE']
        ))
    else:
        msg = ' ** not matches found at all'
        print(colored(msg, 'red'))

if __name__ == '__main__':
    filepath = sys.argv[1]
    # filepath = 'mp3/伊格赛听,不靠谱组合 - 广寒谣.mp3'
    recognize_file(filepath)
