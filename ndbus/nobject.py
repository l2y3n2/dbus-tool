#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DBus Object Class
"""

import os
import xml.etree.ElementTree as etree
from .niface import NIFace
from .nutils import parse_code, parse_file

REGISTER_OBJECT_HEADER = """
void $$OBJECT_L$$_init(DBusGConnection *bus)
{
\t$$OBJECT$$Object *tmp;
"""
REGISTER_OBJECT = """
\ttmp = $$OBJECT_L$$_object_new();
\t$$OBJECT_L$$_object_register(tmp, bus, "{0}");
"""
REGISTER_OBJECT_TAIL = '}\n'

DOC_HEAD = """
<table border="1">
<tr><td>对象</td><td>{0}</td></tr>
"""
DOC_PATH = '<tr><td>访问路径</td><td>{0}</td></tr>\n'
DOC_TAIL = '</table>\n'

class NObject(object):
    """docstring for NObject"""
    def __init__(self, obj, basepath):
        super(NObject, self).__init__()

        self.name = obj.find('name').text
        self.name = self.name[0].upper() + self.name[1:]
        self.paths = [pnode.text for pnode in obj.findall('path')]
        self.reg_objs = REGISTER_OBJECT_HEADER
        self.reg_objs += ''.join(
                [REGISTER_OBJECT.format(path) for path in self.paths])
        self.reg_objs += REGISTER_OBJECT_TAIL

        self.filename = os.path.join(basepath, obj.find('iface').text)
        root = etree.parse(self.filename).getroot()

        self.ifaces = []
        for inode in root.findall('interface'):
            self.ifaces.append(NIFace(inode))

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        outdir = os.path.join(outdir, self.name.lower())
        os.mkdir(outdir)

        patterns['OBJECT'] = self.name
        self.reg_objs = parse_code(patterns, self.reg_objs)
        for iface in self.ifaces:
            iface.gencode(patterns.copy(), indir, outdir)

        patterns['SIGNAL_LIST'] = ''
        patterns['REGISTER_SIGNALS'] = ''
        patterns['IFACE_FILES'] = ' '.join(
                [iface.filename for iface in self.ifaces])
        for iface in self.ifaces:
            patterns['SIGNAL_LIST'] += ''.join(
                    ['\t{0},\n'.format(sig.enum) for sig in iface.signals])
            patterns['REGISTER_SIGNALS'] += ''.join(
                    [sig.reg for sig in iface.signals])

        parse_file(patterns, indir, outdir, 'object.gob',
                self.name.lower() + '.gob')
        parse_file(patterns, indir, outdir, 'Makefile.am.object', 'Makefile.am')
        parse_file({}, indir, outdir, self.filename, 'iface.xml')

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        tbfile.write(DOC_HEAD.format(self.name))
        for path in self.paths:
            tbfile.write(DOC_PATH.format(path))
        for iface in self.ifaces:
            iface.gendoc(tbfile)
        tbfile.write(DOC_TAIL)


