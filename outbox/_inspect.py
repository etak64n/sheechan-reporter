import json, glob

for f in sorted(glob.glob("outbox/*.json")):
    if f.split("/")[-1].startswith("_"):
        continue
    print("===", f, "===")
    try:
        d = json.load(open(f))
        print("keys:", list(d.keys()))
        print("slug:", d.get("slug"))
        print("title:", d.get("title"))
        print("body_md len:", len(d.get("body_md", "")))
        print("body_md_en len:", len(d.get("body_md_en", "")))
        print("tags:", d.get("tags"))
        print("importance:", d.get("importance"))
        print("emotion:", d.get("emotion"))
        print("published_at:", d.get("published_at"))
        print("source_url:", d.get("source_url"))
        print("og_title:", d.get("og_title"))
    except Exception as e:
        print("ERROR", e)
