# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — SÉMANTIQUE THERMIQUE OFFICIELLE (V3 PRO) · Amendement : terme canonique suspension_relance_meteo
#
# 📌 STATUT :
#   AMENDEMENT au contrat sémantique fondateur
#   `90_semantique_thermique.md`
#
# 🎯 OBJET :
#   Introduire dans la sémantique officielle le terme canonique
#   `suspension_relance_meteo` et sa définition opposable, et
#   acter la distinction conceptuelle entre un `neutre` thermique
#   et un `neutre` issu d'une suspension météo.
#
# 🔒 SUBORDINATION :
#   • 00_gouvernance_chauffage.md (+ amendement)
#   • 01_doctrine_registres.md
#   Cohérent avec : 70_autorisation_thermostat (+ amendement)
#
# ==========================================================

---

## 1. Objet

`90` définit la sémantique de `comfort`, `neutre`, `reduced` et des états
fonctionnels du domaine, mais ne nommait pas la modulation météo présente dans
la couche d'autorisation. Cet amendement comble cette lacune sémantique en
introduisant le terme canonique `suspension_relance_meteo`, conformément au
principe de `90` selon lequel tout terme doit posséder un sens unique et
opposable.

---

## 2. Nouvelle entrée sémantique — `suspension_relance_meteo`

> **Définition canonique.**
> `suspension_relance_meteo` désigne une **modulation de sobriété
> contextuelle** de la couche d'autorisation, qui transforme une intention
> d'autorisation `comfort` en `neutre` lorsque la météo favorable rend une
> relance de chauffe superflue.

Caractéristiques :

- registre : **stabilisation thermique** (cf. `01` D4) ;
- localisation : couche d'autorisation, en sortie de
  `sensor.chauffage_autorisation_cible` ;
- effet unique : `comfort → neutre` ;
- nature : **suspension de relance**, jamais interdiction.

N'EST PAS :

- une interdiction ni un blocage (ne produit jamais `reduced`) ;
- une anticipation temporelle prédictive (ne repose sur aucune date / horaire) ;
- une décision (reste une intention d'autorisation) ;
- une cause de sécurité système.

Dépend exactement de :

- `input_boolean.chauffage_anticipation_meteo` ;
- `binary_sensor.meteo_favorable_chauffage`.

---

## 3. Distinction sémantique : `neutre` thermique vs `neutre` météo

> **Précision sémantique (opposable).**
> Le `neutre` (cf. `90` §3.3) demeure un état unique d'abstention thermique
> volontaire. Toutefois, sa **cause** peut être de deux natures distinctes :
>
> - **`neutre` thermique** : abstention issue du calcul thermique local (zone
>   morte d'hystérésis, confort jugé suffisant) ;
> - **`neutre` météo** : abstention issue d'une `suspension_relance_meteo`
>   (relance suspendue car réchauffement passif attendu).
>
> Ces deux `neutre` sont **conceptuellement distincts par leur cause**, tout
> en produisant une abstention identique pour le moteur décisionnel. La
> distinction est normative pour le diagnostic et l'explication ; elle n'altère
> pas la sémantique unique de l'état `neutre` lui-même.

Cette distinction est **immédiatement normative**. Sa matérialisation runtime
(attribut de traçabilité ou raison dédiée) est une amélioration différée, non
ouverte ici (cf. `70` §5, R-70.6).

---

## 4. Cohérence avec les interdictions sémantiques existantes

L'ajout respecte les interdictions sémantiques de `90` §12 :

- `suspension_relance_meteo` ne réutilise aucun terme existant ;
- elle ne confond pas `neutre` avec une erreur (le `neutre` météo est un état
  normal) ;
- elle ne confond pas `neutre` avec `reduced` (la modulation ne produit jamais
  `reduced`) ;
- elle ne constitue ni un blocage, ni un standby, ni une attente thermique.

---

## 5. Invariants exposés (CI)

- **INV-SEM-METEO-1** — Le terme `suspension_relance_meteo` est l'unique
  désignation canonique de la modulation météo ; aucune autre dénomination
  n'est admise dans les contrats, scripts, logs, UI, diagnostics.
- **INV-SEM-METEO-2** — La modulation désignée par ce terme ne produit que
  `comfort → neutre` (cohérent INV-METEO-1).
- **INV-SEM-METEO-3** — La distinction conceptuelle `neutre` thermique /
  `neutre` météo est reconnue ; aucun document ne traite ces deux causes comme
  identiques au niveau diagnostique.

---

## 6. Dépendances et portée

**Subordonné à :** `00_gouvernance_chauffage.md` (+ amendement) ·
`01_doctrine_registres.md`

**Transversal à :** l'ensemble des contrats Chauffage (comme `90`).

**Cohérent avec :** `70_autorisation_thermostat__amendement.md` (mécanisme).

Cet amendement est sémantique, stable, opposable, et versionné avec `90`. Il
prend effet conjointement avec l'amendement de `70`. Aucun patch runtime n'est
ouvert.

# ==========================================================
