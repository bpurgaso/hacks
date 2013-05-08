#!/bin/bash
#libtorrent -- redhat 6.1
mkdir -p ship_yard
cd ship_yard
sudo yum clean all
sudo yum groupinstall "Development Tools" -y
sudo yum groupinstall "Development Libraries" -y
sudo yum install boost-* python-setuptools m2crypto pyOpenSSL openssl openssl-devel python-devel -y
wget https://libtorrent.googlecode.com/files/libtorrent-rasterbar-0.16.9.tar.gz
tar -zxvf ./libtorrent-rasterbar-0.16.9.tar.gz
cd libtorrent-rasterbar-0.16.9/
./configure --enable-python-binding --with-boost-libdir=/usr/lib64
make
sudo make install
cd bindings/python/
python setup.py build
sudo python setup.py install
export LD_LIBRARY_PATH=/usr/local/lib/
