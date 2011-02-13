#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Misc Utilities
"""

import os
import re

PATTERN = re.compile(r'[A-Z]+[a-z0-9]+')

def parse_name(name, sep):
    """docstring for parse_name"""
    return sep.join(PATTERN.findall(name)).lower()

def parse_code(patterns, code):
    """docstring for parse_code"""
    ret = code

    for index in patterns:
        ret = ret.replace('$${0}_U$$'.format(index), patterns[index].upper())
        ret = ret.replace('$${0}_L$$'.format(index), patterns[index].lower())
        ret = ret.replace('$${0}$$'.format(index), patterns[index])

    return ret

def parse_file(patterns, indir, outdir, infile, outfile = None):
    """docstring for parse_file"""
    inf = open(os.path.join(indir, infile), 'r')
    text = inf.read()
    inf.close()

    text = parse_code(patterns, text)
    if not outfile:
        outfile = infile

    outf = open(os.path.join(outdir, outfile), 'w')
    outf.write(text)
    outf.close()

