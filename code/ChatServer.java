/*
  File: ChatServer.java

  Description: The server for a simple chat client/server interface.  Uses port 8042.

  Student Name: Michael DePalatis

  Course Name / Unique Number: CS 313E / 50885

  Date Created: 04.30.2004

  Date Last Modified: 05.06.2004

*/

import java.util.*;
import java.io.*;
import java.net.*;

// A thread for each connection.
class ChatThread extends Thread
{
	// Data.
	private Socket connection;
	private String name;
	private int id;
	private BufferedReader in;
	private PrintWriter out;
	
	// Initialize the ChatThread.
	public ChatThread(Socket sock, int ident)
	{
		connection = sock;
		name = "User " + ident;
		id = ident;
		try
		{
			in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
			out = new PrintWriter(new OutputStreamWriter(connection.getOutputStream()));
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
	
	// Returns the running ID number.
	public int getID()
	{
		return id;
	}
	
	// Sends a message to the chat server, so it can be displayed to everyone.
	private void sendMessage(String msg)
	{
		if(out != null)
		{
			out.println(msg);
			out.flush();
		}
	}
	
	// Broadcasts a message sent by a user.
	private void broadcastMessage(String msg)
	{
		Iterator i = ChatServer.active_clients.iterator();
		while(i.hasNext())
		{
			ChatThread next = (ChatThread) i.next();
			if(next != this)
				next.sendMessage(name + ": " + msg);
		}
	}

	// Broadcasts an info message (user leaves, user enters, etc.).
	private void broadcastInfoMessage(String msg)
	{
		Iterator i = ChatServer.active_clients.iterator();
		while(i.hasNext())
		{
			ChatThread next = (ChatThread) i.next();
			if(next != this)
				next.sendMessage(msg);
		}
	}
	
	// Prints the welcome message.
	private void printWelcome()
	{
		sendMessage("Welcome to ChatServer v. 1.0!");
		sendMessage("Your current user name is set to " + name + ". " + "Please type NAME followed by your desired name to change it.");
		sendMessage("Type BYE to exit.");
	}
	
	// Runs the thread.
	public void run()
	{
		if(in != null && out != null)
		{
			try
			{
				// Print a welcome message and let everyone else know that you're here.
				System.out.println(name + " has connected.");	// Output on the server who joined.
				printWelcome();
				broadcastInfoMessage(">>> " + name + " has entered.");
				
				// Loop until user types BYE.
				while(true)
				{
					// Read the line.
					String msg = in.readLine();
					
					// Quit if he typed BYE.
					if(msg.trim().equals("BYE"))
						break;
					
					// Check for a name change.
					String[] newname = msg.split(" ");
					if(newname.length > 1)
					{
						if(newname[0].trim().equals("NAME"))
						{
							String oldname = name;
							name = newname[1];
							System.out.println(oldname + " is now known as " + name + ".");
							sendMessage("*** You are now known as " + name);
							broadcastInfoMessage("*** " + oldname + " is now known as " + name + ".");
							continue;
						}
					}
					
					// Iterate through the active clients and send the message.
					broadcastMessage(msg);
				}
				
				// Close the connection and print a nice quit message.
				System.out.println(name + " has disconnected.");
				sendMessage("Goodbye!");
				broadcastInfoMessage("<<< " + name + " has left.");
				connection.close();
				ChatServer.active_clients.remove(this);
			}
			catch(Exception e)
			{
				e.printStackTrace();
				System.out.println(e.getMessage());
			}
		}
	}
}

// Server class.  Listens for connections and spawns new threads for each user.
public class ChatServer
{
	// Active clients.
	public static Set active_clients = new HashSet();
	
	// Main method.
	public static void main(String[] args)
	{
		// Current id number to use.
		int curr_id = 0;
		
		try
		{
			// The server socket.
			ServerSocket sock = new ServerSocket(8042);
			
			// Listen for connections.
			while(true)
			{
				Socket connection = sock.accept();
				ChatThread client = new ChatThread(connection, curr_id++);
				active_clients.add(client);
				client.start();
			}
		}
		catch(Exception e)
		{
			e.printStackTrace();
			System.out.println(e.getMessage());
		}
	}
}

