#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

LOGO_FILE = "/usr/share/pixmaps/plymouth-pardus.png"
THEMEPATH = "/usr/share/plymouth/themes"

# The end-start colors seems to be used by the two-step plugin
BASE_CONFIGURE_PARAMS = "--disable-tracing \
                         --with-logo=%s \
                         --with-release-file=/etc/pardus-release \
                         --with-background-color=0x000000 \
                         --with-background-end-color-stop=0x000000 \
                         --with-background-start-color-stop=0x000000 \
                         --with-system-root-install \
                         --with-boot-tty=/dev/tty7 \
                         --with-shutdown-tty=/dev/tty1 \
                         --with-log-viewer \
                         --disable-tests \
                         --disable-static \
                         --disable-gdm-transition \
                         --without-rhgb-compat-link \
                         --without-gdm-autostart-file \
                         --localstatedir=/var" % LOGO_FILE


def setup():
    autotools.autoreconf("-fis")
    autotools.configure(BASE_CONFIGURE_PARAMS)

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR='%s'" % get.installDIR())

    # Copy necessary files for Charge theme
    pisitools.dodir("%s/charge" % THEMEPATH)
    for f in ("box", "bullet", "entry", "lock"):
        shelltools.copy("%s%s/glow/%s.png" % (get.installDIR(), THEMEPATH, f), "%s%s/charge/" % (get.installDIR(), THEMEPATH))

    # Remove glow theme as it's premature
    pisitools.removeDir("/usr/share/plymouth/themes/glow")

    # Remove fedora scripts
    pisitools.remove("/usr/libexec/plymouth/*")

    # Generate initramfs filelist
    #shelltools.system("./generate-flist %s" % get.installDIR())

    pisitools.dodoc("TODO", "COPYING", "README", "ChangeLog")
