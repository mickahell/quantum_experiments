#########################################################################################
# Idea from https://medium.com/qiskit/getting-to-know-your-quantum-processor-ea418867615f
#########################################################################################

import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, execute, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, plot_gate_map, plot_error_map
from qiskit.tools.monitor import job_monitor
import math
import random

nb_qubits = 10
nb_decoherence = 5

random_circuit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
random.shuffle(random_circuit)

# Init Qasm simulator backend
qasm = Aer.get_backend('qasm_simulator')

# Init Real Quantum computer
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
quantum_computer = provider.get_backend('ibmq_16_melbourne')

backend_sim = quantum_computer  # Choose your backend : <quantum_computer> or <qasm>

#########################################################
#########################################################
# #Circuit

# Quantum Circuit
q = QuantumRegister(nb_qubits + nb_decoherence, "game")
c = ClassicalRegister(nb_qubits + nb_decoherence)

qc = QuantumCircuit(q, c)

# print("00 --A-- 01 --B-- 02 --C-- 03 --D-- 04 --E-- 05 --F-- 06\n"
#       " |        |        |        |        |        |        |\n"
#       " U        T        S        R        Q        P        O\n"
#       " |        |        |        |        |        |        |\n"
#       "14 --N-- 13 --M-- 12 --L-- 11 --K-- 10 --J-- 09 --I-- 08 --H-- 07")

plot_gate_map(quantum_computer)
# plt.show()

# Make random pairing
qubit_decoherence = nb_qubits
for i in range(0, nb_qubits):
    if i % 2 == 0:
        qc.rx(math.pi / 2, q[i])
        qc.cx(q[i], q[i + 1])
        qc.ccx(q[i], q[i + 1], q[qubit_decoherence])
        qubit_decoherence += 1

qc.measure(range(nb_qubits + nb_decoherence), range(nb_qubits + nb_decoherence))

# # Drawing the circuit
qc.draw(output='mpl')
# plt.show()
# print(qc)

#########################################################
#########################################################
# #Simulating

job = execute(qc, backend_sim, shots=1024, optimization_level=3)
job_monitor(job)

# Result job
result_sim = job.result()
counts = result_sim.get_counts()

#########################################################
#########################################################
# #Results

value_q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for x in range(0, nb_qubits + nb_decoherence):
    for key in counts:
        if key[x] == "1":
            value_q[x] += (1 * int(counts[key]))

value_q.reverse()

def calculus_differencial(value_q):
    # Calculus link between each qubit
    link = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
    for letter in range(0, 10):
        if 0 <= letter < 6:
            link[letter] = abs(abs(value_q[letter]) - abs(value_q[letter + 1]))
        elif 7 <= letter < 9:
            link[letter] = abs(abs(value_q[letter]) - abs(value_q[letter + 1]))
        if 8 <= letter <= 9:
            link[letter + 1] = abs(abs(value_q[letter]) - abs(value_q[nb_qubits - letter + 4]))

    print("",value_q[0]," -- ",link[0]," -- ",value_q[1]," -- ",link[1]," -- ",value_q[2]," -- ",link[2]," -- ",value_q[3]," -- ",link[3]," -- ",value_q[4]," -- ",link[4]," -- ",value_q[5]," -- ",link[5]," -- ",value_q[6],"\n"
            "                                                                                       |                |\n"
            "                                                                                      ",link[10],"              ",link[9],"\n"
            "                                                                                       |                |\n"
            "                                                                                  ",value_q[9]," -- ",link[8]," -- ",value_q[8]," -- ",link[7]," -- ",value_q[7])

    return 0
calculus_differencial(value_q)

print("Value qubits : ", value_q)

if backend_sim == quantum_computer:
    plot_error_map(quantum_computer)
    qubit_decoherence = nb_qubits
    value_decoherence = [0, 0, 0, 0, 0]
    for i in range(0, nb_qubits):
        if i % 2 == 0:
            value_decoherence[qubit_decoherence - 10] = ((value_q[qubit_decoherence] - value_q[i]) + (value_q[qubit_decoherence] - value_q[i + 1])) / 512
            print("q", i, "[", value_q[qubit_decoherence], "-", value_q[i], "] + q", i + 1, "[", value_q[qubit_decoherence], "-", value_q[i + 1], "] => ", (value_q[qubit_decoherence] - value_q[i]) + (value_q[qubit_decoherence] - value_q[i + 1]), "/ 512 = ", value_decoherence[qubit_decoherence - 10])
            qubit_decoherence += 1

        value_q[i] *= 1 + value_decoherence[qubit_decoherence - nb_qubits - 1]
        value_q[i] = round(value_q[i])

    calculus_differencial(value_q)

# # Show the results
# print(counts)
# plot_histogram(counts)
plt.show()
