# sheechan-reporter

`sources.json` に定義したテックブログ(初期: AWS / Anthropic / OpenAI / Cloudflare)を監視し、
新着記事の紹介記事を Claude Code(サブスク枠)で生成して
[blog.sheechan.etak64n.dev](https://blog.sheechan.etak64n.dev) に全自動入稿する bot。

## 仕組み

```
GitHub Actions (cron 6時間おき)
  ├─ scripts/check_feeds.py   … RSS×3 + Anthropic sitemap を state/seen.json と差分(LLM不使用)
  ├─ claude-code-action       … prompts/generate.md に従い outbox/*.json を生成(setup-token / サブスク枠)
  ├─ scripts/post_articles.py … OIDC トークンで POST → 成功分を seen に追加し articles/ へアーカイブ
  └─ git commit               … state と記事アーカイブを永続化
```

- 新着ゼロの回は Claude を起動しないので、サブスク利用枠を消費しない
- 投稿に失敗した記事は既読にならず、次回の実行で自動リトライされる
- `articles/` が全入稿記事のアーカイブ = ブログ D1 のバックアップ(全件再 POST で復元可能)

## セットアップ

1. このリポジトリを `etak64n/sheechan-reporter` として GitHub に push(ブログ側の
   `ALLOWED_OIDC_SUB` が `repo:etak64n/sheechan-reporter:ref:refs/heads/main` 固定のため、
   リポジトリ名を変える場合はブログ側 wrangler.jsonc も変更する)
2. 手元で `claude setup-token` を実行し、出力されたトークンをリポジトリ Secret
   `CLAUDE_CODE_OAUTH_TOKEN` に登録(Pro/Max サブスクで有効。期限 1 年)
3. 初回の既読状態はコミット済み(`state/seen.json`)。以降の新着だけが投稿される
4. 手動実行: Actions タブ → watch → Run workflow

## 監視サイトの追加

1. `sources.json` にエントリを1つ足す:

   ```json
   { "name": "GitHub", "type": "atom", "url": "https://github.blog/feed/" }
   ```

   - `type` は `rss` / `atom` / `sitemap` の3種。`sitemap` の場合は記事URLの共通パスを
     `include_path` に指定する(例: Anthropic の `"/news/"`)
   - `name` はブログにそのまま表示されるソース名
2. ブログ側 `wrangler.jsonc` の `ALLOWED_SOURCE_HOSTS` に新サイトのドメインを足して deploy
3. push するだけ。**追加直後の実行でそのサイトの過去記事が一斉投稿されることはない**
   (未ブートストラップのソースは現時点の記事を既読化し、次の新着から拾う)

ソースの削除は sources.json から消すだけ。`state/seen.json` に残る履歴は無害。

## 記事の取り消し

ブログ側 README を参照(`DELETE /api/articles/:slug`)。取り消した記事を再投稿させたくない場合は
`state/seen.json` に URL が残っていることを確認する(残っていれば再生成されない)。

## ローカルでの動作確認

```sh
python3 scripts/check_feeds.py            # work/new_articles.json を確認
BLOG_DEV_TOKEN=xxx BLOG_API_URL=http://localhost:8787 python3 scripts/post_articles.py
# ブログ側は .dev.vars に DEV_BEARER_TOKEN=xxx を置いて wrangler dev
```
