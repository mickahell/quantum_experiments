#########################################################################################
# Idea from https://medium.com/qiskit/getting-to-know-your-quantum-processor-ea418867615f
#########################################################################################

import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, execute, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_gate_map, plot_error_map
from qiskit.tools.monitor import job_monitor
import math
import random

nb_qubits = 15

random_circuit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
random.shuffle(random_circuit)

# Init Qasm simulator backend
qasm = Aer.get_backend('qasm_simulator')

# Init Real Quantum computer
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
quantum_computer = provider.get_backend('ibmq_16_melbourne')

backend_sim = qasm  # Choose your backend : <quantom_computer> or <qasm>

#########################################################
#########################################################
# #Circuit

# Quantum Circuit
q = QuantumRegister(nb_qubits)
c = ClassicalRegister(nb_qubits)

qc = QuantumCircuit(q, c)

# print("00 --A-- 01 --B-- 02 --C-- 03 --D-- 04 --E-- 05 --F-- 06\n"
#       " |        |        |        |        |        |        |\n"
#       " U        T        S        R        Q        P        O\n"
#       " |        |        |        |        |        |        |\n"
#       "14 --N-- 13 --M-- 12 --L-- 11 --K-- 10 --J-- 09 --I-- 08 --H-- 07")

plot_gate_map(quantum_computer)
plt.show()

# Make random pairing
i = 0
while i < nb_qubits:
    cible_qbit = random.choice(random_circuit)
    qc.rx(math.pi / 2, q[cible_qbit])
    random_circuit.remove(cible_qbit)
    if len(random_circuit) != 0:
        target_qbit = random.choice(random_circuit)
        qc.cx(q[cible_qbit], q[target_qbit])
        random_circuit.remove(target_qbit)
    i += 2


qc.measure(range(nb_qubits), range(nb_qubits))

# # Drawing the circuit
qc.draw(output='mpl')
# plt.show()
# print(qc)

#########################################################
#########################################################
# #Simulating

job = execute(qc, backend_sim, shots=1024)
job_monitor(job)

# Result job
result_sim = job.result()
counts = result_sim.get_counts()

#########################################################
#########################################################
# #Results

value_q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for x in range(0, nb_qubits):
    for key in counts:
        if key[x] == "1":
            value_q[x] += (1 * int(counts[key]))

# Calculus link between each qubit
link = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V"]
for letter in range(0, 19):
    if 0 <= letter < 6:
        link[letter] = abs(abs(value_q[letter]) - abs(value_q[letter + 1]))
    elif 7 <= letter < 14:
        link[letter] = abs(abs(value_q[letter]) - abs(value_q[letter + 1]))
    if 8 <= letter <= 14:
        link[letter + 6] = abs(abs(value_q[letter]) - abs(value_q[nb_qubits - 1 - letter]))

print("",value_q[0]," -- ",link[0]," -- ",value_q[1]," -- ",link[1]," -- ",value_q[2]," -- ",link[2]," -- ",value_q[3]," -- ",link[3]," -- ",value_q[4]," -- ",link[4]," -- ",value_q[5]," -- ",link[5]," -- ",value_q[6],"\n"
        " |                |                 |                 |                |               |               |\n"
        "",link[20],"             ",link[19],"              ",link[18],"              ",link[17],"             ",link[16],"            ",link[15],"             ",link[14],"\n"
        " |                |                 |                 |                |               |               |\n"
        "",value_q[14]," -- ",link[13]," -- ",value_q[13]," -- ",link[12]," -- ",value_q[12]," -- ",link[11]," -- ",value_q[11]," -- ",link[10]," -- ",value_q[10]," -- ",link[9]," -- ",value_q[9]," -- ",link[8]," -- ",value_q[8]," -- ",link[7]," -- ",value_q[7])

if backend_sim == quantum_computer:
    plot_error_map(quantum_computer)

# # Show the results
# print(counts)
# plot_histogram(counts)
plt.show()
