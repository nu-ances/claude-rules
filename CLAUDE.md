<!-- COMMON:START — bloc généré, NE PAS ÉDITER (source : nu-ances/claude-rules) -->
# Règles communes — groupe Nuances

> Bloc commun à **tous** les repos `nu-ances`. Source de vérité unique :
> `nu-ances/claude-rules` (`common.md`). Propagé dans chaque `CLAUDE.md`
> par `sync-claude-md.py`. **Ne pas éditer ce bloc dans un repo** — éditer la
> source puis resynchroniser.

## ⛔ Politique de sécurité — application obligatoire

Avant **tout** plan ou **toute** modification touchant infrastructure, code,
IAM, secrets ou accès :

1. **Conformité obligatoire** — toute proposition applique la politique de
   sécurité du groupe. Les contrôles non négociables ci-dessous ne se
   contournent pas.
2. **Déclaration systématique** — chaque plan/modification indique
   explicitement s'il est ✅ **CONFORME** ou ⚠️ **NON CONFORME**, même quand
   tout est conforme.
3. **Validation explicite avant dérogation** — toute modification qui n'adhère
   pas pleinement à la politique est **bloquée** jusqu'à accord explicite de
   l'utilisateur (préciser le contrôle dérogé, le motif, le risque).

### Contrôles non négociables (autoportants)

- **Aucun secret dans git** — clés API, private keys, tokens, mots de passe.
- **Aucune clé JSON de service account** — WIF ou impersonation uniquement
  (garanti par l'org policy `iam.disableServiceAccountKeyCreation`).
- **Aucun rôle IAM accordé à un individu** — uniquement via groupes Workspace.
- **Ressources confinées en UE** (`gcp.resourceLocations`).
- **Toute ressource GCP existe dans `nuances-gcp-iac`** (Terraform) — pas de
  création manuelle non importée.

Référence complète : [`security/README.md`](https://github.com/nu-ances/docs/blob/main/docs/security/README.md).

## Conventions de travail

- Le français est la langue de travail du groupe.
- Commits/PRs : ne jamais committer ni pousser sans demande explicite.
- En cas de doute sur la conformité : exécuter les audits indexés dans
  [`security/README.md`](https://github.com/nu-ances/docs/blob/main/docs/security/README.md) —
  [`verify-security-baseline.sh`](https://github.com/nu-ances/docs/blob/main/docs/gcp/scripts/verify-security-baseline.sh)
  pour GCP, [`verify-github-baseline.sh`](https://github.com/nu-ances/docs/blob/main/docs/github/scripts/verify-github-baseline.sh)
  pour GitHub.
<!-- COMMON:END -->

## Règles spécifiques à ce repo (`claude-rules`)

- **Source de vérité** des règles communes. Pour modifier une règle commune :
  éditer `common.md` puis `python3 sync-claude-md.py` (propage partout).
- Le bloc commun ci-dessus est **lui-même généré** (auto-référence) — ne pas
  l'éditer directement.
- Repo volontairement **non sensible** : son contenu doit rester sûr à diffuser
  largement (la CI de chaque repo le lit).

