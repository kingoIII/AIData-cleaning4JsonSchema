"""Derive a JSON Schema from a sample JSONL using genson.

Usage:
  python generate_schema.py --input_file merged.jsonl --output_file schema.json
"""

import json, argparse
from genson import SchemaBuilder

def main(input_file: str, output_file: str):
    builder = SchemaBuilder()
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                builder.add_object(json.loads(line))
    schema = builder.to_schema(with_schema_version=True)
    with open(output_file, "w", encoding="utf-8") as w:
        json.dump(schema, w, indent=2, ensure_ascii=False)
    print(f"Schema with {len(schema.get('properties', {}))} properties written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default="merged.jsonl")
    parser.add_argument("--output_file", default="schema.json")
    args = parser.parse_args()
    main(args.input_file, args.output_file)

