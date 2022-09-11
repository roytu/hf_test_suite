
import numpy
from pyscf import lib
from pyscf import gto
from pyscf import scf
from pyscf.scf import dhf

class Molecule(object):
    def __init__(self, _id, name, xyz_path):
        self._id = name
        self.name = name
        self.xyz_path = xyz_path

    def build_mol(self, basis):
        return mol

    def compute_energy(self, basis, hf_func_name):
        # Construct molecule in basis
        mol = gto.Mole()
        mol.build(atom=self.xyz_path, basis=basis)

        # Specify HF variant
        hf_func = {
            "rhf": scf.RHF,
            "rohf": scf.ROHF,
            "uhf": scf.UHF
        }[hf_func_name]
        hf = hf_func(mol)
        hf.conv_tol = 1e-11

        # Solve for energy
        energy = hf.kernel()

        return energy
