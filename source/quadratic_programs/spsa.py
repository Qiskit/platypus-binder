# This code is part of a Qiskit project.
#
# (C) Copyright IBM 2018, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Simultaneous Perturbation Stochastic Approximation (SPSA) optimizer.
"""

import numpy as np
from scipy.optimize import OptimizeResult

def minimize_spsa(func, x0, args=(), maxiter=100,
                  a=1.0, alpha=0.602, c=0.2, gamma=0.101,
                  callback=None):
    """
    Minimization of scalar function of one or more variables using simultaneous
    perturbation stochastic approximation (SPSA).

    Parameters:
        func (callable): The objective function to be minimized.

                          ``fun(x, *args) -> float``

                          where x is an 1-D array with shape (n,) and args is a
                          tuple of the fixed parameters needed to completely 
                          specify the function.

        x0 (ndarray): Initial guess. Array of real elements of size (n,), 
                      where ‘n’ is the number of independent variables.
      
        maxiter (int): Maximum number of iterations.  The number of function
                       evaluations is twice as many. Optional.

        a (float): SPSA gradient scaling parameter. Optional.

        alpha (float): SPSA gradient scaling exponent. Optional.

        c (float):  SPSA step size scaling parameter. Optional.
        
        gamma (float): SPSA step size scaling exponent. Optional.

        callback (callable): Function that accepts the current parameter vector
                             as input. Optional.

    Returns:
        OptimizeResult: Solution in SciPy Optimization format.

    Notes:
        See the `SPSA homepage <https://www.jhuapl.edu/SPSA/>`_ for usage and
        additional extentions to the basic version implimented here.
    """
    A = 0.01 * maxiter
    x0 = np.asarray(x0)
    x = x0

    for kk in range(maxiter):
        ak = a * (kk+1.0+A)**-alpha
        ck = c * (kk+1.0)**-gamma
        # Bernoulli distribution for randoms
        deltak =  2*np.random.randint(2, size=x.shape[0])-1
        grad = (func(x + ck*deltak, *args) - func(x - ck*deltak, *args)) / (2*ck*deltak)
        x -= ak*grad
        
        if callback is not None:
            callback(x)

    return OptimizeResult(fun=func(x, *args), x=x, nit=maxiter, nfev=2*maxiter, 
                          message='Optimization terminated successfully.',
                          success=True)
