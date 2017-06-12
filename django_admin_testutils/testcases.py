from __future__ import absolute_import

import contextlib
import functools
import re
from unittest import expectedFailure, SkipTest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Model
try:
    # Django 1.10
    from django.urls import reverse
except ImportError:
    # Django <= 1.9
    from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils import six
from django.utils.six.moves.urllib.parse import urlparse

from .selenium import SeleniumTestCaseBase, SeleniumTestCase


class AdminSeleniumTestCaseBase(SeleniumTestCaseBase):

    def __new__(cls, name, bases, attrs):
        new_cls = super(AdminSeleniumTestCaseBase, cls).__new__(cls, name, bases, attrs)
        root_urlconf = getattr(new_cls, 'root_urlconf', 'django_admin_testutils.urls')
        return override_settings(ROOT_URLCONF=root_urlconf)(new_cls)


class SeleniumLiveServerTestCaseMixin(object):
    maxDiff = None
    longMessage = True
    page_load_timeout = 10
    default_timeout = 10

    def _post_teardown(self):
        # Close any popup windows that might have stuck around (for instance,
        # if an assertion failed or an exception occurred while a popup was
        # open)
        try:
            popup_window = self.selenium.window_handles[1]
        except:
            pass
        else:
            self.selenium.switch_to.window(popup_window)
            self.selenium.close()
            self.selenium.switch_to.window(self.selenium.window_handles[0])
        super(SeleniumLiveServerTestCaseMixin, self)._post_teardown()

    def wait_for(self, css_selector, timeout=None):
        """
        Helper function that blocks until a CSS selector is found on the page.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as ec

        if timeout is None:
            timeout = self.default_timeout

        self.wait_until(
            ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)),
            timeout)

    def wait_until(self, callback, timeout=None, message=None):
        """
        Helper function that blocks the execution of the tests until the
        specified callback returns a value that is not falsy. This function can
        be called, for example, after clicking a link or submitting a form.
        See the other public methods that call this function for more details.
        """
        from selenium.webdriver.support.wait import WebDriverWait

        if timeout is None:
            timeout = self.default_timeout

        WebDriverWait(self.selenium, timeout).until(callback, message)

    def wait_page_loaded(self):
        """
        Block until page has started to load.
        """
        # Wait for the next page to be loaded
        self.wait_for('body')

    def wait_until_visible_selector(self, selector, timeout=None):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as ec

        self.wait_until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector)),
            timeout=timeout,
            message="Timeout waiting for visible element at selector='%s'" % selector)

    def wait_until_clickable_xpath(self, xpath, timeout=None):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as ec

        if timeout is None:
            timeout = self.default_timeout

        self.wait_until(
            ec.element_to_be_clickable((By.XPATH, xpath)), timeout=timeout,
            message="Timeout waiting for clickable element at xpath='%s'" % xpath)

    def wait_until_clickable_selector(self, selector, timeout=None):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as ec

        self.wait_until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, selector)),
            timeout=timeout,
            message="Timeout waiting for clickable element at selector='%s'" % selector)

    def wait_until_available_selector(self, selector, timeout=None):
        self.wait_until(
            lambda driver: driver.find_element_by_css_selector(selector),
            timeout=timeout,
            message="Timeout waiting for available element at selector='%s'" % selector)

    def wait_until_available_xpath(self, xpath, timeout=None):
        self.wait_until(
            lambda driver: driver.find_element_by_xpath(xpath),
            timeout=timeout,
            message="Timeout waiting for available element at xpath='%s'" % xpath)

    @contextlib.contextmanager
    def visible_selector(self, selector, timeout=None):
        self.wait_until_visible_selector(selector, timeout)
        yield self.selenium.find_element_by_css_selector(selector)

    @contextlib.contextmanager
    def clickable_selector(self, selector, timeout=None):
        self.wait_until_clickable_selector(selector, timeout)
        yield self.selenium.find_element_by_css_selector(selector)

    @contextlib.contextmanager
    def clickable_xpath(self, xpath, timeout=10):
        self.wait_until_clickable_xpath(xpath, timeout)
        yield self.selenium.find_element_by_xpath(xpath)

    @contextlib.contextmanager
    def available_selector(self, selector, timeout=10):
        self.wait_until_available_selector(selector, timeout)
        yield self.selenium.find_element_by_css_selector(selector)

    @contextlib.contextmanager
    def available_xpath(self, xpath, timeout=10):
        self.wait_until_available_xpath(xpath, timeout)
        yield self.selenium.find_element_by_xpath(xpath)

    @contextlib.contextmanager
    def switch_to_popup_window(self):
        self.wait_until(lambda d: len(d.window_handles) == 2)
        self.selenium.switch_to.window(self.selenium.window_handles[1])
        yield
        try:
            self.wait_until(lambda d: len(d.window_handles) == 1)
        except:
            self.close()
            raise
        finally:
            self.selenium.switch_to.window(self.selenium.window_handles[0])


class SeleniumLiveServerTestCase(
        SeleniumLiveServerTestCaseMixin, SeleniumTestCase):
    pass


class AdminSeleniumTestCase(six.with_metaclass(
        AdminSeleniumTestCaseBase, SeleniumLiveServerTestCaseMixin,
        SeleniumTestCase, StaticLiveServerTestCase)):

    window_size = (1120, 1300)
    page_load_timeout = 10
    default_timeout = 10
    admin_site_name = 'admin'

    @property
    def has_grappelli(self):
        return 'grappelli' in settings.INSTALLED_APPS

    @property
    def has_suit(self):
        return 'suit' in settings.INSTALLED_APPS

    @property
    def available_apps(self):
        apps = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django_admin_testutils',
        ]
        if self.has_grappelli:
            apps.insert(0, 'grappelli')

        current_app = type(self).__module__.rpartition('.')[0]

        parent_app = re.split(r'\.tests(?:\.|$)', current_app)[0]
        if parent_app != current_app:
            apps.append(parent_app)

        apps.append(current_app)

    @classmethod
    def setUpClass(cls):
        super(AdminSeleniumTestCase, cls).setUpClass()
        __import__(settings.ROOT_URLCONF)

    def setUp(self):
        super(AdminSeleniumTestCase, self).setUp()
        self.set_window_size()
        self.selenium.set_page_load_timeout(self.page_load_timeout)
        get_user_model().objects.create_superuser(
            username='super', password='secret', email='super@example.com')
        self.admin_login("super", "secret")

    def set_window_size(self):
        self.selenium.set_window_size(*self.window_size)

    def initialize_page(self):
        self.set_window_size()
        self.selenium.set_page_load_timeout(self.page_load_timeout)
        try:
            self.selenium.execute_script("window.$ = django.jQuery")
        except:
            pass
        else:
            self.make_header_footer_position_static()

    invalid_re = re.compile(r'(?<=INVALID {{ )((?:.(?!}}))*?) }}')

    def wait_page_loaded(self):
        """
        Block until page has started to load.
        """
        from selenium.common.exceptions import TimeoutException
        try:
            # Wait for the next page to be loaded
            super(AdminSeleniumTestCase, self).wait_page_loaded()
        except TimeoutException:
            # IE7 occasionally returns an error "Internet Explorer cannot
            # display the webpage" and doesn't load the next page. We just
            # ignore it.
            pass
        else:
            invalid_matches = self.invalid_re.findall(self.selenium.page_source)
            self.assertEqual(invalid_matches, [])

    def admin_login(self, username, password):
        """
        Helper function to log into the admin.
        """
        self.client.login(username=username, password=password)
        self.selenium.get("%s%s" %
            (self.live_server_url, '/static/admin_testutils/blank.html'))
        self.wait_page_loaded()
        domain = urlparse(self.live_server_url).netloc.split(':')[0]
        cookie_dict = {'path': '/', 'domain': domain}
        for k, v in self.client.cookies.items():
            cookie = dict(cookie_dict, name=k, value=v.value)
            self.selenium.add_cookie(cookie)

    def load_admin(self, obj=None):
        if isinstance(obj, type) and issubclass(obj, Model):
            opts = obj._meta
            pk = None
        elif isinstance(obj, Model):
            opts = type(obj)._meta
            pk = obj.pk

        info = (opts.app_label, opts.object_name.lower())
        if pk:
            url = reverse(
                'admin:%s_%s_change' % info, args=[pk],
                current_app=self.admin_site_name)
        else:
            url = reverse('admin:%s_%s_add' % info, current_app=self.admin_site_name)
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.wait_page_loaded()
        self.initialize_page()

    def save_form(self):
        has_continue = bool(
            self.selenium.execute_script(
                'return django.jQuery("[name=_continue]").length'))
        name_attr = "_continue" if has_continue else "_save"
        self.selenium.find_element_by_xpath('//*[@name="%s"]' % name_attr).click()
        if has_continue:
            self.wait_page_loaded()
            self.initialize_page()

    def make_header_footer_position_static(self):
        """
        Make grappelli header and footer element styles 'position: static

        Without this the header and footer can cover other elements, making
        them unclickable by selenium.
        '"""
        if not self.has_grappelli:
            return
        self.selenium.execute_script(
            "(function($) {"
            "$('footer').attr('class', 'grp-module grp-submit-row');"
            "$('#content-inner').css('bottom', '0');"
            "$('#grp-header').css('position', 'static');"
            "$('#grp-content').css('top', '0');"
            "})(django.jQuery);")


def expected_failure_if_grappelli(f):
    return expectedFailure(f) if 'grappelli' in settings.INSTALLED_APPS else f


def expected_failure_if_suit(f):
    return expectedFailure(f) if 'suit' in settings.INSTALLED_APPS else f


def skip_if_not_grappelli(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'grappelli' not in settings.INSTALLED_APPS:
            raise SkipTest("Skipping (grappelli required)")
        return func(*args, **kwargs)
    return wrapper
