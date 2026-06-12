#!/usr/bin/env python3
"""Synchronise le bloc commun des CLAUDE.md du groupe Nuances.

Source de vérité : common.md (à côté de ce script).
Cible : le CLAUDE.md de chaque repo `nu-ances` (siblings dans le conteneur
nuances-ops) + le CLAUDE.md racine du conteneur (loader local).

Le bloc commun est délimité par des marqueurs ; seul ce bloc est réécrit, le
contenu spécifique de chaque repo est préservé.

Usage :
    sync-claude-md.py            # écrit / met à jour le bloc commun partout
    sync-claude-md.py --check    # vérifie la dérive (exit 1 si divergence) — pour la CI
    sync-claude-md.py --list     # liste les cibles détectées
"""
import sys
from pathlib import Path

START = "<!-- COMMON:START — bloc généré, NE PAS ÉDITER (source : nu-ances/claude-rules) -->"
END = "<!-- COMMON:END -->"

SCRIPT_DIR = Path(__file__).resolve().parent
COMMON_FILE = SCRIPT_DIR / "common.md"
CONTAINER = SCRIPT_DIR.parent  # claude-rules -> nuances-ops

STUB_SPECIFIC = "## Règles spécifiques à ce repo\n\n_(à compléter)_\n"


def common_block() -> str:
    body = COMMON_FILE.read_text(encoding="utf-8").strip()
    return f"{START}\n{body}\n{END}"


def find_repos(root: Path) -> list[Path]:
    """Tous les repos git sous root (récursif), sans descendre dans un repo."""
    repos = []

    def walk(d: Path) -> None:
        for child in sorted(d.iterdir()):
            if not child.is_dir() or child.name == ".git":
                continue
            if (child / ".git").exists():
                repos.append(child)  # frontière de repo : on n'y descend pas
            else:
                walk(child)

    walk(root)
    return repos


def targets() -> list[Path]:
    """CLAUDE.md du conteneur + de chaque repo git découvert (récursif)."""
    return [CONTAINER / "CLAUDE.md"] + [r / "CLAUDE.md" for r in find_repos(CONTAINER)]


def extract_block(text: str) -> str | None:
    if START not in text or END not in text:
        return None
    pre, rest = text.split(START, 1)
    block, _ = rest.split(END, 1)
    return block.strip()


def render(existing: str | None) -> str:
    block = common_block()
    if existing and START in existing and END in existing:
        pre, rest = existing.split(START, 1)
        _, post = rest.split(END, 1)
        return f"{pre}{block}{post}"
    # Pas de marqueurs : on préfixe le bloc commun, on garde l'existant en dessous.
    tail = existing.strip() if existing else STUB_SPECIFIC
    return f"{block}\n\n{tail}\n"


def check_one(claude_md: Path, canonical: str) -> int:
    """Vérifie un seul CLAUDE.md (mode CI : un repo isolé, hors conteneur)."""
    if not claude_md.exists():
        print(f"✗ {claude_md} — ABSENT")
        return 1
    block = extract_block(claude_md.read_text(encoding="utf-8"))
    if block is None:
        print(f"✗ {claude_md} — pas de marqueurs COMMON")
        return 1
    if block != canonical:
        print(f"✗ {claude_md} — bloc commun DÉRIVÉ (lancer sync-claude-md.py)")
        return 1
    print(f"✓ {claude_md}")
    return 0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--write"
    # Filtre optionnel : ne traiter que les cibles dont le chemin commence par cet argument.
    filt = sys.argv[2] if len(sys.argv) > 2 else None
    canonical = COMMON_FILE.read_text(encoding="utf-8").strip()

    # Mode CI : vérifie un fichier explicite, sans dépendre de la structure conteneur.
    if mode == "--check-one":
        if not filt:
            print("usage: sync-claude-md.py --check-one <chemin/CLAUDE.md>")
            return 2
        return check_one(Path(filt), canonical)

    drift = 0

    for path in targets():
        rel = path.relative_to(CONTAINER)
        if filt and not str(rel).startswith(filt):
            continue
        existing = path.read_text(encoding="utf-8") if path.exists() else None

        if mode == "--list":
            print(rel)
            continue

        if mode == "--check":
            block = extract_block(existing) if existing else None
            if existing is None:
                print(f"✗ {rel} — ABSENT")
                drift = 1
            elif block is None:
                print(f"✗ {rel} — pas de marqueurs COMMON")
                drift = 1
            elif block != canonical:
                print(f"✗ {rel} — bloc commun DÉRIVÉ")
                drift = 1
            else:
                print(f"✓ {rel}")
            continue

        # --write
        new = render(existing)
        if new != (existing or ""):
            path.write_text(new, encoding="utf-8")
            print(f"~ {rel} — {'créé' if existing is None else 'mis à jour'}")
        else:
            print(f"= {rel} — inchangé")

    if mode == "--check" and drift:
        print("\nDÉRIVE détectée — lancer sync-claude-md.py pour réaligner.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
