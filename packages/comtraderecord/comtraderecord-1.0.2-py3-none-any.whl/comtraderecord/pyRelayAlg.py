import numpy as np
import math

def fourier(data, SamplePoint, N=1, har = 1):
    """
    The N periods Fourier transform with array data
    Return complex value of Fourier, please use abs() to get magnitude and angle() to get angle    

    Parameters
    ----------
    data:           Source data array
    SamplePoint:    SamplePoint per cycle
    N:              N periods fourier, default is one period fourier
    har:            Harmonic order, default is fundamental

    Example
    ----------
     - Full period fourier
       IA = fourier(sampleIA,SamplePoint);
     - 2 periods fourier
       IA = fourier(sampleIA,SamplePoint,2);
     - 2 periods fourier for 3 order harmonic
       UA = fourier(sampleUA,SamplePoint,2,3);
    """

    SamplePointNP = SamplePoint*N
    # n = np.arange(SamplePointNP) + 0.5
    n = np.arange(SamplePointNP) - 1
    
    # fourier coefficent
    ys = np.cos(2*har*np.pi*n/SamplePoint)
    yc = np.sin(2*har*np.pi*n/SamplePoint)

    RecEnd = len(data)
    Rel = np.zeros(RecEnd)
    Imag = np.zeros(RecEnd)    
    for i in range(SamplePointNP,RecEnd):
        sig = data[i-SamplePointNP:i]
        yc = np.roll(yc,-1)
        ys = np.roll(ys,-1)
        Rel[i]  = sum(yc*sig)/(SamplePointNP)
        Imag[i] = sum(ys*sig)/(SamplePointNP)

    Rel[0:SamplePointNP]  = Rel[SamplePointNP]
    Imag[0:SamplePointNP] = Imag[SamplePointNP]

    FF = math.sqrt(2)*(Rel + Imag*1j)

    return FF

def fourierTrack(data, SampleRate, ftrack):
    RecEnd = len(data)
    Rel = np.zeros(RecEnd)
    Imag = np.zeros(RecEnd)    
    recStart = 200
    for i in range(recStart,RecEnd):
        SamplePoint = int(SampleRate/ftrack[i])
        n = np.arange(SamplePoint) + 0.5

        # fourier coefficent
        ys = np.cos(2*np.pi*n/SamplePoint)
        yc = np.sin(2*np.pi*n/SamplePoint)        
        sig = data[i-SamplePoint:i]
        Rel[i]  = sum(yc*sig)/(SamplePoint)
        Imag[i] = sum(ys*sig)/(SamplePoint)

    Rel[0:recStart]  = Rel[recStart]
    Imag[0:recStart] = Imag[recStart]

    FF = math.sqrt(2)*(Rel + Imag*1j)

    return FF

def TrueRMS(data, SamplePoint):
    """
    Return true RMS value of one analog channel   

    Parameters
    ----------
    data:           Source data array
    SamplePoint:    SamplePoint per cycle
    """
    
    RecEnd = len(data)  
    RMSData = np.zeros(len(data))  
    
    for k in range(SamplePoint,RecEnd):  
        onePeriodData = data[k-SamplePoint:k] # One period sample data  
        RMSData[k] = math.sqrt(sum(onePeriodData**2)/SamplePoint)  
    
    RMSData[0:SamplePoint]  = RMSData[SamplePoint]

    return RMSData


def PosSequence(Va, Vb, Vc):
    """
    Return positive seuqnce analog with complex value
    """

    a = np.exp(2j*np.pi/3)
    return (Va + a*Vb + a**2*Vc)/3

def NegSequence(Va, Vb, Vc):
    """
    Return negative seuqnce analog with complex value
    """

    a = np.exp(2j*np.pi/3)
    return (Va + a**2*Vb + a*Vc)/3

def ZeroSequence(Va, Vb, Vc):
    """
    Return zero seuqnce analog with complex value
    """

    return Va + Vb + Vc