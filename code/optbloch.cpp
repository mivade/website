/*
optbloch.cpp

Performs time step integration of the optical Bloch equations for a
two level atom (see, e.g., Metcalf and van der Straten, Laser Cooling
and Trapping).

To compile with gcc:
  g++ -ooptbloch optbloch.cpp
*/

#include <stdlib.h>
#include <complex.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <string>


using namespace std;

const double pi = 4*atan(1);

int main(int argc, char* argv[])
{
    // Variables
    double gamma = 500e3;
    double Omega = gamma,
	delta = -gamma;
    double T = 2*pi/Omega;
    double dt = T/1e4;

    // Initial conditions
    complex double rho_gg = 1,
	rho_ee = 0,
	rho_ge = 0,
	rho_eg = 0;

    // Data file
    string filename("rho.txt");
    ofstream rhofile;
    rhofile.open(filename.c_str());
    rhofile << "# t |rho_gg| |rho_ee|" << endl;

    // Time evolve
    for(double t=0; t<T; t+=dt)
    {
	complex double drho_gg = gamma*rho_ee + I*Omega*(rho_eg - rho_ge)/2.,
	    drho_ge = -1*(gamma/2.+I*delta)*rho_ge + I*Omega*(rho_ee - rho_gg)/2.;
	rho_gg += drho_gg*dt;
	rho_ee -= drho_gg*dt;
	rho_ge += drho_ge*dt;
	rho_eg += conj(drho_ge)*dt;
	rhofile << setprecision(3) << scientific
		<< t << ' ' << cabs(rho_gg) << ' ' 
	        << cabs(rho_ee) << endl;
    }
    rhofile.close();
 
    // Plot if requested
    bool plot = true;
    if(argc > 1 && atoi(argv[1]) != 1)
	plot = false;
    if(plot)
    {
	ofstream tmpfile;
	tmpfile.open("tmp.gp");
	tmpfile << "plot '" << filename << "' using 1:2 w l, \\" << endl
		<< "'" << filename << "' using 1:3 w l" << endl;
	tmpfile.close();
	system("gnuplot -persist tmp.gp");
	remove("tmp.gp");
    }

    return 0;
}
