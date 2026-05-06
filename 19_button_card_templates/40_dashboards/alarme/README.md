# `40_dashboards/alarme/` — Architecture UI

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Cartes d'action critique

Exemple : `carte_action_arret_sirene`

- Aucune lecture d'état — exécution immédiate
- Confirmation obligatoire
- Effet opérationnel direct
- **Type UI : action** (déclenche une exécution utilisateur explicite)

→ À isoler absolument. Ce n'est ni du statut, ni du diagnostic, ni de l'info.

---

### B. Cartes d'intention

Exemple : `carte_alarme_intention`

- Expose une intention backend
- La confronte à l'état réel
- Neutralité possible avec `NOOP`
- **Type UI : interprétative** (expose une intention et la confronte au réel)

→ Ce n'est pas un affichage brut : il y a comparaison avec le réel. Pas "pure", pas autoritative.

---

### C. Cartes de diagnostic

Exemples : `carte_alarme_decision`, `alarme_diagnostic_coherence`

- Lecture de cohérence système
- Confrontation backend / état réel
- Rendu orienté fiabilité et divergence
- **Type UI : diagnostic** (qualifie la cohérence du système)

Deux sous-niveaux dans cette famille :

- `carte_alarme_decision` : **carte pivot** — lit l'intention, l'état réel et conclut sur la cohérence. Emplacement correct dans `30_diagnostic/`, mais rôle à documenter explicitement dans l'entête.
- `alarme_diagnostic_coherence` : diagnostic synthétique global

→ Famille centrale du lot.

---

### D. Cartes d'information contextuelle

Exemple : `alarme_diagnostic_coherence_raison`

- Affiche la raison textuelle d'un état de cohérence
- Ne porte pas la cohérence elle-même — sert d'explicitation
- **Type UI : info** (explicite une raison ou un contexte textuel)

→ Carte satellite de `alarme_diagnostic_coherence`. Doit être explicitement rattachée au diagnostic, pas laissée comme carte d'info flottante.

---

## Taxonomie des types UI

| Type UI        | Signification                                 | Exemples                                                |
|----------------|-----------------------------------------------|---------------------------------------------------------|
| action         | déclenche une exécution utilisateur explicite | `carte_action_arret_sirene`                             |
| interprétative | expose une intention et la confronte au réel  | `carte_alarme_intention`                                |
| diagnostic     | qualifie la cohérence du système              | `carte_alarme_decision`, `alarme_diagnostic_coherence`  |
| info           | explicite une raison ou un contexte textuel   | `alarme_diagnostic_coherence_raison`                    |

> Le libellé "UI uniquement (aucune décision)" est **inexact** pour `carte_alarme_intention` et `carte_alarme_decision`, qui comparent, qualifient et concluent sur une cohérence ou une divergence. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Groupes fonctionnels

### Axe "commande"

- `carte_action_arret_sirene`

Monde à part. Ne pas mélanger avec les cartes de lecture.

---

### Axe "intention / décision / réel"

- `carte_alarme_intention`
- `carte_alarme_decision`

Cartes sœurs, profondeur différente :

- `intention` : lecture centrée sur la consigne/intention
- `decision` : lecture riche avec état réel, cible et cohérence (carte pivot)

→ Même grappe, pas même couche.

---

### Axe "cohérence système"

- `alarme_diagnostic_coherence`
- `alarme_diagnostic_coherence_raison`

Duo naturellement lié : état de cohérence + raison de cohérence.

---

## Lecture globale

Le domaine alarme impose structurellement une distinction forte entre :

- ce qu'on veut (intention)
- ce qui est réellement armé (état réel)
- si le système est cohérent (diagnostic)
- pourquoi il ne l'est pas (raison)
- quelle action critique est disponible (commande)

Le point central de ce domaine n'est pas la mesure (contrairement à `aeration`) — c'est la **cohérence entre backend, intention et état réel**. Ce dossier n'appelle pas d'abord une factorisation technique ; il appelle une **clarification de couches et de vocabulaire**.

---

## Structure cible recommandée

```
40_dashboards/alarme/

  10_action/
    carte_action_arret_sirene.yaml

  20_intention/
    carte_alarme_intention.yaml

  30_diagnostic/
    carte_alarme_decision.yaml
    alarme_diagnostic_coherence.yaml
    alarme_diagnostic_coherence_raison.yaml   ← option pragmatique
```

> `alarme_diagnostic_coherence_raison` peut alternativement être isolée dans `31_info_diagnostic/` si la rigueur architecturale prime sur la compacité. Les deux options sont valides.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Ajouter `TYPE UI` dans les entêtes**

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Documenter `carte_alarme_decision` comme carte pivot**
Ajouter dans son entête : lecture intention + lecture réel + diagnostic de cohérence.

**Étape 4 — Rattacher explicitement `raison` au diagnostic**
Clarifier dans l'entête de `alarme_diagnostic_coherence_raison` qu'elle est satellite de `alarme_diagnostic_coherence`.

**Étape 5 — Doctrine (optionnel)**
Aligner la taxonomie UI avec celle du domaine `aeration` et contribuer au socle Arsenal transverse (`00_documentation_arsenal/ui/architecture_ui.md`).
