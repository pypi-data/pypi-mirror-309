# Python-Markdown GitLab-Links Extension

An extension to [Python-Markdown](https://github.com/Python-Markdown/markdown)
which adds support for [GitLab-specific references](https://docs.gitlab.com/ee/user/markdown.html#gitlab-specific-references).
Inspired by [github-links](https://github.com/Python-Markdown/github-links/tree/master).

## Installation

```text
pip install mdx-gitlab-links
```

## Usage

To use the extension simply include its name in the list of extensions
passed to Python-Markdown.

To set configuration options,
you may pass them to Markdown's `exension_configs` keyword.

```python
import markdown

markdown.markdown(
    src,
    extensions=["mdx_gitlab_links"],
    extension_configs={
        "mdx_gitlab_links": {
            "domain": "https://gitlab.mydomain.com",
            "group": "my-group/my-subgroup",
            "project": "my-project",
        },
    },
)
```

Or you may import and pass the configs directly
to an instance of the `mdx_gitlab_links.GitlabLinks` class.

```python
import markdown
from mdx_gitlab_links import GitlabLinks

extension = GitlabLinks(
    domain="https://gitlab.mydomain.com",
    group="my-group/my-subgroup",
    project="my-project",
)

markdown.markdown(src, extensions=[extension])
```

The following configurations options are available:

- **domain**:
    The GitLab domain or Enterprise Server domain.
    Default to `https://gitlab.com`.
- **group**:
    The GitLab user or group (and subgroup).
- **project**:
    The GitLab repository name.

## Syntax

All links are assigned the `gl-link` class as well
as a class unique to that type of link.
See each type for the specific class assigned.

### Merge Requests

All merge requests links are assigned the `gl-mr` class.

The following table provides various examples
(with the defaults set as `group='group/subgroup'`, `project='project'`):

| input               | href                                            | render |
|---------------------|-------------------------------------------------|--------|
| `!123`              | `https://gitlab.com/group/subgroup/project/123` | [!123](https://gitlab.com/group/subgroup/project/-/merge_requests/123 "GitLab Merge Request group/subgroup/project/123") |
| `proj!123`          | `https://gitlab.com/group/subgroup/proj/123`    | [proj/!123](https://gitlab.com/group/subgroup/proj/-/merge_requests/123 "GitLab Merge Request group/subgroup/proj/123") |
| `grp/sub/proj!123`  | `https://gitlab.com/grp/sub/proj/123`           | [grp/sub/proj/!123](https://gitlab.com/grp/sub/proj/-/merge_requests/123 "GitLab Merge Request grp/sub/proj/123") |
| `\!123`             |                                                 | !123 |
| `proj\!123`         |                                                 | proj!123 |
| `grp/sub/proj\!123` |                                                 | grp/sub/proj!123 |
