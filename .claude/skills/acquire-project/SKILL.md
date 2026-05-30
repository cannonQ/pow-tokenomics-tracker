---
name: acquire-project
description: End-to-end agent-driven acquisition of one PoW project's tokenomics data. Classifies the project, dispatches research subagents in parallel to gather non-homogenous data from the web, reviews and merges their findings, computes derived fields, runs validation, and presents to a human for approval on the project's own branch before submitting a PR. Invoke as /acquire-project <name>.
---

# /acquire-project &lt;name&gt;

You are the **primary/orchestrator agent**. Subagents gather data; you review, merge, validate, and
present it to the human for approval. Work strictly through the five checkpoints below — each is a
**gate**: do not advance until its pass criteria are met, and on failure do the stated recovery rather
than fudging data to move on.

`<name>` is the lowercase project id (e.g. `kaspa`, `ergo`). If omitted, ask for it.

Read `docs/DATA_FIELDS.md` first — it defines what to find, the source map, and source priority.

---

## CP1 — Classify + branch
1. Determine `consensus` and `launch_type` from a quick whitepaper/CoinGecko lookup (you may use
   WebSearch/WebFetch directly here).
2. Using the conditional matrix in `docs/DATA_FIELDS.md`, decide which files are needed
   (`data/projects/<name>.json` always; `allocations/<name>/genesis.json` if premine/forensic;
   vesting/emission CSV if applicable) and which subagents to dispatch.
3. Put the work on the project's **own branch** so it stays isolated from other coins:
   ```bash
   git fetch origin && git checkout -B coin/<name> origin/HEAD   # reuse existing coin/<name> for refreshes
   mkdir -p .acquisition
   ```
4. Identity fields (`project, ticker, consensus, algorithm, launch_date, launch_type, has_premine`)
   are yours to fill now.

**Gate:** working tree is on `coin/<name>`; `launch_type` fixed; the required field set + file list +
subagent list are printed. **Fail:** if `launch_type` is ambiguous, ask the human (AskUserQuestion).

## CP2 — Gather (fan out subagents in parallel)
Dispatch the applicable subagents **in a single message with multiple Agent calls** so they run
concurrently. Always: `supply-emission-researcher`, `market-data-researcher`.
Conditionally: `allocation-researcher` (premine/ICO/private_sale), `forensics-researcher` (suspicion /
missing data / dev_tax / treasury_emission, and the Analysis-tab `red_flags`/`transparency_notes` for
any premined project). Pass each the project name, ticker, and the evidence path
`.acquisition/<name>.evidence.json`.

(There is intentionally **no mining researcher** — the site renders no mining data; see
`docs/DATA_FIELDS.md`.)

**Gate:** every required field for this `launch_type` has a candidate value **with a `source_url`**, or
is explicitly `null`/`"unknown"` with a `notes` reason. **Fail:** re-dispatch the relevant subagent
with a narrower instruction for the missing fields.

## CP3 — Review & merge (this is your core job)
1. Collect all subagent outputs into `.acquisition/<name>.evidence.json` (field → value, source_url,
   confidence, notes).
2. **Cross-check overlaps** (e.g. current_supply may appear from supply and market subagents) — they
   must agree; resolve conflicts using the **source priority** in `docs/DATA_FIELDS.md` and record the
   discrepancy in notes.
3. Downgrade any value lacking a real `source_url` to `confidence: low` and flag it.
4. Produce a **coverage report**: fields filled / sourced / unknown.

**Gate:** no unresolved value conflicts; coverage report produced. **Fail:** send a follow-up to the
subagent that owns the disputed/missing field.

## CP4 — Assemble + validate (deterministic gate)
1. Write `data/projects/<name>.json` from the merged findings, mirroring
   `templates/project-template.json` field-for-field — **with no `_comment` keys**. Aggregate all
   source URLs into `data_sources`. Set `last_updated` to today.
2. If premine/forensic: write `allocations/<name>/genesis.json` (mirror `genesis-template.json`); if
   vesting/emission CSVs were produced, convert them:
   `python scripts/csv_to_vesting_json.py <name>` / `python scripts/csv_to_emission_json.py <name>`.
3. **Compute derived fields** — never by hand:
   ```bash
   python scripts/compute_derived.py <name>
   ```
4. **Run the gate:**
   ```bash
   python scripts/validate_submission.py <name>
   ```

**Gate:** `validate_submission.py` exits 0 (no errors). **Fail:** read the error — if it's a sourced
data problem, loop back to CP2/CP3 to re-research the offending field; if it's a math/derived problem,
re-run `compute_derived.py`. **Never** edit a number purely to satisfy the validator.

## CP5 — Human approval → submit
1. Write the provenance sidecar `allocations/<name>/.sources.json` (or
   `data/projects/<name>.sources.json` for fair launches): every non-derived field → `{source_url,
   confidence}`.
2. Present to the human: the **coverage report**, a **field / value / source / confidence table**, the
   `git diff`, and a plain-language statement of confidence and remaining gaps. Then **stop**.
3. On explicit approval, submit this one coin:
   ```bash
   git add data/projects/<name>.json allocations/<name>/ data/projects/<name>.sources.json 2>/dev/null
   git commit -m "Add/update <name> tokenomics data"
   git push -u origin coin/<name>
   ```
   Then open a PR for `coin/<name>` (one PR per coin) — its **submitted** state for human
   review/checks. **Do not** write to or merge into the default branch; merging the PR is the human's
   call.

**Gate:** human approved before any commit/push. **Fail/decline:** leave the branch unpushed and apply
the requested edits, then re-run from the appropriate checkpoint.

---

## Notes
- One branch per coin keeps coins independent — a single coin can be cut, reworked, or refreshed
  without touching others. Refreshes reuse `coin/<name>`.
- `.acquisition/` holds scratch evidence/CSVs; it is not part of the dataset (gitignore it or leave it
  uncommitted).
- Honesty over completeness: `null`/`"unknown"` + a reason always beats an unsourced guess.
