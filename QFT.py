import numpy as np
from qiskit import *
from qiskit_ibm_provider import IBMProvider
from qiskit.visualization import plot_histogram
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

def generic_circuit(n, BE, l):
    h_cir = QuantumCircuit(n)
    for i in range(n):
        h_cir.h(i)
    qft_cir = generic_qft(n)
    g_cir = h_cir.compose(qft_cir)
    g_cir.measure_all()
    g_cir.draw(output='mpl', reverse_bits=True, filename='pic_generic_q=' + str(n) + '.png')
    backend = provider.get_backend(BE)
    transpiled = transpile(g_cir, backend)
    job = backend.run(transpiled, shots = 8000)
    counts = job.result().get_counts()
    plot = plot_histogram(counts, figsize=(l, 11))
    plot.savefig('res_generic_' + BE + '_q=' + str(n) + '.png')
    
def bounded_circuit(n, m, BE, l):
    h_cir = QuantumCircuit(n)
    for i in range(n):
        h_cir.h(i)
    qft_cir = bounded_qubits_qft(n, m)
    b_cir = h_cir.compose(qft_cir)
    b_cir.measure_all()
    b_cir.draw(output='mpl', reverse_bits=True, filename='pic_bounded_q=' + str(n) + '_b=' + str(m) + '.png')
    backend = provider.get_backend(BE)
    transpiled = transpile(b_cir, backend)
    job = backend.run(transpiled, shots = 8000)
    counts = job.result().get_counts()
    plot = plot_histogram(counts, figsize=(l, 11))
    plot.savefig('res_bounded_' + BE + '_q=' + str(n) + '_b=' + str(m) + '.png')

generic_circuit(3, 'simulator_statevector', 20)
generic_circuit(3, 'ibm_lagos', 20)
print(3)

bounded_circuit(3, 1, 'simulator_statevector', 20)
bounded_circuit(3, 1, 'ibm_lagos', 20)
print(3, 1)
print("3 qubits done")

generic_circuit(4, 'simulator_statevector', 23)
generic_circuit(4, 'ibm_lagos', 23)
print(4)

bounded_circuit(4, 1, 'simulator_statevector', 23)
bounded_circuit(4, 1, 'ibm_lagos', 23)
print(4, 1)

bounded_circuit(4, 2, 'simulator_statevector', 23)
bounded_circuit(4, 2, 'ibm_lagos', 23)
print(4, 2)
print("4 qubits done")

generic_circuit(5, 'simulator_statevector', 25)
generic_circuit(5, 'ibm_lagos', 25)
print(5)

bounded_circuit(5, 1, 'simulator_statevector', 25)
bounded_circuit(5, 1, 'ibm_lagos', 25)
print(5, 1)

bounded_circuit(5, 2, 'simulator_statevector', 25)
bounded_circuit(5, 2, 'ibm_lagos', 25)
print(5, 2)

bounded_circuit(5, 3, 'simulator_statevector', 25)
bounded_circuit(5, 3, 'ibm_lagos', 25)
print(5, 3)
print("5 qubits done")

generic_circuit(6, 'simulator_statevector', 28)
generic_circuit(6, 'ibm_lagos', 28)
print(6)

bounded_circuit(6, 1, 'simulator_statevector', 28)
bounded_circuit(6, 1, 'ibm_lagos', 28)
print(6, 1)

bounded_circuit(6, 2, 'simulator_statevector', 28)
bounded_circuit(6, 2, 'ibm_lagos', 28)
print(6, 2)

bounded_circuit(6, 3, 'simulator_statevector', 28)
bounded_circuit(6, 3, 'ibm_lagos', 28)
print(6, 3)

bounded_circuit(6, 4, 'simulator_statevector', 28)
bounded_circuit(6, 4, 'ibm_lagos', 28)
print(6, 4)
print("6 qubits done")

generic_circuit(7, 'simulator_statevector', 30)
generic_circuit(7, 'ibm_lagos', 30)
print(7)

bounded_circuit(7, 1, 'simulator_statevector', 30)
bounded_circuit(7, 1, 'ibm_lagos', 30)
print(7, 1)

bounded_circuit(7, 2, 'simulator_statevector', 30)
bounded_circuit(7, 2, 'ibm_lagos', 30)
print(7, 2)

bounded_circuit(7, 3, 'simulator_statevector', 30)
bounded_circuit(7, 3, 'ibm_lagos', 30)
print(7, 3)

bounded_circuit(7, 4, 'simulator_statevector', 30)
bounded_circuit(7, 4, 'ibm_lagos', 30)
print(7, 4)

bounded_circuit(7, 5, 'simulator_statevector', 30)
bounded_circuit(7, 5, 'ibm_lagos', 30)
print(7, 5)
print("7 qubits done")
