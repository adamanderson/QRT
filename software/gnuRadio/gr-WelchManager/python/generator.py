import numpy as np
import matplotlib.pylab as plt
import scipy as sp
from scipy.signal import welch
def generate(inputs):
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
a = generate(10000)
#print a
#print len(a)
np.savetxt('generatedstuff.txt', a) 
#fig1 = plt.plot(a)
#plt.show(fig1)
nperseg = 10000
scale = 'density'
src = np.genfromtxt('input2.txt')
comp = src + 1j*np.zeros(len(src))
freq, pow = welch(comp,fs=10000,window='hann',nperseg=nperseg,noverlap=nperseg/2,scaling=scale)
#print freq
#print pow
#a0 = zip(freq, pow)
np.savetxt('power.txt', pow)
np.savetxt('freq.txt', freq)
plt.semilogy(freq, np.sqrt(pow), color='r')
#plt.semilogy(*zip(*a0), color='cyan')
#plt.axhline(2*np.sqrt(2), color = 'g')
#plt.axhline(1, color='c')
plt.savefig('generatorprogramfft.svg')
plt.show()
