from pathlib import Path
from typing import List, Dict, Set
import tomli
import importlib.resources

import copier
import typer
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

app = typer.Typer(
    name="components",
    help="Install and update components from basic-components",
    add_completion=False,
)
console = Console()

# Default values for REPO_URL and COMPONENTS_DIR
DEFAULT_REPO_URL = "https://github.com/basicmachines-co/basic-components.git"
DEFAULT_COMPONENTS_DIR = Path("components/ui")
DEFAULT_BRANCH = "main"

def load_dependencies() -> Dict[str, List[str]]:
    """Load component dependencies from component_dependencies.toml within the package."""
    try:
        with importlib.resources.open_text('basic_components', 'component_dependencies.toml') as f:
            toml_data = tomli.loads(f.read())
            return toml_data.get('dependencies', {})
    except Exception as e:
        console.print(f"[red]Error loading dependencies: {e}[/red]")
        return {}

def normalize_component_name(name: str) -> str:
    """Convert component references to normalized form"""
    # Only normalize if it's an icon reference
    if name.startswith("icons/"):
        # If already in icons/Name format, return as-is
        return name

    if "/" not in name and name != "icons":
        # Handle bare icon names (without icons/ prefix)
        # Convert to PascalCase if needed
        if name.lower() in {"check", "x", "moon", "sun"}:
            return f"icons/{name.title()}"
        # Handle compound names
        if name.lower() in {"chevron-right", "chevron-down", "chevron-up", "chevrons-up-down"}:
            parts = name.split("-")
            pascal_name = "".join(p.title() for p in parts)
            return f"icons/{pascal_name}"

    return name

def get_component_pattern(component: str) -> str:
    """Get the file pattern for a component."""
    if component.startswith("icons/"):
        icon_name = component.split("/")[1]
        return f"icons/{icon_name}Icon.jinja"
    else:
        return f"{component}/**"

def add_component(
        component: str,
        dest_dir: Path,
        repo_url: str = DEFAULT_REPO_URL,
        branch: str = DEFAULT_BRANCH,
        dry_run: bool = False,
) -> None:
    """Add a specific component to the project."""
    try:
        console.print(f"[green]Installing {component}...[/green]")

        # Get the pattern for this component
        pattern = get_component_pattern(component)

        # Build exclude list - exclude everything except our pattern
        excludes = ["*", f"!{pattern}"]

        # Run copier to copy the component
        copier.run_copy(
            src_path=repo_url,
            dst_path=str(dest_dir),
            exclude=excludes,
            vcs_ref=branch,
            pretend=dry_run,
        )

    except Exception as e:
        error_message = str(e)
        if "No files or folders to copy" in error_message or "Nothing to do" in error_message:
            console.print(f"[red]Error: Component '{component}' not found in the repository.[/red]")
        else:
            console.print(f"[red]Error installing {component}: {error_message}[/red]")
        raise typer.Exit(1)

def display_installation_plan(component: str, dependencies: Set[str], dry_run: bool = False) -> None:
    """Display what will be installed in a tree format"""
    tree = Tree(
        f"[bold cyan]{component}[/bold cyan] "
        f"[dim]({'preview' if dry_run else 'will be installed'})[/dim]"
    )

    if dependencies:
        deps_branch = tree.add("[bold yellow]Dependencies[/bold yellow]")
        for dep in sorted(dependencies):
            deps_branch.add(f"[green]{dep}[/green]")

    console.print(tree)

@app.command()
def add(
        component: str = typer.Argument(..., help="Name of the component to install"),
        branch: str = typer.Option(
            DEFAULT_BRANCH, "--branch", "-b", help="Branch, tag, or commit to install from"
        ),
        repo_url: str = typer.Option(
            DEFAULT_REPO_URL, "--repo-url", "-r", help="Repository URL to use"
        ),
        components_dir: Path = typer.Option(
            DEFAULT_COMPONENTS_DIR, "--components-dir", "-d", help="Directory to install components"
        ),
        with_deps: bool = typer.Option(
            True, "--with-deps/--no-deps", help="Install dependencies automatically"
        ),
        dry_run: bool = typer.Option(
            False, "--dry-run", help="Preview what would be installed without making changes"
        )
) -> None:
    """Add a component to your project."""
    try:
        # Load dependencies
        deps_map = load_dependencies()

        # Normalize component name
        component = normalize_component_name(component)

        # Check if component exists in dependencies
        if component not in deps_map:
            console.print(f"[red]Error: Component '{component}' not found.[/red]")
            raise typer.Exit(1)

        # Get all dependencies if requested
        components_to_install = {component}
        if with_deps:
            dependencies = set(deps_map.get(component, []))
            if dependencies:
                components_to_install.update(dependencies)
        else:
            dependencies = set()

        # Display installation plan
        display_installation_plan(component, dependencies, dry_run)

        if dry_run:
            console.print("\n[yellow]Dry run complete. No changes made.[/yellow]")
            return

        # Install each component separately with its own exclude pattern
        installed = []
        for comp in sorted(components_to_install):
            add_component(comp, components_dir, repo_url, branch, dry_run)
            installed.append(comp)

        # Show completion message
        deps_msg = "\n[cyan]Installed dependencies:[/cyan]\n" + "\n".join(
            f"  - {comp}" for comp in installed[1:]
        ) if len(installed) > 1 else ""

        console.print(
            Panel(
                f"[green]✓[/green] Added {component} component{deps_msg}\n\n"
                f"[cyan]components-dir={components_dir}[/cyan]",
                title="Installation Complete",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def init(
        components_dir: Path = typer.Option(
            DEFAULT_COMPONENTS_DIR,
            "--components-dir",
            "-d",
            help="Directory to install components"
        ),
) -> None:
    """Initialize project for basic-components."""
    components_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        Panel(
            "[green]✓[/green] Initialized basic-components\n\n"
            "Directory structure created:\n"
            f"   [cyan]{components_dir}[/cyan]\n\n"
            "Next steps:\n\n"
            "1. Add the cn() utility function:\n"
            "   [cyan]components.basicmachines.co/docs/utilities#cn[/cyan]\n\n"
            "2. Configure JinjaX to use the components directory:\n"
            "   [cyan]components.basicmachines.co/docs/utilities#jinjax[/cyan]\n\n"
            "3. Start adding components:\n"
            "   [cyan]components add button[/cyan]\n\n"
            "View all available components:\n"
            "   [cyan]components.basicmachines.co/docs/components[/cyan]",
            title="Setup Complete",
            border_style="green",
        )
    )

if __name__ == "__main__":
    app()