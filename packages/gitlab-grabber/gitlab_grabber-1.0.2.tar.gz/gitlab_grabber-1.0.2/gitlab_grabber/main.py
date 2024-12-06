"""Main module."""

import asyncio

from gitlab_grabber.logger import Logging
from gitlab_grabber.gitlab import get_project, clone_all_repositories
from gitlab_grabber.cli import create_parser
from gitlab_grabber.http_client import HTTPClient

logger = Logging(__name__)
parser, gitlab = create_parser()
http_client = HTTPClient(gitlab=gitlab)


async def async_main():
    """Async main."""
    projects = await get_project(gitlab=gitlab, http_client=http_client)
    await clone_all_repositories(gitlab=gitlab, projects=projects)


def main():
    """Syn main."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
