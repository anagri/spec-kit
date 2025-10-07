#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install specify-cli --from git+https://github.com/anagri/spec-kit.git
    speclaude init <project-name>
    speclaude init .
    speclaude init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import Optional, Tuple

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

# Constants
# Hardcoded to Claude Code only (macOS-focused spec-kit)
AI_AGENT = "claude"
# Hardcoded to bash/sh scripts (macOS/Unix only)
SCRIPT_TYPE = "sh"

# Claude CLI local installation path after migrate-installer
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

# ASCII Art Banner
BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "GitHub Spec Kit - Spec-Driven Development Toolkit"
class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree



MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩ 
"""

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()
    
    # Arrow keys
    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'
    
    # Enter/Return
    if key == readchar.key.ENTER:
        return 'enter'
    
    # Escape
    if key == readchar.key.ESC:
        return 'escape'
        
    # Ctrl+C
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key



def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.
    
    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with
        
    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0
    
    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")
        
        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
        
        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")
        
        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
    
    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)
                    
                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    # Suppress explicit selection print; tracker / later logic will report consolidated status
    return selected_key



console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""
    
    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="speclaude",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    # Show banner only when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'specify --help' for usage information[/dim]"))
        console.print()


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool_for_tracker(tool: str, tracker: StepTracker) -> bool:
    """Check if a tool is installed and update tracker."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    else:
        tracker.error(tool, "not found")
        return False


def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""
    
    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/anagri/spec-kit/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            return True
    
    if shutil.which(tool):
        return True
    else:
        return False


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True
        
    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def download_template_from_github(download_dir: Path, *, verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    """Download Claude Code + bash template from GitHub releases.

    This fork only supports Claude Code with bash scripts (hardcoded).
    """
    repo_owner = "anagri"
    repo_name = "spec-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            msg = f"GitHub API returned {status} for {api_url}"
            if debug:
                msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
            raise RuntimeError(msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    # Find the template asset (Claude Code + bash only)
    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{AI_AGENT}-{SCRIPT_TYPE}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]Claude Code + bash[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]
    
    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")
    
    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"Download failed with {response.status_code}\nHeaders: {response.headers}\nBody (truncated): {body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata


def download_and_extract_template(project_path: Path, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """Download the latest Claude Code + bash release and extract it to create a new project.

    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup).
    This fork only supports Claude Code with bash scripts (hardcoded).
    """
    current_dir = Path.cwd()

    # Step: fetch + download combined
    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            current_dir,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise
    
    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")
    
    try:
        # Create project directory only if not using current directory
        if not is_current_dir:
            project_path.mkdir(parents=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in the ZIP for debugging
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")
            
            # For current directory, extract to a temp location first
            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)
                    
                    # Check what was extracted
                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")
                    
                    # Handle GitHub-style ZIP with a single root directory
                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")
                    
                    # Copy contents to current directory
                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                # Recursively copy directory contents
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                # Extract directly to project directory (original behavior)
                zip_ref.extractall(project_path)
                
                # Check what was extracted
                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")
                
                # Handle GitHub-style ZIP with a single root directory
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # Move contents up one level
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"
                    # Move the nested directory contents to temp location
                    shutil.move(str(nested_dir), str(temp_move_dir))
                    # Remove the now-empty project directory
                    project_path.rmdir()
                    # Rename temp directory to project directory
                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")
                    
    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")
        # Clean up downloaded ZIP file
        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")
    
    return project_path


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .specify/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")


def validate_local_repo(local_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate that a local path contains required spec-kit repository structure.

    Args:
        local_path: Resolved absolute Path object to validate

    Returns:
        (is_valid, error_message): (True, None) if valid, (False, error_msg) if invalid
    """
    required_dirs = {
        "templates": local_path / "templates",
        "templates/commands": local_path / "templates" / "commands",
        "scripts/bash": local_path / "scripts" / "bash",
        "memory": local_path / "memory",
    }

    missing = []
    found = []

    for label, dir_path in required_dirs.items():
        if dir_path.exists() and dir_path.is_dir():
            found.append(label)
        else:
            missing.append(label)

    if missing:
        # Build formatted error message
        error_lines = ["Invalid spec-kit repository structure", ""]
        error_lines.append("Missing required directories:")
        for m in missing:
            error_lines.append(f"  ✗ {m}/")

        if found:
            error_lines.append("")
            error_lines.append("Found:")
            for f in found:
                error_lines.append(f"  ✓ {f}/")

        error_lines.extend([
            "",
            "Required structure:",
            "  templates/",
            "  templates/commands/",
            "  scripts/bash/",
            "  memory/",
            "",
            "Ensure you're pointing to the root of a spec-kit repository."
        ])

        return False, "\n".join(error_lines)

    return True, None


def copy_local_templates(
    project_path: Path,
    local_path: Path,
    is_current_dir: bool,
    tracker: Optional[StepTracker] = None,
) -> None:
    """
    Copy PRE-PROCESSED templates from local repository to project directory.

    Templates are already processed for Claude Code + bash during preprocessing,
    so we just copy them as-is without any transformations.

    Args:
        project_path: Target project directory
        local_path: Source spec-kit repository path
        is_current_dir: True if using --here flag
        tracker: Optional progress tracker

    Raises:
        OSError, PermissionError on copy failure
    """
    if tracker:
        tracker.add("copy", "Copy templates from local")
        tracker.start("copy")

    try:
        file_count = 0

        # Path mapping (templates are pre-processed, copy as-is):
        # templates/*.md (exclude commands/) → .specify/templates/
        # templates/commands/*.md → .claude/commands/
        # scripts/bash/ → .specify/scripts/bash/
        # memory/ → .specify/memory/

        # 1. Copy templates/*.md (excluding commands/) to .specify/templates/
        templates_src = local_path / "templates"
        templates_dst = project_path / ".specify" / "templates"
        templates_dst.mkdir(parents=True, exist_ok=True)

        for item in templates_src.glob("*.md"):
            shutil.copy2(item, templates_dst / item.name)
            file_count += 1

        # 2. Copy templates/commands/ to .claude/commands/
        commands_src = local_path / "templates" / "commands"
        commands_dst = project_path / ".claude" / "commands"
        if commands_src.exists():
            shutil.copytree(
                commands_src,
                commands_dst,
                symlinks=False,  # Follow symlinks (dereference)
                dirs_exist_ok=True,  # Merge with existing (for --here mode)
            )
            # Count files in commands
            file_count += sum(1 for f in commands_dst.rglob("*.md") if f.is_file())

        # 3. Copy scripts/bash/ to .specify/scripts/bash/
        scripts_src = local_path / "scripts" / "bash"
        scripts_dst = project_path / ".specify" / "scripts" / "bash"
        if scripts_src.exists():
            shutil.copytree(
                scripts_src,
                scripts_dst,
                symlinks=False,
                dirs_exist_ok=True,
            )
            # Count files in scripts
            file_count += sum(1 for f in scripts_dst.rglob("*.sh") if f.is_file())

        # 4. Copy memory/ to .specify/memory/
        memory_src = local_path / "memory"
        memory_dst = project_path / ".specify" / "memory"
        if memory_src.exists():
            shutil.copytree(
                memory_src,
                memory_dst,
                symlinks=False,
                dirs_exist_ok=True,
            )
            # Count files in memory
            file_count += sum(1 for f in memory_dst.rglob("*") if f.is_file())

        if tracker:
            tracker.complete("copy", f"{file_count} files")

    except (OSError, PermissionError) as e:
        if tracker:
            tracker.error("copy", str(e))
        raise


@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for Claude Code CLI"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
    local: str = typer.Option(None, "--local", help="Path to local spec-kit repository (for template development)"),
):
    """
    Initialize a new Specify project for Claude Code with bash scripts.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Download the Claude Code + bash template from GitHub
    3. Extract the template to a new project directory or current directory
    4. Initialize a fresh git repository (if not --no-git and no existing repo)
    5. Set up Claude Code slash commands

    This fork only supports Claude Code with bash scripts.

    Examples:
        speclaude init my-project
        speclaude init my-project --no-git
        speclaude init my-project --ignore-agent-tools
        speclaude init .                     # Initialize in current directory
        speclaude init --here                # Alternative syntax for current directory
        speclaude init --here --force        # Skip confirmation when current directory not empty
    """
    # Show banner first
    show_banner()
    
    # Handle '.' as shorthand for current directory (equivalent to --here)
    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic
    
    # Validate arguments
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)
    
    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)
    
    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()
        
        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                # Ask for confirmation
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)
    
    # Create formatted setup info with column alignment
    current_dir = Path.cwd()
    
    setup_lines = [
        "[cyan]Specify Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]
    
    # Add target path only if different from working dir
    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")
    
    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))
    
    # Check git only if we might need it (not --no-git)
    # Only set to True if the user wants it and the tool is available
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", "https://git-scm.com/downloads")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # Check for Claude Code CLI unless ignored
    if not ignore_agent_tools:
        if not check_tool("claude", "https://docs.anthropic.com/en/docs/claude-code/setup"):
            error_panel = Panel(
                "Claude Code CLI not found\n"
                "Install from: [cyan]https://docs.anthropic.com/en/docs/claude-code/setup[/cyan]\n\n"
                "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                title="[red]Claude Code Required[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    console.print(f"[cyan]Using Claude Code with bash scripts[/cyan]")
    
    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker("Initialize Specify Project")
    # Flag to allow suppressing legacy headings
    sys._specify_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")

    # Add steps based on mode (local vs GitHub)
    if local:
        for key, label in [
            ("validate", "Validate local repository"),
            ("copy", "Copy templates from local"),
            ("chmod", "Ensure scripts executable"),
            ("git", "Initialize git repository"),
            ("final", "Finalize")
        ]:
            tracker.add(key, label)
    else:
        for key, label in [
            ("fetch", "Fetch latest release"),
            ("download", "Download template"),
            ("extract", "Extract template"),
            ("zip-list", "Archive contents"),
            ("extracted-summary", "Extraction summary"),
            ("chmod", "Ensure scripts executable"),
            ("cleanup", "Cleanup"),
            ("git", "Initialize git repository"),
            ("final", "Finalize")
        ]:
            tracker.add(key, label)

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            if local:
                # LOCAL MODE: Validate and copy from local repository
                local_path = Path(local).resolve()

                # Validate path exists
                if not local_path.exists():
                    error_panel = Panel(
                        f"Local path '[cyan]{local}[/cyan]' does not exist\n\n"
                        "Provide a valid path to a spec-kit repository.",
                        title="[red]Invalid Local Path[/red]",
                        border_style="red",
                        padding=(1, 2)
                    )
                    console.print()
                    console.print(error_panel)
                    raise typer.Exit(1)

                # Validate path is directory
                if not local_path.is_dir():
                    error_panel = Panel(
                        f"Local path '[cyan]{local}[/cyan]' is not a directory\n\n"
                        "The --local flag requires a directory containing a spec-kit repository.",
                        title="[red]Invalid Local Path[/red]",
                        border_style="red",
                        padding=(1, 2)
                    )
                    console.print()
                    console.print(error_panel)
                    raise typer.Exit(1)

                # Validate repository structure
                tracker.start("validate")
                is_valid, error_msg = validate_local_repo(local_path)
                if not is_valid:
                    tracker.error("validate", "missing directories")
                    # Stop live rendering to show error panel
                    live.stop()
                    console.print()
                    error_panel = Panel(
                        error_msg,
                        title="[red]Invalid Repository Structure[/red]",
                        border_style="red",
                        padding=(1, 2)
                    )
                    console.print(error_panel)
                    raise typer.Exit(1)

                tracker.complete("validate", "3 directories found")

                # Copy templates from local repository
                copy_local_templates(project_path, local_path, here, tracker)
            else:
                # GITHUB MODE: Download and extract template
                # Create a httpx client with verify based on skip_tls
                verify = not skip_tls
                local_ssl_context = ssl_context if verify else False
                local_client = httpx.Client(verify=local_ssl_context)

                download_and_extract_template(project_path, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            # Ensure scripts are executable (POSIX)
            ensure_executable_scripts(project_path, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")
    
    # Claude folder security notice
    security_notice = Panel(
        "Claude Code may store credentials, auth tokens, or other private data in [cyan].claude/[/cyan]\n"
        "Consider adding [cyan].claude/[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
        title="[yellow]Security Notice[/yellow]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print()
    console.print(security_notice)
    
    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        steps_lines.append("2. Start using slash commands with Claude Code:")
    else:
        steps_lines.append("1. You're already in the project directory!")
        steps_lines.append("2. Start using slash commands with Claude Code:")

    steps_lines.append("   2.1 [cyan]/constitution[/] - Establish project principles")
    steps_lines.append("   2.2 [cyan]/specify[/] - Create baseline specification")
    steps_lines.append("   2.3 [cyan]/plan[/] - Create implementation plan")
    steps_lines.append("   2.4 [cyan]/tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.5 [cyan]/implement[/] - Execute implementation")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "Optional commands that you can use for your specs [bright_black](improve quality & confidence)[/bright_black]",
        "",
        f"○ [cyan]/clarify[/] [bright_black](optional)[/bright_black] - Ask structured questions to de-risk ambiguous areas before planning (run before [cyan]/plan[/] if used)",
        f"○ [cyan]/analyze[/] [bright_black](optional)[/bright_black] - Cross-artifact consistency & alignment report (after [cyan]/tasks[/], before [cyan]/implement[/])"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title="Enhancement Commands", border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)

@app.command()
def check():
    """Check that required tools are installed."""
    show_banner()
    console.print("[bold]Checking for required tools...[/bold]\n")

    tracker = StepTracker("Check Required Tools")

    tracker.add("git", "Git version control")
    tracker.add("claude", "Claude Code CLI")

    git_ok = check_tool_for_tracker("git", tracker)
    claude_ok = check_tool_for_tracker("claude", tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")
    if not claude_ok:
        console.print("[dim]Tip: Install Claude Code for AI assistance[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
