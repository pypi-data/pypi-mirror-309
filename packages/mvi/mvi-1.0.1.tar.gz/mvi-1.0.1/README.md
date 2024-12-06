# mvi
Move files by text edit

Organising large amounts of files via the command line is cumbersome. The
standard UNIX `mv` command can rename a file or directory, or move items in
bulk, but the two operations cannot be combined. Furthermore, editing
capabilities on the command line offered by most shells are too limited to
comfortably alter long file or directory names, or add characters from foreign
character sets. Names containing spaces or other special characters should be
quoted or escaped, adding yet another layer of annoyance.

Larry Wall's `rename` complements `mv` with the ability to rename in bulk, but
being based on regular expressions it is suited mostly for file sets that share
a common naming structure. It also requires fluidity in Perl's regular
expression syntax to be useful, which sets a very high bar for entry.

Mvi (which can be seen to be either a contraction of "mv vi" or a more general
abbreviation of "move interactively") aims to simplify bulk renames of files
and directories by opening the directory listing in a text editor, thus
providing a powerful interface for editing destination paths. Names can be
changed by editing the lines in place while preserving order. Upon save and
exit mvi will show a list of scheduled rename operations and ask for
confirmation before performing the changes on disk.

## examples

The equivalence of `mv bar baz` in mvi involves an edit of the first line "bar"
into "baz" (not shown, but listed by mvi in summary):

    $ ls
    bar foo

    $ mvi
    line 1: bar -> baz
    proceed yes/no? y
    renamed bar to baz
    nothing left to rename.

    $ ls
    baz foo

Swapping lines results in swapping files:

    $ ls
    bar foo

    $ mvi
    line 1: bar -> foo
    line 2: foo -> bar
    proceed yes/no? y
    cycle detected: foo bar
    renamed foo to bar_
    renamed bar to foo
    renamed bar_ to bar
    nothing left to rename.

    $ ls
    bar foo

Items can be organized in subdirectories by simply editing a (relative or
absolute) destination path including directory separators.

    $ ls
    bar foo

    $ mvi
    line 1: bar -> sub/bar
    line 2: foo -> sub/foo
    proceed yes/no? y
    renamed bar to sub/bar
    renamed foo to sub/foo
    nothing left to rename.

    $ ls
    sub/

## installation

Mvi is available on [pypi](https://pypi.org/project/mvi/) for installation via
pip:

    $ pip3 install mvi

Note that in externally managed environments (i.e. having Python packages
installed via apt or similar) you may need to add `--break-system-packages` to
step over pip's guard rails.
