 
'''
Takes arguments: 
    time (whole seconds)
    sigma (noise width)
    fs (sampling rate)
    nWps (number of times Welch module is called per second)
    nf (length of FFT)
    DO NOT DETREND
'''
import numpy as np
import matplotlib.pylab as plt
from welch import welch
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from welch import welch
import sys
time = int(sys.argv[1])
sigma = float(sys.argv[2])
fs = int(sys.argv[3])
nWps = float(sys.argv[4])
nf = int(sys.argv[5])
noverlap = .5
def complexgen(time,sigma,fs):
    np.random.seed(0)
    realdata = np.random.normal(0,sigma,fs*time)
    #imagdata = np.random.normal(0,sigma,fs*time)*1j
    imagdata = np.zeros(len(realdata))
    data = np.add(realdata, imagdata)
    return data
def generate():
	fs = 10000.0
	f1 = 1234.0
	amp1 = 2*np.sqrt(2)
	f2 = 2500.2157
	amp2 = 1.
	ulsb = 1.e-3
	t = np.arange(fs*time) / fs
	waves = amp1*np.sin(t*(2*np.pi)*f1)+amp2*np.sin(t*(2*np.pi)*f2)
	noise = np.floor(waves/ulsb+.5)*ulsb
	data = waves + noise
	return data
def complexwav(time,sigma,fs):
    #np.random.seed(0)
    #realdata = np.random.normal(0,sigma,fs*time)
    #imagdata = np.random.normal(0,sigma,fs*time)*1j
    #t = np.arange(time*fs)/fs
    #amp1 = 2*np.sqrt(2)
    #amp2 = 1.
    #f1 = 1234.
    #f2 = 2500.
    #ulsb = 1.e-3
    #waves = (amp1*np.sin(t*(2*np.pi)*f1)
             #+amp2*np.sin(t*(2*np.pi)*f2))
    #wavimag = np.zeros(len(waves))*1j
    #wavc = np.add(waves,wavimag)
    #noise = np.floor(waves/ulsb+.5)*ulsb
    #nimag = np.zeros(len(noise))*1j
    #ncompx = np.add(noise,nimag)
    #data = wavc + ncompx
    #noise = np.add(realdata, imagdata)
    #data = noise + wavc
    a = generate()
    data = np.add(a,np.zeros(len(a))*1j)
    return data
sourcedata = complexgen(time,sigma,fs)
def test():
    tb = gr.top_block ()
    item_size = np.dtype("complex64").itemsize
    nData = int((1/nWps)*fs)
    s2v = blocks.stream_to_vector(item_size, nData)
    scale = 'density'
    src = blocks.vector_source_c(sourcedata)
    wel = welch(nData, scale, nf, fs, noverlap)
    dst = blocks.vector_sink_c(nf)
    tb.connect(src,s2v)
    tb.connect(s2v,wel)
    tb.connect(wel,dst)
    tb.run ()
    result = dst.data()
    return result
def test2():
    tb = gr.top_block ()
    sourcedata2 = complexwav(time,sigma,fs)
    item_size = np.dtype("complex64").itemsize
    nData = int((1/nWps)*fs)
    s2v = blocks.stream_to_vector(item_size, nData)
    scale = 'density'
    src = blocks.vector_source_c(sourcedata2)
    wel = welch(nData, scale, nf, fs, noverlap)
    dst = blocks.vector_sink_c(nf)
    tb.connect(src,s2v)
    tb.connect(s2v,wel)
    tb.connect(wel,dst)
    tb.run ()
    result = dst.data()
    return result
def testall():
    tb = gr.top_block ()
    item_size = np.dtype("complex64").itemsize
    nData = len(sourcedata)
    s2v = blocks.stream_to_vector(item_size, nData)
    scale = 'density'
    src = blocks.vector_source_c(sourcedata)
    wel = welch(nData, scale, nf, fs, noverlap)
    dst = blocks.vector_sink_c(nf)
    tb.connect(src,s2v)
    tb.connect(s2v,wel)
    tb.connect(wel,dst)
    tb.run ()
    result = dst.data()
    return result
noise = test()
waves = test2()
noise2 = testall()
navg = np.add(np.zeros(nf),np.zeros(nf)*1j)
c = 1
for n in range(0,time):
    navg = np.add(navg, noise[n*nf:c*nf])
    c = c + 1
wavg = np.add(np.zeros(nf),np.zeros(nf)*1j)
d = 1
for m in range(0,time):
    wavg = np.add(wavg,waves[m*nf:d*nf])
    d = d + 1
wavg = wavg/time
navg = navg/time
nametocall = 'fspectrum'+str(nf)+'.txt'
frange = np.genfromtxt(nametocall)
plt.figure(0)
plt.title('Data from 1 Welch method per second, 10 seconds')
plt.semilogy(noise,'c')
plt.savefig('alldata.svg')
plt.figure(2)
plt.title('Data from 1 Welch method over 10 seconds')
plt.semilogy(frange,np.sqrt(noise2),'r')
plt.savefig('longwelch.svg')
plt.figure(1)
plt.title('Data from 1 Welch method per second, 10 seconds, averaged')
plt.semilogy(frange,np.sqrt(navg),'g')
plt.savefig('average.svg')
plt.show()
h = len(wavg)/2
nonmir1 = wavg[:h]
nonmir2 = wavg[::-1]
nonmir3 = nonmir2[:h]
nonmir = np.add(nonmir1, nonmir3)
i = len(frange)/2
minirange = frange[i:]
plt.figure(4)
plt.title('Averaged Data from Welches, with signals')
plt.semilogy(minirange,(np.sqrt(nonmir)),'r')
plt.savefig('signal.svg')
plt.show()
