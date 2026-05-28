# ==========================================================
# 🧠 ARSENAL — AMENDEMENT NORMATIF
#     CHAUFFAGE — GOUVERNANCE GÉNÉRALE (V3 PRO)
#     Amendement : ancrage de la doctrine des registres
# ==========================================================
#
# 📌 STATUT :
#   AMENDEMENT au contrat fondateur `00_gouvernance_chauffage.md`
#
# 🎯 OBJET :
#   Ancrer dans la constitution du domaine la distinction
#   sécurité système / stabilisation thermique formalisée par
#   le contrat racine `01_doctrine_registres.md`, et préciser
#   que le Niveau 1 de la hiérarchie des causes est strictement
#   sécuritaire.
#
#   Cet amendement ne réécrit pas la constitution. Il en précise
#   l'interprétation et y introduit une référence normative.
#   La constitution n'était pas fautive ; elle ne nommait pas
#   explicitement la distinction des registres.
#
# ==========================================================

---

## A1. Insertion d'une référence racine

Ajouter, en tête de la hiérarchie documentaire (§11 de `00`), la mention :

> Le présent contrat est complété par le contrat racine
> `01_doctrine_registres.md`, qui définit la clé de lecture du domaine
> (sécurité système vs stabilisation thermique) et gouverne l'interprétation
> de tous les contrats subordonnés. En cas de divergence d'interprétation
> entre deux contrats de domaine, la classification des registres posée par
> `01` fait foi.

---

## A2. Précision sur la hiérarchie des causes (§5)

Le §5 « Hiérarchie des causes » de `00` est précisé comme suit, sans
modification de l'ordre des niveaux existants :

> **Précision normative (registres).**
> Le NIVEAU 1 — INTERDICTIONS ABSOLUES est strictement réservé aux causes de
> **sécurité système** : fenêtre ouverte, épisode d'aération, indisponibilité
> d'exécution, interdiction système explicite, mode vacances en tant que
> contexte majeur. Une cause de **stabilisation thermique** (poêle,
> inhibition géofencing, verrou de standby, modulation météo) ne peut jamais
> être portée au NIVEAU 1.
>
> Les causes de stabilisation s'expriment exclusivement dans les couches
> d'autorisation et d'application, et se résolvent par la qualité du signal,
> l'hystérésis et la corroboration — jamais par dominance hiérarchique.

---

## A3. Précision sur la souveraineté décisionnelle (§4)

Compléter le §4 « Souveraineté décisionnelle » de `00` par l'invariant de
non-remontée :

> **Précision normative (non-remontée — D3).**
> Aucune grandeur produite par la décision centrale, ou en aval de celle-ci,
> ne peut remonter alimenter une couche amont comme si elle en était une
> cause. La persistance, l'historisation ou l'exposition en diagnostic d'une
> telle grandeur ne la transforment jamais en cause décisionnelle. Toute
> remontée d'une conséquence vers une cause constitue une inversion de
> responsabilité et une régression architecturale.

---

## A4. Conséquence sur `binary_sensor.chauffage_autorise_systeme`

> Le capteur `binary_sensor.chauffage_autorise_systeme` est, par la présente
> précision, qualifié de capteur de **sécurité système pure**. Sa composition
> est limitée aux causes de sécurité (notamment le blocage post-aération et
> les indisponibilités d'exécution). Aucune grandeur de stabilisation,
> notamment le verrou `input_boolean.chauffage_standby_force`, n'entre dans sa
> composition.
>
> La mise en conformité de l'implémentation est régie par `30` et `50`.

---

## A5. Invariants exposés

- **INV-GOV-1** — Le NIVEAU 1 de la hiérarchie des causes ne contient que des
  causes de sécurité système.
- **INV-GOV-2** — Aucune conséquence décisionnelle ne figure en entrée d'une
  cause amont (reprise de INV-D3).

---

## A6. Portée

Cet amendement est stable, opposable, et versionné avec la constitution du
domaine. Il prend effet en même temps que la publication de
`01_doctrine_registres.md`.

# ==========================================================
