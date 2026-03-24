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

| Type UI        | Signification                                                                                   | Règle d'usage                                              |
|----------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| pure           | aucune transformation — affichage direct                                                        | 1 entité, 1 état, 1 mapping                                |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non utilisée par le système comme source de vérité | seuils, comparaison intention/réel, classification |
| agrégative     | combinaison de plusieurs signaux                                                                 | lecture multi-entités, logique de priorité                 |
| diagnostic     | qualifie la cohérence ou l'état du système                                                      | confrontation backend / réel, rendu fiabilité/divergence   |
| action         | proxy UI d'une commande backend, déclenchée explicitement par l'utilisateur                     | confirmation obligatoire, isolée des cartes de lecture     |
| info           | explicite une raison ou un contexte textuel                                                     | satellite d'une carte parente, rattachement obligatoire    |
| supervision    | synthèse multi-entités riche                                                                    | agrégation lourde, dossier `90_supervision/`               |

> Le libellé "UI uniquement (aucune décision)" est **inexact** pour les types interprétative, agrégative et diagnostic, qui embarquent des transformations locales. Utiliser le champ `TYPE UI` à la place.

### Qualificatif complémentaire : carte pivot

Une carte lisant plusieurs axes simultanément (ex. intention + état réel + cohérence) peut être qualifiée de **pivot** dans son entête. Ce n'est pas un type UI distinct — c'est un marqueur documentaire signalant une responsabilité élargie.

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

Chaque carte doit déclarer son type UI dans son entête :

```yaml
# 🧱 TYPE UI : [pure|interprétative|agrégative|diagnostic|action|info|supervision]
```

Pour les cartes satellites :

```yaml
# 🔗 SATELLITE DE : [nom de la carte parente]
```

Pour les cartes pivot :

```yaml
# ⚠️ CARTE PIVOT
#     Traverse plusieurs couches :
#       - intention (20)
#       - état réel (source)
#       - diagnostic (30)
#     Ne doit pas être dupliquée ailleurs
```

---

## Implémentations de référence

| Domaine  | Couche centrale   | Type UI dominant | Document                               |
|----------|-------------------|------------------|----------------------------------------|
| aeration | mesure évaluée    | interprétative   | `40_dashboards/aeration/README.md`     |
| alarme   | cohérence système | diagnostic       | `40_dashboards/alarme/README.md`       |

---

## Règles de gouvernance

1. Tout nouveau dossier domaine produit un `README.md` d'architecture avant toute carte.
2. Le type UI de chaque carte est déclaré dans l'entête avant mise en production.
3. Les cartes d'action (`10_action/`) ne cohabitent jamais avec des cartes de lecture.
4. Une carte satellite sans rattachement explicite est invalide d'un point de vue documentaire.
5. Aucune logique métier critique ne réside en UI — les transformations locales sont tolérées uniquement pour l'affichage.
6. La taxonomie ci-dessus est la référence Arsenal. Toute extension doit être justifiée et enregistrée ici.
