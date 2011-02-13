#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DBus Interface Class
"""

import os
from .nmethod import NMethod
from .nsignal import NSignal
from .nutils import parse_name, parse_code

SOURCE_HEADER = """
#include "$$OBJECT_L$$-object.h"
#include "dbus-iface.h"

"""

DOC_HEAD = """
<tr>
<td>{0}</td>
<td><table border="1">
"""
DOC_TITLE_METHOD = """
<tr><td>方法名</td><td>参数</td><td>类型</td><td>输入/输出</td></tr>
"""
DOC_TITLE_SIGNAL = """
<tr><td>信号名</td><td>参数</td><td>类型</td></tr>
"""
DOC_TAIL = """
</table></td>
</tr>
"""

class NIFace(object):
    """docstring for NIFace"""
    def __init__(self, inode):
        super(NIFace, self).__init__()

        self.name = inode.attrib['name']
        self.symbol = inode.find('annotation').attrib['value']
        self.filename = 'iface-{0}.c'.format(parse_name(self.name, '-'))
        self.code = SOURCE_HEADER

        self.methods = []
        for mnode in inode.findall('method'):
            self.methods.append(NMethod(mnode))

        self.signals = []
        for snode in inode.findall('signal'):
            self.signals.append(NSignal(snode))

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        patterns['IFACE_SYMBOL'] = self.symbol
        self.code = parse_code(patterns, self.code)

        source = open(os.path.join(outdir, self.filename), 'w')
        header = open(os.path.join(outdir, 'dbus-iface.h'), 'a')
        marshal = open(os.path.join(outdir, 'marshal.list'), 'a')

        source.write(self.code)
        header.write('\n//Interface {0}\n'.format(self.name))

        for method in self.methods:
            method.gencode(patterns.copy(), indir, outdir)
            source.write(method.proto)
            source.write(method.code)
            header.write(method.proto + ';\n')

        for sig in self.signals:
            sig.gencode(patterns.copy(), indir, outdir)
            source.write(sig.proto)
            source.write(sig.code)
            header.write(sig.proto + ';\n')
            marshal.write(sig.marshal)

        marshal.close()
        header.close()
        source.close()

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        tbfile.write(DOC_HEAD.format(self.name))

        if self.methods:
            tbfile.write(DOC_TITLE_METHOD)
        for method in self.methods:
            method.gendoc(tbfile)

        if self.signals:
            tbfile.write(DOC_TITLE_SIGNAL)
        for sig in self.signals:
            sig.gendoc(tbfile)
        tbfile.write(DOC_TAIL)


