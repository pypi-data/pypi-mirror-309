"""Main CLI interface."""

from __future__ import annotations

from pathlib import Path

import click
from fmf import Tree

from .. import __version__
from ..template import TemplateContext


@click.group("fmf-jinja")
@click.version_option(__version__, message="%(version)s")
@click.option(
    "-r",
    "--root",
    metavar="PATH",
    type=Path,
    default=".",
    show_default=True,
    help="Path to the fmf tree root",
)
@click.pass_context
def main(ctx: click.Context, root: Path) -> None:
    """
    FMF-Jinja template generator.

    \f

    :param ctx: click context
    :param root: fmf tree root path
    """  # noqa: D301
    ctx.ensure_object(dict)
    ctx.obj["tree"] = Tree(root)


@main.command()
@click.option(
    "-o",
    "--output",
    metavar="PATH",
    type=Path,
    default=".",
    show_default=True,
    help="Path to generated output directory",
)
@click.option(
    "--recursive/--no-recursive",
    default=True,
    help="Re-run the generator if any fmf file is generated",
)
@click.pass_context
def generate(ctx: click.Context, output: Path, recursive: bool) -> None:  # noqa: FBT001
    """
    Generate template output.

    \f

    :param ctx: click context
    :param output: output path
    :param recursive: run recursively
    """  # noqa: D301
    template_ctx = TemplateContext(
        tree_root=ctx.obj["tree"],
        recursive=recursive,
    )
    template_ctx.generate(output)
