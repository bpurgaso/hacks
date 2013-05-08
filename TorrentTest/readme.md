Quick overview

TorrentTest.sh contains the code to download a torrent.  python TorrentTest /path/to/whatever.torrent /path/to/destination/
server.py contains the code to create and start a torrent, with support for a tracker:  python server.py /path/to/directory/or/file/to/make/into/torrent


INSTALLING LIBTORRENT AND PYTHON BINDINGS

REDHAT 6.1 AND EQUIVALENTS
install_libtorrent.sh:   Installs the libtorrent library on RedHat 6.1 (and equivalents) as well as the python bindings.

UBUNTU 12.10
sudo apt-get install python-libtorrent



INSTALLING OPENTRACKER (CREATING OPEN TRACKER EXECUTABLE)

REDHAT 6.1
install_opentracker.sh:  Creates two small executables for opentracker, a very good and light-weight bit torrent tracker.

UBUNTU 12.10
sudo apt-get install cvs
install_opentracker.sh:  Creates two small executables for opentracker, a very good and light-weight bit torrent tracker.
