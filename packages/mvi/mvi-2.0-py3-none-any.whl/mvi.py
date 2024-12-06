'''Move Interactively'''

import os
import sys
import tempfile

__version__ = '2.0'


def display_and_verify(sources, destinations):
    '''Print and verify rename operations.

    Given a list of source paths and a list of destination paths, print an
    overview of the rename operations and verify that the input is valid. If
    the input is not valid, for instance because the lists are of different
    length or a destination exists, raise a ValueError with an appropriate
    message detailing the issue.'''

    for i, (source, destination) in enumerate(zip(sources, destinations), start=1):
        if source != destination:
            print(f'Line {i}: {source} -> {destination}')

    if len(destinations) < len(sources):
        for i, source in enumerate(sources[len(destinations):], start=1+len(destinations)):
            print(f'Line {i}: {source} -> ?')
        raise ValueError('list of destination names is too short')

    if len(destinations) > len(sources):
        for i, destination in enumerate(destinations[len(sources):], start=1+len(sources)):
            print(f'Line {i}: ? -> {destination}')
        raise ValueError('list of destination names is too long')

    if not all(destinations):
        raise ValueError('filenames must be at least one character long')

    seen = {}
    for source, destination in zip(sources, destinations):
        if destination in seen:
            raise ValueError(f'both {seen[destination]} and {source} want to move to {destination}')
        seen[destination] = source

    renames = {source: destination for source, destination in zip(sources, destinations) if source != destination}
    for destination in renames.values():
        if destination not in renames and os.path.exists(destination):
            raise ValueError(f'destination exists: {destination}')


def move(source, destination):
    '''Rename file if destination is free and print feedback.

    Aims to avoid that files get overwritten by raising a FileExistsError
    if the destination path is occupied. Note that some platforms such as
    Windows refuse to rename to an existing path, but others such as Linux
    don't, so we add a check for caution and for consistency.'''

    if os.path.exists(destination):
        raise FileExistsError(destination)
    os.renames(source, destination)
    print(f'Moved {source} -> {destination}')


def move_all(sources, destinations):
    '''Perform all renames from the rename dictionary.

    Items are popped off the dictionary in place after every succesful rename
    operation, to allow remaining items to be recovered on error.'''

    assert len(sources) == len(destinations) and isinstance(sources, list)

    queue = list(range(len(sources)))
    cycle = None
    for i in queue:
        source = sources[i]
        destination = destinations[i]
        if source == destination:
            pass
        elif destination not in sources:
            move(source, destination)
            sources[i] = destination
            cycle = None
        else: # destination position is occupied
            queue.append(i) # try again later
            if cycle == i: # we already cycled back to this index without making any move
                while sources[i] in destinations:
                    sources[i] += '_'
                move(source, sources[i]) # break cycle by moving to temporary location
            elif cycle is None: # not presently waiting for another index to reappear
                cycle = i # start tracking

    assert sources == destinations


# INTERACTVE ZONE


def choose(*options):
    '''Print a selection dialog and return the choice.'''

    while True:
        s = input(f'Proceed: {"/".join(options)} ')
        choices = [option for option in options if option.startswith(s)]
        if len(choices) == 1:
            return choices[0]


def choose_or_abort(*options):
    '''Print a selection dialog including 'abort' and return the choice.

    Raise a KeyboardInterrupt if abort is chosen. This allows for the same code
    path to handle a menu abort and a Ctrl+C (Linux) or Ctrl+Z (Windows) input.'''

    assert 'abort' not in options
    choice = choose(*options, 'abort')
    if choice == 'abort':
        raise KeyboardInterrupt
    return choice


def main():
    '''Create rename file and commit changes.

    The rename file is opened in the system temp directory and maintained until
    the last change is committed. The sources list with the corresponding
    original paths is edited in place after every successful move.'''

    if len(sys.argv) != 1:
        sys.exit(f'mvi does not take any arguments')

    editor = os.environ.get('EDITOR', 'vim')

    sources = sorted(os.listdir())

    fd, tmp = tempfile.mkstemp(prefix='mvi')
    try:

        with os.fdopen(fd, 'w') as f:
            for source in sources:
                print(source, file=f)

        while True:

            try:

                if os.system(f'{editor} {tmp}') != 0:
                    print('Warning: editor returned with non-zero status')
                with open(tmp, 'r') as f:
                    destinations = f.read().splitlines()
                if destinations == sources:
                    print('Nothing to move.')
                else:
                    display_and_verify(sources, destinations)
                    if choose_or_abort('continue', 'edit') == 'edit':
                        continue
                    move_all(sources, destinations)
                    print('Done.')
                break

            except Exception as e:
                print('Error:', e)

            choose_or_abort('edit')

    except KeyboardInterrupt:
        print('Aborted.')
    except Exception as e:
        print('Fatal error:', e)
    finally:
        os.remove(tmp)
