import os
import re
import shutil
import subprocess
from enum import Enum, auto

import msgspec
import questionary
import toml
import tomlkit
from halo import Halo
from pyfiglet import Figlet
from questionary.prompts.common import Choice
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import track
from rich.text import Text
from rich.theme import Theme


def parse_version(version: str) -> list[int]:
    return list(map(int, version.lstrip("v").split(".")))


def compare_releases(version1: str, version2: str) -> int:
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
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_ascii_art():
    """Display an ASCII art title."""
    f = Figlet(font='big')
    console.print(Panel(Text(f.renderText("Weavearc"), style="bold magenta")), justify="center")


# Define console here
custom_theme = Theme(
    {"success": "bold green", "error": "bold red", "question": "blue", "info": "cyan"}
)
console = Console(theme=custom_theme)


def main():
    clear_console()
    display_ascii_art()

    # Loading animation while checking environment
    spinner = Halo(text='Checking environment', spinner='dots')
    spinner.start()

    # Ensure GitHub CLI is installed
    gh_cli = shutil.which("gh")
    if not gh_cli:
        spinner.fail("GitHub CLI ('gh') is required to run this script.")
        raise ValueError("GitHub CLI ('gh') is required to run this script.")

    # Fetch latest release tag
    result = subprocess.run(
        [gh_cli, "release", "list", "--json", "tagName"],
        env={**os.environ, "GH_PAGER": "cat"},
        capture_output=True,
        text=True,
        check=True,
    )
    spinner.succeed("Environment check completed successfully.")

    releases = msgspec.json.decode(result.stdout)
    tag_version = releases[0].get("tagName") if releases else "v0.0.0"

    # Release type selection with beautiful prompts
    console.print(Panel(Markdown("### What kind of release are you doing?"), title="Choose Release Type", title_align="left"))
    choices = [
        Choice(title="Patch", value=ReleaseType.PATCH),
        Choice(title="Feature", value=ReleaseType.FEATURE),
        Choice(title="Major", value=ReleaseType.MAJOR),
    ]
    user_response = questionary.select("", choices=choices, style=questionary.Style([
        ('question', 'fg:#673ab7 bold'),
        ('answer', 'fg:#03a9f4 bold')
    ])).ask()

    # Double confirmation for major or feature releases
    if user_response in [ReleaseType.MAJOR, ReleaseType.FEATURE]:
        for i in track(range(2), description="[info]Confirming release type..."):
            if not questionary.confirm(
                f"Are you sure you want to proceed with a {user_response.name} release?",
                default=False,
                style=questionary.Style([('question', 'fg:#673ab7 bold')])
            ).ask():
                console.print(Panel("Release process terminated.", style="question"))
                return

    # Load and update pyproject.toml
    pyproject = toml.load("pyproject.toml")
    project = pyproject.get("project", None)
    if not project or "version" not in project:
        console.print(Panel("The 'version' field is required in 'pyproject.toml'.", style="error"))
        raise ValueError("The 'version' field is required in 'pyproject.toml'.")

    # Calculate new version
    parsed_version = parse_version(tag_version)
    if user_response == ReleaseType.MAJOR:
        parsed_version[0] += 1
        parsed_version[1] = 0
        parsed_version[2] = 0
    elif user_response == ReleaseType.FEATURE:
        parsed_version[1] += 1
        parsed_version[2] = 0
    else:
        parsed_version[2] += 1

    new_version = f"v{'.'.join(map(str, parsed_version))}"

    # Git operations
    if questionary.confirm("Add, commit, and push everything not stashed before releasing?", default=True).ask():
        commands = [
            ["git", "add", "."],
            ["git", "commit", "-m", new_version],
            ["git", "push"],
        ]
        for cmd in commands:
            with Halo(text=f'Running {" ".join(cmd)}', spinner='dots'):
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    if cmd[1] == 'commit' and 'nothing to commit' in result.stdout.lower():
                        console.print(Panel("Nothing to commit.", style="info"))
                    else:
                        console.print(Panel(f"Command {' '.join(cmd)} failed with return code {result.returncode}", style="error"))
                        console.print(Panel(f"Output:\n{result.stdout}\n{result.stderr}", style="error"))
                        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
                else:
                    console.print(Panel("Command executed successfully.", style="success"))

        console.print(Panel("Changes committed and pushed to the repository.", style="success"))

    # Update pyproject.toml
    pyproject["project"]["version"] = new_version
    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(pyproject))

    # Ensure CHANGELOG.md exists
    changelog_path = "CHANGELOG.md"
    if not os.path.exists(changelog_path):
        with open(changelog_path, "w") as f:
            f.write("# Changelog\n\n")
        console.print(Panel(f"{changelog_path} created.", style="info"))
    else:
        # Check if the current version in CHANGELOG.md matches the new version
        with open(changelog_path, 'r') as f:
            content = f.read()

            # Regex pattern to match version strings like v0.1.2 or v0.2.1
            match = re.search(r'#* v?(\d+\.\d+\.\d+)', content)

            if match:
                current_version = match.group(1).strip()
            else:
                current_version = "v0.0.0"  # Default version if no version header is found

        if current_version and new_version:
            if compare_releases(current_version, new_version) != 0:
                if questionary.confirm(f"The version in {changelog_path} ({current_version}) does not match the new version ({new_version}). Do you want to overwrite the file?", default=False).ask():
                    with open(changelog_path, "w") as f:
                        f.write(f"# Changelog\n\n## {new_version}\n\n- \n")
                else:
                    console.print(Panel("Keeping existing CHANGELOG.md content.", style="info"))
        else:
            console.print(Panel(f"Could not determine version from {changelog_path}. Overwriting with new version.", style="info"))
            with open(changelog_path, "w") as f:
                f.write(f"# Changelog\n\n## {new_version}\n\n- \n")

    # Git commit and push for changes in pyproject.toml and CHANGELOG.md
    commands = [
        ["git", "add", "pyproject.toml", changelog_path],
        ["git", "commit", "-m", f"Release {new_version}"],
        ["git", "push"],
    ]
    for cmd in commands:
        with Halo(text=f'Running {" ".join(cmd)}', spinner='dots'):
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                if cmd[1] == 'commit' and 'nothing to commit' in result.stdout.lower():
                    console.print(Panel("Nothing to commit.", style="info"))
                else:
                    console.print(Panel(f"Command {' '.join(cmd)} failed with return code {result.returncode}", style="error"))
                    console.print(Panel(f"Output:\n{result.stdout}\n{result.stderr}", style="error"))
                    raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
            else:
                console.print(Panel("Command executed successfully.", style="success"))

    # Create release using GitHub CLI
    release_title = questionary.text("Enter release title (default: version tag):", default=new_version).ask()
    extra_flags = questionary.text("Enter additional GitHub CLI flags (optional):").ask()

    try:
        subprocess.run(
            [
                gh_cli,
                "release",
                "create",
                new_version,
                "-F",
                changelog_path,
                "-t",
                release_title or new_version,
                *(extra_flags.split() if extra_flags else []),
            ],
            check=True,
        )
        console.print(Panel(f"Release [success]{new_version}[/success] created successfully!", style="success"))
    except subprocess.CalledProcessError as e:
        console.print(Panel(f"Failed to create release: {e}", style="error"))


if __name__ == "__main__":
    main()
