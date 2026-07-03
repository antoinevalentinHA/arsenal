# PATCH DOCUMENTAIRE (SÉPARÉ) — Correction de l'intention « asymétrie max/min COOL »

> **✅ Statut : APPLIQUÉ** (commit `2efb563` — `docs(clim): audit topologie mono-zone COOL`).
> Le remplacement décrit ci-dessous est **en place** dans `90_observations.md` : l'ancienne
> formulation trompeuse (« l'ensemble des zones redescendent ») a disparu, la nouvelle intention
> (topologie mono-zone / atteignabilité de OFF / compromis assumé) est présente. Ce document est
> conservé comme **trace** du raisonnement ; il n'y a plus rien à appliquer.

> **Version : v2** (révise la v1 de ce patch).
> **Nature :** correction **éditoriale simple**, **non normative**.
> Ne modifie **aucun runtime**, **aucun contrat exécutable**, **aucun capteur**,
> **aucune automatisation**. Corrige uniquement la *justification écrite* d'une
> asymétrie déjà existante, pour la rendre conforme à l'**intention réelle**
> démontrée en Phase 6 de
> [`audit_strategie_max_on_min_off_cool.md`](audit_strategie_max_on_min_off_cool.md)
> (contre-analyse topologique).
>
> **Changement v1 → v2 de ce patch.** La v1 corrigeait la phrase d'intention en la
> cadrant comme une **fragilité** du `min`-OFF (effondrement de bande morte,
> sur-refroidissement). La v2 **remplace ce cadrage** par l'intention véritable :
> `min`-OFF est un **mécanisme de robustesse mono-zone** qui garantit
> l'**atteignabilité de l'état OFF** face à une chambre thermiquement découplée.
> Le revers (arrêt potentiellement précoce en régime couplé) est documenté comme
> **compromis assumé**, non comme défaut.

---

## Fichier concerné

`00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/90_observations.md`
(section *« Asymétrie max / min — COOL »*, lignes 39-44 au commit `ce24fb28`)

## Texte exact à trouver

```
Cette asymétrie est volontaire :

- l'allumage se déclenche dès qu'une zone atteint une température élevée
- l'extinction attend que l'ensemble des zones redescendent sous le seuil

Ce mécanisme favorise une réactivité rapide à la surchauffe locale et une extinction stabilisée (évite les oscillations).
```

## Texte exact de remplacement

```
Cette asymétrie est volontaire et reflète la topologie **mono-zone** du système (un seul climatiseur sur le palier, chambres ouvrables/fermables, aucun capteur de porte ; pilotage multi-zones explicitement hors périmètre — voir `11_perimetre_exclu.md`) :

- **Allumage indexé sur la chambre la plus chaude** (`temperature_max_chambres`) : réactivité à la surchauffe locale — aucune pièce chaude n'est ignorée.
- **Extinction indexée sur la chambre la plus froide** (`temperature_min_chambres`) : en régime de refroidissement, la pièce la plus froide est presque toujours une pièce **couplée** (porte ouverte), donc une pièce que le climatiseur **contrôle effectivement**. Indexer l'extinction sur elle garantit que l'état **OFF reste atteignable**.

**Intention réelle.** L'extinction n'attend **pas** que toutes les zones repassent sous le seuil (cela imposerait `max` pour OFF). Le critère `min`-OFF empêche qu'une chambre **thermiquement découplée** (porte fermée, hors d'atteinte de l'appareil de palier) ne maintienne **indéfiniment** la climatisation active. Rappel `01_finalite.md` : « OFF est un état normal et volontaire, jamais une erreur ».

⚠️ **Portée exacte de la garantie.** `min`-OFF protège l'atteignabilité de OFF **uniquement lorsque la chambre la plus chaude est repassée sous le seuil d'allumage** (le franchissement ON est prioritaire dans `besoin_clim_cool`). Au-dessus du seuil d'allumage, c'est le critère d'**allumage sur le max** qui gouverne le maintien en marche, indépendamment de l'extinction.

**Compromis assumé.** En régime entièrement **couplé** (toutes portes ouvertes) et avec un écart inter-chambres ≥ hystérésis, le revers de `min`-OFF est un arrêt **possiblement précoce** de la pièce la plus chaude accessible. Ce compromis est **accepté** : il est borné et auto-corrigé (la pièce se réchauffe et redéclenche, ou l'utilisateur ouvre une porte). Le compromis **refusé** est celui qu'imposerait `max`-OFF : un **acharnement climatique** sur une chambre fermée, sans échappatoire automatique. Analyse complète : `audit_strategie_max_on_min_off_cool.md`, Phase 6.
```

## Justification

La formule documentée par ailleurs (`temp_max ≥ seuil` / `temp_min ≤ seuil`) est
exacte ; seule la **phrase d'intention** est à corriger. « L'extinction attend que
l'ensemble des zones redescendent sous le seuil » décrirait `max`-OFF, alors que
le runtime utilise `min`-OFF — **et surtout** cette phrase masque la vraie raison
du choix : sous topologie mono-zone, `min`-OFF garantit l'atteignabilité de OFF et
évite l'acharnement sur une chambre découplée. Le remplacement aligne l'intention
sur le comportement réel **et** sur la philosophie Arsenal (« OFF est normal »,
« éviter toute action par principe »). Aucune logique exécutable n'est touchée :
la correction est strictement documentaire.

## Commande de vérification (après remplacement)

```bash
# 1) L'ancienne formulation trompeuse a bien disparu :
grep -n "l'ensemble des zones redescendent" \
  00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/90_observations.md
#   → attendu : aucun résultat

# 2) La nouvelle intention (découplage / atteignabilité de OFF) est présente :
grep -n "OFF reste atteignable\|thermiquement découplée" \
  00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/90_observations.md
#   → attendu : au moins 1 résultat

# 3) Aucun runtime ni contrat exécutable n'a changé (seul le .md d'observation) :
git diff --name-only
#   → attendu : uniquement .../seuils_et_franchissements/90_observations.md
```

*Patch éditorial uniquement. Aucune modification appliquée par ce document.*
