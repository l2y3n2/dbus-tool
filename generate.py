#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Generate automake projects for DBus Services

[Usage]
\tgenerate.py <project.xml>
"""

import os
import sys
import shutil
import random
import ndbus

SCRIPTS = """
#! /bin/sh

cd {0}
autoreconf -i
./configure
make distcheck
mv *.gz {1}
"""

def process():
    """docstring for process"""
    filename = os.path.abspath(sys.argv[1])
    service = ndbus.NService(filename)

    tmppath = 'tmp_{0:08d}'.format(random.randint(0, 99999999))
    tmppath = os.path.abspath(os.path.join(os.getcwd(), tmppath))
    os.mkdir(tmppath)

    service.gencode(os.path.abspath('./templates'), tmppath)
    os.system(SCRIPTS.format(tmppath, os.getcwd()))
    shutil.rmtree(tmppath, True)

    tbfile = open('{0}.xls'.format(service.name.lower()), 'w')
    service.gendoc(tbfile)
    tbfile.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    process()

