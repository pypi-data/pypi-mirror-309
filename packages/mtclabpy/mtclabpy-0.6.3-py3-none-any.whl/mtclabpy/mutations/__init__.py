"""
Mutations analysis module
"""

from .CTR_projections import ctr_project
from .ddG_Prediction_Toolbox import ddg_predict
from .geoStab_prediction import geostab_predict
from .pssm_locus_information_organizer import pssm_organize
from .pssm_online_generation_tool import pssm_generate
from .seq_mutation_generation import generate_mutations

# Aliases for backward compatibility
pssm_generation = pssm_generate
seq2mutation = generate_mutations
pssm_result_2_excel = pssm_organize

__all__ = [
    'ctr_project',
    'ddg_predict',
    'geostab_predict',
    'pssm_organize',
    'pssm_generate',
    'generate_mutations',
    'pssm_generation',
    'seq2mutation',
    'pssm_result_2_excel'
]