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
import matplotlib.pylab as plt
import numpy
from gnuradio import gr
import scipy.signal as sp
class welch(gr.sync_block):
    """
    docstring for block welch
    """
    def __init__(self, nData, scale, nf, fs, noverlap):
        gr.sync_block.__init__(self,
            name="welch",
            in_sig=[(numpy.complex64, nData)],
            out_sig=[(numpy.complex64, nf)])
 	self.nData = nData
        self.scale = scale
        self.nf = nf
        self.fs = fs
        self.noverlap = noverlap


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for i in xrange (len(in0)):
            x = in0[i]
            f, pw = sp.welch(x,fs=self.fs,window='hann',
                         nperseg = self.nf,
                         noverlap=self.nf*self.noverlap,
                         scaling=self.scale,detrend=False)
            #fname = 'fspectrum'+str(self.nf)+'.txt'
            #numpy.savetxt(fname, f)
            out[i] = pw
        return len(output_items[0])
        (output_items[0])

