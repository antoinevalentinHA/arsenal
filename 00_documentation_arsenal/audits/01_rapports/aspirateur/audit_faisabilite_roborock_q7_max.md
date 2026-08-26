# 🤖 ARSENAL — AUDIT — Faisabilité d'un pilotage **Roborock Q7 Max**

> **Trace d'audit runtime, strictement lecture seule.** Aucune action Home Assistant appelée, aucun paramètre modifié, aucune commande envoyée au robot. Aucun contrat, script, helper, automation, dashboard ni checker créé.
> Convention : **[FAIT]** observé dans le runtime · **[CODE]** établi par lecture du code source exact — Home Assistant Core au tag `2026.8.3` et `python-roborock` au tag `v5.31.1`, les versions effectivement en service · **[HYP]** inférence non prouvée · **[RECO]** à arbitrer par l'opérateur · **[DOC]** connaissance documentaire externe au runtime — jamais une preuve terrain propre à cet appareil.
> Ce document est un **relevé d'observation**, pas un contrat. Il n'est ni normatif ni opposable.

---

## Verdict

**`GO AVEC RÉSERVES` — faisabilité native confirmée pour *périmètre + profil + **Lancer***, mais **mono-carte par construction** et **sans nombre de passages**.**

L'expérience cible réduite à *choisir un périmètre, choisir un profil, appuyer sur **Lancer*** est **structurellement réalisable** : `vacuum.clean_area` accepte une sélection **multiple** de pièces, la puissance d'aspiration est réglable, le mode `vacuum` / `vac_and_mop` et l'intensité d'eau (`off` … `high`) sont exposés, `pause` / `stop` / `return_to_base` sont supportés.

Trois réserves ont changé de nature après lecture du code source exact (§2.1) :

1. **`clean_area` est inopérant en l'état** — le mappage area ↔ segment n'est pas configuré sur l'entité ; le service échoue en erreur de validation tant qu'un geste opérateur ne l'a pas créé (§3.1, **V11**).
2. **Une commande segmentée est mono-carte, et elle échoue en silence.** La commande protocolaire ne transporte **aucun identifiant de carte** ; Home Assistant écarte sans erreur les segments hors carte active, et n'émet **rien du tout** si aucun segment ne subsiste (§8). D'où la **contrainte de sécurité candidate IMC-1** posée au §8.
3. **Le nombre de passages existe dans le protocole mais n'est pas exposé.** `app_segment_clean` accepte un champ `repeat` dans le même appel que la liste de segments ; `vacuum.clean_area` ne le remplit pas (§6.3.1). L'arbitrage **V10** porte désormais sur l'opportunité d'une commande brute, non sur un choix entre pièces et coordonnées.

Les inconnues terrain restantes portent sur l'acceptation de `repeat` par cet appareil et sur le comportement de la carte active après déplacement physique du robot. Elles appellent une qualification terrain ciblée ; elles ne rendent pas la faisabilité indéterminée.

---

## 1. Date, contexte et périmètre

| | |
|---|---|
| **Date d'observation** | 2026-08-25 — **relevé de contrôle le 2026-08-26** (§5.4) — **audit du code exact le 2026-08-26** (§2.1) |
| **Contexte** | Étude d'opportunité préalable à tout chantier. Aucun besoin runtime ouvert à ce jour. |
| **Nature** | Audit **strictement read-only** du runtime Home Assistant + lecture du code source des versions en service + recherche d'antériorité dans le dépôt. |
| **Méthode** | Lecture des états, du registre d'entités, du registre d'appareils, du registre d'areas et du registre de services depuis le frontend HA. Aucune action appelée, aucun formulaire enregistré, aucun flux d'options ouvert. Pour la passe du 2026-08-26 : lecture des sources de Home Assistant Core au tag `2026.8.3` (`components/vacuum/`, `components/roborock/`, tests d'intégration associés) et de `python-roborock` au tag `v5.31.1`, hors dépôt Arsenal. |
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

### 2.1 Chaîne de commande réelle — lecture du code exact

Les faits de cette sous-section proviennent du **code source des versions en service**, pas d'une inférence sur le runtime. Ils précisent — et sur trois points **corrigent** — les constats des passes précédentes.

**[FAIT] La classe qui s'exécute est identifiée sans ambiguïté.** L'entité expose `supported_features = 30524`, soit exactement `PAUSE | STOP | RETURN_HOME | FAN_SPEED | SEND_COMMAND | LOCATE | CLEAN_SPOT | STATE | START | CLEAN_AREA`. C'est la signature de la classe **protocole V1** de l'intégration. La classe homonyme destinée au « Roborock Q7 » de génération B01 — qui n'a **ni** `clean_area` **ni** nettoyage zoné — n'est pas celle-ci. Le chemin de code décrit ci-dessous est donc bien celui qui s'exécute sur cet appareil.

**[CODE] Chaîne complète de `vacuum.clean_area`.**

| Étage | Ce qui se passe |
|---|---|
| Action HA | `cleaning_area_id` : liste d'`area_id` HA, requise |
| Cœur `vacuum` | lit le mappage **area → segments** stocké dans les *options* de l'entité au registre ; **si ce mappage est absent, le service lève une erreur de validation** et rien n'est émis ; les areas fournies mais non mappées lèvent une seconde erreur de validation |
| Plateforme `roborock` | chaque segment est identifié par la paire **`<index de carte>_<index de segment>`** ; la plateforme **filtre sur la carte active** et **jette silencieusement** les segments des autres cartes ; si la liste filtrée est vide, elle **retourne sans émettre aucune commande et sans erreur** ; elle **ne bascule jamais** de carte |
| Bibliothèque → protocole | `app_segment_clean` avec, pour seule charge utile, la liste des index de segments retenus. **Aucun index de carte. Aucun nombre de passages.** |

Ce comportement est **couvert par les tests d'intégration officiels** : l'un d'eux vérifie explicitement qu'une demande portant uniquement sur des segments d'une carte non active **n'émet aucune commande**, un autre qu'une demande mixte est **réduite aux seuls segments de la carte active**.

**[CODE] Chaîne complète de `roborock.set_vacuum_zoned_cleaning`.** Les quatre coordonnées et `repeats` (entier borné `0..2`) sont transmis tels quels à la commande `app_zoned_clean`, sous forme d'un rectangle unique. **Aucune validation géométrique**, et là encore **aucun index de carte**.

**[CODE] `vacuum.send_command` transmet sans transformation.** Le nom de commande est accepté comme chaîne libre et les paramètres sont passés verbatim jusqu'à l'encodage du message. **C'est une action publique de Home Assistant** — elle n'a rien d'un contournement de l'API — **mais elle expose une commande protocolaire privée sans la validation ni l'abstraction qu'apporte `clean_area`** : ni résolution des areas, ni contrôle de la carte active, ni vérification des bornes, ni message d'erreur intelligible. Ce qu'elle offre en capacité, elle le retire en garanties.

**[CODE] Relecture après écriture.** Toute commande émise par une entité coordonnée de cette intégration est **immédiatement suivie d'un rafraîchissement du coordinateur**, dans le même appel. La cadence de polling de fond est de 15 s en nettoyage et 30 s au repos sur canal local (30 s / 60 s en repli cloud), mais elle ne conditionne pas la relecture qui suit une écriture. Cela **réduit fortement** la crainte de course exprimée au §7 sans la supprimer : la mesure terrain reste à faire.

---

## 3. Entités et capacités utiles

### 3.1 Commande et état

| Rôle | Entité / service | Valeurs ou état observés |
|---|---|---|
| Aspirateur | `vacuum.roborock_q7_max` | `idle` |
| Aspiration | `vacuum.set_fan_speed` (attribut `fan_speed`) | `quiet` · `balanced` · `turbo` · `max` · `gentle` — courant : `max` |
| Nettoyage par pièces | `vacuum.clean_area` | champ `cleaning_area_id` **requis**, sélecteur d'**areas HA** avec **`multiple: true`** et **`reorder: true`** — **mais inopérant en l'état**, cf. encadré ci-dessous |
| Mode | `select.entree_roborock_q7_max_mode_de_nettoyage` | `vacuum` · `vac_and_mop` — courant : `vac_and_mop` |
| Intensité d'eau | `select.roborock_q7_max_intensite_de_frottement` | `off` · `low` · `medium` · `high` · `custom_water_flow` — courant : `medium` |
| Parcours de lavage | `select.roborock_q7_max_parcours_de_lavage_de_sol` | `standard` · `deep` · `deep_plus` — **état `unknown`** |
| Interruption | `vacuum.pause` · `vacuum.stop` · `vacuum.return_to_base` | supportés |
| Autres services natifs | `clean_spot`, `locate`, `send_command` ; côté `roborock` : `get_maps`, `get_vacuum_current_position`, `set_vacuum_goto_position`, `set_vacuum_zoned_cleaning` | disponibles, non appelés |

**[FAIT] Toutes les capacités requises sont déclarées supportées par l'appareil.** Le contrôle des bits de capacité exigés par chaque service (`start`, `pause`, `stop`, `return_to_base`, `clean_area`, `locate`) est **satisfait** pour cette entité.

> **[FAIT] Correction — `vacuum.clean_area` n'est pas utilisable en l'état.** Les options de `vacuum.roborock_q7_max` au registre d'entités ne contiennent **aucun mappage area ↔ segment** : la seule clé présente relève de l'assistant conversationnel. Or ce mappage est **le seul chemin** par lequel le service traduit une area HA en segment Roborock (§2.1). Tant qu'il n'existe pas, tout appel échoue en erreur de validation, avec le message *« le mappage des areas n'est pas configuré pour cette entité »*.
>
> **Ce n'est ni un blocage technique ni un défaut de l'intégration** : le mappage se crée par un **geste opérateur** dans les paramètres de l'entité, qui écrit dans le registre. Il n'a pas été fait, et l'audit s'est interdit de le faire. Ce geste devient un **prérequis dur** de toute voie fondée sur `clean_area` — inscrit en **V11** au §9.
>
> Conséquence sur la lecture des passes précédentes : la disponibilité du **schéma** du service avait été constatée à juste titre ; elle avait été lue comme une disponibilité **opérationnelle**, ce qu'elle n'est pas.

### 3.2 Observation

| Rôle | Entité | État observé |
|---|---|---|
| État machine | `sensor.roborock_q7_max_etat` | `charger_disconnected` — énumération riche incluant `cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, `returning_home`, `docking`, `charging`, `error`, `device_offline` |
| Session non terminée | `binary_sensor.roborock_q7_max_nettoyage` | `off` — **ce n'est pas un témoin de « cycle en cours »**, cf. encadré ci-dessous |
| Batterie | `sensor.roborock_q7_max_batterie` | `75 %` |
| Progression | `sensor.roborock_q7_max_duree_de_nettoyage` · `sensor.roborock_q7_max_surface_de_nettoyage` | `24,4 min` · `12,2` |
| Pièce courante | `sensor.roborock_q7_max_piece_actuelle` | énumère les segments de la **carte active** (cf. §5) |
| En charge | `binary_sensor.roborock_q7_max_en_charge` | `off` |

> **[FAIT] Correction — les deux témoins ne sont pas concordants, et l'un des deux ne dit pas ce qu'on croyait.**
>
> `binary_sensor.…_nettoyage` ne reflète pas « le robot nettoie ». Il reflète le champ `in_cleaning` du statut, dont l'énumération est **`0` terminé · `1` nettoyage global inachevé · `2` nettoyage zoné inachevé · `3` nettoyage par segments inachevé**. Sa vraie sémantique est donc **« une session n'est pas terminée »**, c'est-à-dire **reprenable**. C'est d'ailleurs exactement ce que l'intégration en fait : `vacuum.start` consulte ce champ pour choisir une commande de **reprise** plutôt qu'un démarrage (§7).
>
> **Observation runtime discordante, 2026-08-26** — relevée pendant la passe de code : `binary_sensor.…_nettoyage = on` **et simultanément** `vacuum.roborock_q7_max = idle`, `sensor.…_etat = charger_disconnected`, `binary_sensor.…_en_charge = off`, `sensor.…_piece_actuelle = Palier`, durée `50,3 min`, surface `29,7`. Le robot ne nettoyait pas : une session par segments restait ouverte, hors de son dock.
>
> **Ce qui reste vrai** : `sensor.…_etat` est un témoin d'activité honnête (`segment_cleaning`, `zoned_cleaning`, `cleaning`, `paused`…). Une garde anti-double-lancement doit s'appuyer **sur lui**, et traiter `binary_sensor.…_nettoyage` comme ce qu'il est — un indicateur de **session inachevée**, utile mais distinct.
>
> **Portée sur l'existant — constat, pas chantier.** L'exclusion d'intrusion en production (§1) est câblée sur ce binaire. Elle reste donc active tant qu'une session segmentée n'est pas achevée, **robot à l'arrêt compris**. Ce constat alimente **V7** ; il n'ouvre aucun travail ici.

### 3.3 Prérequis matériels observables

| Prérequis | Entité | État observé |
|---|---|---|
| Serpillière fixée | `binary_sensor.roborock_q7_max_serpilliere_fixee` | **`off`** — aucune serpillière posée |
| Réservoir d'eau fixé | `binary_sensor.roborock_q7_max_reservoir_d_eau_fixe` | `on` |
| Pénurie d'eau | `binary_sensor.entree_roborock_q7_max_penurie_d_eau` | `off` |
| Séchage serpillière (dock) | `binary_sensor.entree_roborock_q7_max_dock_sechage_de_la_serpilliere` | `off` |

**[FAIT] Les prérequis matériels des profils avec eau sont observables.** Ils ne sont pas commandables : poser ou retirer la serpillière est un **geste opérateur**.

### 3.4 Prérequis runtime réversibles

**[FAIT] Plusieurs entités utiles au chantier sont désactivées par l'utilisateur — supportées par l'intégration, donc réactivables.** Ce ne sont pas des blocages techniques.

| Entité désactivée | Ce qu'elle apporterait |
|---|---|
| `select.roborock_q7_max_carte_selectionnee` | Sélection explicite de la carte active — **passe de confort à prérequis**, cf. §8 |
| `sensor.roborock_q7_max_erreur_de_l_aspirateur` | Motif d'erreur détaillé du robot |
| `sensor.roborock_q7_max_dock_erreur_de_dock` | Motif d'erreur du dock |
| `sensor.roborock_q7_max_debut_du_dernier_nettoyage` / `…_fin_du_dernier_nettoyage` | Bornes natives d'une session |
| `button.roborock_q7_max_nettoyage_complet` | **Déclenchement d'une routine Roborock existante**, cf. encadré ci-dessous |

**[FAIT] Un diagnostic minimal honnête est déjà possible sans elles**, à partir de l'état général du robot, du caractère `unknown` / `unavailable` des entités, de l'état machine et des prérequis matériels. Les capteurs détaillés **amélioreront** ce diagnostic après réactivation ; ils ne le conditionnent pas.

> **[FAIT] Une routine Roborock est déjà exposée dans le runtime — et elle n'avait pas été identifiée.** `button.roborock_q7_max_nettoyage_complet` porte l'identifiant unique `8303163_<identifiant appareil>` et **aucune clé de traduction**. Cette forme — identifiant numérique préfixé, libellé provenant du compte — est celle des **boutons de routine** créés dynamiquement par l'intégration à partir des scènes du compte Roborock. Il s'agit donc d'une routine réelle nommée « Nettoyage complet », d'identifiant `8303163`, **désactivée par l'utilisateur**. C'est la 45ᵉ entrée du registre, jusqu'ici comptée mais non caractérisée.
>
> **[CODE] Le bouton n'accepte aucun paramètre** : il déclenche la routine par son identifiant, via l'**API web du compte Roborock** — donc **par le cloud, obligatoirement**. Le périmètre, le profil et le nombre de passages sont figés dans la définition de la routine, côté application. Portée et limites au §6.3.1.

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

**[FAIT] La table index de carte ↔ nom de carte est établie.** Elle a été relevée en lecture seule le 2026-08-26 (§5.1) ; l'hypothèse antérieure — *« la correspondance entre l'index interne d'une carte et son nom n'est pas observable en lecture seule »* — est **levée**.

| Index de carte | Nom exposé | Segments nommés |
|---|---|---|
| **0** | `RDC` | 4 |
| **1** | `Étage ` — **avec une espace finale** | 8 |
| **2** | `Annexe` | 4 |
| *(non énuméré)* | `Garage` | **0** — l'entité `image` existe, la carte ne porte aucune pièce nommée |

**[FAIT] La carte active au moment du relevé est l'Étage, index `1`** — `sensor.roborock_q7_max_piece_actuelle` énumère exactement ses huit segments. L'ancienne mention `[HYP]` est convertie en fait.

**[FAIT] Le nom de carte `Étage ` porte une espace finale**, propagée jusque dans l'identifiant unique de l'entité image. La règle de restitution du §5.3 s'applique donc **aussi aux noms de cartes**, et pas seulement aux noms de pièces.

**[FAIT] Les trois périmètres métier visés sont portés par trois cartes distinctes** — Petite maison / Annexe, RDC, Étage. Conjugué à la contrainte de sécurité candidate **IMC-1** (§8), cela signifie qu'**un lancement ne peut jamais couvrir plus d'un de ces trois périmètres**.

---

## 5. Pièces observées et divergences de nommage

Trois référentiels distincts coexistent et **ne doivent pas être confondus** :

1. la **pièce Roborock** — un segment nommé dans une carte du robot ;
2. l'**area Home Assistant** — l'unité que consomme `vacuum.clean_area` ;
3. le **périmètre métier Arsenal** (`RDC`, `Étage`, `Petite maison`…) — une **composition contractuelle** de pièces, qui n'a pas vocation à devenir une area HA.

### 5.1 Segments observés

#### Carte active (Étage), suivi historique

**[FAIT] au 2026-08-25** — `Pallier` · `Chambre Parents` · `Chambre Arnaud` · `Chambre Matthieu` · `Dressing` · `SDB Parents` · `WC Étage` · `SDB Enfants`.

**[FAIT] au 2026-08-26, après renommage opérateur** — `Palier` · `Chambre Parents` · `Chambre Enfants` · `Salle de Jeux` · `Dressing` · `SDB Parents` · `WC Étage` · `SDB Enfants`.

#### Table complète des segments, toutes cartes — **[FAIT] 2026-08-26**

L'affirmation antérieure — *« les segments des cartes RDC, Annexe et Garage n'ont pas pu être relevés : seule la carte active énumère ses pièces »* — était **fausse**. Elle décrivait la limite d'une **entité** (`sensor.…_piece_actuelle`, qui n'énumère effectivement que la carte active), pas celle du runtime. L'intégration conserve en mémoire la description de **toutes** les cartes, et cette description est lisible sans aucune action.

| Identifiant de segment | Nom du segment | Carte |
|---|---|---|
| `0_16` | `Salon` | RDC |
| `0_18` | `Entrée` | RDC |
| `0_20` | `WC RDC` | RDC |
| `0_21` | `Cage d'escaliers` | RDC |
| `1_16` | `Palier` | Étage |
| `1_17` | `Chambre Parents` | Étage |
| `1_18` | `Chambre Enfants` | Étage |
| `1_19` | `Salle de Jeux` | Étage |
| `1_20` | `Dressing` | Étage |
| `1_21` | `SDB Parents` | Étage |
| `1_22` | `WC Étage` | Étage |
| `1_23` | `SDB Enfants` | Étage |
| `2_16` | `Salle de bain` | Annexe |
| `2_17` | `Ext` | Annexe |
| `2_18` | `Chambre1` | Annexe |
| `2_19` | `Chambre` | Annexe |

**[FAIT] Homonymie d'identifiants, démontrée et non théorique.** L'index `16` existe sur les **trois** cartes peuplées, sous trois noms différents — `Salon`, `Palier`, `Salle de bain`. L'unicité n'est portée que par la paire `<carte>_<segment>`. Un index de segment **seul** est intrinsèquement ambigu : c'est la raison technique de la contrainte de sécurité candidate **IMC-1** (§8).

**[FAIT] Homonymie de noms, également présente.** `Chambre` (`2_19`, Annexe) face à `Chambre Parents` et `Chambre Enfants` (Étage) ; `Salle de bain` (Annexe) face à `SDB Parents` et `SDB Enfants` (Étage).

**[FAIT] La carte Garage ne porte aucun segment nommé.** Son entité `image` existe, sa description ne contient aucune pièce. La raison — carte sans pièces nommées, ou entrée dégradée du cache de l'intégration — n'est pas déterminable en lecture seule.

**[FAIT] Le RDC ne compte que quatre segments**, et le nom Roborock du séjour est `Salon` là où l'area HA s'appelle `Séjour`. Aucun segment ne couvre la cuisine.

### 5.2 Areas Home Assistant

**[FAIT] 14 areas**, créées manuellement à l'été 2025, sans alias ni libellé particulier, réparties sur trois étages (`RDC`, `Premier`, `Cave`) :

`All House` · `Cave` · `Chambre Enfants` · `Chambre parents` · `Cage d'escaliers` · `Entrée` · `Garage` · `Jardin` · `Palier` · `Petite Maison` · `Salle de jeux` · `SDB enfants` · `SDB parents` · `Séjour`.

**[FAIT] Aucun lien observable entre les areas HA et les segments Roborock** : les areas ne portent ni alias ni marquage issus de l'intégration.

### 5.3 Divergences relevées

| Nature | Détail | Statut |
|---|---|---|
| **Noms périmés côté Roborock** | La carte Étage portait **`Chambre Arnaud`** et **`Chambre Matthieu`** — noms proscrits. | **RÉSOLU le 2026-08-26** — renommés en `Chambre Enfants` et `Salle de Jeux` dans l'application Roborock ; correction constatée dans le runtime. |
| **Faute d'orthographe** | `Pallier` côté Roborock (double L). | **RÉSOLU le 2026-08-26** — corrigé en `Palier` ; correction constatée dans le runtime. |
| **Casse** | Côté Roborock `Chambre Parents`, `Salle de Jeux`, `SDB Parents`, `SDB Enfants` vs côté HA `Chambre parents`, `Salle de jeux`, `SDB parents`, `SDB enfants`. | Ouvert — mineur, à arbitrer. `Palier` et `Chambre Enfants` concordent désormais exactement. |
| **Pluriel** | `Cage d'escaliers` côté HA vs `Cage d'escalier` attendu. | Ouvert — mineur, à arbitrer. |
| **Pièces sans area HA** | Liste désormais **exhaustive** grâce à la table du §5.1 : `Dressing` et `WC Étage` (Étage) ; `WC RDC` (RDC) ; `Salle de bain`, `Ext`, `Chambre1`, `Chambre` (Annexe — l'area `Petite Maison` n'est pas découpée). | Ouvert — préparation runtime limitée : création ou ajustement de quelques areas. **V2 est déblocable** : les noms exacts sont connus. |
| **Nom divergent, séjour** | Segment Roborock `Salon` (`0_16`) vs area HA `Séjour`. | Ouvert — à arbitrer avec V2. |

> **[RECO] Règle de restitution — durable.** L'UI Arsenal ne devra **jamais** restituer un nom de pièce provenant directement du robot sans contrôle. Toute pièce affichée doit l'être sous son nom canonique Arsenal, ou pas du tout. Les anciens noms ont été corrigés à la source le 2026-08-26 ; la règle reste nécessaire, car rien n'empêche qu'un futur renommage réintroduise un écart.

> **[FAIT] Correction — il n'y a pas de « second référentiel ». La divergence signalée n'existe pas.**
>
> Les passes précédentes avaient relevé « deux listes de pièces qui ne se recouvrent pas » : les 8 segments de la carte active, et « une liste courte issue du compte » de 4 entrées — `Salle de bain`, `Ext`, `Chambre1`, `Chambre` — en s'interrogeant sur celle qui ferait autorité pour `clean_area`.
>
> La table complète du §5.1 lève l'ambiguïté : **ces quatre entrées sont exactement les quatre segments de la carte Annexe** (`2_16` à `2_19`). Ce n'était pas un référentiel concurrent, mais **une autre carte du même référentiel**. Il n'existe qu'une seule liste de pièces, indexée par carte, et c'est elle qui alimente la résolution.
>
> Cette question — *« déterminer laquelle des deux listes fait autorité »* — devient **sans objet** et disparaît du lot terrain (§9).

### 5.4 Relevé de contrôle du 2026-08-26

**[FAIT]** Après renommage des segments par l'opérateur dans l'application Roborock, la correction est **remontée jusqu'à Home Assistant sans intervention** : les segments de la carte active sont désormais `Palier`, `Chambre Parents`, `Chambre Enfants`, `Salle de Jeux`, `Dressing`, `SDB Parents`, `WC Étage`, `SDB Enfants`.

**[FAIT]** Le référentiel d'areas Home Assistant est **inchangé** (14 areas, mêmes noms). `Palier` et `Chambre Enfants` concordent désormais exactement entre les deux référentiels ; les écarts de casse subsistent sur les quatre autres.

**[FAIT] Enseignement complémentaire.** Le renommage d'un segment côté application est répercuté par l'intégration. Un futur affichage ne peut donc pas traiter ces libellés comme stables : ils sont **modifiables hors du dépôt et hors de Home Assistant**.

---

## 6. Les quatre profils métier envisagés

Valeurs réellement exposées, sans traduction métier inventée.

| Profil | Aspiration | Eau / lavage | Faisabilité | Réserve |
|---|---|---|---|---|
| **1 — forte / pas d'eau** | `turbo` ou `max` | `intensité = off` — le `mode = vacuum` en **découle** (§6.1) | Valeurs disponibles | Correspondance « forte » → `turbo` **ou** `max` à arbitrer. **Sémantique de « pas d'eau » désormais établie** (§6.1) |
| **2 — normale / pas d'eau** | **`balanced` [FAIT]** — correspondance établie §6.3 | idem profil 1 | Valeurs disponibles, **correspondance établie** | Profil **observé en conditions réelles** le 2026-08-26 ; commande depuis HA : écrire l'intensité d'eau et l'aspiration, **jamais le mode** (§6.1) |
| **3 — faible / eau moyenne** | `quiet` [HYP] — `gentle` écarté provisoirement (§6.3) | `mode = vac_and_mop` + `intensité = medium` | Valeurs disponibles | **Non commandable tant que la serpillière est absente** |
| **4 — faible / eau importante** | `quiet` [HYP] — idem | `mode = vac_and_mop` + `intensité = high` | Valeurs disponibles | Idem profil 3 ; `high` plutôt que `custom_water_flow` à arbitrer |

### 6.1 Le point « pas d'eau »

**[FAIT] Deux leviers exposés peuvent porter l'intention, sans qu'aucun ne soit établi comme faisant autorité** : le mode de nettoyage (`vacuum`) et l'intensité de frottement (`off`). Le parcours de lavage n'offre **aucune valeur « aucun »** — il n'exprime pas l'absence de lavage. L'absence physique de serpillière est un **état matériel non commandable**, donc jamais un moyen de réaliser un profil.

**[FAIT] Cycle réel recoupé, 2026-08-26 — voir §6.3.** Un nettoyage lancé par l'opérateur depuis l'application, déclaré « Niveau de l'eau : **Arrêt** », présentait simultanément dans Home Assistant `mode = vacuum` **et** `intensité de frottement = off`.

> **[CODE] Résolution — le mode de nettoyage est un état *dérivé*, pas un writer concurrent.**
>
> L'hypothèse formulée à la passe précédente — *« une intention à deux projections »* — est **confirmée par le code**, et même resserrée.
>
> **En lecture**, le mode de nettoyage n'a pas d'existence propre : il est **calculé** à partir des trois réglages bas niveau. La règle est littérale — si l'intensité d'eau vaut `off`, le mode affiché est `vacuum` ; sinon `vac_and_mop`. `select.…_mode_de_nettoyage` est donc **un affichage**, jamais un état indépendant.
>
> **Il n'y a par conséquent aucun writer concurrent à départager.** Le writer unique de l'intention « pas d'eau » est l'**intensité de frottement** — `off`. Le mode suit tout seul. La crainte d'anti-patron exprimée ici tombe.
>
> **[CODE] Mais écrire le mode a un effet de bord destructeur.** Sélectionner `vacuum` (ou `vac_and_mop`) **n'écrit pas seulement l'eau** : l'intégration émet **une seule commande** qui impose d'un bloc l'aspiration, l'eau **et** le parcours — et l'aspiration qu'elle impose est **toujours `balanced`**, quelle que soit la valeur précédente. Écrire le mode **après** avoir réglé l'aspiration **écrase donc silencieusement le profil d'aspiration**.
>
> Deux conséquences, à porter dans tout futur chantier :
>
> 1. **Ne pas écrire le mode de nettoyage.** Piloter l'intensité d'eau et la puissance d'aspiration séparément suffit ; ce sont deux writers **disjoints** — régler l'eau ne touche pas l'aspiration. Le mode se déduit.
> 2. **Si le mode devait malgré tout être écrit**, il devrait l'être **avant** l'aspiration, jamais après.
>
> Cela **réduit V4** : le levier d'écriture de « pas d'eau » n'est plus à trancher, il est établi. Restent ouvertes les seules correspondances de « forte » et « faible ».

### 6.2 Serpillière absente — condition matérielle, pas blocage

**[FAIT]** `binary_sensor.roborock_q7_max_serpilliere_fixee = off` au moment de l'audit.

C'est une **condition matérielle normale à représenter explicitement**, relevant de la commandabilité (impossibilité physique, catégorie A de [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)) :

- profils **sans eau** (1 et 2) : potentiellement autorisables ;
- profils **avec eau** (3 et 4) : **refus explicite** assorti d'un motif lisible tant que la serpillière est absente.

Le dashboard reste donc réalisable ; il doit simplement dire la vérité sur ce qu'il ne peut pas lancer.

### 6.3 Cycle de référence recoupé — 2026-08-26

**[FAIT]** L'opérateur a lancé depuis l'application un cycle sur la carte Étage, et en a **déclaré les réglages**. Ils ont été recoupés avec le runtime pendant l'exécution.

| Réglage déclaré (application) | Observé dans Home Assistant |
|---|---|
| Puissance d'aspiration : **Normal** | `fan_speed = balanced` |
| Niveau de l'eau : **Arrêt** | `intensité de frottement = off` **et** `mode = vacuum` |
| 7 pièces : Chambre Enfants, Salle de Jeux, Palier, SDB Enfants, Chambre Parents, Dressing, SDB Parents | `sensor.…_etat = segment_cleaning`, `sensor.…_piece_actuelle` progressant de pièce en pièce |
| **× 2** (deux passages) | aucune entité HA ne l'expose — **§6.3.1** |

**[FAIT] Correspondance établie pour un seul niveau d'aspiration.** « Normal » côté application ↔ **`balanced`** côté HA, par recoupement d'une déclaration opérateur et d'une observation runtime concordantes. Les correspondances de « forte » (`turbo` ou `max`) et de « faible » **restent ouvertes** — V4 n'est donc que partiellement levé.

**[DOC] Gamme standard Roborock.** La documentation de la gamme distingue quatre niveaux d'aspiration — `quiet`, `balanced`, `turbo`, `max` — dont `balanced` est le niveau courant, ce que le recoupement ci-dessus confirme pour cet appareil. `gentle` n'appartient pas à cette échelle : il relève d'un régime de déplacement distinct, hors gradation de puissance. Cette connaissance est **documentaire** ; elle n'a pas été vérifiée sur le Q7 Max et ne vaut pas preuve terrain.

**[CODE] Corroboration structurelle.** La liste d'aspiration n'est pas figée par modèle : elle est **composée** à partir des bits de capacité de l'appareil. Le socle est `quiet` · `balanced` · `turbo` · `max` ; `gentle` y est **ajouté ensuite**, précisément parce que cet appareil ne sait pas laver sans aspirer. L'ordre relevé dans le runtime correspond exactement à cette composition. `gentle` porte par ailleurs un code protocolaire **supérieur** à celui de `max` : le code ne le classe donc **pas** comme un niveau faible.

**[HYP]** Sur cette base, « faible » correspondrait à **`quiet`**, et `gentle` peut être **écarté provisoirement** des quatre profils métier. L'arbitrage V4 reste requis : seule une observation terrain ferait de cette hypothèse un fait.

**[FAIT] Composition de périmètre confirmée sur l'appareil.** Sept segments d'une même carte ont été nettoyés en une seule demande — soit tous les segments de la carte Étage **sauf `WC Étage`**. La capacité du robot à traiter un périmètre composé est donc établie. Cela ne préjuge pas de la façon dont `vacuum.clean_area` résout les areas HA, qui reste à qualifier.

### 6.3.1 Nombre de passages — le point dur du besoin

Le nombre de passages (**×1 / ×2 / ×3**) **fait partie du besoin à exposer**. Son traitement par l'intégration a donc été instruit précisément.

**[FAIT] Aucune entité ne le porte.** Sur les **45 entrées** du registre — 19 actives et 26 désactivées — aucune ne représente un nombre de passages. La seule entité de comptage, `sensor.roborock_q7_max_nombre_total_de_nettoyages` (désactivée), est un cumul de vie, sans rapport avec le réglage d'un cycle.

**[FAIT] Un seul service natif l'expose — et ce n'est pas celui du besoin.**

| Service | Désignation du périmètre | Nombre de passages |
|---|---|---|
| `vacuum.clean_area` | **pièces** (areas HA, sélection multiple) | **absent** — le service n'a qu'un champ, `cleaning_area_id` |
| `roborock.set_vacuum_zoned_cleaning` | **coordonnées** d'un rectangle (`x1`, `y1`, `x2`, `y2`) | **`repeats`**, requis, entier `0..2` — libellé officiel : « le nombre de fois où le nettoyage de la zone est répété ; `0` correspond à un seul nettoyage » |

**[FAIT] `repeats` couvre exactement l'amplitude du besoin** : `0` = ×1, `1` = ×2, `2` = ×3.

**[FAIT] Tension au niveau des *services* Home Assistant.** Les deux moitiés du besoin sont portées par **deux services disjoints** : celui qui sait désigner des pièces ne sait pas répéter, celui qui sait répéter ne sait pas désigner de pièces — il exige des coordonnées de rectangle, incompatibles avec une sélection de périmètre par pièces.

> **[CODE] Correction majeure — la tension n'existe pas au niveau du protocole, seulement au niveau de l'exposition.**
>
> La commande protocolaire `app_segment_clean` — celle-là même que `vacuum.clean_area` finit par émettre — **accepte un champ `repeat` dans le même appel que la liste de segments**. La documentation de la bibliothèque embarquée par l'intégration la décrit sans ambiguïté : *elle démarre un nettoyage par segments et le répète le nombre de fois indiqué*, avec une charge utile associant une liste de segments et un `repeat`.
>
> **Home Assistant construit cette charge utile sans le champ `repeat`.** Le manque n'est donc **pas** dans le protocole ni dans l'appareil : il est dans la **couche d'exposition** de l'intégration. « Pièces + répétitions » est exprimable en **une seule primitive** ; simplement, aucune action publique de Home Assistant ne l'expose.
>
> Trois indices convergents dans la bibliothèque, tous **non exposés** par l'intégration : le statut du robot décode un champ `repeat` (aucune entité ne le porte) ; l'énumération des commandes comporte un `set_clean_repeat_times` (jamais appelé, non documenté) ; un bit de capacité relatif à la répétition existe (jamais lu).
>
> **Portée de la preuve, et sa limite.** Cette description est **documentaire côté bibliothèque**, et l'appareil explicitement coché dans cette documentation **n'est pas le Q7 Max**. L'acceptation de `repeat` par `roborock.vacuum.a38` est donc **non prouvée** : c'est le premier objet du lot terrain (§9).

**[CODE] Ce que change cette découverte pour V10.** L'arbitrage ne porte plus sur *« pièces sans répétition, ou coordonnées avec répétition »*. Il porte sur : **accepter ou refuser d'émettre la commande segmentée avec `repeat` par `vacuum.send_command`**.

Ce que cela coûterait, énoncé sans complaisance :

- `vacuum.send_command` **reste une action publique de Home Assistant** — l'utiliser n'est pas un contournement de l'API. **Mais elle expose une commande protocolaire privée sans la validation ni l'abstraction de `clean_area`** : ni résolution des areas, ni contrôle de la carte active, ni bornes vérifiées, ni erreur intelligible. Tout ce que `clean_area` garantit devrait être **réimplémenté et maintenu côté Arsenal**.
- Le contrat de cette commande n'est garanti ni par Home Assistant ni par l'appareil : il peut changer sans préavis, et un `repeat` **ignoré en silence** est une issue plausible — c'est-à-dire un lancement qui réussit en apparence et ne répète rien.
- La contrainte de sécurité candidate **IMC-1** (§8) s'applique intégralement : cette voie reste **mono-carte**.

**[FAIT] Une quatrième voie existe et elle est déjà présente : les routines Roborock (§3.4).** La structure d'une routine associe, dans une même définition, une liste de segments, **un index de carte**, un profil complet et **un nombre de passages**. C'est la seule structure connue qui exprime tout cela d'un coup.

Ses limites sont toutefois dirimantes pour une architecture pilotée par contrat :

- elle **n'est pas paramétrable depuis Home Assistant** — le bouton ne prend aucun argument ; il faudrait **une routine, donc un bouton, par combinaison** périmètre × profil × passages ;
- la définition vit **dans l'application Roborock**, donc **hors du dépôt, hors CI et hors contrat** ;
- son déclenchement passe **obligatoirement par le cloud** ;
- **le fait qu'une routine porte un index de carte ne démontre pas qu'une mission unique puisse couvrir plusieurs cartes.** Une routine porteuse d'un index de carte est **liée à cette carte** : l'index y désigne le contexte d'exécution, il ne compose rien. Rien dans ce qui a été lu n'établit qu'une mission puisse traverser plusieurs cartes.

> **[RECO]** Le nombre de passages reste la contrainte la plus structurante de l'expérience cible, mais elle a **changé de nature** : ce n'est plus une impossibilité protocolaire, c'est un **choix de dépendance**. Quatre options s'offrent — commande brute assumée, UI sans ce réglage, répétition supervisée par missions successives, ou délégation aux routines Roborock. Trancher relève de **V10**, et **aucune ne doit être engagée avant l'essai `×2` du §9**.

### 6.3.2 Historisation — extension optionnelle

**[FAIT]** `recorder.yaml` fonctionne en liste d'inclusion et ne contient **aucune** entité Roborock. L'API d'historique le confirme : zéro série retournée pour `sensor.roborock_q7_max_etat`. Aucun cycle n'est donc reconstituable a posteriori.

**Portée du constat.** Le besoin exprimé porte sur la **commande** et le **diagnostic courant** — ce que le système peut faire maintenant, et pourquoi. Ni l'un ni l'autre ne dépend de l'historique : l'état courant, la disponibilité, le cycle en cours et les prérequis matériels sont tous lisibles en direct.

> **[RECO]** À traiter comme une **extension optionnelle d'observabilité**, **hors chemin critique** du dashboard demandé. Inscrire des entités au `recorder` n'a d'intérêt que si un besoin de reconstitution a posteriori est un jour exprimé (**V9**).

### 6.4 Régime `unknown`

**[FAIT]** `select.roborock_q7_max_parcours_de_lavage_de_sol` est à **`unknown`**. Conformément à [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) §6 (trois régimes) et §8 (disponibilité explicite), `unknown` ne vaut ni `standard`, ni une valeur par défaut. Ce régime devra être traité explicitement par tout futur consommateur.

---

## 7. Séquence de lancement

**[FAIT] Home Assistant séquence les actions d'un script.** Aucune course structurelle ne peut être affirmée avant mesure — et aucune mesure n'a été faite, l'audit s'interdisant toute exécution.

**[CODE] La relecture après écriture n'est pas laissée au polling.** Chaque commande émise par l'intégration est **immédiatement suivie d'un rafraîchissement du coordinateur**, dans le même appel (§2.1). Le polling de fond — 15 s en nettoyage, 30 s au repos sur canal local — ne gouverne donc pas le délai perçu après une écriture. La crainte de course est **fortement réduite**, mais non levée : rien ne garantit encore que l'appareil ait appliqué le réglage au moment où il répond.

**[CODE] `vacuum.clean_area` lance bien lui-même le nettoyage.** L'ancienne mention `[HYP]` est **levée** : la commande finalement émise est `app_segment_clean`, qui **est** une commande de démarrage. Le libellé officiel du service — « indique à un aspirateur de nettoyer une ou plusieurs pièces » — décrit exactement ce que fait le code.

> **[CODE] Rôle exact de `vacuum.start` — et pourquoi il ne faut surtout pas l'ajouter.**
>
> `vacuum.start` **n'est pas un démarreur neutre**. Il choisit sa commande en fonction du champ `in_cleaning` du statut — celui-là même dont le §3.2 corrige la sémantique :
>
> | État lu | Commande réellement émise |
> |---|---|
> | retour en cours | retour à la base |
> | session **zonée** inachevée | **reprise** du nettoyage zoné |
> | session **par segments** inachevée | **reprise** du nettoyage par segments |
> | cartographie inachevée | reprise de la cartographie |
> | aucun des cas ci-dessus | démarrage d'un nettoyage **global** |
>
> Enchaîner `vacuum.start` après `clean_area` ne « confirmerait » donc rien : la session par segments venant d'être ouverte, l'appel tomberait sur le cas « session par segments inachevée » et provoquerait une **reprise**. Et si la session avait entre-temps été close, il déclencherait un **nettoyage global** — c'est-à-dire toute la carte, au lieu du périmètre demandé.
>
> La règle de prudence antérieure est donc **confirmée et durcie** : un `vacuum.start` **ne doit jamais** être ajouté après `clean_area`. Ce n'est plus une précaution par ignorance, c'est une interdiction motivée.

Points à mesurer, non à supposer :

- délai d'application effectif de `fan_speed` ;
- délai d'application effectif des `select` ;
- persistance des réglages lors d'un changement de carte.

---

## 8. Réserve structurante — le comportement multi-cartes

**C'est le point central du prochain lot terrain.** Le Q7 Max porte quatre cartes pour un seul robot ; l'expérience cible traverse trois d'entre elles.

### 8.1 Ce que le code établit

**[CODE] Une commande segmentée ne transporte aucun index de carte.** La charge utile de `app_segment_clean` se réduit à une liste d'index de segments. Or ces index sont **ambigus entre cartes** : `16` désigne `Salon` sur la carte RDC, `Palier` sur l'Étage et `Salle de bain` sur l'Annexe (§5.1). La commande est donc nécessairement interprétée **dans la carte active du robot**, et rien d'autre ne peut la désambiguïser.

**[CODE] Le même constat vaut pour la commande zonée.** `app_zoned_clean` ne transporte que des coordonnées ; aucun index de carte ne l'accompagne.

**[CODE] Home Assistant filtre — et échoue en silence.** La plateforme compare l'index de carte de chaque segment demandé à la carte active, **jette** sans erreur ceux qui ne correspondent pas, et **n'émet rien du tout** si aucun segment ne subsiste. Elle **ne bascule jamais** de carte de sa propre initiative. Les trois issues possibles d'une demande sont donc :

| Demande | Résultat |
|---|---|
| Segments **tous** sur la carte active | Exécutée normalement |
| Segments **partiellement** hors carte active | **Tronquée en silence** — seul le sous-ensemble de la carte active est nettoyé |
| Segments **tous** hors carte active | **Aucune commande émise, aucune erreur levée** — l'action « réussit » et le robot ne bouge pas |

Ce comportement est **couvert par les tests officiels de l'intégration** ; il n'est ni un défaut de configuration ni un accident.

**[CODE] La carte active est un état du robot, pas une intention de Home Assistant.** Elle se déduit du statut de l'appareil. Le sélecteur `select.roborock_q7_max_carte_selectionnee` — **désactivé** dans ce runtime — est le **seul** moyen de la commander depuis HA ; il émet une commande de chargement de carte, attend, puis relit. Son acceptation lorsque le robot se trouve physiquement ailleurs **n'est pas établie** : l'appareil sait refuser ce type de commande dans certains états.

### 8.2 Contrainte de sécurité candidate

> ### IMC-1 — Intégrité multi-cartes d'une commande segmentée
>
> **Aucune commande segmentée ne peut être émise tant que la carte active n'est pas explicitement connue et concordante avec l'intégralité des segments demandés.**
>
> **Pourquoi.** L'index de segment est ambigu entre cartes et la commande ne porte pas la carte (§8.1). Une émission « à l'aveugle » n'a que deux issues, toutes deux inacceptables : **ne rien faire en prétendant avoir lancé**, ou **nettoyer la mauvaise pièce**. Aucune n'est signalée par une erreur.
>
> **Ce que la contrainte de sécurité candidate exige, dans cet ordre :**
>
> 1. la carte active est **lue et connue** au moment de la commande — ce qui rend la réactivation du sélecteur de carte **obligatoire**, et non plus optionnelle (**V5** est requalifié en prérequis) ;
> 2. **tous** les segments demandés appartiennent à cette carte ; à défaut, la demande est **refusée explicitement**, avec un motif lisible — jamais tronquée, jamais silencieuse ;
> 3. un lancement porte sur **une seule carte** — donc sur **un seul** des trois périmètres métier visés (§4) ;
> 4. si la carte active ne peut pas être lue, **aucune commande n'est émise**.
>
> **Portée.** La contrainte de sécurité candidate s'applique à **toute** voie segmentée — `vacuum.clean_area`, commande brute avec `repeat`, ou répétition supervisée. Elle vaut aussi, pour les mêmes raisons, pour la commande zonée. Elle ne s'applique pas aux routines Roborock, qui embarquent leur propre index de carte — **ce qui les lie à une carte, et ne leur permet pas davantage d'en couvrir plusieurs** (§6.3.1).
>
> **Statut.** **Contrainte de sécurité candidate**, issue de l'audit — **à reprendre et arbitrer dans le futur contrat** du domaine. Ce n'est ni un contrat, ni une clause opposable, ni un checker : elle n'a aujourd'hui aucune force normative, et il n'existe d'ailleurs aucun code à contraindre. Un audit relève ; il ne norme pas.
>
> **Le fait technique qui la motive, lui, est établi et ne dépend d'aucun arbitrage** : une commande segmentée émise sans concordance préalable entre la carte active et les segments demandés peut **nettoyer une mauvaise pièce**, ou **réussir silencieusement sans provoquer aucune action** (§8.1).

### 8.3 Ce qui reste à qualifier sur le terrain

1. le comportement de la carte active lorsque le robot est **déplacé physiquement** entre RDC, Étage et Annexe — bascule automatique, ou carte figée ;
2. l'acceptation d'une commande de changement de carte quand le robot se trouve **sur une autre carte** ;
3. la **stabilité dans le temps** des index de segments, notamment après toute re-cartographie (**V8**) ;
4. l'index de la carte Garage et la raison de son absence de segments (§5.1).

Les points antérieurs *« relever la correspondance area ↔ segment ↔ carte »*, *« établir la table index de carte ↔ nom »* et *« traiter les pièces homonymes »* sont **clos** par les §4 et §5.1.

---

## 9. Prochain lot terrain minimal

**Un seul lot, non ouvert à ce jour : « Qualification du nombre de passages sur une pièce unique, carte active prouvée ».**

Objet : produire des **preuves**, pas des livrables. Aucune conception, aucun contrat, aucun YAML runtime, aucune UI.

Le périmètre de ce lot a été **fortement réduit** par la passe du 2026-08-26 : la correspondance area ↔ segment ↔ carte, la table index ↔ nom de carte et la prétendue « seconde liste de pièces » sont **closes par lecture seule** (§4, §5.1, §5.3). Le lot ne conserve que ce qui exige réellement une exécution.

> **Ce lot est explicitement mono-carte.** Aucun essai multi-cartes n'y figure et aucun ne doit y être ajouté. Envoyer un index de segment appartenant à une autre carte que la carte active **ne qualifie pas le multi-cartes** : cela provoque exactement l'ambiguïté déjà démontrée par le code (§8.1) — le robot nettoierait potentiellement `Palier` (`1_16`) là où l'intention était `Salon` (`0_16`). Un tel essai n'apporterait aucune information que le code ne donne déjà, et ferait courir un risque réel. Les questions multi-cartes du §8.3 relèvent d'un **lot ultérieur**, à définir après celui-ci.

### 9.1 Protocole terrain minimal — `×1` puis `×2` sur une pièce unique

**Pièce d'essai : `1_22` — `WC Étage`.** Petite, située sur la carte déjà active, et **explicitement exclue** du cycle de référence du 2026-08-26 (§6.3) — donc sans interférence avec le périmètre métier visé.

**Prérequis, tous obligatoires et vérifiés avant le premier essai :**

| # | Prérequis | Contrôle |
|---|---|---|
| P0 | Robot **sur son dock**, batterie > 50 % | `binary_sensor.…_en_charge = on` |
| P1 | **Aucune session inachevée** — sinon toute lecture est faussée et un démarrage deviendrait une reprise (§7) | `binary_sensor.…_nettoyage = off` |
| P2 | **Carte active prouvée = Étage**, conformément à **IMC-1** | sélecteur de carte réactivé (**V5**) et lu, **ou** énumération de `sensor.…_piece_actuelle` concordant avec les huit segments de l'Étage (§5.1) |
| P3 | Aucune serpillière posée ; profil **sans eau** imposé pour tout le protocole | `binary_sensor.…_serpilliere_fixee = off`, intensité de frottement `off` |
| P4 | Capteur d'erreur du robot réactivé, pour disposer d'un motif en cas d'échec | **V5** |

**Étape 1 — référence `×1`. Obligatoire, et bloquante.**

- Émettre une commande segmentée portant **le seul segment `22`**, **sans** champ de répétition.
- États à observer : `sensor.…_etat` doit passer à `segment_cleaning` ; `sensor.…_piece_actuelle` doit afficher `WC Étage` ; `sensor.…_surface_de_nettoyage` doit croître.
- **Réussite** : les trois témoins basculent et le robot traite la pièce, puis s'arrête.
- **Échec** : aucun mouvement, ou une pièce autre que `WC Étage`.
- **Clôture** : `vacuum.return_to_base` ; attendre `en_charge = on` **et** `nettoyage = off`. **Relever la surface et la durée** — ce sont les grandeurs de référence de l'étape 2.
- Si l'étape 1 est rouge, **le protocole s'arrête là**.

**Étape 2 — `×2`. Seulement si l'étape 1 est verte.**

- Rejouer **strictement la même commande**, avec en plus le champ de répétition correspondant à deux passages.
- Trois issues à distinguer sans ambiguïté :

| Issue | Observation | Lecture |
|---|---|---|
| **Réussite** | Surface ≈ **2 ×** la référence, durée ≈ 2 ×, **sans** retour au dock intercalé | Le champ de répétition est **honoré** par cet appareil |
| **Ignoré en silence** | Commande acceptée, surface ≈ **1 ×** la référence | Le champ est **accepté puis ignoré** — l'issue la plus dangereuse, car aucune erreur n'est levée |
| **Refus** | Erreur protocolaire | Le champ est **rejeté** par cet appareil ; la voie « commande brute » est close |

- **Clôture** : `vacuum.return_to_base`, retour à l'état initial, `nettoyage = off`.

**Règles transverses :** un seul essai par étape ; robot ramené au dock entre les deux ; aucune écriture du mode de nettoyage (§6.1) ; toute étape rouge arrête le protocole ; **aucun essai portant sur une carte autre que l'Étage**.

**Ce que ce protocole ne fait pas** : il ne mesure pas les délais d'application des réglages, ne teste pas la composition de plusieurs pièces, et n'aborde aucune question multi-cartes. Ces objets relèvent de lots ultérieurs.

### 9.2 Arbitrages et gestes opérateur préalables

| # | Attendu | Nature |
|---|---|---|
| V1 | ~~Renommer les segments périmés dans l'application Roborock : `Chambre Arnaud` → `Chambre Enfants`, `Chambre Matthieu` → `Salle de Jeux`, `Pallier` → `Palier`~~ — **RÉALISÉ le 2026-08-26**, correction constatée dans le runtime (§5.4) | Geste terrain — **clos** |
| V2 | Décider des areas HA à créer ou ajuster. **Déblocable** : la liste exhaustive des segments sans area est désormais connue (§5.1, §5.3) — `Dressing`, `WC Étage`, `WC RDC`, et les quatre segments de l'Annexe ; s'y ajoute l'écart `Salon` / `Séjour` | Arbitrage |
| V3 | Trancher le sort de `WC Étage` : intégrer ou exclure explicitement. **Note** : cette pièce sert de pièce d'essai au protocole §9.1, ce qui ne préjuge pas de son sort dans le périmètre métier | Arbitrage |
| V4 | Trancher la sémantique des profils. **Réduit** (§6.1, §6.3) : « normale » ↔ `balanced` est **établi** ; le writer unique de « pas d'eau » est **établi** — c'est l'intensité de frottement, le mode de nettoyage n'étant qu'un état dérivé. Restent à trancher « forte » (`turbo` ou `max`) et « faible » (`quiet` ou `gentle`) | Arbitrage — **résiduel** |
| V5 | Autoriser la réactivation des entités désactivées utiles. **Requalifié en prérequis dur** : sans le sélecteur de carte, la contrainte de sécurité candidate **IMC-1** (§8.2) ne peut pas être satisfaite, et le prérequis `P2` du protocole §9.1 non plus | Décision opérateur — **prérequis** |
| V6 | Autoriser une exécution de test encadrée sur un périmètre restreint — **c'est le protocole §9.1**, une pièce, deux essais | Autorisation explicite |
| V7 | Confirmer la non-régression de l'exclusion alarme portée par `binary_sensor.roborock_q7_max_nettoyage`. **Élément nouveau** : ce binaire signifie « session inachevée », pas « nettoyage en cours » (§3.2) — l'exclusion reste donc active robot à l'arrêt | Validation |
| V8 | Statuer sur la saturation multi-cartes (4/4) : toute re-cartographie invaliderait les index de segments désormais consignés (§5.1) | Arbitrage |
| V10 | Trancher le **nombre de passages** (×1 / ×2 / ×3), qui **fait partie du besoin**. **Recadré** (§6.3.1) : le protocole sait l'exprimer — `app_segment_clean` accepte un champ `repeat` aux côtés des segments — mais aucune action publique de Home Assistant ne l'expose. L'arbitrage porte désormais sur un **choix de dépendance** : commande brute assumée, UI sans ce réglage, répétition supervisée, ou routines Roborock. **À ne trancher qu'après l'essai `×2` du §9.1** | Arbitrage — **structurant** |
| V11 | **Créer le mappage area ↔ segment** sur `vacuum.roborock_q7_max`, absent à ce jour (§3.1). Sans lui, `vacuum.clean_area` échoue en erreur de validation et **aucune voie fondée sur ce service n'est utilisable** | Geste terrain — **prérequis dur** |
| V9 | *(hors chemin critique)* Décider si des entités Roborock doivent entrer au `recorder`. **Extension optionnelle d'observabilité** : ni la commande ni le diagnostic courant n'en dépendent (§6.3.2) | Arbitrage — **optionnel** |

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
| Entité réactivée ou désactivée | **aucune** |
| Mappage area ↔ segment créé ou modifié | **aucun** — c'est précisément le geste `V11` qui reste à faire |

Nature exclusive des accès : lecture des états, des registres (entités, appareils, areas, étages), du registre de services et des libellés de services. Aucun appel de service, aucune écriture.

**Précision sur le relevé de contrôle du 2026-08-26.** Un cycle de nettoyage était **en cours** au moment de cette relecture. Il a été **lancé par l'opérateur depuis l'application Roborock**, hors de cet audit, et ses réglages ont été **déclarés par lui** (§6.3) : aucune commande n'a été émise ici, ni ce jour-là ni la veille. Ce cycle a été observé, jamais provoqué, modifié ni interrompu.

**Précision sur la passe d'audit du code exact (2026-08-26, §2.1).** Elle a porté sur deux natures de sources, toutes deux en lecture :

- **hors runtime** — les sources publiques de Home Assistant Core au tag `2026.8.3` et de `python-roborock` au tag `v5.31.1`, lues hors du dépôt Arsenal ; rien n'en a été copié dans le dépôt ;
- **dans le runtime** — uniquement des commandes de **lecture** de l'API websocket : configuration générale, états, registre de services, registres d'entités, d'appareils et d'areas, entrées de configuration, liste des *repairs*, et l'énumération des segments de l'aspirateur.

Cette dernière est signalée explicitement pour lever toute ambiguïté : **l'énumération des segments est une commande de lecture, pas une action**. Son implémentation retourne le contenu déjà présent en mémoire dans l'intégration, **sans aucune entrée-sortie vers l'appareil** — ce qui a été vérifié dans le code source **avant** de l'appeler. Elle ne peut pas commander le robot et ne provoque aucun trafic vers lui. Le service `roborock.get_maps`, qui est une **action**, n'a **pas** été appelé.

**Aucun flux d'options de config entry n'a été ouvert**, et **aucune boîte de dialogue de mappage segment ↔ area n'a été ouverte ni enregistrée** — l'une comme l'autre créent un état côté serveur.

---

## 11. Ce que ce document n'est pas

- Ce n'est **pas un contrat** : rien ici n'est normatif ni opposable. **IMC-1** (§8.2) n'échappe pas à cette règle : c'est une **contrainte de sécurité candidate** issue de l'audit, **à reprendre et arbitrer dans le futur contrat** du domaine — ni clause opposable, ni checker. Seul le **fait technique** qu'elle consigne est établi.
- Aucun chantier n'est ouvert.
- Aucune architecture n'est décidée : autorité de décision, writer unique, couche de diagnostic et rôle de l'UI restent **à concevoir et à valider** avant toute proposition de code.
- Aucun code, aucun YAML runtime n'est proposé.
