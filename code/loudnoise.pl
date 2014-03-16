# This script will use ssh to play a sound on a specified computer in
# order to notify you that someone wants you. A certain keyword needs
# to be set to trigger the sound.

# If the specified machine is remote, then ssh will be used in order
# to play a sound on that machine (in order to work, you have to have
# ssh-agent running and have your keys setup properly so as to avoid
# the need to enter a password). If the machine is 'localhost', then
# ssh is not used, instead just invoking $noise_cmd locally.

#####################
##PRELIMINARY STUFF##
#####################

use strict;
use Irssi;
use vars qw($VERSION %IRSSI);

$VERSION = "0.1.0";
%IRSSI = (
	  authors 	=> "Michael V. De Palatis",
	  contact	=> "mvd at gatech dot edu",
	  name		=> "loudnoise",
	  description	=> "Plays a loud noise on a specified machine " .
	  "when a particular keyword is said by " .
	  "someone.",
	  license	=> "GPLv2",
	  written	=> "3 Aug 2006",
	  changed	=> "N/A"
);

###############
##SUBROUTINES##
###############

# Examines each incoming message for the keyword.
sub checkMessage
{
    my ($server, $data, $nick, $address) = @_;
    my $keywords = Irssi::settings_get_str("noise_keywords");
    my @keywordlist = split(/\s/, $keywords);

    # Match keywords.
    for ( @keywordlist )
    {
	if ( $data =~ m/$_/i )
	{
	    playSound();
	    return;
	}
    }

    # Also match nick.
    $nick = $server->{nick};
    if ( $data =~ m/$nick/i )
    {
	playSound();
    }
}

# Plays a sound on the specified machine.
sub playSound
{
    # Get current settings.
    my $use_ssh;
    my $machine = Irssi::settings_get_str("noise_machine");
    my $cmd = Irssi::settings_get_str("noise_cmd");
    my $file = Irssi::settings_get_str("noise_file");

    # Check if we are using ssh to run the command or not.
    if ( $machine eq "localhost" )
    {
	Irssi::print "Playing sound locally...";
	$use_ssh = 0;
    }
    else
    {
	Irssi::print "Playing sound remotely with ssh...";
	$use_ssh = 1;
    }

    # Play the sound.
    if ( $use_ssh )
    {
	system "ssh $machine $cmd $file 1>/dev/null 2>&1";
    }
    else
    {
	system "$cmd $file 1>/dev/null 2>&1 &";
    }
}

##################
##IRSSI SETTINGS##
##################

# Remote machine's address.
# If this is set to localhost, ssh will *not* be used.
Irssi::settings_add_str("misc", "noise_machine", undef);

# Command to use to play sound on remote machine.
Irssi::settings_add_str("misc", "noise_cmd", "mplayer");

# Sound file on remote machine.
Irssi::settings_add_str("misc", "noise_file", undef);

# The keyword that will trigger the noise.
# In the future, multiple keywords can be used to trigger a noise.
Irssi::settings_add_str("misc", "noise_keywords", "loudnoise");

# Plays the sound.
# This is for testing purposes only and will be removed in the future.
Irssi::command_bind("loudnoise", \&playSound);

# Add the signal.
Irssi::signal_add("event privmsg", \&checkMessage);
