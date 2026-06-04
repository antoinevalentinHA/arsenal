# Plan d'action de gouvernance — version révisée (sobre)

**Périmètre** : dépôt `antoinevalentinHA/arsenal`. **Base** : HEAD `899c172` (2026-06-04).
**Nature** : révision du plan d'action précédent, intégrant la contre-expertise A1/B1. **En cas de divergence, cette version prévaut.**
**Posture assumée** : après examen contradictoire, **les actions réellement justifiées sont très peu nombreuses**. Ce document ne cherche pas à remplacer A1/B1 par d'autres priorités.

---

## 1. Ce que la contre-expertise a tranché

- **A1 (étendre `CONFIGS` du moteur chauffage) — retirée.** La couverture décisionnelle du chauffage n'est pas portée par la liste de fichiers lintés mais par un **registre déclaré complet et bloquant** (`registres_entites.yaml` : `perimetre_statut: complet`, `meta2_mode: bloquant`) et par **trois étages** déjà actifs (lint, décision, exécution). L'action visait un vide qui n'existe pas ; étendre le lint à des fichiers d'observabilité produirait du bruit.
- **B1 (validateur statique `pannes`) — retirée sous cette forme.** Les invariants de `pannes` sont **comportementaux/temporels** (frontière d'épisode, idempotence à travers un redémarrage, « intention, non action »). Un validateur statique passerait au **vert** sans vérifier ce qui compte → fausse assurance sur un chemin d'échec. La gouvernance y est déjà stratifiée (contrat **socle** + dérivé).

Constat transverse : sur ce dépôt, le levier dominant n'est pas d'ajouter des contrôles, mais de **lire exactement ce qui est déjà contrôlé**.

---

## 2. Action documentaire (seule action positive justifiée)

### D1. Clarifier la documentation du moteur chauffage
- **Type** : action documentaire.
- **État actuel** : le `README` de `tools/arsenal_ci/` contient un exemple de chemin périmé (`packages/chauffage/autorisation.yaml`, `packages/` absent) ; rien n'explicite que le lint de fichier est **intentionnellement ancré** sur l'autorité Niveau 1 tandis que la couverture des entités relève du **registre** (complet, bloquant).
- **Bénéfice** : dissiper la confusion « fichier linté = domaine validé » — celle-là même qui avait, à tort, motivé A1.
- **Coût** : quasi nul (correction d'un exemple + une note de portée).
- **Priorité** : la seule réellement utile, et faible en valeur absolue.
- **Justification** : corrige un fait inexact et prévient une mauvaise lecture récurrente, sans ajouter aucun contrôle.

---

## 3. Décisions d'architecture (laissées à l'auteur, sans recommandation directive)

Ces points **ne sont pas recommandés** par ce plan ; ils relèvent d'un arbitrage que l'audit ne peut pas trancher faute d'information métier.

- **A3.1 — Extension de `CONFIGS`** : à n'envisager que **fichier par fichier, avec justification explicite** que le fichier visé est une *autorité décisionnelle* dont les règles du moteur ont quelque chose à dire. **Défaut = ne pas étendre.** Aucune extension par glob, aucune extension « pour homogénéité ».
- **A3.2 — Tests de scénario runtime pour `pannes`** : **uniquement si** le besoin métier est confirmé (chemin d'échec rarement exercé). Le cas échéant, ce serait un **rejeu d'épisode** (idempotence post-redémarrage, intention vs action) — **hors** du dispositif de validation statique. Ce n'est pas une action recommandée ici, c'est une option conditionnée à un besoin que seul l'auteur peut établir.

---

## 4. Absence d'action recommandée

- **Domaines en catégorie (B) « gouverné non automatisé »** (sante, imprimerie, pannes, bluetti, mouvements) : statut **légitime**. Un contrat sans validateur reste une gouvernance. Aucune action.
- **`reveils` / `electromenager`** (seul manque démontré partiel) : un contrat racine minimal n'aurait de valeur que si ces automatisations encodent une décision non triviale — information non disponible. **Pas d'action recommandée** ; à l'appréciation de l'auteur, sans priorité.
- **Re-validation périodique (`schedule:`)** : option non réfutée mais **non prioritaire** ; à ne considérer que si la dérive externe (renommages HA) se manifeste réellement.

---

## 5. Actions à ne PAS entreprendre

- **Ne pas ouvrir de chantier de gouvernance global.** Rien dans l'analyse ne le justifie ; ce serait de l'homogénéisation.
- **Ne pas étendre `CONFIGS`** sans justification fichier par fichier (cf. §3.1).
- **Ne pas créer de validateur statique `pannes`** (cf. contre-expertise).
- **Ne pas créer de contrats-parapluie `system`/`meteo`** : gouvernance distribuée délibérée.
- **Ne pas gouverner la perception passive** (`statistiques`, `babyphone`).
- **Ne pas remplir le squelette d'audit `voiture`** sans problème déclencheur.
- **Ne pas renommer de dossiers** pour cohérence (aucune règle interne, renommage à haut risque pour gain cosmétique).
- **Ne pas généraliser le moteur de type chauffage** aux autres domaines (les validateurs par domaine passent et sont substantiels).

---

## 6. Synthèse

Après contre-expertise, **une seule action positive est justifiée** : D1, une clarification documentaire à coût quasi nul. Les deux priorités précédentes tombent (A1 retirée, B1 retirée sous forme statique). Les rares pistes restantes sont des **décisions d'architecture conditionnées à un besoin métier** que l'auteur seul peut établir, ou des **non-actions assumées**.

C'est, en soi, un résultat de gouvernance : l'examen montre un système **plus complet que les premières lectures ne le suggéraient**, où l'effort le mieux placé est de documenter précisément l'existant plutôt que d'y ajouter des contrôles.

---

## 7. Limites

- Établi à `HEAD 899c172` ; périssable.
- D1 suppose seulement des faits déjà vérifiés (chemin périmé, portée du registre) ; sans risque.
- A3.1/A3.2 dépendent d'informations métier non disponibles ; posées en conditions, pas en recommandations.
- Aucune action n'est appliquée ; document d'aide à la décision.

---

*Fin du plan révisé. Sobre, coût-conscient, sans chantier global.*
