#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyleft 2012 Pardus ANKA Community
# Copyright 2005-2011 TUBITAK/UEAKE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "mozilla-release"

# Set object directory name correctly. This directory is specific to the build host, and its name is generated by
# value returned by config.guess script.
# config.guess returns 'x86_64-unknown-linux-gnu' on x86_64 machines, and 'i686-pc-linux-gnu' on x86 machines
ObjDir = "obj-%s-unknown-linux-gnu" % get.ARCH() if get.ARCH() == "x86_64" else "obj-%s-pc-linux-gnu" % get.ARCH()

locales = ["ca", "de", "es-AR", "es-ES", "fr", "hu", "it", "nl", "pl", "ru", "sv-SE", "tr"]

def setup():
    # Mozilla sticks on with autoconf-213
    shelltools.chmod("autoconf-213/autoconf-2.13", 0755)

    # Set job count for make
    pisitools.dosed(".mozconfig", "%%JOBS%%", get.makeJOBS())

    shelltools.system("/bin/bash ./autoconf-213/autoconf-2.13 --macro-dir=autoconf-213/m4")
    shelltools.cd("js/src")
    shelltools.system("/bin/bash ../../autoconf-213/autoconf-2.13 --macro-dir=../../autoconf-213/m4")
    shelltools.cd("../..")

    shelltools.makedirs(ObjDir)
    shelltools.cd(ObjDir)

    shelltools.system("../configure --prefix=/usr --libdir=/usr/lib --disable-strip --disable-install-strip") 

def build():
    # FIXME: Change library path and version with variables
    shelltools.export("LDFLAGS", "%s -Wl,-rpath,/usr/lib/%s-%s" % (get.LDFLAGS(), get.srcNAME(), get.srcVERSION()))

    shelltools.cd(ObjDir)
    autotools.make("-f ../client.mk build")

    # LOCALE
    # See: https://developer.mozilla.org/en/Creating_a_Language_Pack
    # FIXME: Find an elegant solution to create the Makefile from Makefile.in
    # We need to execute configure, otherwise the Makefile in browser/locales doesn't generate.
    # Don't execute it before "make -f client.mk". Otherwise it's conflicts with mozconfig
    # With 'make -f client.mk' call, build action takes place in $TOPSRCDIR/$OBJDIR by default. No need to specify l10n dir again, it's read from mozconfig

    autotools.make("-f ../client.mk configure")

    for locale in locales:
       autotools.make("-C browser/locales langpack-%s" % locale)

def install():
    autotools.rawInstall("-f client.mk DESTDIR=%s" % get.installDIR())

    # Any reason to do this renaming ?
    pisitools.rename("/usr/lib/%s-%s" % (get.srcNAME(), get.srcVERSION()), "MozillaFirefox")

    pisitools.remove("/usr/bin/firefox") # new Additional File  will replace that

    #install locales
    for locale in locales:
        pisitools.insinto("/usr/lib/MozillaFirefox/extensions/langpack-%s@firefox.mozilla.org" % locale, "%s/dist/xpi-stage/locale-%s/*" % (ObjDir, locale), sym=False)
        pisitools.removeDir("/usr/lib/MozillaFirefox/extensions/langpack-%s@firefox.mozilla.org/defaults" % locale)
        pisitools.remove("/usr/lib/MozillaFirefox/extensions/langpack-%s@firefox.mozilla.org/chrome/%s/locale/branding/browserconfig.properties" % (locale, locale))
        pisitools.dosym("../../../../../../browserconfig.properties", "/usr/lib/MozillaFirefox/extensions/langpack-%s@firefox.mozilla.org/chrome/%s/locale/branding/browserconfig.properties" % (locale, locale))

    pisitools.dodir("/usr/lib/MozillaFirefox/dictionaries")
    shelltools.touch("%s%s/dictionaries/tr-TR.aff" % (get.installDIR(), "/usr/lib/MozillaFirefox"))
    shelltools.touch("%s%s/dictionaries/tr-TR.dic" % (get.installDIR(), "/usr/lib/MozillaFirefox"))
    
    # Install fix language packs
    pisitools.insinto("/usr/lib/MozillaFirefox/extensions", "be.xpi")

    # Create profile dir, we'll copy bookmarks.html in post-install script
    pisitools.dodir("/usr/lib/MozillaFirefox/defaults/profile")

    # Install branding icon
    pisitools.insinto("/usr/share/pixmaps", "browser/branding/official/default256.png", "firefox.png")

    # Install docs
    pisitools.dodoc("LEGAL", "LICENSE")
