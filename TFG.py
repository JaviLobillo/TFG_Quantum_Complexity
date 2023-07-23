import numpy as np
import time
from qiskit import QuantumCircuit, transpile
from math import gcd
from fractions import Fraction
from qiskit_ibm_provider import IBMProvider
print("Imports Successful")

#Javier Lobillo Olmedo. Bachelor's Thesis. 2022/2023
#In this file we will compare the time it takes to run Shor's algorithm in different backends of IBMQ.
#The code is based on the code given in the Qiskit textbook: https://learn.qiskit.org/course/ch-algorithms/shors-algorithm

provider = IBMProvider()



N_COUNT = 8  # number of counting qubits
N = 15   # number to factorize
a = 7   # a^2 mod 15 = 1, so a = 4,7,11,13 are the valid values

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13")
    U = QuantumCircuit(4)
    for _iteration in range(power):
        if a in [2,13]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [7,8]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [4, 11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U

def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

"""
# Create QuantumCircuit with N_COUNT counting qubits
# plus 4 qubits for U to act on
qc = QuantumCircuit(N_COUNT + 4, N_COUNT)

# Initialize counting qubits
# in state |+>
for q in range(N_COUNT):
    qc.h(q)

# And auxiliary register in state |1>
qc.x(N_COUNT)

# Do controlled-U operations
for q in range(N_COUNT):
    qc.append(c_amod15(a, 2**q),
             [q] + [i+N_COUNT for i in range(4)])

# Do inverse-QFT
qc.append(qft_dagger(N_COUNT), range(N_COUNT))

# Measure circuit
qc.measure(range(N_COUNT), range(N_COUNT))
qc.draw(fold=-1)  # -1 means 'do not fold'





rows, measured_phases = [], []
for output in counts:
    decimal = int(output, 2)  # Convert (base 2) string to decimal
    phase = decimal/(2**N_COUNT)  # Find corresponding eigenvalue
    measured_phases.append(phase)
    # Add these values to the rows in our table:
    rows.append([f"{output}(bin) = {decimal:>3}(dec)",
                 f"{decimal}/{2**N_COUNT} = {phase:.2f}"])
# Print the rows in a table
headers=["Register Output", "Phase"]
df = pd.DataFrame(rows, columns=headers)
print(df)
"""

def qpe_amod15(a, BE):
    """Performs quantum phase estimation on the operation a*r mod 15.
    Args:
        a (int): This is 'a' in a*r mod 15
    Returns:
        float: Estimate of the phase
    """
    start1 = time.time()
    time_without_run = 0
    N_COUNT = 8
    qc = QuantumCircuit(4+N_COUNT, N_COUNT)
    for q in range(N_COUNT):
        qc.h(q)     # Initialize counting qubits in state |+>
    qc.x(3+N_COUNT) # And auxiliary register in state |1>
    for q in range(N_COUNT): # Do controlled-U operations
        qc.append(c_amod15(a, 2**q),
                 [q] + [i+N_COUNT for i in range(4)])
    qc.append(qft_dagger(N_COUNT), range(N_COUNT)) # Do inverse-QFT
    qc.measure(range(N_COUNT), range(N_COUNT))
    # Simulate Results
    backend = provider.get_backend(BE)
    # `memory=True` tells the backend to save each measurement in a list
    transpiled = transpile(qc, backend)
    stop1 = time.time()
    #print("stop1 - start1: " + str(stop1 - start1))
    job = backend.run(transpiled, shots=1, memory=True)
    start2 = time.time()
    readings = job.result().get_memory()
    print("Register Reading: " + readings[0])
    #start25 = time.time()
    phase = int(readings[0],2)/(2**N_COUNT)
    print("Corresponding Phase:" + str(phase))
    stop2 = time.time()
    #print("start25 - start2: " + str(start25 - start2))
    #time_without_run = stop1 - start1 + stop2 - start2
    time_run = job.result().time_taken
    #ret_time = time_run + time_without_run
    ret_time = time_run + stop1 - start1 + stop2 - start2
    #print(str(time_run) + ", " + str(time_without_run) +", " + str(ret_time))
    return (phase, ret_time)

def iteration(BE):
    start0 = time.time()
    global ITERATION
    ITERATION += 1
    print("\nITERATION:" + str(ITERATION))
    TIME_qpe = 0.0
    FACTOR_FOUND = False
    ATTEMPT = 0
    stop0 = time.time()
    TIME = stop0 - start0
    #print("TIME (init): " + str(TIME))
    while not FACTOR_FOUND:
        start11 = time.time()
        ATTEMPT += 1
        print("\nATTEMPT" + str(ATTEMPT))
        stop11 = time.time()
        #print("stop11 - start11 : " + str(stop11 - start11))
        (phase, TIME_qpe) = qpe_amod15(a, BE) # Phase = s/r
        start2 = time.time()
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        print(f"Result: r = {r}")
        if phase != 0:
			# Guesses for factors are gcd(x^{r/2} ±1 , 15)
            guesses = [gcd(a**(r//2)-1, N), gcd(a**(r//2)+1, N)]
            print(f"Guessed Factors: {guesses[0]} and {guesses[1]}")
            for guess in guesses:
                if guess not in [1,N] and (N % guess) == 0:
					# Guess is a factor!
                    print("*** Non-trivial factor found: " + str(guess) + " ***")
                    FACTOR_FOUND = True
        stop2 = time.time()
        #print("stop2 - start2" + str(stop2 - start2))
        TIME += TIME_qpe + stop11 - start11 + stop2 - start2
        #print("TIME: " + str(TIME))
    #print("TIME: " + str(TIME))
    return TIME, ATTEMPT


def avg_n_iterations(n, BE):
    attempts = [0,0,0,0,0]
    TIME = 0.0
    grossTIME = 0.0
    for i in range(n):
        start = time.time()
        itTIME, att = iteration(BE)
        attempts[att-1] += 1
        #print("Attempts: " + str(attempts))
        TIME += itTIME
        #print("TIME: " + str(TIME))
        stop = time.time()
        grossTIME += stop - start
        #print("brutetime: " + str(brutetime))
    return TIME/n, grossTIME/n, attempts



ITERATION = 0
n = 100     
BE = 'simulator_statevector'
avg_statevector, gross_avg_statevector, attempts_statevector = avg_n_iterations(n, BE)
f = open("statevector.txt", "w")
f.write("Tries: " + str(n) + "\n")
f.write("avg_statevector: " + str(avg_statevector) + "\n")
f.write("gross_avg_statevector: " + str(gross_avg_statevector) + "\n")
f.write("attempts_statevector: " + str(attempts_statevector) + "\n")
f.close()

BE = 'simulator_mps'
avg_mps, gross_avg_mps, attempts_mps = avg_n_iterations(n, BE)
f = open("mps.txt", "w")
f.write("Tries: " + str(n) + "\n")
f.write("avg_mps: " + str(avg_mps) + "\n")
f.write("gross_avg_mps: " + str(gross_avg_mps) + "\n")
f.write("attempts_mps: " + str(attempts_mps) + "\n")
f.close()

BE = 'ibmq_qasm_simulator'
avg_qasm_simulator, gross_avg_qasm_simulator, attempts_qasm = avg_n_iterations(n, BE)
f = open("qasm_simulator.txt", "w")
f.write("Tries: " + str(n) + "\n")
f.write("avg_qasm_simulator: " + str(avg_qasm_simulator) + "\n")
f.write("gross_avg_qasm_simulator: " + str(gross_avg_qasm_simulator) + "\n")
f.write("attempts_qasm: " + str(attempts_qasm) + "\n")
f.close()



print("Average time for 'simulator_statevector': " + str(avg_statevector) + " seconds")
print("Average gross time for 'simulator_statevector': " + str(gross_avg_statevector) + " seconds")
print("Attempts: " + str(attempts_statevector))
print("Average time for 'simulator_mps': " + str(avg_mps) + " seconds")
print("Average gross time for 'simulator_mps': " + str(gross_avg_mps) + " seconds")
print("Attempts: " + str(attempts_mps))
print("Average time for 'ibmq_qasm_simulator': " + str(avg_qasm_simulator) + " seconds")
print("Average gross time for 'ibmq_qasm_simulator': " + str(gross_avg_qasm_simulator) + " seconds")
print("Attempts: " + str(attempts_qasm))

