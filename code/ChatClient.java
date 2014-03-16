/*
  File: ChatClient.java

  Description: A simple chat client that goes along with the ChatServer server.

  Student Name: Michael DePalatis

  Course Name / Unique Number: CS 313E / 50885

  Date Created: 04.30.2004

  Date Last Modified: 05.06.2004

*/

import java.io.*;
import java.net.*;

// Input thread class (gets the messages from the server).
class InputThread extends Thread
{
	// Input.
	private BufferedReader in;

	// Constructor.
	public InputThread(BufferedReader reader)
	{
		in = reader;
	}
	
	// Main loop.
	public void run()
	{
		while(true)
		{
			try
			{
				// Get the message from the server.
				String msg = in.readLine();
				
				// If the message was nothing, don't worry about it.
				if(msg == null)
					break;
					
				// Display the message locally.
				else
					System.out.println(msg);
			}
			catch(Exception e)
			{
				e.printStackTrace();
			}
		}
	}
}

// Output thread class (sends messages to the server for broadcast).
class OutputThread extends Thread
{
	// Output.
	private PrintWriter out;
	
	// Input (from client).
	private BufferedReader in;
	
	// Constructor.
	public OutputThread(PrintWriter writer)
	{
		out = writer;
		in = new BufferedReader(new InputStreamReader(System.in));
	}
	
	// Main loop.
	public void run()
	{
		while(true)
		{
			try
			{
				// Read the user's message.
				String msg = in.readLine();
				
				// Send the message to the server.
				out.println(msg);
				out.flush();
				
				// Make sure we exit if BYE was typed.
				if(msg.trim().equals("BYE"))
					System.exit(0);
			}
			catch(Exception e)
			{
				e.printStackTrace();
			}
		}
	}
}

// Client program.
public class ChatClient
{
	// Reader and writer objects.
	public static BufferedReader in;
	public static PrintWriter out;
	
	// Socket used to connect to the server.
	private static Socket connection;

	// Main method.
	public static void main(String[] args)
	{
		// Variables.
		String msg = new String("");	// message to be sent.
		InputThread input;
		OutputThread output;

		// Connect to the server.
		try
		{
			// Attempt to get the hostname from the commandline.
			String hostname;
			if(args.length > 0)
				hostname = args[0];
			else
				hostname = "localhost";

			// Make the connection.
			connection = new Socket(hostname, 8042);

			// Create the input and output objects.
			in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
			out = new PrintWriter(new OutputStreamWriter(connection.getOutputStream()));
			
			// Initialize the input and output threads.
			input = new InputThread(in);
			output = new OutputThread(out);
			
			// Spawn the input and output threads.
			input.start();
			output.start();
		}
		catch(ConnectException e)
		{
			System.out.println("Connection refused.  Exiting...");
			System.exit(0);
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
}

