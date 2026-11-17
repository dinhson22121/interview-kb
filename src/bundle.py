"""Build index.html from src/: python3 src/build.py && python3 src/bundle.py (run inside src/)."""
import json, urllib.request, pathlib
here = pathlib.Path(__file__).parent
data = (here / 'data.json').read_text(encoding='utf-8').replace('</', '<\\/')
marked_path = here / 'node_modules/marked/marked.min.js'
marked = marked_path.read_text(encoding='utf-8').replace('</script', '<\\/script')
t = (here / 'template.html').read_text(encoding='utf-8')
t = t.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>', '<script>' + marked + '</script>')
(here.parent / 'index.html').write_text(t.replace('__DATA__', data), encoding='utf-8')
print('index.html written')
