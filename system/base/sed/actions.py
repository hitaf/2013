#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure()

def build():
    autotools.make("LDFLAGS=%s" % get.LDFLAGS())

def check():
    autotools.make("check")

def install():
    autotools.install()

    pisitools.dodoc("NEWS", "README*", "THANKS", "AUTHORS", "BUGS", "ChangeLog")
