import numpy as np
import matplotlib.pyplot as plt

# x0 -> The start of the interval
# xn -> The end of the interval
# h -> The step that we are taking
# fy0 -> The starting values
# odj -> The function

def rk4(a, b, h, nfX0, dnfX):
    x = np.arange(a, b+h, h)
    n = len(x)
    order = len(nfX0)
    fnX = np.empty([order, n])
    fnX[:, 0] = nfX0.T
    k1,k2, k3, k4 = np.empty((1,order)), np.empty((1,order)), np.empty((1,order)), np.empty((1,order))
    for it in range(1, n):
        # k1
        for itOrder in range(order-1):
            k1[0,itOrder] = fnX[itOrder + 1, it - 1]

        args = [x[it-1]]

        for i in range(len(fnX)):
            args.append(fnX[i, it - 1])

        k1[0,order-1] = dnfX(*args)
        
        # k2
        for itOrder in range(order - 1):
            k2[0,itOrder] = fnX[itOrder + 1, it - 1] + h/2*k1[0,itOrder + 1]
       
        args = [x[it-1]+ h/2]
      
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1]+ h/2*k1[j][0])
           
        k2[0,order-1] = dnfX(*args)

        # k3
        for itOrder in range(order - 1):
            k3[0,itOrder] = fnX[itOrder + 1, it - 1] + h/2*k2[0,itOrder + 1]

        args = [x[it-1]+ h/2]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1]+ h/2*k2[j][0])        
        k3[0,order-1] = dnfX(*args)
         
        # k4
        for itOrder in range(order - 1):
            k4[0,itOrder] = fnX[itOrder + 1, it - 1] + h*k3[0,itOrder + 1]

        args = [x[it-1]+ h]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1]+  h*k3[j][0])   
     
        k4[0,order-1] = dnfX(*args)

        for itOrder in range(order):
            fnX[itOrder, it] = fnX[itOrder, it - 1] + h/6*(k1[0,itOrder] + 2*k2[0,itOrder] + 2*k3[0,itOrder] + k4[0,itOrder])
       
    
    return fnX
