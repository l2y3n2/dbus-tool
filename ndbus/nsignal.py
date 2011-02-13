#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DBus Signal Class
"""

from .narg import NSignalArg
from .nutils import parse_name, parse_code

ENUMCODE = '$$OBJECT_U$$_SIGNAL_{0}'
MARSHAL = 'VOID:{0}\n'
FUNCDEF = 'void {0}($$OBJECT$$Object *obj{1})'
FUNCCODE = """
\t$$OBJECT$$ObjectClass *klass;

\tklass = $$OBJECT_U$$_OBJECT_GET_CLASS(obj);
\tg_signal_emit(obj, klass->signals[{0}], 0{1});
"""
REGCODE = """
\tklass->signals[{0}] = g_signal_new("{1}",
\t\t\tG_OBJECT_CLASS_TYPE(klass),
\t\t\tG_SIGNAL_RUN_LAST | G_SIGNAL_DETAILED,
\t\t\t0, NULL, NULL,
\t\t\tdbus_marshal_VOID__{2},
\t\t\tG_TYPE_NONE, {3}{4});
"""

DOC = '<tr><td rowspan={0}>{1}</td><td colspan=3></td></tr>\n'

class NSignal(object):
    """docstring for NSignal"""
    def __init__(self, snode):
        super(NSignal, self).__init__()

        self.name = snode.attrib['name']
        self.symbol = parse_name(self.name, '_')
        self.args = []
        for anode in snode.findall('arg'):
            self.args.append(NSignalArg(anode))

        self.enum = ENUMCODE
        self.marshal = MARSHAL
        self.proto = FUNCDEF
        self.code = FUNCCODE
        self.reg = REGCODE
        if snode.find('annotation'):
            self.prefix = snode.find('annotation').attrib['value']
        else:
            self.prefix = None

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        for arg in self.args:
            arg.gencode(patterns.copy(), indir, outdir)

        if not self.prefix:
            self.prefix = '$$IFACE_SYMBOL_L$$_' + self.symbol

        args_code = ', '.join([arg.code for arg in self.args])
        if args_code:
            args_code = ', ' + args_code

        marshal = ','.join([arg.mtype for arg in self.args])
        if not marshal:
            marshal = 'VOID'
        regs_type = marshal.replace(',', '_')

        regs_code = ', '.join([arg.gtype for arg in self.args])
        if regs_code:
            regs_code = ', ' + regs_code

        name_code = ', '.join([arg.name for arg in self.args])
        if name_code:
            name_code = ', ' + name_code

        self.enum = self.enum.format(self.symbol.upper())
        self.enum = parse_code(patterns, self.enum)
        self.marshal = self.marshal.format(marshal)
        self.proto = self.proto.format(self.prefix, args_code)
        self.proto = parse_code(patterns, self.proto)
        self.code = self.code.format(self.enum, name_code)
        self.code = parse_code(patterns, self.code)
        self.code = '\n{' + self.code + '}\n\n'
        self.reg = self.reg.format(self.enum, self.symbol, regs_type,
                len(self.args), regs_code)
        self.reg = parse_code(patterns, self.reg)

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        tbfile.write(DOC.format(len(self.args) + 1, self.name))
        for arg in self.args:
            arg.gendoc(tbfile)


