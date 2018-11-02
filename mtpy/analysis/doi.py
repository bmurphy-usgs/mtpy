"""
Description:
    calculate Sensitivity value as function of Bostick depth of investigation.
Author: fei.zhang@ga.gov.au

Date: 2017-07-14
"""

import numpy as np
import math
import cmath

import matplotlib

# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

mu0 = 4*math.pi*math.pow(10,-7)

def bostick_depth(f, rho):
    """
    :param f: freq
    :param rho: apparent resistivity
    :return:
    """
    h = (rho/(f*2*math.pi*mu0))**0.5

    #print(h)
    return h


def bostick_resistivity(f, rho, pha):
    """
    :param f:  f is not used?
    :param rho:
    :param pha: phase in radian
    :return:
    """
    if pha > 2*math.pi:
        print("WARN: pha is too large, in unit degree? ", pha)
        pha_rad = pha * math.pi / 180.0
    else:
        pha_rad=pha

    rho_b = rho*(math.pi / (2 * pha_rad) - 1)
    print(rho_b)
    return rho_b


# def sensitivity(z, sigma_conduct=0.01, freq=0.01):
def sensitivity(z, sigma_conduct=100.0, freq=10.0):
    """
    compute sensitivty S(z,sigma, omega)= -kz*exp(-2*kz).
    The result is independent of sigma and freq.
    :param z:
    :param sigma_conduct:
    :param freq:
    :return: the sensitivity vslue
    """

    omega= 2*math.pi*freq

    k = cmath.sqrt( (0.0+1j)*omega*mu0*sigma_conduct )

    p=1/np.real(k)  #It is the same as delta=sqrt(2/mu0*sigma*omega)

    # print ("k and p = ", k, p)
    zp=z*p  # zp is normalized Z
    sen = -k*zp*cmath.exp(-2*k*zp)
    #print (z, sen)
    return sen

# ===========================================
if __name__ == "__main__":

    for n in xrange(0,36):
        zn = 0.1*n
        sen = sensitivity(zn, sigma_conduct=10.0, freq=1.0)
        #print (zn, sen)  # sen is a complex value
        print "%s, %s" % (zn, np.absolute(sen))


    # Below show that the sensitivity is indepedent of freq and conductivty !!!!

    zn_list=0.1*np.array(range(0,40))
    sens_list = [np.absolute(sensitivity(zn, sigma_conduct=0.20, freq=10)) for zn in zn_list]
    sens_list2= [np.absolute(sensitivity(zn, sigma_conduct=2000.0, freq=0.1)) for zn in zn_list]

    plt.plot(zn_list, sens_list)
    plt.plot(zn_list, sens_list2, '^', color='r')

    plt.title("Depth of Investigation (DOI)")
    plt.ylabel("Sensitivity")
    plt.xlabel("Normalized Penetration Depth")
    plt.show()

