import numpy as np
import matplotlib.pyplot as plt


def LeastSquares(x, y, power=1):

    sumx = np.zeros(power * 2 + 1)
    sumxy = np.zeros(power + 1)

    for pow in range(power * 2 + 1):
        for j in range(len(x)):
            sumx[pow] += x[j] ** pow

    for pow in range(power + 1):
        for j in range(len(x)):
            sumxy[pow] += y[j] * x[j] ** pow

    A = np.zeros((power + 1, power + 1))


    for row in range(power + 1):
        for col in range(power + 1):
            A[row][col] = sumx[row + col]

    a = np.linalg.solve(A,sumxy)
    return a

def Horner(x, coeffs):
    n = len(coeffs)
    sum = coeffs[n-1]
    for i in range(n-2, -1, -1):
        sum = sum * x + coeffs[i]

    return sum

def PlotLeastSquares(x, y, power):
    a = LeastSquares(x, y, power)

    npoints = 201
    xvals = np.linspace(x[0], x[len(x)-1], npoints)
    yvals = np.zeros_like(xvals)

    for i in range(len((xvals))):
        yvals[i] = Horner(xvals[i],a)

    plt.plot(xvals, yvals)
    plt.plot(x,y,"ro")
    plt.show()

def main():
    x=np.array([.05,.11,.15,.31,.46,.52,.7,.74,.82,.98,1.17])


    y=np.array([.956,1.09,1.332,.717,.771,.539,.378,.370,.306,.242,.104])

    a = LeastSquares(x,y)
    print(a)
    PlotLeastSquares(x,y,1)

    a = LeastSquares(x,y,2)
    print("\n",a)
    PlotLeastSquares(x,y,2)

    a = LeastSquares(x, y, 3)
    print("\n", a)
    PlotLeastSquares(x, y, 3)

    a = LeastSquares(x,y,4)
    print("\n",a)
    PlotLeastSquares(x, y, 4)

    # power=1
    # PlotLeastSquares(np.array(x),np.array(y),power)
    #
    # power=3
    # PlotLeastSquares(np.array(x), np.array(y), power)

main()




