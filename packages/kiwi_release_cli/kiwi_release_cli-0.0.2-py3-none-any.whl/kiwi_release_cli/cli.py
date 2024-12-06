"""CLI for updating release tags manually."""
import re
import sys


import click
from git import Repo
import semver


@click.group()
def cli():
    """Release actions."""


def _get_latest_tag(repo: Repo) -> str | None:
    """Return the latest tag that is a semver tag, else return None."""
    semver_pattern = r'^\d+\.\d+\.\d+$'
    tags = [
        t for t in sorted(
            repo.tags,
            key=lambda t: t.commit.committed_datetime
        ) if re.match(semver_pattern, t.name)
    ]

    # Find the latest tag that matches the semver format (x.x.x)
    if tags:
        return str(tags[-1])

    # No existing tags
    return None


def _comma_separated_list(
    ctx: click.Context,  # pylint: disable=unused-argument
    param: click.core.Option,   # pylint: disable=unused-argument
    value: str
) -> list[str]:
    """Return a list of strings from input comma-separated string."""
    if not value:
        return []
    return [x.strip() for x in value.split(",")]


@cli.command()
@click.option("--major", is_flag=True, help="Bump major version")
@click.option("--minor", is_flag=True, help="Bump minor version")
@click.option("--patch", is_flag=True, help="Bump patch version")
@click.option("--dryrun", is_flag=True, help="Preview the release tag change")
@click.option(
    "--additional-tags",
    help="Comma-separated list of extra tags to add to release",
    callback=_comma_separated_list,
    type=click.STRING,
)
def tag(
    major: bool,
    minor: bool,
    patch: bool,
    dryrun: bool,
    additional_tags: list[str]
) -> None:
    """Cut a new tag for the release."""
    repo = Repo()
    if repo.is_dirty():
        raise click.ClickException(
            "Local repo is dirty, stash all changes before proceeding."
        )
    restore_branch = None
    if repo.active_branch != "main":
        restore_branch = repo.active_branch
        print("Checking out main branch...")
        repo.git.checkout("main")
    repo.remotes.origin.pull()
    latest_tag = _get_latest_tag(repo)
    new_tag = latest_tag or "0.0.1"
    if latest_tag:
        print(f"Changes since tag {latest_tag}:")
        print(repo.git.log("--oneline", f"{latest_tag}..main"))
        if major:
            new_tag = semver.bump_major(new_tag)
        if minor:
            new_tag = semver.bump_minor(new_tag)
        if patch:
            new_tag = semver.bump_patch(new_tag)

    new_tags = additional_tags + [new_tag]
    if dryrun:
        for add_tag in new_tags:
            print(f"Would create tag {add_tag}.")
    else:
        for add_tag in new_tags:
            if add_tag in repo.tags:
                print(f"Deleting existing tag {add_tag}...")
                tag_ref = repo.tag(add_tag)
                repo.delete_tag(tag_ref)

            print(f"Creating tag {add_tag}...")
            repo.create_tag(add_tag)

            print(f"Pushing tag {add_tag}...")
            repo.remotes.origin.push(add_tag)
    if restore_branch:
        print(f"Restoring branch {restore_branch}.")
        repo.git.checkout(restore_branch)


def main():
    """CLI entrypoint."""
    cli()


if __name__ == "__main__":
    sys.exit(main())
