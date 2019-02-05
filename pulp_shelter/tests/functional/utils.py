# coding=utf-8
"""Utilities for tests for the shelter plugin."""
from functools import partial
from unittest import SkipTest

from pulp_smash import api, selectors
from pulp_smash.pulp3.constants import (
    REPO_PATH
)
from pulp_smash.pulp3.utils import (
    gen_remote,
    gen_repo,
    gen_publisher,
    get_content,
    require_pulp_3,
    require_pulp_plugins,
    sync
)

from pulp_shelter.tests.functional.constants import (
    SHELTER_CONTENT_NAME,
    SHELTER_CONTENT_PATH,
    SHELTER_FIXTURE_URL,
    SHELTER_REMOTE_PATH,
)


def set_up_module():
    """Skip tests Pulp 3 isn't under test or if pulp_shelter isn't installed."""
    require_pulp_3(SkipTest)
    require_pulp_plugins({'pulp_shelter'}, SkipTest)


def gen_shelter_remote(**kwargs):
    """Return a semi-random dict for use in creating a shelter Remote.

    :param url: The URL of an external content source.
    """
    remote = gen_remote(SHELTER_FIXTURE_URL)
    # FIXME: Add any fields specific to a shelter remote here
    shelter_extra_fields = {
        **kwargs
    }
    remote.update(**shelter_extra_fields)
    return remote


def gen_shelter_publisher(**kwargs):
    """Return a semi-random dict for use in creating a Remote.

    :param url: The URL of an external content source.
    """
    publisher = gen_publisher()
    # FIXME: Add any fields specific to a plugin_teplate publisher here
    shelter_extra_fields = {
        **kwargs
    }
    publisher.update(**shelter_extra_fields)
    return publisher


def get_shelter_content_unit_paths(repo):
    """Return the relative path of content units present in a shelter repository.

    :param repo: A dict of information about the repository.
    :returns: A list with the paths of units present in a given repository.
    """
    # FIXME: The "relative_path" is actually a file path and name
    # It's just an example -- this needs to be replaced with an implementation that works
    # for repositories of this content type.
    return [
        content_unit['relative_path']
        for content_unit in get_content(repo)[SHELTER_CONTENT_NAME]
    ]


def gen_shelter_content_attrs(artifact):
    """Generate a dict with content unit attributes.

    :param: artifact: A dict of info about the artifact.
    :returns: A semi-random dict for use in creating a content unit.
    """
    # FIXME: Add content specific metadata here.
    return {'_artifact': artifact['_href']}


def populate_pulp(cfg, url=SHELTER_FIXTURE_URL):
    """Add shelter contents to Pulp.

    :param pulp_smash.config.PulpSmashConfig: Information about a Pulp application.
    :param url: The shelter repository URL. Defaults to
        :data:`pulp_smash.constants.SHELTER_FIXTURE_URL`
    :returns: A list of dicts, where each dict describes one file content in Pulp.
    """
    client = api.Client(cfg, api.json_handler)
    remote = {}
    repo = {}
    try:
        remote.update(client.post(SHELTER_REMOTE_PATH, gen_shelter_remote(url)))
        repo.update(client.post(REPO_PATH, gen_repo()))
        sync(cfg, remote, repo)
    finally:
        if remote:
            client.delete(remote['_href'])
        if repo:
            client.delete(repo['_href'])
    return client.get(SHELTER_CONTENT_PATH)['results']


skip_if = partial(selectors.skip_if, exc=SkipTest)
"""The ``@skip_if`` decorator, customized for unittest.

:func:`pulp_smash.selectors.skip_if` is test runner agnostic. This function is
identical, except that ``exc`` has been set to ``unittest.SkipTest``.
"""
