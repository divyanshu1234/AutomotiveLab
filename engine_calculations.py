import numpy as np
import pandasql as pd
import engine_calculations_helper as ech


cylinders = float(input("Number of cylinders = "))
strokes = float(input("Number of strokes = "))
comp_ratio = float(input("Compression ratio = "))
cv_fuel = float(input("Calorific Value of fuel (kJ/kg) = "))
den_fuel = float(input("Density of fuel (kg/m3) = "))
dia_orifice = float(input("Diameter of air intake orifice (mm) = "))
dia_cyl = float(input("Diameter of cylinder (mm) = "))
stroke_length = float(input("Stroke length (mm) = "))
dynamo_arm_length = float(input("Dynamometer arm length (mm) = "))

rpm = 1553
load = 3
h = 90
v_fuel = 11.6
ip = 2500

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


print("Output Torque = " + str(output_torque) + " Nm")
print("Brake Power = " + str(bp) + " W")
print("Friction Power = " + str(fp) + " W")
print("BMEP = " + str(bmep) + " Pa")
print("IMEP = " + str(imep) + " Pa")
print("Brake Thermal Efficiency = " + str(bte))
print("Indicated Thermal Efficiency = " + str(ite))
print("Mechanical Efficiency = " + str(me))
print("Fuel Flow = " + str(fuel_flow) + " kg/hr")
print("Air Flow = " + str(air_flow) + " kg/hr")
print("BSFC = " + str(bsfc) + "g/kW-hr")
print("ISFC = " + str(isfc) + "kg/kW-hr")
print("Volumetric Efficiency = " + str(vole))
