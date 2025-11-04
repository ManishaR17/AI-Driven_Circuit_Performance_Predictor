import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
from engineering_notation import EngNumber

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


#CIRCUIT NETLIST
#------------------------

circuit = Circuit('Common-Source MOSFET Amplifier')

#Define amplitude and frequency of input sinusoid
amp=100@u_mV
freq=1@u_kHz
#Define transient simulation step time and stop time
steptime=1@u_us
finaltime = 5@u_ms

#Define MOSFET models
#https://ltwiki.org/LTspiceHelp/LTspic...
#https://ltwiki.org/index.php?title=St...

#simplified model
circuit.model('2N7000', 'NMOS', Kp=0.13, Vto=2.475)

#simplified model with channel length and width
#circuit.model('2N7000', 'NMOS', L=100E-6, W=200E-6, Kp=0.13, Vto=2.475)

source = circuit.SinusoidalVoltageSource(2, 'input', circuit.gnd, amplitude=amp, frequency = freq)

circuit.R('s', 'input','inmos',         100@u_kΩ)
circuit.C(1,'inmos', 'gate',            1@u_uF)
circuit.R('1', 'Vdd', 'gate',        200@u_kΩ)
circuit.R('2', 'gate', circuit.gnd,  100@u_kΩ)
circuit.R('D', 'Vdd', 'drain',    3@u_kΩ)
circuit.R('So', 'source', circuit.gnd,1.5@u_kΩ)
circuit.V(1, 'Vdd', circuit.gnd,      18@u_V)
circuit.MOSFET(1, 'drain', 'gate', 'source','source', model='2N7000')
circuit.C(2,'drain', 'output',    10@u_uF)
circuit.C(3,'source', circuit.gnd, 22@u_uF)
circuit.R('L', 'output',circuit.gnd,  10@u_kΩ)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=steptime, end_time=finaltime)

#THEORETICAL RESULTS

print('------------------')
print('Theoretical Values')
print('------------------')

K = 0.13
VT =2.475@u_V

#DC bias analysis
VTH = (circuit.V1.dc_value)*(circuit.R2.resistance/(circuit.R1.resistance+ circuit.R2.resistance))
RTH = (circuit.R1.resistance*circuit.R2.resistance)/(circuit.R1.resistance+ circuit.R2.resistance)

a = K * float(circuit.RSo.resistance)
b = 1- 2*K*float(circuit.RSo.resistance)*np.abs(VT)
c = K*float(circuit.RSo.resistance)*VT*VT- np.abs(float(VTH))
V_GS = ((-b + np.sqrt(b*b-4*a*c))/(2*a))*1@u_V

I_D = (VTH-V_GS)/circuit.RSo.resistance

#small signal AC analysis
gm = 2*K*float((V_GS-VT))

R_in = RTH
R_o = circuit.RD.resistance
A_v = float(-gm*R_o*(R_in/(R_in + circuit.Rs.resistance))*(circuit.RL.resistance/(circuit.RL.resistance+ R_o)))

#Find the theoretical output waveform; use the time output of the simulation
time=np.array(analysis.time)
v_out = A_v*(amp)*(np.sin(2*np.pi*freq*time))

#Display the DC and AC parameter values
print('VTH={} V'.format(EngNumber(float(VTH))))
print('RTH={} Ω'.format(EngNumber(float(RTH))))
print('a={}'.format(EngNumber(a)))
print('b={}'.format(EngNumber(b)))
print('c={}'.format(EngNumber(c)))
print('VGS={} V'.format(EngNumber(float(V_GS))))
print('ID={} A'.format(EngNumber(float(I_D))))
print('gm={}'.format(EngNumber(gm)))

print('Rin={} Ω'.format(EngNumber(float(R_in))))
print('Ro={} Ω'.format(EngNumber(float(R_o))))
print('Av={}'.format(EngNumber(float(A_v))))

#Plot the voltages
figure, axe = plt.subplots(figsize=(11, 6))

plt.title('MOSFET Amplifier Voltages')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.grid()
plot(analysis['input'], axis=axe)
plot(analysis['output'], axis=axe)
plt.plot(time, v_out)
plt.legend(('sim:input', 'sim:output', 'theory'), loc=(.05,.1))
cursor = Cursor(axe, useblit=True, color='red', linewidth=1)

plt.show()