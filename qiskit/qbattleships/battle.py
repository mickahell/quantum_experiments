import matplotlib.pyplot as plt
from qiskit import BasicAer, Aer, QuantumCircuit, QuantumRegister, ClassicalRegister, execute, IBMQ
from qiskit.visualization import *
from qiskit.tools.monitor import job_monitor
import math

#########################################################
#########################################################
# #INIT

qasm = Aer.get_backend('qasm_simulator')
IBMQ.load_account()  # Init Real Quantum computeur
provider = IBMQ.get_provider('ibm-q')
quantum_computer = provider.get_backend('ibmq_burlington')

backend_sim = qasm  # Choose your backend : <quantom_computer> or <qasm>

statevector_sim = Aer.get_backend("statevector_simulator")

ship = ["petit", "moyen", "grand"]

nb_qubits = len(ship)
qubits = [1, 2, 3, 4, 5]
fake_qubit = 5 - nb_qubits
play = True

#########################################################
#########################################################
# #Circuit

# Quantum Circuit
q = QuantumRegister(nb_qubits + fake_qubit)  # initialize a register with a single qubit

qc = QuantumCircuit(q)

for qubit in range(0, nb_qubits + fake_qubit):
    qc.x(q[qubit])  # NOT gate on each qubit with a ship

#########################################################
#########################################################
# #Jeu

while play:
    tire_ship = int(input("Sur quel qubit veux tu tirer : 0, 1, 2, 3, 4 ? "))

    if tire_ship == 0 and int(qubits[4]) != 0:
        qc.x(q[0])
        print("Touchééééé petit bateau")
    elif tire_ship == 1 and int(qubits[3]) != 0:
        qc.ry(math.pi / 2, q[1])
        print("Touchééééé moyen bateau")
    elif tire_ship == 2 and int(qubits[2]) != 0:
        qc.ry(math.pi / 3, q[2])
        print("Touchééééé grand bateau")
    else:
        print("Plouffff... point de bateau ici")

    # Statevector
    statevector_job = execute(qc, statevector_sim)
    statevector_result = statevector_job.result()
    psi = statevector_result.get_statevector()

    if (psi[-2] == (1+0j) or psi[-6] == (1+0j) or psi[-4] == (1+0j) or psi[-8] == (1+0j)) and "petit" in ship:
        print("The little ship is in the deep water... Well done !")
        ship.remove("petit")
    if (psi[-3] == (1+0j) or psi[-4] == (1+0j) or psi[-7] == (1+0j) or psi[-8] == (1+0j)) and "moyen" in ship:
        print("The medium ship is the new neighbor of the Titanic... Well done !")
        ship.remove("moyen")
    if (psi[-5] == (1+0j) or psi[-6] == (1+0j) or psi[-7] == (1+0j) or psi[-8] == (1+0j)) and "grand" in ship:
        print("The large ship seems joining the fish... Well done !")
        ship.remove("grand")

    plot_bloch_multivector(psi)
    plt.show()

    if psi[-8] == (1+0j):
        print("You wiiiin !")
        play = False

#########################################################
#########################################################
# #Analyse

# Drawing the circuit
qc.draw(output='mpl')
plt.show()
# print(qc)
