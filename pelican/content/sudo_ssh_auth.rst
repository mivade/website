:title: ssh-agent for sudo authentication with a passwordless account
:date: 2014-12-07 15:25
:tags: debian, ssh, sudo, linux

For best security on a public system, it is generally best to disable
password-based logins with ssh and instead require authorized
keys. However, this complicates things if you want to use ``sudo``
with a regular user account, since by default it uses the standard
system password to verify the user is authorized to run commands as
root.

Enter `pam_ssh_agent_auth`_. This module allows using regular ssh keys
and ``ssh-agent`` to verify the user has the proper authorization to
use ``sudo``.

.. _pam_ssh_agent_auth: http://pamsshagentauth.sourceforge.net/

Prerequisites
-------------

You'll want to start by ensuring you have generated ssh keys for your
user and are using ``ssh-agent``. To generate the keys:

.. code-block:: shell-session

   $ ssh-keygen

Then just accept the defaults, but make sure to set a password for
your new key pair. Add the public key to
``$HOME/.ssh/authorized_keys``.

Installation
------------

Since the PAM module isn't in Debian, first grab the build
dependencies:

.. code-block:: shell-session

   # apt-get install build-essential checkinstall libssl-dev libpam0g-dev

.. note:: I had never heard about ``checkinstall`` until reading the
	  references to figure out how to do this. Although I rarely
	  have the need to install things from source, it seems like a
	  very nice utility!

Next, grab the source and build:

.. code-block:: shell-session

   # wget http://downloads.sourceforge.net/project/pamsshagentauth/pam_ssh_agent_auth/v0.10.2/pam_ssh_agent_auth-0.10.2.tar.bz2
   # tar -xvjf pam_ssh_agent_auth-0.10.2.tar.bz2
   # cd pam_ssh_agent_auth-0.10.2
   # ./configure --libexecdir=/lib/security --with-mantype=man
   # make
   # checkinstall

.. note:: The ``libexecdir`` option to the ``configure`` script is set
	  since apparently Debian keeps PAM modules in a different
	  place than ``pam_ssh_agent_auth`` expects by default.

.. warning:: The preceding commands are run as root simply because as
	     I was setting this up, the regular user had no password
	     set and so could not use ``sudo``. You may wish to only
	     install as root!

Configuration
-------------

Edit the file ``/etc/pam.d/sudo`` and add the following line *before*
any other ``auth`` or ``@include`` commands:

.. code-block:: cfg

   auth sufficient pam_ssh_agent_auth.so file=~/.ssh/authorized_keys

Run ``visudo`` to edit ``/etc/sudoers`` and add this line before any
other ``Defaults`` lines:

.. code-block:: cfg

   Defaults env_keep += SSH_AUTH_SOCK

Invoking ``sudo``
-----------------

To actually be able to use ``sudo`` now, run ``ssh-agent`` like so:

.. code-block:: shell-session

  $ eval `ssh-agent`

and add the key:

.. code-block:: shell-session

  $ ssh-add -t 600

This will set the keys to timeout in 10 minutes (600 seconds).

TODO
----

A more elegant way of adding keys and running ``ssh-agent``, including
checking to see if a process is already running!

References
----------

#. `How to allow authentication with sudo using an alternate password?`__
#. `Using SSH agent for sudo authentication`__
#. `Using ssh-agent with ssh`__

__ http://unix.stackexchange.com/a/158452
__ http://www.evans.io/posts/ssh-agent-for-sudo-authentication/
__ http://mah.everybody.org/docs/ssh
