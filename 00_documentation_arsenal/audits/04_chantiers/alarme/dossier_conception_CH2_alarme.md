# ==========================================================
# 🧠 ARSENAL — DOSSIER DE CONCEPTION
#     Chantier CH-2 — Cerveau décisionnel : autorité des helpers & propreté
# ==========================================================

## 📌 Cadre

- **Chantier** : CH-2 (racine « Cerveau décisionnel : autorité des helpers & propreté logique »).
- **Lots couverts** : **ALM-IMP-2** (autorité/observabilité de `alarme_raison`) + **ALM-MIN-4** (code mort dans le cerveau).
- **Position dans le plan** : chantier **déclencheur** (aucune dépendance amont), **prérequis de CH-1 et CH-3**, **non bloqué** par une validation runtime (V2 est confirmatoire).
- **Interdits respectés** : aucun patch, aucun YAML, aucun code, aucune correction. Le dossier expose la revue, le périmètre, les impacts, les risques, les **décisions à prendre** et les **options**, sans trancher.

---

## 🏛️ Revue architecturale

### Rappel des constats

- **ALM-IMP-2** — le cerveau calcule une variable `raison` mais ne la publie jamais ; ce sont les scripts d'armement/désarmement qui écrivent `input_text.alarme_raison` (`"armement"` / `"desarmement"`). L'alerte d'incohérence affiche ce helper, donc une raison trompeuse en cas d'incident. Contradiction d'autorité avec le contrat 30.
- **ALM-MIN-4** — variable `alarme_etat` calculée et inutilisée dans le cerveau ; condition `… and not presence_securite` de la branche `DELAI_ENTREE` toujours vraie à ce stade.

### État des lieux factuel (qui écrit / qui lit)

| Helper | Écrivain réel (runtime) | Consommateur(s) réel(s) |
|--------|-------------------------|-------------------------|
| `input_text.alarme_decision` (code machine) | Cerveau `decision_centrale.yaml` | **Aucun** consommateur runtime/UI détecté |
| `input_text.alarme_etat_cible` (intention) | Cerveau `decision_centrale.yaml` | `application_decision_centrale.yaml` (snapshot), `alerte_incoherence.yaml` (divergence), `carte_alarme_decision.yaml`, `dashboards/alarme.yaml` |
| `input_text.alarme_raison` (justification) | `armement.yaml`, `desarmement.yaml` | `alerte_incoherence.yaml` (message), `carte_alarme_decision.yaml` |

Trois faits structurants ressortent :

1. **Confusion sémantique sur `alarme_raison`.** Le helper porte aujourd'hui deux concepts incompatibles : la **raison décisionnelle** (pourquoi le cerveau a choisi la cible — ce que visent les contrats 10/30/40) et le **marqueur du dernier acte d'application** (`armement`/`desarmement` — ce que produit le runtime). Les deux ne peuvent pas cohabiter dans un même champ sans ambiguïté.
2. **`alarme_decision` est publié sans lecteur.** Le code décisionnel machine est écrit par le cerveau mais n'est consommé nulle part. La « vraie » trace décisionnelle existe donc déjà, mais elle est inerte.
3. **`alarme_etat_cible` est le helper porteur.** Il est lourdement consommé (application + divergence + UI). Il n'entre **pas** dans le périmètre de CH-2 : y toucher relèverait du contrat d'application (territoire CH-1).

### Invariant Arsenal en jeu

- **Autorité d'écriture unique par helper** (contrat 30 : « helpers exclusivement écrits par le cerveau » ; « interdit d'écrire `alarme_*` depuis une automation/script »).
- **Séparation décision / application** (gouvernance) : la décision *publie une intention*, l'application *exécute*. Or aujourd'hui l'application **écrit un helper décisionnel** — inversion d'autorité.
- **Non-exécutoire** (contrat 10 : la raison est informative, jamais un trigger). Cet invariant **réduit le risque** : quelle que soit l'option retenue, `alarme_raison` n'a aucun pouvoir causal sur l'armement.

---

## 🎯 Périmètre exact

### Dans le périmètre

- **Sémantique et autorité d'écriture de `input_text.alarme_raison`.**
- **Statut de `input_text.alarme_decision`** (trace décisionnelle consommée vs audit pur non lu).
- **Publication (ou non) de la raison décisionnelle par le cerveau.**
- **Nettoyage du code mort du cerveau** (variable `alarme_etat`, condition redondante de `DELAI_ENTREE`) — lot MIN-4.
- **Alignement documentaire** des contrats et en-têtes décrivant ces helpers.
- **Coordination des deux consommateurs** de `alarme_raison` (alerte d'incohérence, carte décision).

### Hors périmètre (à ne pas toucher dans CH-2)

- **`input_text.alarme_etat_cible`** : helper porteur de l'application (CH-1 / contrat d'application).
- **Logique d'intrusion, délai d'entrée, sirène, blocage** : autres chantiers.
- **Clause `person.* == 'Zone maison'`** de `presence.yaml` : **domaine Présence**, hors domaine Alarme — à traiter ailleurs même si signalée en MIN-4.
- **Attribut `raison` du capteur `binary_sensor.alarme_systeme_coherent`** : concept **distinct** (raison de cohérence), non lié à `input_text.alarme_raison` — à ne pas confondre.
- **Entrées du cerveau** (mode, présence, blocages, délai) : non modifiées.

---

## 📁 Fichiers impactés

> Impact = potentiellement modifié **ou** à coordonner. Aucune modification n'est proposée ici.

| Fichier | Rôle | Type d'impact |
|---------|------|---------------|
| `10_scripts/alarme/decision_centrale.yaml` | Cerveau (calcul + publication) | **Cœur** : publication éventuelle de la raison ; nettoyage code mort (MIN-4) |
| `10_scripts/alarme/armement.yaml` | Application armement | Écrivain actuel de `alarme_raison` → statut à arbitrer |
| `10_scripts/alarme/desarmement.yaml` | Application désarmement | Écrivain actuel de `alarme_raison` → statut à arbitrer |
| `04_input_texts/alarme/raison.yaml` | Définition + doctrine du helper | En-tête « écrit par » à réaligner |
| `04_input_texts/alarme/decision.yaml` | Définition du helper code machine | Statut de consommation à clarifier |
| `11_automations/alarme/system/alerte_incoherence.yaml` | Alerte d'incident (consommateur) | Affiche `alarme_raison` ; cible d'affichage à reconsidérer |
| `19_button_card_templates/40_dashboards/alarme/30_diagnostic/carte_alarme_decision.yaml` | UI diagnostic (consommateur) | Affiche `alarme_raison` (fallback `|| ''` présent) |
| *(Option 2 uniquement)* nouveau helper « dernier acte / origine application » | Marqueur d'application | Création + consommateurs + recorder à définir |

> `dashboards/alarme.yaml` consomme `alarme_etat_cible` (hors périmètre) — cité pour mémoire, non impacté par CH-2.

---

## 📜 Contrats impactés

| Contrat | Énoncé en tension | Impact CH-2 |
|---------|-------------------|-------------|
| `30_decision_centrale.md` (interfaces) | `alarme_raison` **écrit exclusivement** par le cerveau ; interdit d'écrire `alarme_*` depuis un script | À confirmer ou amender selon l'option |
| `40_application_decision.md` (décision pure) | `alarme_raison` listée en **sortie obligatoire** du cerveau | À confirmer ou amender selon l'option |
| `10_modele_etats_et_vocabulaire.md` | `alarme_raison` = justification humaine, alignée sur le code décisionnel, **non exécutoire** | Cadre la sémantique cible ; à préserver |
| `04_input_texts/alarme/raison.yaml` (en-tête) | « écrit par scripts d'armement/désarmement **ET** decision_centrale » | Contradiction interne avec 30 → à lever |

> Rappel : `20_interfaces_contexte_et_helpers.md` et `30/40` sont aussi affectés par la dette documentaire **ALM-DOC-1** (décalage des en-têtes). Le réalignement formel relève de **CH-5** ; CH-2 ne fait que **fixer la doctrine** que CH-5 retranscrira.

---

## ⚠️ Risques

- **Risque d'observabilité (principal)** : changer l'écrivain ou la sémantique de `alarme_raison` modifie le contenu de l'alerte d'incident et de la carte diagnostic. À vérifier : la carte tolère une valeur vide (fallback présent) ; l'alerte interpole la valeur dans un texte (sans pouvoir causal). Aucun blocage technique attendu, mais **revue des consommateurs nécessaire**.
- **Risque de perte d'information** : si l'écriture par les scripts d'application est retirée (Option 1), le marqueur « dernier acte + origine » disparaît. Décider s'il doit survivre ailleurs (les en-têtes des scripts le qualifient de « mémoire métier minimale »).
- **Risque de couplage / surface** (Option 2) : un helper supplémentaire implique recorder, restore_state, et de nouveaux consommateurs.
- **Risque doctrinal** (Option 3) : acter `alarme_raison` comme marqueur d'application contredit l'intention des contrats 10/40 et **ne corrige pas** l'observabilité d'incident — il faudrait alors rediriger l'alerte vers `alarme_decision`.
- **Risque de double édition du cerveau** : CH-3 (babysitting) éditera aussi `decision_centrale.yaml`. **Séquencer CH-2 avant CH-3** pour éviter les conflits.
- **Risque de sécurité directe** : **nul** — le cerveau ne pilote rien et `alarme_raison` est non-exécutoire (contrat 10). C'est ce qui classe CH-2 en risque « moyen » (observabilité) et non « élevé ».

---

## 🧭 Décisions d'architecture à prendre

1. **D1 — Que représente `input_text.alarme_raison` ?** Raison décisionnelle (concept du cerveau) ou marqueur du dernier acte d'application — **un seul** des deux.
2. **D2 — Qui en est l'écrivain canonique unique ?** Cerveau, scripts d'application, ou (cas scindé) deux écrivains pour deux helpers distincts.
3. **D3 — L'information « dernier acte + origine » doit-elle être conservée ?** Si oui, dans quel helper et sous quelle autorité.
4. **D4 — Quel statut pour `alarme_decision` (publié sans lecteur) ?** Promu en trace décisionnelle consommée, ou assumé comme audit pur non lu.
5. **D5 — Vers quoi pointe l'alerte d'incohérence pour exposer la cause réelle ?** `alarme_raison` (si raison décisionnelle), `alarme_decision`, ou une combinaison.
6. **D6 — Séquencement du lot MIN-4** : exécuté isolément (quick win indépendant) ou groupé avec IMP-2 (passe unique sur le cerveau).

---

## 🔀 Options possibles

> Présentées à plat, avec compromis. Aucune n'est recommandée ; le choix relève de D1–D5.

### Option 1 — Raison décisionnelle, autorité unique au cerveau

- **Principe** : le cerveau devient l'écrivain exclusif de `alarme_raison` (raison décisionnelle) ; les scripts d'application cessent d'y écrire.
- **Avantages** : conforme aux contrats 30/40 existants ; restaure l'observabilité décisionnelle (l'alerte d'incident affiche la vraie cause) ; supprime l'inversion d'autorité.
- **Inconvénients** : perte du marqueur « dernier acte + origine » (à réaffecter si jugé utile — D3).
- **Surface** : cerveau + 2 scripts d'application + 2 consommateurs + en-tête `raison.yaml`.

### Option 2 — Deux helpers séparés (séparation des préoccupations)

- **Principe** : `alarme_raison` = raison décisionnelle (cerveau, exclusif) ; **un nouveau helper** porte le dernier acte d'application + origine (scripts d'application).
- **Avantages** : sépare proprement décision et application ; conserve les deux informations ; pleinement aligné sur la doctrine de séparation Arsenal.
- **Inconvénients** : +1 helper (recorder, restore, UI, contrat à écrire) ; surface et coût de maintenance accrus.
- **Surface** : la plus large des trois options.

### Option 3 — Documenter le runtime : raison = marqueur d'application

- **Principe** : acter `alarme_raison` comme marqueur d'application (statu quo runtime) ; retirer la raison des sorties exclusives du cerveau (amender 30/40) ; réhabiliter `alarme_decision` comme trace décisionnelle consommable.
- **Avantages** : changement runtime minimal ; aligne le contrat sur le runtime (principe « le runtime est la référence »).
- **Inconvénients** : ne corrige **pas** l'objectif d'observabilité de CH-2 tant que l'alerte d'incident n'est pas redirigée vers `alarme_decision` (D5) ; contredit l'intention des contrats 10/40 ; impose un amendement contractuel plus lourd.
- **Surface** : faible côté runtime, mais notable côté contrats + redirection de l'alerte.

### Lot MIN-4 (transverse aux options)

- Suppression de la variable `alarme_etat` inutilisée et simplification de la condition redondante de `DELAI_ENTREE` : **sans changement de comportement**, risque faible. Réalisable isolément (quick win) ou dans la même passe que l'option retenue.

---

## ❓ Questions ouvertes

- **Q1** — L'information « dernier acte d'application + origine » a-t-elle un consommateur réel ou prévu (UI, historique, audit) ? Sa conservation conditionne le choix entre Option 1 et Option 2.
- **Q2** — `alarme_decision` doit-il devenir la trace décisionnelle consommée (et par qui), ou rester un diagnostic d'audit non lu assumé ?
- **Q3** — Faut-il lever la **collision de vocabulaire** « raison » entre `input_text.alarme_raison` et l'attribut `raison` du capteur de cohérence (clarification conceptuelle / nommage) ?
- **Q4** — La raison décisionnelle doit-elle conserver le mapping code→texte déjà présent dans le cerveau (alignement contrat 10), ou être enrichie ?
- **Q5** — Le réalignement des contrats 30/40 (et la dette ALM-DOC-1) est-il porté par CH-2 (doctrine) puis CH-5 (rédaction), ou regroupé ?

---

## 🔬 Validation runtime de cadrage (V2 — confirmatoire, non bloquante)

Avant l'arbitrage D1–D5, observer à chaud :

- la valeur réellement portée par `input_text.alarme_raison` en exploitation (confirmer qu'elle vaut `armement`/`desarmement` et jamais la raison riche) ;
- le contenu réel de la notification de l'alerte d'incohérence lors d'une divergence ;
- la confirmation que `input_text.alarme_decision` n'a aucun consommateur actif.

> V2 ne bloque pas le chantier (le constat est *Confirmé* statiquement) ; elle sécurise le choix d'option et la rédaction de la doctrine cible.

---

## 🔗 Articulation avec les autres chantiers

- **Amont de CH-1** : si l'« intrusion confirmée » (cible §9) devient un helper, son autorité d'écriture devra suivre la **même doctrine** que celle fixée ici. CH-2 doit donc **précéder** la conception de cet état.
- **Amont de CH-3** : CH-3 ajoutera une branche d'inhibition au cerveau ; un cerveau **déjà nettoyé** (MIN-4) et à **doctrine de sortie stabilisée** réduit le risque de conflit.
- **Vers CH-5** : la doctrine retenue ici alimente le réalignement contractuel (contrats 30/40, en-tête `raison.yaml`) que CH-5 retranscrira.

---

*Fin du dossier de conception CH-2. Aucun code, aucun YAML, aucune correction. Les décisions D1–D6 et les questions Q1–Q5 restent ouvertes ; elles déterminent l'option retenue et le périmètre final.*
