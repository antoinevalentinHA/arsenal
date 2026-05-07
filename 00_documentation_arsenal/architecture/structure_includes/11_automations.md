# Structure — 11_automations

## Rôle

Déclaration des automatisations Home Assistant.

Les `automation` servent à :
- réagir à des événements,
- appliquer des décisions,
- orchestrer des transitions,
- synchroniser des états,
- déclencher des scripts,
- maintenir la cohérence système,
- matérialiser des comportements réactifs.

Une automatisation relie un contexte observé à une exécution contrôlée.

---

## Doctrine Arsenal

Les automatisations constituent la couche réactive d’Arsenal.

Une automatisation peut :
- observer,
- filtrer,
- synchroniser,
- déclencher,
- appliquer,
- réconcilier.

Mais une automatisation ne doit jamais :
- devenir une autorité métier diffuse,
- dupliquer une décision centrale existante,
- mélanger plusieurs responsabilités indépendantes,
- contourner les contrats du domaine concerné.

Toute automatisation doit posséder :
- un périmètre explicite,
- des déclencheurs identifiables,
- des effets observables,
- une stratégie de concurrence cohérente,
- une idempotence compatible avec les retriggers.

---

## Include

```yaml
automation: !include_dir_merge_list 11_automations/
```

---

## Structure attendue

```yaml
- id: "<identifiant>"
  alias: <nom_lisible>
  description: <texte_libre>
  mode: <mode>

  trigger:
    - <trigger>

  condition:
    - <condition>

  action:
    - <action | choose>
```

---

## Clés courantes

- id
- alias
- description
- mode
- trigger
- condition
- action
- variables
- max
- max_exceeded
- trace

---

## Typologies Arsenal

Une `automation` peut représenter :

- une automation d’application,
- une automation de synchronisation,
- une automation de remédiation,
- une automation de réconciliation,
- une automation événementielle,
- une automation de protection,
- une automation d’orchestration,
- une automation de contexte.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- ID fourni par Arsenal
- L’ID doit être une chaîne (`string`)
- Les guillemets autour de l’ID sont obligatoires
- Pas d’auto-génération d’ID
- Pas de dépendance par alias
- Toute condition importante doit être explicitement visible
- Toute automation doit posséder une responsabilité identifiable
- Toute logique décisionnelle doit avoir une autorité clairement définie
- Toute automation doit être compatible avec les retriggers et redémarrages
- Toute séparation décision / application doit être explicitement documentée
- Aucun pilotage critique ne doit dépendre implicitement d’un ordre d’exécution non garanti

---

## Modes Arsenal — Doctrine générale

Le choix du `mode` fait partie du contrat comportemental de l’automatisation.

Chaque mode doit être cohérent avec :
- la criticité du domaine,
- la nature des effets produits,
- les contraintes de concurrence,
- les garanties transactionnelles attendues.

Exemples courants :

- `single`
  - Exclusivité stricte
  - Refus des retriggers concurrents

- `restart`
  - Nouvelle variation prioritaire
  - Remplacement explicite de l’exécution en cours

- `queued`
  - Sérialisation ordonnée
  - Conservation des événements successifs

- `parallel`
  - Exécutions concurrentes autorisées
  - Réservé aux traitements explicitement indépendants

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — AUTOMATION
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🆔 IDENTIFIANT
#   <id Arsenal — string, guillemets obligatoires>
#
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Couvre : <responsabilité incluse>
#   - Exclut : <responsabilité explicitement hors périmètre>
#
# 🔖 NATURE
#   <Application | Synchronisation | Remédiation
#    | Réconciliation | Événementielle | Protection
#    | Orchestration | Contexte>
#
# ⚙️ MODE
#   <single | restart | queued | parallel>
#   Justification : <raison du choix>
#
# 📣 DÉCLENCHEURS
#   <Événements, états ou conditions qui déclenchent l'automation>
#
# 🔗 DÉPENDANCES
#   Lit      : <entités consultées>
#   Appelle  : <scripts, services ou événements appelés>
#   Écrit    : <helpers, entités ou états modifiés>
#
# 🧠 AUTORITÉ
#   <Applique une décision externe | Décide et applique
#    — avec justification si les deux>
#
# ♻️ IDEMPOTENCE
#   <Compatible retrigger | Non garantie — justification>
#
# 🚫 INTERDITS
#   - Devenir une autorité métier diffuse
#   - Dupliquer une décision centrale existante
#   - Mélanger plusieurs responsabilités indépendantes
#   - Contourner les contrats du domaine concerné
#   - <Interdits spécifiques au domaine>
#
# 🏷️ STATUT
#   <Socle | Réactive | Réconciliation | Protection> — Arsenal v14.x
# ==========================================================
```