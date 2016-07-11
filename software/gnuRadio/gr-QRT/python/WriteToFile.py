#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
#Version 2

import numpy
from gnuradio import gr
import h5py
import datetime as dt

class WriteToFile(gr.sync_block):
    """
    docstring for block WriteToFile
    """
    def __init__(self, tname, nf, scale, fs, path):
        gr.sync_block.__init__(self,
            name="WriteToFile",
            in_sig=[(numpy.complex64, nf)],
            out_sig=None)
        #Carries over perameters
        self.tname = tname
        self.nf = nf
        self.scale = scale
        self.fs = fs
        self.path = path

    def work(self, input_items, output_items):
        in0 = input_items[0]
        #Accesses date and time
        date = dt.datetime.today()
        #Writes the file to specified path
        filename = str(self.path) + str(self.tname) + str(date.year) + str(date.month) + str(date.day) + str(date.hour) + '.hdf5'
        #Opens hdf file with read/write access
        f = h5py.File(filename, 'a')
        #Sets up hierarchy
        subgroup = str(date.minute)
        dset_name = str(date.second)
        time = (date.year,date.month,date.day,date.hour,date.minute,date.second)
        if subgroup+'/'+dset_name in f:
            #Writes data and metadata
            dset = f[subgroup+'/'+dset_name]
            dset.attrs['telescope'] = self.tname
            dset.attrs['date'] = time
            dset.attrs['scale'] = self.scale
            dset.attrs['fs'] = self.fs
            dset = dset[...] + in0[0]
        else:
            #Writes data and metadata
            dset = f.create_dataset(subgroup+'/'+dset_name,data=in0[0])
            dset.attrs['date'] = time
            dset.attrs['telescope'] = self.tname
            dset.attrs['scale'] = self.scale
            dset.attrs['fs'] = self.fs
        return len(input_items[0])

