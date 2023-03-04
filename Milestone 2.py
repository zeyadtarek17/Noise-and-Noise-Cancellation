import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft

#setting the total song duration to 3 seconds
k=np.linspace(0,3,12*1024)

#creating an array for left and right hand frequencies ,  pressing start time and total pressing time for every note in the song
left=[0,246.93,0,220,196] #the right hand frequencies of 4th octave
right=[261.63,0,261.63,0,0] #the left hand frequencies of 3rd octave
Ti=[0,0.9,1.4,1.9,2.3] #pressing start time (0<=Ti<3)
Tf=[0.9,0.5,0.5,0.4,0.7] #Total pressing time

def music(k,right,left,Ti,Tf):
    f=np.zeros(np.shape(k))  #an array of zeros of length k
    # loop for traversing the arrays and resulting at the end the value of x(t) (summation of N pair of notes)
    for i in range(len(right)):
        #for each i, the values of f1,F1,ti,Ti will be substituted in the single tone generation formula
        f+=((np.sin(2*np.pi*left[i]*k))+(np.sin(2*np.pi*right[i]*k)))*((k>Ti[i])*(k<(Ti[i]+Tf[i])))
    return f
o=music(k,right,left,Ti,Tf)
sd.play(o, 3*1024)    
       
N= 3*1024
f= np.linspace(0,512,int(N/2))
xf=fft(o)
xf = (2/N)*np.abs(xf[0:np.int(N/2)])

f_n1,f_n2=np.random.randint(0,512,2)
randomnoise=np.sin(2*np.pi*f_n1*k)+np.sin(2*np.pi*f_n2*k)

#add the noise to sound 
add=randomnoise+o
addFun=fft(add)

#abs to remove complex part
addF=2/N * np.abs(addFun[0:np.int(N/2)])

#sort the arrays to get the highes 2 frequencies
sortAdd=np.sort(addF)

#Search for the two peeks > max peek in original and remove them
#search for them and restore their places -1,-2 predifined
addFn1=sortAdd[-1]
addFn2=sortAdd[-2]
#remove max from time domain instead of freq by transforming it inversely 

#FREQ DOMAIN to see peeks, differentiate between signal and  noise (x(t))
#noises that are less than max peek cannot be removed as you couldn't find them
#u(t) decides the interval
                                                                                                                                                                                            
#Get their place in freq domain (random+noise)
place1=np.where(addF==addFn1)
place2=np.where(addF==addFn2)

f1=round(f[place1[0][0]])
f2=round(f[place2[0][0]])

#remove noises that i rounded them
filterS=add-(np.sin(2*np.pi*f_n1*k)+np.sin(2*np.pi*f_n2*k))
filterSF=fft(filterS)
filterSF=2/N * np.abs(filterSF[0:np.int(N/2)])
sd.play(filterS,3*1024)

plt.figure()
plt.subplot(3,1,1)
plt.plot(k,o)

plt.subplot(3,1,2)
plt.plot(k,add)

plt.subplot(3,1,3)
plt.plot(k,filterS)

plt.figure()
plt.subplot(3,1,1)
plt.plot(f,xf)

plt.subplot(3,1,2)
plt.plot(f,addF)

plt.subplot(3,1,3)
plt.plot(f,filterSF)

