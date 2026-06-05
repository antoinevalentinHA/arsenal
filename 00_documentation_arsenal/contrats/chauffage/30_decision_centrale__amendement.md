# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — DÉCISION CENTRALE V3 · Amendement : sécurité pure de Niveau 1 & causalité honnête
#
# 📌 STATUT :
#   AMENDEMENT au contrat central `30_decision_centrale.md`
#   NIVEAU : structurant — point de convergence du chemin critique
#
# 🎯 OBJET :
#   Mettre la Décision Centrale en conformité avec la doctrine
#   des registres (`01`). Trois effets normatifs :
#     1. qualifier `binary_sensor.chauffage_autorise_systeme`
#        comme autorité STRICTEMENT sécurité système (Niveau 1) ;
#     2. exclure doctrinalement `input_boolean.chauffage_standby_force`
#        de la composition de Niveau 1 ;
#     3. poser la règle de causalité honnête des `reason` :
#        une stabilisation n'est jamais exposée comme une
#        interdiction système.
#
#   Cet amendement prépare la désintrication runtime (phase 3)
#   sans produire aucun patch runtime.
#
# 🔒 AUTORITÉ :
#   Opposable à toute implémentation de la décision centrale,
#   de ses raisons métier, et de ses miroirs de diagnostic.
#
# ----------------------------------------------------------
# 🧱 SUBORDINATION
#
#   Subordonné à :
#     • 00_gouvernance_chauffage.md
#     • 00_gouvernance_chauffage__amendement.md
#     • 01_doctrine_registres.md
#
#   Cohérent avec :
#     • 50_standby_hysteresis__amendement.md
#     • 40_blocages__amendement.md
#     • 80_table_decision_canonique__reecriture_partielle.md
#
#   Implémente :
#     • 80_table_decision_canonique__reecriture_partielle.md
#
# ==========================================================

---

## 1. Objet et portée

Cet amendement précise, sans réécrire l'algorithme métier de `30`, la nature
des entrées de la hiérarchie décisionnelle et la sémantique des raisons
produites.

Il ne modifie **pas** l'arbitrage métier ni l'ordre des gardes (G1, G3, G4,
G5, G2). Il qualifie les registres des causes lues par la décision et corrige
la causalité diagnostique.

Le contrat `30` n'était pas fautif dans sa structure de décision. La dérive
corrigée ici est strictement la **composition runtime** de
`binary_sensor.chauffage_autorise_systeme`, qui faisait remonter une
conséquence de stabilisation (`standby_force`) en cause de Niveau 1, et la
**raison** qui en résultait.

---

## 2. Qualification de `chauffage_autorise_systeme` (Niveau 1 — sécurité pure)

> **R-30.1 — Autorité strictement sécurité système.**
> `binary_sensor.chauffage_autorise_systeme` est, au sens de la décision
> centrale, une autorité de **sécurité système pure**. Sa valeur `off`
> signifie une et une seule chose : **le chauffage est sous interdiction de
> sécurité** (interdiction système explicite, maintenance, blocage
> post-aération, indisponibilité d'exécution relevant de la sécurité).
>
> Cette valeur doit être interprétable par tout lecteur **sans glose** : `off`
> = interdit. Aucune signification de stabilisation (« il fait assez chaud »,
> « confort suffisant ») ne peut être portée par ce capteur.

> **R-30.2 — Composition doctrinale de Niveau 1.**
> La composition de `chauffage_autorise_systeme` est limitée aux causes de
> sécurité système. En particulier, `input_boolean.chauffage_standby_force`
> **n'entre pas** dans sa composition, ni aujourd'hui ni dans aucune évolution
> future. Toute remontée du standby en Niveau 1 est une violation de D1 et D3
> (cf. `01`).

Justification : le standby est une **conséquence** de l'autorisation thermique
(`50__amendement` A1), donc un objet de registre stabilisation. Le faire
composer un capteur de sécurité fusionne deux registres irréductibles (D0) et
prive le Niveau 1 de sa propriété cardinale d'interprétabilité directe.

---

## 3. Règle de causalité honnête des raisons

> **R-30.3 — Réservation de `chauffage_non_autorise`.**
> La raison métier `chauffage_non_autorise` est **strictement réservée** aux
> interdictions de sécurité système (Niveau 1 réel). Elle ne doit jamais être
> émise pour un état de stabilisation, de sobriété ou de confort suffisant.

> **R-30.4 — Le « confort suffisant / sobriété » relève du Niveau 3.**
> Lorsque le système s'abstient ou réduit parce que le confort est atteint ou
> que la sobriété est nominale (origine : `sensor.chauffage_autorisation_cible`
> = `reduced`, en régime présence), la cause appartient au **Niveau 3** et la
> raison émise est `confort_suffisant`. Ce cas ne doit jamais être confondu
> avec une interdiction de Niveau 1.

> **R-30.5 — Non-déguisement des registres.**
> Aucune raison ne doit présenter une cause de stabilisation comme une
> interdiction de sécurité, ni l'inverse. La raison émise reflète le **registre
> réel** de la cause dominante : sécurité pour les interdictions, stabilisation
> pour les abstentions de confort / sobriété.

Conséquence sur les miroirs de diagnostic : les capteurs explicatifs
(`sensor.chauffage_raison_calculee`, `sensor.chauffage_mode_calcule`) lisent
le même `chauffage_autorise_systeme`. Une fois ce capteur redevenu sécurité
pur, leur branche `chauffage_non_autorise` / `Eco-pour-interdiction` ne se
déclenche plus que sur une vraie interdiction. La correction de la causalité
se propage à l'ensemble des cascades sans réécriture de chacune.

---

## 4. Invariance de l'effet thermique (équivalence comportementale)

> **R-30.6 — Iso-comportement thermique.**
> Le refactor cible (désintrication de `standby_force` hors de
> `chauffage_autorise_systeme`) **ne doit pas modifier l'effet thermique
> attendu** : pour tout contexte, le `desired_mode` produit après refactor est
> identique au `desired_mode` produit avant.
>
> Seule la **causalité diagnostique** (`reason` et miroirs) change : elle
> devient honnête. Le chauffage se comporte exactement comme avant ; il ne
> ment plus sur le pourquoi.

Fondement de l'iso-comportement : l'information « autorisation = reduced en
présence » est déjà disponible au Niveau 3 (branche `confort_suffisant`). Le
câblage de Niveau 1 par le standby était une **duplication** de cette
information, dont une copie était mal étiquetée. Son retrait n'enlève aucune
information décisionnelle — il supprime un doublon trompeur.

---

## 5. Préparation de la désintrication runtime (sans patch)

Cet amendement **prépare** la phase 3 runtime ; il ne la réalise pas. Les
faits runtime suivants, établis et opposables (cf. `01` §9 annexe factuelle),
fondent la sûreté du refactor à venir :

- aucun lecteur cross-domaine de `chauffage_autorise_systeme` ;
- aucun couplage attributaire (les attributs du capteur ne sont lus nulle
  part) ;
- aucune présence en UI ;
- aucune dépendance recorder / history_stats / statistics (les statistiques de
  sobriété sont ancrées sur `sensor.programme_chauffage`, état matériel réel) ;
- aucun trou de réveil décisionnel : tout changement d'autorisation réveille
  déjà la décision centrale via le trigger `sensor.chauffage_autorisation_cible`,
  indépendamment de `chauffage_autorise_systeme` ; le trigger sur
  `chauffage_autorise_systeme` reste utile pour les bascules de sécurité
  (aération), qui ne dépendent pas de l'autorisation.

> **R-30.7 — Garde de re-vérification pré-refactor.**
> Avant exécution de la désintrication runtime, l'ensemble des dépendances de
> `chauffage_autorise_systeme` doit être re-vérifié sur le runtime courant
> (graphe de triggers, recorder). La présente preuve porte sur l'état du
> runtime au moment de l'audit ; toute évolution intermédiaire invalide la
> garantie tant qu'elle n'a pas été re-confirmée.

---

## 6. Interdictions explicites

Il est strictement interdit, au niveau de la Décision Centrale et de ses
miroirs :

- de composer `chauffage_autorise_systeme` par une cause de stabilisation,
  notamment `input_boolean.chauffage_standby_force` ;
- d'émettre `chauffage_non_autorise` pour un état de stabilisation, de
  sobriété ou de confort suffisant ;
- de présenter une cause de stabilisation comme une interdiction de sécurité
  (ou l'inverse) dans une raison ou un miroir de diagnostic ;
- de modifier l'effet thermique (`desired_mode`) à l'occasion du refactor de
  causalité ;
- de faire remonter une conséquence décisionnelle (standby, autorisation
  appliquée) en entrée d'une couche amont (violation D3).

---

## 7. Invariants exposés (CI)

Formulations stables, destinées à être vérifiées structurellement.

- **INV-30-1** — `binary_sensor.chauffage_autorise_systeme` ne dépend que de
  causes de sécurité système ; `input_boolean.chauffage_standby_force` n'entre
  pas dans sa composition. *(aligné INV-STANDBY-2, INV-D1)*
- **INV-30-2** — La raison `chauffage_non_autorise` n'est atteignable que sous
  la condition Niveau 1 (sécurité). Aucune branche de stabilisation ne peut la
  produire.
- **INV-30-3** — Le cas « présence ∧ autorisation cible = reduced » produit la
  raison `confort_suffisant` (Niveau 3), jamais `chauffage_non_autorise`.
- **INV-30-4** — Aucune raison n'associe une cause de stabilisation à une
  sémantique d'interdiction système (non-déguisement des registres).
- **INV-30-5** — Équivalence comportementale : pour tout contexte, le
  `desired_mode` est invariant par le refactor de désintrication (seule la
  `reason` évolue).
- **INV-30-6** — Cohérence des miroirs : `sensor.chauffage_raison_calculee` et
  `sensor.chauffage_mode_calcule` dérivent de la même hiérarchie que la
  décision et ne produisent aucune raison interdite par INV-30-2/3/4.

*(Les invariants racine INV-D1 / INV-D3 de `01` et INV-STANDBY-1/2/4 de `50`
s'appliquent également.)*

---

## 8. Impact attendu sur le runtime cible (descriptif, non prescriptif)

À titre de spécification d'intention pour la phase 3, sans constituer un
patch :

- **Composition de `chauffage_autorise_systeme`** : retrait de la composante
  `standby_force` ; le capteur ne reflète plus que les causes de sécurité.
- **`desired_mode`** : inchangé dans tous les contextes **par le seul refactor de
  désintrication CH-2** (R-30.6). Cette invariance est relative à CH-2 ; elle
  n'interdit pas une évolution thermique ultérieure décidée par un chantier
  métier distinct et explicitement documenté (cf. §10).
- **`reason` (décision + miroirs)** : le cas « confort suffisant » cesse de
  produire `chauffage_non_autorise` et produit `confort_suffisant` (Niveau 3).
  Correction propagée simultanément aux quatre cascades par lecture commune du
  capteur purifié.
- **Observabilité** : `standby_force` demeure historisé et exposé
  (INV-STANDBY-4) — aucune perte d'observabilité.
- **Effet visible** : toute statistique ou notification comptant les
  occurrences de `chauffage_non_autorise` verra sa valeur évoluer. Il s'agit
  d'une **correction de sémantique**, non d'une régression ; à annoncer comme
  telle dans le changelog.

---

## 9. Portée et stabilité

Cet amendement est structurant, stable long terme, opposable, et versionné
avec `30`. Sa publication clôt le chemin critique documentaire et déverrouille
formellement la phase 3 (désintrication runtime), sous réserve de la garde de
re-vérification R-30.7.

---

## 10. Articulation avec le chantier « Vacances sur l'effectivité » (VAC-IMP-1)

Le chantier VAC-IMP-1 fait consommer au régime d'absence chauffage l'effectivité
`binary_sensor.vacances_actives` au lieu de la projection
`input_select.mode_maison`. Il s'agit d'un **changement de `desired_mode`
intentionnel, postérieur et distinct** du refactor de désintrication CH-2.

- R-30.6, §6 et INV-30-5 conservent toute leur valeur **pour le périmètre CH-2** :
  la désintrication de `standby_force` n'a pas modifié `desired_mode`.
- VAC-IMP-1 modifie délibérément `desired_mode` dans le seul contexte
  « projection Vacances ∧ présence réelle » (correction de S-CHAUFFAGE-PRESENCE),
  conformément à [`vacances.md`](../vacances.md) §10. Ce changement est **hors du champ
  d'invariance de CH-2** et n'en constitue pas une violation.
- **Invariant structurel maintenu (permanent, indépendant de CH-2) :**
  l'isomorphisme des gardes de tête entre les axes `desired_mode` et `reason` de
  la Décision Centrale (R-ISO-1 ; INV-30-5 au sens « équivalence de squelette »)
  reste **obligatoire** après VAC-IMP-1. Le changement de la garde Vacances doit
  donc être appliqué **identiquement** aux deux axes.
- **Garde de re-vérification (R-30.7) applicable :** avant tout patch runtime,
  le graphe de dépendances de `decision_centrale.yaml` est re-vérifié sur le
  runtime courant.

---

# ==========================================================
