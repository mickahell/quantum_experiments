import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, execute, IBMQ
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

typ_dice = int(input("Choisi un dès 4, 6, 8, 10, 12, 20 : "))
print("Tu as choisi un dè de ", typ_dice)

nb_qubits = len(bin(typ_dice - 1)[2:])  # Optimisation du nombre de qubit pour minimiser la décohérence

#########################################################
#########################################################
# #Circuit

# Quantum Circuit
circ = QuantumCircuit(nb_qubits)
for i in range(0, nb_qubits):
    circ.h(i)

# Measurement Circuit
meas = QuantumCircuit(nb_qubits, nb_qubits)
# map the quantum measurement to the classical bits
meas.measure(range(nb_qubits), range(nb_qubits))

qc = circ+meas  # merge circuits

# # Drawing the circuit
# qc.draw(output='mpl')
# plt.show(block=False)
# print(qc)

#########################################################
#########################################################
# #Simulating

# Init Qasm simulator backend
qasm = Aer.get_backend('qasm_simulator')

# Init Real Quantum computeur
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
quantum_computer = provider.get_backend('ibmq_burlington')

# Launch job
backend_sim = qasm  # Choose your backend : <quantom_computer> or <qasm>

job = execute(qc, backend_sim, shots=1, memory=True)
job_monitor(job)

# Result job
result_sim = job.result()
counts = result_sim.get_counts(qc)

# # Show the results
# print(counts)
# plot_histogram(counts)
# plt.show()

#########################################################
#########################################################
# #Results

memory = result_sim.get_memory()

result = int(memory[0], 2)

# Convertion du nombre en tirage du dé 4, 6, 8, 10, 12 ou 20
value_dice = round((result + 1) / 2**nb_qubits * typ_dice)
if value_dice == 0:
    value_dice += 1

print("Dé : ", value_dice)
