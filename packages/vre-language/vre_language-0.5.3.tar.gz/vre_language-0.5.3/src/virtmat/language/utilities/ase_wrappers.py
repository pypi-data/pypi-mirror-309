"""wrapper classes for ASE calculators and algorithms"""
import importlib
from contextlib import contextmanager
import numpy
from matplotlib import pyplot
from ase import Atoms
from ase.utils import IOContext
from ase.io import read
from ase.io.trajectory import TrajectoryWriter
from ase.build import minimize_rotation_and_translation
from ase.geometry.analysis import Analysis
from ase.eos import EquationOfState
from ase.dft.dos import DOS
from ase.mep import NEBTools, DimerControl, MinModeAtoms, MinModeTranslate
from ase.calculators.singlepoint import SinglePointCalculator
from virtmat.language.utilities.errors import RuntimeValueError
from virtmat.language.utilities.ase_params import spec


@contextmanager
def plot_backend(backend):
    """a context manager for switching to a non-interactive backend and back"""
    assert backend in pyplot.rcsetup.all_backends
    current_backend = pyplot.get_backend()
    try:
        pyplot.switch_backend(backend)
        yield pyplot
    finally:
        pyplot.close()
        pyplot.switch_backend(current_backend)


class RMSD(IOContext):  # not covered
    """A wrapper algorithm to calculate root mean square deviation"""
    results = None

    def __init__(self, atoms):
        self.atoms_list = [atoms] if isinstance(atoms, Atoms) else atoms

    def run(self, reference, adjust=True):
        """Calculate the root mean square deviation (RMSD) between a structure
           and a reference"""
        assert len(reference) == 1
        rmsd = []
        for atoms in self.atoms_list:
            ref_atoms = reference.to_ase()[0]
            if adjust:
                minimize_rotation_and_translation(ref_atoms, atoms)
            rmsd.append(numpy.sqrt(numpy.mean((numpy.linalg.norm(atoms.get_positions()
                                   - ref_atoms.get_positions(), axis=1))**2, axis=0)))
        self.results = {'rmsd': numpy.mean(rmsd), 'output_structure': self.atoms_list}
        return True


class RDF(IOContext):
    """A wrapper algorithm to calculate radial distribution function"""
    results = None

    def __init__(self, atoms):
        self.atoms_list = [atoms] if isinstance(atoms, Atoms) else atoms
        if any(sum(sum(a.cell)) == 0 for a in self.atoms_list):
            # not covered
            msg = 'the structure cell must have at least one non-zero vector'
            raise RuntimeValueError(msg)

    def run(self, rmax=None, nbins=40, neighborlist=None, neighborlist_pars=None,
            elements=None):
        """Calculate the radial distribution function for a structure"""
        neighborlist_pars = neighborlist_pars or {}
        analysis = Analysis(self.atoms_list, neighborlist, **neighborlist_pars)
        rmax = rmax or 0.49*max(max(a.cell.lengths()) for a in self.atoms_list)
        ret = analysis.get_rdf(rmax, nbins, elements=elements, return_dists=True)
        self.results = {'rdf': numpy.mean([a for a, b in ret], axis=0),
                        'rdf_distance': numpy.mean([b for a, b in ret], axis=0)}
        return True


class EOS(IOContext):
    """A wrapper algorithm to fit the equation of state"""
    results = None

    def __init__(self, configs):
        assert isinstance(configs, list)
        self.volumes = [a.get_volume() for a in configs]

    def run(self, energies, eos='sjeos', filename=None):
        """v0: optimal volume, e0: minimum energy, B: bulk modulus"""
        obj = EquationOfState(self.volumes, energies, eos=eos)
        keys = ('minimum_energy', 'optimal_volume', 'bulk_modulus', 'eos_volume',
                'eos_energy')
        self.results = dict(zip(keys, obj.getplotdata()[1:7]))
        with plot_backend('agg'):
            obj.plot(filename)
        return True


class DensityOfStates(IOContext):  # no covered
    """A wrapper algorithm to calculate the density of states"""
    results = None

    def __init__(self, atoms):
        atoms.get_potential_energy()
        self.calc = atoms.calc

    def run(self, width=0.1, window=None, npts=401, spin=None):
        """add density of states and sampling energy points to results"""
        window = window if window is None else tuple(window.tolist())
        obj = DOS(self.calc, width=width, window=window, npts=npts)
        self.results = {'dos_energy': obj.get_energies(), 'dos': obj.get_dos(spin=spin)}
        return True


class BandStructure(IOContext):
    """A wrapper algorithm to calculate the band structure"""
    results = None

    def __init__(self, atoms):
        atoms.get_potential_energy()
        self.calc = atoms.calc

    def run(self, **kwargs):
        """add band structure path, energies, reference to results"""
        obj = self.calc.band_structure()
        keys = ('path', 'energies', 'reference')
        self.results = {'band_structure': {k: getattr(obj, k) for k in keys}}
        if kwargs.get('filename'):
            with plot_backend('agg'):
                obj.plot(**kwargs)
        return True


class NudgedElasticBand(IOContext):
    """a wrapper class for the NEB algorithm from ASE, no parallel NEB yet"""
    results = None
    attached = None

    def __init__(self, if_inp, **kwargs):
        assert isinstance(if_inp, list) and len(if_inp) == 2
        assert all(isinstance(a, Atoms) for a in if_inp)

        self.n_images = kwargs.pop('number_of_images')
        images = [if_inp[0]]
        for _ in range(self.n_images-2):
            image = if_inp[0].copy()
            image.calc = if_inp[0].calc  # should be copied for parallel
            image.set_constraint(if_inp[0].constraints)
            images.append(image)
        images.append(if_inp[1])

        if_inp[0].calc = SinglePointCalculator(if_inp[0],
                                               energy=if_inp[0].get_potential_energy(),
                                               forces=if_inp[0].get_forces())
        if_inp[1].calc = SinglePointCalculator(if_inp[1],
                                               energy=if_inp[1].get_potential_energy(),
                                               forces=if_inp[1].get_forces())
        interpolate_method = kwargs.pop('interpolate_method')
        interpolate_mic = kwargs.pop('interpolate_mic')
        self.dynamic_relaxation = kwargs.pop('dynamic_relaxation')
        if self.dynamic_relaxation:
            self.fmax = kwargs['fmax']
            class_name = 'DyNEB'
        else:
            del kwargs['fmax']
            del kwargs['scale_fmax']
            class_name = 'NEB'
        neb_class = getattr(importlib.import_module('ase.mep'), class_name)
        self.neb = neb_class(images, allow_shared_calculator=True, **kwargs)
        self.neb.interpolate(method=interpolate_method, mic=interpolate_mic,
                             apply_constraint=False)

    def attach(self, obj):
        """attach a trajectory object"""
        assert isinstance(obj, TrajectoryWriter)
        self.attached = obj

    def run(self, optimizer, fit=False, filename=None, logfile=None):
        """run an NEB simulation"""
        module = importlib.import_module(spec[optimizer['name']]['module'])
        opt_class = getattr(module, spec[optimizer['name']]['class'])
        fmax = optimizer['parameters'].pop('fmax', 0.05)
        if self.dynamic_relaxation:
            fmax = self.fmax
        optimizer['parameters'].pop('trajectory', None)
        if self.attached is None:
            raise RuntimeValueError('the NEB algorithm works only with (trajectory: true)')
        obj = opt_class(self.neb, trajectory=self.attached, logfile=logfile,
                        **optimizer['parameters'])
        converged = obj.run(fmax=fmax)
        images = read(f'{self.attached.filename}@-{self.n_images}:')
        self.results = {}
        self.results['final_images'] = images
        nebt = NEBTools(images)
        energies = nebt.get_barrier(fit=fit)
        self.results['activation_energy'] = energies[0]
        self.results['reaction_energy'] = energies[1]
        self.results['maximum_force'] = numpy.sqrt((self.neb.get_forces() ** 2).sum(axis=1).max())
        self.results['forces'] = [i.get_forces() for i in images]
        self.results['energy'] = [i.get_potential_energy() for i in images]
        if filename:
            with plot_backend('agg'):
                nebt.plot_band().savefig(filename)
        return converged


class Dimer(IOContext):
    """a wrapper class for the Dimer algorithm from ASE"""
    results = None

    def __init__(self, initial, mask=None, logfile=None, **kwargs):
        assert isinstance(initial, Atoms)
        self.atoms = initial
        self.logfile = logfile
        self.mask = mask if mask is None else mask.tolist()
        d_control = DimerControl(mask=self.mask, logfile=logfile, **kwargs)
        self.d_atoms = MinModeAtoms(self.atoms, d_control)
        self.displacement_method = kwargs.get('displacement_method')
        self.trajectory = None

    def attach(self, obj):
        """attach a trajectory object"""
        assert isinstance(obj, TrajectoryWriter)
        self.trajectory = obj
        self.trajectory.write()

    def run(self, target=None, fmax=0.05, **kwargs):
        """run a dimer simulation"""
        displ_kwargs = {'mic': any(self.atoms.pbc), 'log': self.logfile}
        if self.displacement_method == 'vector':
            if target is None:
                msg = 'target structure needed to calculate displacement vector'
                raise RuntimeValueError(msg)
            displ = target.to_ase()[0].positions - self.atoms.positions
            displ_kwargs['displacement_vector'] = 0.1*displ
        self.d_atoms.displace(**displ_kwargs)
        obj = MinModeTranslate(self.d_atoms, trajectory=self.trajectory,
                               logfile=self.logfile, **kwargs)
        converged = obj.run(fmax=fmax)
        self.results = {'energy': self.atoms.get_potential_energy(),
                        'forces': self.atoms.get_forces()}
        return converged
