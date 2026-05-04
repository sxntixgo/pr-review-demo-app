# Demo prompts — copy/paste during the talk

Every prompt and command for the four live demos in *Claude Skills for Security* (DC435, 2026-06-05). Open this file on a second monitor or in a tab and copy/paste from it on stage.

---

## Demo 1: Installing a marketplace, a plugin, and a skill

In a fresh Claude Code session.

```
/plugin
```

```
/plugin marketplace add trailofbits/skills
```

```
/plugin menu
```

(Select `differential-review`, install.)

```
What skills do I have available?
```

---

## Demo 2: Defensive pull-request security review

Have one of the open PRs in this repo checked out (`feat/note-detail`, `feat/search`, or `feat/create-note`). In Claude Code, with the repo open and the PR branch checked out:

```
Review this pull request for security issues.
```

If the model needs more direction:

```
Run differential-review against the diff between main and the current branch.
Show every finding with confidence and blast-radius.
```

---

## Demo 3: Offensive GitHub Actions supply-chain audit

In Claude Code, with this repo open. The Trail of Bits marketplace is already added from Demo 1, so only the plugin install is needed:

```
/plugin menu
```

(Select `agentic-actions-auditor`, install.)

Audit the dangerous workflow:

```
Audit .github/workflows/vulnerable.yml for security issues.
```

Audit the safe one:

```
Audit .github/workflows/safe.yml for security issues.
```

(Optional: ask the auditor to compare them.)

```
Compare safe.yml and vulnerable.yml. What is the exploitable difference?
```

---

## Demo 4: Authoring a skill from scratch

The HAR file `demo-assets/sample.har` has six entries with five planted findings.

Install `skill-creator`:

```
/plugin marketplace add anthropics/skills
```

```
/plugin menu
```

(Select `skill-creator`, install.)

Scaffold the new skill:

```
Use skill-creator to scaffold a new skill called har-triage. The skill
should ingest a HAR file and flag: bearer tokens or session cookies sent
to hosts outside the primary origin, API keys or secrets in query
strings, and tracking pixels exfiltrating user identifiers in the URL.
Treat the first request's host as the primary origin.
```

After `skill-creator` writes the SKILL.md, edit the description deliberately too vague:

```
description: Analyzes web traffic.
```

Try the audit prompt and show the skill does not fire:

```
Audit demo-assets/sample.har for credentials leaking to third-party hosts.
```

Tighten the description:

```
description: Audits a HAR export for auth headers, bearer tokens, and
  session identifiers sent to hosts outside the primary origin, plus
  API keys in query strings and tracking pixels exfiltrating user data.
  Use when the user provides a HAR file or asks for a HAR audit.
```

Re-run the same audit prompt. The skill fires this time.

Add a bundled Python script that does the actual JSON walk:

```
Add a script at scripts/triage.py that parses the HAR and returns a
list of findings: each finding has a category (bearer_leak,
api_key_in_querystring, cross_origin_cookie, tracking_pixel_pii),
the host, the URL, and a brief reason. Then update SKILL.md so the
body invokes the script with `python scripts/triage.py <har-file>`
instead of asking the model to walk the JSON itself.
```

Re-run the audit prompt. The output is now sharper, and the model is reasoning over structured findings instead of raw HAR.
