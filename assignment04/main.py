import matplotlib.pyplot as plt
import numpy as np


def p1(t):
    return (1/6) * t**3


def p2(t):
    return (1/6) * (1 + 3 * t + 3 * (t**2) - 3 * (t**3))


def p3(t):
    return (1/6) * (4 - 6 * (t**2) + 3 * (t**3))


def p4(t):
    return (1/6) * (1 - 3 * t + 3 * (t**2) - (t**3))


def b(t):
    if t < 0:
        return 0
    elif t <= 1:
        return p1(t)
    elif t <= 2:
        return p2(t - 1)
    elif t <= 3:
        return p3(t - 2)
    elif t <= 4:
        return p4(t - 3)
    else:
        return 0


def b_spline(x):
    return [b(t) for t in x]


if __name__ == '__main__':
    x = np.linspace(0, 4, 401)
    i = 1

    # plot Gaussian Function
    # plt.plot(x, 0.564 * np.exp(-(x - i)**2))

    # plot b-splines
    plt.plot(x, b_spline(x))

    plt.show()
