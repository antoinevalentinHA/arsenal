# ==========================================================
# 🧠 ARSENAL — PROJET CHAUFFAGE
# Gouvernance des régimes thermiques
# ==========================================================
#
# Chemin :
# /homeassistant/documentation_arsenal/outils_externes/chat_gpt/cas_d_usage/projet_chauffage/regimes_thermiques.md
#
# Statut : FONDATEUR — GELÉ
# Portée : Chauffage — Segmentation thermique & gouvernance des données
#
# Ce document définit la notion centrale de **régime thermique**
# dans le projet “Observabilité & Auto-Ajustement Thermique”.
#
# Il formalise :
# - la définition d’un régime thermique
# - ses conditions de création et de clôture
# - les règles de segmentation des données
# - les mécanismes d’invalidation et de purge
# - les interdictions structurelles associées
#
# Ce document est contractuel et opposable.
# Toute analyse, agrégation ou auto-ajustement doit s’y conformer.
#
# ==========================================================

# ----------------------------------------------------------
# 🎯 OBJET DU DOCUMENT
# ----------------------------------------------------------

Ce document définit la **gouvernance des régimes thermiques**
utilisés pour structurer l’observabilité et l’analyse inertielle
au sein du projet Chauffage Arsenal.

Objectifs :

* garantir l’homogénéité physique des données analysées
* empêcher tout mélange de dynamiques incompatibles
* assurer une séparation stricte entre courbe de chauffe et offsets
* fournir un cadre robuste pour l’auto-ajustement futur

Ce document s’applique à :

* Phase 1 : Observabilité / Diagnostic
* Phase 2 : Auto-ajustement des offsets

Il est :

* normatif
* stable
* fondation architecturale du projet

# ----------------------------------------------------------
# 🧠 PRINCIPE FONDAMENTAL
# ----------------------------------------------------------

Le comportement thermique du système dépend directement de :

* la pente de la courbe de chauffe
* le parallèle de la courbe de chauffe

Ces deux paramètres définissent une **dynamique thermique globale**
qui conditionne :

* vitesse de montée
* inertie apparente
* overshoot
* durée des cycles

Toute modification de l’un de ces paramètres crée un système physique différent.

Conséquence fondamentale :

> **Les données thermiques ne sont comparables que dans un régime thermique constant.**

# ----------------------------------------------------------
# 🔹 DÉFINITION D’UN RÉGIME THERMIQUE
# ----------------------------------------------------------

Un **régime thermique** est défini par le couple :

* `pente_consigne`
* `parallele_consigne`

Ce couple est considéré comme constant sur une période donnée.

Un régime thermique est caractérisé par :

* une dynamique thermique homogène
* une inertie effective stable
* une relation quasi fixe entre décision et réponse

Chaque régime est identifié par un :

* `regime_id`

unique dans le temps.

# ----------------------------------------------------------
# 🔹 SOURCES DE VÉRITÉ DU RÉGIME
# ----------------------------------------------------------

Les seules entités autorisées à définir un régime sont :

* `input_number.chauffage_pente_consigne`
* `input_number.chauffage_parallele_consigne`

Ces entités sont :

* souveraines
* locales
* persistantes
* uniques sources de vérité

Les capteurs de suggestion :

* `sensor.chauffage_pente_suggeree`
* `sensor.chauffage_parallele_suggeree`

ne participent **jamais** à la définition d’un régime.

# ----------------------------------------------------------
# 🔹 CRÉATION D’UN NOUVEAU RÉGIME
# ----------------------------------------------------------

Un nouveau régime thermique est créé dès que l’une des conditions suivantes est vraie :

## 1️⃣ Modification directe de pente

Si :

* `input_number.chauffage_pente_consigne` change de valeur

→ création immédiate d’un nouveau régime

## 2️⃣ Modification directe de parallèle

Si :

* `input_number.chauffage_parallele_consigne` change de valeur

→ création immédiate d’un nouveau régime

## 3️⃣ Événement auto-ajustement

Si réception de :

* `event: chauffage_adjustment`
* avec `mode = real`

→ création immédiate d’un nouveau régime

Même si les valeurs finales sont identiques aux valeurs précédentes.

## 4️⃣ Redémarrage système (optionnel)

En cas de redémarrage Home Assistant :

* un nouveau régime peut être créé
* ou le régime courant peut être reconstruit

Ce choix relève de l’implémentation.

# ----------------------------------------------------------
# 🔹 CLÔTURE D’UN RÉGIME
# ----------------------------------------------------------

Un régime thermique est clôturé dès qu’un nouveau régime est créé.

À la clôture :

* tous les échantillons en cours sont invalidés
* toute fenêtre glissante est purgée
* toute agrégation est figée

Aucune donnée du régime précédent ne doit être réutilisée
pour le nouveau régime.

# ----------------------------------------------------------
# 🔹 ATTACHEMENT DES ÉCHANTILLONS
# ----------------------------------------------------------

Chaque échantillon thermique contient obligatoirement :

* `regime_id`
* `pente_T0`
* `parallele_T0`

Ces valeurs sont :

* capturées à T0
* immuables pour l’échantillon
* utilisées pour validation ultérieure

Un échantillon dont :

* `pente_T0` ≠ pente courante
  ou
* `parallele_T0` ≠ parallèle courant

est automatiquement invalide.

# ----------------------------------------------------------
# ❌ INTERDICTIONS STRUCTURELLES
# ----------------------------------------------------------

Il est formellement interdit :

* de mélanger des échantillons de régimes différents
* de moyenner inter-régimes
* d’agréger inter-régimes
* d’ajuster des offsets à partir de plusieurs régimes
* de conserver des fenêtres glissantes multi-régimes

Toute violation constitue :

* une anomalie architecturale
* une dette scientifique
* une cause d’instabilité future

# ----------------------------------------------------------
# 🔍 RÈGLES D’EXPLOITATION D’UN RÉGIME
# ----------------------------------------------------------

Un régime est considéré **exploitable** uniquement si :

* âge du régime ≥ 48 h
* N cycles valides ≥ 20
* taux d’invalidation < 30 %

Avant ces seuils :

* les statistiques sont affichables
* mais toute décision automatique est interdite

# ----------------------------------------------------------
# 🧮 FENÊTRES GLISSANTES PAR RÉGIME
# ----------------------------------------------------------

Chaque régime dispose de sa propre fenêtre glissante.

Paramètres canoniques :

* fenêtre primaire : 7 jours
* fenêtre maximale : 14 jours

Règles :

* purge totale à chaque nouveau régime
* aucune conservation brute inter-régimes
* seules les synthèses figées peuvent être archivées

# ----------------------------------------------------------
# 🔒 RÔLE DANS L’AUTO-AJUSTEMENT
# ----------------------------------------------------------

Les régimes thermiques constituent :

* l’unité minimale d’apprentissage
* l’unité minimale de décision

Toute proposition d’auto-ajustement doit :

* porter sur un seul régime
* ignorer totalement les régimes précédents
* vérifier les critères d’exploitabilité

Un ajustement ne doit jamais :

* compenser un ancien régime
* anticiper un futur régime

# ----------------------------------------------------------
# ⚠️ CAS LIMITES ET EXCEPTIONS
# ----------------------------------------------------------

## Régimes très courts

Si durée régime < 24 h :

* régime non exploitable
* données conservées uniquement à titre diagnostic

## Régimes sans cycles suffisants

Si N cycles < seuil :

* affichage autorisé
* décision automatique interdite

## Régimes pollués

Si taux invalidation élevé :

* régime marqué instable
* toute auto-adaptation bloquée

# ----------------------------------------------------------
# 🏁 STATUT
# ----------------------------------------------------------

Document :

* FONDATEUR
* GELÉ
* Référentiel de segmentation thermique officiel

Ce document gouverne directement :

* la validité des statistiques
* la sécurité de Phase 2
* la stabilité à long terme du système

Toute évolution future devra :

* préserver strictement ces principes
* expliciter toute dérogation
* maintenir la séparation courbe / offsets

# ==========================================================
