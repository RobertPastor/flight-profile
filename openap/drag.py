"""OpenAP drag model."""

import glob
import importlib
import os
import warnings

import pandas as pd
import yaml

from . import prop
from .extra import ndarrayconvert

curr_path = os.path.dirname(os.path.realpath(__file__))
dir_dragpolar = os.path.join(curr_path, "data/dragpolar/")
file_synonym = os.path.join(curr_path, "data/dragpolar/_synonym.csv")

print(" openap/drag : ==================== read drap polar synonym file ==============")
polar_synonym = pd.read_csv(file_synonym)


class Drag(object):
    """Compute the drag of an aircraft."""

    def __init__(self, ac, wave_drag=False, **kwargs):
        """Initialize Drag object.

        Args:
            ac (string): ICAO aircraft type (for example: A320).
            wave_drag (bool): enable Wave drag model (experimental).

        """
        if not hasattr(self, "np"):
            self.np = importlib.import_module("numpy")

        if not hasattr(self, "aero"):
            self.aero = importlib.import_module("openap").aero

        self.use_synonym = kwargs.get("use_synonym", False)
        self.use_synonym = True

        self.ac = ac.lower()
        self.aircraft = prop.aircraft(ac, **kwargs)
        self.polar = self.dragpolar()

        self.wave_drag = wave_drag
        if self.wave_drag:
            warnings.warn("Warning: Wave drag is experimental.")

    def dragpolar(self):
        """Find and construct the drag polar model.

        Returns:
            dict: drag polar model parameters.
        """
        polar_files = glob.glob(dir_dragpolar + "*.yml")
        ac_polar_available = [s[-8:-4].lower() for s in polar_files]

        if self.ac in ac_polar_available:
            ac = self.ac
        else:
            syno = polar_synonym.query("orig==@self.ac")
            if self.use_synonym and syno.shape[0] > 0:
                ac = syno.new.iloc[0]
            else:
                raise ValueError(f"Drag polar for {self.ac} not available.")

        f = dir_dragpolar + ac + ".yml"
        with open(f, "r") as file:
            dragpolar = yaml.safe_load(file.read())
        return dragpolar

    @ndarrayconvert
    def _cl(self, mass, tas, alt):
        v = tas * self.aero.kts
        h = alt * self.aero.ft

        S = self.aircraft["wing"]["area"]

        rho = self.aero.density(h)
        qS = 0.5 * rho * v**2 * S
        L = mass * self.aero.g0

        # 1e-3: avoid zero division
        qS = self.np.maximum(qS, 1e-3)
        cl = L / qS
        return cl

    @ndarrayconvert
    def _calc_drag(self, mass, tas, alt, cd0, k, vs):
        v = tas * self.aero.kts
        h = alt * self.aero.ft

        gamma = self.np.arctan2(vs * self.aero.fpm, tas * self.aero.kts)

        S = self.aircraft["wing"]["area"]

        rho = self.aero.density(h)
        qS = 0.5 * rho * v**2 * S
        L = mass * self.aero.g0 * self.np.cos(gamma)

        # 1e-3: avoid zero division
        qS = self.np.maximum(qS, 1e-3)
        
        cl = L / qS
        cd = cd0
        #if (tas > 70.0) :
        ''' 17th November 2024 - Robert '''
        cd = cd0 + k * cl**2
        D = cd * qS
        return D

    @ndarrayconvert
    def clean(self, mass, tas, alt, vs=0):
        """Compute drag at clean configuration (considering compressibility).

        Args:
            mass (int or ndarray): Mass of the aircraft (unit: kg).
            tas (int or ndarray): True airspeed (unit: kt).
            alt (int or ndarray): Altitude (unit: ft).
            vs (float or ndarray): Vertical rate (unit: feet/min). Defaults to 0.

        Returns:
            int: Total drag (unit: N).

        """

        cd0 = self.polar["clean"]["cd0"]
        k = self.polar["clean"]["k"]

        if self.wave_drag:
            mach = self.aero.tas2mach(tas * self.aero.kts, alt * self.aero.ft)
            cl = self._cl(mass, tas, alt)

            sweep = self.aircraft["wing"]["sweep"] * self.np.pi / 180
            tc = self.aircraft["wing"]["t/c"]

            # Default thickness to chord ratio, based on Obert (2009)
            if tc is None:
                tc = 0.12

            cos_sweep = self.np.cos(sweep)

            kappa = 0.95  # assume supercritical airfoils

            # Equation 17 and 18 in Gur et al. (2010) - for conventional airfoil
            mach_crit = (
                kappa / cos_sweep - tc / cos_sweep**2 - 0.1 * cl / cos_sweep**3 - 0.108
            )

            # Equation 15 in Gur et al. (2010)
            dmach = self.np.maximum(mach - mach_crit, 0.0)
            dCdw = 20 * dmach**4

        else:
            dCdw = 0

        cd0 = cd0 + dCdw

        D = self._calc_drag(mass, tas, alt, cd0, k, vs)
        return D

    @ndarrayconvert
    def nonclean(self, mass, tas, alt, flap_angle, vs=0, landing_gear=False):
        """Compute drag at at non-clean configuration.

        Args:
            mass (int or ndarray): Mass of the aircraft (unit: kg).
            tas (int or ndarray): True airspeed (unit: kt).
            alt (int or ndarray): Altitude (unit: ft).
            flap_angle (int or ndarray): flap deflection angle (unit: degree).
            vs (float or ndarray): Vertical rate (unit: feet/min). Defaults to 0.
            landing_gear (bool): Is landing gear extended? Defaults to False.

        Returns:
            int or ndarray: Total drag (unit: N).

        """
        cd0 = self.polar["clean"]["cd0"]
        k = self.polar["clean"]["k"]

        # --- calc new CD0 ---
        lambda_f = self.polar["flaps"]["lambda_f"]
        cfc = self.polar["flaps"]["cf/c"]
        SfS = self.polar["flaps"]["Sf/S"]

        # Equation 3.45-3.46 in McCormick (1994), page 109.
        delta_cd_flap = (
            lambda_f
            * (cfc) ** 1.38
            * (SfS)
            * self.np.sin(flap_angle * self.np.pi / 180) ** 2
        )

        if landing_gear:
            # Equation 6.1 in Mair and Birdsall (1996)
            # 3.16e-5 is the K_uc factor value corresponding to
            # maximum flap deflection
            delta_cd_gear = (
                self.aircraft["limits"]["MTOW"]
                * self.aero.g0
                / self.aircraft["wing"]["area"]
                * 3.16e-5
                * self.aircraft["limits"]["MTOW"] ** (-0.215)
            )
        else:
            delta_cd_gear = 0

        cd0_total = cd0 + delta_cd_flap + delta_cd_gear

        # --- calc new k ---
        if self.aircraft["engine"]["mount"] == "rear":
            # See Figure 27.38 in Obert (2009)
            delta_e_flap = 0.0046 * flap_angle
        else:
            # See Figure 27.39 in Obert (2009)
            delta_e_flap = 0.0026 * flap_angle

        ar = self.aircraft["wing"]["span"] ** 2 / self.aircraft["wing"]["area"]
        k_total = 1 / (1 / k + self.np.pi * ar * delta_e_flap)

        D = self._calc_drag(mass, tas, alt, cd0_total, k_total, vs)
        return D
