# Arsenal — Architecture UI transverse
## Contrat d'architecture UI Arsenal — v1

---

## Principes fondateurs

**UI ≠ décision**
Une carte UI expose, interprète ou agrège. Elle ne décide pas, ne commande pas au sens backend du terme, et n'est pas source de vérité.

**Backend source de vérité**
Toute carte lit un état produit par le backend. Elle ne le produit pas, ne le déduit pas de manière autoritative.

**Pas de logique métier critique en UI**
Une carte UI ne doit jamais porter une logique métier critique dont la cohérence est requise pour le fonctionnement du système. Les seuils et classifications UI sont tolérés uniquement pour l'affichage — ils ne sont pas utilisés par le système comme source de vérité.

**Séparation commande / lecture**
Les cartes d'action sont physiquement isolées des cartes de lecture. Pas de mélange dans un même dossier ou groupe fonctionnel.

**Cartes satellites explicites**
Une carte qui explicite ou contextualise une autre carte doit être rattachée à sa carte parente dans la documentation. Une carte satellite sans rattachement explicite est **invalide d'un point de vue documentaire**.

**Pas de dépendance UI → UI**
Une carte UI ne doit jamais dépendre d'une autre carte UI pour son fonctionnement. Toute dépendance doit pointer vers le backend.

> Exception : rattachement documentaire (satellite → parent).

---

## Symétrie backend / UI

| Backend    | UI             |
|------------|----------------|
| décision   | affichage      |
| exécution  | action         |
| diagnostic | diagnostic     |
| vérité     | lecture        |

L'UI est une projection de l'architecture système, pas une couche indépendante.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                   | Règle d'usage                                              | Cardinalité                        |
|----------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------|-------------------------------------|
| pure           | aucune transformation — affichage direct                                                        | 1 entité, 1 état, 1 mapping                                | 1 entité STRICT                    |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non utilisée par le système comme source de vérité | seuils, comparaison intention/réel, classification | 1 entité (tolérance 2 si comparaison) |
| agrégative     | combinaison simple de plusieurs signaux (≤ 3 entités, logique lisible), destinée à une lecture directe | lecture multi-entités, logique de priorité           | 2 à 3 entités MAX                  |
| diagnostic     | qualifie la cohérence ou l'état du système                                                      | confrontation backend / réel, rendu fiabilité/divergence   | multi-entités autorisé si cohérent |
| action         | proxy UI d'une commande backend, déclenchée explicitement par l'utilisateur                     | confirmation obligatoire, isolée des cartes de lecture     | —                                  |
| info           | explicite une raison ou un contexte textuel                                                     | satellite d'une carte parente, rattachement obligatoire    | —                                  |
| supervision    | agrégation complexe ou transverse, multi-domaines ou priorisation — jamais utilisée comme source opérationnelle | agrégation lourde, dossier `90_supervision/`   | non borné                          |

> Le libellé "UI uniquement (aucune décision)" est **inexact** pour les types interprétative, agrégative et diagnostic, qui embarquent des transformations locales. Utiliser le champ `TYPE UI` à la place.

### Qualificatif complémentaire : carte pivot

Une carte lisant plusieurs axes simultanément (ex. intention + état réel + cohérence) peut être qualifiée de **pivot** dans son entête. Ce n'est pas un type UI distinct — c'est un marqueur documentaire signalant une responsabilité élargie.

---

## Règles sur les transformations UI

Toute transformation UI doit respecter au moins une des conditions suivantes :

1. Représentation visuelle (mapping état → couleur / icône)
2. Comparaison non persistée (ex. intention vs réel)
3. Classification locale non utilisée ailleurs

**INTERDIT :**
- recalcul métier (ex. seuil de décision)
- reproduction d'une logique backend existante
- création d'un état implicite non exposé par le backend

---

## Règles sur les cartes d'action

Une carte d'action :

- ne contient **aucune logique conditionnelle métier**
- ne décide jamais d'exécuter ou non
- ne fait que déclencher une action backend explicite

Toute condition doit être portée par :
- le backend (automation / script)
- ou la validation utilisateur (confirmation UI)

---

## Modèle de couches UI

Chaque domaine dashboard exprime un pipeline UI. La structure cible générique est :

```
10_action/          ← commandes critiques (isolées)
20_[intention]/     ← statut / intention / état brut
30_[diagnostic]/    ← cohérence, interprétation, synthèse
40_[contexte]/      ← contexte métier spécifique au domaine
90_supervision/     ← agrégation lourde multi-entités
```

Les noms entre crochets sont adaptés au domaine. Le schéma de numérotation est stable.

---

## Entête normative

Modèle canonique — à respecter pour toute carte Arsenal UI :

```yaml
# ==========================================================
# 🧠 ARSENAL — CARTE UI
#     [Domaine] — [Fonction courte]
#
# 🗂️ COUCHE : [10_action|20_xxx|30_xxx|40_xxx|90_supervision]
# 🧱 TYPE UI : [pure|interprétative|agrégative|diagnostic|action|info|supervision]
# 🔍 NIVEAU DE CONFIANCE : [fort|indicatif|diagnostic]
# ==========================================================
#
# 🎯 RÔLE
#   ...
#
# 📡 SOURCE
#   ...
#
# ⚙️ LOGIQUE UI
#   ...
#
# ----------------------------------------------------------
# 🔒 STRUCTURE
#   SATELLITE et PIVOT sont mutuellement exclusifs
# ----------------------------------------------------------
#
# 🔗 SATELLITE DE : [carte parente]
#
# ⚠️ CARTE PIVOT
#   Traverse :
#     - intention
#     - état réel
#     - diagnostic
# ==========================================================
```

### Champs obligatoires

| Champ | Valeurs |
|-------|---------|
| `COUCHE` | `10_action` / `20_xxx` / `30_xxx` / `40_xxx` / `90_supervision` |
| `TYPE UI` | `pure` / `interprétative` / `agrégative` / `diagnostic` / `action` / `info` / `supervision` |
| `NIVEAU DE CONFIANCE` | `fort` / `indicatif` / `diagnostic` |

- **fort** → reflet direct backend
- **indicatif** → transformation locale
- **diagnostic** → interprétation / incohérence

### Champs conditionnels

`SATELLITE DE` et `CARTE PIVOT` sont **mutuellement exclusifs**. Omis si aucun ne s'applique.

---

## Implémentations de référence

| Domaine  | Couche centrale   | Type UI dominant | Document                               |
|----------|-------------------|------------------|----------------------------------------|
| aeration | mesure évaluée    | interprétative   | `40_dashboards/aeration/README.md`     |
| alarme   | cohérence système | diagnostic       | `40_dashboards/alarme/README.md`       |

---

## Règles de gouvernance

1. Tout nouveau dossier domaine produit un `README.md` d'architecture avant toute carte.
2. Le type UI et le niveau de confiance de chaque carte sont déclarés dans l'entête avant mise en production.
3. Les cartes d'action (`10_action/`) ne cohabitent jamais avec des cartes de lecture.
4. Une carte satellite sans rattachement explicite est invalide d'un point de vue documentaire.
5. Aucune logique métier critique ne réside en UI — les transformations locales sont tolérées uniquement dans les conditions définies ci-dessus.
6. Une carte UI ne dépend jamais d'une autre carte UI — toute dépendance pointe vers le backend.
7. La cardinalité par type UI est contrainte — les dépassements doivent être justifiés et enregistrés.
8. La taxonomie ci-dessus est la référence Arsenal. Toute extension doit être justifiée et enregistrée ici.
