Linux Notes
===========

Git
---

To produce colored diff output in HTML form:

    git diff --color-words <commit> <commit> | aha

`aha` is a simple program (packaged in [Debian][]) for converting ANSI
terminal output to HTML.

[Debian]: http://www.debian.org/

Gnome 3
-------

A lot of people seem to greatly dislike [Gnome 3][]. At first, I fell
in that camp, but after getting a new laptop and doing a fresh Debian_
installation, I decided to play around with it a bit. Its default
configuration leaves something to be desired, but it doesn't take too
much tweaking (mostly involving installation of some extensions) to
become extremely nice. Here are some helpful notes.

* Disable built-in shortcuts such as C-` (annoying for us emacs users)

Use `dconf-editor` to edit window manager keybindings: Look under
`org->gnome->desktop->wm->keybindings` for the appropriate shortcut to
disable. [Source][dconf keys].

[Gnome 3]: http://www.gnome.org
[dconf keys]: http://askubuntu.com/questions/175369/how-do-i-disable-ctrl-alt-d-in-gnome-shell

