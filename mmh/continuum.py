#!/usr/bin/env python
# encoding: utf-8

__author__ = 'michael'

import bisect
import threading
from mmh import hash_f


class _Point(object):
    def __init__(self, value, desc):
        self.value = value
        self.desc = desc

    def __str__(self):
        return '_Point(%d,%s)' % (self.value, self.desc)

    def __cmp__(self, other):
        return self.value - other.value


class Continuum(object):
    def __init__(self, name):
        self.name = name
        self.continuum_lock = threading.Lock()
        self.points = []
        self.desc_capacity = {} # desc:capacity

    def get_name(self):
        return self.name

    def Size(self):
        with self.continuum_lock:
            return len(self.points)

    def Locate(self, hash):
        with self.continuum_lock:
            if not self.points:
                return None
            p = _Point(hash, "")
            i = bisect.bisect_right(self.points, p)
            point_size = len(self.points)
            if i != point_size:
                return self.points[i % point_size].desc
            else:
                return self.points[0].desc

    def Rebuild(self):
        self.continuum_lock.acquire()
        try:
            total_value = 0
            for v in self.desc_capacity.itervalues():
                total_value += v

            if total_value == 0:
                return False

            new_points = []
            for desc, val in self.desc_capacity.iteritems():
                for i in range(val):
                    replicated_desc = '%s-%x' % (desc, i) # very important!!!
                    hash_value = Continuum.Hash(replicated_desc)
                    bisect.insort(new_points, _Point(hash_value, desc))  # very important!!!
            del self.points[:]
            self.points = new_points
        finally:
            self.continuum_lock.release()
        return True

    def Add(self, desc, capacity):
        with self.continuum_lock:
            self.desc_capacity[desc] = capacity

    def Remove(self, desc):
        with self.continuum_lock:
            if desc in self.desc_capacity:
                del self.desc_capacity[desc]

    def Clear(self):
        with self.continuum_lock:
            self.desc_capacity.clear()

    @staticmethod
    def Hash(str):
        return hash_f.get_unsigned_hash32(str, len(str), 0)
