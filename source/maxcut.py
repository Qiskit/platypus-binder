import numpy as np
import rustworkx as rx
from qiskit.circuit import ClassicalRegister
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Estimator, Sampler
from docplex.mp.model import Model
from quantum_serverless import get_arguments, save_result

from quadratic_programs.spsa import minimize_spsa
from quadratic_programs.translators import docplex_mp_to_qp, qubo_to_sparse_pauli_op
from quadratic_programs.workflows import QuadraticProgramConverter, QuadraticProgramPostprocess

# Step 1: Mapping the classical input to a quantum representation
def map_to_quantum(G):
    mdl = Model(name="Max-cut")
    x = {i: mdl.binary_var(name=f"x_{i}") for i in range(G.num_nodes())}
    objective = mdl.sum(
        w * x[i] * (1 - x[j]) + w * x[j] * (1 - x[i])
        for i, j, w in G.weighted_edge_list()
    )
    mdl.maximize(objective)
    qp = docplex_mp_to_qp(mdl)

    quadratic_transformer = QuadraticProgramConverter()
    qubo = quadratic_transformer.run(qp)
    hamiltonian, offset = qubo_to_sparse_pauli_op(qubo)
    ansatz = RealAmplitudes(hamiltonian.num_qubits, entanglement="linear", reps=2)

    return ansatz, hamiltonian, qubo, quadratic_transformer

# Step 2: Optimize the circuit
def optimize_for_backend(ansatz, hamiltonian):
    # We will not use real hardware in remote execution. 
    return ansatz, hamiltonian

# Step 3: Execute using Qiskit Runtime Primitive
def execute(ansatz_ibm, observable_ibm):
    def cost_func(params, ansatz, hamiltonian, estimator):
        """Ground state energy evaluation."""
        cost = (
            estimator.run(ansatz, hamiltonian, parameter_values=params)
            .result()
            .values[0]
        )
        return cost

    x0 = 2 * np.pi * np.random.random(size=ansatz_ibm.num_parameters)
    estimator = Estimator()
    res = minimize_spsa(
        cost_func, x0, args=(ansatz_ibm, observable_ibm, estimator), maxiter=100
    )
    ansatz_opt = ansatz_ibm.assign_parameters(res.x)
    sampler = Sampler()
    ansatz_opt.measure_all()
    quasi_dist = sampler.run(ansatz_opt).result().quasi_dists[0]

    return quasi_dist

# Step 4: Post-processing results
def postprocess(quasi_dist, qubo, quadratic_transformer):
    return QuadraticProgramPostprocess(qubo, quadratic_transformer).run(quasi_dist)


# Get input argument
arguments = get_arguments()
matrix = arguments.get("graph")
graph = rx.PyGraph.from_adjacency_matrix(matrix)

# Execute the Qiskit pattern
ansatz, hamiltonian, qubo, quadratic_transformer = map_to_quantum(graph)
ansatz_opt, hamiltonian_opt = optimize_for_backend(ansatz, hamiltonian)
quasi_dist = execute(ansatz_opt, hamiltonian_opt)
solution = postprocess(quasi_dist, qubo, quadratic_transformer)

# Save MaxCut solution
save_result({"solution": solution})
