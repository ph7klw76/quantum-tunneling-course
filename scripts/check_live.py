"""Verify the actual deployment URL and key public resources over HTTPS."""
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin

base=os.environ.get('SITE_URL','https://ph7klw76.github.io/quantum-tunneling-course/').rstrip('/')+'/'
publication=json.loads((Path(__file__).resolve().parents[1]/'course/publication_config.json').read_text(encoding='utf-8'))
assert base.startswith('https://ph7klw76.github.io/quantum-tunneling-course/')
paths=['','config.js','quizzes.json','lecture.srt','h5p/quantum-tunneling.html','h5p/question-1.html','h5p/Quantum_Tunneling_Interactive.h5p','lab/lab/index.html','lab/files/Quantum_Tunneling_Lab.ipynb','assessment.html']
results=[]
for path in paths:
    for attempt in range(12):
        try:
            with urlopen(Request(urljoin(base,path),headers={'User-Agent':'Quantum-course-deployment-check'}),timeout=30) as response:
                body=response.read()
                assert response.status==200 and body
                if path=='config.js':assert publication['active_youtube_url'].encode() in body
                if path=='h5p/quantum-tunneling.html':assert b'H5PIntegration' in body
                if path.endswith('.ipynb'):assert json.loads(body)['nbformat']==4
                results.append(dict(path=path or '/',status=response.status,bytes=len(body)))
                break
        except Exception:
            if attempt==11:raise
            time.sleep(5)
print(json.dumps(dict(url=base,resources=results),indent=2))
