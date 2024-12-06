from __future__ import annotations

import pytest
from markdown import markdown

from mdx_gitlab_links import GitlabLinks

params = [
    pytest.param(
        "Merge Request !123.",
        '<p>Merge Request <a class="gl-link gl-mr" '
        'href="https://gitlab.com/foo/bar/gitlab-links/-/merge_requests/123" '
        'title="GitLab Merge Request foo/bar/gitlab-links!123">!123</a>.</p>',
        {},
        id="mr",
    ),
    pytest.param(
        "Merge Request project!123.",
        '<p>Merge Request <a class="gl-link gl-mr" '
        'href="https://gitlab.com/foo/bar/project/-/merge_requests/123" '
        'title="GitLab Merge Request foo/bar/project!123">project!123</a>.</p>',
        {},
        id="mr-same-namespace",
    ),
    pytest.param(
        "Merge Request grp/sub/project!123.",
        '<p>Merge Request <a class="gl-link gl-mr" '
        'href="https://gitlab.com/grp/sub/project/-/merge_requests/123" '
        'title="GitLab Merge Request grp/sub/project!123">grp/sub/project!123</a>.</p>',
        {},
        id="mr-cross-projet",
    ),
    pytest.param(
        "Merge Request !foo.",
        "<p>Merge Request !foo.</p>",
        {},
        id="not-mr",
    ),
    pytest.param(
        "Merge Request project!foo.",
        "<p>Merge Request project!foo.</p>",
        {},
        id="not-mr-same-namespace",
    ),
    pytest.param(
        "Merge Request grp/sub/project!foo.",
        "<p>Merge Request grp/sub/project!foo.</p>",
        {},
        id="not-mr-cross-project",
    ),
    pytest.param(
        "Merge Request \\!123.",
        "<p>Merge Request !123.</p>",
        {},
        id="mr-escaped",
    ),
    pytest.param(
        "Merge Request project\\!123.",
        "<p>Merge Request project!123.</p>",
        {},
        id="mr-same-namespace-escaped",
    ),
    pytest.param(
        "Merge Request grp/sub/project\\!123.",
        "<p>Merge Request grp/sub/project!123.</p>",
        {},
        id="mr-cross-project-escaped",
    ),
]


@pytest.mark.parametrize(("source", "expected", "config_kwargs"), params)
def test_merge_request(
    source: str,
    expected: str,
    config_kwargs: dict[str, str],
) -> None:
    configs = {"group": "foo/bar", "project": "gitlab-links"}
    configs.update(config_kwargs)
    output = markdown(source, extensions=[GitlabLinks(**configs)])
    assert output == expected
