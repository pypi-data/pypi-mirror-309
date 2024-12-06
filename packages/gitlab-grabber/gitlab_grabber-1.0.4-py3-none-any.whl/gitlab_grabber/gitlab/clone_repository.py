"""Clone repo module."""

import os.path
from typing import Dict, Any
from git import Repo, GitCommandError
from gitlab_grabber.logger import Logging
from gitlab_grabber.cli import GitlabConfig
import asyncio

logger = Logging(__name__)


async def clone_repository(
    repo_url: str, clone_dir: str, repo_name: str, gitlab: GitlabConfig
) -> None:
    """Clone repo. GitPython is sync lib, we should use to_thread method."""
    await asyncio.to_thread(
        clone_repository_sync, repo_url, clone_dir, repo_name, gitlab
    )


def clone_repository_sync(
    repo_url: str, clone_dir: str, repo_name: str, gitlab: GitlabConfig
) -> None:
    """Sync method to clone repo."""
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    dest_path = os.path.join(clone_dir, repo_name)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    if gitlab.skip_verify:
        env["GIT_SSL_NO_VERIFY"] = "true"
    elif gitlab.crt_path:
        env["GIT_SSL_CAINFO"] = gitlab.crt_path
    if gitlab.identity_file:
        env["GIT_SSH_COMMAND"] = (
            f"ssh -i {gitlab.identity_file} -o BatchMode=yes -o IdentitiesOnly=yes"
        )

    if os.path.exists(dest_path):
        logger.info(
            "Repository %s already exists in %s, execute git pull",
            repo_name,
            dest_path,
        )
        try:
            repo = Repo(dest_path)
            repo.git.pull(env=env)
            logger.info("Repository %s updated", repo_name)
        except GitCommandError as err:
            raise err
        return

    try:
        logger.info("Clone repository %s in %s", repo_name, dest_path)
        Repo.clone_from(repo_url, dest_path, env=env)
        logger.info("Repository %s successful cloned", repo_name)
    except GitCommandError as err:
        raise err


async def clone_all_repositories(
    gitlab: GitlabConfig, projects: Dict[str, Dict[str, Any]]
):
    """Clone all repos, start from here."""
    tasks = []
    clone_dir = gitlab.clone_dir
    semaphore = asyncio.Semaphore(20)
    for project in projects.values():
        if gitlab.auth == "ssh":
            repo_url = project["ssh_url_to_repo"]
        else:
            repo_url = project["http_url_to_repo"]
            if gitlab.token:
                repo_url = repo_url.replace(
                    "https://", f"https://oauth2:{gitlab.token}@"
                )
        repo_name = project["repo_name"]
        tasks.append(
            clone_repository_with_semaphore(
                repo_url=repo_url,
                clone_dir=clone_dir,
                repo_name=repo_name,
                semaphore=semaphore,
                gitlab=gitlab,
            )
        )
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result, project in zip(results, projects.values()):
        if isinstance(result, Exception):
            logger.error(
                "Clone repository %s failed with error: %s",
                project["repo_name"],
                result,
            )


async def clone_repository_with_semaphore(
    repo_url: str,
    clone_dir: str,
    repo_name: str,
    semaphore: asyncio.Semaphore,
    gitlab: GitlabConfig,
):
    """Usage semaphore to limit thread with sync func for clone."""
    async with semaphore:
        try:
            await clone_repository(
                repo_url=repo_url,
                clone_dir=clone_dir,
                repo_name=repo_name,
                gitlab=gitlab,
            )
        except Exception as err:
            return err
