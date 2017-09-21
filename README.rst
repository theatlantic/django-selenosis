django-selenosis
================

**selenosis**

    *noun* sel·e·no·sis /sɛliːˈnəʊsɪs/. **poisoning due to excessive
    intake of selenium.**

django-selenosis (formerly django-admin-testutils) contains helpers to make
writing selenium unit tests for Django, and in particular the Django admin,
easier. It is based on the code that supported selenium unit tests in
`django-nested-admin`_.

The test runner is designed to work similarly to the Django framework’s own
runtests.py. The best guide on usage can be found in the unit tests for this
repository. Specifically, look at `runtests.py`_ and `selenosis/tests/test.py`_.

.. _django-nested-admin: https://github.com/theatlantic/django-nested-admin
.. _runtests.py: https://github.com/theatlantic/django-selenosis/blob/master/runtests.py
.. _selenosis/tests/test.py: https://github.com/theatlantic/django-selenosis/blob/master/selenosis/tests/test.py
