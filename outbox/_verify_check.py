import json, re

REQUIRED = ["slug","title","summary","body_md","title_en","summary_en","body_md_en","emotion","importance","source_url","source_name","og_title","tags","published_at"]
VALID_TAGS = {"aws","cloudflare","openai","anthropic","microsoft","ai","ai-safety","security","infrastructure","serverless","devops","web","business","science"}
VALID_EMOTIONS = {"happy","energetic","thinking","smug","confused"}

files = [
  "outbox/aws-what-s-new-kiro-opus-sonnet-monitoring-launch-aws-govcloud-us.json",
  "outbox/aws-what-s-new-amazon-ses-simplified-smtp-mail-manager.json",
]

for f in files:
    d = json.load(open(f))
    missing = [k for k in REQUIRED if k not in d]
    print(f)
    print(" missing fields:", missing)
    print(" tags valid:", all(t in VALID_TAGS for t in d["tags"]), d["tags"])
    print(" emotion valid:", d["emotion"] in VALID_EMOTIONS, d["emotion"])
    print(" importance:", d["importance"], type(d["importance"]))
    for field in ["body_md","body_md_en"]:
        text = d[field]
        html_hits = re.findall(r'<[a-zA-Z/]', text)
        bad_schemes = re.findall(r'(javascript|data|vbscript):', text)
        print("  ", field, "len=", len(text), "html_tags=", html_hits, "bad_schemes=", bad_schemes)
    print(" title len", len(d["title"]), "summary len", len(d["summary"]))
    print()
