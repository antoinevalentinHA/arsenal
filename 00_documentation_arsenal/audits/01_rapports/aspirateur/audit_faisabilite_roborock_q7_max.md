# 🤖 ARSENAL — AUDIT — Faisabilité d'un pilotage **Roborock Q7 Max**

> **Trace d'audit runtime, strictement lecture seule.** Aucune action Home Assistant appelée, aucun paramètre modifié, aucune commande envoyée au robot. Aucun contrat, script, helper, automation, dashboard ni checker créé.
> Convention : **[FAIT]** observé dans le runtime · **[HYP]** inférence non prouvée · **[RECO]** à arbitrer par l'opérateur.
> Ce document est un **relevé d'observation**, pas un contrat. Il n'est ni normatif ni opposable.

---

## Verdict

**`GO AVEC RÉSERVES` — faisabilité native très probable, qualification terrain minimale requise.**

L'expérience cible — *choisir un périmètre, choisir un profil, appuyer sur **Lancer*** — est **structurellement réalisable** avec les primitives natives observées : `vacuum.clean_area` accepte une sélection **multiple** de pièces, la puissance d'aspiration est réglable, le mode `vacuum` / `vac_and_mop` et l'intensité d'eau (`off` … `high`) sont exposés, `pause` / `stop` / `return_to_base` sont supportés, et deux témoins indépendants permettent de détecter un cycle en cours.

Les inconnues restantes portent sur le **comportement multi-cartes**, la **correspondance areas HA ↔ segments Roborock** et la **séquence runtime exacte** (délais d'application des réglages). Elles appellent une qualification terrain ciblée ; elles ne rendent pas la faisabilité indéterminée.

---

## 1. Date, contexte et périmètre

| | |
|---|---|
| **Date d'observation** | 2026-08-25 |
| **Contexte** | Étude d'opportunité préalable à tout chantier. Aucun besoin runtime ouvert à ce jour. |
| **Nature** | Audit **strictement read-only** du runtime Home Assistant + recherche d'antériorité dans le dépôt. |
| **Méthode** | Lecture des états, du registre d'entités, du registre d'appareils, du registre d'areas et du registre de services depuis le frontend HA. Aucune action appelée, aucun formulaire enregistré, aucun flux d'options ouvert. |
| **Preuve de non-commande** | Cf. §10. |

**Antériorité dans le dépôt [FAIT]** — le domaine n'existe pas :

- aucun contrat, aucun dashboard, aucune entrée de navigation, aucun script, aucun helper ;
- **un seul consommateur en production** : `binary_sensor.roborock_q7_max_nettoyage` sert de condition d'exclusion à la détection d'intrusion — [`contrats/alarme/50_intrusion_detection.md`](../../../contrats/alarme/50_intrusion_detection.md) et `11_automations/alarme/intrusion/mouvement.yaml`. **Cet invariant est à préserver** par tout chantier futur ;
- `logger.yaml` porte déjà un bloc de journalisation Roborock.

---

## 2. Runtime observé

| Élément | Valeur observée | Preuve |
|---|---|---|
| Version Home Assistant | **2026.8.3** | [FAIT] |
| Modèle | **Roborock Q7 Max** (`roborock.vacuum.a38`), firmware `02.09.18` | [FAIT] |
| Appareils exposés | **2** : le robot et son dock. **Un seul robot.** | [FAIT] |
| Intégration | `roborock` **native** (core HA), `integration_type: hub`, `quality_scale: silver` | [FAIT] |
| Classe d'E/S | **`local_polling`** — l'appareil est joignable localement et interrogé en polling | [FAIT] |
| Appairage | Config entry créé à partir d'un **compte cloud Roborock** ; l'entrée est chargée et saine | [FAIT] |
| Disponibilité | Robot **en ligne** au moment de l'audit ; aucun *repair* ni *issue* ouvert | [FAIT] |
| Entités du device | **45** au registre — **19 actives**, **26 désactivées** | [FAIT] |

> **[FAIT] Nuance cloud / local.** L'intégration est déclarée `local_polling` et le robot dispose d'une adresse locale connue de HA : le pilotage courant ne transite pas systématiquement par le cloud. Le compte cloud reste nécessaire à l'appairage. La répartition exacte local/cloud **selon l'opération** n'a pas été établie.

---

## 3. Entités et capacités utiles

### 3.1 Commande et état

| Rôle | Entité / service | Valeurs ou état observés |
|---|---|---|
| Aspirateur | `vacuum.roborock_q7_max` | `idle` |
| Aspiration | `vacuum.set_fan_speed` (attribut `fan_speed`) | `quiet` · `balanced` · `turbo` · `max` · `gentle` — courant : `max` |
| Nettoyage par pièces | `vacuum.clean_area` | champ `cleaning_area_id` **requis**, sélecteur d'**areas HA** avec **`multiple: true`** et **`reorder: true`** |
| Mode | `select.entree_roborock_q7_max_mode_de_nettoyage` | `vacuum` · `vac_and_mop` — courant : `vac_and_mop` |
| Intensité d'eau | `select.roborock_q7_max_intensite_de_frottement` | `off` · `low` · `medium` · `high` · `custom_water_flow` — courant : `medium` |
| Parcours de lavage | `select.roborock_q7_max_parcours_de_lavage_de_sol` | `standard` · `deep` · `deep_plus` — **état `unknown`** |
| Interruption | `vacuum.pause` · `vacuum.stop` · `vacuum.return_to_base` | supportés |
| Autres services natifs | `clean_spot`, `locate`, `send_command` ; côté `roborock` : `get_maps`, `get_vacuum_current_position`, `set_vacuum_goto_position`, `set_vacuum_zoned_cleaning` | disponibles, non appelés |

**[FAIT] Toutes les capacités requises sont déclarées supportées par l'appareil.** Le contrôle des bits de capacité exigés par chaque service (`start`, `pause`, `stop`, `return_to_base`, `clean_area`, `locate`) est **satisfait** pour cette entité.

### 3.2 Observation

| Rôle | Entité | État observé |
|---|---|---|
| État machine | `sensor.roborock_q7_max_etat` | `charger_disconnected` — énumération riche incluant `cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, `returning_home`, `docking`, `charging`, `error`, `device_offline` |
| Cycle en cours | `binary_sensor.roborock_q7_max_nettoyage` | `off` |
| Batterie | `sensor.roborock_q7_max_batterie` | `75 %` |
| Progression | `sensor.roborock_q7_max_duree_de_nettoyage` · `sensor.roborock_q7_max_surface_de_nettoyage` | `24,4 min` · `12,2` |
| Pièce courante | `sensor.roborock_q7_max_piece_actuelle` | énumère les segments de la **carte active** (cf. §5) |
| En charge | `binary_sensor.roborock_q7_max_en_charge` | `off` |

**[FAIT] Deux témoins indépendants et concordants** permettent de détecter un cycle en cours (`binary_sensor.…_nettoyage` et `sensor.…_etat`) — matière suffisante pour une garde anti-double-lancement.

### 3.3 Prérequis matériels observables

| Prérequis | Entité | État observé |
|---|---|---|
| Serpillière fixée | `binary_sensor.roborock_q7_max_serpilliere_fixee` | **`off`** — aucune serpillière posée |
| Réservoir d'eau fixé | `binary_sensor.roborock_q7_max_reservoir_d_eau_fixe` | `on` |
| Pénurie d'eau | `binary_sensor.entree_roborock_q7_max_penurie_d_eau` | `off` |
| Séchage serpillière (dock) | `binary_sensor.entree_roborock_q7_max_dock_sechage_de_la_serpilliere` | `off` |

**[FAIT] Les prérequis matériels des profils avec eau sont observables.** Ils ne sont pas commandables : poser ou retirer la serpillière est un **geste opérateur**.

### 3.4 Prérequis runtime réversibles

**[FAIT] Trois entités utiles au chantier sont désactivées par l'utilisateur — supportées par l'intégration, donc réactivables.** Ce ne sont pas des blocages techniques.

| Entité désactivée | Ce qu'elle apporterait |
|---|---|
| `select.roborock_q7_max_carte_selectionnee` | Sélection explicite de la carte active |
| `sensor.roborock_q7_max_erreur_de_l_aspirateur` | Motif d'erreur détaillé du robot |
| `sensor.roborock_q7_max_dock_erreur_de_dock` | Motif d'erreur du dock |
| `sensor.roborock_q7_max_debut_du_dernier_nettoyage` / `…_fin_du_dernier_nettoyage` | Bornes natives d'une session |

**[FAIT] Un diagnostic minimal honnête est déjà possible sans elles**, à partir de l'état général du robot, du caractère `unknown` / `unavailable` des entités, du cycle en cours et des prérequis matériels. Les capteurs détaillés **amélioreront** ce diagnostic après réactivation ; ils ne le conditionnent pas.

---

## 4. Cartes observées

**[FAIT] Quatre cartes, un seul robot.** Elles sont exposées comme entités `image` :

| Carte | Entité |
|---|---|
| RDC | `image.roborock_q7_max_rdc` |
| Étage | `image.roborock_q7_max_etage` |
| Annexe | `image.roborock_q7_max_annexe` |
| Garage | `image.roborock_q7_max_garage` |

**[FAIT] Le robot est à sa capacité maximale de cartes (4 sur 4).** Aucune carte supplémentaire n'est créable sans en détruire une.

**[FAIT] Le multi-cartes est supporté par le matériel** (bascule de carte et minuteries par segment multi-cartes déclarées comme capacités de l'appareil).

**[HYP] La carte active au moment de l'audit est l'Étage**, d'après les segments énumérés par `sensor.roborock_q7_max_piece_actuelle`. La correspondance entre l'index interne d'une carte et son nom n'est pas observable en lecture seule.

**[FAIT] Les trois périmètres métier visés sont portés par trois cartes distinctes** — Petite maison / Annexe, RDC, Étage.

---

## 5. Pièces observées et divergences de nommage

Trois référentiels distincts coexistent et **ne doivent pas être confondus** :

1. la **pièce Roborock** — un segment nommé dans une carte du robot ;
2. l'**area Home Assistant** — l'unité que consomme `vacuum.clean_area` ;
3. le **périmètre métier Arsenal** (`RDC`, `Étage`, `Petite maison`…) — une **composition contractuelle** de pièces, qui n'a pas vocation à devenir une area HA.

### 5.1 Segments observés sur la carte active (Étage)

**[FAIT]** `Pallier` · `Chambre Parents` · `Chambre Arnaud` · `Chambre Matthieu` · `Dressing` · `SDB Parents` · `WC Étage` · `SDB Enfants`.

Les segments des cartes RDC, Annexe et Garage **n'ont pas pu être relevés** : seule la carte active énumère ses pièces.

### 5.2 Areas Home Assistant

**[FAIT] 14 areas**, créées manuellement à l'été 2025, sans alias ni libellé particulier, réparties sur trois étages (`RDC`, `Premier`, `Cave`) :

`All House` · `Cave` · `Chambre Enfants` · `Chambre parents` · `Cage d'escaliers` · `Entrée` · `Garage` · `Jardin` · `Palier` · `Petite Maison` · `Salle de jeux` · `SDB enfants` · `SDB parents` · `Séjour`.

**[FAIT] Aucun lien observable entre les areas HA et les segments Roborock** : les areas ne portent ni alias ni marquage issus de l'intégration.

### 5.3 Divergences relevées

| Nature | Détail | Gravité |
|---|---|---|
| **Noms périmés côté Roborock** | La carte Étage porte encore **`Chambre Arnaud`** et **`Chambre Matthieu`** — noms proscrits. Les noms attendus sont `Chambre Enfants` et `Salle de Jeux`. | **À corriger dans l'application Roborock avant conception de l'UI.** Anomalie de référentiel, pas impossibilité architecturale. |
| **Faute d'orthographe** | `Pallier` côté Roborock (double L) vs `Palier` côté HA. | À corriger dans l'application Roborock. |
| **Casse** | `Chambre parents`, `SDB enfants`, `SDB parents`, `Salle de jeux` côté HA vs noms canoniques Arsenal. | Mineur, à arbitrer. |
| **Pluriel** | `Cage d'escaliers` côté HA vs `Cage d'escalier` attendu. | Mineur, à arbitrer. |
| **Pièces sans area HA** | `Dressing` **existe réellement** dans la carte Étage ; `WC Étage` également ; aucune area HA ne leur correspond. Le `WC` du RDC n'a pas d'area HA. `Petite Maison` est une area unique, non découpée en `Chambre` et `Salle de bain`. | Préparation runtime limitée : création ou ajustement de quelques areas. |

> **[RECO] Règle de restitution.** L'UI Arsenal ne devra **jamais** restituer silencieusement les anciens noms (`Chambre Arnaud`, `Chambre Matthieu`, `Pallier`). Toute pièce affichée doit l'être sous son nom canonique Arsenal, ou pas du tout.

> **[FAIT] Divergence interne au runtime, à consigner.** Deux listes de pièces coexistent dans l'intégration et ne se recouvrent pas : celle des segments de la carte active (8 entrées, noms d'étage) et une liste courte issue du compte (4 entrées : `Salle de bain`, `Ext`, `Chambre1`, `Chambre`). Laquelle alimente la résolution de `clean_area` n'est pas observable sans exécution.

---

## 6. Les quatre profils métier envisagés

Valeurs réellement exposées, sans traduction métier inventée.

| Profil | Aspiration | Eau / lavage | Faisabilité | Réserve |
|---|---|---|---|---|
| **1 — forte / pas d'eau** | `turbo` ou `max` | `mode = vacuum` et/ou `intensité = off` | Valeurs disponibles | Correspondance « forte » → `turbo` **ou** `max` à arbitrer ; sémantique de « pas d'eau » à qualifier |
| **2 — normale / pas d'eau** | `balanced` [HYP] | idem profil 1 | Valeurs disponibles | « normale » → `balanced` est une inférence lexicale, non une preuve |
| **3 — faible / eau moyenne** | `quiet` ou `gentle` | `mode = vac_and_mop` + `intensité = medium` | Valeurs disponibles | **Non commandable tant que la serpillière est absente** |
| **4 — faible / eau importante** | `quiet` ou `gentle` | `mode = vac_and_mop` + `intensité = high` | Valeurs disponibles | Idem profil 3 ; `high` plutôt que `custom_water_flow` à arbitrer |

### 6.1 Le point « pas d'eau »

**[FAIT] Deux leviers exposés peuvent porter l'intention, sans qu'aucun ne soit établi comme faisant autorité** : le mode de nettoyage (`vacuum`) et l'intensité de frottement (`off`). Le parcours de lavage n'offre **aucune valeur « aucun »** — il n'exprime pas l'absence de lavage. L'absence physique de serpillière est un **état matériel non commandable**, donc jamais un moyen de réaliser un profil.

**[RECO]** Un seul levier devra être retenu comme writer de l'intention « pas d'eau ». Deux writers concurrents sur une même intention seraient un anti-patron.

### 6.2 Serpillière absente — condition matérielle, pas blocage

**[FAIT]** `binary_sensor.roborock_q7_max_serpilliere_fixee = off` au moment de l'audit.

C'est une **condition matérielle normale à représenter explicitement**, relevant de la commandabilité (impossibilité physique, catégorie A de [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)) :

- profils **sans eau** (1 et 2) : potentiellement autorisables ;
- profils **avec eau** (3 et 4) : **refus explicite** assorti d'un motif lisible tant que la serpillière est absente.

Le dashboard reste donc réalisable ; il doit simplement dire la vérité sur ce qu'il ne peut pas lancer.

### 6.3 Régime `unknown`

**[FAIT]** `select.roborock_q7_max_parcours_de_lavage_de_sol` est à **`unknown`**. Conformément à [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) §6 (trois régimes) et §8 (disponibilité explicite), `unknown` ne vaut ni `standard`, ni une valeur par défaut. Ce régime devra être traité explicitement par tout futur consommateur.

---

## 7. Séquence de lancement

**[FAIT] Home Assistant séquence les actions d'un script.** Aucune course structurelle ne peut être affirmée avant mesure — et aucune mesure n'a été faite, l'audit s'interdisant toute exécution.

**[FAIT] L'intégration fonctionne en `local_polling`** : la relecture de l'état d'un `select` ou de `fan_speed` après écriture n'est pas instantanée. Ce qu'il faut en déduire n'est pas encore établi.

**[HYP — hypothèse principale] `vacuum.clean_area` lance lui-même le nettoyage.** Le libellé officiel du service est explicite : « indique à un aspirateur de nettoyer une ou plusieurs pièces ».

> **[RECO] Règle de prudence.** Un appel supplémentaire à `vacuum.start` **ne devra jamais être ajouté sans preuve terrain explicite** qu'il est nécessaire.

Points à mesurer, non à supposer :

- délai d'application effectif de `fan_speed` ;
- délai d'application effectif des `select` ;
- nécessité éventuelle d'une relecture ou d'une courte attente avant lancement ;
- persistance des réglages lors d'un changement de carte.

---

## 8. Réserve structurante — le comportement multi-cartes

**C'est le point central du prochain lot terrain.** Le Q7 Max porte quatre cartes pour un seul robot ; l'expérience cible traverse trois d'entre elles. Restent à qualifier :

1. la sélection de la carte — **automatique ou explicite** ;
2. le rôle exact de `select.roborock_q7_max_carte_selectionnee` une fois réactivée ;
3. la **stabilité dans le temps** des correspondances entre areas HA et segments Roborock ;
4. le traitement de pièces portant **le même nom sur plusieurs cartes** ;
5. le comportement lorsque le robot est **déplacé physiquement** entre RDC, Étage et Annexe ;
6. les **limites de commande** induites par ce déplacement matériel.

---

## 9. Prochain lot terrain minimal

**Un seul lot, non ouvert à ce jour : « Qualification du comportement multi-cartes et de la correspondance des pièces ».**

Objet : produire des **preuves**, pas des livrables. Aucune conception, aucun contrat, aucun YAML runtime, aucune UI.

Contenu minimal :

1. relever la correspondance réelle area HA ↔ segment Roborock ↔ carte, pour les quatre cartes ;
2. établir la table index de carte ↔ nom de carte ;
3. déterminer laquelle des deux listes de pièces du runtime fait autorité pour `clean_area` ;
4. vérifier que `clean_area` démarre bien le cycle seul, et qu'il accepte plusieurs pièces d'une même carte ;
5. observer le comportement d'une demande portant sur une carte non active, et après déplacement physique du robot ;
6. mesurer les délais d'application des réglages d'aspiration et d'eau.

### Arbitrages et gestes opérateur préalables

| # | Attendu | Nature |
|---|---|---|
| V1 | Renommer les segments périmés dans l'application Roborock : `Chambre Arnaud` → `Chambre Enfants`, `Chambre Matthieu` → `Salle de Jeux`, `Pallier` → `Palier` | Geste terrain — préalable |
| V2 | Décider des areas HA à créer ou ajuster (`WC` RDC, découpe de `Petite Maison`, `Dressing`) — préparation runtime limitée | Arbitrage |
| V3 | Trancher le sort de `WC Étage` : intégrer ou exclure explicitement | Arbitrage |
| V4 | Trancher la sémantique des quatre profils : correspondances « forte / normale / faible », et levier unique retenu pour « pas d'eau » | Arbitrage |
| V5 | Autoriser la réactivation des entités désactivées utiles (sélecteur de carte, capteurs d'erreur) | Décision opérateur |
| V6 | Autoriser une exécution de test encadrée sur un périmètre restreint | Autorisation explicite |
| V7 | Confirmer la non-régression de l'exclusion alarme portée par `binary_sensor.roborock_q7_max_nettoyage` | Validation |
| V8 | Statuer sur la saturation multi-cartes (4/4) : toute re-cartographie invaliderait les correspondances établies | Arbitrage |

---

## 10. Preuve de non-commande

Pendant toute la durée de l'audit :

| Contrôle | Résultat |
|---|---|
| Actions Home Assistant exécutées | **aucune** |
| Commandes envoyées au Roborock | **aucune** |
| Démarrage, arrêt, pause, déplacement du robot | **aucun** |
| Modification de puissance, mode de lavage, débit d'eau, carte | **aucune** |
| Paramètres Home Assistant modifiés | **aucun** |
| Mapping pièce / area / étage / appareil modifié | **aucun** |
| Helper, script, automation, scène, dashboard créé ou modifié | **aucun** |
| Formulaire Home Assistant enregistré | **aucun** |
| Flux d'options de config entry ouvert | **aucun** — volontairement écarté, un tel flux crée un état côté serveur |

Nature exclusive des accès : lecture des états, des registres (entités, appareils, areas, étages), du registre de services et des libellés de services. Aucun appel de service, aucune écriture.

---

## 11. Ce que ce document n'est pas

- Ce n'est **pas un contrat** : rien ici n'est normatif ni opposable.
- Aucun chantier n'est ouvert.
- Aucune architecture n'est décidée : autorité de décision, writer unique, couche de diagnostic et rôle de l'UI restent **à concevoir et à valider** avant toute proposition de code.
- Aucun code, aucun YAML runtime n'est proposé.
