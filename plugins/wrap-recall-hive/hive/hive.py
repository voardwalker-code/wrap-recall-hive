#!/usr/bin/env python3
"""hive.py — seat-neutral hivemind memory search (/hive).

Read-only. No writes to any pack.
Each coding seat owns its wrap pack; this tool searches registered roots
with hard attribution so the active seat can reason through foreign memory.

Usage:
  python3 hive.py --list-owners
  python3 hive.py --focus "peer MA seed"
  python3 hive.py --focus "inject" --from agent-b
  python3 hive.py --focus "bug-id" --budget-chars 80000

Env:
  HIVE_REGISTRY  override path to registry.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ~4 chars ≈ 1 token; 30k tokens ≈ 120k chars sweet spot
DEFAULT_BUDGET_CHARS = 120_000
CEILING_CHARS = 200_000

SECRET_NAME_RE = re.compile(
    r"(auth\.json|credentials|\.env|secret|api[_-]?key|token\.json|private[_-]?key)",
    re.I,
)

RECALL_SECTION_RE = re.compile(
    r"(?ms)^## Recall\s*\n(.*?)(?=^## |\Z)"
)


def expand(p: str, base: Path | None = None) -> Path:
    """Expand ~ and resolve. Relative paths resolve against *base* (registry dir) then cwd."""
    if p.startswith("~"):
        return Path(os.path.expanduser(p)).resolve()
    path = Path(p)
    if path.is_absolute():
        return path.resolve()
    if base is not None:
        cand = (base / path).resolve()
        if cand.exists():
            return cand
        # also try base's parent (repo root when registry lives in examples/ or hive/)
        cand2 = (base.parent / path).resolve()
        if cand2.exists():
            return cand2
    return path.resolve()


def load_registry(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def tokenize(focus: str) -> list[str]:
    # keep short tokens; drop pure noise
    raw = re.findall(r"[a-zA-Z0-9_./+-]{2,}", focus.lower())
    stop = {"the", "and", "for", "from", "with", "what", "that", "this", "into", "about"}
    return [t for t in raw if t not in stop]


@dataclass
class Hit:
    owner: str
    kind: str  # spine | recall | worklog | board | ledger | shared | file
    path: Path
    when: str  # filename date-ish or mtime iso date
    score: float
    status: str = "unknown"
    body: str = ""
    title: str = ""

    def envelope(self) -> str:
        rel = str(self.path)
        header = (
            f"### [memory owner={self.owner} kind={self.kind} "
            f"when={self.when} status={self.status} not_me=true]\n"
            f"<source>{rel}</source>\n"
        )
        if self.title:
            header += f"**{self.title}**\n\n"
        return header + self.body.strip() + "\n"


def extract_recall(text: str) -> str | None:
    m = RECALL_SECTION_RE.search(text)
    if not m:
        return None
    body = m.group(1).strip()
    return body if body else None


def guess_when(path: Path) -> str:
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", path.name)
    if m:
        return m.group(1)
    try:
        return path.stat().st_mtime_ns and __import__("datetime").datetime.fromtimestamp(
            path.stat().st_mtime
        ).strftime("%Y-%m-%d")
    except OSError:
        return "unknown"


def score_text(text: str, name: str, tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    low = text.lower()
    nlow = name.lower()
    score = 0.0
    for t in tokens:
        if t in nlow:
            score += 8.0
        # filename slug fragments
        if t.replace("-", "") in nlow.replace("-", ""):
            score += 2.0
        c = low.count(t)
        if c:
            score += min(c, 12) * 1.5
        # heading-ish boost
        if re.search(rf"(?im)^#{{1,3}}.*{re.escape(t)}", text):
            score += 4.0
    return score


def read_text(path: Path, max_bytes: int = 400_000) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="replace")
    except OSError:
        return ""


def iter_coding_pack_files(owner: dict, base: Path | None = None) -> Iterable[tuple[str, Path]]:
    root = expand(owner["root"], base=base)
    if not root.exists():
        return
    layers = owner.get("layers") or {}
    spine = layers.get("spine")
    if spine:
        p = root / spine
        if p.is_file():
            yield "spine", p
    journal = layers.get("journal")
    if journal:
        jdir = root / journal
        if jdir.is_dir():
            for p in sorted(jdir.glob("*.md"), reverse=True):
                if p.is_file() and not SECRET_NAME_RE.search(p.name):
                    yield "journal", p
    worklog = layers.get("worklog")
    if worklog:
        wdir = root / worklog
        if wdir.is_dir():
            for p in sorted(wdir.glob("*.md"), reverse=True):
                if p.is_file() and not SECRET_NAME_RE.search(p.name):
                    yield "worklog", p


def collect_hits(
    registry: dict,
    tokens: list[str],
    owner_filter: str | None,
    include_own: str | None,
    base: Path | None = None,
) -> list[Hit]:
    hits: list[Hit] = []
    for owner in registry.get("owners") or []:
        oid = owner["id"]
        if owner_filter and oid != owner_filter and not oid.startswith(owner_filter):
            # allow prefix: from:agent-b matches agent-b
            if owner_filter not in oid:
                continue
        # hive default: search everyone; include_own is just documentation for skill
        _ = include_own

        kind_root = owner.get("kind", "file")
        root = expand(owner["root"], base=base)

        if kind_root in ("shared-correspondence", "shared-work") or root.is_file():
            if not root.is_file():
                continue
            if SECRET_NAME_RE.search(root.name):
                continue
            text = read_text(root)
            sc = score_text(text, root.name, tokens) if tokens else 1.0
            if tokens and sc <= 0:
                continue
            # shared files: take relevant chunks if long
            body = text
            if len(body) > 12_000 and tokens:
                body = extract_matching_chunks(text, tokens, max_chars=8_000)
            hits.append(
                Hit(
                    owner=oid,
                    kind="board" if "board" in oid else ("ledger" if "ledger" in oid else "shared"),
                    path=root,
                    when=guess_when(root),
                    score=sc + 0.5,  # slight shared boost when matched
                    status="shared",
                    body=body,
                    title=root.name,
                )
            )
            continue

        if kind_root == "coding-pack" or owner.get("layers"):
            for layer, path in iter_coding_pack_files(owner, base=base):
                text = read_text(path)
                sc = score_text(text, path.name, tokens) if tokens else 0.0
                if layer == "spine" and tokens:
                    # spines only if they hit — avoid dumping every relationship file
                    if sc < 4.0:
                        continue
                elif layer != "spine" and tokens and sc <= 0:
                    continue
                elif not tokens:
                    # no focus: only recent journals (top by name) — handled later
                    if layer != "journal":
                        continue
                    sc = 1.0

                if layer == "journal":
                    recall = extract_recall(text)
                    body = recall if recall else text[:6000]
                    kind = "recall" if recall else "file"
                    # status heuristic
                    status = "unknown"
                    low = text.lower()
                    if "status:** done" in low or "**status:** done" in low or "status: done" in low:
                        status = "done"
                    elif "partial" in low[:2000]:
                        status = "partial"
                    hits.append(
                        Hit(
                            owner=oid,
                            kind=kind,
                            path=path,
                            when=guess_when(path),
                            score=sc + (3.0 if recall else 0.0),
                            status=status,
                            body=body,
                            title=path.stem,
                        )
                    )
                elif layer == "worklog":
                    body = extract_matching_chunks(text, tokens, max_chars=6_000) if tokens else text[-4000:]
                    if tokens and not body.strip():
                        continue
                    hits.append(
                        Hit(
                            owner=oid,
                            kind="worklog",
                            path=path,
                            when=guess_when(path),
                            score=sc,
                            status="worklog",
                            body=body,
                            title=path.name,
                        )
                    )
                elif layer == "spine":
                    body = extract_matching_chunks(text, tokens, max_chars=5_000) if tokens else text[:4000]
                    hits.append(
                        Hit(
                            owner=oid,
                            kind="spine",
                            path=path,
                            when=guess_when(path),
                            score=sc,
                            status="spine",
                            body=body,
                            title=f"{oid} spine",
                        )
                    )
    return hits


def extract_matching_chunks(text: str, tokens: list[str], max_chars: int = 6000) -> str:
    if not tokens:
        return text[:max_chars]
    lines = text.splitlines()
    keep_idx: set[int] = set()
    for i, line in enumerate(lines):
        low = line.lower()
        if any(t in low for t in tokens):
            for j in range(max(0, i - 3), min(len(lines), i + 8)):
                keep_idx.add(j)
    if not keep_idx:
        return ""
    # also keep ### headers near kept lines
    out_lines = []
    for i in sorted(keep_idx):
        out_lines.append(lines[i])
    body = "\n".join(out_lines)
    if len(body) > max_chars:
        body = body[:max_chars] + "\n…[truncated]"
    return body


def assemble(hits: list[Hit], budget: int, focus: str) -> tuple[str, list[Hit], list[Hit]]:
    hits_sorted = sorted(hits, key=lambda h: (-h.score, h.when, h.owner), reverse=False)
    # sort score desc
    hits_sorted = sorted(hits, key=lambda h: (-h.score, h.when))

    # de-dupe path
    seen: set[str] = set()
    unique: list[Hit] = []
    for h in hits_sorted:
        key = str(h.path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(h)

    header = (
        "# Hive assembly (not your memories)\n\n"
        f"**Focus:** {focus or '(none — recent journal hits only)'}\n"
        f"**Law:** Every span below is labeled. `not_me=true` = evidence, not autobiography.\n"
        f"**Tool:** wrap-recall-hive (seat-neutral). Wrap/recall unchanged.\n\n"
        "---\n\n"
    )
    used = len(header)
    taken: list[Hit] = []
    dropped: list[Hit] = []
    parts = [header]

    for h in unique:
        block = h.envelope() + "\n---\n\n"
        if used + len(block) > budget and taken:
            dropped.append(h)
            continue
        if used + len(block) > budget and not taken:
            # always take at least a truncated first hit
            room = max(500, budget - used - 200)
            h.body = h.body[:room] + "\n…[truncated to fit budget]"
            block = h.envelope() + "\n---\n\n"
        parts.append(block)
        used += len(block)
        taken.append(h)

    report = (
        f"\n## Hive report\n\n"
        f"- **Hits taken:** {len(taken)}\n"
        f"- **Hits dropped (budget):** {len(dropped)}\n"
        f"- **Approx chars:** {used}\n"
        f"- **Owners:** {', '.join(sorted({h.owner for h in taken})) or '(none)'}\n"
        f"- **Paths:**\n"
    )
    for h in taken:
        report += f"  - `{h.owner}` {h.kind} {h.path.name} (score={h.score:.1f})\n"
    if dropped:
        report += "- **Dropped:**\n"
        for h in dropped[:20]:
            report += f"  - `{h.owner}` {h.path.name} (score={h.score:.1f})\n"
        if len(dropped) > 20:
            report += f"  - …and {len(dropped) - 20} more\n"

    return "".join(parts) + report, taken, dropped


def default_registry_path() -> Path:
    env = os.environ.get("HIVE_REGISTRY")
    if env:
        return expand(env)
    return Path(__file__).resolve().parent / "registry.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Hivemind memory search (/hive) — read-only")
    ap.add_argument("--focus", "-f", default="", help="Search stub / focus note")
    ap.add_argument("--from", dest="owner_from", default=None, help="Filter owner id (e.g. codex, claude)")
    ap.add_argument("--budget-chars", type=int, default=DEFAULT_BUDGET_CHARS)
    ap.add_argument("--registry", type=str, default=None)
    ap.add_argument("--list-owners", action="store_true")
    ap.add_argument(
        "--include-own",
        default=None,
        help="Optional: active seat id (documentation only; hive still labels all spans not_me)",
    )
    args = ap.parse_args(argv)

    reg_path = expand(args.registry) if args.registry else default_registry_path()
    if not reg_path.is_file():
        print(f"error: registry not found: {reg_path}", file=sys.stderr)
        return 2

    registry = load_registry(reg_path)

    if args.list_owners:
        print(f"# Hive registry: {reg_path}\n")
        for o in registry.get("owners") or []:
            root = expand(o["root"], base=reg_path.parent)
            exists = "ok" if root.exists() else "MISSING"
            print(f"- {o['id']:16} kind={o.get('kind','?'):22} {exists:7} {root}")
        return 0

    budget = max(4_000, min(args.budget_chars, CEILING_CHARS))
    tokens = tokenize(args.focus)
    reg_base = reg_path.parent
    hits = collect_hits(registry, tokens, args.owner_from, args.include_own, base=reg_base)

    if not hits and not tokens:
        # no focus: take newest journal recall per owner (max 2 each)
        tokens = []  # explicit
        # re-collect with empty tokens only journals scored 1.0 — then keep top by when
        hits = collect_hits(registry, [], args.owner_from, args.include_own, base=reg_base)
        hits = sorted(hits, key=lambda h: h.when, reverse=True)[:12]

    if not hits:
        print(
            f"# Hive assembly\n\n**Focus:** {args.focus or '(none)'}\n\n"
            "No hits. Try a different stub, or `--list-owners` to verify pack paths.\n"
            f"Registry: `{reg_path}`\n"
        )
        return 0

    text, _taken, _dropped = assemble(hits, budget, args.focus)
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
