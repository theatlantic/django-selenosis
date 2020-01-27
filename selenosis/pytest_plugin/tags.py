"""Adds support for the django.test @tag decorator to pytest"""


def pytest_addoption(parser):
    group = parser.getgroup("tags")
    group._addoption(
        "--tag",
        action="append",
        dest="tags",
        help="Run only tests with the specified tag. Can be used multiple times.")
    group._addoption(
        '--exclude-tag', action='append', dest='exclude_tags',
        help='Do not run tests with the specified tag. Can be used multiple times.')


def pytest_configure(config):
    config.addinivalue_line("markers", "tags: mark test to run iff it has tag")


def pytest_collection_modifyitems(items, config):
    tags = set(config.option.tags or [])
    exclude_tags = set(config.option.exclude_tags or [])

    if not tags and not exclude_tags:
        return

    remaining = []
    deselected = []
    for item in items:
        test_tags = set(getattr(item.obj, 'tags', set()))
        test_tags |= set(getattr(item.parent.obj, 'tags', set()))
        for tag_mark in item.iter_markers('tags'):
            test_tags |= set(tag_mark.args)
        matched_tags = tags & test_tags
        if (matched_tags or not tags) and not (test_tags & exclude_tags):
            remaining.append(item)
        else:
            deselected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining


def pytest_collection_finish(session):
    """
    Print how many tests were actually selected and are going to be run.
    :param session: this py.test session
    :return: None
    """
    line = "selected " + str(len(session.items)) + " items\n"
    tr = session.config.pluginmanager.getplugin('terminalreporter')
    if tr:  # terminal reporter is not available when running with xdist
        tr.rewrite(line, bold=True)


def pytest_report_header(config):
    tags = list(config.option.tags or [])
    exclude_tags = list(config.option.exclude_tags or [])

    if not tags and not exclude_tags:
        return

    header_parts = []
    if tags:
        header_parts.append("tags = %s" % ", ".join(tags))
    if exclude_tags:
        header_parts.append("exclude tags = %s" % ", ".join(exclude_tags))

    return "; ".join(header_parts)
