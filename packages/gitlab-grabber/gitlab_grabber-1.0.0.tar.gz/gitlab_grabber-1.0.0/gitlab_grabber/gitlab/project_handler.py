"""Gitlab project module."""

from gitlab_grabber.logger import Logging
from gitlab_grabber.http_client import HTTPClient
from gitlab_grabber.cli import GitlabConfig
from typing import Dict, Any

logger = Logging(__name__)


async def get_project(
    gitlab: GitlabConfig, http_client: HTTPClient
) -> Dict[str, Dict[str, Any]]:
    """Collect all gitlab project."""
    projects = {}
    page = 1
    while True:
        response = await http_client.send_request(
            request_type="get",
            url=gitlab.url + gitlab.api_url,
            headers={"PRIVATE-TOKEN": gitlab.token},
            params={"page": page},
        )
        if response is None:
            logger.error("Can't get data from page %s", page)
            break

        data = await response.json()
        for _, item in enumerate(data):
            projects[f"{item['id']}-{item['name']}"] = {
                "repo_name": item["name"],
                "path_with_namespace": item["path_with_namespace"],
                "ssh_url_to_repo": item["ssh_url_to_repo"],
                "http_url_to_repo": item["http_url_to_repo"],
            }
            logger.info("Collect data from project %s", item["name"])
        next_page = response.headers.get("X-Next-Page")
        if next_page:
            page = int(next_page)
        else:
            break

    return projects
