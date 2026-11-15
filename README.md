# 幻兔 / SnapFlow Privacy Policy

Public bilingual privacy policy for the 幻兔 / SnapFlow app. Only public policy assets belong in this repository. App source, internal documentation and credentials must not be committed here.

GitHub Pages deployment: `main`, repository root.

## Published policy

- Language selector: https://bitlap.org/sf-app-privacy/
- 简体中文: https://bitlap.org/sf-app-privacy/zh-CN.html
- English: https://bitlap.org/sf-app-privacy/en.html

Edit `policies/zh-CN.json` and `policies/en.json` together, preserving section IDs and meaning. Paragraphs are reviewed HTML fragments; only ordinary text and necessary HTTPS/mailto links belong there. Do not add scripts, forms, trackers or private data. Run:

```sh
python3 scripts/build.py
python3 scripts/check.py
```

Commit the generated HTML with the source. Pages serves `main` at the repository root; `.nojekyll` disables Jekyll. No package installation or Actions build workflow is needed. Use a linked issue and squash PR for changes. The bootstrap README is not evidence of a deployed policy: verify Pages and both language URLs after merging.

Contact: dreamylost@outlook.com (the public developer contact also used by iAssets). Publishing a policy does not implement account deletion or certify App Store review compliance. The policy describes the current lack of an in-app self-service account-deletion entry accurately.
