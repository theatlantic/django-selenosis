================
django-selenosis
================

**selenosis** *noun* sel·e·no·sis /sɛliːˈnəʊsɪs/. **poisoning due to excessive intake of selenium.**

django-selenosis (formerly django-admin-testutils) contains helpers to make
writing selenium unit tests for Django, and in particular the Django admin,
easier. It is based on the code that supported selenium unit tests in
`django-nested-admin`_.

The test runner is designed to work similarly to the Django framework’s own
runtests.py. The best guide on usage can be found in the unit tests for this
repository. Specifically, look at `runtests.py`_ and `selenosis/tests/test.py`_.

Development and Testing
=======================

Install ``chromedriver``
------------------------

You can use homebrew or manually download ``chomedriver``:

1. homebrew::

    brew install --cask chromedriver

2. Manually::

    export PATH="$PWD:$PATH"
    export CHROMEDRIVER_VERSION=$(curl -q http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    curl -O http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_mac64.zip
    unzip chromedriver_mac64.zip
    rm chromedriver_mac64.zip
    chmod +x chromedriver

Run ``tox`` To Test
-------------------

Run all tests::

    tox -- --selenium=chrome-headless

Run only a specified test environment::

    tox -e py37-dj22 -- --selenium=chrome-headless

If you would like to observe the browser during a test run, simply remove ``-headless``
in the above examples.


.. _django-nested-admin: https://github.com/theatlantic/django-nested-admin
.. _runtests.py: https://github.com/theatlantic/django-selenosis/blob/master/runtests.py
.. _selenosis/tests/test.py: https://github.com/theatlantic/django-selenosis/blob/master/selenosis/tests/test.py
