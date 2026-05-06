# 🧠 ARSENAL — ECS  
# Journalisation et traçabilité des cycles

Chemin : `/homeassistant/00_documentation_arsenal/ecs/08_journalisation_et_tracabilite.md`  
Statut : **CRITIQUE — OPPOSABLE**  
Périmètre : Traçabilité ECS

---

## 1. Objet

Ce document définit les règles de journalisation
et de traçabilité des cycles ECS.

Il garantit qu'aucun cycle
ne peut exister sans preuve.

---

## 2. Principe fondamental

> Un cycle ECS n'existe que s'il est traçable
> du début au gel final déclenché par le signal canonique de fin de cycle.

Toute chauffe non documentée
est réputée invalide.

---

## 3. Chaîne de journalisation

Chaque cycle ECS doit produire
les éléments suivants :

1. journalisation du début de cycle
2. capture du pic thermique réel
3. stabilisation via timer d'inertie post-cycle
4. gel des diagnostics à l'échéance du timer
5. émission du signal canonique de fin de cycle

L'absence d'un maillon
constitue une anomalie critique.

---

## 4. Début de cycle

À l'ouverture d'un cycle :

- horodatage immédiat
- identification du mode
- initialisation du contexte
- création du journal

Aucun cycle ne démarre
sans journal ouvert.

---

## 5. Pic thermique réel

Le pic thermique est :

- mesuré
- horodaté
- enregistré
- opposable

Toute valeur supposée
est proscrite.

---

## 6. Consolidation finale

### 6.1 Séquence

À l'échéance du timer d'inertie post-cycle :

- calcul des durées
- agrégation des données
- génération du résumé
- gel définitif des diagnostics
- émission du signal canonique `ecs_fin_cycle_signal`

Le gel final constitue l'unique point de clôture exploitable d'un cycle ECS.

Les données sont ensuite immuables.

### 6.2 Référence temporelle

La consolidation et le gel final ne s'appuient pas
sur la fin thermique du cycle.

Ils dépendent exclusivement :

- de l'expiration du timer d'inertie post-cycle
- de l'émission du signal canonique `ecs_fin_cycle_signal`

Aucune donnée ne peut être considérée comme consolidée
avant cet événement.

---

## 7. Supports de traçabilité

La traçabilité repose sur :

- input_datetime
- capteurs figés
- journaux persistants
- archives JSON

Chaque support est redondant.

---

## 8. Exploitation des données

Les dashboards et analyses :

- consomment uniquement du figé
- ne recalculent rien
- ne corrigent rien

Toute analyse dynamique est interdite.

---

## 9. Anti-patterns

Sont interdits :

- cycle sans journal
- modification a posteriori
- effacement silencieux
- reconstruction implicite
- historisation partielle

Toute violation est critique.
