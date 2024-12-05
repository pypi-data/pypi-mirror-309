# coding: utf-8
from __future__ import print_function, unicode_literals

import argparse
import os
import re
import time

from .__init__ import ANYWIN, MACOS
from .authsrv import AXS, VFS
from .bos import bos
from .util import chkcmd, min_ex, undot

class Fstab(object):
    def __init__(self, log , args ):
        self.log_func = log

        self.warned = False
        self.trusted = False
        self.tab  = None
        self.oldtab  = None
        self.srctab = "a"
        self.cache   = {}
        self.age = 0.0
        self.maxage = args.mtab_age

    def log(self, msg , c   = 0)  :
        self.log_func("fstab", msg, c)

    def get(self, path )  :
        now = time.time()
        if now - self.age > self.maxage or len(self.cache) > 9000:
            self.age = now
            self.oldtab = self.tab or self.oldtab
            self.tab = None
            self.cache = {}

        fs = "ext4"
        msg = "failed to determine filesystem at [{}]; assuming {}\n{}"

        if ANYWIN:
            fs = "vfat"
            try:
                path = self._winpath(path)
            except:
                self.log(msg.format(path, fs, min_ex()), 3)
                return fs

        path = undot(path)
        try:
            return self.cache[path]
        except:
            pass

        try:
            fs = self.get_w32(path) if ANYWIN else self.get_unix(path)
        except:
            self.log(msg.format(path, fs, min_ex()), 3)

        fs = fs.lower()
        self.cache[path] = fs
        self.log("found {} at {}".format(fs, path))
        return fs

    def _winpath(self, path )  :
        # try to combine volume-label + st_dev (vsn)
        path = path.replace("/", "\\")
        vid = path.split(":", 1)[0].strip("\\").split("\\", 1)[0]
        try:
            return "{}*{}".format(vid, bos.stat(path).st_dev)
        except:
            return vid

    def build_fallback(self)  :
        self.tab = VFS(self.log_func, "idk", "/", AXS(), {})
        self.trusted = False

    def build_tab(self)  :
        self.log("inspecting mtab for changes")

        sptn = r"^.*? on (.*) type ([^ ]+) \(.*"
        if MACOS:
            sptn = r"^.*? on (.*) \(([^ ]+), .*"

        ptn = re.compile(sptn)
        so, _ = chkcmd(["mount"])
        tab1   = []
        atab = []
        for ln in so.split("\n"):
            m = ptn.match(ln)
            if not m:
                continue

            zs1, zs2 = m.groups()
            tab1.append((str(zs1), str(zs2)))
            atab.append(ln)

        # keep empirically-correct values if mounttab unchanged
        srctab = "\n".join(sorted(atab))
        if srctab == self.srctab:
            self.tab = self.oldtab
            return

        self.log("mtab has changed; reevaluating support for sparse files")

        tab1.sort(key=lambda x: (len(x[0]), x[0]))
        path1, fs1 = tab1[0]
        tab = VFS(self.log_func, fs1, path1, AXS(), {})
        for path, fs in tab1[1:]:
            tab.add(fs, path.lstrip("/"))

        self.tab = tab
        self.srctab = srctab

    def relabel(self, path , nval )  :
        self.cache = {}
        if ANYWIN:
            path = self._winpath(path)

        path = undot(path)
        ptn = re.compile(r"^[^\\/]*")
        vn, rem = self.tab._find(path)
        if not self.trusted:
            # no mtab access; have to build as we go
            if "/" in rem:
                self.tab.add("idk", os.path.join(vn.vpath, rem.split("/")[0]))
            if rem:
                self.tab.add(nval, path)
            else:
                vn.realpath = nval

            return

        visit = [vn]
        while visit:
            vn = visit.pop()
            vn.realpath = ptn.sub(nval, vn.realpath)
            visit.extend(list(vn.nodes.values()))

    def get_unix(self, path )  :
        if not self.tab:
            try:
                self.build_tab()
                self.trusted = True
            except:
                # prisonparty or other restrictive environment
                if not self.warned:
                    self.warned = True
                    self.log("failed to build tab:\n{}".format(min_ex()), 3)
                self.build_fallback()

        ret = self.tab._find(path)[0]
        if self.trusted or path == ret.vpath:
            return ret.realpath.split("/")[0]
        else:
            return "idk"

    def get_w32(self, path )  :
        if not self.tab:
            self.build_fallback()

        ret = self.tab._find(path)[0]
        return ret.realpath
