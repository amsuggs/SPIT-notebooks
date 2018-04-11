import numpy as np
import matplotlib.pyplot as plt
import math
import pickle
import datetime
import arg_parser as ap

params = ap.parse_args() #Read in flags and arguments. Stored as dot-accessible members in a namespace.
#Used in the quad_chirp call at the end of the file using the parameters gathered from the argument parser.

#Generates a quadratic chirp. Takes in number of samples, amplitude, 
#starting frequency, ending frequency, sample time, and pulse offset.
def quad_chirp(nr_samples=int(params.nr_samples), amp=float(params.amplitude), f0=int(params.begin), f1=int(params.end), t1=int(params.time), phi=int(params.phi)):
    #Calculation section.
    t=np.linspace(0,t1,nr_samples) #Array of samples.
    beta = (f1-f0)/(t1**2) #Change between start and end frequencies.
    ft = f0*t+beta*t**3/3 #Instantaneous frequency. Array.
    real = np.cos(2*np.pi*ft + phi) #Real component of the chirp.
    imag = np.sin(2*np.pi*ft + phi) #Imaginary component of the chirp.
    sig = amp*(real + 1j * imag) #Output signal. Real and imaginary components combined.
    
    #Plotting section.
    plt.figure(figsize=[10,4])
    plt.clf()
    plt.subplot(2,1,1)
    plt.title("Quadratic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1))
    plt.ylabel('Amplitude')
    plt.xlabel('time (sec)')
    plt.plot(t, sig.real)
    plt.plot(t, sig.imag)
    
    plt.subplot(2,1,2)
    plt.grid(True)
    
    plt.plot(t, ft, 'r')
    plt.show()
    
    gauss_pulse(chirp = sig, x = t) #Gauss pulse generation
    
def gauss_pulse(chirp, x, mean=0.5, std_dev=0.1):
    gauss = (1/math.sqrt(2*math.pi*std_dev**2))*(math.e**(-(x-mean)**2/(2*std_dev**2)))
    real = chirp.real*gauss
    imag = chirp.imag*gauss
    pulse = (real + 1j * imag)
    
    #Output file section.
    now = datetime.datetime.now()
    file_str = "PulsarSignalOutputs/" + params.output + "(%s).bin" % (now.isoformat()) #append the datetime to the end of the file.
    file = open(file_str, "wb")
    pickle.dump(pulse, file) #DUMP
    file.close()
    
    #Plotting section.
    plt.subplot(1,1,1)
    plt.title("Gaussian pulse")
    plt.plot(pulse.real)
    plt.plot(pulse.imag)
    plt.show()
    
quad_chirp()