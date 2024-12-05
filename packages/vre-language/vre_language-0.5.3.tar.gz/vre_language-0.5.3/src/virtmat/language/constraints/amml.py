"""checks / constraints for AMML objects"""
from textx import get_children_of_type
from virtmat.language.utilities.errors import raise_exception, StaticValueError
from virtmat.language.utilities.textx import get_reference
from virtmat.language.utilities.ase_params import spec

compat_calc = {
  'single point': ['energy', 'forces', 'dipole', 'stress', 'charges', 'magmom', 'magmoms'],
  'local minimum': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory'],
  'global minimum': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory'],
  'transition state': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory'],
  'normal modes': ['vibrational_energies', 'energy_minimum', 'transition_state'],
  'micro-canonical': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory'],
  'canonical': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory'],
  'isothermal-isobaric': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory'],
  'grand-canonical': ['energy', 'forces', 'dipole', 'stress', 'charges', 'trajectory']
}


def check_amml_property_processor(model, _):
    """check compatibility of properties with calculator task"""
    for obj in get_children_of_type('AMMLProperty', model):
        assert obj.calc or obj.algo
        task = obj.calc and get_reference(obj.calc).task
        calc = obj.calc and get_reference(obj.calc).name
        algo = obj.algo and get_reference(obj.algo).name
        mstr = f'algo \"{str(algo or str())}\" or calc \"{str(calc or str())}\"'
        tstr = f'task \"{str(task or str())}\"'
        for name in obj.names:
            if algo and name not in spec[algo]['properties']:
                if calc:
                    if name not in spec[calc]['properties']:
                        msg = f'property \"{name}\" not available in {mstr}'
                        raise_exception(obj, StaticValueError, msg)
                else:
                    msg = f'property \"{name}\" not available in {mstr}'
                    raise_exception(obj, StaticValueError, msg)
            if not algo and task and name not in compat_calc[task]:
                msg = f'property \"{name}\" not available in {tstr}'
                raise_exception(obj, StaticValueError, msg)
