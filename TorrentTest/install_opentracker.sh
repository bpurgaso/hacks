#!/bin/bash
#opentracker -- redhat 6.1
mkdir -p ship_yard
cd ship_yard
cvs -d :pserver:cvs@cvs.fefe.de:/cvs -z9 co libowfat
cd libowfat
make
cd ..
cvs -d:pserver:anoncvs@cvs.erdgeist.org:/home/cvsroot co opentracker
cd opentracker
make
echo "Completed binaries are at ./ship_yard/opentracker/ -- opentracker and opentracker.debug"
