# md2lang-oai

Minimal CLI that translates Markdown/text into a target locale using an OpenAI-compatible **Chat Completions** HTTP endpoint.

## Install / run (uv)

Run without installing:

```bash
uv run md2lang-oai --help
```

## Usage

Translate from stdin to stdout:

```bash
echo "Hello" | uv run md2lang-oai --to es-ES
```

Translate a file:

```bash
uv run md2lang-oai --to es-ES --input README.md
```

Write to a file:

```bash
uv run md2lang-oai --to es-ES --input input.md --output output.md
```

Pipe-friendly (stdin):

```bash
cat input.md | uv run md2lang-oai --to es-ES > output.md
```

## Configuration

- API key is read from `OPENAI_API_KEY` by default.
- Choose a different env var name with `--api-key-env`.
- Override the endpoint with `--base-url` (must be OpenAI-compatible).
- Choose a model with `--model`.

Example:

```bash
export OPENAI_API_KEY="..."
uv run md2lang-oai --to es-ES --model gpt-4o-mini --base-url https://api.openai.com/v1 < input.md
```

## Markdown handling

The tool preserves Markdown structure as much as possible:

- Does **not** translate inside fenced code blocks (`...`).
- Does **not** translate inline code spans (`like this`).
- Keeps link/image syntax intact; URLs are never translated.

## Development

Run tests:

```bash
uv run pytest
```
