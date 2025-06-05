"""Minimal Mistral‑7B sampling that enforces a schema hint.

Example:
  python mistral_pipeline_example.py --schema schema.json
"""

import argparse, json, textwrap, torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def main(model_name: str, schema_path: str, device: str):
    print(f"Loading {model_name} …")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto" if device == "auto" else None,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        trust_remote_code=True,
    )
    gen = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512, do_sample=True)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    prompt = textwrap.dedent(f"""            You are an AI that outputs JSON objects strictly matching this JSON Schema:
        {json.dumps(schema, indent=2)}

        Respond with one valid JSON object and nothing else.
        """)

    output = gen(prompt)[0]["generated_text"]
    print("\n=== Generated ===\n")
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="mistralai/Mistral-7B-Instruct-v0.2")
    parser.add_argument("--schema", default="schema.json")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu"])
    args = parser.parse_args()
    main(args.model, args.schema, args.device)

