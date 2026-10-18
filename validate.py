"""Fail closed on unintended deploy files, broken internal links and secret patterns."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
root=Path(__file__).parent/'public'
expected={'index.html','styles.css','_headers','robots.txt','privacy/index.html','terms/index.html','contact/index.html','404.html'}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual==expected, f'Deploy file allowlist mismatch: {actual^expected}'
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  assert tag not in {'script','iframe','form'},'Unexpected active content'
  for k in ('href','src'):
   v=a.get(k,'');u=urlsplit(v)
   if v.startswith('/'):
    p=root/u.path.lstrip('/')
    assert p.is_file() or (p/'index.html').is_file(),f'Broken link: {v}'
for p in root.rglob('*'):
 if not p.is_file():continue
 text=p.read_text(encoding='utf-8')
 assert not re.search(r'[A-Za-z0-9._%+-]+@(?:gmail|yahoo|outlook|hotmail)\.[A-Za-z.]+',text,re.I),'Personal mailbox must not be deployed'
 assert not re.search(r'-----BEGIN .*PRIVATE KEY|AIza[\w-]{30,}|gh[pousr]_[A-Za-z0-9]{20,}|GOCSPX-|ya29\.|C:\\Users\\|/home/denis|TODO_CONTACT',text),'Sensitive or unfinished content'
 if p.suffix=='.html':
  assert '<meta name="viewport"' in text and '<title>' in text
  Links().feed(text)
print(f'PASS: {len(actual)} deploy files; static-only, internal links and targeted content checks')
