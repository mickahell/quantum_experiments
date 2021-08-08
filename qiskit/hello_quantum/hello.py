#########################################################################################
# Idea from https://medium.com/qiskit/making-a-quantum-computer-smile-cee86a6fc1de
#########################################################################################

import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, execute, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.tools.monitor import job_monitor

nb_qubits = 16

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

" ;) = 0011101100101001"
" 8) = 0011100000101001"

qc.x(0)
qc.x(3)
qc.x(5)
qc.x(11)
qc.x(12)
qc.x(13)

qc.h(8)
qc.cx(8, 9)

qc.measure(range(nb_qubits), range(nb_qubits))

# # Drawing the circuit
# qc.draw(output='mpl')
# plt.show(block=False)
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

# # Show the results
print(counts)
# plot_histogram(counts)
# plt.show()

characterDict = {}
for bitString in counts:  # loop over all results
    char1 = chr(int(bitString[0:8], 2))  # convert first octet to an ASCII character
    char2 = chr(int(bitString[8:16], 2))  # convert second octet to an ASCII character
    characterDict[char1 + char2] = counts[bitString] / 1024

plt.rc('font', family='monospace')
for char in characterDict.keys():
    # plot all characters on top of each other with alpha given by how often it turned up in the output
    plt.annotate(char, (0.5, 0.5), va="center", ha="center", color=(0, 0, 0, characterDict[char]), size=300)
plt.axis('off')
plt.show()
