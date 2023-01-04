import numpy as np

#################################
#  ALGORITHM FOR APPROXIMATING  #
#       SOLUTIONS FOR ODE       #
#################################


# x0 -> The start of the interval
# xn -> The end of the interval
# h -> The step that we are taking
# fy0 -> The starting values
# odj -> The function

def eulerN(x0, xn, h, fy0, odj):
    x = np.arange(x0, xn+h, h)
    n = len(x)
    
    # Number of starting values should be the same as the order of the ODE
    order = len(fy0)

    #Initializing starting values
    fnX = np.empty([order, n])
    fnX[: , 0] = fy0.T

    for i in range (1, n):
        for j in range (order-1):
            fnX[j, i] = fnX[j, i - 1] + h*fnX[j + 1, i - 1]

        args = [x[i-1]]

        for i in range(len(fnX)):
            args.append(fnX[i, i - 1])
        
        fnX[order-1, i] = fnX[order-1, i - 1] + h*odj(*args)
    
    return fnX

    
    
