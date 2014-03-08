Bash Cheat Sheet
================

This file contains a list of useful tips when using the [Bash][]
shell.

[Bash]: http://en.wikipedia.org/wiki/Bash_(Unix_shell)

* Redirection
    * ``STDERR`` redirected to ``STDOUT``: ``<command> 2>&1``
        * Example: Output make commands both to the terminal and to a
		  log file using ``tee``. ``make 2>&1 | tee make.log``
