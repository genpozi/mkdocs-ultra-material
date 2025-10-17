"""CLI commands for MkDocs AI Assistant."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown

from .generation.prompt import PromptGenerator
from .providers import get_provider, ProviderError
from .cache import CacheManager
from .enhancement import (
    EnhancementPipeline,
    EnhancementOptions,
    EnhancementConfig
)

console = Console()


@click.group()
@click.version_option(package_name="mkdocs-ai-assistant")
def main():
    """MkDocs AI Assistant - AI-powered documentation generation."""
    pass


@main.command()
@click.argument("prompt")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: auto-generated in docs/generated/)",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--model",
    "-m",
    help="Model to use (provider-specific)",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key (or set via environment variable)",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Disable caching for this generation",
)
@click.option(
    "--template",
    "-t",
    type=click.Path(exists=True),
    help="Use a Jinja2 template file",
)
@click.option(
    "--context",
    "-c",
    multiple=True,
    help="Template context variables (key=value)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def generate(
    prompt: str,
    output: Optional[str],
    provider: str,
    model: Optional[str],
    api_key: Optional[str],
    no_cache: bool,
    template: Optional[str],
    context: tuple[str, ...],
    verbose: bool,
):
    """Generate documentation from a prompt.
    
    Examples:
    
        # Basic generation
        mkdocs ai generate "Create a guide to Docker Compose"
        
        # Specify output file
        mkdocs ai generate "Kubernetes basics" -o docs/k8s.md
        
        # Use specific model
        mkdocs ai generate "API docs" -m anthropic/claude-3-opus
        
        # Use template
        mkdocs ai generate "API reference" -t templates/api.md.j2
        
        # With context variables
        mkdocs ai generate "Service docs" -t templates/service.md.j2 -c name=auth -c version=2.0
    """
    asyncio.run(_generate_async(
        prompt=prompt,
        output=output,
        provider=provider,
        model=model,
        api_key=api_key,
        no_cache=no_cache,
        template=template,
        context=context,
        verbose=verbose,
    ))


async def _generate_async(
    prompt: str,
    output: Optional[str],
    provider: str,
    model: Optional[str],
    api_key: Optional[str],
    no_cache: bool,
    template: Optional[str],
    context: tuple[str, ...],
    verbose: bool,
):
    """Async implementation of generate command."""
    
    # Show header
    console.print(Panel.fit(
        "[bold cyan]MkDocs AI Assistant[/bold cyan]\n"
        "[dim]Document Generation[/dim]",
        border_style="cyan",
    ))
    
    # Parse context variables
    context_dict = {}
    for ctx in context:
        if "=" not in ctx:
            console.print(f"[red]Error:[/red] Invalid context format: {ctx}")
            console.print("Use: -c key=value")
            sys.exit(1)
        key, value = ctx.split("=", 1)
        context_dict[key] = value
    
    # Initialize provider
    try:
        provider_config = {
            "name": provider,
            "api_key": api_key,
            "model": model,
        }
        
        ai_provider = get_provider(provider_config)
        ai_provider.validate_config()
        
        if verbose:
            console.print(f"[dim]Provider: {provider}[/dim]")
            console.print(f"[dim]Model: {model or ai_provider.model}[/dim]")
        
    except ProviderError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    
    # Initialize cache
    cache_manager = None
    if not no_cache:
        try:
            cache_manager = CacheManager(cache_dir=".ai-cache")
            if verbose:
                console.print("[dim]Cache: enabled[/dim]")
        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Cache initialization failed: {e}")
    
    # Initialize generator
    generator = PromptGenerator(
        provider=ai_provider,
        cache_manager=cache_manager,
    )
    
    # Determine output path
    if not output:
        # Auto-generate filename from prompt
        filename = _sanitize_filename(prompt[:50]) + ".md"
        output_path = Path("docs/generated") / filename
    else:
        output_path = Path(output)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        console.print(f"[dim]Output: {output_path}[/dim]")
    
    # Generate content
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating content...", total=None)
            
            if template:
                content = await generator.generate_from_template(
                    template_path=template,
                    context=context_dict,
                    prompt=prompt,
                )
            else:
                content = await generator.generate_from_prompt(prompt)
            
            progress.update(task, completed=True)
        
        # Write to file
        output_path.write_text(content, encoding="utf-8")
        
        # Show success
        console.print()
        console.print(f"[green]✓[/green] Generated: [bold]{output_path}[/bold]")
        
        # Show preview
        if verbose:
            console.print()
            console.print(Panel(
                Markdown(content[:500] + ("..." if len(content) > 500 else "")),
                title="Preview",
                border_style="green",
            ))
        
        # Show stats
        console.print()
        console.print(f"[dim]Length: {len(content)} characters[/dim]")
        if cache_manager:
            stats = cache_manager.get_stats()
            console.print(f"[dim]Cache: {stats['hits']} hits, {stats['misses']} misses[/dim]")
        
    except ProviderError as e:
        console.print()
        console.print(f"[red]Error:[/red] Generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        console.print()
        console.print(f"[red]Error:[/red] Unexpected error: {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)
    finally:
        if cache_manager:
            cache_manager.close()


def _sanitize_filename(text: str) -> str:
    """Convert text to safe filename."""
    # Remove special characters
    safe = "".join(c if c.isalnum() or c in " -_" else "" for c in text)
    # Replace spaces with hyphens
    safe = safe.replace(" ", "-")
    # Remove multiple hyphens
    while "--" in safe:
        safe = safe.replace("--", "-")
    # Lowercase
    safe = safe.lower()
    # Remove leading/trailing hyphens
    safe = safe.strip("-")
    return safe or "generated"


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="mkdocs.yml",
    help="Path to mkdocs.yml",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def batch(config: str, verbose: bool):
    """Generate documents from config file tasks.
    
    Reads generation tasks from mkdocs.yml and processes them in batch.
    
    Example mkdocs.yml:
    
        plugins:
          - ai-assistant:
              generation:
                tasks:
                  - prompt: "Create API docs"
                    output: docs/api.md
                  - prompt: "Write tutorial"
                    output: docs/tutorial.md
    """
    console.print("[yellow]Batch generation not yet implemented[/yellow]")
    console.print("Coming in next update!")
    # TODO: Implement batch generation


@main.command()
def cache_stats():
    """Show cache statistics."""
    try:
        cache_manager = CacheManager(cache_dir=".ai-cache")
        stats = cache_manager.get_stats()
        
        console.print(Panel.fit(
            f"[bold]Cache Statistics[/bold]\n\n"
            f"Entries: {stats['count']}\n"
            f"Size: {stats['size'] / 1024 / 1024:.2f} MB\n"
            f"Hits: {stats['hits']}\n"
            f"Misses: {stats['misses']}\n"
            f"Hit Rate: {stats['hits'] / max(stats['hits'] + stats['misses'], 1) * 100:.1f}%",
            border_style="cyan",
        ))
        
        cache_manager.close()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.confirmation_option(prompt="Are you sure you want to clear the cache?")
def cache_clear():
    """Clear the cache."""
    try:
        cache_manager = CacheManager(cache_dir=".ai-cache")
        cache_manager.clear()
        console.print("[green]✓[/green] Cache cleared")
        cache_manager.close()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--preview",
    is_flag=True,
    help="Preview changes without applying",
)
@click.option(
    "--apply",
    is_flag=True,
    help="Apply changes to file",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive mode (review each change)",
)
@click.option(
    "--grammar",
    is_flag=True,
    help="Enable grammar enhancement",
)
@click.option(
    "--clarity",
    is_flag=True,
    help="Enable clarity enhancement",
)
@click.option(
    "--consistency",
    is_flag=True,
    help="Enable consistency checking",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key for provider",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def enhance(
    file_path: str,
    preview: bool,
    apply: bool,
    interactive: bool,
    grammar: bool,
    clarity: bool,
    consistency: bool,
    provider: str,
    api_key: Optional[str],
    verbose: bool
):
    """Enhance existing documentation.
    
    Improves grammar, clarity, and terminology consistency while preserving
    technical content (code blocks, frontmatter, etc.).
    
    Examples:
    
        # Preview changes
        mkdocs-ai enhance docs/guide.md --preview
        
        # Apply all enhancements
        mkdocs-ai enhance docs/guide.md --apply --grammar --clarity --consistency
        
        # Interactive mode
        mkdocs-ai enhance docs/guide.md --interactive
    """
    # If no specific features selected, enable all
    if not (grammar or clarity or consistency):
        grammar = clarity = consistency = True
    
    # Check API key
    if not api_key:
        console.print("[red]Error: API key required[/red]")
        console.print("Set OPENROUTER_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    try:
        # Initialize provider and cache
        ai_provider = get_provider(provider, api_key=api_key)
        cache_manager = CacheManager(cache_dir=".ai-cache")
        
        # Create enhancement pipeline
        config = EnhancementConfig(
            enabled=True,
            provider=provider,
            temperature=0.3
        )
        pipeline = EnhancementPipeline(ai_provider, cache_manager, config)
        
        # Create options
        options = EnhancementOptions(
            grammar=grammar,
            clarity=clarity,
            consistency=consistency,
            temperature=0.3
        )
        
        # Enhance file
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Enhancing {file_path}...", total=None)
            
            result = asyncio.run(pipeline.enhance_file(file_path, options))
            
            progress.update(task, completed=True)
        
        # Display results
        if not result.has_changes:
            console.print("[green]✓[/green] No changes needed - document is already well-written!")
            return
        
        console.print(f"\n[bold]Found {result.change_count} potential improvements:[/bold]\n")
        console.print(result.summary())
        
        # Show changes by type
        from .enhancement import ChangeType
        
        for change_type in ChangeType:
            type_changes = result.changes_by_type(change_type)
            if type_changes:
                console.print(f"\n[bold]{change_type.value.capitalize()}:[/bold]")
                for i, change in enumerate(type_changes[:5], 1):  # Show first 5
                    console.print(f"  {i}. {change}")
                if len(type_changes) > 5:
                    console.print(f"  ... and {len(type_changes) - 5} more")
        
        # Preview mode
        if preview or interactive:
            console.print("\n[bold]Diff:[/bold]")
            console.print(result.diff)
        
        # Interactive mode
        if interactive:
            console.print()
            response = click.prompt(
                "Apply changes? [y/n/d(iff)]",
                type=str,
                default="n"
            )
            
            if response.lower() == 'd':
                console.print(result.diff)
                response = click.prompt("Apply changes? [y/n]", type=str, default="n")
            
            if response.lower() == 'y':
                apply = True
        
        # Apply changes
        if apply:
            pipeline.apply_enhancement(file_path, result)
            console.print(f"\n[green]✓[/green] Applied {result.change_count} changes to {file_path}")
        elif not preview and not interactive:
            console.print("\n[yellow]Use --apply to save changes or --preview to see diff[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
