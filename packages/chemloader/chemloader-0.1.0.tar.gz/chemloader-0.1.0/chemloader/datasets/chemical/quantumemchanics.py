from typing import List, Tuple
from chemloader import (
    MolDataLoader,
    DataDownloader,
    UnTarFile,
    MolToStoragePipeline,
)
from rdkit import Chem
from rdkit.Chem import rdDistGeom
import os
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def compute_centroid(coords):
    return np.mean(coords, axis=0)


def kabsch(P, Q):
    """
    The Kabsch algorithm: finds the optimal rotation matrix that minimizes RMSD
    between two paired sets of points P and Q.
    """
    C = np.dot(np.transpose(P), Q)
    V, S, Wt = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(Wt)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    U = np.dot(V, Wt)
    return U


def hungarian_algorithm_(cost_matrix):
    """
    A simple implementation of the Hungarian (Munkres) algorithm using NumPy.
    This function returns two lists: row indices and column indices that represent the optimal assignment.
    """
    cost_matrix = cost_matrix.copy()
    n_rows, n_cols = cost_matrix.shape
    n = max(n_rows, n_cols)

    # Pad the cost matrix to make it square
    if n_rows != n_cols:
        pad_value = cost_matrix.max() + 1
        padded_matrix = np.full((n, n), pad_value)
        padded_matrix[:n_rows, :n_cols] = cost_matrix
        cost_matrix = padded_matrix
    else:
        padded_matrix = cost_matrix

    # Step 1: Subtract the row minimum from each row
    cost_matrix -= cost_matrix.min(axis=1)[:, np.newaxis]

    # Step 2: Subtract the column minimum from each column
    cost_matrix -= cost_matrix.min(axis=0)

    # Step 3: Cover all zeros with a minimum number of lines
    def cover_zeros(matrix):
        n = matrix.shape[0]
        covered_rows = np.zeros(n, dtype=bool)
        covered_cols = np.zeros(n, dtype=bool)
        zero_matrix = matrix == 0
        star_matrix = np.zeros_like(matrix, dtype=bool)
        prime_matrix = np.zeros_like(matrix, dtype=bool)

        # Step 3.1: Star zeros
        for i in range(n):
            for j in range(n):
                if zero_matrix[i, j] and not covered_rows[i] and not covered_cols[j]:
                    star_matrix[i, j] = True
                    covered_rows[i] = True
                    covered_cols[j] = True

        covered_rows[:] = False
        covered_cols[:] = False

        # Step 4 and beyond
        def find_a_zero():
            for i in range(n):
                for j in range(n):
                    if (
                        matrix[i, j] == 0
                        and not covered_rows[i]
                        and not covered_cols[j]
                    ):
                        return (i, j)
            return (-1, -1)

        def find_star_in_row(row):
            for j in range(n):
                if star_matrix[row, j]:
                    return j
            return -1

        def find_star_in_col(col):
            for i in range(n):
                if star_matrix[i, col]:
                    return i
            return -1

        def find_prime_in_row(row):
            for j in range(n):
                if prime_matrix[row, j]:
                    return j
            return -1

        while True:
            # Step 4: Cover columns containing starred zeros
            for i in range(n):
                for j in range(n):
                    if star_matrix[i, j]:
                        covered_cols[j] = True

            num_covered_cols = covered_cols.sum()
            if num_covered_cols >= n:
                break  # Algorithm finished

            while True:
                row, col = find_a_zero()
                if row == -1:
                    # Step 6: Add the smallest uncovered value to all uncovered elements
                    min_uncovered = np.min(matrix[~covered_rows][:, ~covered_cols])
                    matrix[~covered_rows, :] -= min_uncovered
                    matrix[:, ~covered_cols] += min_uncovered
                else:
                    # Step 5: Prime the zero
                    prime_matrix[row, col] = True
                    star_col = find_star_in_row(row)
                    if star_col != -1:
                        # Cover this row and uncover the starred column
                        covered_rows[row] = True
                        covered_cols[star_col] = False
                    else:
                        # Step 5.3: Augmenting path
                        # Construct a series of alternating primes and stars
                        path = [(row, col)]
                        while True:
                            star_row = find_star_in_col(path[-1][1])
                            if star_row == -1:
                                break
                            path.append((star_row, path[-1][1]))
                            prime_col = find_prime_in_row(path[-1][0])
                            path.append((path[-1][0], prime_col))
                        # Unstar all starred zeros in the path and star the primed zeros
                        for r, c in path:
                            if star_matrix[r, c]:
                                star_matrix[r, c] = False
                            else:
                                star_matrix[r, c] = True
                        # Clear covers and erase all primes
                        covered_rows[:] = False
                        covered_cols[:] = False
                        prime_matrix[:] = False
                        break

        # Extract the assignments from the starred zeros
        assignments = []
        for i in range(n_rows):
            for j in range(n_cols):
                if star_matrix[i, j]:
                    assignments.append((i, j))
        return zip(*assignments)  # Returns two tuples: rows, cols

    rows, cols = cover_zeros(cost_matrix)
    # Remove any padding if necessary
    assignments = []
    for r, c in zip(rows, cols):
        if r < n_rows and c < n_cols:
            assignments.append((r, c))
    if not assignments:
        return ([], [])
    rows, cols = zip(*assignments)
    return list(rows), list(cols)


def hungarian_algorithm(cost_matrix):
    cost_matrix = np.array(cost_matrix)
    if cost_matrix.ndim != 2:
        raise ValueError("Cost matrix must be 2D.")
    if cost_matrix.shape[0] != cost_matrix.shape[1]:
        raise ValueError("Cost matrix must be square.")

    C = cost_matrix.copy()
    C -= C.min(axis=1)[:, np.newaxis]
    C -= C.min(axis=0)

    n = C.shape[0]
    m = C.shape[1]
    row_covered = np.zeros(n, dtype=bool)
    col_covered = np.zeros(m, dtype=bool)
    marked = np.zeros(C.shape, dtype=int)  # Use int for possible states: 0, 1, 2

    def _find_zero():
        for i in range(n):
            for j in range(m):
                if C[i][j] == 0 and not row_covered[i] and not col_covered[j]:
                    return i, j
        return -1, -1

    def _cover_columns_with_starred_zero():
        for i in range(n):
            for j in range(m):
                if marked[i][j] == 1:
                    col_covered[j] = True

    # Step 1: Star zeros
    for i in range(n):
        for j in range(m):
            if C[i][j] == 0 and not row_covered[i] and not col_covered[j]:
                marked[i][j] = 1  # Starred
                row_covered[i] = True
                col_covered[j] = True

    row_covered[:] = False
    col_covered[:] = False

    # Step 2: Cover columns with starred zeros
    _cover_columns_with_starred_zero()

    while True:
        num_covered = np.sum(col_covered)
        if num_covered == n:
            break  # Optimal assignment found

        # Step 3: Find a non-covered zero and prime it
        done = False
        while not done:
            z = _find_zero()
            if z == (-1, -1):
                # Step 6: Add the smallest uncovered value to covered rows and subtract from uncovered columns
                smallest = np.min(C[~row_covered][:, ~col_covered])
                C[~row_covered] -= smallest
                C[:, col_covered] += smallest
                continue  # Continue searching for zeros
            i, j = z
            marked[i][j] = 2  # Prime it

            # Check if there's a starred zero in the same row
            star_col = np.where(marked[i] == 1)[0]
            if star_col.size:
                star_j = star_col[0]
                row_covered[i] = True
                col_covered[star_j] = False
            else:
                # Step 5: Augmenting path
                path = [(i, j)]
                while True:
                    star_row = np.where(marked[:, path[-1][1]] == 1)[0]
                    if star_row.size == 0:
                        break
                    star_i = star_row[0]
                    path.append((star_i, path[-1][1]))
                    prime_col = np.where(marked[path[-1][0]] == 2)[0][0]
                    path.append((path[-1][0], prime_col))

                # Flip the stars and primes along the path
                for r, c in path:
                    if marked[r][c] == 1:
                        marked[r][c] = 0
                    else:
                        marked[r][c] = 1

                row_covered[:] = False
                col_covered[:] = False
                marked[marked == 2] = 0
                _cover_columns_with_starred_zero()
                break

    # Extract the assignments
    assignments = []
    for i in range(n):
        for j in range(m):
            if marked[i][j] == 1:
                assignments.append((i, j))

    rows, cols = zip(*assignments)
    total_cost = cost_matrix[rows, cols].sum()
    return list(rows), list(cols), total_cost


def align_and_match(
    labels_a, coords_a, labels_b, coords_b, max_iterations=100, tol=1e-5
):
    """
    Aligns two sets of labeled coordinates and finds the best correspondence.
    """
    # Group atoms by label
    unique_labels = set(labels_a)
    if unique_labels != set(labels_b):
        raise ValueError("Both sets must have the same labels.")

    label_groups = {}
    for label in unique_labels:
        indices_a = [i for i, _label in enumerate(labels_a) if _label == label]
        indices_b = [i for i, _label in enumerate(labels_b) if _label == label]
        if len(indices_a) != len(indices_b):
            raise ValueError(f"Label {label} counts do not match.")
        label_groups[label] = (indices_a, indices_b)

    # Initialize correspondences (arbitrary)
    correspondences = {}
    for label, (indices_a, indices_b) in label_groups.items():
        correspondences[label] = list(zip(indices_a, indices_b))

    prev_rmsd = None

    for iteration in range(max_iterations):
        # Gather paired points
        paired_a = []
        paired_b = []
        for label, pairs in correspondences.items():
            for ia, ib in pairs:
                paired_a.append(coords_a[ia])
                paired_b.append(coords_b[ib])
        paired_a = np.array(paired_a)
        paired_b = np.array(paired_b)

        # Compute centroids
        centroid_a = compute_centroid(paired_a)
        centroid_b = compute_centroid(paired_b)

        # Center the points
        centered_a = paired_a - centroid_a
        centered_b = paired_b - centroid_b

        # Compute optimal rotation
        U = kabsch(centered_a, centered_b)
        rotated_a = np.dot(centered_a, U)

        # Compute RMSD
        diff = rotated_a - centered_b
        rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))
        # print(f"Iteration {iteration + 1}: RMSD = {rmsd}")

        if prev_rmsd is not None and abs(prev_rmsd - rmsd) < tol:
            break
        prev_rmsd = rmsd

        # Assign correspondences based on current alignment
        new_correspondences = {}
        for label, (indices_a, indices_b) in label_groups.items():
            # Compute distance matrix between label groups
            points_a = coords_a[indices_a]
            points_b = coords_b[indices_b]
            # Apply current rotation and translation to points_a
            transformed_a = (
                np.dot(points_a - compute_centroid(points_a), U) + centroid_b
            )
            # Compute cost matrix (Euclidean distances)
            cost_matrix = np.linalg.norm(
                transformed_a[:, np.newaxis, :] - points_b[np.newaxis, :, :], axis=2
            )
            # Solve assignment problem using custom Hungarian algorithm
            row_ind, col_ind, cost = hungarian_algorithm(cost_matrix)
            # print(f"Cost = {cost}")
            if len(row_ind) != len(indices_a):
                raise ValueError(
                    "Hungarian algorithm failed to find a complete assignment."
                )
            # Update correspondences
            new_correspondences[label] = list(
                zip(np.array(indices_a)[row_ind], np.array(indices_b)[col_ind])
            )
        correspondences = new_correspondences

    return correspondences, U, centroid_a, centroid_b, rmsd


def map_mol_to_xyz(mol: Chem.Mol, xyz: List[Tuple[str, float, float, float]]):
    if mol.GetNumAtoms() < len(xyz):
        mol = Chem.AddHs(mol)

    if mol.GetNumAtoms() != len(xyz):
        raise ValueError("Number of atoms in molecule and in file do not match.")

    labels_a = [a[0] for a in xyz]
    coords_a = np.array([a[1:] for a in xyz])

    labels_b = [atom.GetSymbol() for atom in mol.GetAtoms()]

    # assert sorted labels are the same
    if sorted(labels_a) != sorted(labels_b):
        raise ValueError("Atom labels do not match.")

    rdDistGeom.EmbedMolecule(mol)

    conf = mol.GetConformer()
    coords_b = np.array(
        [list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())]
    )

    (
        correspondences,
        rotation_matrix,
        centroid_a,
        centroid_b,
        final_rmsd,
    ) = align_and_match(labels_a, coords_a, labels_b, coords_b)
    # print("correspondences", correspondences)
    # print("rotation_matrix", rotation_matrix)
    # print("centroid_a", centroid_a)
    # print("centroid_b", centroid_b)
    # print("final_rmsd", final_rmsd)

    atom_map = {atom.GetIdx(): None for atom in mol.GetAtoms()}

    for label, pairs in correspondences.items():
        for ia, ib in pairs:
            atom_map[ia] = ib

    for atomidx, xyzidx in atom_map.items():
        conf.SetAtomPosition(atomidx, coords_a[xyzidx])

    return mol, atom_map


def qm9_make_molecule(
    smiles,
    partial_charges,
    atoms: List[Tuple[str, float, float, float]],
):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string provided.")

    mol, atom_map = map_mol_to_xyz(mol, atoms)

    # Add properties
    positions = np.array(
        [list(mol.GetConformer().GetAtomPosition(i)) for i in range(mol.GetNumAtoms())]
    )
    for atom in mol.GetAtoms():
        atom.SetDoubleProp("pc", partial_charges[atom_map[atom.GetIdx()]])
        atom.SetDoubleProp("x", positions[atom.GetIdx()][0])
        atom.SetDoubleProp("y", positions[atom.GetIdx()][1])
        atom.SetDoubleProp("z", positions[atom.GetIdx()][2])
    return mol


def qm9_parse_file(file_path):
    # Initialize data containers
    num_atoms = 0
    properties = {}
    atoms: List[Tuple[str, float, float, float]] = []
    partial_charges = []
    frequencies = []
    smiles = []
    # inchis = []

    # Property keys based on the provided list
    property_keys = [
        "tag",
        "index",
        "A",
        "B",
        "C",
        "mu",
        "alpha",
        "homo",
        "lumo",
        "gap",
        "r2",
        "zpve",
        "U0",
        "U",
        "H",
        "G",
        "Cv",
    ]

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Ensure the file has at least 2 lines
    if len(lines) < 2:
        raise ValueError(
            f"File '{file_path}' is too short to contain necessary information."
        )

    # Parse number of atoms
    num_atoms = int(lines[0].strip())

    # Parse properties
    properties_line = lines[1].strip().split()
    if len(properties_line) < 17:
        raise ValueError("Properties line does not contain all 17 properties.")
    for i, key in enumerate(property_keys):
        properties[key] = properties_line[i]

    # Parse atom lines
    for i in range(2, 2 + num_atoms):
        parts = (
            lines[i]
            .strip()
            .replace("*^", "e")  # sometimes floats are given e.g. with 1.213*^-6
            .split()
        )

        if len(parts) < 5:
            raise ValueError(f"Atom line {i+1} does not contain enough data.")
        element = parts[0]
        x, y, z = map(float, parts[1:4])
        charge = float(parts[4])
        atoms.append((element, x, y, z))
        partial_charges.append(charge)

    # Parse frequencies (line na+3)
    frequencies_line = lines[2 + num_atoms].strip().split()
    frequencies = list(map(float, frequencies_line))

    # Parse SMILES (line na+4)
    smiles_line = lines[3 + num_atoms].strip().split("\t")
    smiles = smiles_line

    # Parse InChI (line na+5)
    # inchis_line = lines[4 + num_atoms].strip().split("\t")
    # inchis = inchis_line
    try:
        mol = qm9_make_molecule(
            smiles=smiles[0],
            partial_charges=partial_charges,
            atoms=atoms,
        )
    except Exception:
        return None, None

    # Add properties
    del properties["tag"]
    inx = int(properties.pop("index"))

    for k, v in properties.items():
        mol.SetDoubleProp(k, float(v))

    # Add frequencies
    frequencies_csv = ",".join(map(str, frequencies))
    mol.SetProp("frequencies", frequencies_csv)

    # since this runs in a separate process, we need to make shure the mol is retunred as full pickle

    Chem.SetDefaultPickleProperties(Chem.PropertyPickleOptions.AllProps)

    return mol, inx


class ReadQM9Files(MolToStoragePipeline):
    def setup(self, dataloader, previous_step=None, force=False):
        self.fallback = "index"
        raw_file_folder = getattr(
            previous_step,
            "raw_file",
        )
        self.presetup(dataloader)

        if not os.path.isdir(raw_file_folder):
            raise FileNotFoundError(f"Expected folder {raw_file_folder} not found")

        try:
            files = [f for f in os.listdir(raw_file_folder) if f.endswith(".xyz")]
            file_paths = [os.path.join(raw_file_folder, f) for f in files]

            num_processes = max(
                1, min(cpu_count() - 1, len(file_paths))
            )  # Avoid creating unnecessary processes

            with Pool(processes=num_processes) as pool:
                with tqdm(total=len(file_paths), desc="Storing Mols") as pbar:
                    # Use imap_unordered for better performance with tqdm
                    for mol, idx in pool.imap_unordered(qm9_parse_file, file_paths):
                        if mol is not None:
                            self.setupstep(dataloader, mol, index=idx)
                        pbar.update()

        finally:
            self.postsetup()


class QM9(MolDataLoader):
    """

    mol properties:
        A         GHz          Rotational constant A
        B         GHz          Rotational constant B
        C         GHz          Rotational constant C
        mu        Debye        Dipole moment
        alpha     Bohr^3       Isotropic polarizability
        homo      Hartree      Energy of Highest occupied molecular orbital (HOMO)
        lumo      Hartree      Energy of Lowest occupied molecular orbital (LUMO)
        gap       Hartree      Gap, difference between LUMO and HOMO
        r2        Bohr^2       Electronic spatial extent
        zpve      Hartree      Zero point vibrational energy
        U0        Hartree      Internal energy at 0 K
        U         Hartree      Internal energy at 298.15 K
        H         Hartree      Enthalpy at 298.15 K
        G         Hartree      Free energy at 298.15 K
        Cv        cal/(mol K)  Heat capacity at 298.15 K
        frequencies  cm⁻¹      List of virational frequencies


    atom properties:
        x        Angstrom      X coordinate
        y        Angstrom      Y coordinate
        z        Angstrom      Z coordinate
        pc       e             Mulliken partial charge
    """

    citation = "https://doi.org/10.6084/m9.figshare.c.978904.v5"
    expected_data_size = 133_885
    expected_mol = 131_473

    setup_pipleline = [
        DataDownloader(
            src="https://springernature.figshare.com/ndownloader/files/3195389",
            raw_file_name="qm9.xyz.tar.bz2",
        ),
        UnTarFile(),
        ReadQM9Files(),
    ]
