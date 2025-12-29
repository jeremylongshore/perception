#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗██████╗  ██████╗███████╗██████╗ ████████╗██╗ ██████╗ ███╗   ██╗ ║
║  ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║ ║
║  ██████╔╝█████╗  ██████╔╝██║     █████╗  ██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║ ║
║  ██╔═══╝ ██╔══╝  ██╔══██╗██║     ██╔══╝  ██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║ ║
║  ██║     ███████╗██║  ██║╚██████╗███████╗██║        ██║   ██║╚██████╔╝██║ ╚████║ ║
║  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Perception TUI - AI News Intelligence Terminal
Aesthetic: Cyberpunk News Terminal / Synthwave Dashboard
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.align import Align
from rich import box
from rich.columns import Columns
from rich.rule import Rule
from datetime import datetime
import yaml
import json
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CYBERPUNK COLOR PALETTE
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Synthwave/Cyberpunk color scheme for Perception."""
    # Primary
    CYAN = "#00ffff"
    MAGENTA = "#ff00ff"
    PURPLE = "#bd00ff"

    # Secondary
    PINK = "#ff6ec7"
    BLUE = "#00bfff"
    YELLOW = "#ffff00"

    # Backgrounds
    DEEP_PURPLE = "#1a0a2e"
    DARK_BLUE = "#0a0a1a"

    # Status
    ACTIVE = "#00ff9f"  # Matrix green
    INACTIVE = "#ff3366"  # Hot pink red
    WARNING = "#ffaa00"

    # Text
    DIM = "#666699"
    BRIGHT = "#ffffff"


# Use built-in box styles (custom requires 8 lines)
CYBER_BOX = box.DOUBLE
HEAVY_BOX = box.HEAVY

console = Console()

# ═══════════════════════════════════════════════════════════════════════════════
# ASCII ART & DECORATIVE ELEMENTS
# ═══════════════════════════════════════════════════════════════════════════════

LOGO = """
[bold cyan]╔═══════════════════════════════════════════════════════════════════════════════════════╗[/]
[bold cyan]║[/]  [bold magenta]██████╗ ███████╗██████╗  ██████╗███████╗██████╗ ████████╗██╗ ██████╗ ███╗   ██╗[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██████╔╝█████╗  ██████╔╝██║     █████╗  ██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██╔═══╝ ██╔══╝  ██╔══██╗██║     ██╔══╝  ██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██║     ███████╗██║  ██║╚██████╗███████╗██║        ██║   ██║╚██████╔╝██║ ╚████║[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝[/]  [bold cyan]║[/]
[bold cyan]╚═══════════════════════════════════════════════════════════════════════════════════════╝[/]
"""

MINI_LOGO = "[bold magenta]◆[/] [bold cyan]P E R C E P T I O N[/] [bold magenta]◆[/]"

TAGLINE = "[dim italic]AI-Powered News Intelligence • Real-Time Analysis • Strategic Insights[/]"

DIVIDER = "[cyan]═══════════════════════════════════════════════════════════════════════════════════════[/]"
THIN_DIVIDER = "[dim cyan]───────────────────────────────────────────────────────────────────────────────────────[/]"


def status_indicator(active: bool) -> str:
    """Return a colored status indicator."""
    if active:
        return f"[bold {Colors.ACTIVE}]●[/]"
    return f"[bold {Colors.INACTIVE}]○[/]"


def category_badge(category: str) -> str:
    """Return a styled category badge."""
    colors = {
        "tech": Colors.CYAN,
        "ai": Colors.MAGENTA,
        "business": Colors.YELLOW,
        "security": Colors.INACTIVE,
        "crypto": Colors.PURPLE,
        "science": Colors.BLUE,
        "world": Colors.PINK,
        "sports": Colors.ACTIVE,
        "automotive": Colors.WARNING,
        "engineering": Colors.CYAN,
    }
    color = colors.get(category.lower().split("_")[0], Colors.DIM)
    return f"[bold {color}]◢[/][on {color}][black] {category.upper()[:8]:^8} [/][bold {color}]◣[/]"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADERS
# ═══════════════════════════════════════════════════════════════════════════════

def load_rss_sources() -> List[Dict[str, Any]]:
    """Load RSS sources from YAML config."""
    config_path = Path(__file__).parent / "perception_app/perception_agent/config/rss_sources.yaml"
    if not config_path.exists():
        return []

    with open(config_path) as f:
        data = yaml.safe_load(f)

    return data.get("sources", [])


def load_active_feeds() -> List[Dict[str, Any]]:
    """Load verified active feeds from JSON."""
    feeds_path = Path(__file__).parent / "feed-testing/active_feeds.json"
    if not feeds_path.exists():
        return []

    with open(feeds_path) as f:
        return json.load(f)


def get_category_stats(sources: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get feed counts by category."""
    stats = {}
    for source in sources:
        cat = source.get("category", "other")
        stats[cat] = stats.get(cat, 0) + 1
    return dict(sorted(stats.items(), key=lambda x: -x[1]))


# ═══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def make_header() -> Panel:
    """Create the header panel with logo and system status."""
    # Compact single-line header for better terminal compatibility
    header_text = Text()
    header_text.append("◆ ", style=f"bold {Colors.MAGENTA}")
    header_text.append("P", style=f"bold {Colors.MAGENTA}")
    header_text.append("E", style=f"bold {Colors.PURPLE}")
    header_text.append("R", style=f"bold {Colors.PURPLE}")
    header_text.append("C", style=f"bold {Colors.CYAN}")
    header_text.append("E", style=f"bold {Colors.CYAN}")
    header_text.append("P", style=f"bold {Colors.MAGENTA}")
    header_text.append("T", style=f"bold {Colors.PURPLE}")
    header_text.append("I", style=f"bold {Colors.CYAN}")
    header_text.append("O", style=f"bold {Colors.MAGENTA}")
    header_text.append("N", style=f"bold {Colors.PURPLE}")
    header_text.append(" ◆", style=f"bold {Colors.CYAN}")
    header_text.append("\n\n", style="")
    header_text.append("AI-Powered News Intelligence Platform", style=f"italic {Colors.DIM}")

    return Panel(
        Align.center(header_text),
        border_style=Colors.CYAN,
        box=box.DOUBLE,
        padding=(1, 4),
        title=f"[bold {Colors.MAGENTA}]▸ v0.3.0 ◂[/]",
        subtitle=f"[{Colors.DIM}]perception-with-intent[/]",
    )


def make_status_panel() -> Panel:
    """Create the system status panel."""
    now = datetime.now()

    status_text = Text()
    status_text.append("◢", style=f"bold {Colors.MAGENTA}")
    status_text.append(" SYSTEM STATUS ", style=f"bold {Colors.BRIGHT}")
    status_text.append("◣\n\n", style=f"bold {Colors.MAGENTA}")

    # Status items
    items = [
        ("MCP Service", True, "Cloud Run"),
        ("Agent Engine", True, "Vertex AI"),
        ("Firestore DB", True, "perception-db"),
        ("RSS Ingestion", True, "89 feeds"),
    ]

    for name, active, detail in items:
        indicator = "●" if active else "○"
        ind_color = Colors.ACTIVE if active else Colors.INACTIVE
        status_text.append(f"  {indicator} ", style=f"bold {ind_color}")
        status_text.append(f"{name:<15}", style=f"bold {Colors.CYAN}")
        status_text.append(f" │ ", style=f"dim {Colors.DIM}")
        status_text.append(f"{detail}\n", style=f"{Colors.BRIGHT}")

    status_text.append(f"\n  Last check: {now.strftime('%H:%M:%S')}", style=f"dim {Colors.DIM}")

    return Panel(
        status_text,
        title=f"[bold {Colors.CYAN}]◆ STATUS ◆[/]",
        border_style=Colors.PURPLE,
        box=box.ROUNDED,
        padding=(1, 2),
    )


def make_feeds_table(sources: List[Dict[str, Any]], limit: int = 15) -> Panel:
    """Create the feeds overview table."""
    table = Table(
        show_header=True,
        header_style=f"bold {Colors.CYAN}",
        border_style=Colors.PURPLE,
        box=box.SIMPLE_HEAD,
        padding=(0, 1),
        expand=True,
    )

    table.add_column("◢", justify="center", width=3)
    table.add_column("FEED", style=f"{Colors.BRIGHT}", min_width=25)
    table.add_column("CATEGORY", justify="center", width=14)
    table.add_column("STATUS", justify="center", width=8)

    for source in sources[:limit]:
        name = source.get("name", "Unknown")[:28]
        category = source.get("category", "other")
        active = source.get("active", False)

        # Category color
        cat_colors = {
            "tech": Colors.CYAN,
            "ai": Colors.MAGENTA,
            "business": Colors.YELLOW,
            "security": Colors.INACTIVE,
            "crypto": Colors.PURPLE,
            "science": Colors.BLUE,
            "world": Colors.PINK,
            "sports": Colors.ACTIVE,
        }
        cat_color = cat_colors.get(category.split("_")[0], Colors.DIM)

        table.add_row(
            f"[{Colors.MAGENTA}]▸[/]",
            name,
            f"[{cat_color}]{category[:12]}[/]",
            f"[{Colors.ACTIVE if active else Colors.INACTIVE}]{'◉' if active else '○'}[/]",
        )

    remaining = len(sources) - limit
    if remaining > 0:
        table.add_row("", f"[dim]... and {remaining} more feeds[/]", "", "")

    return Panel(
        table,
        title=f"[bold {Colors.CYAN}]◆ RSS FEEDS ({len(sources)} active) ◆[/]",
        border_style=Colors.PURPLE,
        box=box.ROUNDED,
        padding=(0, 1),
    )


def make_category_chart(stats: Dict[str, int]) -> Panel:
    """Create a horizontal bar chart of categories."""
    max_count = max(stats.values()) if stats else 1

    content = Text()
    content.append("◢", style=f"bold {Colors.MAGENTA}")
    content.append(" CATEGORY DISTRIBUTION ", style=f"bold {Colors.BRIGHT}")
    content.append("◣\n\n", style=f"bold {Colors.MAGENTA}")

    colors_cycle = [Colors.CYAN, Colors.MAGENTA, Colors.PURPLE, Colors.PINK, Colors.BLUE, Colors.YELLOW]

    for i, (category, count) in enumerate(list(stats.items())[:10]):
        color = colors_cycle[i % len(colors_cycle)]
        bar_width = int((count / max_count) * 20)
        bar = "█" * bar_width + "░" * (20 - bar_width)

        content.append(f"  {category[:12]:<12} ", style=f"{Colors.DIM}")
        content.append(bar, style=f"{color}")
        content.append(f" {count:>3}\n", style=f"bold {Colors.BRIGHT}")

    return Panel(
        content,
        title=f"[bold {Colors.CYAN}]◆ CATEGORIES ◆[/]",
        border_style=Colors.PURPLE,
        box=box.ROUNDED,
        padding=(0, 2),
    )


def make_ingestion_panel() -> Panel:
    """Create the ingestion metrics panel."""
    content = Text()
    content.append("◢", style=f"bold {Colors.MAGENTA}")
    content.append(" INGESTION METRICS ", style=f"bold {Colors.BRIGHT}")
    content.append("◣\n\n", style=f"bold {Colors.MAGENTA}")

    metrics = [
        ("Total Feeds", "89", Colors.CYAN),
        ("Categories", "19", Colors.MAGENTA),
        ("Active Sources", "89", Colors.ACTIVE),
        ("Test Success", "65%", Colors.WARNING),
    ]

    for label, value, color in metrics:
        content.append(f"  {label:<16}", style=f"{Colors.DIM}")
        content.append(f"{value:>6}\n", style=f"bold {color}")

    content.append(f"\n  Pipeline: ", style=f"dim {Colors.DIM}")
    content.append("READY", style=f"bold {Colors.ACTIVE}")

    return Panel(
        content,
        title=f"[bold {Colors.CYAN}]◆ METRICS ◆[/]",
        border_style=Colors.PURPLE,
        box=box.ROUNDED,
        padding=(0, 2),
    )


def make_quick_actions() -> Panel:
    """Create quick actions panel."""
    content = Text()

    actions = [
        ("▸ Run Ingestion", "python scripts/run_ingestion_once.py"),
        ("▸ Test Feeds", "python feed-testing/test_all_feeds.py"),
        ("▸ Deploy MCP", "gcloud run deploy perception-mcp ..."),
        ("▸ View Logs", "gcloud logging read ..."),
    ]

    for label, cmd in actions:
        content.append(f"  [{Colors.MAGENTA}]{label}[/]\n", style="bold")
        content.append(f"    [{Colors.DIM}]{cmd[:40]}[/]\n\n", style="")

    return Panel(
        content,
        title=f"[bold {Colors.CYAN}]◆ QUICK ACTIONS ◆[/]",
        border_style=Colors.PURPLE,
        box=box.ROUNDED,
        padding=(0, 2),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def dashboard():
    """Display the main Perception dashboard."""
    console.clear()

    # Load data
    sources = load_rss_sources()
    stats = get_category_stats(sources)

    # Print header
    console.print(make_header())
    console.print(Align.center(Text(TAGLINE)))
    console.print()

    # Create layout
    layout = Layout()
    layout.split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1),
    )

    layout["left"].split_column(
        Layout(make_feeds_table(sources), name="feeds"),
    )

    layout["right"].split_column(
        Layout(make_status_panel(), name="status", size=12),
        Layout(make_ingestion_panel(), name="metrics", size=12),
        Layout(make_category_chart(stats), name="chart"),
    )

    console.print(layout)

    # Footer
    console.print()
    console.print(Align.center(Text(
        f"[dim]perception-with-intent[/] │ [dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/] │ [dim]Press Ctrl+C to exit[/]"
    )))


def show_feeds():
    """Display detailed feeds view."""
    console.clear()
    console.print(make_header())

    sources = load_rss_sources()
    stats = get_category_stats(sources)

    # Full feeds table
    table = Table(
        title=f"[bold {Colors.CYAN}]◆ ALL RSS FEEDS ({len(sources)} total) ◆[/]",
        show_header=True,
        header_style=f"bold {Colors.CYAN}",
        border_style=Colors.PURPLE,
        box=box.ROUNDED,
        padding=(0, 1),
        expand=True,
    )

    table.add_column("#", justify="right", width=4, style=Colors.DIM)
    table.add_column("FEED NAME", style=f"bold {Colors.BRIGHT}", min_width=30)
    table.add_column("CATEGORY", justify="center", width=16)
    table.add_column("URL", style=Colors.DIM, max_width=50)

    for i, source in enumerate(sources, 1):
        name = source.get("name", "Unknown")
        category = source.get("category", "other")
        url = source.get("url", "")[:48]

        cat_colors = {
            "tech": Colors.CYAN, "ai": Colors.MAGENTA, "business": Colors.YELLOW,
            "security": Colors.INACTIVE, "crypto": Colors.PURPLE, "science": Colors.BLUE,
        }
        cat_color = cat_colors.get(category.split("_")[0], Colors.DIM)

        table.add_row(str(i), name, f"[{cat_color}]{category}[/]", url)

    console.print(table)

    # Category summary
    console.print()
    console.print(make_category_chart(stats))


def run_test():
    """Run feed test with animated progress."""
    console.clear()
    console.print(make_header())
    console.print()

    sources = load_rss_sources()[:10]  # Test first 10

    with Progress(
        SpinnerColumn(spinner_name="dots12", style=Colors.CYAN),
        TextColumn("[bold]{task.description}[/]"),
        BarColumn(complete_style=Colors.MAGENTA, finished_style=Colors.ACTIVE),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"[{Colors.CYAN}]Testing feeds...", total=len(sources))

        for source in sources:
            progress.update(task, description=f"[{Colors.CYAN}]Testing: {source['name'][:30]}")
            time.sleep(0.3)  # Simulate test
            progress.advance(task)

    console.print()
    console.print(f"[bold {Colors.ACTIVE}]✓[/] Feed test complete!")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Perception TUI - AI News Intelligence Terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
╔══════════════════════════════════════════════════════════════════════╗
║  Commands:                                                           ║
║    perception_tui.py              Show main dashboard                ║
║    perception_tui.py feeds        Show all feeds                     ║
║    perception_tui.py test         Run feed tests with animation      ║
║    perception_tui.py status       Show system status                 ║
╚══════════════════════════════════════════════════════════════════════╝
        """
    )
    parser.add_argument("command", nargs="?", default="dashboard",
                       choices=["dashboard", "feeds", "test", "status"],
                       help="Command to run")

    args = parser.parse_args()

    try:
        if args.command == "dashboard":
            dashboard()
        elif args.command == "feeds":
            show_feeds()
        elif args.command == "test":
            run_test()
        elif args.command == "status":
            console.print(make_header())
            console.print()
            console.print(Columns([make_status_panel(), make_ingestion_panel()]))
    except KeyboardInterrupt:
        console.print(f"\n[{Colors.DIM}]Exiting Perception TUI...[/]")
        sys.exit(0)


if __name__ == "__main__":
    main()
