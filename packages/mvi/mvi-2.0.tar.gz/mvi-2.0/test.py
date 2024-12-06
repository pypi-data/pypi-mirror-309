import unittest, tempfile, os, contextlib, io
import mvi


class TestCase(unittest.TestCase):

    def setUp(self):
        ctx = tempfile.TemporaryDirectory()
        path = ctx.__enter__()
        self.addCleanup(ctx.__exit__, None, None, None)
        oldwd = os.getcwd()
        os.chdir(path)
        self.addCleanup(os.chdir, oldwd)

    def assertFileEquals(self, path, contents):
        with open(path) as f:
            self.assertEqual(f.read(), contents)

    @contextlib.contextmanager
    def assertStdout(self, output):
        with contextlib.redirect_stdout(io.StringIO()) as f:
            yield
        self.assertEqual(f.getvalue(), output)


class display_and_verify(TestCase):

    def test(self):
        sources = ['a', 'b', 'c']
        destinations = ['a', 'newb', 'c']
        with self.assertStdout('Line 2: b -> newb\n'):
            mvi.display_and_verify(sources, destinations)

    def test_too_short(self):
        sources = ['a', 'b', 'c']
        destinations = ['a', 'newb']
        with (self.assertStdout('Line 2: b -> newb\nLine 3: c -> ?\n'),
              self.assertRaisesRegex(ValueError, 'list of destination names is too short')):
            mvi.display_and_verify(sources, destinations)

    def test_too_long(self):
        sources = ['a', 'b', 'c']
        destinations = ['a', 'newb', 'c', 'd']
        with (self.assertStdout('Line 2: b -> newb\nLine 4: ? -> d\n'),
              self.assertRaisesRegex(ValueError, 'list of destination names is too long')):
            mvi.display_and_verify(sources, destinations)

    def test_empty(self):
        sources = ['a', 'b', 'c']
        destinations = ['a', 'newb', '']
        with (self.assertStdout('Line 2: b -> newb\nLine 3: c -> \n'),
              self.assertRaisesRegex(ValueError, 'filenames must be at least one character long')):
            mvi.display_and_verify(sources, destinations)

    def test_collision(self):
        sources = ['a', 'b', 'c']
        destinations = ['x', 'b', 'x']
        with (self.assertStdout('Line 1: a -> x\nLine 3: c -> x\n'),
              self.assertRaisesRegex(ValueError, 'both a and c want to move to x')):
            mvi.display_and_verify(sources, destinations)

    def test_cycle(self):
        sources = ['a', 'b', 'c']
        destinations = ['b', 'c', 'a']
        with self.assertStdout('Line 1: a -> b\nLine 2: b -> c\nLine 3: c -> a\n'):
            mvi.display_and_verify(sources, destinations)

    def test_exists(self):
        with open('newb', 'w') as f:
            f.write('foo')
        sources = ['a', 'b', 'c']
        destinations = ['a', 'newb', 'c']
        with (self.assertStdout('Line 2: b -> newb\n'),
              self.assertRaisesRegex(ValueError, 'destination exists: newb')):
            mvi.display_and_verify(sources, destinations)

    def test_not_exists(self):
        with open('b', 'w') as f:
            f.write('foo')
        with open('c', 'w') as f:
            f.write('bar')
        sources = ['a', 'b', 'c']
        destinations = ['b', 'c', 'newc']
        with self.assertStdout('Line 1: a -> b\nLine 2: b -> c\nLine 3: c -> newc\n'):
            mvi.display_and_verify(sources, destinations)


class move(TestCase):

    def test_move_file(self):
        with open('a', 'w') as f:
            f.write('foo')
        mvi.move('a', 'b')
        self.assertEqual(os.listdir(), ['b'])
        self.assertFileEquals('b', 'foo')

    def test_move_to_dir(self):
        with open('a', 'w') as f:
            f.write('foo')
        mvi.move('a', 'dir/a')
        self.assertFileEquals('dir/a', 'foo')

    def test_exists(self):
        with open('a', 'w') as f:
            f.write('foo')
        with open('b', 'w') as f:
            f.write('bar')
        with self.assertRaises(FileExistsError):
            mvi.move('a', 'b')


class move_all(TestCase):

    def test_move_files(self):
        with open('a', 'w') as f:
            f.write('foo')
        with open('b', 'w') as f:
            f.write('bar')
        sources = ['a', 'b']
        destinations = ['newa', 'newb']
        mvi.move_all(sources, destinations)
        self.assertEqual(sources, destinations)
        self.assertEqual(set(os.listdir()), {'newa', 'newb'})
        self.assertFileEquals('newa', 'foo')
        self.assertFileEquals('newb', 'bar')

    def test_move_to_dir(self):
        with open('a', 'w') as f:
            f.write('foo')
        with open('b', 'w') as f:
            f.write('bar')
        sources = ['a', 'b']
        destinations = ['dira/a', 'dirb/b']
        mvi.move_all(sources, destinations)
        self.assertEqual(sources, destinations)
        self.assertEqual(set(os.listdir()), {'dira', 'dirb'})
        self.assertFileEquals('dira/a', 'foo')
        self.assertFileEquals('dirb/b', 'bar')

    def test_exists(self):
        with open('a', 'w') as f:
            f.write('foo')
        with open('b', 'w') as f:
            f.write('bar')
        sources = ['a']
        destinations = ['b']
        with self.assertRaises(FileExistsError):
            mvi.move_all(sources, destinations)

    def test_swap(self):
        with open('a', 'w') as f:
            f.write('foo')
        with open('b', 'w') as f:
            f.write('bar')
        with open('c', 'w') as f:
            f.write('baz')
        sources = ['a', 'b', 'c']
        destinations = ['b', 'c', 'a']
        mvi.move_all(sources, destinations)
        self.assertEqual(sources, destinations)
        self.assertEqual(set(os.listdir()), {'a', 'b', 'c'})
        self.assertFileEquals('a', 'baz')
        self.assertFileEquals('b', 'foo')
        self.assertFileEquals('c', 'bar')

    def test_swap_and_rename(self):
        with open('a', 'w') as f:
            f.write('foo')
        with open('b', 'w') as f:
            f.write('bar')
        with open('c', 'w') as f:
            f.write('baz')
        sources = ['a', 'b', 'c']
        destinations = ['c', 'newb', 'a']
        mvi.move_all(sources, destinations)
        self.assertEqual(sources, destinations)
        self.assertEqual(set(os.listdir()), {'a', 'newb', 'c'})
        self.assertFileEquals('a', 'baz')
        self.assertFileEquals('newb', 'bar')
        self.assertFileEquals('c', 'foo')
