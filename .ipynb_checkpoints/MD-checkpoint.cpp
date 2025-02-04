#include <iostream>
#include <cstdio>
#include <cmath>
#include <vector>

using namespace std;

void write_gro_file(FILE *fp, const char *title, int num_atoms,
                    const vector<double>& x, 
                    const vector<double>& y, 
                    const vector<double>& z,
                    double box_x, double box_y, double box_z)
{
    // Write the title line
    fprintf(fp, "%s\n", title);

    // Write the number of atoms
    fprintf(fp, "%5d\n", num_atoms);

    // Write atom details
    for (int i = 0; i < num_atoms; i++) {
        int res_num = 1;              // Residue number
        const char *res_name = "Ar";  // Residue name (Argon)
        const char *atom_name = "Ar"; // Atom name
        int atom_num = i + 1;         // Atom number (1-based index)

        // Format: %5d%-5s%5s%5d%8.3f%8.3f%8.3f
        fprintf(fp, "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n",
                res_num, res_name, atom_name, atom_num,
                x[i], y[i], z[i]);
    }

    // Write the box dimensions (x, y, z)
    fprintf(fp, "%10.5f%10.5f%10.5f\n", box_x, box_y, box_z);
}

inline double pbc(double x, double l)
{
    return x - floor(x/l)*l;
}

inline double min_img(double x, double l)
{
    return x - round(x/l)*l;
}

int main()
{
    /* initialization */
    const int N = 216;
    int n = cbrt(N);

    double rho = 0.8442, mass = 1.0, sig = 1.0, ep = 1.0;
    double rcut = 2.5*sig, kB = 1.0;
    double L = cbrt(mass*N/rho);
    double box_x = L, box_y = L, box_z = L;
    double rcut2 = rcut*rcut;
    long unsigned int nsteps = 10000;
    int out_freq = 10;
    double dt = 1e-3, dt2 = dt*dt;
    double kB = 1.0, T0 = 0.728;

    vector<double> x(N, 0), y(N, 0), z(N, 0);
    vector<double> vx(N, 0), vy(N, 0), vz(N, 0);
    vector<double> fx(N, 0), fy(N, 0), fz(N, 0);
    vector<double> new_fx(N, 0), new_fy(N, 0), new_fz(N, 0);

    int ctr = 0;
    double spacing = 1.0;

    for(int i=0; i<n; i++)
    {
        for(int j=0; j<n; j++)
        {
            for(int k=0; k<n; k++)
            {
                x[ctr] = i*spacing;
                y[ctr] = j*spacing;
                z[ctr] = k*spacing;
                ctr++;
            }
        }
    }

    FILE *init = fopen("init.gro", "w");
    write_gro_file(init, "initial config", N, x, y, z, box_x, box_y, box_z);
    fclose(init);


    double pe = 0.0, ke = 0.0;
    /* initialization */

    /* calculate forces before time loop */
    for(int i=0; i<N; i++)
    {
        for(int j=i+1; j<N; j++)
        {
            /* min image convention */
            double dx = min_img(x[j] - x[i], box_x);
            double dy = min_img(y[j] - y[i], box_y);
            double dz = min_img(z[j] - z[i], box_z);
            /* min image convention */

            double r2 = dx*dx + dy*dy + dz*dz;

            if(r2 > rcut2)
            {
                continue;
            }

            double r = sqrt(r2);

            double sig_by_r6 = pow(sig/r, 6);

            double ff = 48*ep*(sig_by_r6*sig_by_r6 - 0.5*sig_by_r6)/r2;
            pe += 4*ep*(sig_by_r6*sig_by_r6 - sig_by_r6);

            fx[i] += ff*dx;
            fy[i] += ff*dy;
            fz[i] += ff*dz;
            
            fx[j] -= ff*dx;
            fy[j] -= ff*dy;
            fz[j] -= ff*dz;
        }
    }
    /* calculate forces before time loop */

    /* time loop */
    FILE *out = fopen("md.gro", "w");
    for(size_t t=0; t<nsteps; t++)
    {
        /* update coordinates */
        for(int i=0; i<N; i++)
        {
            x[i] = x[i] + vx[i]*dt + 0.5*fx[i]*dt2/mass;
            y[i] = y[i] + vy[i]*dt + 0.5*fy[i]*dt2/mass;
            z[i] = z[i] + vz[i]*dt + 0.5*fz[i]*dt2/mass;

            /* PBC */
            x[i] = pbc(x[i], box_x);
            y[i] = pbc(y[i], box_y);
            z[i] = pbc(z[i], box_z);
            /* PBC */
        }
        /* update coordinates */

        /* calculate new forces */
        for(int i=0; i<N; i++)
        {
            for(int j=i+1; j<N; j++)
            {
                /* min image convention */
                double dx = min_img(x[i] - x[j], box_x);
                double dy = min_img(y[i] - y[j], box_y);
                double dz = min_img(z[i] - z[j], box_z);
                /* min image convention */

                double r2 = dx*dx + dy*dy + dz*dz;

                if(r2 > rcut2)
                {
                    continue;
                }

                double r = sqrt(r2);
                if(r < 0.1)
                {
                    cout<<i<<" "<<j<<" "<<r<<endl;
                    return 0;
                }
                double sig_by_r6 = pow(sig/r, 6);

                double ff = 48*ep*(sig_by_r6*sig_by_r6 - 0.5*sig_by_r6)/r2;
                pe += 4*ep*(sig_by_r6*sig_by_r6 - sig_by_r6);

                new_fx[i] += ff*dx;
                new_fy[i] += ff*dy;
                new_fz[i] += ff*dz;
                
                new_fx[j] -= ff*dx;
                new_fy[j] -= ff*dy;
                new_fz[j] -= ff*dz;
            }
        }
        /* calculate new forces */

        /* update velocities */
        double vcom_x = 0.0, vcom_y = 0.0, vcom_z = 0.0;
        for(int i=0; i<N; i++)
        {
            vx[i] = vx[i] + 0.5*(fx[i] + new_fx[i])*dt;
            vy[i] = vy[i] + 0.5*(fy[i] + new_fy[i])*dt;
            vz[i] = vz[i] + 0.5*(fz[i] + new_fz[i])*dt;

            /* accumulating COM drift */
            vcom_x += mass*vx[i];
            vcom_y += mass*vy[i];
            vcom_z += mass*vz[i];
            /* accumulating COM drift */
        }

        vcom_x /= N; vcom_y /= N; vcom_z /= N; 
        /* update velocities */

        /* perform corrections and updates in a final particle loop */
        double ke = 0.0;
        for(int i=0; i<N; i++)
        {
            // remove COM drift
            vx[i] -= vcom_x; vy[i] -= vcom_y; vz[i] -= vcom_z; 

            ke += vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i];

            // copy forces
            fx[i] = new_fx[i]; fy[i] = new_fy[i]; fz[i] = new_fz[i];

            // set new_f to 0
            new_fx[i] = 0.0; new_fy[i] = 0.0; new_fz[i] = 0.0; 
        }
        /* perform corrections and updates in a final particle loop */

        /* scale temperature using v-rescale */
        double scale = sqrt(3*N*kB*T0/(mass*ke));
        for(int i=0; i<N; i++)
            {
                
            }
        /* scale temperature using v-rescale */
        
        /* write outputs */
        ke = 0.5*mass*ke/N; // KE per particle
        pe /= N;            // PE per particle

        if(t%out_freq == 0)
        {
            printf("%d, %.6f, %.6f, %.6f\n", t, pe, ke, pe + ke);
            write_gro_file(init, "initial config", N, x, y, z, box_x, box_y, box_z);
        }
        /* write outputs */
    }
    fclose(out);
    /* time loop */

    return 0;
}
