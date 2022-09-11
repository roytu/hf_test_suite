
"""
TABS database of molecules

https://www2.unb.ca/~ajit/download.htm
https://www.sciencedirect.com/science/article/abs/pii/S2210271X14002400?via%3Dihub
"""

import json
import os
import timeit
from pyscf import gto

from molecule import Molecule


class Database(object):

    BASIS_FUNCS = ["sto-3g", "sto-6g", "321g"]

    def __init__(self):
        self.molecules = {}

    def read_all_molecules(self, direc="tabs"):
        for xyz_name in os.listdir(direc):
            if not xyz_name.endswith(".xyz"):
                continue

            # Get ID
            id_ = xyz_name[:-4]  # id_ = Mxxxx

            # Get full path
            full_xyz_path = os.path.join(direc, xyz_name)

            # Get name
            with open(full_xyz_path, "r") as f:
                name = f.readlines()[1].strip()

            # Build molecule
            mol = Molecule(id_, name, full_xyz_path)
            self.molecules[id_] = mol

    def run_tests(self):
        for id_, mol in self.molecules.items():
            print(f"Running tests for {id_}:")
            print(f"{mol.name}")
            for basis_func in Database.BASIS_FUNCS:
                t0 = timeit.default_timer()
                e = mol.compute_energy(basis_func, "rhf")
                t1 = timeit.default_timer()

                # Save result
                j = {
                    "id": id_,
                    "name": mol.name,
                    "energy": e,
                    "basis": basis_func,
                    "hf": "rhf",
                    "runtime": t1 - t0
                }

                with open(f"results/{id_}_{basis_func}_rhf.json", "w") as f:
                    json.dump(j, f)

            print("")

if __name__ == "__main__":
    db = Database()
    db.read_all_molecules()
    db.run_tests()
