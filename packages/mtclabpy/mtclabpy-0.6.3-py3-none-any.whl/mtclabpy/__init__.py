"""
mtclabpy - A comprehensive tool for molecular and enzyme calculations
"""

__version__ = "0.6.3"

from . import kcat_prediction
from . import solubility
from . import molecular_pockets
from . import mutations
from . import affinities
from . import Enzyme_Self_Calc
from . import molecular_docking
from . import developmental_tree
from . import self_service_calculation_of_enzyme_resources
from .kcat_prediction import dlkcat
from .self_service_calculation_of_enzyme_resources.self_service import enzyme_self_calc

__all__ = [
    'kcat_prediction',
    'solubility',
    'molecular_pockets',
    'mutations',
    'affinities',
    'Enzyme_Self_Calc',
    'molecular_docking',
    'developmental_tree',
    'self_service_calculation_of_enzyme_resources',
    'enzyme_self_calc'
]