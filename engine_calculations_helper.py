import math
import numpy as np
import matplotlib.pyplot as plt


def calc_output_torque(load, dynamo_arm_length):  # load = kg, arm_length = mm
    return load * 9.81 * dynamo_arm_length / 1000.0  # Nm


def calc_brake_power(output_torque, rpm):  # output_torque = Nm
    return output_torque * 2 * 3.1415 * rpm / 60  # W


def calc_friction_power(ip, bp):  # ip = W, bp = W
    return ip - bp  # W


def calc_bmep(bp, rpm, dia_cyl, stroke_length, cylinders):  # bp = W, dia_cyl = mm, stroke_length = mm
    return (bp * 60 * 2 * 4) / (
        math.pi * rpm * math.pow(dia_cyl, 2) * stroke_length * cylinders / math.pow(10, 9))  # Pa


def calc_imep(ip, rpm, dia_cyl, stroke_length, cylinders):  # ip = W, dia_cyl = mm, stroke_length = mm
    return (ip * 60 * 2 * 4) / (
        math.pi * rpm * math.pow(dia_cyl, 2) * stroke_length * cylinders / math.pow(10, 9))  # Pa


def calc_bte(bp, v_fuel, den_fuel, cv_fuel):  # bp = W, v_fuel = L/min, d_fuel = kg/m3, cv_fuel = kJ/kg
    return bp * 60 / (v_fuel * den_fuel * cv_fuel / 1000)  # not in percentage


def calc_ite(ip, v_fuel, den_fuel, cv_fuel):  # ip = W, v_fuel = L/min, d_fuel = kg/m3, cv_fuel = kJ/kg
    return ip * 60 / (v_fuel * den_fuel * cv_fuel / 1000)  # not in percentage


def calc_me(bp, ip):  # bp = W, ip = W
    return bp / ip  # not in percentage


def calc_fuel_flow(v_fuel, den_fuel):  # v_fuel = L/min, d_fuel = kJ/kg
    return v_fuel * math.pow(10, -6) * 60 * den_fuel  # kg/hr


def calc_air_flow(h, dia_orifice):  # h = mm, dia_orifice = mm
    a = 1 - 9.81 * h / (1.013 * math.pow(10, 5))
    b = np.power(a, 2.0 / 7.0)
    c = 2 * 1000 * 302 * (1 - b)
    v = np.power(c, 0.5)
    return 0.6 * v * 1.17 * math.pi * math.pow(dia_orifice, 2) / 4 * 60 * 60 * math.pow(10, -6)  # kg/hr


def calc_bsfc(fuel_flow, bp):  # fuel_flow = kg/hr, bp = W
    return fuel_flow / (bp / 1000)  # kg/kW-hr


def calc_isfc(fuel_flow, ip):  # fuel_flow = kg/hr, ip = W
    return fuel_flow / (ip / 1000)  # kg/kW-hr


def calc_vole(air_flow, dia_cyl, stroke_length, rpm, cylinders):  # air_flow = kg/hr, dia_cyl = mm, stroke_length = mm
    return air_flow / (60 * 60) * 2 * 4 * math.pow(10, 9) * 60 / (1.17 * 3.1415 * math.pow(dia_cyl, 2) * stroke_length * rpm * cylinders)  # not in percentage


def calc_el_per_heat_input(v_water_cal, fuel_flow, cv_fuel, t3, t4, t5, t6):  # v_water_cal = LPH, fuel_flow = kg/hr, cv_fuel = kJ/kg, t3 = C, t4 = C, t5 = C, t6 = C
    return v_water_cal * 4.186 * (t4 - t3) * (t5 - 29) / (fuel_flow * cv_fuel * (t5 - t6))  # not in percentage


def calc_hl_per_heat_input(v_water_engine, fuel_flow, cv_fuel, t1, t2):  # v_water_engine = LPH, fuel_flow = kg/hr, t1 = C, t2 = C
    return v_water_engine * 4.186 * (t2 - t1) / (fuel_flow * cv_fuel)  # not in percentage


def plot(x, xlabel, y, ylabel, figure_name):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig("DataSheets/Outputs/Figures/" + figure_name + ".png")
    plt.clf()
