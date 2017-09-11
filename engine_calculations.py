from tkinter.filedialog import askopenfilename
import pandas as pd
import engine_calculations_helper as ech


input_filename = askopenfilename()
input_dataframe = pd.read_csv(input_filename)

cylinders = input_dataframe['cylinders'][0]
strokes = input_dataframe['strokes'][0]
fuel = input_dataframe['fuel'][0]
dia_orifice = input_dataframe['dia_orifice'][0]
dia_cyl = input_dataframe['dia_cyl'][0]
stroke_length = input_dataframe['stroke_length'][0]
dynamo_arm_length = input_dataframe['dynamo_arm_length'][0]

if fuel == 'diesel':
    cv_fuel = 42000
    den_fuel = 830

else:
    cv_fuel = 44000
    den_fuel = 740

rpm = input_dataframe['rpm']
load = input_dataframe['load']
h = input_dataframe['h']
v_fuel = input_dataframe['v_fuel']
v_water_engine = input_dataframe['v_water_engine']
v_water_cal = input_dataframe['v_water_cal']
ip = input_dataframe['ip'] * 1000  # Input is in kW while we need W
t1 = input_dataframe['t1']
t2 = input_dataframe['t2']
t3 = input_dataframe['t3']
t4 = input_dataframe['t4']
t5 = input_dataframe['t5']
t6 = input_dataframe['t6']


output_torque = ech.calc_output_torque(load, dynamo_arm_length)
bp = ech.calc_brake_power(output_torque, rpm)
fp = ech.calc_friction_power(ip, bp)
bmep = ech.calc_bmep(bp, rpm, dia_cyl, stroke_length, cylinders)
imep = ech.calc_imep(ip, rpm, dia_cyl, stroke_length, cylinders)
bte = ech.calc_bte(bp, v_fuel, den_fuel, cv_fuel)
ite = ech.calc_ite(ip, v_fuel, den_fuel, cv_fuel)
me = ech.calc_me(bp, ip)
fuel_flow = ech.calc_fuel_flow(v_fuel, den_fuel)
air_flow = ech.calc_air_flow(h, dia_orifice)
bsfc = ech.calc_bsfc(fuel_flow, bp)
isfc = ech.calc_isfc(fuel_flow, ip)
vole = ech.calc_vole(air_flow, dia_cyl, stroke_length, rpm, cylinders)

bp_per_heat_input = bte
el_per_heat_input = ech.calc_el_per_heat_input(v_water_cal, fuel_flow, cv_fuel, t3, t4, t5, t6)
hl_per_heat_input = ech.calc_hl_per_heat_input(v_water_engine, fuel_flow, cv_fuel, t1, t2)
sum_bp_losses = bp_per_heat_input + el_per_heat_input + hl_per_heat_input


output_dict = {
    'Output Torque (Nm)': output_torque,
    'Brake Power (kW)': bp / 1000,                  # W -> kW
    'Friction Power (kW)': fp / 1000,               # W -> kW
    'BMEP (bar)': bmep / 100000,                    # Pa -> bar
    'IMEP (bar)': imep / 100000,                    # Pa -> bar
    'Brake Thermal Efficiency (%)': bte * 100,      # fraction -> %
    'Indicated Thermal Efficiency (%)': ite * 100,  # fraction -> %
    'Mechanical Efficiency (%)': me * 100,          # fraction -> %
    'Fuel Flow (kg/hr)': fuel_flow,
    'Air Flow (kg/hr)': air_flow,
    'BSFC (kg/kW-hr)': bsfc,
    'ISFC (kg/kW-hr)': isfc,
    'Volumetric Efficiency (%)': vole * 100,                               # fraction -> %
    'Brake Power as percent of Heat Input (%)': bp_per_heat_input * 100,   # fraction -> %
    'Exhaust Loss as percent of Heat Input (%)': el_per_heat_input * 100,  # fraction -> %
    'Heat Loss as percent of Heat Input (%)': hl_per_heat_input * 100,     # fraction -> %
    'Sum of Brake Power and Losses (%)': sum_bp_losses * 100               # fraction -> %
}

output_dataframe = pd.DataFrame(output_dict)

output_filename = input_filename[0: input_filename.rfind('/')] \
                  + '/Outputs/output_' \
                  + input_filename[input_filename.rfind('/') + 1:]

output_dataframe.to_csv(output_filename)
