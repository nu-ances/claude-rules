# claude-rules

**Source de vérité unique** des règles communes Claude pour tous les repos
`nu-ances`. Repo volontairement **non sensible et largement lisible** : la CI de
chaque repo doit pouvoir le récupérer pour vérifier l'absence de dérive.

> **Ce qui vit ici (et ce qui n'y vit pas).** Test en une phrase : « est-ce que
> ça doit être dans *tous* les repos *et* public ? » — Oui → ici ; non → dans
> [`nu-ances/docs`](https://github.com/nu-ances/docs). Donc `claude-rules` =
> bloc commun + machinerie (`sync-claude-md.py`, `ci-template/`), rien de plus ;
> toute la doctrine de profondeur (le pourquoi, le détail, les ADR) vit dans
> `docs` et le bloc commun la pointe par URL. Règle complète :
> [`principles/documentation-principles.md`](https://github.com/nu-ances/docs/blob/main/docs/principles/documentation-principles.md#frontière-claude-rules--docs).

## Contenu

| Fichier | Rôle |
|---|---|
| `common.md` | Bloc commun canonique (politique de sécurité + conventions) |
| `sync-claude-md.py` | Propage le bloc dans le `CLAUDE.md` de chaque repo + `--check` CI |
| `ci-template/claude-md-check.yml` | Workflow CI : vérifie la non-dérive du bloc commun (à copier dans chaque repo) |
| `ci-template/conformity-check.yml` | Workflow CI : gate de conformité des PR pour les repos `prod` (cf. ci-dessous) |

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

## Gate de conformité par niveau de repo

Acté par [ADR 012](https://github.com/nu-ances/docs/blob/main/docs/decisions/012-conformite-build-time-builder.md).
Chaque repo déclare son niveau dans un fichier `.nuances.yml` à sa racine :

```yaml
# Métadonnées de gouvernance du repo (lu par la CI de conformité)
niveau: prod   # prod | dev
```

- **`prod`** → le workflow `conformity-check.yml` **bloque** une PR tant qu'un
  `PLAN.md` (copié de [`docs/patterns/PLAN.template.md`](https://github.com/nu-ances/docs/blob/main/docs/patterns/PLAN.template.md))
  ne porte pas de déclaration de conformité résolue (`Statut : ✅ CONFORME` ou
  `⚠️ NON CONFORME`, avec tableau de dérogation rempli dans ce dernier cas).
- **`dev`** (ou `.nuances.yml` absent — **défaut sûr**) → gate inactif ; le
  template de plan reste une invitation, sans blocage CI.

La validation explicite humaine d'une dérogation passe par l'**approbation de la
PR**, pas par la CI (cf. point 3 de la politique de sécurité).
