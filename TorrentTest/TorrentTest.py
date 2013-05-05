'''
Created on May 4, 2013

@author: bpurgaso
'''

import libtorrent
import time
import sys
import os


class Client(object):
    def __init__(self):
        self.state_string = ['queued',
                             'checking',
                             'downloading metadata',
                             'downloading',
                             'finished',
                             'seeding',
                             'allocating',
                             'checking fastresume']

        self.progress_string = '\r{0:3.2f}% complete (down: {1:.1f}% kb/s up:'\
                               ' {2:.1f}% kb/s peers: {3}) {4}'
        self.update_delay = 1

    def getUpdateFactory(self, handle, seed=False):
        while not handle.is_seed() or seed:
            s = handle.status()  # update status
            time.sleep(self.update_delay)
            yield self.progress_string.format(s.progress * 100,
                                             s.download_rate / 1000,
                                             s.upload_rate / 1000,
                                             s.num_peers,
                                             self.state_string[s.state])

    def download_torrent(self, torrent_path, save_path, mode='console'):
        if mode != 'console' and mode != 'generator':
            raise(Exception('InvalidMode'))
        session = libtorrent.session()
        session.listen_on(6881, 6891)
        info = libtorrent.torrent_info(torrent_path)
        handle = session.add_torrent({'ti': info, 'save_path': save_path})

        print 'starting', handle.name()
        for i in self.getUpdateFactory(handle):
            sys.stdout.write(i)
            sys.stdout.flush()
        print
        print handle.name(), 'complete'

#    def download_magnet(self, link, mode='console'):
#        if mode != 'console' and mode != 'generator':
#            raise(Exception('InvalidMode'))
#        session = libtorrent.session()
#        session.listen_on(6881, 6891)
#        handle = libtorrent.add_magnet_uri(session, link, {'save_path': './'})
#
#        print 'starting', handle.name()
#        for i in self.getUpdateFactory(handle):
#            sys.stdout.write(i)
#            sys.stdout.flush()
#        print
#        print handle.name(), 'complete'

c = Client()
target = sys.argv[1]
save_path = sys.argv[2]
if os.path.isfile(target):
    c.download_torrent(target, save_path)
else:
    c.download_magnet(target)
