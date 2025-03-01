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

def potential(r, sigma, ep, alpha, beta):
    return 0.0 # write the expression of the potential here

def force(r, sigma, ep, alpha, beta):
    return 0.0 # write the expression of the force here


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
out_freq = 10
nsteps = int(2e3)

coords = np.array([[i, j, k] for i in range(n) for j in range(n) for k in range(n)])*spacing
velocities = np.random.normal(loc=0, scale=1.0, size=coords.shape)
velocities = velocities - np.mean(mass*velocities, axis=0) # remove COM drift

pe = 0.0
ke = 0.0
te = 0.0

# ============================================= #
# change these values as per the question paper #

alpha = 0.0 
beta = 0.0

# change these values as per the question paper #
# ============================================= #

pe_shift = potential(rcut, sig, ep, alpha, beta)

# calculate initial forces
forces = np.zeros_like(coords)
for i in range(N):
    for j in range(i+1, N):
        dr = coords[i] - coords[j]
        dr -= np.round(dr/box)*box # min img
        r = np.linalg.norm(dr)

        if r > rcut:
            continue

        ff = force(r, sig, ep, alpha, beta)
        pe += (potential(r, sig, ep, alpha, beta) - pe_shift)

        forces[i] += ff*dr/r
        forces[j] -= ff*dr/r

ke = 0.5*mass*np.sum(velocities**2)

# time loop
iterator = trange(int(1e3))

dt2 = dt*dt/mass

gro = open("nve.gro", "w")
write_gro(gro, coords, velocities, box)

nrg = open("energies_nve.txt", "w")
nrg.write("#time, step, KE, PE, TE\n")
nrg.write(f"0.0, 0, {ke/N:.6f}, {pe/N:.6f}, {(ke+pe)/N:.6f}\n")

for t in iterator:
    coords = coords + velocities*dt + 0.5*forces*dt2
    coords -= np.floor(coords/box)*box

    new_forces = np.zeros_like(forces)
    new_pe = 0.0
    for i in range(N):
        for j in range(i+1, N):
            dr = coords[i] - coords[j]
            dr -= np.round(dr/box)*box # min img
            r = np.linalg.norm(dr)
    
            if r > rcut:
                continue
    
            ff = force(r, sig, ep, alpha, beta)
            new_pe += (potential(r, sig, ep, alpha, beta) - pe_shift)
            
            new_forces[i] += ff*dr/r
            new_forces[j] -= ff*dr/r

    velocities = velocities + 0.5*(forces + new_forces)*dt/mass

    velocities -= np.mean(mass*velocities, axis=0) # remove COM momentum
    
    forces = np.copy(new_forces)
    pe = new_pe
    ke = 0.5*mass*np.sum(velocities**2)

    if (t+1)%out_freq == 0:
        write_gro(gro, coords, velocities, box)
        nrg.write(f"{(t+1)*dt:.6f}, {t+1}, {ke/N:.6f}, {pe/N:.6f}, {(ke+pe)/N:.6f}\n")
    
    iterator.set_postfix_str(f"KE={ke/N:.6f}, PE={pe/N:.6f}, TE={(ke+pe)/N:.6f}")

with open("final.gro", "w") as w:
    write_gro(w, coords, velocities, box)

gro.close()
nrg.close()

print("""Trajectory file has been written to nve.gro.
The final snapshot has been written to final.gro"""
