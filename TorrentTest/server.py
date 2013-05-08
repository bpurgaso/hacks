'''
Created on May 4, 2013

@author: bpurgaso
'''

import libtorrent
import time
import sys
import os


def getUpdateFactory(handle, seed=False):
    while not handle.is_seed() or seed:
        s = handle.status()  # update status
        time.sleep(1)
        yield '{0: >80}'.format(progress_string.format(s.progress * 100,
                                                     s.download_rate / 1000,
                                                     s.upload_rate / 1000,
                                                     s.num_peers,
                                                     state_string[s.state]))

state_string = ['queued',
                             'checking',
                             'downloading metadata',
                             'downloading',
                             'finished',
                             'seeding',
                             'allocating',
                             'checking fastresume']

progress_string = '{0:3.2f}% complete (down: {1:.1f}% kb/s up:'\
                               ' {2:.1f}% kb/s peers: {3}) {4}\r'


tfile_path = './test.torrent'
files = libtorrent.file_storage()
libtorrent.add_files(files, './dummy_torrent')
torrent_file = libtorrent.create_torrent(files)
libtorrent.set_piece_hashes(torrent_file, ".")
torrent_file.set_comment('Test torrent1')
torrent_file.set_creator('bpurgaso')
# Needs to be changed to correct tracker
torrent_file.add_tracker('udp://babylon.att.net:6969/announce')

try:
    os.remove(tfile_path)
except OSError:
    pass
with open(tfile_path, 'wb') as f:
    f.write(libtorrent.bencode(torrent_file.generate()))


session = libtorrent.session()
session.listen_on(6881, 6891)
info = libtorrent.torrent_info(tfile_path)
handle = session.add_torrent({'ti': info, 'save_path': './'}, )

for i in getUpdateFactory(handle, seed=True):
    sys.stdout.write(i)
    sys.stdout.flush()
