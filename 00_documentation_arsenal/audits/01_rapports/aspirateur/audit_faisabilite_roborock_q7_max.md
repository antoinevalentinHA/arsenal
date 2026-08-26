# 🤖 ARSENAL — AUDIT — Faisabilité d'un pilotage **Roborock Q7 Max**

> **Trace d'audit runtime.** Les passes des 2026-08-25 et 2026-08-26 ont été **strictement en lecture**. Le **lot terrain du 2026-08-26** (§9) a émis, sous autorisation opérateur explicite et essai par essai, des **réglages préparatoires** et des **commandes de nettoyage** — inventaire exhaustif et niveaux de certitude au **§10.2**. Aucun contrat, script, helper, automation, dashboard ni checker créé.
> Convention : **[FAIT]** observé dans le runtime · **[TERRAIN]** établi par le lot terrain T1/T2 · **[CODE]** établi par lecture du code source exact — Home Assistant Core au tag `2026.8.3` et `python-roborock` au tag `v5.31.1`, les versions effectivement en service · **[HYP]** inférence non prouvée · **[RECO]** à arbitrer par l'opérateur · **[DOC]** connaissance documentaire externe au runtime — jamais une preuve terrain propre à cet appareil.
> Ce document est un **relevé d'observation**, pas un contrat. Il n'est ni normatif ni opposable.

---

## Verdict

**`GO` — la voie technique est qualifiée sur le terrain. Elle est **mono-carte par construction**, et le nombre de passages y est **acquis**.**

Le lot terrain du 2026-08-26 (§9) a qualifié la **voie segmentée directe** de bout en bout sur cet appareil : désignation exacte d'un segment dans la carte active, exclusivité du périmètre, nombre de passages honoré, déroulement complet et retour au dock nominal. L'expérience cible — *choisir une carte, choisir des pièces, choisir un profil, choisir le nombre de passages, **Lancer*** — n'a plus d'inconnue technique structurante.

**Ce qui est établi par le terrain (§9) :**

1. `vacuum.send_command` avec `app_segment_clean` et la charge utile enveloppée `[{"segments": [N]}]` **désigne correctement** un segment de la carte active, l'exécute **exclusivement**, et rend la main proprement — **T1 validé**.
2. Le champ `repeat` est **accepté par le Q7 Max**, et sa convention est celle du **comptage** : `repeat: 2` produit **deux passages** — **T2 validé**. Cette convention est **distincte** de celle du nettoyage zoné, où `0` vaut un passage.
3. Le profil `intensité = off` → `mode = vacuum` **tient pendant toute la mission** ; l'appareil le rétablit à `medium` / `vac_and_mop` **au passage en `returning_home`**, jamais au lancement (§6.1).

**Ce que les arbitrages opérateur ont fixé :**

- **La voie technique retenue est la commande segmentée directe** (§9.2) — seule à satisfaire simultanément la sélection libre de pièces, le nombre de passages et le mono-carte contrôlé.
- **Cinq profils métier sont arrêtés** (§6) : aspiration normale, turbo, maximale — toutes trois sans eau — puis serpillière moyenne et intensive. `gentle` exclu. **V4 clos.**
- **Le périmètre de l'Étage compte huit pièces**, `WC Étage` incluse. **V3 clos.**
- **`vacuum.clean_area`, les areas HA et le mappage `area_mapping` sont sans objet** pour la voie retenue — leur analyse est conservée à titre historique (§3.1, §5.3). **V2 et V11 ne sont pas des arbitrages ouverts.**

**Ce qui reste ouvert, et de quelle nature :**

- **La contrainte de sécurité candidate IMC-1** (§8) reste entière et s'est **vérifiée sur le terrain** : la carte doit être sélectionnée et confirmée avant toute commande segmentée. Les index de segments sont homonymes entre cartes.
- **V8** — saturation multi-cartes (4/4) — et **V9** — historisation, hors chemin critique.
- Les questions **multi-cartes** du §8.3 — comportement de la carte active après déplacement physique du robot — restent à qualifier dans un lot ultérieur.

La conception du dashboard et du moteur de commande n'est pas engagée par ce document.

---

## 1. Date, contexte et périmètre

| | |
|---|---|
| **Date d'observation** | 2026-08-25 — **relevé de contrôle le 2026-08-26** (§5.4) — **audit du code exact le 2026-08-26** (§2.1) — **lot terrain T1/T2 le 2026-08-26** (§9) |
| **Contexte** | Étude d'opportunité préalable à tout chantier. Aucun besoin runtime ouvert à ce jour. |
| **Nature** | Audit read-only du runtime Home Assistant + lecture du code source des versions en service + recherche d'antériorité dans le dépôt, **puis** lot terrain de qualification (§9) sous autorisation opérateur essai par essai. |
| **Méthode** | Lecture des états, du registre d'entités, du registre d'appareils, du registre d'areas et du registre de services depuis le frontend HA. Aucune action appelée, aucun formulaire enregistré, aucun flux d'options ouvert. Pour la passe du 2026-08-26 : lecture des sources de Home Assistant Core au tag `2026.8.3` (`components/vacuum/`, `components/roborock/`, tests d'intégration associés) et de `python-roborock` au tag `v5.31.1`, hors dépôt Arsenal. |
| **Preuve de non-commande** | Cf. §10. |

**Antériorité dans le dépôt [FAIT]** — le domaine n'existe pas :

- aucun contrat, aucun dashboard, aucune entrée de navigation, aucun script, aucun helper ;
- **un seul consommateur en production**, dans le domaine alarme — l'exclusion de la détection d'intrusion par mouvement ([`contrats/alarme/50_intrusion_detection.md`](../../../contrats/alarme/50_intrusion_detection.md), `11_automations/alarme/intrusion/mouvement.yaml`). Ce consommateur reposait sur `binary_sensor.roborock_q7_max_nettoyage` ; **il a été corrigé et mergé en production** (PR #724) et s'appuie désormais sur l'état du `vacuum` — `cleaning` et `returning` — c'est-à-dire sur le mouvement réel du robot. **Cet invariant reste à préserver** par tout chantier futur ;
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
| Entités du device | **45** au registre — **19 actives** et **26 désactivées** au relevé initial ; **22 / 23** après les trois réactivations opérateur du 2026-08-26 (§3.4) | [FAIT] |

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
> **Ce n'est ni un blocage technique ni un défaut de l'intégration** : le mappage se crée par un **geste opérateur** dans les paramètres de l'entité, qui écrit dans le registre. Il n'a pas été fait, et l'audit s'est interdit de le faire. Ce geste serait un **prérequis dur** de toute voie fondée sur `clean_area`. La voie retenue étant la commande segmentée directe (§9.2), **il est sans objet** — l'analyse est conservée à titre historique.
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
> **[TERRAIN] Le désalignement est confirmé dans les deux sens.** T1 et T2 (§9) l'ont observé à l'identique : le témoin repasse à **`off` pendant `returning_home`**, alors que le robot roule encore vers son dock — 53 secondes de déplacement à `off` en T1, 25 en T2. Il est donc **sous-exclusif** en fin de mission, autant qu'il était **sur-exclusif** sur une session ouverte robot immobile.
>
> **Portée sur l'existant — résolu en production.** L'exclusion d'intrusion était câblée sur ce binaire. **La PR #724 l'a corrigée et mergée** : l'inhibition repose désormais sur l'état du `vacuum` (`cleaning`, `returning`), c'est-à-dire sur le mouvement réel. **V7 est clos.** Aucun travail alarme n'est ouvert ni requis par ce document.

### 3.3 Prérequis matériels observables

| Prérequis | Entité | État observé |
|---|---|---|
| Serpillière fixée | `binary_sensor.roborock_q7_max_serpilliere_fixee` | **`off`** — aucune serpillière posée |
| Réservoir d'eau fixé | `binary_sensor.roborock_q7_max_reservoir_d_eau_fixe` | `on` |
| Pénurie d'eau | `binary_sensor.entree_roborock_q7_max_penurie_d_eau` | `off` |
| Séchage serpillière (dock) | `binary_sensor.entree_roborock_q7_max_dock_sechage_de_la_serpilliere` | `off` |

**[FAIT] Les prérequis matériels des profils avec eau sont observables.** Ils ne sont pas commandables : poser ou retirer la serpillière est un **geste opérateur**.

### 3.4 Prérequis runtime — réactivations réalisées

**[TERRAIN] Trois entités décisives ont été réactivées par l'opérateur le 2026-08-26**, avant le lot terrain. Elles sont désormais **actives et exploitées** :

| Entité | Statut | Rôle établi |
|---|---|---|
| `select.roborock_q7_max_carte_selectionnee` | **active** | Sélection **et lecture** de la carte active — prérequis d'IMC-1 (§8), utilisé et validé par T1/T2 |
| `sensor.roborock_q7_max_erreur_de_l_aspirateur` | **active** | Motif d'erreur détaillé — a rendu lisible l'immobilisation `wheels_suspended` du 2026-08-26 |
| `sensor.roborock_q7_max_dock_erreur_de_dock` | **active** | Motif d'erreur du dock |

**V5 est donc clos.** Restent désactivées, sans conséquence sur le chemin critique :

| Entité désactivée | Ce qu'elle apporterait |
|---|---|
| `sensor.roborock_q7_max_debut_du_dernier_nettoyage` / `…_fin_du_dernier_nettoyage` | Bornes natives d'une session |
| `button.roborock_q7_max_nettoyage_complet` | **Déclenchement d'une routine Roborock existante**, cf. encadré ci-dessous |

**[FAIT] Un diagnostic minimal honnête était déjà possible sans elles**, à partir de l'état général du robot, du caractère `unknown` / `unavailable` des entités, de l'état machine et des prérequis matériels. Les capteurs d'erreur **améliorent** ce diagnostic ; ils ne le conditionnaient pas.

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

**[FAIT] La carte active au moment du relevé initial était l'Étage, index `1`** — `sensor.roborock_q7_max_piece_actuelle` énumérait exactement ses huit segments. L'ancienne mention `[HYP]` est convertie en fait.

> ### [TERRAIN] Le sélecteur de carte exprime une **sélection**, pas une **localisation**
>
> Le 2026-08-26, après un cycle à l'Étage, le robot a été **transporté manuellement** jusqu'à sa base, située au RDC. **Le sélecteur est resté sur `Étage`.** Le robot se trouvait donc physiquement au RDC pendant que le contexte cartographique désignait l'Étage.
>
> `select.roborock_q7_max_carte_selectionnee` **ne prouve donc jamais où se trouve le robot**, et il ne se recale pas de lui-même après un déplacement physique. Il ne peut être lu que comme ce qu'il est : le dernier contexte cartographique sélectionné.
>
> **[TERRAIN] La sélection explicite fonctionne, et se vérifie par deux voies indépendantes.** Après écriture de `RDC` sur le sélecteur :
>
> - `sensor.…_piece_actuelle` a exposé les **quatre segments RDC** (`Salon`, `Entrée`, `WC RDC`, `Cage d'escaliers`) — confirmation par la couche entités ;
> - le statut brut a donné **`mapStatus = 3`**, soit `map_flag = 0` — **confirmation protocolaire**, indépendante de la couche entités.
>
> Cette bascule n'a produit **aucun mouvement** du robot, resté amarré et en charge.
>
> **[TERRAIN] Corroboration de position.** Après la bascule, `piece_actuelle` est passé à `Entrée` — la pièce où se trouve la base. Le runtime localise donc le robot sur la carte sélectionnée ; c'est la **conjonction** du sélecteur et de la pièce courante qui devient informative, jamais le sélecteur seul.
>
> **Conséquence pour le futur contrat.** Les index de segments étant homonymes entre cartes (§5.1), **la sélection de la carte et sa confirmation restent un prérequis de sécurité** de toute commande segmentée — c'est le premier point d'IMC-1 (§8.2).

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
| **Pièces sans area HA** | Liste désormais **exhaustive** grâce à la table du §5.1 : `Dressing` et `WC Étage` (Étage) ; `WC RDC` (RDC) ; `Salle de bain`, `Ext`, `Chambre1`, `Chambre` (Annexe — l'area `Petite Maison` n'est pas découpée). | **Sans objet pour la voie retenue** (§9.2) — la commande segmentée désigne des segments, pas des areas. Liste conservée à titre historique. |
| **Nom divergent, séjour** | Segment Roborock `Salon` (`0_16`) vs area HA `Séjour`. | Sans effet sur la voie retenue ; le libellé UI canonique Arsenal reste « Séjour ». |

> **[RECO] Règle de restitution — durable.** L'UI Arsenal ne devra **jamais** restituer un nom de pièce provenant directement du robot sans contrôle. Toute pièce affichée doit l'être sous son nom canonique Arsenal, ou pas du tout. Les anciens noms ont été corrigés à la source le 2026-08-26 ; la règle reste nécessaire, car rien n'empêche qu'un futur renommage réintroduise un écart.

> **[FAIT] Correction — il n'y a pas de « second référentiel ». La divergence signalée n'existe pas.**
>
> Les passes précédentes avaient relevé « deux listes de pièces qui ne se recouvrent pas » : les 8 segments de la carte active, et « une liste courte issue du compte » de 4 entrées — `Salle de bain`, `Ext`, `Chambre1`, `Chambre` — en s'interrogeant sur celle qui ferait autorité pour `clean_area`.
>
> La table complète du §5.1 lève l'ambiguïté : **ces quatre entrées sont exactement les quatre segments de la carte Annexe** (`2_16` à `2_19`). Ce n'était pas un référentiel concurrent, mais **une autre carte du même référentiel**. Il n'existe qu'une seule liste de pièces, indexée par carte, et c'est elle qui alimente la résolution.
>
> Cette question — *« déterminer laquelle des deux listes fait autorité »* — est **sans objet**. Elle avait été inscrite au lot terrain ; elle en a été retirée avant exécution.

### 5.4 Relevé de contrôle du 2026-08-26

**[FAIT]** Après renommage des segments par l'opérateur dans l'application Roborock, la correction est **remontée jusqu'à Home Assistant sans intervention** : les segments de la carte active sont désormais `Palier`, `Chambre Parents`, `Chambre Enfants`, `Salle de Jeux`, `Dressing`, `SDB Parents`, `WC Étage`, `SDB Enfants`.

**[FAIT]** Le référentiel d'areas Home Assistant est **inchangé** (14 areas, mêmes noms). `Palier` et `Chambre Enfants` concordent désormais exactement entre les deux référentiels ; les écarts de casse subsistent sur les quatre autres.

**[FAIT] Enseignement complémentaire.** Le renommage d'un segment côté application est répercuté par l'intégration. Un futur affichage ne peut donc pas traiter ces libellés comme stables : ils sont **modifiables hors du dépôt et hors de Home Assistant**.

---

## 6. Les profils métier — **arrêtés**

**[RECO → arbitré] Les profils sont fixés par décision opérateur du 2026-08-26.** Ils sont au nombre de **cinq**, et non plus quatre : la correspondance de « forte » — `turbo` ou `max` — n'a pas été tranchée en faveur de l'une, mais **résolue en exposant les deux**.

| Profil métier | Aspiration | Intensité d'eau | Mode *(dérivé, jamais écrit)* | Prérequis matériel |
|---|---|---|---|---|
| **Aspiration normale** | `balanced` | `off` | `vacuum` | — |
| **Aspiration turbo** | `turbo` | `off` | `vacuum` | — |
| **Aspiration maximale** | `max` | `off` | `vacuum` | — |
| **Serpillière moyenne** | `quiet` | `medium` | `vac_and_mop` | serpillière posée |
| **Serpillière intensive** | `quiet` | `high` | `vac_and_mop` | serpillière posée |

**Règles attachées à cette table :**

- **`gentle` est exclu** des profils métier. Il ne relève pas de la gradation de puissance (§6.3).
- **`mode_de_nettoyage` reste un état dérivé** et **ne doit jamais être écrit** : l'écrire écrase l'aspiration à `balanced` (§6.1). Seules l'intensité d'eau et l'aspiration se pilotent.
- **Le nombre de passages `×1` / `×2` / `×3` est indépendant du profil.** Il se règle dans la charge utile de la commande, pas dans le profil (§6.3.1).
- Les deux profils avec eau restent **non commandables tant que la serpillière est absente** — condition matérielle à représenter explicitement, jamais à contourner (§6.2).

**V4 est clos.** Ce qui suit conserve la trace de la manière dont ces valeurs ont été établies.

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
> Cela a **réduit V4** : le levier d'écriture de « pas d'eau » n'était plus à trancher. Les correspondances restantes ont depuis été arbitrées (§6) — **V4 est clos**.

> ### [TERRAIN] Le profil est rétabli **en fin de mission**, pas au lancement
>
> Reproduit à l'identique sur **T1 et T2** (§9), aux horodatages près :
>
> | Instant | `intensité` / `mode` |
> |---|---|
> | Après écriture préparatoire | `off` / `vacuum` |
> | **Au lancement** | **inchangé** |
> | Pendant toute la mission | **inchangé** |
> | **Au passage en `returning_home`** | **→ `medium` / `vac_and_mop`** |
>
> La bascule coïncide **à la seconde** avec l'entrée en retour au dock. `fan_speed` n'est jamais touché et reste à la valeur posée.
>
> **Trois conséquences pour tout futur chantier :**
>
> 1. **Le profil doit être écrit explicitement avant chaque lancement.** Il ne se conserve pas d'un cycle au suivant.
> 2. **L'état du profil lu après un cycle ne prouve pas le profil utilisé pendant ce cycle.** Un diagnostic a posteriori fondé sur cette lecture serait faux.
> 3. Le réglage posé avant lancement, lui, **tient pendant toute la mission** — c'est ce qui rend la séquence « régler puis lancer » praticable.
>
> **Ce qui est établi, et ce qui ne l'est pas.**
>
> **[TERRAIN] Établi — le moment.** Le rétablissement coïncide avec le **passage en `returning_home`**, reproduit deux fois à la seconde près.
>
> **[FAIT — opérateur] Établi — l'expérience opérateur.** Dans l'application officielle, la carte, les pièces, l'aspiration, l'eau et le nombre de passages sont **redéfinis à chaque nouvelle préparation** de nettoyage. **Aucun profil persistant par pièce n'est exposé dans cette expérience opérateur.**
>
> **Non établi — la cause interne.** Le mécanisme qui produit le retour à `medium` / `vac_and_mop` n'est **pas attribué**. Rien ici ne permet d'affirmer qu'aucun profil persistant par pièce n'existe **techniquement** dans l'appareil : seule son absence d'exposition côté application est constatée. Le document ne se prononce pas au-delà.

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

**[FAIT] Correspondance établie par recoupement.** « Normal » côté application ↔ **`balanced`** côté HA, par une déclaration opérateur et une observation runtime concordantes. C'est le premier maillon de la table de profils du §6, depuis **arrêtée**.

**[DOC] Gamme standard Roborock.** La documentation de la gamme distingue quatre niveaux d'aspiration — `quiet`, `balanced`, `turbo`, `max` — dont `balanced` est le niveau courant, ce que le recoupement ci-dessus confirme pour cet appareil. `gentle` n'appartient pas à cette échelle : il relève d'un régime de déplacement distinct, hors gradation de puissance. Cette connaissance est **documentaire** ; elle n'a pas été vérifiée sur le Q7 Max et ne vaut pas preuve terrain.

**[CODE] Corroboration structurelle.** La liste d'aspiration n'est pas figée par modèle : elle est **composée** à partir des bits de capacité de l'appareil. Le socle est `quiet` · `balanced` · `turbo` · `max` ; `gentle` y est **ajouté ensuite**, précisément parce que cet appareil ne sait pas laver sans aspirer. L'ordre relevé dans le runtime correspond exactement à cette composition. `gentle` porte par ailleurs un code protocolaire **supérieur** à celui de `max` : le code ne le classe donc **pas** comme un niveau faible.

**[HYP → arbitré]** Sur cette base, « faible » a été retenu comme **`quiet`** et `gentle` **exclu** des profils métier (§6). L'hypothèse reposait sur la convergence documentaire et structurelle ci-dessus, non sur une observation terrain — l'arbitrage opérateur l'a assumée comme telle.

**[FAIT] Composition de périmètre confirmée sur l'appareil.** Sept segments d'une même carte ont été nettoyés en une seule demande — soit tous les segments de la carte Étage **sauf `WC Étage`**. La capacité du robot à traiter un périmètre composé est donc établie. Cela ne préjuge pas de la façon dont `vacuum.clean_area` résout les areas HA, qui reste à qualifier.

### 6.3.1 Nombre de passages — **résolu par le terrain**

Le nombre de passages (**×1 / ×2 / ×3**) **fait partie du besoin à exposer**. Il a été qualifié par le lot terrain du §9 : **il est atteignable, et son encodage est connu.**

**[FAIT] Aucune entité ne le porte.** Sur les **45 entrées** du registre — actives comme désactivées — aucune ne représente un nombre de passages. La seule entité de comptage, `sensor.roborock_q7_max_nombre_total_de_nettoyages` (désactivée), est un cumul de vie, sans rapport avec le réglage d'un cycle. Il n'est donc **pas** réglable par une entité, mais par la charge utile de la commande.

**[FAIT] Deux commandes protocolaires le portent, avec deux conventions distinctes.**

| Commande | Désignation du périmètre | Champ | Convention |
|---|---|---|---|
| `app_segment_clean` | **segments** de la carte active | `repeat` | **comptage** — `repeat: 2` = **deux** passages · **[TERRAIN] établi** |
| `app_zoned_clean` *(via `roborock.set_vacuum_zoned_cleaning`)* | **coordonnées** d'un rectangle | `repeats`, borné `0..2` | **décalage** — `0` = un seul nettoyage · **[FAIT]** libellé officiel du service |

> **[TERRAIN] Ne jamais transposer l'une à l'autre.** Ces deux conventions sont **incompatibles**, et une passe antérieure de cet audit avait commis l'erreur d'appliquer la convention zonée à la commande segmentée. Le terrain a tranché : sur `app_segment_clean`, `repeat` **compte les passages**.

**[TERRAIN] La tension supposée entre « désigner des pièces » et « répéter » n'existe pas.** Elle avait été énoncée au niveau des *services* Home Assistant, où elle est réelle : `vacuum.clean_area` ne porte qu'un champ, `cleaning_area_id`. Mais la commande protocolaire sous-jacente, elle, porte les deux. **`app_segment_clean` désigne des segments et les répète dans le même appel** — c'est désormais un fait terrain, pas une lecture de documentation.

> **[CODE] Correction majeure — la tension n'existe pas au niveau du protocole, seulement au niveau de l'exposition.**
>
> La commande protocolaire `app_segment_clean` — celle-là même que `vacuum.clean_area` finit par émettre — **accepte un champ `repeat` dans le même appel que la liste de segments**. La documentation de la bibliothèque embarquée par l'intégration la décrit sans ambiguïté : *elle démarre un nettoyage par segments et le répète le nombre de fois indiqué*, avec une charge utile associant une liste de segments et un `repeat`.
>
> **Home Assistant construit cette charge utile sans le champ `repeat`.** Le manque n'est donc **pas** dans le protocole ni dans l'appareil : il est dans la **couche d'exposition** de l'intégration. « Pièces + répétitions » est exprimable en **une seule primitive** ; simplement, aucune action publique de Home Assistant ne l'expose.
>
> Trois indices convergents dans la bibliothèque, tous **non exposés** par l'intégration : le statut du robot décode un champ `repeat` (aucune entité ne le porte) ; l'énumération des commandes comporte un `set_clean_repeat_times` (jamais appelé, non documenté) ; un bit de capacité relatif à la répétition existe (jamais lu).
>
> **[TERRAIN] L'acceptation par `roborock.vacuum.a38` est désormais prouvée** (§9). La réserve antérieure — *« l'appareil coché dans cette documentation n'est pas le Q7 Max »* — est **levée**. Le bit de capacité `isCtmWithRepeatSupported`, relevé à `false` sur cet appareil, **ne gouverne pas** la répétition segmentée : il ne doit pas être lu comme un signal de non-support.

**[TERRAIN] Ce que le terrain change pour V10.** L'arbitrage ne porte plus sur *« pièces sans répétition, ou coordonnées avec répétition »*, ni sur l'acceptation du champ. Il porte uniquement sur : **assumer ou non la dépendance à `vacuum.send_command`** pour émettre la commande segmentée avec `repeat`.

Ce que cela coûterait, énoncé sans complaisance :

- `vacuum.send_command` **reste une action publique de Home Assistant** — l'utiliser n'est pas un contournement de l'API. **Mais elle expose une commande protocolaire privée sans la validation ni l'abstraction de `clean_area`** : ni résolution des areas, ni contrôle de la carte active, ni bornes vérifiées, ni erreur intelligible. Tout ce que `clean_area` garantit devrait être **réimplémenté et maintenu côté Arsenal**.
- Le contrat de cette commande n'est garanti ni par Home Assistant ni par l'appareil : **il peut changer sans préavis**. Le risque d'un `repeat` ignoré en silence, lui, est **écarté sur cet appareil et à cette version** par T2 — il n'est pas écarté pour l'avenir.
- **La structure de la charge utile est déterminante.** T1 et T2 ont validé la forme **enveloppée** `[{"segments": [...], "repeat": N}]` — celle que l'intégration émet elle-même. Un objet **nu** `{"segments": …}` est documenté comme **échouant en silence** ; il ne doit jamais être employé.
- La contrainte de sécurité candidate **IMC-1** (§8) s'applique intégralement : cette voie reste **mono-carte**.

**[FAIT] Une quatrième voie existe et elle est déjà présente : les routines Roborock (§3.4).** La structure d'une routine associe, dans une même définition, une liste de segments, **un index de carte**, un profil complet et **un nombre de passages**. C'est la seule structure connue qui exprime tout cela d'un coup.

Ses limites sont toutefois dirimantes pour une architecture pilotée par contrat :

- elle **n'est pas paramétrable depuis Home Assistant** — le bouton ne prend aucun argument ; il faudrait **une routine, donc un bouton, par combinaison** périmètre × profil × passages ;
- la définition vit **dans l'application Roborock**, donc **hors du dépôt, hors CI et hors contrat** ;
- son déclenchement passe **obligatoirement par le cloud** ;
- **le fait qu'une routine porte un index de carte ne démontre pas qu'une mission unique puisse couvrir plusieurs cartes.** Une routine porteuse d'un index de carte est **liée à cette carte** : l'index y désigne le contexte d'exécution, il ne compose rien. Rien dans ce qui a été lu n'établit qu'une mission puisse traverser plusieurs cartes.

> **[RECO] V10 est clos pour la conception.** Le nombre de passages n'est plus une contrainte : il est **atteignable, encodé et prouvé** sur cet appareil, par la voie segmentée directe. Les options « UI sans ce réglage », « répétition supervisée par missions successives » et « délégation aux routines Roborock » **deviennent sans objet** — elles n'existaient que pour contourner une impossibilité qui n'en était pas une.
>
> Ce qui subsiste est un **choix de dépendance assumé** : utiliser `vacuum.send_command` implique de réimplémenter côté Arsenal les garanties que `clean_area` apportait. C'est une décision d'architecture, à porter dans le futur contrat — pas une inconnue technique.

#### Niveaux de preuve du nombre de passages

| Élément | Niveau de preuve |
|---|---|
| `×1` — commande segmentée sans `repeat` | **Preuve terrain** — T1 (§9) |
| `repeat: 2` = **deux passages** | **Preuve terrain** — T2 (§9) |
| Convention de **comptage** sur `app_segment_clean` | **Établie** — par comparaison T1 / T2 |
| `repeat: 3` = **trois passages** | **Déduction protocolaire**, cohérente avec la sémantique de comptage établie et avec la capacité `×3` offerte par l'application officielle sur cet appareil — **non testé par Arsenal** |
| Suffisance de ces preuves | **Acceptation opérateur explicite**, sans essai supplémentaire |

**Aucun essai `repeat: 3` n'est requis ni demandé.** L'application officielle propose déjà `×1`, `×2` et `×3` sur cet appareil, et l'opérateur a jugé un troisième essai inutile. Le document ne prétend pas que `×3` a été vérifié sur le terrain — il consigne une déduction assumée.

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

**[TERRAIN] La séquence « régler puis lancer » est praticable.** T1 et T2 l'ont exécutée deux fois : écriture de l'intensité d'eau, confirmation par relecture, puis émission de la commande. Le réglage a été **appliqué et tenu pendant toute la mission** dans les deux cas. Aucune course n'a été observée entre le réglage et le lancement, avec une confirmation intercalée.

Restent à mesurer, sans caractère bloquant :

- le délai d'application **minimal** de `fan_speed` et des `select` — les essais ont laissé s'écouler une confirmation, sans chercher la borne basse ;
- la persistance des réglages **lors d'un changement de carte**.

---

## 8. Contrainte structurante — le mono-carte

Le Q7 Max porte quatre cartes pour un seul robot ; l'expérience cible traverse trois d'entre elles. **Un lancement ne peut en couvrir qu'une.**

Ce n'est plus une inconnue mais une **contrainte de conception établie**, dont le fait technique est démontré par le code et vérifié sur le terrain. Ce qui reste à qualifier — comportement de la carte active après déplacement physique — relève d'un lot ultérieur (§8.3) et ne bloque pas un pilotage mono-carte.

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

**[CODE] La carte active est un état du robot, pas une intention de Home Assistant.** Elle se déduit du statut de l'appareil. Le sélecteur `select.roborock_q7_max_carte_selectionnee` — **désormais actif** (§3.4) — est le **seul** moyen de la commander depuis HA ; il émet une commande de chargement de carte, attend, puis relit.

**[TERRAIN] La bascule de carte fonctionne, robot amarré, et se confirme par deux voies.** Sélection de `RDC` acceptée, quatre segments RDC exposés par `piece_actuelle`, et `mapStatus = 3` (`map_flag = 0`) au statut brut. Aucun mouvement provoqué. La bascule s'est ensuite **maintenue plus de quatre heures** et à travers deux missions.

**[TERRAIN] Le sélecteur ne se recale pas après un déplacement physique** : transporté de l'Étage au RDC, le robot a laissé le sélecteur sur `Étage` (§4). L'acceptation d'un changement de carte **lorsque le robot se trouve physiquement sur une autre carte** reste **non établie** — le cas testé était celui d'un robot déjà présent sur la carte demandée.

### 8.2 Contrainte de sécurité candidate

> ### IMC-1 — Intégrité multi-cartes d'une commande segmentée
>
> **Aucune commande segmentée ne peut être émise tant que la carte active n'est pas explicitement connue et concordante avec l'intégralité des segments demandés.**
>
> **Pourquoi.** L'index de segment est ambigu entre cartes et la commande ne porte pas la carte (§8.1). Une émission « à l'aveugle » n'a que deux issues, toutes deux inacceptables : **ne rien faire en prétendant avoir lancé**, ou **nettoyer la mauvaise pièce**. Aucune n'est signalée par une erreur.
>
> **Ce que la contrainte de sécurité candidate exige, dans cet ordre :**
>
> 1. la carte active est **lue et connue** au moment de la commande — ce qui rend le sélecteur de carte **obligatoire** ; il a été réactivé, et T1/T2 ont validé la pratique consistant à **sélectionner puis confirmer** avant toute émission (**V5** clos) ;
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

1. le comportement de la carte active lorsque le robot est **déplacé physiquement** entre RDC, Étage et Annexe — **[TERRAIN] partiellement tranché** : la carte **ne se recale pas** d'elle-même après transport (§4). Reste à savoir si un déplacement peut, dans d'autres conditions, provoquer une bascule automatique ;
2. l'acceptation d'une commande de changement de carte quand le robot se trouve **physiquement sur une autre carte** — **non établie** ; le cas validé par T1/T2 est celui d'un robot déjà présent sur la carte demandée ;
3. la **stabilité dans le temps** des index de segments, notamment après toute re-cartographie (**V8**) ;
4. l'index de la carte Garage et la raison de son absence de segments (§5.1).

Les points antérieurs *« relever la correspondance area ↔ segment ↔ carte »*, *« établir la table index de carte ↔ nom »* et *« traiter les pièces homonymes »* sont **clos** par les §4 et §5.1.

**Ces questions relèvent d'un lot ultérieur.** Elles ne bloquent pas la conception d'un pilotage mono-carte, qui est le cadre imposé par IMC-1.

---

## 9. Lot terrain — **consommé le 2026-08-26**

Le lot terrain prévu par les passes précédentes a été **exécuté et clos**. Il portait sur une pièce unique, carte active prouvée, en mono-carte strict. Son objet était de produire des preuves, non des livrables : aucun contrat, aucun YAML runtime, aucune UI n'en est issu.

**Cadre d'exécution.** Chaque écriture a été autorisée par l'opérateur, essai par essai, après relecture de douze contrôles de garde. Aucune seconde tentative, aucune action corrective. Le risque matériel au RDC avait été explicitement levé par l'opérateur.

### 9.1 Résultats

**Cible commune aux deux essais** : carte `RDC`, segment `0_21` — `Cage d'escaliers`. Petite pièce, peu encombrée, sur la carte rendue active et confirmée au préalable.

> **Rappel de l'enjeu d'homonymie.** L'index nu `21` désigne `Cage d'escaliers` sur la carte RDC, mais `SDB Parents` sur la carte Étage (§5.1). La sélection **et la confirmation** de la carte étaient donc un prérequis absolu, conformément à IMC-1.

#### T1 — `×1`, sans champ `repeat` · **VALIDÉ**

Commande : `vacuum.send_command`, `command: app_segment_clean`, `params: [{"segments": [21]}]`.

| Observation | Résultat |
|---|---|
| Acceptation | commande acceptée, contexte Home Assistant retourné |
| État machine | `segment_cleaning` dès la seconde de l'émission |
| Cible | `sensor.…_piece_actuelle` → **`Cage d'escaliers`** |
| Surface finale | **4,7 m²** |
| Durée | **3,8 min** |
| Exclusivité | périmètre restreint à une seule petite pièce |
| Fin de cycle | `returning_home` → `docked` → `charging`, automatique |
| Erreurs | **aucune**, ni robot ni dock |

**[TERRAIN] La structure enveloppée est opérante.** `[{"segments": [N]}]` — la forme que l'intégration émet elle-même — désigne correctement le segment et l'exécute.

#### T2 — `repeat: 2` · **VALIDÉ**

Commande identique, augmentée du champ : `params: [{"segments": [21], "repeat": 2}]`.

| | T1 — sans `repeat` | T2 — `repeat: 2` | Rapport |
|---|---|---|---|
| **Durée de nettoyage** | **3,8 min** | **7,2 min** | **× 1,89** |
| Surface finale | 4,7 m² | 4,4 m² | × 0,94 |
| Cible | `Cage d'escaliers` | `Cage d'escaliers` | identique |
| Erreurs | aucune | aucune | — |

**[TERRAIN] Deux passages établis.** Le rapport de durée est indiscernable de 2 aux imprécisions de trajectoire près. Un `×3` aurait donné environ 11,4 min ; un `×1`, environ 3,8. L'écart ne prête pas à interprétation.

**[TERRAIN] La convention est celle du comptage** : `repeat: 2` signifie **deux passages**. Elle est **distincte** de la convention décalée du nettoyage zoné, où `0` vaut un seul nettoyage (§6.3.1).

> **[TERRAIN] Comment lire les deux compteurs — leçon de méthode.**
>
> La surface a **plafonné à 4,4 m²** à mi-parcours, pendant que la durée continuait de croître près de quatre minutes de plus. Ce n'est pas une anomalie : `cleanArea` mesure l'**aire couverte**, et repasser sur une zone déjà comptabilisée n'y ajoute rien.
>
> - **La durée est le discriminant du nombre de passages.**
> - **La surface est le discriminant du périmètre.**
>
> L'attente initiale d'un doublement de surface était erronée ; le plafonnement, suivi de plusieurs minutes de nettoyage supplémentaire, est en soi la preuve du repassage.

#### Acquis transverses des deux essais

| Élément | Statut |
|---|---|
| `vacuum.send_command` + `app_segment_clean` | ✅ accepté par l'appareil |
| Structure enveloppée `[{…}]` | ✅ opérante, avec et sans `repeat` |
| Désignation d'un segment dans la carte active | ✅ exacte |
| Exclusivité du segment | ✅ vérifiée deux fois |
| Champ `repeat` accepté par le Q7 Max | ✅ oui |
| Encodage de `repeat` | ✅ comptage — `2` = deux passages |
| Déroulement complet et retour au dock | ✅ nominal, deux fois |
| Profil tenu pendant la mission, rétabli au retour | ✅ reproduit deux fois (§6.1) |
| Témoin de session `off` pendant `returning_home` | ✅ reproduit deux fois (§3.2) |

### 9.1.1 Un incident d'outillage, sans effet sur l'appareil

Une première émission de T1 a **échoué en transport** côté client : exception opaque, sans requête parvenue à Home Assistant. Le robot n'a pas bougé, aucun état n'a changé, et le journal système est resté vide. La même émission, rejouée à l'identique après rechargement, a abouti normalement.

**[TERRAIN] Enseignement.** Une exception côté client **ne qualifie pas** la commande Roborock. Un futur moteur devra distinguer trois issues — canal indisponible, commande rejetée, commande acceptée — et ne jamais conclure à l'invalidité d'une commande sur la seule foi d'une erreur de transport.

*(Un cycle antérieur a par ailleurs été **arrêté manuellement** par une personne présente sur place. Il n'avait accumulé que `cleanTime = 5 s` de nettoyage — grandeur à ne pas confondre avec le délai écoulé entre la commande et l'arrêt, de l'ordre de la minute. Cet essai a été écarté comme non concluant, et rejoué intégralement.)*

### 9.2 Arbitrages — état au 2026-08-26

#### Voie technique retenue

**[RECO → arbitré] Le futur moteur reposera sur la commande segmentée directe.** C'est la seule voie qui satisfait **simultanément** les trois exigences du besoin :

| Exigence | Commande segmentée directe | `vacuum.clean_area` |
|---|---|---|
| Sélection libre d'une ou plusieurs pièces | ✅ liste de segments | ✅ areas HA |
| `×1` / `×2` / `×3` | ✅ champ `repeat` | ❌ **absent du service** |
| Fonctionnement mono-carte contrôlé | ✅ sous IMC-1 | ✅ sous IMC-1 |

Ce choix a une conséquence directe sur les arbitrages : **`vacuum.clean_area`, les areas Home Assistant et le mappage `area_mapping` ne sont plus des prérequis du moteur retenu.**

#### Clos

| # | Objet | Clôture |
|---|---|---|
| **V1** | Renommer les segments périmés dans l'application Roborock | **Réalisé** — `Chambre Enfants`, `Salle de Jeux`, `Palier` ; correction constatée dans le runtime (§5.4) |
| **V3** | Sort de `WC Étage` dans le périmètre métier | **Tranché — `WC Étage` fait partie du besoin.** L'Étage métier compte **huit pièces** : `Palier`, `Chambre Enfants`, `Chambre Parents`, `Salle de Jeux`, `SDB Enfants`, `SDB Parents`, `Dressing`, `WC Étage` |
| **V4** | Sémantique des profils métier | **Tranché** — cinq profils arrêtés (§6). « forte » n'est pas départagé entre `turbo` et `max` : **les deux sont exposés** comme profils distincts. `gentle` exclu. Le mode reste dérivé et non écrit |
| **V5** | Réactiver les entités désactivées utiles | **Réalisé** — sélecteur de carte et deux capteurs d'erreur actifs ; utilisés et validés par T1/T2 (§3.4) |
| **V6** | Autoriser une exécution de test encadrée | **Consommé** — lot terrain §9, deux essais, deux validations |
| **V7** | Exclusion alarme fondée sur le témoin de session | **Résolu en production** — PR #724 mergée ; l'inhibition repose désormais sur l'état du `vacuum` (`cleaning`, `returning`), donc sur le mouvement réel. Aucun chantier alarme ouvert par ce document |
| **V10** | Nombre de passages ×1 / ×2 / ×3 | **Clos pour la conception** — atteignable, encodé, prouvé (§6.3.1). `×3` reste une déduction protocolaire assumée, non testée, explicitement acceptée par l'opérateur |

#### Sans objet pour la voie retenue

Ces deux points **ne sont pas des arbitrages ouverts** : ils ne concernent que la voie `clean_area`, qui n'est pas retenue. Leur analyse est conservée au §3.1 et au §5.3 à titre historique, et redeviendrait pertinente si la voie technique était un jour reconsidérée.

| # | Objet | Statut |
|---|---|---|
| **V2** | Créer ou ajuster des areas HA pour les segments qui n'en ont pas | **Sans objet** — la commande segmentée désigne des segments, pas des areas |
| **V11** | Créer le mappage area ↔ segment sur l'entité | **Sans objet** — prérequis de `clean_area` seul |

#### Ouverts

| # | Attendu | Nature |
|---|---|---|
| **V8** | Statuer sur la saturation multi-cartes (4/4) : toute re-cartographie invaliderait les index de segments consignés (§5.1) | Arbitrage |
| **V9** | *(hors chemin critique)* Inscrire ou non des entités Roborock au `recorder`. Extension optionnelle d'observabilité (§6.3.2) | Arbitrage — **optionnel** |

#### Questions techniques restantes

Elles relèvent d'un **lot ultérieur** et ne bloquent pas un pilotage mono-carte : comportement de la carte active après déplacement physique du robot, acceptation d'un changement de carte robot situé ailleurs, stabilité des index dans le temps, cas de la carte Garage (§8.3).

## 10. Écritures et commandes — inventaire exhaustif

Ce document couvre deux régimes distincts, qu'il ne faut pas confondre.

### 10.1 Passes d'audit des 2026-08-25 et 2026-08-26 — lecture seule

| Contrôle | Résultat |
|---|---|
| Actions Home Assistant exécutées | **aucune** |
| Commandes envoyées au Roborock | **aucune** |
| Paramètres Home Assistant modifiés | **aucun** |
| Mapping pièce / area / étage / appareil modifié | **aucun** |
| Helper, script, automation, scène, dashboard créé ou modifié | **aucun** |
| Flux d'options de config entry ouvert | **aucun** — volontairement écarté, un tel flux crée un état côté serveur |
| Mappage area ↔ segment créé ou modifié | **aucun** — geste `V11`, désormais sans objet (§9.2) |

Nature exclusive des accès : lecture des états, des registres (entités, appareils, areas, étages), du registre de services et des libellés de services.

**Précision sur la passe d'audit du code exact (§2.1).** Elle a porté sur deux natures de sources, toutes deux en lecture : **hors runtime**, les sources publiques de Home Assistant Core au tag `2026.8.3` et de `python-roborock` au tag `v5.31.1`, lues hors du dépôt Arsenal, rien n'en ayant été copié ; **dans le runtime**, uniquement des commandes de lecture de l'API websocket.

L'énumération des segments est signalée explicitement pour lever toute ambiguïté : **c'est une commande de lecture, pas une action**. Son implémentation retourne le contenu déjà présent en mémoire dans l'intégration, **sans aucune entrée-sortie vers l'appareil** — ce qui a été vérifié dans le code source **avant** de l'appeler. Le service `roborock.get_maps`, qui est une **action**, n'a **pas** été appelé.

**Cycle observé mais non provoqué.** Le cycle du 2026-08-26 lancé par l'opérateur depuis l'application Roborock, dont les réglages ont été déclarés par lui (§6.3), a été observé pendant ces passes. Il n'a été ni provoqué, ni modifié, ni interrompu par l'audit. *(Le cycle arrêté manuellement, lui, relève du lot terrain et figure au §10.2 — il avait été commandé par l'audit.)*

### 10.2 Lot terrain du 2026-08-26 (§9) — inventaire des appels

Chaque appel est listé, avec son **niveau de certitude de réception** par Home Assistant. Aucun total agrégé n'est avancé au-delà de ce que la trace établit.

| Horodatage UTC | Appel | Nature | Réception par Home Assistant |
|---|---|---|---|
| 13:09:29 | `select.select_option` · `carte_selectionnee` → `RDC` | réglage | **certaine** — bascule d'état constatée, puis confirmée au niveau protocolaire |
| 13:11:39 | `select.select_option` · `intensite_de_frottement` → `off` | réglage | **certaine** — bascule d'état constatée |
| 13:15:40 | `vacuum.send_command` · `app_segment_clean` · `[{"segments":[21]}]` | **commande de nettoyage** | **INDÉTERMINÉE** — exception opaque côté client ; aucun effet observé sur le robot, journal serveur vide. Voir §9.1.1 |
| 13:22:47 | `vacuum.send_command` · `app_segment_clean` · `[{"segments":[21]}]` | **commande de nettoyage** | **certaine** — mission démarrée, puis arrêtée manuellement vers 13:24 ; `cleanTime = 5 s` |
| *(≈ 14:08)* | `select.select_option` · `intensite_de_frottement` → `off` | réglage | **non émis — certain** : l'onglet du client a été détruit avant l'exécution, et l'état est resté inchangé depuis 13:22:55 |
| 14:09:17 | `select.select_option` · `intensite_de_frottement` → `off` | réglage | **certaine** |
| 14:10:08 | `vacuum.send_command` · `app_segment_clean` · `[{"segments":[21]}]` | **commande de nettoyage** | **certaine** — **T1 complet, validé** |
| 14:21:26 | `select.select_option` · `intensite_de_frottement` → `off` | réglage | **certaine** |
| 14:22:14 | `vacuum.send_command` · `app_segment_clean` · `[{"segments":[21],"repeat":2}]` | **commande de nettoyage** | **certaine** — **T2 complet, validé** |

**Décompte, tel que la trace le permet :**

| Catégorie | Nombre |
|---|---|
| Écritures de réglage parvenues à Home Assistant | **4** — chacune confirmée par bascule d'état |
| Commandes de nettoyage parvenues à Home Assistant | **3** — chacune confirmée par contexte retourné |
| Tentative de commande de nettoyage à **réception indéterminée** | **1** — celle de 13:15:40 |
| Tentative de réglage **certainement non émise** | **1** — onglet client détruit avant l'appel |

**Aucun total unique n'est donné.** Le nombre d'appels ayant atteint Home Assistant est de **sept** ; y ajouter la tentative de 13:15:40 supposerait de trancher une réception qui n'est pas établie. Une passe antérieure de ce document avançait « quatre écritures » : ce chiffre était **faux** et est corrigé ici.

**Ce qui n'est pas une action de cette session :**

- l'**arrêt manuel** du cycle de 13:22:47, effectué par un tiers présent sur place ;
- les **cycles lancés par l'opérateur** depuis l'application Roborock (§10.1) ;
- les **trois réactivations d'entités**, réalisées par l'opérateur (§3.4) ;
- le **renommage des segments** dans l'application Roborock (§5.4).

**Autorisations.** Chaque écriture a été précédée d'un `GO` opérateur explicite, et les commandes de nettoyage d'un `GO` distinct de celui des réglages.

| Contrôle | Résultat |
|---|---|
| Secondes tentatives d'un essai déjà abouti | **aucune** |
| Actions correctives après anomalie | **aucune** |
| `vacuum.start`, `clean_area`, voie zonée employés | **aucun** — interdits maintenus |
| Segments autres que `21` commandés | **aucun** |
| Essais multi-cartes | **aucun** |
| Contrat, chantier, YAML runtime, helper, script, automation, dashboard créé | **aucun** |
| Mappage area ↔ segment créé ou modifié | **aucun** |
| Entité activée ou désactivée par l'audit | **aucune** |

**État du robot à la clôture** : amarré, en charge, sans session ouverte, sans erreur. Carte `RDC` active. Profil rétabli par l'appareil à `medium` / `vac_and_mop` en fin de mission (§6.1).

---

## 11. Ce que ce document n'est pas

- Ce n'est **pas un contrat** : rien ici n'est normatif ni opposable. **IMC-1** (§8.2) n'échappe pas à cette règle : c'est une **contrainte de sécurité candidate** issue de l'audit, **à reprendre et arbitrer dans le futur contrat** du domaine — ni clause opposable, ni checker. Seul le **fait technique** qu'elle consigne est établi.
- Aucun chantier n'est ouvert.
- Aucune architecture n'est décidée : autorité de décision, writer unique, couche de diagnostic et rôle de l'UI restent **à concevoir et à valider** avant toute proposition de code.
- Aucun code, aucun YAML runtime n'est proposé.
