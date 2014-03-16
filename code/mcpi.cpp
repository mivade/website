// mcpi.cpp
// A simple Monte Carlo method for calculating pi.
// This works by taking the first quadrant of the unit circle and
// picking random points between (0, 0) and (1, 1). The probability
// that a random point is contained within the unit circle is P =
// pi/4, so we can use this to calculate pi.

#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <cmath>

// Returns a random double between 0 and 1.
double rand_dbl()
{
    return (double)rand()/((double)RAND_MAX + (double)1);
}

// Calculates pi.
double pi(double inside, double total)
{
    double P = inside/total;
    return 4*P;
}

// Main program.
int main()
{
    // Variables.
    double inside = 0.0,	// Number of points inside unit circle.
	total = 0.0;		// Total number of points.
    unsigned int loop_limit = (int)1e15;

    // Seed random number generator.
    srand(time(0));
    
    // Loop to find pi.
    for(int i=0; i<loop_limit; i++)
    {
	// Pick a random point between (0, 0) and (1, 1).
	double x = rand_dbl();
	double y = rand_dbl();
	
	// Determine if (x, y) is within the unit circle.
	double r = sqrt(x*x + y*y);
	if(r < 1.0)
	    inside = inside + 1.0;
	total = total + 1.0;

	// Report status from time to time.
	if(i%5000 == 0)
	{
	    std::cout << "Value of pi as of iteration " << i << " is " <<
		std::setprecision(10) << pi(inside, total) << std::endl;
	}
    }

    // Output whatever we found for pi.
    std::cout << "After " << loop_limit << " iterations, pi = " << 
	std::setprecision(10) << pi(inside, total) << std::endl;

    // Done.
    return 1;
}
