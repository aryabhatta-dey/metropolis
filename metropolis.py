import matplotlib.pyplot as plt
import numpy as np


def initialState(N):
    """
    Generate a random initial configuration
    """
    initialState = 2 * np.random.randint(2, size=(N, N)) - 1
    return initialState


def trialMove(config, beta, N):

    for i in range(N):
        for j in range(N):
            I = np.random.randint(0, N)
            J = np.random.randint(0, N)
            spin = config[I, J]
            neighbours = (
                config[(I + 1) % N, J]
                + config[I, (J + 1) % N]
                + config[(I - 1) % N, J]
                + config[I, (J - 1) % N]
            )

            cost = 2 * spin * neighbours

            if cost <= 0:
                spin *= -1
            elif np.exp(-cost * beta) > np.random.rand():
                spin *= -1

            config[I, J] = spin

    return config


def magSum(config):
    mSum = np.sum(config)
    return mSum


def main():

    N = 10  #  size of the lattice is NxN
    Tn = 50  #  number of temperature points

    Tlow, Thigh = 1, 4
    T = np.linspace(
        Tlow, Thigh, Tn
    )  # create an array of Tn size of temperature points in given temp range
    M = np.zeros(Tn)  # initialise an array of Tn size with zeros

    Neq = 250  #  Number of iterations for reaching equilibrium
    Nc = 500  #  Number of iterations for calculating magnetisation

    a = 1.0 / (Nc * N * N) # Normalization constant

    k = 1 # Boltzman constant; taking one for easier calculation of beta

    for i in range(Tn):

        config = initialState(N)  # initialise

        M1 = 0
        beta = 1.0 / (k * T[i])

        # try to reach equilibrium
        for j in range(Neq):
            trialMove(config, beta, N)

        # calculate sum of magnetisation
        for j in range(Nc):
            trialMove(config, beta, N)
            Mag = magSum(config)
            M1 = M1 + Mag

        M[i] = a * M1  # normalize

    fig = plt.figure()
    fig.add_subplot()
    plt.scatter(T, abs(M))
    plt.xlabel("Temperature")
    plt.ylabel("Magnetization")
    plt.axis('tight')
    plt.show()

if __name__ == "__main__":
    main()
