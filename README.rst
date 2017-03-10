django-admin-testutils
======================

django-admin-testutils contains helpers to make writing selenium unit tests
for the Django admin easier. It is based on the code that supported selenium
unit tests in `django-nested-admin`_.

The test runner is designed to work similarly to the Django framework’s own
runtests.py. Until this project has had documentation written for it, the
best guide on usage can be found in the unit tests for this repository.
Specifically, look at `runtests.py`_ and `django_admin_testutils/tests/test.py`_.

.. _django-nested-admin: https://github.com/theatlantic/django-nested-admin
.. _runtests.py: https://github.com/theatlantic/django-admin-testutils/blob/master/runtests.py
.. _django_admin_testutils/tests/test.py: https://github.com/theatlantic/django-admin-testutils/blob/master/django_admin_testutils/tests/test.py
