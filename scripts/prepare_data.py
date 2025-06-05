"""Merge multiple *.jsonl files in ./data into a single JSONL.

Usage:
  python prepare_data.py --data_dir data --output_file merged.jsonl
"""

import json, argparse
from pathlib import Path

def main(data_dir: str, output_file: str):
    data_path = Path(data_dir)
    records = []
    for jsonl_file in sorted(data_path.glob("*.jsonl")):
        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"[WARN] {jsonl_file}:{e.pos} -> {e.msg}")
    print(f"Loaded {len(records)} total JSON objects from {data_dir}")
    out_path = Path(output_file)
    with open(out_path, "w", encoding="utf-8") as w:
        for obj in records:
            w.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"Wrote merged file to {out_path.resolve()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data")
    parser.add_argument("--output_file", default="merged.jsonl")
    args = parser.parse_args()
    main(args.data_dir, args.output_file)

