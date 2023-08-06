import numpy as np
from qiskit import *
from qiskit_ibm_provider import IBMProvider
from qiskit.visualization import plot_histogram
import matplotlib.figure as fig
print("Imports Successful")

provider = IBMProvider()

def generic_qft(n):
    circuit = QuantumCircuit(n)
    for i in range(n-1,-1,-1):
        circuit.h(i)
        for j in range(i-1,-1,-1):
            circuit.cp(np.pi/float(2**(i-j)), j, i)
        circuit.barrier()
    for i in range(n//2):
        circuit.swap(i, n-i-1)
    return circuit


def bounded_qubits_qft(n, m):
    circuit = QuantumCircuit(n)
    for i in range(n-1,-1,-1):
        circuit.h(i)
        if i >= m:
            for j in range(i-1, i-m-1, -1):
                circuit.cp(np.pi/float(2**(i-j)), j, i)
        else:
            for j in range(i-1,-1,-1):
                circuit.cp(np.pi/float(2**(i-j)), j, i)
        circuit.barrier()
    for i in range(n//2):
        circuit.swap(i, n-i-1)
    return circuit

def generic_circuit(n, BE):
    h_cir = QuantumCircuit(n)
    for i in range(n):
        h_cir.h(i)
    qft_cir = generic_qft(n)
    g_cir = h_cir.compose(qft_cir)
    g_cir.measure_all()
    g_cir.draw(output='mpl', reverse_bits=True, filename='drawn_generic_circuit.png')
    backend = provider.get_backend(BE)
    transpiled = transpile(g_cir, backend)
    job = backend.run(transpiled, shots = 8000)
    counts = job.result().get_counts()
    plot = plot_histogram(counts)
    plot.savefig('results_generic_circuit_' + BE + '.png')
    
def bounded_circuit(n, m, BE):
    h_cir = QuantumCircuit(n)
    for i in range(n):
        h_cir.h(i)
    qft_cir = bounded_qubits_qft(n, m)
    b_cir = h_cir.compose(qft_cir)
    b_cir.measure_all()
    b_cir.draw(output='mpl', reverse_bits=True, filename='drawn_bounded_circuit.png')
    backend = provider.get_backend(BE)
    transpiled = transpile(b_cir, backend)
    job = backend.run(transpiled, shots = 8000)
    counts = job.result().get_counts()
    plot = plot_histogram(counts)
    plot.savefig('results_bounded_circuit_' + BE + '.png')

generic_circuit(5, 'simulator_statevector')
generic_circuit(5, 'ibmq_manila')

bounded_circuit(5, 2, 'simulator_statevector')
bounded_circuit(5, 2, 'ibmq_manila')