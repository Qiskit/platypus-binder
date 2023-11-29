# This code is a derivative work of the Qiskit Optimization Module
# ----------------------------------------------------------------

# This code is part of Qiskit.
#
# (C) Copyright IBM 2021, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Translator functions from a QuadraticProgram Object to a Qiskit Operator 
and today we only support an Operator in Sparse Pauli form

"""

import numpy as np
from qiskit.quantum_info import Pauli, SparsePauliOp

from ..quadratic_program import QuadraticProgram
from ..quadratic_program.exceptions import QuadraticProgramError



def qubo_to_sparse_pauli_op(qp: QuadraticProgram):
    """Return the Ising Hamiltonian of this problem.

    Variables are mapped to qubits in the same order, i.e.,
    i-th variable is mapped to i-th qubit.
    See https://github.com/Qiskit/qiskit-terra/issues/1148 for details.

    Returns:
        qubit_op: The qubit operator for the problem
        offset: The constant value in the Ising Hamiltonian.

    Raises:
        QuadraticProgramError: If a variable type is not binary.
        QuadraticProgramError: If constraints exist in the problem.
    """
    # if problem has variables that are not binary, raise an error
    if qp.get_num_vars() > qp.get_num_binary_vars():
        raise QuadraticProgramError(
            "The type of all variables must be binary. "
            "You can use Quadratic Program Passes"
            "to convert integer variables to binary variables. "
            "If the problem contains continuous variables this method does not work "
        )

    # if constraints exist, raise an error
    if qp.linear_constraints or qp.quadratic_constraints:
        raise QuadraticProgramError(
            "There must be no constraint in the problem. "
            "You can use Quadratic Program Passes"
            "to convert constraints to penalty terms of the objective function."
        )
    # initialize Hamiltonian.
    num_vars = qp.get_num_vars()
    pauli_list = []
    offset = 0.0
    zero = np.zeros(num_vars, dtype=bool)

    # set a sign corresponding to a maximized or minimized problem.
    # sign == 1 is for minimized problem. sign == -1 is for maximized problem.
    sense = qp.objective.sense.value

    # convert a constant part of the objective function into Hamiltonian.
    offset += qp.objective.constant * sense

    # convert linear parts of the objective function into Hamiltonian.
    for idx, coef in qp.objective.linear.to_dict().items():
        z_p = zero.copy()
        weight = coef * sense / 2
        z_p[idx] = True

        pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), -weight))
        offset += weight

    # create Pauli terms
    for (i, j), coeff in qp.objective.quadratic.to_dict().items():
        weight = coeff * sense / 4

        if i == j:
            offset += weight
        else:
            z_p = zero.copy()
            z_p[i] = True
            z_p[j] = True
            pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), weight))

        z_p = zero.copy()
        z_p[i] = True
        pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), -weight))

        z_p = zero.copy()
        z_p[j] = True
        pauli_list.append(SparsePauliOp(Pauli((z_p, zero)), -weight))

        offset += weight

    if pauli_list:
        # Remove paulis whose coefficients are zeros.
        qubit_op = sum(pauli_list).simplify(atol=0)
    else:
        # If there is no variable, we set num_nodes=1 so that qubit_op should be an operator.
        # If num_nodes=0, I^0 = 1 (int).
        num_vars = max(1, num_vars)
        qubit_op = SparsePauliOp("I" * num_vars, 0)

    return qubit_op, offset
