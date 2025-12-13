from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Optional

import click

from md2lang_oai.locale import normalize_and_validate_locale
from md2lang_oai.oai import OpenAIChatCompletionsClient
from md2lang_oai.protect import protect_markdown, restore_markdown


DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"


@dataclass(frozen=True)
class IOPaths:
    input_path: Optional[str]
    output_path: Optional[str]


def _read_all_input(input_path: Optional[str]) -> str:
    if input_path:
        with open(input_path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def _write_all_output(output_path: Optional[str], content: str) -> None:
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return
    sys.stdout.write(content)


def _resolve_api_key(env_name: str) -> str:
    value = os.environ.get(env_name)
    if not value:
        raise click.ClickException(
            f"Missing API key: environment variable {env_name!r} is not set."
        )
    return value


def _version() -> str:
    try:
        from importlib.metadata import version

        return version("md2lang-oai")
    except Exception:
        from md2lang_oai import __version__

        return __version__


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=_version(), prog_name="md2lang-oai")
@click.option("--to", "to_locale", required=True, metavar="LOCALE", help="Target locale: xx or xx-YY (e.g. es or es-ES).")
@click.option("--input", "input_path", type=click.Path(dir_okay=False, path_type=str), default=None, help="Read input from a file instead of stdin.")
@click.option("-o", "--output", "output_path", type=click.Path(dir_okay=False, path_type=str), default=None, help="Write output to a file instead of stdout.")
@click.option("--model", default=DEFAULT_MODEL, show_default=True, help="Chat Completions model name.")
@click.option("--base-url", default=DEFAULT_BASE_URL, show_default=True, help="OpenAI-compatible base URL (e.g. https://api.openai.com/v1).")
@click.option("--api-key-env", default=DEFAULT_API_KEY_ENV, show_default=True, help="Environment variable name holding the API key.")
def main(
    to_locale: str,
    input_path: Optional[str],
    output_path: Optional[str],
    model: str,
    base_url: str,
    api_key_env: str,
) -> None:
    """Translate Markdown/text into a target locale (pipe-friendly)."""

    try:
        locale = normalize_and_validate_locale(to_locale)
    except ValueError as e:
        raise click.ClickException(str(e)) from e
    api_key = _resolve_api_key(api_key_env)

    raw = _read_all_input(input_path)

    protected, mapping = protect_markdown(raw)

    client = OpenAIChatCompletionsClient(base_url=base_url, api_key=api_key)
    try:
        translated = client.translate(text=protected, to_locale=locale, model=model)
    except Exception as e:
        raise click.ClickException(str(e)) from e

    restored = restore_markdown(translated, mapping)

    _write_all_output(output_path, restored)
