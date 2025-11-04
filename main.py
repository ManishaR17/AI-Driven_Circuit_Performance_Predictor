import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Probe.Plot import plot
from PySpice.Unit import *
from PySpice.Spice.Library import SpiceLibrary
# Path to ngspice executable (optional, PySpice tries to auto-detect)

simulator = Circuit('RC Circuit').simulator(temperature=25, nominal_temperature=25)

circuit = Circuit('RC Test')
circuit.V('input', 'in', circuit.gnd, 10@u_V)
circuit.R(1, 'in', 'out', 1@u_kΩ)
circuit.C(1, 'out', circuit.gnd, 1@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1@u_us, end_time=5@u_ms)



plt.figure(figsize=(10, 5))
plt.plot(analysis['out'])
plt.title('RC Circuit Response')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.grid()
plt.show()