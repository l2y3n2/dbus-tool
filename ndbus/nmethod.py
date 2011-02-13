#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DBus Method Class
"""

from .narg import NMethodArg
from .nutils import parse_name, parse_code

FUNCDEF = 'gboolean {0}($$OBJECT$$Object *obj{1}, GError **error)'
FUNCCODE = """
{
\tg_set_error(error, 0, 0, "not implemented yet");

\treturn FALSE;
}

"""

DOC = '<tr><td rowspan={0}>{1}</td><td colspan=3></td></tr>\n'

class NMethod(object):
    """docstring for NMethod"""
    def __init__(self, mnode):
        super(NMethod, self).__init__()

        self.name = mnode.attrib['name']
        self.symbol = parse_name(self.name, '_')
        self.args = []
        for anode in mnode.findall('arg'):
            self.args.append(NMethodArg(anode))

        self.proto = FUNCDEF
        self.code = FUNCCODE
        if mnode.find('annotation'):
            self.prefix = mnode.find('annotation').attrib['value']
        else:
            self.prefix = None

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        for arg in self.args:
            arg.gencode(patterns.copy(), indir, outdir)

        if not self.prefix:
            self.prefix = '$$IFACE_SYMBOL_L$$_' + parse_name(self.name, '_')

        args_code = ', '.join([arg.code for arg in self.args])
        if args_code:
            args_code = ', ' + args_code

        self.proto = self.proto.format(self.prefix, args_code)
        self.proto = parse_code(patterns, self.proto)

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        tbfile.write(DOC.format(len(self.args) + 1, self.name))
        for arg in self.args:
            arg.gendoc(tbfile)


