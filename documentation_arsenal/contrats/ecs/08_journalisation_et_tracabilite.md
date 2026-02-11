# 🧠 ARSENAL — ECS  
# Journalisation et traçabilité des cycles

Chemin : `/homeassistant/documentation_arsenal/ecs/08_journalisation_et_tracabilite.md`  
Statut : **CRITIQUE — OPPOSABLE**  
Périmètre : Traçabilité ECS

---

## 1. Objet

Ce document définit les règles de journalisation
et de traçabilité des cycles ECS.

Il garantit qu’aucun cycle
ne peut exister sans preuve.

---

## 2. Principe fondamental

> Un cycle ECS n’existe que s’il est traçable
> du début au gel final.

Toute chauffe non documentée
est réputée invalide.

---

## 3. Chaîne de journalisation

Chaque cycle ECS doit produire
les éléments suivants :

1. journalisation du début de cycle
2. capture du pic thermique réel
3. consolidation post-stabilisation
4. gel des diagnostics

L’absence d’un maillon
constitue une anomalie critique.

---

## 4. Début de cycle

À l’ouverture d’un cycle :

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

Après stabilisation :

- calcul des durées
- agrégation des données
- génération du résumé
- gel définitif

Les données sont ensuite immuables.

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

---