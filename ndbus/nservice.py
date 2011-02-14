#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DBus Service Class
"""

import os
import xml.etree.ElementTree as etree
from .nobject import NObject
from .nutils import parse_file

DOC_HEAD = """
<head>
<meta http-equiv=Content-Type content="text/html; charset=UTF-8">
<body>

<table border="1">
<tr><td>软件包</td><td>{0}</td></tr>
<tr><td>服务名称</td><td>{1}</td></tr>
<tr><td>服务类型</td><td>{2}</td></tr>
</table>
"""
DOC_TAIL = """
</body>
</head>
</html>
"""

class NService(object):
    """docstring for NService"""
    def __init__(self, filename):
        super(NService, self).__init__()
        root = etree.parse(filename).getroot()
        basepath = os.path.dirname(filename)

        self.name = root.find('name').text
        self.service = root.find('service').find('name').text
        self.type = root.find('service').find('type').text.lower()

        self.objects = []
        for obj in root.findall('object'):
            self.objects.append(NObject(obj, basepath))

    def gencode(self, indir, outdir):
        """docstring for gencode"""
        for obj in self.objects:
            obj.gencode({}, indir, outdir)

        patterns = {}
        patterns['PACKAGE'] = self.name
        patterns['SERVICE'] = self.service
        patterns['SERVICE_TYPE'] = self.type
        patterns['SUBMAKEFILES'] = ' '.join(
                [obj.name.lower() + '/Makefile' for obj in self.objects])
        patterns['SUBDIRS'] = ' '.join(
                [obj.name.lower() for obj in self.objects])
        patterns['INIT_OBJECTS'] = '\n'.join(
                ['\t{0}_init(bus);'.format(obj.name.lower())
                    for obj in self.objects])
        patterns['OBJECT_HEADERS'] = '\n'.join(
                ['#include "{0}/{0}-object.h"'.format(obj.name.lower())
                    for obj in self.objects])
        patterns['OBJECT_LIBS'] = ' '.join(
                ['{0}/lib{0}.la'.format(obj.name.lower())
                    for obj in self.objects])
        patterns['REGISTER_OBJECTS'] = '\n'.join(
                [obj.reg_objs for obj in self.objects])

        parse_file(patterns, indir, outdir, 'configure.ac')
        parse_file(patterns, indir, outdir, 'main.c')
        parse_file(patterns, indir, outdir, 'Makefile.am.' + self.type,
                'Makefile.am')
        parse_file(patterns, indir, outdir, 'service.' + self.type,
                self.service + '.service.in')
        if self.type == 'system':
            parse_file(patterns, indir, outdir, 'package.conf',
                    self.name + '.conf')

    def gendoc(self, tbfile):
        """docstring for gendoc"""
        tbfile.write(DOC_HEAD.format(self.name, self.service, self.type))
        for obj in self.objects:
            obj.gendoc(tbfile)
        tbfile.write(DOC_TAIL)


