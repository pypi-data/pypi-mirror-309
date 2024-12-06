"""CLI module."""

import argparse
import os
from dataclasses import dataclass


@dataclass
class GitlabConfig:
    """Gitlab parameters."""

    token: str
    url: str
    crt_path: str
    auth: str
    identity_file: str = None
    timeout: int = 60
    skip_verify: bool = False
    api_url: str = "/api/v4/projects?simple=true"
    clone_dir: str = "."


def create_parser() -> tuple[argparse.ArgumentParser, GitlabConfig]:
    """CLI parser."""
    parser = argparse.ArgumentParser(description="Gitlab grabber")
    parser.add_argument(
        "-t",
        "--token",
        required=False,
        default=os.environ.get(
            "GITLAB_TOKEN",
        ),
        dest="token",
        help="Gitlab token",
    )
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        dest="url",
        default=os.environ.get("GITLAB_URL", "gitlab.com"),
        help="Gitlab base url like domain.com",
    )
    parser.add_argument(
        "--crt-path",
        dest="crt_path",
        required=False,
        default=os.environ.get("SSL_CRT_PATH"),
        help="Path to CA gitlab certificate.",
    )
    parser.add_argument(
        "-k",
        "--skip-verify",
        dest="skip_verify",
        required=False,
        action="store_true",
        help="Skip ssl verification",
    )
    parser.add_argument(
        "--timeout",
        dest="timeout",
        required=False,
        type=int,
        default=os.environ.get("HTTP_TIMEOUT", 30),
        help="set http request timeout",
    )
    parser.add_argument(
        "--auth",
        dest="auth",
        required=False,
        default=os.environ.get(
            "AUTH",
            "ssh",
        ),
        choices=["ssh", "http"],
        help="Auth usage ssh or http.",
    )
    parser.add_argument(
        "-i",
        "--identify-file",
        dest="identity_file",
        required=False,
        help="Path to ssh private key.",
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="clone_dir",
        required=False,
        default=os.environ.get("SAVE_DIR", "."),
        help="Path to clone repository.",
    )

    args = parser.parse_args()

    if args.auth == "ssh" and not args.identity_file:
        parser.error("-i (--identity-file) is required when --auth is 'ssh'")

    gitlab_cfg = GitlabConfig(
        token=args.token,
        url=args.url,
        crt_path=args.crt_path,
        skip_verify=args.skip_verify,
        timeout=args.timeout,
        auth=args.auth,
        identity_file=args.identity_file,
        clone_dir=args.clone_dir,
    )
    if not gitlab_cfg.token:
        parser.error(
            "Gitlab token is missing. Please set it using -t or GITLAB_TOKEN env."
        )
    return parser, gitlab_cfg
