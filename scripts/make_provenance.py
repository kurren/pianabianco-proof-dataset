#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

FILES = [
  "proof_map.json",
  "career.json",
  "hire.json",
  "schema-person.jsonld",
  "llms.txt",
  "sitemap.xml",
  "README.md",
  "CITATION.cff",
  "LICENSE",
]

def sha256_file(path: Path) -> str:
  h = hashlib.sha256()
  with path.open("rb") as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b""):
      h.update(chunk)
  return h.hexdigest()

def main():
  root = Path(__file__).resolve().parents[1]
  out = {
    "name": "Proof Dataset — Alessandro L. Piana Bianco",
    "version": "0.1.0",
    "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "algorithm": "SHA-256",
    "files": []
  }

  for rel in FILES:
    p = root / rel
    if not p.exists():
      print(f"Missing: {rel}")
      continue
    out["files"].append({
      "path": rel,
      "bytes": p.stat().st_size,
      "sha256": sha256_file(p)
    })

  (root / "provenance.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
  print("Wrote provenance.json")

if __name__ == "__main__":
  main()
