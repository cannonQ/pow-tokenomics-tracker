# Adding a Project with Claude Code

The repository ships with a [Claude Code](https://claude.com/claude-code) skill
(`/acquire-project`) that runs the full data-gathering, validation, and
PR-submission pipeline for one project. You review and approve before anything
is committed.

The skill is the **fast path**. It produces the same files as the manual flow
described in [CONTRIBUTING.md](../CONTRIBUTING.md), passes the same
`scripts/validate_submission.py` gate, and follows the same data conventions in
[`docs/DATA_FIELDS.md`](DATA_FIELDS.md).

## Prerequisites

1. **Claude Code installed**
   - CLI: `npm install -g @anthropic-ai/claude-code`
   - or the VS Code / JetBrains extension
2. **Anthropic account** with API/subscription access. One coin run typically
   spends a few hundred thousand tokens across the orchestrator and four
   research subagents.
3. **Python 3.7+** for `scripts/validate_submission.py`,
   `scripts/compute_derived.py`, and `scripts/csv_to_vesting_json.py`. Pure
   stdlib — no `pip install` required.
4. **`gh` CLI** authenticated against your fork if you want the skill to push
   the branch and open the PR for you. (Without it, the skill stops after
   producing the local commit and you push manually.)

## Run

From the repository root:

```text
/acquire-project <lowercase-project-slug>
```

Examples: `/acquire-project kaspa`, `/acquire-project ergo`,
`/acquire-project new-coin`.

For a brand-new project, the slug is whatever you want the entry on the site
to be — it becomes the filename (`data/projects/<slug>.json`) and the
`project` field. For a refresh of an existing entry, use the same slug
already in `data/projects/`.

## What happens

The skill walks five checkpoints. You can interrupt at any of them.

| CP | What it does | What you see |
|---|---|---|
| **CP1** | Classifies the project (consensus, launch type), creates `coin/<slug>` branch | Skill prints the classification and asks if `launch_type` is ambiguous |
| **CP2** | Dispatches research subagents in parallel — `supply-emission-researcher`, `market-data-researcher`, `allocation-researcher` (premined only), `forensics-researcher` (premined/suspicious only) | Subagent outputs land in `.acquisition/<slug>.*.json` (gitignored scratch) |
| **CP3** | Cross-checks subagent findings, resolves source conflicts, produces a coverage report | Coverage table printed |
| **CP4** | Writes `data/projects/<slug>.json`, `allocations/<slug>/genesis.json` (if premine), runs `compute_derived.py`, runs `validate_submission.py` | Validator must exit 0 to advance |
| **CP5** | Prints field/value/source/confidence table + `git diff`. **Stops for your approval.** On approval, commits and pushes `coin/<slug>` and opens a PR | You read, you say yes/no |

Nothing lands on `main` automatically. The PR is the deliverable.

## Honesty conventions

The skill is built to **leave a value `null` or `"unknown"` with a sourced
reason rather than guess**. If a researcher can't find a verifiable figure,
that's what shows up in the output — not a fabricated number. Validator and
human review are the gates, not optimism.

Mirror this when reviewing: don't ask the skill to "fill in" a number that
doesn't have a primary source. Add it later when you have one.

## What the skill won't do

- **Auto-merge.** PRs are opened, never merged.
- **Bypass the validator.** A CP4 failure loops back to CP2/CP3 to re-research
  the offending field, not to edit numbers into compliance.
- **Touch other coins.** Each run is scoped to one slug on one branch.
- **Research fields the site doesn't render.** Hashrate, mining hardware,
  pool concentration, cost-to-mine are explicitly *not* gathered (see
  `docs/DATA_FIELDS.md`).

## When the manual flow is better

- You already have the data and just want to drop it in — `QUICK_START.md` is
  faster than waiting for subagents to find things you can paste in.
- The project has unusual structure that requires editorial framing the
  agents won't produce (genuinely novel emission models, hybrid launches,
  forensic deep-dives with proprietary on-chain analysis).
- You're offline or want zero API spend.

## Troubleshooting

- **Skill doesn't appear:** confirm `.claude/skills/acquire-project/SKILL.md`
  exists at the repo root in your clone. The skill is repo-local; it loads
  when Claude Code opens the directory.
- **Subagents not found:** confirm `.claude/agents/*.md` exists. Same loading
  mechanism.
- **Validator fails on a math field:** never edit the number to make it pass.
  Re-run `scripts/compute_derived.py <slug>` first; if it still fails, the
  source data is wrong and CP2/CP3 needs to re-research it.
- **`gh` not authenticated:** the skill will produce the local commit and
  stop. Run `gh auth login` once, then `git push -u origin coin/<slug>` and
  `gh pr create` manually.
