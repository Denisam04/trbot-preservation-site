# TrBot Preservation public website

Original, dependency-free static HTML/CSS. Contains public application information only. Never copy private project artifacts, credentials, archive objects or internal logs into this repository.

## Deployment

Cloudflare Pages Git integration: production branch `main`, build command `python3 validate.py`, output directory `public`. Disable automatic preview deployments for unreviewed branches. Run validation and review the exact diff before merging a pull request into main. Cloudflare must not receive access to unrelated private repositories.

## Local check

Run `python validate.py`, then `python -m http.server 8080 --directory public` for a local preview. The validator does not prove absence of every secret; human review is required before publication.
