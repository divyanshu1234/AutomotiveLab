from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
import engine_calculations_helper as ech


input_filename = askopenfilename()
input_dataframe = pd.read_csv(input_filename)

dynamo_arm_length = input_dataframe['dynamo_arm_length'][0]

rpm = input_dataframe['rpm']
load = input_dataframe['load']

output_torque = ech.calc_output_torque(load, dynamo_arm_length)
bp = ech.calc_brake_power(output_torque, rpm)

ip = []

for i in range(0, bp.size):
    if i % 2 == 0:
        ip.append(abs(bp[i] - bp[i+1]) / 1000)  # W -> kW
    else:
        ip.append(0)

input_dataframe['ip1'] = np.array(ip)

output_filename = input_filename[0: input_filename.rfind('/')] \
                  + '/Outputs/output_' \
                  + input_filename[input_filename.rfind('/') + 1:]

input_dataframe.to_csv(output_filename)
