import numpy as np
from tqdm.auto import tqdm, trange

# functions
def write_gro(file_pointer, coordinates, velocities, box_dims, residue_name="Ar", atom_name="Ar"):
    r"""
    Appends a frame to a .gro file.

    Parameters:
    - file_pointer: Open file object in append mode.
    - coordinates: array of (x, y, z) tuples for atom positions in nm.
    - velocities:array of (vx, vy, vz) tuples for atom velocities in nm/ps.
    - box_dims: array of (x, y, z) for box dimensions in nm.
    - residue_name: Residue name (default: 'Ar').
    - atom_name: Atom name (default: 'Ar').

    Retuns:
    None
    """
    num_atoms = len(coordinates)

    # Write frame header and number of atoms
    file_pointer.write("Appended Frame\n")
    file_pointer.write(f"{num_atoms:5d}\n")

    # Write atom information
    for i, ((x, y, z), (vx, vy, vz)) in enumerate(zip(coordinates, velocities), start=1):
        residue_number = 1  # Default residue number
        atom_number = i
        file_pointer.write(f"{residue_number:5d}{residue_name:<5}{atom_name:>5}{atom_number:5d}{x:8.3f}{y:8.3f}{z:8.3f}{vx:8.4f}{vy:8.4f}{vz:8.4f}\n")

    # Write box dimensions
    file_pointer.write(f"{box_dims[0]:10.5f}{box_dims[1]:10.5f}{box_dims[2]:10.5f}\n")

# initialization
N = 216
n = int(np.cbrt(N))
rho = 0.8442
mass = 1.0
sig = 1.0
ep = 1.0
T = 0.728
kB = 1.0
dt = 0.001
rcut = 2.5*sig
spacing = 1.0
box = np.ones(3)*np.cbrt(N*mass/rho)
out_freq = 10#0 

coords = np.array([[i, j, k] for i in range(n) for j in range(n) for k in range(n)])*spacing
coords = coords - coords.mean(axis=0) + 0.5*box
velocities = np.random.normal(loc=0, scale=0.1, size=coords.shape)
velocities = velocities - np.mean(mass*velocities, axis=0) # remove COM drift


nsteps = int(1e3)
gro = open("md.gro", "w")

pe = 0.0
ke = 0.0
te = 0.0

pe_shift = 4*ep*(np.power(sig/rcut, 12) - np.power(sig/rcut, 6))

# calculate forces and potential energy initially
forces = np.zeros_like(coords)
for i in range(N):
    for j in range(i+1, N):
        dr = coords[i] - coords[j]
        dr = dr - box*np.round(dr/box) # minimum image convention
        r = np.linalg.norm(dr)

        if r > rcut:
            continue

        sig_by_r6 = np.power(sig/r, 6)

        ff = 48*(sig_by_r6*sig_by_r6 - 0.5*sig_by_r6)/r**2
        pe += 4*ep*(sig_by_r6*sig_by_r6 - sig_by_r6)

        forces[i] += ff*dr
        forces[j] -= ff*dr

iterator = trange(nsteps)
for t in iterator:    
    # update positions and velocities
    coords = coords + velocities*dt + 0.5*forces*dt*dt/mass # velocity verlet

    coords = coords - box*np.floor(coords/box) # PBC

    # calculate new forces and potential energy
    new_forces = np.zeros_like(coords)
    pe = 0.0
    for i in range(N):
        for j in range(i+1, N):
            dr = coords[i] - coords[j]
            dr = dr - box*np.round(dr/box) # minimum image convention
            r = np.linalg.norm(dr)
    
            if r > rcut:
                continue
    
            sig_by_r6 = np.power(sig/r, 6)
    
            ff = 48*(sig_by_r6*sig_by_r6 - 0.5*sig_by_r6)/r**2
            pe += 4*ep*(sig_by_r6*sig_by_r6 - sig_by_r6)
    
            new_forces[i] += ff*dr
            new_forces[j] -= ff*dr

    velocities = 0.5*(forces + new_forces)*dt/mass # velocity verlet

    forces = np.copy(new_forces)

    velocities = velocities - np.mean(mass*velocities, axis=0) # remove COM drift

    # write output
    if not t%out_freq:
        write_gro(gro, coords, velocities, box, residue_name="Ar", atom_name="Ar")

    # update progress bar
    pe = pe/N + pe_shift 
    ke = 0.5*mass*np.sum(velocities**2)/N
    
    iterator.set_postfix_str(f"PE = {pe:.3e}, KE={ke:.3e}, TE={pe+ke:.3e}")

gro.close()