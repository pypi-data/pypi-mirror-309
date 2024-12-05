import os
import shutil
import subprocess
import typing
from enum import Enum, auto

import msgspec
import questionary
import toml
import tomlkit
from questionary.prompts.common import Choice
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.theme import Theme


def parse_version(version: str) -> list[int]:
    """
    Parse a version string (e.g., 'v0.1.2') into a list of integers [major, minor, patch].

    Args:
        version (str): The version string to parse, prefixed with 'v'.

    Returns:
        List[int]: A list representing the version [major, minor, patch].
    """
    return list(map(int, version.lstrip("v").split(".")))


def compare_releases(version1: str, version2: str) -> int:
    """
    Compare two semantic versions.

    Args:
        version1 (str): The first version string (e.g., 'v0.1.2').
        version2 (str): The second version string (e.g., 'v0.2.0').

    Returns:
        int: -1 if version1 < version2,
             0 if version1 == version2,
             1 if version1 > version2.
    """
    parsed_version1 = parse_version(version1)
    parsed_version2 = parse_version(version2)

    if parsed_version1 < parsed_version2:
        return -1
    elif parsed_version1 > parsed_version2:
        return 1
    else:
        return 0


class ReleaseType(Enum):
    MAJOR = auto()
    FEATURE = auto()
    PATCH = auto()


def clear_console() -> None:
    print("\033[H\033[3J", end="")

def main() -> None:
    # Setup rich console with a custom theme
    custom_theme = Theme({
        "success": "bold green",
        "error": "bold red",
        "question": "blue"
    })
    console = Console(theme=custom_theme)

    user_response = questionary.select(
        "What kind of release are you doing?",
        [
            Choice(title="Major", value=ReleaseType.MAJOR),
            Choice(title="Feature", value=ReleaseType.FEATURE),
            Choice(title="Patch", value=ReleaseType.PATCH),
        ],
    ).ask()

    # Load pyproject.toml
    pyproject: dict[str, typing.Any] = toml.load("pyproject.toml")
    project: typing.Optional[dict[str, typing.Any]] = pyproject.get("project", None)

    if not project or "version" not in project:
        console.print("The 'version' field is required in 'pyproject.toml'.", style="error")
        raise ValueError("The 'version' field is required in 'pyproject.toml'.")

    # Ensure GitHub CLI is installed
    gh_cli = shutil.which("gh")
    if not gh_cli:
        console.print("GitHub CLI ('gh') is required to run this script.", style="error")
        raise ValueError("GitHub CLI ('gh') is required to run this script.")

    # Fetch latest release tag
    result = subprocess.run(
        [gh_cli, "release", "list", "--json", "tagName"],
        env={**os.environ, "GH_PAGER": "cat"},
        capture_output=True,
        text=True,
        check=True,
    )

    releases = msgspec.json.decode(result.stdout)
    tag_version = releases[0].get("tagName") if releases else "v0.0.0"

    # Calculate new version
    parsed_version = parse_version(tag_version)
    match user_response:
        case ReleaseType.MAJOR:
            parsed_version[0] += 1
            parsed_version[1] = 0
            parsed_version[2] = 0
        case ReleaseType.FEATURE:
            parsed_version[1] += 1
            parsed_version[2] = 0
        case ReleaseType.PATCH:
            parsed_version[2] += 1

    new_version = f"v{'.'.join(map(str, parsed_version))}"

    # Update pyproject.toml
    pyproject["project"]["version"] = new_version
    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(pyproject))

    # Ensure CHANGELOG.md exists or handle empty file
    changelog_path = "CHANGELOG.md"
    if not os.path.exists(changelog_path):
        console.print(f"{changelog_path} does not exist. Creating an empty file.", style="question")
        with open(changelog_path, 'w') as f:
            f.write("# Changelog\n\n")
    elif os.stat(changelog_path).st_size == 0:
        console.print(f"{changelog_path} is empty. Would you like to add some notes?", style="question")
        if Confirm.ask("Add notes to CHANGELOG.md?", default=False):
            notes = Prompt.ask("Enter changelog notes:")
            with open(changelog_path, 'a') as f:
                f.write(f"## {new_version}\n\n- {notes}\n\n")
        else:
            console.print("Continuing with empty changelog.", style="question")

    # Create release using GitHub CLI
    release_title = Prompt.ask("Enter release title (default: version tag):", default=new_version)
    extra_flags = Prompt.ask("Enter additional GitHub CLI flags (optional):")

    try:
        subprocess.run(
            [
                gh_cli,
                "release",
                "create",
                new_version,
                "-F", changelog_path,
                "-t", release_title or new_version,
                *(extra_flags.split() if extra_flags else []),
            ],
            check=True,
        )
        console.print(f"Release [success]{new_version}[/success] created successfully!")
    except subprocess.CalledProcessError as e:
        console.print(f"Failed to create release: {e}", style="error")

if __name__ == "__main__":
    clear_console()
    main()
