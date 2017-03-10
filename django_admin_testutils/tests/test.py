from django_admin_testutils import AdminSeleniumTestCase

from .models import Publisher, Book, Author


class TestUtilsTestCase(AdminSeleniumTestCase):

    def setUp(self):
        super(TestUtilsTestCase, self).setUp()
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
