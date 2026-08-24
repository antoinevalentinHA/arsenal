# ARSENAL — Contrat de résilience des intégrations

**Composant :** `arsenal-ha`
**Version :** v2.7
**Scope :** Détection et relance automatique des intégrations critiques (gel des données, indisponibilité des entités, échec de configuration d'une entrée).
**Maille de couverture :** l'**entrée de configuration** (*config entry*) — voir §12.
**Mode d'application :** report-only — voir §10 et le registre.
**Dépendances :**
- `script.resilience_integration_recover` (action canon)
- `binary_sensor.panne_secteur_en_cours` (inhibition secteur)
- `binary_sensor.contexte_wan_indisponible` (inhibition WAN des intégrations cloud — voir §11)
- Contrat `pannes/internet/30` — contexte de remédiation réseau
- Contrat Notifications
- Doctrine [`gestion_du_temps.md`](../architecture/03_doctrines/gestion_du_temps.md) — réveil périodique de la couche observation (§13.3)
- Doctrine [`solvabilite_probatoire.md`](../architecture/03_doctrines/solvabilite_probatoire.md) — qualification des preuves et des réserves (§13.3, §14.1)
- Registre : `scripts/arsenal_contracts/resilience_integrations_registre.yaml`

---

## 1. Principe fondamental

> Une intégration peut défaillir de trois manières orthogonales :
> ses données peuvent **vieillir** (fraîcheur), ses entités peuvent **disparaître** (disponibilité),
> ou l'une de ses **entrées de configuration** peut ne plus se charger (échec de configuration).
> Un détecteur de fraîcheur ne détecte pas une disparition.
> Ni l'un ni l'autre ne détecte une entrée qui échoue pendant qu'une entrée voisine reste saine.
> **Un âge figé bas ne vaut jamais preuve de santé. Un périmètre peuplé non plus.**

Les trois axes doivent exister **séparément**. Aucun ne peut servir de substitut à un autre.

---

## 2. Définitions opposables

| Terme | Définition |
|---|---|
| **Entrée de configuration** | Unité de chargement de Home Assistant (*config entry*), identifiée par son `entry_id`. C'est elle qui est chargée, qui échoue et qui se recharge. Un domaine d'intégration peut en porter **plusieurs, indépendantes**. **C'est la maille de couverture du présent contrat** (§12). |
| **Domaine d'intégration** | Nom technique de l'intégration (`homekit_controller`, `switchbot`, `ping`…). **N'est pas une unité de défaillance** : il regroupe des entrées qui défaillent séparément. |
| **Fraîcheur** | Âge des données, dérivé du `last_reported` le plus récent des membres exploitables du groupe source, plafonné. Mesure la *liveness* (l'intégration rapporte-t-elle encore ?), pas la stabilité de la valeur. `last_reported` se rafraîchit à chaque écriture du coordinateur même valeur identique ; `last_updated`/`last_changed` ne bougent qu'au changement de valeur et feraient passer une intégration saine mais « calme » pour gelée. |
| **Disponibilité** | Présence d'au moins un membre exploitable du groupe source. L'**indisponibilité franche** = « 0 membre exploitable » maintenu sur une temporisation. Mesure la disparition. |
| **Échec de configuration** | État de l'**entrée** elle-même : elle n'est pas chargée et ne se charge pas. Porte sur l'entrée, jamais sur ses entités (§13). |
| **Recovery** | Procédure de relance déléguée au script canon `resilience_integration_recover` (attempt / reset / block), bornée par backoff et plafond, inhibée en panne secteur. |
| **Épisode de recovery** | Séquence ouverte à la première tentative et fermée par un **retour constaté**. Un épisode reste ouvert tant que le backoff tourne **ou** que le compteur de tentatives est non nul. **N'est pas** synonyme de « backoff actif » : l'expiration du backoff est un événement *interne* à l'épisode (§4.1). |
| **Chaîne complète** | Entrée possédant tous les maillons des couches diagnostic, décision, action, UI (§4), câblant **les trois** axes applicables à son mode. |
| **Chaîne orpheline** | Infrastructure de diagnostic et/ou d'action présente, mais **aucune automation de décision** ne la consomme. L'incident est diagnostiqué, jamais traité. **Non conforme.** |
| **Chaîne aveugle** | Automation de décision présente mais ne déclenchant que sur **un seul** axe (typiquement la fraîcheur), ignorant les autres axes applicables. **Non conforme.** |
| **Chaîne mal ancrée** | Chaîne dont le périmètre de détection contient des entités **n'appartenant pas** à l'entrée que son action répare. Elle observe ce qu'elle ne répare pas et répare ce qu'elle n'observe pas. **Non conforme** — et plus dangereuse que les deux précédentes, car elle produit un signal vert (§12.3). |
| **Entrée non couverte** | Entrée de configuration existante qu'aucune chaîne ne déclare ni n'observe. **Écart**, jamais un silence légitime (§12.2). |
| **Exception documentée** | Intégration dérogeant légitimement au canon d'âge, inscrite au registre avec motif (ex. disponibilité native + action propre). |

---

## 3. Les trois axes — règle de non-substitution

- L'axe **fraîcheur** repose sur un capteur d'âge et un binaire de gel avéré (seuil numérique, débouncé).
- L'axe **disponibilité** repose sur un comptage de membres exploitables du groupe source et un binaire d'indisponibilité franche (débouncé).
- L'axe **échec de configuration** repose sur l'état de l'entrée de configuration et un binaire d'échec avéré (débouncé) — voir §13.
- **Interdit :** utiliser l'âge comme preuve de disponibilité. Lorsque tous les membres deviennent indisponibles, l'âge peut se figer sur une dernière valeur basse ; le binaire de gel reste alors `off` et ne déclenche aucune relance. Cet état est couvert par l'axe disponibilité.
- **Interdit :** utiliser la fraîcheur ou la disponibilité comme preuve de chargement. Lorsqu'une entrée d'un domaine multi-entrées échoue, le périmètre agrégé du domaine reste frais et peuplé par les entrées saines ; les deux premiers binaires restent `off`. Cet état n'est couvert que par l'axe échec de configuration.

> Les deux règles ci-dessus ont la même forme : **un axe qui reste `off` n'est une preuve de santé que pour ce qu'il observe.**

### 3.1 Condition d'applicabilité de l'axe fraîcheur

L'axe fraîcheur repose sur une hypothèse qui n'est **pas universelle** : que le
coordinateur de l'intégration **écrive périodiquement**, même à valeur inchangée.
C'est le cas des intégrations en *polling*. Ce n'est **pas** le cas des entités
en *push* pur, qui ne rapportent qu'au changement d'état : `last_reported` y
reste figé tant que rien ne bouge, et l'âge croît linéairement **sur un
périmètre parfaitement sain**.

> **R-AXE1-1 (opposable).** Avant de câbler l'axe fraîcheur sur un périmètre,
> il faut avoir **constaté** que ses entités rapportent périodiquement hors
> changement d'état. À défaut, l'axe est **inapplicable** : il doit être déclaré
> `non_applicable` au registre, **jamais** simplement doté d'un seuil plus élevé.
>
> Relever le seuil ne corrige rien : l'âge d'une entité en push n'est pas borné.
> Un seuil, quel qu'il soit, finit par être franchi. Le défaut n'est pas un
> mauvais réglage, c'est une **absence de grandeur mesurable**.

> **R-AXE1-2.** Une entrée dont l'axe fraîcheur est inapplicable n'est pas pour
> autant sous-couverte : les axes disponibilité et échec de configuration
> suffisent à constituer une chaîne complète. Le mode déclaré au registre doit
> alors énoncer exactement les axes câblés.

> **R-AXE1-3 (câblage).** L'inapplicabilité se déclare au script canon par le
> paramètre **`axe_fraicheur: false`**, qui retire le terme d'âge de la condition
> d'incident **et** de la condition de succès. Le script exige alors au moins un
> axe de substitution (`unavail_entity` ou `fail_entity`) : sans lui, la condition
> de succès serait vide et le script conclurait au retour sans rien constater.
> Neutraliser l'axe par un seuil sentinelle est **interdit** — c'est un
> contournement, pas une déclaration.

---

## 4. Anatomie d'une chaîne complète

**Diagnostic** — groupe source **restreint à une entrée** (§12.3) ; capteur d'âge ; binaire gel avéré ; binaire indisponibilité franche ; binaire échec de configuration ; binaire retour OK ; binaire recovery en cours.
**Décision** — automation déclenchant sur gel **et** indisponibilité **et** échec de configuration **et** fin de backoff **et** retour OK, sous garde `input_boolean.systeme_stable = on`, en `mode: single`, sans `time_pattern`.
**Action** — délégation à `script.resilience_integration_recover` ; timer de backoff dédié ; compteur de tentatives dédié ; `entry_id` désignant l'entrée effectivement observée.
**UI** — exposition non trompeuse de l'état des axes et du recovery, à la maille de l'entrée (§12.6).

### 4.1 Cycle de vie d'un épisode de recovery

Un épisode s'ouvre à la première tentative et ne se ferme que d'une seule
façon : un **retour constaté**. Entre les deux, le backoff démarre et expire
autant de fois qu'il y a de tentatives — ces expirations sont **internes** à
l'épisode, elles ne le referment pas.

> **R-RECOV-1 (opposable).** Le binaire « recovery en cours » décrit
> l'**ouverture d'un épisode**, jamais l'état d'un timer. Le définir sur le seul
> backoff actif en fait une **dent de scie** : le binaire retombe à chaque
> expiration, alors que l'épisode, lui, continue.
>
> Conséquence observée (§15) : le retour OK, débouncé, peut voir sa
> temporisation **coupée par une expiration de backoff**. Le retour n'est alors
> jamais prononcé, le compteur jamais remis à zéro, et l'épisode reste
> ouvert indéfiniment.

> **R-RECOV-2 (opposable).** Un **retour constaté referme l'épisode et réarme la
> chaîne**, y compris après un blocage au plafond. Un blocage n'est pas un état
> terminal : il borne les *relances*, il ne condamne pas l'intégration. Une
> intégration qui revient d'elle-même doit pouvoir bénéficier d'un budget de
> tentatives neuf au prochain incident.
>
> Le réarmement **DOIT** être notifié : le blocage l'ayant été (invariant 9), sa
> levée est une information de même nature.

> **R-RECOV-3.** La fermeture d'un épisode ayant comporté au moins une tentative
> infructueuse **DOIT** être notifiée. Un épisode ouvert par une notification
> d'échec ne peut pas se refermer en silence — c'est l'exigence de l'invariant 9
> sur le « retour OK », qui doit être effectivement câblée et non seulement
> déclarée.

---

## 5. Invariants obligatoires

1. **Fraîcheur** — capteur d'âge dérivé de `last_reported` (liveness), plafonné. Usage de `last_updated`/`last_changed` proscrit ici : ils mesurent la stabilité de valeur, pas la liveness, et génèrent de faux gels sur intégration saine mais calme. **Cet axe présuppose une écriture périodique du coordinateur** — voir la condition d'applicabilité en §3.1, qui est une condition d'existence de l'axe, pas un réglage.
2. **Disponibilité** — binaire d'indisponibilité distinct de l'âge, fondé sur comptage de membres exploitables (« 0 membre exploitable » maintenu = indisponibilité confirmée).
3. **Non-substitution** — l'âge ne prouve pas la disponibilité ; ni l'un ni l'autre ne prouve le chargement de l'entrée (§3).
4. **Recovery** — convergence vers le script canon unique, jamais une seconde chaîne d'action.
5. **Retour OK** — détecté explicitement, conditionné à un **épisode de recovery ouvert** (§4.1, R-RECOV-1) — et non au seul backoff actif —, débouncé, et **notifié** (R-RECOV-3).
6. **Backoff** — borné par un cap.
7. **Plafond tentatives** — au-delà du plafond, passage en `block` et arrêt des relances. Le blocage borne les relances **sans être terminal** : un retour constaté referme l'épisode, réarme la chaîne et le notifie (R-RECOV-2).
8. **Inhibition panne secteur** — aucune tentative pendant `panne_secteur_en_cours = on` ; le reset reste autorisé.
9. **Observabilité** — état des axes, compteur, backoff exposables ; notifications sur attempt/échec/block/retour OK.
10. **Absence de boucle agressive** — `mode: single`, `max_exceeded: silent`, déclenchement sur transition, garde `systeme_stable`. **En couche décision uniquement** : le réveil périodique de la couche observation autorisé par R-AXE3-5 ne déroge pas à cet invariant (§13.3).
11. **Support WAN disponible** — une intégration de classe `cloud_wan` ne tente aucun recovery (`op == attempt`) tant que le contexte WAN est indisponible (`binary_sensor.contexte_wan_indisponible = on`). Cette inhibition ne concerne **que** les intégrations `cloud_wan` ; les intégrations `local_lan` n'y sont jamais soumises. Comme pour l'inhibition panne secteur (invariant 8), seul `attempt` est inhibé ; `reset` et `block` restent autorisés.
12. **Maille entrée de configuration** — la couverture se déclare, se câble et se vérifie **par entrée**, jamais par domaine ni par nom commercial (§12).
13. **Ancrage détection ↔ action** — le périmètre observé appartient à l'entrée que l'action répare (§12.3).
14. **Axe échec de configuration** — troisième axe, observé sur l'état de l'entrée, débouncé, soumis aux gardes communes (§13).
15. **Honnêteté de l'indicateur** — aucun indicateur ne peut afficher sain un domaine dont une entrée est en échec ou non couverte (§12.6).

---

## 6. Interdictions absolues

- Relance non bornée (sans backoff ni plafond).
- Reload pendant une panne secteur active.
- Déclenchement sur un seul axe quand plusieurs sont requis (chaîne aveugle).
- Infrastructure de diagnostic sans automation consommatrice (chaîne orpheline).
- Appel direct à `homeassistant.reload_config_entry` ou `hassio.addon_restart` **hors** du script canon, **sauf exception inscrite au registre** (§7).
- Tenter un recovery d'une intégration `cloud_wan` pendant un contexte WAN indisponible ou un contexte de remédiation réseau actif (cf. `pannes/internet/30`).
- Coder `binary_sensor.contexte_wan_indisponible` en dur dans une garde globale du script canon : la garde WAN est **paramétrée** (`wan_entity`), pour qu'une intégration `local_lan` ne puisse jamais être inhibée par effet de bord.
- Inhiber une intégration `local_lan` (Airstage, HomeKit, SwitchBot, Synology, Zigbee2MQTT) sur un signal WAN.
- **Déclarer une couverture au nom d'un domaine** lorsque celui-ci porte plusieurs entrées : c'est une couverture partielle silencieuse (§12.2).
- **Ancrer la détection** d'une chaîne sur des entités n'appartenant pas à l'entrée que son action recharge (§12.3).
- **Substituer** l'axe fraîcheur ou l'axe disponibilité à l'axe échec de configuration (§3).
- **Traiter comme un incident** une entrée volontairement désactivée (`disabled_by` renseigné) (§13.2).
- **Déclencher un recovery sur `setup_retry` sans débounce**, en concurrence avec le réessai natif de Home Assistant (§13.2).
- **Exposer un indicateur de santé agrégé** calculé sur un sous-ensemble des entrées d'un domaine (§12.5).
- **Énumérer les entrées par balayage runtime** des entités : l'énumération est déclarative, elle vient du registre (§13.3).

---

## 7. Exceptions documentées

Une intégration peut déroger au canon d'âge si elle dispose d'un signal de disponibilité natif et d'une action propre, **à condition d'être inscrite au registre** avec son motif. L'exception ne dispense pas des invariants 6 à 10, ni des invariants 12, 13 et 15.

**Zigbee2MQTT** est une exception documentée légitime : disponibilité native via `binary_sensor.zigbee2mqtt_bridge_connection_state`, action `hassio.addon_restart`, backoff et garde anti-boucle maintenus. Le canon d'âge ne s'applique pas. Cette intégration ne doit pas être normalisée dans le canon d'âge.

---

## 8. Chaînes orphelines à arbitrer

**Audi** et **Withings** disposent d'une infrastructure partielle (groupe, capteur d'âge, binaires gel/retour OK/recovery, timer de backoff) mais **sans automation de décision ni compteur de tentatives**. Ce sont des chaînes orphelines, **non conformes**, inscrites au registre comme dettes temporaires à arbitrer. Aucun runtime n'est ajouté pour ces intégrations tant qu'un ID d'automatisation n'est pas fourni : compléter ou décommissionner relève d'un arbitrage ultérieur.

---

## 9. Séparation des couches (mapping dépôt)

| Couche | Emplacement |
|---|---|
| Diagnostic | `02_groups/integrations/`, `12_template_sensors/system/integrations/` |
| Décision | `11_automations/system/reload_integrations/` |
| Action | `10_scripts/system/resilience_integration_recover.yaml` |
| UI | `18_lovelace/` |

---

## 10. Conformité CI et statut d'application

La conformité est vérifiée par `scripts/arsenal_contracts/check_resilience_integrations_contracts.py`, dont la source d'autorité est le registre `resilience_integrations_registre.yaml`. Le checker raisonne par registre, **jamais** par nom de fichier (rappel : `fujitsu.yaml` porte l'intégration Airstage).

Le registre type chaque maillon par un statut fermé : `present`, `absent_non_conforme_temporaire` (dette tolérée en report-only via les exceptions du registre), ou `non_applicable` (hors périmètre pour le mode de l'intégration, jamais une dette). Une dérogation légitime n'est pas un statut de maillon mais un bloc `exception_documentee` au niveau de l'intégration. Le checker lit ces statuts tels quels, sans inférence.

Le contrat s'applique en **mode report-only** : les écarts connus inscrits au registre n'échouent pas la CI ; tout écart **nouveau ou non documenté** échoue dès `STRICT_ON_NEW=1`.  La résorption d'une dette se traduit par la suppression de sa ligne d'exception au registre.

### 10.1 Dette de migration vers la maille « entrée » (v2.0)

Le registre et le checker **implémentent encore la maille v1.1** : une ligne par intégration, désignée par un nom commercial. Ils ne connaissent ni les `entry_id`, ni la règle d'ancrage (R-ANCRAGE-1), ni l'axe échec de configuration.

> **Dette déclarée, ouverte à la date de gel du présent contrat.** Elle porte sur trois points :
> 1. le registre énumère les **entrées** (couple domaine + `entry_id`), non les intégrations ;
> 2. le checker vérifie l'**ancrage** — les membres du groupe source appartiennent-ils tous à l'entrée que l'action recharge (§12.4) ;
> 3. le checker vérifie l'existence du **maillon axe 3** pour les entrées qui le requièrent.

**Résorption (v2.5).** Les trois points sont traités, dans les limites de ce qu'une analyse statique peut établir :
1. le registre énumère les **entrées** — chaque chaîne déclare `maille`, `domaine_integration`, `entree_libelle` et `entry_ref` (référence de la clé `secrets.yaml`, l'identifiant lui-même n'étant jamais publié). Un domaine portant plusieurs chaînes est désormais **lisible en direct** ;
2. l'**ancrage** est contrôlé par R-ANCRAGE-3 (§12.4) — volet statique en CI (R15), volet runtime par capteur dédié. La CI ne peut pas porter le volet runtime, et le contrat le dit plutôt que de le laisser croire ;
3. le maillon **axe 3** est vérifié depuis la v2.2 (R7 multi-axes).

S'ajoute **R16** : champs de maille obligatoires, et interdiction de mutualiser un groupe source, un timer de backoff ou un compteur entre deux chaînes.

**Ce qui reste hors de portée d'un contrôle**, et doit être dit : ni la CI ni le capteur runtime ne détectent une entrée **qui n'est déclarée nulle part**. Énumérer les entrées réellement présentes suppose de parcourir le registre de configuration de Home Assistant ; le contrôle actuel vérifie la cohérence de ce qui est déclaré, pas l'exhaustivité de la déclaration.

**Qualification historique** (au sens de [`solvabilite_probatoire.md`](../architecture/03_doctrines/solvabilite_probatoire.md) §3) : **réserve différée solvable**, **non bloquante**. Les points 2 et 3 ci-dessus sont **partiellement traités** : le checker modélise désormais l'axe 3 (règle R7 généralisée en « câblage multi-axes », qui exige le trigger et la transmission au canon de **chaque axe déclaré présent**), et il traite `non_applicable` comme ce que le registre dit qu'il est — hors périmètre, jamais un maillon manquant. Reste ouvert : l'énumération des entrées par `entry_id` et la vérification de l'**ancrage** (point 1).

**Qualification** (au sens de [`solvabilite_probatoire.md`](../architecture/03_doctrines/solvabilite_probatoire.md) §3) : **réserve différée solvable**, **non bloquante**. La preuve nécessaire est productible — `config_entry_id()` et `config_entry_attr()` sont disponibles et vérifiés (§13.3).
**Propriétaire :** chantier de mise en conformité du registre de résilience.
**Critère de levée :** registre migré à la maille entrée et checker portant les règles 1 à 3 ci-dessus.
**Réévaluation :** à la première mise en conformité runtime d'une chaîne consommant le présent contrat.

Tant que cette dette n'est pas résorbée, **la CI ne peut pas constater une entrée non couverte**. L'absence d'écart signalé par le checker ne vaut donc pas preuve de couverture — c'est précisément le défaut que la leçon terrain du §15 a rendu visible.

---

## 11. Garde réseau WAN (intégrations cloud)

### 11.1 Principe

Une intégration dont le support transite par Internet (**`cloud_wan`**) devient légitimement `unavailable` pendant une panne WAN ou une campagne de remédiation réseau. Dans ce cas, son indisponibilité est un **KO attendu**, pas un dysfonctionnement d'intégration : un recovery (reload de config entry) serait **futile** — le support distant est inatteignable — et consommerait tentatives, backoff et notifications jusqu'au blocage.

Par symétrie stricte avec l'inhibition panne secteur (invariant 8), le recovery des intégrations `cloud_wan` est inhibé tant que le support WAN n'est pas disponible et stabilisé.

### 11.2 Conformité à `pannes/internet/30`

Le contrat `pannes/internet/30` (Contexte de remédiation réseau) impose à tout composant **réseau-dépendant** de bloquer toute action corrective fondée sur une observation réseau pendant un contexte de remédiation actif. L'axe disponibilité des intégrations `cloud_wan` est un tel composant.

**Déclaration explicite (exigée par `pannes/internet/30`) :** pendant un contexte de remédiation réseau, une indisponibilité WAN, ou un retour WAN non encore stabilisé, les recoveries des intégrations `cloud_wan` sont **inhibés**. Les diagnostics (axes fraîcheur/disponibilité/échec de configuration) continuent d'observer ; seule l'action de recovery est suspendue.

### 11.3 Signal canon

Le contexte WAN est porté par un binaire diagnostic unique :

> **`binary_sensor.contexte_wan_indisponible`** (`unique_id: contexte_wan_indisponible`)

Il est `on` si une campagne de remédiation réseau est active (`input_boolean.reboot_box_en_cours = on`) **ou** si l'accès externe n'est pas disponible (`binary_sensor.acces_externe != on`, donc `off`/`unknown`/`unavailable`). Il ne repasse `off` qu'après stabilisation du retour WAN (cf. son `delay_off`). Ce binaire décrit un **état système WAN** ; il ne lit ni ne modifie `binary_sensor.panne_secteur_en_cours`, et n'évoque aucune action de recovery. La garde secteur (invariant 8) et la garde WAN sont **complémentaires et indépendantes**.

### 11.4 Contrat de câblage

| Élément | Rôle |
|---|---|
| `meta.inhibition_wan` (registre) | nom canonique du signal WAN : `binary_sensor.contexte_wan_indisponible`. Déclaré **une seule fois**. |
| `classe_reseau` (registre, par entrée) | `cloud_wan` ou `local_lan`. **Seule clé de vérité** ; aucune clé `garde_wan` concurrente. |
| `wan_entity` (paramètre du script canon) | optionnel. Transmis par l'appel `op: attempt` d'une intégration `cloud_wan`, jamais par une `local_lan`. |

**Règles de câblage :**

- Pour une intégration **`cloud_wan`** avec automation active, l'appel `op: attempt` à `script.resilience_integration_recover` transmet `wan_entity: binary_sensor.contexte_wan_indisponible`.
- Pour une intégration **`local_lan`**, l'appel `op: attempt` ne transmet **jamais** `wan_entity`.
- Dans le script canon, la garde WAN est **optionnelle et paramétrée** : elle ne s'arme que si `wan_entity` est défini, inhibe uniquement `op == attempt`, bloque si l'entité transmise est `on`, et ne bloque jamais `reset` ni `block`. Elle ne code jamais le binaire en dur.

**Classification :**

| Classe | Intégrations |
|---|---|
| `cloud_wan` | Netatmo, Overkiz, Audi, Withings |
| `local_lan` | Airstage / Fujitsu, HomeKit, SwitchBot, Synology, Zigbee2MQTT |

Câblage runtime immédiat : Netatmo et Overkiz (cloud actives). Audi et Withings sont `cloud_wan` mais orphelines (§8) — leur classe est enregistrée pour le jour de leur câblage, sans appel à garder aujourd'hui.

### 11.5 Réserve — gardes locales hors périmètre

Cet invariant couvre **exclusivement** le support WAN. Les intégrations `local_lan` ne sont **jamais** inhibées par une panne WAN : Airstage (équipement joignable sur le LAN via `binary_sensor.climatiseur`), HomeKit (pont local), SwitchBot (BLE via proxys ESP32), Synology (NAS LAN) et Zigbee2MQTT (bridge MQTT) conservent un recovery pleinement actif même Internet coupé.

Une éventuelle garde « support **local/LAN** disponible » — qui inhiberait le recovery d'une intégration locale pendant un KO LAN attendu — relèverait d'un **invariant distinct**, non traité ici. Elle utiliserait d'autres signaux (LAN, non WAN) et un autre périmètre d'intégrations. Sa mention ici vaut **réserve explicite**, pas ouverture de chantier.

---

## 12. La maille de couverture — l'entrée de configuration

### 12.1 Principe

Une intégration n'est pas une unité de défaillance. L'unité de défaillance est l'**entrée de configuration** : c'est elle qui est chargée, qui échoue, qui se recharge. Un domaine (`homekit_controller`, `ping`, `switchbot`…) peut en porter une ou plusieurs, **indépendantes entre elles**.

> **R-MAILLE-1 (opposable).** La couverture de résilience se déclare, se câble et se vérifie **par entrée de configuration**, jamais par domaine ni par nom commercial d'intégration.
> Le nom d'une intégration au registre est une **étiquette de lecture**, pas une identité. L'identité opposable est le couple **(domaine, `entry_id`)**.

### 12.2 Conséquences directes

- Une entrée existante qu'aucune chaîne ne déclare est une **entrée non couverte** — un **écart**, jamais un silence légitime.
- Un domaine à N entrées exige **N chaînes**, ou une chaîne explicitement déclarée multi-entrées dont le périmètre de détection couvre l'union des N entrées **et** dont l'action sait laquelle recharger.
- Un `entry_id` unique en paramètre d'action ne peut couvrir qu'une entrée. Le déclarer au nom d'un domaine multi-entrées constitue une **couverture partielle silencieuse** : la chaîne paraît complète au registre, elle ne couvre qu'une fraction du domaine.

> **R-MAILLE-2.** Le nombre d'entrées d'un domaine n'est pas une constante. L'ajout d'une entrée à un domaine déjà couvert crée mécaniquement une entrée non couverte. La couverture est donc **une propriété à revérifier**, pas un acquis.

### 12.3 Ancrage détection ↔ action

> **R-ANCRAGE-1 (opposable).** Le périmètre de détection d'une chaîne **DOIT** être composé exclusivement d'entités appartenant à l'entrée que son action répare.

Une chaîne dont le groupe source contient des entités d'une autre entrée est **mal ancrée** : elle observe un périmètre qu'elle ne répare pas, et répare un périmètre qu'elle n'observe pas. Deux défaillances en découlent, et elles sont symétriques :

- **faux négatif** — l'entrée réparée tombe, mais le périmètre observé (peuplé par une autre entrée) reste sain : aucune relance n'est déclenchée ;
- **remédiation mal ciblée** — le périmètre observé tombe, et la relance vise une entrée qui n'y est pour rien.

Une chaîne mal ancrée est **non conforme**, au même titre qu'une chaîne orpheline ou aveugle. Elle est **plus dangereuse que les deux** : une chaîne orpheline ne dit rien, une chaîne aveugle ne voit qu'un axe, mais une chaîne mal ancrée **produit un signal vert** sur un périmètre en panne.

> **R-ANCRAGE-2 (opposable).** Le périmètre de détection ne contient que des
> entités **produites directement par l'entrée**. Y placer une entité **dérivée**
> — template, consolidation, façade, valeur stabilisée — est **interdit**.
>
> Une entité dérivée porte sa **propre cadence de rafraîchissement** et sa
> **propre logique de disponibilité**, toutes deux découplées de l'intégration
> observée. Elle peut donc maintenir le périmètre « frais » et « peuplé » alors
> que l'intégration est morte — et neutraliser **les deux axes à la fois**.
>
> Le cas est aggravé si la dérivée est **inter-intégrations** : elle reste alors
> vivante grâce à une *autre* intégration, et le périmètre ne peut plus jamais
> se vider. Voir la leçon terrain du §15.
>
> Test de recevabilité : une entité est admissible au périmètre si et seulement
> si `config_entry_id()` retourne l'entrée observée. Toute entité sans entrée de
> configuration est **de facto** dérivée ou étrangère, donc irrecevable.

### 12.4 Vérifiabilité — deux moitiés, aucune ne remplace l'autre

L'ancrage est mécaniquement vérifiable, mais **pas au même endroit** selon ce qu'on vérifie.

> **R-ANCRAGE-3 (opposable).** Le contrôle d'ancrage se décompose en deux volets,
> et **aucun des deux ne suffit seul** :
>
> | Volet | Ce qu'il vérifie | Où |
> |---|---|---|
> | **Statique** | Aucun membre du périmètre n'est une entité **produite par les templates du dépôt** — donc dérivée par construction (R-ANCRAGE-2) | CI, règle **R15** |
> | **Runtime** | Les membres appartiennent tous à **une seule et même entrée** (R-ANCRAGE-1) | `binary_sensor.ancrage_chaines_resilience_non_conforme` |
>
> Le volet runtime **ne peut pas** être porté par la CI : l'appartenance d'une
> entité à une entrée n'existe que dans le registre d'entités de Home Assistant
> et se lit par `config_entry_id()`, une fonction de template. Aucune analyse
> statique du dépôt n'y a accès.
>
> Prétendre le contraire serait plus dangereux que l'absence de contrôle : une
> CI verte serait lue comme une preuve d'ancrage qu'elle n'a pas produite.

Le volet statique n'est pas un lot de consolation : c'est lui qui capte le cas le
plus dangereux — une entité dérivée qui, portant sa propre cadence et sa propre
disponibilité, **neutralise les deux axes** sans qu'aucun maillon soit manquant
(§15, quatrième enseignement).

### 12.5 Domaines dont les entrées sont des appareils

Certains domaines créent **une entrée par appareil** — le périmètre métier utile
couvre alors naturellement plusieurs entrées.

Cette configuration ne rend pas la maille caduque : chaque entrée charge et
échoue toujours indépendamment. Elle déplace la question sur l'**action** :

> **R-ANCRAGE-4.** Lorsqu'un périmètre couvre légitimement plusieurs entrées d'un
> même domaine, l'action de recovery **DOIT** couvrir **toutes** ces entrées, ou
> l'écart **DOIT** être inscrit au registre comme arbitrage ouvert, avec ce qu'il
> coûte. Recharger une entrée sur N en réponse à une panne qui les concerne
> toutes est une **remédiation partielle silencieuse** — la chaîne se déclare
> réparée alors qu'elle n'a traité qu'une fraction du périmètre.

**Moyen canonique de la satisfaire.** Le script canon accepte, en alternative
exclusive à `entry_id`, un paramètre **`reload_target`** : l'action **cible le
périmètre lui-même**, Home Assistant remonte aux entrées de chaque entité ciblée
et les recharge toutes.

> **R-ANCRAGE-5.** Quand l'action cible le périmètre, elle en **dérive** — elle ne
> peut donc plus en diverger. R-ANCRAGE-1 cesse d'être une règle qu'on vérifie
> pour devenir une propriété structurelle, **pour cette chaîne**.
>
> Corollaire de contrôle : un périmètre multi-entrées n'est pas fautif en soi. Il
> l'est lorsque l'action ne couvre qu'une entrée. Le contrôle runtime doit donc
> distinguer les deux familles — périmètres à action mono-entrée (multi-entrées
> interdit) et périmètres à action ciblée (multi-entrées légitime) — et non
> signaler indistinctement toute cardinalité supérieure à 1.
>
> **Déclarer un périmètre comme « à action ciblée » sans que son automation
> transmette réellement `reload_target` revient à faire taire un écart réel.**
> La déclaration de contrôle et le câblage de l'action doivent bouger ensemble.

*Comportement vérifié en terrain le 2026-08-24 : un appel ciblé sur un groupe de
24 entités réparties sur 6 entrées a rechargé les 6, constaté par le saut
simultané de leurs horodatages.*

> **R-ANCRAGE-6 (opposable — condition d'éligibilité au ciblage).** Une chaîne ne
> peut cibler son périmètre que si ce périmètre est **fermé sur son domaine
> d'intégration** : toutes les entrées qu'il résout appartiennent au domaine
> déclaré au registre.
>
> **Avec un ciblage, le groupe cesse d'être un ensemble de surveillance pour
> devenir une ACL d'action** : sa composition décide de ce qui sera rechargé.
> Une entité étrangère n'y dilue plus seulement un axe — elle **étend la
> réparation à une intégration tierce**.
>
> Symétriquement, retirer la dernière entité représentant une entrée **retire
> cette entrée de la réparation**, sans qu'aucun axe ne s'en aperçoive. Les deux
> dérives, élargissement et rétrécissement, sont des écarts.

**Leçon terrain — 2026-08-24, ciblage retiré après coup.** La première
application de R-ANCRAGE-5 a dû être annulée le jour même. `group.switchbot_capteurs`
n'était pas fermé sur son domaine : il résolvait des entrées de `switchbot`,
`switchbot_cloud` **et `mqtt`**. Un déclenchement de la chaîne aurait rechargé
l'entrée du broker MQTT, avec cascade vers la chaîne Zigbee2MQTT — perte des
entités MQTT, bascule du bridge, redémarrage de l'add-on.

Le défaut de composition **préexistait** ; il ne diluait qu'un axe. Le ciblage l'a
transformé en danger d'action. D'où R-ANCRAGE-6 : **la fermeture du périmètre est
une condition d'éligibilité au ciblage, pas une conséquence.**

### 12.6 Honnêteté de l'indicateur

> **R-UI-1 (opposable).** Un indicateur de santé **ne doit jamais** afficher sain un domaine dont une entrée est en échec ou non couverte.

Un indicateur calculé sur un sous-ensemble des entrées d'un domaine, mais **étiqueté au nom du domaine**, est trompeur : il transforme une couverture partielle en affirmation de santé globale. C'est l'inverse de ce qu'exige l'invariant 9.

Deux formes conformes, au choix :

- **un indicateur par entrée**, chacun étiqueté de manière à ne pas laisser croire qu'il couvre le domaine ;
- **un indicateur agrégé** dont l'état se dégrade dès qu'**une** entrée du domaine se dégrade ou n'est pas couverte.

> **R-UI-2.** Un indicateur vert calculé sur un périmètre incomplet est **pire qu'une absence d'indicateur** : l'absence appelle la vérification, le vert la décourage.

---

## 13. Troisième axe — l'échec de configuration

### 13.1 Pourquoi un axe distinct

Les axes fraîcheur et disponibilité observent tous deux les **entités** d'un périmètre. Ils sont structurellement aveugles à une entrée qui échoue pendant qu'une autre entrée du même domaine reste saine : le périmètre agrégé demeure frais et peuplé, les deux binaires restent `off`.

> **R-AXE3-1.** L'axe échec de configuration observe l'**état de l'entrée**, pas ses entités. Il ne se déduit ni de la fraîcheur ni de la disponibilité, et ne les remplace pas.

Cet axe est également le seul à voir une entrée qui n'a **jamais** réussi à se charger : elle n'a alors ni données à vieillir, ni entités à disparaître.

### 13.2 États d'entrée et qualification

| État de l'entrée | Qualification | Constitue un incident |
|---|---|---|
| `loaded` | nominal | non |
| `setup_retry` | échec **avec réessai natif** de Home Assistant | **seulement après persistance** (§13.4) |
| `setup_error` / `migration_error` | échec **terminal** — Home Assistant ne réessaie pas | oui |
| `not_loaded` | non chargée | **seulement si `disabled_by` est nul** |
| `setup_in_progress` / `failed_unload` | transitoire | non |

> **R-AXE3-2 (opposable).** `setup_retry` signifie que **Home Assistant réessaie déjà**, avec son propre backoff. Un recovery Arsenal déclenché sans délai entrerait en concurrence avec ce réessai natif — deux boucles de relance sur la même entrée, sans coordination. L'incident n'est constitué qu'après **persistance** de l'état. Le débounce est **obligatoire**, jamais facultatif.

> **R-AXE3-3.** Une entrée `not_loaded` dont `disabled_by` est renseigné est **désactivée par décision**, pas en panne. La traiter comme un incident est interdit : la remédiation lutterait contre une intention explicite.

### 13.3 Solvabilité probatoire et contrainte de réactivité

La preuve est l'état de l'entrée, lu par `config_entry_attr(entry_id, 'state')`.

**Productibilité vérifiée** sur l'installation le 2026-08-24 (§15) : la fonction restitue l'état et les attributs `title`, `domain`, `disabled_by`, `source`. Niveau **L1** au sens de [`solvabilite_probatoire.md`](../architecture/03_doctrines/solvabilite_probatoire.md) §1 — la preuve est produite par le runtime.

> **R-AXE3-4 (contrainte d'implémentation, opposable).** Cette fonction **n'est pas réactive** : elle n'émet aucun événement de changement d'état et ne provoque aucune réévaluation. Un capteur d'état d'entrée **DOIT** donc être un capteur à **déclencheurs explicites** — réveil périodique grossier **plus** `homeassistant: start`. Un template sans trigger est **interdit** ici : il n'aurait aucune garantie de réévaluation et figerait la valeur lue au démarrage, produisant exactement le faux vert que cet axe existe pour supprimer.

> **R-AXE3-5.** Ce réveil périodique appartient à la **couche observation**. Il ne déclenche aucune action : la couche décision continue de se déclencher sur la **transition d'état du binaire**, jamais sur le tick. L'invariant 10 (« pas de `time_pattern` en couche décision ») demeure donc **intact**.
> Cet usage est celui explicitement autorisé par [`gestion_du_temps.md`](../architecture/03_doctrines/gestion_du_temps.md) — rubrique « surveillance et résilience système », et règle « tick pour déclencher l'évaluation quand le seuil est atteint sans événement ». La fréquence doit rester **grossière** ; une cadence fine serait du polling déguisé.

> **R-AXE3-6.** Est **interdit** un capteur qui énumérerait les entrées par balayage de l'ensemble des entités du système : un tel capteur s'abonne à **tous** les changements d'état, ce qui est un coût permanent injustifiable pour une observation rare. **L'énumération des entrées à surveiller est déclarative** : elle vient du registre (§12.1), jamais d'un balayage runtime.

### 13.4 Débounce, gardes et bornes

- **Débounce sur `setup_retry`** — jamais inférieur au délai de gel de référence du registre. Il confirme que le réessai natif de Home Assistant ne converge pas.
- **Échec terminal** (`setup_error`, `migration_error`) — pas de débounce requis : Home Assistant ne réessaiera pas de lui-même.
- **Gardes communes inchangées** — `input_boolean.systeme_stable = on` (garde de démarrage), inhibition panne secteur (invariant 8), garde WAN pour les entrées `cloud_wan` (invariant 11).
- **Bornes inchangées** — backoff plafonné, plafond de tentatives, passage en `block` au-delà. Cet axe n'ouvre **aucun régime dérogatoire** : il alimente le script canon comme les deux autres.

---

## 14. Frontières de propriété — ce que ce contrat ne possède pas

### 14.1 Remédiation physique (power-cycle)

Ce contrat possède la remédiation **logicielle** : reload d'entrée de configuration, redémarrage d'add-on. Il ne possède **pas** la remédiation par l'alimentation.

Le précédent propriétaire dans le corpus est [`homekit_diagnostic.md`](homekit_diagnostic.md) §9.1 : la politique de power-cycle d'une station Netatmo y vit dans le **contrat de domaine**, bornée (tir unique), ciblée (une prise par station) et gardée. Ce positionnement est délibéré : une remédiation physique engage un équipement, une topologie d'alimentation et une commandabilité qui sont des faits de domaine, pas des faits d'intégration.

> **R-FRONTIERE-2.** Toute escalade vers un power-cycle relève d'un **contrat de domaine** qui la définit explicitement — cible, débounce, tir unique, gardes, plafond. Le présent contrat ne l'autorise ni ne l'interdit ; il déclare qu'elle **n'est pas de son ressort**.

**Réserve qualifiée** au sens de [`solvabilite_probatoire.md`](../architecture/03_doctrines/solvabilite_probatoire.md) §3 :

| Champ | Valeur |
|---|---|
| **Objet** | Escalade reload d'entrée → power-cycle, pour un pont matériel dont le reload seul ne suffit pas |
| **Qualification** | **Réserve différée solvable** — **non bloquante** |
| **Propriétaire** | Contrat de domaine du pont concerné |
| **Critère de levée** | Rédaction dudit contrat de domaine, **ou** preuve terrain qu'un reload d'entrée suffit seul |
| **Statut** | ✅ **LEVÉE le 2026-08-24** — critère rempli par la rédaction de [`pont_idiamant.md`](pont_idiamant.md) v1.0 |

**Levée (v2.1).** Le premier contrat de domaine consommant cette frontière est
[`pont_idiamant.md`](pont_idiamant.md) : il définit une escalade bornée à deux échelons
(reload, puis power-cycle unique au seuil de 2 tentatives), ses gardes, et son anti-boucle.
Il confirme R-FRONTIERE-2 par l'usage : la remédiation physique vit bien dans le contrat de
domaine, jamais ici.

La frontière du §14.1 reste **pleinement en vigueur** pour tout autre équipement : la levée
concerne le pont iDiamant, pas la règle. Tout nouveau besoin d'escalade physique exige son
propre contrat de domaine.

### 14.2 Ping et santé applicative

Le ping d'un hôte ne prouve que sa **joignabilité réseau**. Les propriétaires de ce sujet sont [`ping_lan_synthese.md`](ping_lan_synthese.md) pour la supervision réseau, et [`architecture/volets.md`](../architecture/volets.md) §7 pour le mode de défaillance « répond au ping tout en étant planté applicativement ».

Le présent contrat ne redéfinit ni l'un ni l'autre, et pose une seule règle à sa frontière :

> **R-FRONTIERE-3.** Un ping n'est **jamais** admis comme preuve de santé d'une entrée de configuration, ni comme substitut à l'un des trois axes.

---

## 15. Leçon terrain — 2026-08-23 / 2026-08-24

### Cas observé

Le domaine `homekit_controller` porte **trois** entrées de configuration : deux stations météo (`Weather Station`, chargées) et un pont de volets (`Prise Control`, passerelle Bubendorff). L'entrée du pont est passée en `setup_retry` le **2026-08-23 à 12:57 UTC** sur une erreur de connexion à l'accessoire. Les quatre `cover.*` qu'elle porte sont devenus `unavailable` et le sont restés **plus de 24 heures**.

Pendant tout cet épisode :

- le capteur d'âge du domaine indiquait **2 minutes** — il dérivait des capteurs des deux stations, saines ;
- les binaires de gel et d'indisponibilité franche étaient **`off`** — le périmètre observé était peuplé et frais ;
- l'automation de relance ne s'était **pas déclenchée** ; son dernier déclenchement remontait au 2026-05-06 ;
- l'indicateur « HomeKit » du dashboard système affichait **vert** ;
- le ping du pont répondait **`on`** ;
- aucune notification n'a été émise.

La remédiation efficace connue de l'opérateur était un **power-cycle de la prise du pont** — non exécuté volontairement, afin de constater le comportement autonome du système.

### Ce que le cas a rendu visible

La chaîne HomeKit était **conforme au contrat v1.1** et **verte en CI**. Elle était pourtant **mal ancrée** sur les trois entrées : son périmètre de détection mélangeait les capteurs de deux entrées, et son action ne pouvait recharger qu'une seule entrée sur trois. Le défaut n'était pas une non-conformité — c'était une **question que le contrat ne posait pas**.

### Conclusions verrouillées

```
1. une intégration n'est pas une unité de défaillance ; l'entrée de configuration l'est
2. un axe agrégé sur un périmètre multi-entrées masque l'entrée en panne au lieu de la révéler
3. un indicateur vert calculé sur un sous-ensemble est pire qu'une absence d'indicateur
4. l'échec de configuration est un mode de panne que ni la fraîcheur ni la disponibilité ne voient
5. la conformité à un contrat ne vaut couverture que dans les limites de ce que ce contrat interroge
```

La cinquième conclusion est la plus générale, et la raison d'être de la v2.0 : le contrat v1.1 était respecté à la lettre. Il ne demandait simplement jamais *combien d'entrées* portait une intégration.

### Suite — 2026-08-24, second enseignement

Après remise en service du pont, la cadence de report de ses `cover.*` a été
mesurée : **`last_reported` identique et figé pour les quatre volets pendant
22 minutes**, sur un périmètre pleinement sain. Ces entités sont en **push pur**.

Le seuil de gel de 45 minutes, aligné par mimétisme sur les autres intégrations
`local_lan`, aurait donc produit un **faux incident toutes les ~50 minutes**. Le
registre portait pourtant déjà la mention `a_confirmer_runtime` sur ce point
précis — la réserve était juste, elle n'a simplement pas été traitée comme
bloquante avant câblage.

D'où R-AXE1-1 (§3.1) : l'applicabilité de l'axe fraîcheur est une **condition
d'existence**, à constater avant câblage, et non un paramètre à ajuster après
coup.

### Troisième enseignement — la course entre retour OK et backoff

Le 2026-08-24, la reprise du pont est survenue à **11:26:30** ; le backoff
expirait à **11:27:57**. Le retour OK, débouncé sur 2 minutes, a vu sa
temporisation **coupée à environ 90 secondes** par la retombée du binaire
« recovery en cours », alors défini sur le seul timer.

Résultat : retour jamais prononcé, compteur resté à 1 sur un épisode pourtant
clos. Défaut **partagé par les sept chaînes**, invisible jusqu'à ce qu'une
escalade vienne consommer ce compteur.

Deux conséquences, corrigées en v2.3 :

1. « recovery en cours » décrit désormais un **épisode ouvert** (R-RECOV-1) ;
2. la fermeture d'un épisode est **notifiée** (R-RECOV-3), et un blocage au
   plafond cesse d'être terminal (R-RECOV-2) — auparavant, une chaîne bloquée le
   restait indéfiniment même si l'intégration revenait d'elle-même, puisque le
   retour OK ne pouvait plus jamais se déclencher.

Le second point n'avait été demandé par personne : il est apparu en corrigeant
le premier. Une chaîne bloquée à vie est un mode de défaillance silencieux que
le contrat n'avait jamais nommé.

### Quatrième enseignement — une dérivée dans un périmètre neutralise les deux axes

La scission des deux stations HomeKit (2026-08-24) a mis au jour, dans le groupe
source historique, **deux façades Arsenal** :
`sensor.temperature_petite_maison` et `sensor.humidite_relative_petite_maison`.

Ce ne sont pas des entités HomeKit. Ce sont des **consolidations
inter-intégrations** — source HomeKit `_1` **et** source SwitchBot `_2` —
adossées à un capteur stabilisé **à mémoire** (TTL 1800 s, 7200 s post-boot),
rafraîchi par un tick `/5`.

Effet mesuré :

- **axe fraîcheur, mort en permanence** : le tick `/5` rafraîchissait
  `last_reported` quoi qu'il arrive à HomeKit. L'âge du groupe, pris sur le
  membre le plus frais, ne pouvait jamais dépasser ~5 min — donc un seuil de gel
  à 45 min était **structurellement inatteignable** ;
- **axe disponibilité, aveuglé** : mémoire et source SwitchBot vivante
  maintenaient des membres exploitables jusqu'à **30 minutes** (2 h post-boot)
  après la mort réelle de la station.

La chaîne HomeKit était donc **aveugle avant même** le défaut de maille du §15 —
et l'était depuis l'ajout de ces façades au groupe. Aucun contrôle ne pouvait le
voir : le registre déclarait tous les maillons `present`, et ils l'étaient.

D'où **R-ANCRAGE-2** (§12.3) : la composition du périmètre est aussi normative
que son ancrage. Une chaîne peut être ancrée sur la bonne entrée **et** rendue
aveugle par un seul membre dérivé.

Mesure de contrôle après scission : âge réel de **3,8 min** et **3,9 min** pour
les deux stations, en variation continue — l'axe fraîcheur y est applicable, et
c'est désormais constaté (R-AXE1-1) et non supposé.

### Ce que ce cas n'établit pas

Cette leçon **ne désigne aucune remédiation** pour le pont concerné. Elle établit un défaut de **détection** et de **maille**, pas l'efficacité d'une action. Le choix entre reload d'entrée seul et escalade vers un power-cycle relève de la réserve du §14.1, et exige sa propre preuve.

---

## 16. Historique de version

- **v1.0** — Contrat initial. Deux axes orthogonaux (fraîcheur / disponibilité), script canon de recovery, registre CI, mode report-only.
- **v1.1** — Ajout de l'invariant 11 et du §11 : garde réseau WAN pour les intégrations `cloud_wan`, garde paramétrée (`wan_entity`) et jamais codée en dur, classification `cloud_wan` / `local_lan`. Conformité déclarée à `pannes/internet/30`.
- **v1.1 (révision)** — Définition de la fraîcheur fondée sur `last_reported` (liveness) ; invariant 1 reformulé ; usage de `last_updated`/`last_changed` proscrit sur cet axe.
- **v2.7** — Ajout de **R-ANCRAGE-6** (§12.5) : la **fermeture du périmètre sur son domaine** est une **condition d'éligibilité au ciblage**. Sous ciblage, le groupe devient une ACL d'action — une entité étrangère étend la réparation à une intégration tierce, et le retrait de la dernière entité d'une entrée l'en exclut silencieusement. Leçon terrain : la première application de R-ANCRAGE-5 (SwitchBot) a été **annulée le jour même**, le périmètre résolvant des entrées `switchbot`, `switchbot_cloud` et `mqtt`. Le contrôle runtime détecte désormais la non-fermeture de domaine.
- **v2.6** — Ajout de **R-ANCRAGE-5** (§12.5) : moyen canonique de satisfaire R-ANCRAGE-4 — le paramètre `reload_target` du script canon fait **cibler le périmètre** par l'action, qui en dérive et ne peut donc plus en diverger. Corollaire : un périmètre multi-entrées n'est fautif que si l'action ne couvre qu'une entrée ; le contrôle runtime distingue désormais les deux familles. Comportement vérifié en terrain. Première application : SwitchBot, dont l'arbitrage ouvert de la v2.5 est **résolu**.
- **v2.5** — **Contrôle d'ancrage effectif.** Ajout de **R-ANCRAGE-3** (§12.4) : le contrôle se décompose en un volet **statique** (CI, règle R15 — aucune entité dérivée dans un périmètre) et un volet **runtime** (capteur dédié — appartenance réelle à une entrée unique) ; aucun ne remplace l'autre, et la CI **ne peut pas** porter le second, `config_entry_id()` étant une fonction de template. Ajout de **R-ANCRAGE-4** (§12.5) : un périmètre couvrant légitimement plusieurs entrées exige une action couvrant **toutes** ces entrées, ou l'inscription de l'écart au registre — recharger une entrée sur N est une remédiation partielle silencieuse. Ajout de **R16** au checker (champs de maille obligatoires, mutualisation interdite). Registre migré à la maille entrée. Dette §10.1 résorbée, avec énoncé explicite de ce qui reste hors de portée d'un contrôle. Ancien §12.5 renuméroté §12.6.
- **v2.4** — Ajout de **R-ANCRAGE-2** (§12.3) : le périmètre de détection ne contient que des entités **produites directement par l'entrée** ; toute entité dérivée (template, consolidation, façade, valeur stabilisée) est interdite, car elle porte sa propre cadence et sa propre disponibilité et peut neutraliser les deux axes simultanément. Test de recevabilité par `config_entry_id()`. Quatrième enseignement terrain en §15 : deux façades inter-intégrations rendaient la chaîne HomeKit aveugle sur ses deux axes, sans qu'aucun maillon soit manquant.
- **v2.3** — **Cycle de vie de l'épisode de recovery** (§4.1, R-RECOV-1/2/3). « Recovery en cours » décrit l'ouverture d'un épisode et non l'état du backoff : la définition précédente, en dent de scie, pouvait couper la temporisation du retour OK et laisser un épisode ouvert indéfiniment. Un blocage au plafond cesse d'être terminal — un retour constaté referme l'épisode, réarme la chaîne et le notifie. La notification de « retour OK », exigée par l'invariant 9 mais jamais câblée, est ajoutée au script canon. Invariants 5 et 7 amendés. Ajout de R-AXE1-3 : l'inapplicabilité de l'axe fraîcheur se déclare par `axe_fraicheur: false`, jamais par un seuil sentinelle. Troisième enseignement terrain en §15.
- **v2.2** — Ajout de la **condition d'applicabilité de l'axe fraîcheur** (§3.1, R-AXE1-1/2) : cet axe présuppose une écriture périodique du coordinateur ; sur des entités en push pur, il est **inapplicable** et doit être déclaré `non_applicable`, jamais re-seuillé. Invariant 1 amendé en conséquence. Résorption partielle de la dette §10.1 : le checker modélise désormais l'axe 3 (R7 généralisée au multi-axes) et traite `non_applicable` conformément au vocabulaire du registre. Second enseignement terrain du 2026-08-24 consigné en §15.
- **v2.1** — Levée de la réserve §14.1 : le contrat de domaine attendu existe ([`pont_idiamant.md`](pont_idiamant.md) v1.0, 2026-08-24). R-FRONTIERE-2 est confirmée par l'usage — la remédiation physique vit dans le contrat de domaine. La frontière elle-même est inchangée et reste opposable pour tout autre équipement. Aucun invariant, aucun axe, aucune règle d'ancrage modifiés.
- **v2.0** — **Changement de maille.** La couverture se déclare et se vérifie par **entrée de configuration** et non plus par intégration (§12, invariant 12, R-MAILLE-1/2). Ajout de la règle d'**ancrage détection ↔ action** et de la notion de **chaîne mal ancrée** (§12.3, invariant 13, R-ANCRAGE-1). Ajout d'un **troisième axe — échec de configuration** (§13, invariant 14), avec qualification des états d'entrée, débounce obligatoire sur `setup_retry`, exclusion des entrées désactivées, et contrainte de réactivité (R-AXE3-4/5/6) articulée avec `gestion_du_temps.md` sans déroger à l'invariant 10. Ajout de l'invariant 15 et du §12.5 sur l'**honnêteté de l'indicateur** (R-UI-1/2). Ajout du §14, **frontières de propriété** : la remédiation physique reste au contrat de domaine (R-FRONTIERE-2, réserve qualifiée), le ping n'est jamais preuve de santé d'entrée (R-FRONTIERE-3). Ajout du §10.1, **dette de migration** du registre et du checker, qualifiée non bloquante. Ajout du §15, leçon terrain 2026-08-23. Les §1 à §11 conservent leur numérotation ; aucun invariant existant n'est supprimé ni affaibli.

---

*Arsenal — document contractuel · résilience des intégrations · maille entrée de configuration · v2.7*
