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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from welch import welch
import numpy as np
import matplotlib.pylab as plt

class qa_welch (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        src_data_real = np.genfromtxt('input2.txt')
        src_data_imag = np.zeros(len(src_data_real), dtype=np.float32)
	expected_result = np.genfromtxt('output2.txt')
        src_data = src_data_real + 1j*src_data_imag
        item_size = np.dtype("complex64").itemsize
        nData = len(src_data)
        s2v = blocks.stream_to_vector(item_size, nData)
	scale = 'density'
	nf = 1024
	fs = 10000
	src = blocks.vector_source_c(src_data)
	wel = welch(nData, scale, nf, fs)
	dst = blocks.vector_sink_c(nf)
	self.tb.connect(src, s2v)
        self.tb.connect(s2v, wel)
	self.tb.connect(wel, dst)
	self.tb.run ()
	result = dst.data()
	#self.assertFloatTuplesAlmostEqual(expected_result, result, 6)
        h = len(result)/2
        nonmir1 = result[:h]
        nonmir2 = result[::-1]
        nonmir3 = nonmir2[:h]
        nonmir = np.add(nonmir1, nonmir3)
        plt.semilogy(nonmir, color ='g')
        plt.semilogy(expected_result, color = 'r')
        plt.axhline(2/np.sqrt(2))
        plt.show()
        

if __name__ == '__main__':
    gr_unittest.run(qa_welch, "qa_welch.xml")
