# Chantier TRANSVERSE (C34) — Comportement au redémarrage, au rechargement YAML et au rechargement d'intégration

| Champ | Valeur |
|---|---|
| **Chantier** | Auditer le comportement de Home Assistant et des périphériques pilotés lors d'un redémarrage complet, d'un rechargement YAML, d'un rechargement d'intégration, et pendant les phases transitoires de restauration, d'indisponibilité et de recalcul qui suivent ces opérations. |
| **Domaine** | Transverse — sept domaines pilotant des actions physiques. |
| **Statut** | **Ouvert (2026-07-21) ; enrichi le 2026-07-23 d'apports probatoires runtime L4** (climatisation, alarme — cf. §5.6). Le cadrage et l'inventaire restent la base. **Aucun verdict de qualification** au sens de la grille §2 (défaut « action physique indésirable » vs « recalcul fonctionnel » légitime) n'est émis : cette qualification relève de l'analyse statique des vagues. Les apports L4 **alimentent la cartographie** (critère ①) sans la clore. |
| **Priorité** | **P1** — le sujet porte sur des actions physiques (chauffe, froid, eau, ventilation, éclairage, armement d'alarme) potentiellement déclenchées par une opération purement technique. |
| **Ouvert le** | 2026-07-21. |
| **Prochain jalon** | **Vague 1 d'audit** (§7). Pas de conclusion générale avant. |
| **Registre** | Chantier **C34** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi.** |

> **Ce document n'établit aucun comportement.** Il définit le périmètre, recense les
> sources à lire et fixe la méthode. Toute affirmation sur le comportement réel du système
> relève des vagues d'audit à venir.

---

## 1. Objet

Déterminer ce que fait le système — et ce que font les équipements pilotés — lorsqu'une
opération **technique** est conduite sur Home Assistant, par opposition à une évolution de
l'**intention** utilisateur ou des **conditions** physiques.

Trois familles d'événements sont visées :

1. **redémarrage complet** de Home Assistant ;
2. **rechargement YAML**, global ou par domaine ;
3. **rechargement d'une intégration**.

S'y ajoutent les **phases transitoires** qui suivent : restauration des helpers, entités
`unknown` ou `unavailable`, recalcul des templates, réarmement des automatisations.

Le sujet n'a **pas de propriétaire documentaire unique préexistant** : deux doctrines en
couvrent chacune un volet (§4), aucune ne couvre l'ensemble. Ce chantier devient le
propriétaire du sujet consolidé.

---

## 2. Invariant recherché

> **Une opération technique ne doit pas provoquer, par elle-même, une activation, une
> coupure, une révocation, une impulsion, un rejeu ou un changement physique injustifié.**

Cet invariant est la **cible d'audit**, non un acquis.

**Le maintien aveugle de l'état antérieur n'est pas pour autant correct.** Certaines
situations imposent au contraire de ne pas restaurer : un verrou de sécurité, une
autorisation périmée, une observation devenue obsolète. L'audit doit donc distinguer sept
qualifications, sans les confondre :

| Qualification | Définition |
|---|---|
| **Continuité légitime** | l'état antérieur reste valide et doit être maintenu |
| **Abstention temporaire** | le système suspend toute action tant que l'observation n'est pas fiable |
| **Restauration** | un état est délibérément rétabli, conformément à un contrat |
| **Recalcul fonctionnel** | une décision est reprise sur données fraîches, et peut légitimement différer |
| **Révocation de sécurité** | un état antérieur est délibérément **non** restauré, par sûreté |
| **Action physique indésirable** | l'opération technique produit un effet matériel non justifié |
| **Anomalie de diagnostic ou d'UI** | l'écart est visible mais sans effet physique |

Les quatre premières peuvent être correctes. La cinquième est parfois **obligatoire**. Seule
la sixième est un défaut au sens de l'invariant. La septième relève d'un autre registre de
gravité.

---

## 3. Périmètre

**Sept domaines**, retenus parce qu'ils commandent des actions physiques :

climatisation · chauffage · VMC · déshumidificateur · arrosage automatique · alarme · éclairage.

**Trois familles d'événements** : reboot HA · reload YAML (global ou par domaine) ·
reload d'intégration.

**Hors périmètre à ce stade** : les domaines sans action physique directe, les mises à jour
de version HA, les coupures d'alimentation (couvertes par un contrat distinct, cf. §4).

---

## 4. Doctrines et contrats applicables

Chaque document est listé avec sa **portée réelle**. Aucun ne se voit attribuer une autorité
qu'il ne revendique pas.

| Document | Nature | Portée sur C34 |
|---|---|---|
| [`restauration_etat_helpers.md`](../../../architecture/03_doctrines/restauration_etat_helpers.md) | Doctrine système, **normative et opposable**, applicabilité globale (v1.1, 2026-07-01) | Couvre la **restauration des helpers YAML exposant une clé `initial`**. Le chantier de résorption y est déclaré **clos**, inventaire propre, CI active et bloquante. **Ne couvre pas** les automatisations, templates, ni le comportement des équipements. |
| [`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) | Architecture, principe **transversal et non négociable** | Fonde la distinction **décision / action** et vise explicitement les « actions déclenchées sur des états techniques instables ». **Ne décrit pas** le comportement au reboot ni aux reloads. |
| [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md) | Doctrine système, **normative et opposable** | Fournit l'échelle **L1–L5**, les trois verdicts et la qualification des réserves. Encadre **ce que l'audit pourra prouver** (§8). |
| [`resilience_integrations.md`](../../../contrats/resilience_integrations.md) | Contrat | **À lire en vague 1** : contrat le plus proche du sujet côté intégrations. Portée exacte **à établir**. |
| [`ups_arret_ha.md`](../../../contrats/ups_arret_ha.md) | Contrat | Traite l'**arrêt** de HA sur onduleur. Frontière avec C34 **à établir** : arrêt subi ≠ opération technique volontaire. |
| [`vmc.md`](../../../contrats/vmc.md) | Contrat | Seul contrat VMC, **fichier isolé** (pas de répertoire de domaine). |

> **Aucune de ces sources ne couvre seule le sujet.** C34 ne crée aucune doctrine : il
> cartographie, puis oriente. Toute règle nouvelle relèverait d'un chantier distinct.

---

## 5. Inventaire des sources

Volumétrie **relevée** au 2026-07-21 sur `main` (`d07e2870`). Cette section répond à
« **où se trouve la preuve potentielle ?** », pas à « que fait le système ? ».

### 5.1 Sources par domaine

| Domaine | Automatisations | Scripts | Templates | Contrats | Chantiers |
|---|---|---|---|---|---|
| climatisation | 23 | 6 | 43 | 43 | 13 |
| chauffage | 21 | 7 | 45 | 52 | 5 |
| VMC | 4 | 2 | 5 | **0** (`vmc.md` isolé) | **0** |
| déshumidificateur | 8 | 2 | 5 | 3 | **0** |
| arrosage | 6 | 3 | 14 | 19 | 3 |
| alarme | 14 | 9 | 7 | 16 | 7 |
| éclairage | 27 | 6 | 12 | 7 | 1 |
| **Total** | **103** | **35** | **131** | **140** | **29** |

Chemins : `11_automations/<domaine>/`, `10_scripts/<domaine>/`,
`12_template_sensors/<domaine>/`, `00_documentation_arsenal/contrats/<domaine>/`,
`00_documentation_arsenal/audits/04_chantiers/<domaine>/`.

**Asymétries à retenir pour le séquencement** : climatisation et chauffage concentrent
**95 contrats sur 140** et **88 templates sur 131**. À l'inverse, **VMC et déshumidificateur
n'ont aucun dossier de chantier**, et la VMC aucun contrat en répertoire. L'éclairage porte
le plus d'automatisations (27) pour seulement 7 contrats.

### 5.2 Helpers (transverses, non ventilés par domaine)

| Répertoire | Fichiers |
|---|---|
| `03_input_numbers/` | 110 |
| `04_input_texts/` | 52 |
| `05_input_booleans/` | 86 |
| `06_input_selects/` | 17 |
| `07_input_datetimes/` | 42 |
| `08_timers/` | 36 |
| `09_counters/` | 6 |
| **Total** | **349** |

Ce sont les porteurs directs de la problématique `initial` / restauration
(cf. `restauration_etat_helpers.md`).

### 5.3 Checkers

**85 checkers** dans `scripts/arsenal_contracts/`. **12** portent explicitement sur les sept
domaines : `check_alarme_contracts.py`, `check_chauffage_courbe_etancheite_contracts.py`,
`check_climatisation_admissibilite_contracts.py`, `check_climatisation_seuils_cool_contracts.py`,
`check_climatisation_ventilation_contracts.py`, `check_deshum_guard_contracts.py`,
`check_deshum_tx_contracts.py`, `check_deshumidificateur_metier_contracts.py`,
`check_eclairage_entree_contracts.py`, `check_eclairage_jardin_contracts.py`,
`check_eclairage_sejour_contracts.py`, `check_vmc_contracts.py`.

**Aucun checker identifié à ce stade ne cible le comportement au reboot ou au reload** — à
confirmer en vague 1.

### 5.4 Preuves terrain existantes

| Preuve | Apport présumé | Statut |
|---|---|---|
| [`preuve_terrain_c15_survie_persistantes_reboot.md`](../../01_rapports/notifications/preuve_terrain_c15_survie_persistantes_reboot.md) | Comportement **au reboot** de notifications persistantes | **À lire en priorité** — seule preuve runtime au reboot repérée |
| [`audit_resilience_integrations_domaine.md`](../../01_rapports/resilience_integrations/audit_resilience_integrations_domaine.md) | Résilience des **intégrations** | À lire en vague 1 |
| `arsenal-runtime/analyses/c34_effet_physique_rechargements_20260723/` (preuve L4, hors dépôt gouverné) | Effet physique **au reload** sur `switch.clim_power` : coupure + rejeu, **98,6 % équipement en marche**, délai médian 9 s ; contrôles négatifs et exclusion `unavailable` inclus | **Preuve runtime L4 acquise (2026-07-23)** — alimente la **vague 2** (climatisation) |
| idem, lot complémentaire (`comparaison_interdomaines.py`) | **Alarme** : aucun effet au reload sur `alarm_control_panel.alarme_maison` (signal propre) ; **5 autres domaines indéterminables** | **Preuve runtime L4 acquise (2026-07-23)** — alimente la **vague 4** (alarme) |

**C32 n'est pas retenu comme preuve générale de maîtrise des reloads.** Le résidu
`update.prise_chambre_enfants_2`, dont l'échec est apparu au journal le 2026-07-20 à
21:56:44, nuance l'affirmation « L6 soldé » et interdit d'en tirer une garantie transverse.

### 5.5 Historiques et sauvegardes

- **Recorder** : `purge_keep_days: 30`, **allowlist** (375 entités enregistrées).
- **Long-term statistics** : disponibles pour les seuls capteurs numériques éligibles.
- **L4 — analyses hors ligne** : la doctrine (§7) référence des **précédents**, pas une
  procédure. **R-L4-1 (clarifiée le 2026-07-23)** : L4 **ne corrige ni le code, ni un fait
  statique observé** — elle ne « répare » pas un défaut L1/L2 et ne remplace pas l'analyse
  statique qui **explique un mécanisme** ou **qualifie un effet**. En revanche, sur des
  entités **dans l'allowlist**, une preuve L4 **peut contredire une hypothèse, lever une
  indétermination ou requalifier une conclusion** L1/L2 lorsque le runtime apporte une preuve
  pertinente. Une entité **hors allowlist** reste absente de la sauvegarde **comme** de la
  base courante — L4 n'y peut rien.
- **`arsenal-runtime`** : dépôt **local, sans remote**, espace d'analyse hors ligne
  (`architecture/ecosysteme_depots_satellites.md` §1.1). **Ni composant runtime, ni satellite
  gouverné, ni méthode propriétaire, ni source normative ou autorité fonctionnelle.** Non
  accessible depuis `/config`. **Aucune conclusion n'est fondée sur la seule présence d'un
  fichier ou d'une affirmation dans ce dépôt.** En revanche, une preuve **peut y être
  conservée et reproduite** lorsqu'elle est fondée sur un **corpus runtime identifié, borné et
  contrôlé** — ici l'**historique Recorder archivé des entités concernées** (allowlist) : le
  dépôt est alors le **support probatoire et reproductible**, non la source de vérité
  fonctionnelle (arbitrage propriétaire du 2026-07-23 ; cf. §8, R-L4-1).

### 5.6 Apports runtime L4 acquis — pré-cartographie (2026-07-23)

Preuve reproductible déposée hors dépôt gouverné, admissible au titre de R-L4-1
clarifiée (§5.5) : historique Recorder archivé, entités **dans l'allowlist**, corpus
borné (2026-02-05 → 2026-07-21, témoin de couverture indépendant), deux contrôles
négatifs, exclusion de l'artefact `unavailable`. **Ce sont des apports à consommer par
les vagues, non des verdicts de qualification.**

| Domaine | Qualification §8 | Grille d'effet §2 | Portée |
|---|---|---|---|
| **climatisation** | démontré par preuve runtime existante | **effet établi** (coupure + rejeu) ; **qualification non tranchée** | La preuve établit **qu'un effet existe**, pas **s'il est un défaut**. « Action physique indésirable » **vs** « recalcul fonctionnel » relève de la **vague 2 (analyse statique)**. |
| **alarme** | démontré par preuve runtime existante | **continuité légitime** (aucun effet) | Aucun effet au reload sur l'état armé, signal propre. Alimente la **vague 4**. |
| **chauffage** | **indéterminable** | — | Aucun actionneur physique dans l'allowlist (seule une consigne planifiée, reconstruite). |
| **VMC** | **indéterminable** | — | Relais physique non historisé ; seul un helper de commande existe. |
| **arrosage** | **indéterminable** | — | Vanne Rain Bird non historisée ; drapeau de session logique, couverture 16 j. |
| **déshumidificateur** | **indéterminable** | — | Signal se reconstruisant au reload → artefact de restauration indissociable. |
| **éclairage** | **indéterminable** | — | Aucune entité `light.` ; une seule puissance de lampe, seuil on/off indéfini. |

**Cohérence avec §8** : les cinq verdicts *indéterminable* **confirment** la conséquence
directe du §8 (une entité hors allowlist ⇒ indéterminable, non contournable). Les
**besoins d'instrumentation** correspondants (historiser un actionneur physique propre par
`recorder.yaml`) sont consignés comme **limites et dépendances** — ils **ne sont pas
implémentés dans ce lot** et relèveraient d'un chantier d'instrumentation distinct (§9).

**Impact sur les critères de clôture (§9)** : ces apports **alimentent le critère ①**
(cartographie) pour la climatisation et l'alarme, et **étayent** les verdicts
*indéterminable* des cinq autres domaines. Ils **ne satisfont aucun critère à eux seuls** :
la cartographie reste à consolider sur les sept domaines et à qualifier statiquement ; le
contre-audit (②), le portefeuille (③) et les solutions (④) restent entiers. **Aucun
correctif n'est orienté** ; le caractère fautif ou légitime de l'effet climatisation reste
**à déterminer**.

---

## 6. Carte décision → action

**Aucun rôle ci-dessous n'est démontré.** Cette carte indique **où chercher**, domaine par
domaine. Chaque attribution est marquée « à vérifier » tant qu'une vague ne l'a pas établie
par lecture du code.

| Rôle | Emplacement candidat (à vérifier) |
|---|---|
| **Observation** | `12_template_sensors/<domaine>/` — capteurs dérivés des sources physiques |
| **Décision** | `12_template_sensors/<domaine>/` — verdicts, besoins, intentions |
| **Autorisation** | `12_template_sensors/<domaine>/` — `binary_sensor.*autorisation*`, vetos, gardes |
| **Action physique** | `11_automations/<domaine>/` et `10_scripts/<domaine>/` |
| **Diagnostic** | `12_template_sensors/<domaine>/` + `12_template_sensors/system/` |
| **UI** | `18_lovelace/` — hors périmètre sauf pour distinguer affichage et effet physique |

**Hypothèse de travail, à confirmer ou infirmer en vague 1** : la doctrine
`separation_decision_action.md` laisse attendre que la décision réside dans les templates et
l'action dans les automatisations/scripts. Cette répartition **n'est pas vérifiée** et
pourrait être partielle ou contredite selon les domaines.

**Points d'attention spécifiques, à instruire sans préjuger :**

- **Readiness** — l'existence et le rôle d'`input_boolean.systeme_stable` (ou d'un
  équivalent) doivent être **établis**, ainsi que les automatisations qui le consomment
  réellement. Sa seule présence ne prouve pas qu'il garde les chemins d'action.
- **Triggers de démarrage** — `homeassistant_start`, `homeassistant_started` et les triggers
  sur transition depuis `unknown` / `unavailable` sont les vecteurs candidats d'un rejeu.
- **Double writer** — plusieurs automatisations pouvant écrire la même cible physique.
- **Alarme** — seul domaine où une **révocation de sécurité** peut être le comportement
  correct : ne pas restaurer y est possiblement obligatoire.
- **Arrosage** — dépendance à un pont matériel externe (Rain Bird / MQTT), donc à une
  intégration dont le reload a un sens propre.

---

## 7. Stratégie d'audit par vagues

Quatre vagues, ordonnées pour **roder la méthode sur un volume faible** avant d'attaquer le
cœur thermique, et pour **isoler l'alarme**, dont la sémantique diffère des autres.

| Vague | Domaines | Volume runtime | Raison |
|---|---|---|---|
| **1** | VMC + déshumidificateur | 21 fichiers | Volume le plus faible, proximité fonctionnelle (traitement de l'air), **aucun chantier existant** — terrain vierge idéal pour fixer la méthode |
| **2** | climatisation + chauffage | 145 fichiers | Cœur thermique, **95 contrats sur 140**, dépendances croisées fortes, risque physique élevé |
| **3** | arrosage + éclairage | 68 fichiers | Arrosage : dépendance pont externe. Éclairage : 27 automatisations pour 7 contrats — asymétrie à instruire |
| **4** | alarme | 30 fichiers | **Traité seul** : la révocation de sécurité y est un comportement potentiellement correct, ce qui inverse la grille de lecture |

Chaque vague produit une section de cartographie **par domaine**, selon les rubriques de
l'audit, et n'émet que des conclusions qualifiées au sens du §8.

**Aucune vague n'est lancée par le présent document.**

---

## 8. Stratégie probatoire

Toute conclusion des vagues portera **obligatoirement** l'une de ces quatre qualifications :

| Qualification | Signification |
|---|---|
| **Démontré statiquement** | établi par lecture du code, des contrats et des checkers, sans dépendre d'une occurrence |
| **Démontré par preuve runtime existante** | établi par un historique, un journal ou un rapport **déjà produit** |
| **Probable mais non prouvé** | cohérent avec les sources, sans preuve suffisante |
| **Indéterminable** | l'observabilité actuelle ne permet pas de trancher |

**Limites déjà établies, opposables à l'audit :**

- **L1** — si le runtime n'émet pas l'événement, il n'y a rien à enregistrer.
- **L2** — une entité **hors allowlist Recorder** n'a **aucun** historique d'état ; un
  template purement dérivé est invisible s'il n'est pas historisé (R-L2-2), tandis qu'un
  helper écrit par appel de service est **partiellement** reconstructible via les événements
  (R-L2-1).
- **L3** — `purge_keep_days: 30` borne la base courante.
- **L4** — **ne corrige ni le code ni un fait statique** (R-L4-1, clarifiée le 2026-07-23) :
  elle ne remplace pas l'analyse statique qui **explique un mécanisme** ou **qualifie un
  effet**. Elle **peut néanmoins compléter une conclusion L1/L2 et en modifier la
  qualification** — contredire une hypothèse, lever une indétermination — quand elle est
  fondée sur un historique **d'entités dans l'allowlist**. Une sauvegarde ne restitue que ce
  qui était déjà enregistré.

**Conséquence directe et importante** : pour tout comportement dont la preuve reposerait sur
une entité hors allowlist, le verdict sera **indéterminable**, et **aucune sauvegarde ne
pourra le lever**. Ce cas devra être qualifié comme tel, non contourné.

**Interdits** : aucune panne provoquée, aucun forçage d'état, aucun reboot ni reload
déclenché pour produire une preuve. Une preuve obtenue en violant ces limites serait **non
solvable dans le cadre du chantier** (R-VERROU-2).

---

## 9. Critères de clôture

C34 est clos lorsque les quatre livrables suivants sont produits et mergés :

1. **Cartographie consolidée** des sept domaines, chaque conclusion portant une des quatre
   qualifications du §8 ;
2. **Contre-audit** ayant levé les raccourcis, confusions et généralisations de la
   cartographie initiale ;
3. **Portefeuille de chantiers** — chaque risque confirmé rattaché à un chantier existant ou
   nouveau, avec propriétaire, lots et preuves manquantes qualifiées ;
4. **Solutions documentées** pour les chantiers prioritaires, au niveau de détail permettant
   l'implémentation sans refaire l'analyse.

> **Aucun critère de clôture ne dépend d'une panne provoquée, d'un reboot fabriqué ou d'un
> reload déclenché pour les besoins de la preuve.** Les quatre critères sont **documentaires**,
> donc solvables sans preuve terrain — au sens du §9 de `solvabilite_probatoire.md`.
>
> Les comportements qui resteront **indéterminables** avec l'observabilité actuelle ne
> bloquent pas la clôture : ils doivent être **qualifiés** comme tels et, le cas échéant,
> donner lieu à un chantier d'instrumentation distinct.

---

## 10. Stop point

**Prochaine étape : vague 1 — VMC et déshumidificateur** (§7).

Ce document ne conclut sur **aucun** comportement. Il n'ouvre **aucun** sous-chantier
correctif. Toute orientation corrective relève du portefeuille (livrable 3), après
cartographie et contre-audit.

---
