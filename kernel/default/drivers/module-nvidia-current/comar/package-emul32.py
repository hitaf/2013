#!/usr/bin/python

import os

driver = "nvidia-current"
libdir = "/usr/lib32/%s" % driver
datadir = "/usr/share/%s" % driver

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    os.system("/usr/sbin/alternatives \
                --install   /usr/lib32/libGL.so.1.2  libGL-32bit   %(libdir)s/libGL.so.1.2     50 \
                --slave     /usr/lib32/xorg/modules/volatile xorg-modules-volatile   %(libdir)s/modules"
                % {"libdir": libdir, "datadir": datadir})

def preRemove():
    # FIXME This is not needed when upgrading package; but pisi does not
    #       provide a way to learn operation type.
    #os.system("/usr/sbin/alternatives --remove libGL-32bit %s/libGL.so.1.2" % libdir)
    pass