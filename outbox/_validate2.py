import json, glob

required = {'slug','title','summary','body_md','title_en','summary_en','body_md_en','emotion','importance','source_url','source_name','og_title','tags','published_at'}

for f in sorted(glob.glob('outbox/*.json')):
    if '_' in f.split('/')[-1][0:1]:
        continue
    try:
        d = json.load(open(f))
    except Exception as e:
        print(f, 'ERROR', e)
        continue
    keys = set(d.keys())
    missing = required - keys
    extra = keys - required
    print(f)
    print('  missing:', missing, 'extra:', extra)
    print('  slug:', d.get('slug'))
    print('  title:', d.get('title'))
    print('  importance:', d.get('importance'), 'emotion:', d.get('emotion'), 'tags:', d.get('tags'))
    print('  body_md len:', len(d.get('body_md','')), 'body_md_en len:', len(d.get('body_md_en','')))
    print('  published_at:', d.get('published_at'))
