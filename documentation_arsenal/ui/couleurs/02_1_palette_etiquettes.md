# 🧱 ARSENAL — Palette structure UI

## Objet

Ce document définit la **palette structurelle Arsenal** : couleurs
assignées aux sous-rôles fonctionnels des artefacts système.

Cette palette est **strictement distincte** de la palette sémantique
définie dans `02_palette.md`. Elle ne traduit aucun état métier.
Elle encode uniquement le **sous-rôle fonctionnel** d'un artefact,
indépendamment de son type technique (`helper`, `sensor`, `script`,
`signal`).

---

## Principe fondamental

> Une couleur de structure UI identifie un sous-rôle fonctionnel.
> Elle ne traduit ni état, ni niveau d'alerte, ni hiérarchie.

---

## Séparation contractuelle avec `02_palette.md`

| Palette | Encode | Référence |
|---------|--------|-----------|
| Sémantique | Un état métier (OK / KO / WARN / INFO / OFF) | `02_palette.md` |
| Structure UI | Un sous-rôle fonctionnel stable | ce document |

Ces deux palettes ne peuvent pas se substituer l'une à l'autre.
Une couleur structurelle ne peut jamais être utilisée pour signaler
un état métier, et inversement.

---

## Mapping officiel

| Sous-rôle | Couleur | HEX |
|-----------|---------|-----|
| `decision` | Violet ardoise | `#7E57C2` |
| `decision_input` | Sarcelle froide | `#26A69A` |
| `execution` | Indigo moyen | `#5C6BC0` |
| `guard` | Brun rosé | `#A1887F` |
| `support` | Bleu-gris froid | `#78909C` |
| `diagnostic` | Olive gris | `#8D9440` |
| `raw` | Gris ardoise | `#757575` |
| `derived` | Sarcelle sombre | `#546E7A` |
| `context` | Indigo clair | `#7986CB` |
| `memory` | Brun foncé chaud | `#6D4C41` |
| `parameter` | Gris bleuté | `#90A4AE` |

---

## Tests de non-collision perceptive

### Contre palette sémantique `02_palette.md`

| Couleur sémantique | HEX | Sous-rôle le plus proche | HEX | Verdict |
|-------------------|-----|--------------------------|-----|---------|
| Vert OK | `#4CAF50` | `decision_input` | `#26A69A` | ✅ sarcelle froide vs vert franc — distinct |
| Rouge critique | `#F44336` | `guard` | `#A1887F` | ✅ distinct |
| Orange warn | `#FF9800` | aucun | — | ✅ |
| Jaune vigilance | `#FFEB3B` | aucun | — | ✅ |
| Bleu info | `#2196F3` | `execution` | `#5C6BC0` | ✅ indigo vs bleu vif — distinct |

### Invariants vérifiés

| Contrainte | Statut |
|------------|--------|
| Pas de gradient `raw → derived → diagnostic` | ✅ aucune progression visuelle monotone explicite |
| `decision` ≠ `context` (non hiérarchisés) | ✅ violet ardoise vs indigo clair — familles distinctes |
| `decision` ≠ `decision_input` (non hiérarchisés) | ✅ violet vs sarcelle froide |
| `guard` ≠ rouge sémantique | ✅ brun rosé vs rouge vif |
| `parameter` / `context` / `memory` distincts | ✅ gris bleuté / indigo clair / brun foncé |
| `execution` ≠ `support` | ✅ indigo vs bleu-gris |
| Pas de code température (froid → chaud) | ✅ aucune progression intentionnelle |

---

## Règles d'usage

1. **Exclusivité** : un artefact porte la couleur de son sous-rôle
   unique. Aucune combinaison, aucune nuance intermédiaire.

2. **Opacité** : ces couleurs sont destinées à des usages en
   texte, bordure ou badge. Pas de fond plein opaque sur carte
   (sauf exception documentée dans `03_exceptions.md`).

3. **Pas de variation dynamique** : la couleur structurelle ne change
   pas en fonction de l'état de l'entité. L'état est porté par la
   palette sémantique (`02_palette.md`), pas par cette palette.

4. **Stabilité** : le sous-rôle d'un artefact est stable. Sa couleur
   structurelle ne change donc jamais en cours de session.

---

## 🚫 Interdits

- Utiliser une couleur de cette palette pour signaler un état métier
- Introduire une nuance non documentée dans ce tableau
- Faire varier l'opacité pour créer une hiérarchie implicite
- Réutiliser une couleur sémantique (`02_palette.md`) pour un sous-rôle
- Assigner deux sous-rôles différents à la même couleur

---

## Référence croisée

| Document | Rôle |
|----------|------|
| `01_principes.md` | Gouvernance générale des couleurs UI |
| `02_palette.md` | Palette sémantique (états métier) |
| `03_exceptions.md` | Couleurs de structure UI (navigation, typographie) — cf. `04_typographie.md` |
| ce document | Palette structurelle par sous-rôle fonctionnel |
