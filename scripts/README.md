# AI Data Pipeline Scripts

A lean collection of helper scripts to take raw `.jsonl` lyric/metadata files, derive a JSON Schema, and run Mistral‑7B in a Transformers pipeline that respects that schema.

## Folder structure

```
.
├── data/                # Put your *.jsonl files here
├── prepare_data.py      # Merge / sanity‑check data
├── generate_schema.py   # Builds schema.json from data
├── mistral_pipeline_example.py
├── requirements.txt
└── README.md
```

## Quick‑start

```bash
# 1.  Clone your repo and drop JSONL inside ./data
git clone <your‑repo>
cd <your‑repo>

# 2.  Install deps (CUDA 11.8+ recommended for fp16)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3.  Merge & validate data (optional)
python prepare_data.py --data_dir data --output_file merged.jsonl

# 4.  Auto‑build a schema from the merged set
python generate_schema.py --input_file merged.jsonl --output_file schema.json

# 5.  Fire up Mistral‑7B and sample
python mistral_pipeline_example.py --schema schema.json
```

All scripts are pure‑Python and self‑contained; no notebook fluff.  Adjust paths via CLI flags.

## Notes
- `generate_schema.py` uses the *genson* library for  quick heuristic schema derivation.
- The Mistral example loads `mistralai/Mistral-7B-Instruct-v0.2`; switch `--model` if you run a local quantised copy (e.g. with `pipeline(..., model="TheBloke/Mistral-7B-Instruct-GGUF")`).
- If you are on CPU‑only hardware, set `--device cpu` or export `CUDA_VISIBLE_DEVICES=""`, but expect painfully slow generation.

