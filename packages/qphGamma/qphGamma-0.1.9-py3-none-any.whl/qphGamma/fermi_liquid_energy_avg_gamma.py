import numpy as np
from scipy.stats import logistic
from scipy.interpolate import interp1d
from scipy import integrate
from .fermi_liquid_gamma import FLGamma
from .fermi_gas_dos import FermiGasDOS
from .fermi_gas_params import FGParams
import warnings

warnings.filterwarnings("ignore")


class FLAvgGamma:
    """
    class FLAvgGamma calculates the energy-averaged scattering rate predicted by the Fermil liquid following the Vignale method
    """

    def __init__(self, Te, N, V, E=np.linspace(-500, 500, 100000)) -> None:
        """Function returns below parameters

        Args:
            Te (float): electronic temperature in eV
            N (int): Number of electrons in cell
            V (float): Volume of cell in Angstrom cubed
            E (array): Energy array in eV from -500 to 500 eV
            E_qph (2D array): Energy-mu and total quasiparticle and quasihole scattering rates
            E_qh (2D array): Energy-mu and  quasihole scattering rates
            E_qp (2D array): Energy-mu and  quasiparticle scattering rates

        """
        self.E = E
        self.Te = Te
        self.N = int(N)
        self.V = V

        fl_data = FLGamma(self.E, self.Te, self.N, self.V)
        gamma_data = fl_data.gamma()
        self.E_qph = gamma_data[0]
        self.E_qh = gamma_data[1]
        self.E_qp = gamma_data[2]

    # get FG dos and then interpolates for data matching
    # The chemical potential should always be 0 eV for the scattering rates that are going to be used with this dos
    def get_fg_dos(self):
        # need this so that there is no interpolation out of range issue when shifting by mu
        E_range = np.linspace(-500, 5000, 1000000)
        fg_params = FGParams(self.Te, self.N, self.V)
        fg_dos = FermiGasDOS(E_range, self.V)
        interp_fg_dos = interp1d(
            E_range - fg_params.mu,
            fg_dos.dos,
            fill_value=(0, np.nan),
            bounds_error=False,
        )
        # mu is set to 0 eV
        return interp_fg_dos(self.E_qph[:, 0])

    # FD distribution
    def get_occ(self):
        # chemical potential should always be set to zero!
        return logistic.sf(self.E_qph[:, 0], 0, self.Te)

    def fl_gamma_occ_dos(self):
        E_qph = self.E_qph
        E = self.E_qph[:, 0]
        gamma = self.E_qph[:, 1]
        occ = FLAvgGamma.get_occ(self)
        dos = FLAvgGamma.get_fg_dos(self)
        return E, gamma, occ, dos

    def avg_fl_gamma(self):
        E_qph = self.E_qph
        E = self.E_qph[:, 0]
        gamma = self.E_qph[:, 1]
        occ = FLAvgGamma.get_occ(self)
        dos = FLAvgGamma.get_fg_dos(self)
        avg_gamma = integrate.simpson(gamma * occ * (1 - occ) * dos, E)
        return avg_gamma
