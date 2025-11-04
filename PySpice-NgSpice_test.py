# PySpice + Ngspice test script

import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create a trivial circuit: 5V source and 1k resistor
circuit = Circuit('Ngspice Connection Test')
circuit.V('1', 'in', circuit.gnd, 5@u_V)
circuit.R(1, 'in', 'out', 1@u_kΩ)

# Try running simulator
try:
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=1@u_ms, end_time=5@u_ms)
    print("✅ PySpice successfully connected to Ngspice!")

    # Plot voltage across resistor
    plt.figure(figsize=(8,4))
    plt.plot(analysis.time, analysis.out)
    plt.title('Ngspice Test: Voltage Across 1k Resistor')
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [V]')
    plt.grid()
    plt.show()

except Exception as e:
    print("❌ PySpice could not connect to Ngspice.")
    print(e)
