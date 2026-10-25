# Diagram sources

Each `dN.py` builds one SVG in `docs/diagrams/` using the helpers in `lib.py`. Regenerate after changing a skill:

```sh
cd docs/diagrams/src && for d in d1 d2 d3 d4 d5; do python3 "$d.py"; done
```

| Script | Output |
|---|---|
| `d1.py` | `overview.svg` |
| `d2.py` | `flow-work-phases.svg` |
| `d3.py` | `branching.svg` |
| `d4.py` | `orchestrator.svg` |
| `d5.py` | `knowledge.svg` |
