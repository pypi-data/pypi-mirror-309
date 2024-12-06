# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:06:49 2023

This module defines classes and functions to simulate spiral membrane filtration processes.

Classes:
    res_membrane: Class to store and calculate membrane filtration results.
    dwsim: Interface class to communicate with DWSIM for process simulation.
    spiral_membrane: Class that simulates the spiral membrane process.

@author: Hedi
"""

from . import *
import time
from numpy import exp, concatenate, array, split, zeros, linspace, argwhere, insert
from numpy import clip, linalg, maximum
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve, root


class res_membrane:
    """
    A class to store and compute results of membrane simulation.

    Properties:
        Vr_out (float): Retentate volumetric flow rate at the membrane outlet (in m3/h).
        Vp_out (float): Permeate volumetric flow rate at the membrane outlet (in m3/h).
        Cr_out (ndarray): Solute concentrations in the retentate at the membrane outlet (in mol/m3).
        Cp_out (ndarray): Solute concentrations in the permeate at the membrane outlet (in mol/m3).
        net_balance (float): Net volumetric mass balance (in m3/h).
        solute_net_balance (ndarray): Solute mass balance (in mol/h).
        FRV (ndarray): Flow rate volume ratio along the membrane.
        T (ndarray): Transmission coefficient along the membrane (mol/mol).
        R (ndarray): Rejection coefficient along the membrane (-).
        FRV_out (float): Flow rate volume ratio at the membrane outlet (-).
        T_out (ndarray): Transmission coefficient at the membrane outlet (mol/mol).
        R_out (ndarray): Rejection coefficient at the membrane outlet (-).
    """

    @property
    def Vr_out(self):
        """
        Retentate volumetric flow rate at the membrane outlet.

        Returns:
        ---------
        float : The volumetric flow rate at the outlet (in m3/h).
        """
        return self.Vr[-1]

    @property
    def Vp_out(self):
        """
        Permeate volumetric flow rate at the membrane outlet.

        Returns:
        ---------
        float : The volumetric flow rate of permeate at the outlet (in m3/h).
        """
        return self.Vp[-1]

    @property
    def Cr_out(self):
        """
        Solute concentrations in the retentate at the membrane outlet.

        Returns:
        ---------
        ndarray : Solute concentrations at the outlet (in mol/m3).
        """
        return self.Cr[:, -1]

    @property
    def Cp_out(self):
        """
        Solute concentrations in the permeate at the membrane outlet.

        Returns:
        ---------
        ndarray : Solute concentrations at the outlet (in mol/m3).
        """
        return self.Cp[:, -1]

    @property
    def net_balance(self):
        """
        Net volumetric mass balance.

        Returns:
        ---------
        float : The net mass balance (in m3/h).
        """
        return self.parent.Vin - self.Vr_out - self.Vp_out

    @property
    def solute_net_balance(self):
        """
        Solute mass balance.

        Returns:
        ---------
        ndarray : The solute mass balance (in mol/h).
        """
        return array(self.parent.Cin) * self.parent.Vin - self.Cp[:, -1] * self.Vp[-1] - self.Cr[:, -1] * self.Vr[-1]

    @property
    def FRV(self):
        """
        Flow rate volume ratio along the membrane Vin/Vr.

        Returns:
        ---------
        ndarray : The flow rate volume ratio.
        """
        return self.parent.Vin / self.Vr

    @property
    def T(self):
        """
        Transmission coefficient along the membrane.

        Returns:
        ---------
        ndarray : The transmission coefficient (mol/mol).
        """
        return self.Cp / self.Cr

    @property
    def R(self):
        """
        Rejection coefficient along the membrane.

        Returns:
        ---------
        ndarray : The rejection coefficient (-).
        """
        return 1 - self.T

    @property
    def FRV_out(self):
        """
        Flow rate volume ratio at the membrane outlet Vin_out/Vr_out.

        Returns:
        ---------
        float : The flow rate volume ratio at the outlet.
        """
        return self.FRV[-1]

    @property
    def T_out(self):
        """
        Transmission coefficient at the membrane outlet.

        Returns:
        ---------
        ndarray : The transmission coefficient at the outlet (mol/mol).
        """
        return self.T[:, -1]

    @property
    def R_out(self):
        """
        Rejection coefficient at the membrane outlet.

        Returns:
        ---------
        ndarray : The rejection coefficient at the outlet (-).
        """
        return self.R[:, -1]


class dwsim:
    """
    A class to interface with DWSIM for the spiral membrane simulation.

    Args:
        parent (spiral_membrane): The spiral membrane instance.
        **args: Additional optional arguments.

    Methods:
        print(Flowsheet, sheetname): Outputs the simulation results to a DWSIM spreadsheet.
        refresh(): Updates the retentate and permeate streams with calculated data.
    """

    def __init__(self, parent, **args):
        self.parent = parent
        for k, v in parent.schema.dwsim.__dict__.items():
            setattr(self, k, v)
        for k, v in args.items():
            if k in list(self.__dict__.keys()):
                setattr(self, k, v)
        if self.feed:
            parent.T = self.feed.GetTemperature() - 273.15
            parent.Pin = self.feed.GetPressure() / 1e5
            parent.Vin = self.feed.GetVolumetricFlow() * 3600
            solutes = []
            Cin = []
            for i, s in enumerate(self.feed.ComponentIds):
                if s != "Water":
                    solutes.append(s)
                    Cin.append(self.feed.GetOverallComposition()[i] / self.feed.GetOverallMolecularWeight() * 1e6)
            parent.solutes = solutes
            parent.Cin = Cin

    def print(self, Flowsheet, sheetname):
        """
        Outputs the simulation results to a DWSIM spreadsheet.

        Args:
            Flowsheet: DWSIM flowsheet object.
            sheetname (str): The name of the worksheet to be created or updated.
        """
        Spreadsheet = Flowsheet.FormSpreadsheet
        ws = Spreadsheet.Spreadsheet.GetWorksheetByName(sheetname)
        if ws is None:
            ws = Spreadsheet.NewWorksheet(sheetname)
        ws.Reset()
        # Write data to worksheet (omitted for brevity)
        # This part writes the various results to the spreadsheet.

    def refresh(self):
        """
        Updates the retentate and permeate streams with calculated data.
        """
        if self.feed and self.ret and self.per:
            self.ret.Clear()
            self.per.Clear()
            self.ret.SetTemperature(self.feed.GetTemperature())
            self.per.SetTemperature(self.feed.GetTemperature())
            self.ret.SetPressure(self.feed.GetPressure() - self.parent.DP * 1e5)
            self.per.SetPressure(self.parent.Patm * 1e5)
            water_index = argwhere(array(self.feed.ComponentIds) == "Water")[0]
            ret_mass_flow = self.parent.res.Cr_out / 1e6
            ret_mass_flow = insert(ret_mass_flow, water_index, 1 - ret_mass_flow.sum())
            per_mass_flow = self.parent.res.Cp_out / 1e6
            per_mass_flow = insert(per_mass_flow, water_index, 1 - per_mass_flow.sum())
            for i in range(len(self.feed.ComponentIds)):
                self.ret.SetOverallCompoundMassFlow(i, float(ret_mass_flow[i] * self.parent.res.Vr_out * 1000 / 3600))
                self.per.SetOverallCompoundMassFlow(i, float(per_mass_flow[i] * self.parent.res.Vp_out * 1000 / 3600))


class spiral_membrane(cf.__obj__):
    """
    A class that simulates the spiral membrane filtration process.

    Args:
        **args: Configuration arguments for the membrane simulation.
        - dwsim (dict): Configuration for DWSIM integration.
        - k_correlation (bool): Whether to use k-correlation (-).
        - k_parameters (list): Correlation parameters for mass transfer (-).
        - l (float): Membrane width (in m).
        - Δm (float): Spacing or clearance (in m).
        - Vin (float): Inlet volumetric flow rate (in m3/h).
        - T (float): Inlet temperature (in °C).
        - Patm (float): Atmospheric pressure (in bar).
        - Pin (float): Inlet pressure (in bar).
        - S (float): Membrane area (in m2).
        - L (float): Membrane length (in m).
        - Aw (float): Water permeability (in m/h/bar).
        - DP (float): Pressure loss across the membrane (in bar).
        - Cin (list): Inlet solute concentrations (in mol/m3).
        - solutes (list): List of solutes.
        - B (list): Membrane mass transfer coefficients (in m/h).
        - k (list): Boundary layer mass transfer coefficients (in m/h).

    Methods:
        calcul(solver_method='fsolve', taylor_terms=2, diffusion=False): Simulates the membrane process.
        mass_layer(p, Cp, Cr, method, taylor_terms=2, diffusion=False): Calculates the concentration at the interface and related variables.
    """

    def __init__(self, **args):
        super().__init__(res_membrane)
        self.dwsim = None
        self.__R__ = 8.314  # J/mol/K
        for k, v in args.items():
            if k in list(self.__dict__.keys()):
                setattr(self, k, v)
            if k == "dwsim":
                self.dwsim = dwsim(self, **v)

    def calcul(self, solver_method='fsolve', taylor_terms=2):
        """
        Simulates the filtration process.

        Args:
            solver_method (str): The method used for solving concentration at the membrane interface.
                Options are 'fsolve', 'root', 'taylor', 'fixed_point'.
            taylor_terms (int): Number of terms to use in the Taylor series approximation (if applicable).
            diffusion (bool): Whether to account for diffusion effects in the calculations.
        """
        st = time.process_time()
        Cin, Vin, B = self.Cin, self.Vin, self.B
        α = self.S / self.L
        DPL = self.DP / self.L
        n_solutes = len(Cin)

        def sysdiff(t, y):
            p, Vp, Vr, VCp, VCr = *y[0:3], *split(y[3:], 2)
            dpdx = -DPL
            Cr = VCr / Vr
            Cp = VCp / Vp if Vp else zeros(n_solutes)
            Cm, Jw = self.mass_layer(p, Cp, Cr, solver_method, taylor_terms, t)[:2]
            dVpdx = Jw * α
            dVrdx = -dVpdx
            dCpdx = B * (Cm - Cp) * α
            dCrdx = -dCpdx
            return concatenate(([dpdx, dVpdx, dVrdx], dCpdx, dCrdx))

        self.res.x = linspace(0, self.L, 100)
        sol = solve_ivp(sysdiff, (0, self.L),
                        concatenate(([self.Pin, 0.0, Vin], [0] * n_solutes, Vin * Cin)),
                        method="BDF", t_eval=self.res.x, rtol=1e-7, atol=1e-9)

        self.res.p, self.res.Vp, self.res.Vr, VCp, VCr = *sol.y[0:3], *split(sol.y[3:], 2)
        self.res.Cr = VCr / self.res.Vr
        self.res.Cp = VCp
        self.res.Cp[:, 1:] = self.res.Cp[:, 1:] / self.res.Vp[1:]
        self.res.Cm = zeros(self.res.Cp.shape)
        self.res.Jw = zeros(self.res.Cp.shape[1])
        self.res.PI = zeros(self.res.Cp.shape)
        self.res.PIm = zeros(self.res.Cp.shape)
        self.res.PIp = zeros(self.res.Cp.shape)
        for i in range(self.res.x.shape[0]):
            self.res.Cm[:, i], self.res.Jw[i], self.res.PIm[:, i], self.res.PIp[:, i], self.res.PI[:, i] = \
                self.mass_layer(self.res.p[i], self.res.Cp[:, i], self.res.Cr[:, i], solver_method, taylor_terms, i)

        self.res.calculation_time = time.process_time() - st
        if self.dwsim:
            self.dwsim.refresh()

    def mass_layer(self, p, Cp, Cr, method='fsolve', taylor_terms=2, diffusion=False):
        """
        Calculates the concentration at the membrane interface and related variables.

        Args:
            p (float): Retentate side pressure in bar.
            Cp (ndarray): Concentration of solute in permeate.
            Cr (ndarray): Concentration of solute in retentate.
            method (str): Method to solve for the concentration at the interface. Options are:
                          'fsolve', 'root', 'taylor', 'fixed_point'.
            taylor_terms (int): Number of terms in the Taylor series if using 'taylor'.
            diffusion (bool): Whether to account for diffusion effects in the calculations.

        Returns:
            tuple: Cm, Jw, PIm, PIp, DPi.
        """
        k = array(self.k)
        T = self.T + 273.15
        PIp = self.__R__ * T * 1e-5 * Cp

        if method == 'fsolve':
            def fm(c):
                PIm = self.__R__ * T * 1e-5 * c
                DPi = PIm - PIp
                Jw = (p - self.Patm - DPi.sum()) * self.Aw
                return abs(c - Cp - (Cr - Cp) * exp(Jw / k))

            Cm = fsolve(fm, Cr)

        elif method == 'root':
            def fm(c):
                PIm = self.__R__ * T * 1e-5 * c
                DPi = PIm - PIp
                Jw = (p - self.Patm - DPi.sum()) * self.Aw
                return c - Cp - (Cr - Cp) * exp(Jw / k)

            result = root(fm, Cr, method='hybr')
            Cm = result.x
            if not result.success:
                raise ValueError(f"Root finding failed: {result.message}")

        elif method == 'taylor':
            Jw = (p - self.Patm - self.__R__ * T * 1e-5 * Cp.sum()) * self.Aw
            Jw_over_k = Jw / k
            taylor_approx = sum((Jw_over_k ** n) / (1 if n == 0 else n) for n in range(taylor_terms))
            Cm = Cp + (Cr - Cp) * taylor_approx
            Cm = maximum(Cm, 1e-10)

        elif method == 'fixed_point':
            Cm = Cr
            tolerance = 1e-6
            max_iter = 100
            for _ in range(max_iter):
                PIm = self.__R__ * T * 1e-5 * Cm
                DPi = PIm - PIp
                Jw = (p - self.Patm - DPi.sum()) * self.Aw
                Jw_over_k = clip(Jw / k, -50, 50)
                Cm_new = Cp + (Cr - Cp) * exp(Jw_over_k)
                if linalg.norm(Cm_new - Cm) < tolerance:
                    break
                Cm = Cm_new

        else:
            raise ValueError(f"Unknown method: {method}")

        PIm = self.__R__ * T * 1e-5 * Cm
        DPi = PIm - PIp
        Jw = (p - self.Patm - DPi.sum()) * self.Aw

        return Cm, Jw, PIm, PIp, DPi

    def print_results(self):
        """
        Print the final calculated results for membrane simulation.
        """
        print("Calculation Time (s):", self.res.calculation_time)
        print("Retentate Flow Rate (Vr_out, m3/h):", self.res.Vr_out)
        print("Permeate Flow Rate (Vp_out, m3/h):", self.res.Vp_out)
        print("Solute Concentrations in Retentate (Cr_out, mol/m3):", self.res.Cr_out)
        print("Solute Concentrations in Permeate (Cp_out, mol/m3):", self.res.Cp_out)
        print("Net Mass Balance (m3/h):", self.res.net_balance)
        print("Solute Net Balance (mol/h):", self.res.solute_net_balance)
