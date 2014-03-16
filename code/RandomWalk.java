// RandomWalk.java
// A simple random walk demonstration.
// Coded by Mike De Palatis	<mdepalatis@mail.utexas.edu>
// 06.21.2004.

// NOTES ON RUNNING:
// After each step is over, a new color is selected.  Thus, you can see visually
// the end of one step and the beginning of the next where there is a color change.

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

// RandomWalk class.
// Controls the demonstration.
public class RandomWalk
{	
	public static void main(String[] args) throws Exception
	{
		// Random number generator.
		Random rand = new Random(System.currentTimeMillis());
		
		// Swing components.
		JFrame frame = new JFrame("Random Walk Demonstration");
		JPanel canvas = new JPanel(true);	// Enable double buffering.
		
		// Current position, direction, and color.
		int x, y;
		int xd, yd;
		int curr_color = 0;
		Color[] colors = { Color.black, Color.blue, Color.cyan, Color.darkGray,
			Color.gray, Color.green, Color.lightGray, Color.magenta, Color.pink,
			Color.red, Color.yellow };
		Color color;
		
		// Step size and step counter.
		final int STEP_SIZE = 10;
		int steps = 0;
		
		// Set the canvas and fram sizes to 800x600.
		frame.setSize(800, 600);
		canvas.setSize(800, 600);
		
		// Initialize the frame.
		frame.getContentPane().add(canvas);
		frame.setVisible(true);
		frame.addWindowListener(new WindowAdapter()
		{
			public void windowClosing(WindowEvent e)
			{
				System.exit(0);
			}
		});
		
		// Create a back buffer and use its graphics object.
		Image buffer = canvas.createImage(800, 600);
		Graphics g = buffer.getGraphics();
		
		// Clear the canvas and move the origin to the center.
		Dimension d = canvas.getSize();
		g.setColor(Color.white);
		g.fillRect(0, 0, d.width, d.height);
		g.translate(d.width / 2, d.height / 2);
		
		// Pick random initial conditions.
		x = rand.nextInt() % 100;
		y = rand.nextInt() % 100;
		xd = rand.nextInt() % 2;
		yd = rand.nextInt() % 2;
		color = colors[curr_color++];
		g.setColor(color);
		
		// Main loop.
		while(true)
		{
			// Walk for the fixed number of steps.
			if(steps <= STEP_SIZE)
			{
				// Draw it.
				g.drawLine(x, y, x + xd, y + yd);
				
				// Update position.
				x += xd;
				y += yd;
				
				// Increment step counter.
				steps++;
			}
			else
			{
				// Set direction.
				xd = rand.nextInt() % 2;
				yd = rand.nextInt() % 2;
				
				// Set new color.
				if(curr_color >= colors.length)
					curr_color = 0;
				color = colors[curr_color++];
				g.setColor(color);
				
				// Reset the step counter.
				steps = 0;
			}
			
			// Flip the buffers.
			d = canvas.getSize();
			canvas.getGraphics().drawImage(buffer, 0, 0, null);
			
			// Wait a short time.
			Thread.sleep(30);
		}
	}
}

