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
# Version 1

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from welch import welch
import numpy as np
import matplotlib.pylab as plt
import scipy.signal as sp

class qa_welch (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        def generate(inputs):
            # Generates data to test with
            fs = 10000.0
            f1 = 1234.0
            amp1 = 2*np.sqrt(2)
            f2 = 2500.2157
            amp2 = 1.
            ulsb = 1.e-3
            t = np.arange(inputs) / fs
            waves = amp1*np.sin(t*(2*np.pi)*f1)+amp2*np.sin(t*(2*np.pi)*f2)
            noise = np.floor(waves/ulsb+.5)*ulsb
            data = waves + noise
            return data
        rdata = generate(10000)
        # Makes data complex
        idata = np.zeros(len(rdata))*1j
        src_data = np.add(rdata,idata)
        # Defines perameters
        nf = 1024
        fs = 10000
        scale = 'density'
        nperseg = nf
        avg = 'False'
        avgn = 1
        # Processes data with Welch method using scipy.signal.welch command
        freq, expected_result = sp.welch(src_data,fs=10000,
                          window='hann',nperseg=nperseg,
                          noverlap=nf*.5,scaling=scale,detrend=False)
        item_size = np.dtype("complex64").itemsize
        nData = len(src_data)
        # Sends the source data through the welch module
        s2v = blocks.stream_to_vector(item_size, nData)
        src = blocks.vector_source_c(src_data)
        wel = welch(nData, scale, nf, fs, .5, avg, avgn)
        dst = blocks.vector_sink_c(nf)
        self.tb.connect(src, s2v)
        self.tb.connect(s2v, wel)
        self.tb.connect(wel, dst)
        self.tb.run ()
        result = dst.data()
        # Checks welch module with scipy.signal.welch
        self.assertFloatTuplesAlmostEqual(expected_result, result, 5)
    def test_001_t (self):
        def generate(inputs):
            # Generates data to test with
            fs = 10000.0
            f1 = 1234.0
            amp1 = 2*np.sqrt(2)
            f2 = 2500.2157
            amp2 = 1.
            ulsb = 1.e-3
            t = np.arange(inputs) / fs
            waves = amp1*np.sin(t*(2*np.pi)*f1)+amp2*np.sin(t*(2*np.pi)*f2)
            noise = np.floor(waves/ulsb+.5)*ulsb
            data = waves + noise
            return data
        rdata = generate(100000)
        # Makes data complex
        idata = np.zeros(len(rdata))*1j
        src_data = np.add(rdata,idata)
        # Defines perameters
        nf = 1024
        fs = 10000
        scale = 'density'
        nperseg = nf
        avg = 'True'
        avgn = 10
        # Processes data with Welch method using scipy.signal.welch command
        avg = np.add(np.zeros(nData),np.zeros(nData)*1.j)
        for a in np.arange(avgn)
            low = a*nData
            high = (a+1)*nData
            avg = np.add(avg,src_data[low:high])
        avg = avg/nData
        freq, expected_result = sp.welch(avg,fs=10000,
                                window='hann',nperseg=nperseg,
                                noverlap=nf*.5,scaling=scale,detrend=False)
        item_size = np.dtype("complex64").itemsize
        nData = len(src_data)
        # Sends the source data through the welch module
        s2v = blocks.stream_to_vector(item_size, nData)
        src = blocks.vector_source_c(src_data)
        wel = welch(nData, scale, nf, fs, .5, avg, avgn)
        dst = blocks.vector_sink_c(nf)
        self.tb.connect(src, s2v)
        self.tb.connect(s2v, wel)
        self.tb.connect(wel, dst)
        self.tb.run ()
        result = dst.data()
        # Checks welch module with scipy.signal.welch
        self.assertFloatTuplesAlmostEqual(expected_result, result, 5)

if __name__ == '__main__':
    gr_unittest.run(qa_welch, "qa_welch.xml")
