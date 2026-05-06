# Structure — 10_scripts

## Rôle

Déclaration de scripts exécutables Home Assistant.

Les `script` servent à :
- appliquer des actions,
- orchestrer des séquences,
- centraliser des calculs,
- exécuter des transactions,
- encapsuler des comportements réutilisables,
- qualifier des états post-action,
- porter des pipelines déterministes.

Un script exécute une séquence contrôlée d’opérations.

---

## Doctrine Arsenal

Les scripts constituent la couche d’exécution et d’orchestration d’Arsenal.

Un script peut :
- calculer,
- orchestrer,
- appliquer,
- qualifier,
- publier un résultat.

Mais un script ne doit jamais :
- porter une logique diffuse,
- contourner l’architecture contractuelle,
- mélanger décision et exécution sans justification explicite.

Tout script doit posséder :
- une responsabilité clairement identifiable,
- un périmètre explicite,
- des effets observables,
- une stratégie d’idempotence cohérente.

---

## Include

```yaml
script: !include_dir_merge_named 10_scripts/
```

---

## Structure

```yaml
<nom_script>:
  alias: <nom_lisible>
  mode: <mode>
  sequence:
    - <action | condition | choose>
```

---

## Clés courantes

- alias
- mode
- icon
- description
- fields
- sequence
- variables
- max
- max_exceeded

---

## Typologies Arsenal

Un `script` peut représenter :

- une action pure,
- une orchestration,
- une décision centrale,
- une transaction applicative,
- une remédiation,
- une qualification post-action,
- un pipeline métier,
- un utilitaire réutilisable.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas d’appel circulaire
- Toute responsabilité doit être explicitement identifiable
- Toute logique décisionnelle doit avoir une autorité clairement définie
- Toute action matérielle doit être observable
- Toute orchestration critique doit être idempotente
- Toute écriture d’état doit être traçable
- Aucun script ne doit contourner les contrats du domaine concerné
- Toute séparation décision / exécution doit être explicitement documentée

---

## Modes Arsenal — Doctrine générale

Le choix du `mode` fait partie du contrat comportemental du script.

Chaque mode doit être justifié par :
- la nature des effets produits,
- les contraintes de concurrence,
- les garanties transactionnelles attendues.

Exemples courants :

- `single`
  - Exclusivité stricte
  - Refus des appels concurrents

- `restart`
  - Nouvelle demande prioritaire
  - Abandon explicite de l’exécution précédente

- `queued`
  - Sérialisation ordonnée
  - Préservation de toutes les demandes

- `parallel`
  - Exécutions concurrentes autorisées
  - Réservé aux traitements explicitement indépendants

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — SCRIPT
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Exécuter une séquence contrôlée d’actions ou
#   d’orchestrations dans le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   Nature du script :
#   - Action pure
#   - Orchestration
#   - Décision centrale
#   - Qualification post-action
#
# 📡 SOURCES
#   - Entités, événements ou appels externes consommés
#
# 🚫 INTERDITS
#   - Introduire une logique diffuse
#   - Mélanger décision et exécution sans contrat explicite
#   - Contourner les autorités métier établies
# ==========================================================
```