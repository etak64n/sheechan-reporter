import json
d = json.load(open('outbox/openai-introducing-genebench-pro.json'))
print('OK', list(d.keys()))
print('title len', len(d['title']))
print('summary len', len(d['summary']))
print('body_md len', len(d['body_md']))
print('tags', d['tags'])
