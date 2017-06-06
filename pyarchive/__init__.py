# -*- coding: utf-8 -*-
from lxml import etree

import subprocess
import os

def main():
    tree = etree.parse("EuterpiaRadio_files.xml")
    for f in tree.xpath('/files/file'):
        source = f.get("source")
        if source == "original":
            name = f.get("name")
            d = os.path.dirname(name)
            if d is not "":
                subprocess.Popen('mkdir -p %s' % d, shell=True).communicate()
            cmd = 'curl -L https://archive.org/download/EuterpiaRadio/%s -o %s' % (name, name)
            print cmd
            print ""
            (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
            print ""
