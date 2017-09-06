import numpy as np
import pandas as pd
import engine_calculations_helper as ech


input_dataframe = pd.read_csv("DataSheets/kirloskar.csv")  # TODO - file picker

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
ip = input_dataframe['ip'] * 1000  # Input is in kW while we need W


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
vole = ech.calc_vole(air_flow, dia_cyl, stroke_length, rpm)


output_dict = {
    'Output Torque (Nm)': output_torque,
    'Brake Power (W)': bp,
    'Friction Power (W)': fp,
    'BMEP (Pa)': bmep,
    'IMEP (Pa)': imep,
    'Brake Thermal Efficiency': bte,
    'Indicated Thermal Efficiency': ite,
    'Mechanical Efficiency': me,
    'Fuel Flow (kg/hr)': fuel_flow,
    'Air Flow (kg/hr)': air_flow,
    'BSFC (kg/kW-hr)': bsfc,
    'ISFC (kg/kW-hr)': isfc,
    'Volumetric Efficiency': vole
}

output_dataframe = pd.DataFrame(output_dict)
output_dataframe.to_csv("DataSheets/Outputs/output_kirloskar.csv")
