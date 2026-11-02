"""Render selected author guides into the static companion without a JS framework."""
from pathlib import Path
import mistune
root=Path(__file__).resolve().parents[1]
for name,target in [('assessment','assessment'),('h5p-guide','h5p-guide'),('sources','sources')]:
    html=mistune.html((root/f'docs/{name}.md').read_text(encoding='utf-8'))
    (root/f'website/dist/{target}.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+name.replace('-',' ').title()+' — Quantum Lab</title><link rel="stylesheet" href="style.css"></head><body><header><a class="brand" href="index.html">ψ / APPLIED QUANTUM LAB</a><a href="index.html">Back to the course ↗</a></header><main class="document">'+html+'</main></body></html>',encoding='utf-8')
