#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DBus Argument Class
"""

DOC_HEAD = '<tr>'
DOC_TAIL = '</tr>\n'

class NArg(object):
    """docstring for NArg"""
    def __init__(self, anode):
        super(NArg, self).__init__()

        self.name = anode.attrib['name']
        self.type = anode.attrib['type']
        self.direction = anode.attrib['direction']

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        pass

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        tbfile.write(DOC_HEAD)
        tbfile.write('<td>{0}</td>'.format(self.name))
        tbfile.write('<td>{0}</td>'.format(self.argmap[self.type][0]))


class NMethodArg(NArg):
    """docstring for NMethodArg"""
    argmap = {
            'y':    ('guchar ', ),
            's':    ('gchar *', ),
            'u':    ('guint ', ),
            'i':    ('gint ', ),
            'x':    ('gint64 ', ),
            't':    ('guint64 ', ),
            'd':    ('gdouble ', ),
            'b':    ('gboolean ', ),
            'ay':   ('GByteArray *', ),
            'as':   ('gchar **', ),
            'au':   ('GArray *', ),
            'ai':   ('GArray *', ),
            'ax':   ('GArray *', ),
            'at':   ('GArray *', ),
            'ad':   ('GArray *', ),
            'ab':   ('GArray *', ),
            }

    def __init__(self, anode):
        super(NMethodArg, self).__init__(anode)

        self.code = self.argmap.get(self.type)[0]
        if not self.code:
            raise ValueError(
                    'unknown method argument type: {0}'.format(self.type))

        if self.direction == 'out':
            self.code += '*'
        else:
            if '*' in self.code:
                self.code = 'const ' + self.code
        self.code += self.name

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        pass

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        NArg.gendoc(self, tbfile)
        tbfile.write('<td>{0}</td>'.format(
            '输入' if self.direction == 'in' else '输出'))
        tbfile.write(DOC_TAIL)


class NSignalArg(NArg):
    """docstring for NSignalArg"""
    argmap = {
            'y':    ('guchar ',     'G_TYPE_UCHAR'),
            's':    ('gchar *',     'G_TYPE_STRING'),
            'u':    ('guint ',      'G_TYPE_UINT'),
            'i':    ('gint ',       'G_TYPE_INT'),
            'x':    ('gint64 ',     'G_TYPE_INT64'),
            't':    ('guint64 ',    'G_TYPE_UINT64'),
            'd':    ('gdouble ',    'G_TYPE_DOUBLE'),
            'b':    ('gboolean ',   'G_TYPE_BOOLEAN'),
            }

    def __init__(self, anode):
        super(NSignalArg, self).__init__(anode)

        (self.code, self.gtype) = self.argmap[self.type]
        if not self.code:
            raise ValueError(
                    'unknown signal argument type: {0}'.format(self.type))
        self.mtype = self.gtype.split('_')[-1]

        if '*' in self.code:
            self.code = 'const ' + self.code
        self.code += self.name

    def gencode(self, patterns, indir, outdir):
        """docstring for gencode"""
        pass

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        NArg.gendoc(self, tbfile)
        tbfile.write('<td></td>')
        tbfile.write(DOC_TAIL)


