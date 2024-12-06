from . import _cupy_numpy as xp
import numpy as np
import pyfastchem
from io import open
import configparser
from pkg_resources import resource_filename

from ._interpolator_3D import regular_grid_interp

class AbundanceGetter:
    def __init__(self, include_condensation=True):
        config = configparser.ConfigParser()
        config.read(resource_filename(__name__, "data/abundances/properties.cfg"))
        properties = config["DEFAULT"]
        self.min_temperature = float(properties["min_temperature"])
        self.logZs = xp.linspace(float(properties["min_logZ"]),
                                 float(properties["max_logZ"]),
                                 int(properties["num_logZ"]))
        self.CO_ratios = xp.array(eval(properties["CO_ratios"]))
        self.included_species = eval(properties["included_species"])

        if include_condensation:
            filename = "with_condensation.npy"
        else:
            filename = "gas_only.npy"

        abundances_path = "data/abundances/{}".format(filename)

        self.log_abundances = xp.log10(xp.load(
            resource_filename(__name__, abundances_path)))


    def get_abunds_from_fastchem(self, logZ, CO_ratio, NO_ratio):
        min_t = 1
        max_t = 6
        
        T_grid_full = np.arange(100, 4100, 100)
        T_grid_small = np.arange(100, 4100, 100)[min_t : max_t] #optimization
        
        P_grid = 10.0**np.arange(-9, 4)
        included_species = ["e-", "H", "H1-", "He", "C", "N", "O", "Na", "Fe", "Ca", "Ti", "K", "Ni", "H2", "N2", "O2", "H1O1",
                            "C1O1", "N1O1", "O1Si1", "O1Ti1", "O1V1", "C1H1N1_1", "C1H4", "C1O2", "H2O1", "H2S1", "H3N1", 
                            "H3P1", "N1O2", "O2S1", "O3", "C2H2", "Fe1H1"]
        P, T = np.array([(p, t) for t in T_grid_small for p in P_grid]).T
        fastchem = pyfastchem.FastChem("/home/stanley/packages/FastChem/input/element_abundances/asplund_2020.dat",
                                       "/home/stanley/packages/FastChem/input/logK/logK.dat",
                                       "/home/stanley/packages/FastChem/input/logK/logK_condensates.dat",
                                       0)
        if logZ > 2.9 and CO_ratio < 0.3:
            #Seems to run into numerical issues        
            fastchem.setParameter("minDensityExponentElement", -1920.0)

        fastchem.setParameter("nbIterationsChem", 60000)

        element_abundances = np.array(fastchem.getElementAbundances())
        for i in range(fastchem.getElementNumber()):
            symbol = fastchem.getGasSpeciesSymbol(i)
            if symbol != 'H' and symbol != 'He':
                element_abundances[i] *= 10**logZ

        index_C = fastchem.getElementIndex('C')
        index_O = fastchem.getElementIndex('O')
        index_N = fastchem.getElementIndex('N')

        sum_CON = element_abundances[index_C] + element_abundances[index_O] + element_abundances[index_N]
        element_abundances[index_O] = sum_CON / (1 + CO_ratio + NO_ratio)
        element_abundances[index_C] = CO_ratio * element_abundances[index_O]
        element_abundances[index_N] = NO_ratio * element_abundances[index_O]

        fastchem.setElementAbundances(element_abundances)

        #create the input and output structures for FastChem
        input_data = pyfastchem.FastChemInput()
        output_data = pyfastchem.FastChemOutput()

        input_data.temperature = T
        input_data.pressure = P
        input_data.equilibrium_condensation = False

        fastchem_flag = fastchem.calcDensities(input_data, output_data)
        #print("FastChem reports for {}, {}:".format(logZ, CO_ratio), pyfastchem.FASTCHEM_MSG[fastchem_flag])
        if fastchem_flag != pyfastchem.FASTCHEM_SUCCESS:
            raise Error("FastChem failed with flag {}".format(fastchem_flag))

        number_densities = np.array(output_data.number_densities)
        abundances = []
        for i in range(len(included_species)):
            index = fastchem.getGasSpeciesIndex(included_species[i])
            abundances.append(number_densities[:,index].reshape((len(T_grid_small), len(P_grid))))

        abundances = np.array(abundances)
        abundances /= abundances.sum(axis=0)
        #import pdb
        #pdb.set_trace()
        full_abunds = np.zeros((abundances.shape[0], len(T_grid_full), len(P_grid)))
        full_abunds[:,min_t:max_t] = abundances
        return xp.array(full_abunds)

    def get(self, logZ, CO_ratio, NO_ratio):
        '''Get an abundance grid at the specified logZ and C/O ratio.  This
        abundance grid can be passed to TransitDepthCalculator, with or without
        modifications.  The end user should not need to call this except in
        rare cases.

        Returns
        -------
        abundances : dict of xp.ndarray
            A dictionary mapping species name to a 2D abundance array, specifying
            the number fraction of the species at a certain temperature and
            pressure.'''
        #interp_log_abund = 10**regular_grid_interp(self.logZs, self.CO_ratios, self.log_abundances, xp.float32(logZ), xp.float32(CO_ratio))
        interp_log_abund = self.get_abunds_from_fastchem(logZ, CO_ratio, NO_ratio)

        abund_dict = {}
        for i, s in enumerate(self.included_species):
            abund_dict[s] = interp_log_abund[i]

        return abund_dict

    def is_in_bounds(self, logZ, CO_ratio, T):
        '''Check to see if a certain metallicity, C/O ratio, and temperature
        combination is within the supported bounds'''
        if T <= self.min_temperature:
            return False
        if logZ <= self.logZs.min() or logZ >= self.logZs.max():
            return False
        if CO_ratio <= self.CO_ratios.min() or \
           CO_ratio >= self.CO_ratios.max():
            return False
        return True

    @staticmethod
    def from_file(filename):
        '''Reads abundances file in the ExoTransmit format (called "EOS" files
        in ExoTransmit), returning a dictionary mapping species name to an
        abundance array of dimension'''
        line_counter = 0

        species = None
        temperatures = []
        pressures = []
        compositions = []
        abundance_data = dict()

        with open(filename) as f:
            for line in f:
                elements = line.split()
                if line_counter == 0:
                    assert(elements[0] == 'T')
                    assert(elements[1] == 'P')
                    species = elements[2:]
                elif len(elements) > 1:
                    elements = xp.array([float(e) for e in elements])
                    temperatures.append(elements[0])
                    pressures.append(elements[1])
                    compositions.append(elements[2:])

                line_counter += 1

        temperatures = xp.array(temperatures)
        pressures = xp.array(pressures)
        compositions = xp.array(compositions)

        N_temperatures = len(xp.unique(temperatures))
        N_pressures = len(xp.unique(pressures))

        for i in range(len(species)):
            c = compositions[:, i].reshape((N_pressures, N_temperatures)).T
            # This file has decreasing temperatures and pressures; we want
            # increasing temperatures and pressures
            c = c[::-1, ::-1]
            abundance_data[species[i]] = c
        return abundance_data
