import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

k=np.linspace(0,3,12*1024)

left=[0,246.93,0,220,196]
right=[261.63,0,261.63,0,0]
Ti=[0,0.9,1.4,1.9,2.3]
Tf=[0.9,0.5,0.5,0.4,3]

def music(k,right,left,Ti,Tf):
    f=np.zeros(np.shape(k))
    for i in range(len(right)):
        f+=((np.sin(2*np.pi*left[i]*k))+(np.sin(2*np.pi*right[i]*k)))*((k>Ti[i])*(k<(Ti[i]+Tf[i])))
    return f
o=music(k,right,left,Ti,Tf)
sd.play(o, 3*1024)    