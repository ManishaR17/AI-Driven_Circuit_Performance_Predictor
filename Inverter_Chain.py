import numpy as np
import pandas as pd
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


def simulate_inverter(W=1 @ u_um, VDD=1.0, temp=300, fanout=1):
    circuit = Circuit('Inverter Chain')

    circuit.V('DD', 'vdd', circuit.gnd, VDD)
    circuit.model('NMOS', 'NMOS')
    circuit.model('PMOS', 'PMOS')

    # Define a simple inverter chain
    # For simplicity, assume fanout = number of inverters in series
    for i in range(fanout):
        nmos = circuit.M(f'N{i}', f'out{i}', f'in{i}', circuit.gnd, circuit.gnd, model='NMOS', W=W, L=1 @ u_um)
        pmos = circuit.M(f'P{i}', f'out{i}', f'in{i}', 'vdd', 'vdd', model='PMOS', W=W, L=1 @ u_um)

    simulator = circuit.simulator(temperature=temp, nominal_temperature=temp)
    analysis = simulator.transient(step_time=1 @ u_ns, end_time=10 @ u_ns)

    # For demonstration: compute delay from 50% crossing
    # (more detailed extraction can be added)
    delay = np.random.uniform(1e-9, 10e-9)  # placeholder
    power = np.random.uniform(1e-6, 10e-6)  # placeholder
    area = W * fanout  # rough estimate

    return delay, power, area


# Generate synthetic dataset
dataset = []
for _ in range(100):
    W = np.random.uniform(0.5, 5)  # micron
    VDD = np.random.uniform(0.9, 1.2)  # Volt
    temp = np.random.uniform(270, 330)  # Kelvin
    fanout = np.random.randint(1, 5)
    delay, power, area = simulate_inverter(W=W, VDD=VDD, temp=temp, fanout=fanout)
    dataset.append([W, VDD, temp, fanout, delay, power, area])

df = pd.DataFrame(dataset, columns=['W', 'VDD', 'Temp', 'Fanout', 'Delay', 'Power', 'Area'])
print(df.head())
