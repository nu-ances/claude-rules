# claude-rules

**Source de vérité unique** des règles communes Claude pour tous les repos
`nu-ances`. Repo volontairement **non sensible et largement lisible** : la CI de
chaque repo doit pouvoir le récupérer pour vérifier l'absence de dérive.

## Contenu

| Fichier | Rôle |
|---|---|
| `common.md` | Bloc commun canonique (politique de sécurité + conventions) |
| `sync-claude-md.py` | Propage le bloc dans le `CLAUDE.md` de chaque repo + `--check` CI |

## Fonctionnement

Chaque `CLAUDE.md` de repo contient un bloc délimité par des marqueurs
`COMMON:START` / `COMMON:END`. Le script n'écrit **que** ce bloc ; les règles
spécifiques de chaque repo, situées sous le bloc, sont préservées.

```bash
python3 claude-rules/sync-claude-md.py          # propage partout
python3 claude-rules/sync-claude-md.py --check   # dérive ? (exit 1) — pour la CI
python3 claude-rules/sync-claude-md.py --list     # cibles détectées
python3 claude-rules/sync-claude-md.py --write docs   # cibler un seul repo
```

Le script découvre les cibles : le `CLAUDE.md` du conteneur `nuances-ops` + le
`CLAUDE.md` de chaque repo git trouvé sous le conteneur (récursif, sans descendre
dans un repo).

## Modifier une règle commune

1. Éditer `common.md`.
2. `python3 claude-rules/sync-claude-md.py`.
3. Committer le bloc régénéré dans chaque repo impacté (ou laisser la CI signaler la dérive).

> Ne **jamais** éditer le bloc commun directement dans un repo : il serait
> écrasé au prochain sync, et la CI le signalerait comme dérive.
