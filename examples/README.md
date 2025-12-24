# Example with local model qwen2.5:7b

Enable large context with (or set max-tokens to 4K):
```bash
ollama create qwen2.5-large -f ./Modelfile
```

```bash
export OPENAI_API_KEY=test   
input="./dnd_sample.md"                          
output="${input%.md}-es.md"
uv run md2lang-oai --to es-ES \
  --model qwen2.5-large \
  --base-url http://localhost:11434/v1 \
  --max-tokens 10000 \
  --timeout 600 \
  --input "$input" \
  --instructions-file ./dnd_instructions.txt \
  --output "$output"
```
