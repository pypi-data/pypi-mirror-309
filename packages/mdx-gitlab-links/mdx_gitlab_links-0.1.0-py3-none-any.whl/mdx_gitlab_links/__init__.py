from __future__ import annotations

from typing import TYPE_CHECKING, Any
from xml.etree.ElementTree import Element

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

if TYPE_CHECKING:
    import re

    from markdown import Markdown


RE_GROUP = r"[A-Za-z0-9_][A-Za-z0-9_.\-]*"
"""GitLab group name regex, as described on the 'Create group' page."""

RE_GROUP_SUBGROUP = rf"(?:{RE_GROUP}\/)?{RE_GROUP}"
"""Gitlab group & optional subgroup."""

RE_PROJECT = r"[A-Za-z0-9_][A-Za-z0-9_.\-]*"
"""GitLab poject name regex, as described on the 'Create project' page."""


def _build_link(label: str, title: str, href: str, classes: str) -> Element:
    el = Element("a")
    el.text = label
    el.set("title", title)
    el.set("href", href)
    el.set("class", classes)
    return el


# TODO: issue
# TODO: mention
# TODO: commit
# TODO: commit range


class MergeRequestPattern(Pattern):  # noqa: D101
    # TODO: mr title (#123+)
    # TODO: mr summary (#123+s)

    ANCESTOR_EXCLUDES = ("a",)

    def __init__(self, config: dict[str, Any], md: Markdown | None = None) -> None:
        pattern = rf"((?:({RE_GROUP_SUBGROUP})\/)?({RE_PROJECT})?!([0-9]+))"
        super().__init__(pattern, md)
        self.config = config

    def handleMatch(self, m: re.Match[str]) -> str | Element | None:
        domain = self.config["domain"]
        label = m.group(2)
        group = m.group(3) or self.config["group"]
        project = m.group(4) or self.config["project"]
        num = m.group(5)
        return _build_link(
            label=label,
            title=f"GitLab Merge Request {group}/{project}!{num}",
            href=f"{domain}/{group}/{project}/-/merge_requests/{num}",
            classes="gl-link gl-mr",
        )


class GitlabLinks(Extension):
    """Extension for parsing GitLab references.

    https://docs.gitlab.com/ee/user/markdown.html#gitlab-specific-references
    """

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        self.config = {
            "domain": [
                "https://gitlab.com",
                "GitLab domain or Enterprise Server domain",
            ],
            "group": ["", "GitLab user or group (and subgroup)."],
            "project": ["", "Repository name"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        md.inlinePatterns.register(
            MergeRequestPattern(self.getConfigs(), md),
            "merge-request",
            20,
        )


def makeExtension(**kwargs: Any) -> GitlabLinks:  # noqa: ANN401
    return GitlabLinks(**kwargs)
