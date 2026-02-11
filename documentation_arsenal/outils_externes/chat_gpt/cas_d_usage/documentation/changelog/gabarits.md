# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
# GABARITS DE CHANGELOG
# ==========================================================

Chemin canonique :
/homeassistant/documentation_arsenal/architecture/gabarits_changelog_arsenal.md

Statut : **NORMATIF — FONDATEUR**
Portée : Tous les fichiers `changelog.md` et `en_cours.md`
Objet : Définir les **formats canoniques** des versions Arsenal
Principe cardinal : **Aucune perte d’information autorisée**

---

## 🎯 OBJET DU CONTRAT

Ce document définit les **gabarits officiels de rédaction**
des changelogs du système **ARSENAL Home Assistant**.

Il établit :

* les **familles légitimes de versions**,
* les **structures canoniques associées**,
* les **sections obligatoires / optionnelles / interdites**,
* les **règles d’uniformisation cosmétique**,
* les invariants garantissant :

  * lisibilité historique,
  * traçabilité architecturale,
  * absence de perte d’information.

Ce contrat est **opposable** à toute consolidation future
du fichier `changelog.md`.

---

## 🧩 TYPOLOGIE OFFICIELLE DES GABARITS

Après analyse complète de l’historique Arsenal,
quatre (4) gabarits canoniques sont reconnus.

Aucun autre format n’est autorisé.

| Code | Nom du gabarit                                 | Rôle principal                             |
| ---- | ---------------------------------------------- | ------------------------------------------ |
| G1   | Version fondatrice / transition d’ère          | Fonder, clore une ère, poser des doctrines |
| G2   | Version de durcissement ciblé                  | Corriger, durcir sans refondre             |
| G3   | Version de doctrine / clarification sémantique | Formaliser, aligner, rendre lisible        |
| G4   | Version majeure structurée / moderne           | Release multi-domaines gouvernée           |

---

# 🥇 GABARIT G1 — VERSION FONDATRICE / TRANSITION D’ÈRE

## 🎯 RÔLE

Utilisé exclusivement pour :

* fondation d’architecture,
* clôture d’un cycle majeur,
* transition historique,
* version de référence restaurable.

Exemples historiques :

* v6.0
* v6.3
* v6.4
* v6.5
* v7.0

---

## 🧱 STRUCTURE CANONIQUE

1. En-tête de version

==============================
🧠 ARSENAL HA — vX.Y[.Z] [QUALIFICATIF]
=======================================

Qualificatifs autorisés :

* STABLE
* CLOSE
* RÉFÉRENCE
* CONSOLIDATION

2. Préambule de gouvernance obligatoire

   * changement d’ère
   * clôture de cycle
   * principes irréversibles

3. Grands chapitres architecturaux (5 à 10 max)

   * multi-domaines
   * structurants
   * doctrinaux

4. Section obligatoire finale :

📌 STATUT DE VERSION

ou, si version de socle :

📦 VERSION DE RÉFÉRENCE

5. Conclusion de gouvernance

   * projection future
   * règles de non-retour

---

## 🚫 INTERDITS

* Pas de section « Impact » détaillée
* Pas de micro-changements listés
* Pas de style compact
* Pas de version courte

---

## 🧠 SIGNATURE

* Long
* Normatif
* Doctrinal
* Multi-domaines
* Texte de gouvernance

---

# 🥈 GABARIT G2 — VERSION DE DURCISSEMENT CIBLÉ

## 🎯 RÔLE

Utilisé pour :

* corrections architecturales ciblées,
* durcissements en conditions réelles,
* renforcement sans refonte globale.

Exemples historiques :

* v6.1
* certaines v7.3.x critiques

---

## 🧱 STRUCTURE CANONIQUE

1. Préambule obligatoire :

   * « évolution fonctionnelle ciblée »
   * « sans remise en cause des principes fondateurs »

2. Sections par problème traité, avec le pattern :

* Problématique traitée
* Principe introduit (blockquote obligatoire)
* Nouvelle logique métier
* Caractéristiques

3. Section obligatoire :

🧱 CONFORMITÉ AUX PRINCIPES ARSENAL

4. Section finale obligatoire :

✅ ÉTAT FINAL

avec indicateur explicite :

* Dette technique ajoutée : X

---

## 🚫 INTERDITS

* Pas de manifeste doctrinal
* Pas de refonte globale
* Pas de synthèse multi-domaines

---

## 🧠 SIGNATURE

* Mono-domaine profond
* Très causal
* Très technique
* Correctif structurant

---

# 🥉 GABARIT G3 — VERSION DE DOCTRINE / CLARIFICATION SÉMANTIQUE

## 🎯 RÔLE

Utilisé pour :

* clarification sémantique,
* formalisation de vérités métier,
* alignement backend ↔ UI ↔ diagnostic,
* maturation conceptuelle sans rupture fonctionnelle.

Exemples historiques :

* v6.2
* v7.1
* v7.2

---

## 🧱 STRUCTURE CANONIQUE

1. Préambule obligatoire :

   * « ne modifie pas les principes fondateurs »
   * « formalise / clarifie / aligne »

2. Section 1 obligatoire :

🧱 PRINCIPES D’ARCHITECTURE (RAPPEL / FORMALISATION)

3. Sections par domaine, avec le pattern :

* Backend / Décision
* Capteurs métier / explicatifs
* Dashboard / UI
* Recorder / Logbook

4. Section obligatoire :

🧠 COHÉRENCE SYSTÈME & MATURITÉ

5. Section finale obligatoire :

📌 STATUT DE VERSION

---

## 🚫 INTERDITS

* Pas de refonte technique lourde
* Pas de manifeste fondateur
* Pas de synthèse globale multi-domaines

---

## 🧠 SIGNATURE

* Très pédagogique
* Très conceptuel
* Orienté lisibilité humaine
* Alignement backend ↔ UI ↔ historique

---

# 🏅 GABARIT G4 — VERSION MAJEURE STRUCTURÉE / MODERNE

## 🎯 RÔLE

Utilisé pour :

* releases incrémentales gouvernées,
* évolutions multi-domaines,
* extensions de gouvernance,
* stabilisations modernes.

Exemples historiques :

* v7.3
* v7.3.4 / v7.3.5
* v8.0
* v8.1

---

## 🧱 STRUCTURE CANONIQUE

1. En-tête standardisé :

ARSENAL HA vX.Y.Z — STABLE

2. Sections par domaine :

---

## 📌 Domaine — Intitulé

* Liste structurée
* Bullets hiérarchiques
* Aucune narration longue

3. Section obligatoire :

📌 STATUT

* nature de la version
* portée fonctionnelle
* invariants garantis

4. Date de consolidation obligatoire

---

## 🚫 INTERDITS

* Pas de manifeste doctrinal
* Pas de refonte globale
* Pas de récit historique

---

## 🧠 SIGNATURE

* Compact
* Gouvernance claire
* Lisible rapidement
* Multi-domaines

---

# 🧱 RÈGLES D’UNIFORMISATION COSMÉTIQUE (COMMUNES)

Ces règles s’appliquent à **tous** les gabarits,
sans jamais modifier le fond.

---

## 1. En-têtes de version

Canon commun :

==============================
🧠 ARSENAL HA — vX.Y[.Z] [QUALIFICATIF]
=======================================

Qualificatifs autorisés :

* STABLE
* CLOSE
* RÉFÉRENCE
* CONSOLIDATION

---

## 2. Séparateurs de sections

Séparateur canonique unique :

---

## 📌 TITRE DE SECTION

Le séparateur :

==================================================

est réservé exclusivement :

* au début d’une version
* à la fin d’une version

---

## 3. Nommage des sections finales

Sections finales autorisées :

* 📌 STATUT DE VERSION
* 📦 VERSION DE RÉFÉRENCE (G1 uniquement)
* ✅ ÉTAT FINAL (G2 uniquement)

Sections éliminées :

* Impact (non canonique)
* Bénéfices (si redondant avec Statut)

---

## 4. Indicateurs transverses normalisables

Mini-bloc canonique optionnel :

Invariants :

* Aucune régression fonctionnelle connue
* Aucune dette technique ajoutée
* Conforme aux contrats Arsenal applicables

---

## 5. Interdits globaux

* Aucune section supprimée
* Aucune phrase supprimée
* Aucun sens modifié
* Aucune réécriture de fond

Autorisé exclusivement :

* renommage cosmétique de titres
* harmonisation des séparateurs
* hiérarchie visuelle

---

## 6. Principe cardinal

Toute opération d’uniformisation doit respecter :

→ **ZÉRO PERTE D’INFORMATION**

Toute violation de ce principe invalide la consolidation.

---

# 📌 STATUT DU PRÉSENT CONTRAT

* Contrat normatif fondateur
* Opposable à toute consolidation future
* Base unique de normalisation des changelogs Arsenal

Toute évolution de ce document requiert :

* une version G1 ou G3 dédiée
* une justification architecturale explicite
* une absence totale de perte d’information
