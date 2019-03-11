import os.path
from os.path import abspath
import pickle
import sys
import unittest

import six

from selenosis import AdminSelenosisTestCase
from selenosis.runner import PatchedTestLoader

from .models import Publisher, Book, Author


class PatchedTestLoaderTestCase(unittest.TestCase):
    """
    Test backport of Python 3.4 fix for unittest picklability. Essentially
    taken wholesale from CPython Lib/unittest/test/test_discovery.py

    See https://bugs.python.org/issue22903
    """

    def setup_import_issue_package_tests(self, vfs):
        self.addCleanup(setattr, os, 'listdir', os.listdir)
        self.addCleanup(setattr, os.path, 'isfile', os.path.isfile)
        self.addCleanup(setattr, os.path, 'isdir', os.path.isdir)
        self.addCleanup(sys.path.__setitem__, slice(None), list(sys.path))

        def list_dir(path):
            return list(vfs[path])

        os.listdir = list_dir
        os.path.isdir = lambda path: not path.endswith('.py')
        os.path.isfile = lambda path: path.endswith('.py')

    def test_discover_with_init_modules_that_fail_to_import(self):
        if six.PY3:
            raise unittest.SkipTest("Patched loader only used for Python 2.x")

        self.setup_import_issue_package_tests({
            abspath('/foo'): ['my_package'],
            abspath('/foo/my_package'): ['__init__.py', 'test_module.py'],
        })

        def _get_module_from_name(name):
            raise ImportError("Cannot import %s" % name)

        loader = PatchedTestLoader()
        loader._get_module_from_name = _get_module_from_name
        suite = loader.discover(abspath('/foo'))

        test = list(list(suite)[0])[0]  # extract test from suite
        method_name = test._testMethodName
        with self.assertRaises(ImportError):
            getattr(test, method_name)()

        # Check picklability
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            pickle.loads(pickle.dumps(test, proto))


class TestSelenosisTestCase(AdminSelenosisTestCase):

    def setUp(self):
        super(TestSelenosisTestCase, self).setUp()
        self.author = Author.objects.create(name="Thomas Pynchon")
        self.against_the_day = Book.objects.create(
            position=0,
            name="Against the Day",
            author=self.author,
            publisher=Publisher.objects.create(name="Penguin Press"))
        self.mason_and_dixon = Book.objects.create(
            position=1,
            name="Mason & Dixon",
            author=self.author,
            publisher=Publisher.objects.create(
                name="Henry Holt and Company"))

    def test_admin_load(self):
        self.load_admin(self.author)

    def test_save_form(self):
        self.load_admin(self.author)
        with self.clickable_selector('#id_book_set-1-name') as el:
            el.clear()
            el.send_keys('Mason and Dixon')
        self.save_form()
        self.mason_and_dixon.refresh_from_db()
        self.assertEqual(self.mason_and_dixon.name, "Mason and Dixon")

    def test_clickable_selector(self):
        self.load_admin(self.author)
        delete_selector = '#id_book_set-1-DELETE'
        if self.has_grappelli:
            delete_selector += '+ a'
        with self.clickable_selector(delete_selector) as el:
            el.click()
        self.save_form()
        books = Book.objects.all()
        self.assertNotEqual(len(books), 2, "Book was not deleted")
        self.assertEqual(len(books), 1)

    def test_switch_to_popup(self):
        self.load_admin(self.author)
        with self.clickable_selector('#id_book_set-4-name') as el:
            el.send_keys('The Crying of Lot 49')
        self.selenium.find_element_by_css_selector('#add_id_book_set-4-publisher').click()
        with self.switch_to_popup_window():
            self.selenium.find_element_by_css_selector('#id_name').send_keys(
                'J. B. Lippincott & Co.')
            self.save_form()
        self.save_form()
        books = Book.objects.all()
        self.assertNotEqual(len(books), 2, "Book was not added")
        self.assertEqual(len(books), 3)
