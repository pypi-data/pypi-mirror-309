# mvi: move interactively

Organising files via the command line can be cumbersome, for many reasons.
Editing capabilities on the command line are limited. Characters from foreign
character sets cannot be inserted. Arguments may require quoting or escaping.
Names may be mistaken for flags.

Mvi aims to simplify bulk renames of files and directories by opening the
directory listing in a text editor, thus providing a powerful interface for
editing destination paths. Names are changed by editing lines in place. Upon
exit mvi will show a list of scheduled rename operations and ask for
confirmation before committing the changes to disk.

A lot of care is taken to make sure that mvi does not bail out halfway through
an operation. File targets are checked for availability before starting a
commit - mvi will never overwrite a file. In case of an unexpected IO error mvi
will return to the editor for manual resolution, from where it can pick up with
the remaining move operations.

## examples

The equivalence of `mv bar baz` in mvi involves an edit of the first line "bar"
into "baz" (not shown, but listed by mvi in summary):

    $ ls
    bar foo

    $ mvi
    Line 1: bar -> baz
    Proceed: continue/edit/abort c
    Moved bar -> baz
    Done.

    $ ls
    baz foo

Swapping lines results in swapping files:

    $ ls
    bar foo

    $ mvi
    Line 1: bar -> foo
    Line 2: foo -> bar
    Proceed: continue/edit/abort c
    Moved bar -> bar_
    Moved foo -> bar
    Moved bar_ -> foo
    Done.

    $ ls
    bar foo

Items can be organized in subdirectories by simply editing a (relative or
absolute) destination path including directory separators.

    $ ls
    bar foo

    $ mvi
    Line 1: bar -> sub/bar
    Line 2: foo -> sub/foo
    Proceed: continue/edit/abort c
    Moved bar -> sub/bar
    Moved foo -> sub/foo
    Done.

    $ ls
    sub/

## installation

Mvi is available on [pypi](https://pypi.org/project/mvi/) for installation via
pip:

    $ pip3 install mvi

Note that in externally managed environments (i.e. having Python packages
installed via apt or similar) you may need to add `--break-system-packages` to
step over pip's guard rails. Alternatively you can use
[pipx](https://pypa.github.io/pipx/) to install mvi in an isolated environment:

    $ pipx install mvi

## see also

The [rename](https://man7.org/linux/man-pages/man1/rename.1.html) command that
is available in most distributions allows for bulk move operations based on
regular expressions.
