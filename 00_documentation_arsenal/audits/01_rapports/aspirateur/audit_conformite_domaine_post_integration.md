# 🤖 ARSENAL — AUDIT — Conformité du domaine **Aspirateur** après intégration des huit lots

> ## ⚠️ AUDIT NON ARBITRÉ
>
> **Ce document consigne des constats proposés. Il ne modifie ni les contrats, ni le
> registre des chantiers, ni l'état de clôture du domaine.**
>
> Aucun écart n'est corrigé, aucun numéro de chantier n'est créé, aucune clause
> contractuelle n'est amendée. Les qualifications portées ici sont **celles de
> l'audit**, soumises à contre-vérification puis à arbitrage opérateur. Tant que cet
> arbitrage n'est pas rendu, **aucun constat de ce rapport n'est opposable**.

> **Trace d'audit documentaire, lecture seule.** Passe du 2026-08-30, **strictement
> statique** : aucun service appelé, aucune commande émise, aucun essai terrain, aucun
> accès à l'instance. Aucun fichier runtime, contrat, checker, Lovelace ou registre
> modifié par cette passe.
> Convention : **[FAIT]** observé par lecture du dépôt à la révision auditée ·
> **[LECTURE]** interprétation d'une clause contractuelle, susceptible d'être infirmée
> par un arbitrage · **[HYP]** comportement d'exécution inféré, non observé ·
> **[À VÉRIFIER]** question ouverte adressée à la contre-vérification.
> Ce document est un **relevé d'observation**, pas un contrat. Il n'est ni normatif ni
> opposable.

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Titre** | Audit de conformité du domaine `aspirateur` après intégration des huit lots |
| **Domaine audité** | `aspirateur` |
| **Nature** | **Audit initial non arbitré** — constats proposés, aucun arbitrage rendu |
| **Date de la passe** | 2026-08-30 |
| **Branche auditée** | `claude/audit-domaine-aspirateur-9akhwp` |
| **SHA exact audité** | `31afb9fde567aa46e62a81d75fc1d3874f556011` |
| **Commit de tête** | `31afb9f` — *Aspirateur — les six profils dans une liste unique, libellés rendus (#751)*, 2026-08-30 |
| **État de l'arbre au moment de l'audit** | propre — `git status --short` vide, un seul worktree |
| **Nature de la passe** | statique (lecture du dépôt), **sans** accès runtime ni terrain |

### 1.1 Périmètre réellement examiné

**Lu intégralement :**

| Ensemble | Fichiers |
|---|---|
| Contrat du domaine | les **16** fichiers de `00_documentation_arsenal/contrats/aspirateur/` |
| Scripts | `10_scripts/aspirateur/` — `lancer_mission.yaml`, `conduire_mission.yaml`, `declarer_entretien.yaml` *(cœur de séquence)*, `appliquer_raccourci.yaml`, `composer_intention.yaml`, `reinitialiser_composition.yaml` |
| Templates | `12_template_sensors/aspirateur/` — `etat_canonique.yaml`, `motif_lisible.yaml`, `conditions_lancement_hors_carte.yaml` |
| Lovelace | `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml`, `entretien_action.yaml` ; `18_lovelace/dashboards.yaml` et `18_lovelace/includes/navigation/aspirateur.yaml` *(rattachement)* |
| Cadrage | `00_documentation_arsenal/audits/02_conception/aspirateur/cadrage_l2_maintenance_ui/10_LOTS.md` |
| Registre | entrée `C42` de `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md` |

**Lu partiellement — inspection ciblée, non exhaustive :**

- `11_automations/aspirateur/` — `notification_mission.yaml`, `supervision_mission.yaml`,
  `remise_a_zero_composition.yaml`, `notification_entretien.yaml` : en-têtes,
  déclencheurs et autorités de lecture. **La logique interne de `supervision_mission.yaml`
  et de `notification_entretien.yaml` n'a pas été dépliée ligne à ligne.**
- `scripts/arsenal_contracts/check_aspirateur_contracts.py` (11 995 lignes) : périmètre de
  balayage, constantes de tables fermées, et contrôles nommément cités.
  **La batterie d'auto-tests n'a pas été relue.**
- `04_input_texts/aspirateur/mission.yaml` : en-tête et décompte du vocabulaire seulement.

**Hors périmètre de cette passe, et non examiné :**

- `12_template_sensors/aspirateur/entretien.yaml` et `carte_courante.yaml` ;
- `18_lovelace/includes/cartes/aspirateur/entretien.yaml` et `carte_robot.yaml` ;
- `19_button_card_templates/40_dashboards/aspirateur/` ;
- les entités natives Roborock elles-mêmes, et tout comportement d'appareil ;
- **tout autre domaine** — l'audit ne s'étend ni à `alarme`, ni aux domaines transverses.

### 1.2 Méthode et commandes de vérification

```
git rev-parse HEAD                       # révision auditée
git status --short                       # arbre propre avant et après
git worktree list                        # worktree unique
python3 scripts/arsenal_contracts/check_aspirateur_contracts.py
grep -rn "cinq profils" 00_documentation_arsenal/contrats/aspirateur/ 12_template_sensors/aspirateur/
grep -n "not in verdict_ouvert" -B 6 10_scripts/aspirateur/conduire_mission.yaml
grep -n "mission_ouverte" 12_template_sensors/aspirateur/etat_canonique.yaml \
                          18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml
```

Méthode : lecture du contrat chapitre par chapitre → lecture du runtime correspondant →
confrontation clause par clause → recherche mécanique des dérives de vocabulaire →
vérification du périmètre de balayage du checker sur chaque écart trouvé.

### 1.3 Résultat du checker observé

Exécution de `scripts/arsenal_contracts/check_aspirateur_contracts.py` à la révision
auditée :

```
OK - domaine Aspirateur : intégrité normative, conduite runtime, acte contractuel
Maintenance, projection d'entretien, projections persistantes, conduite et supervision
de mission, couche d'intention vérifiées — 40 lignes affichées pour 42 contrôles
logiques, 0 écart.
```

Périmètre déclaré par le checker : 16 fichiers de contrat · 463 fichiers Lovelace ·
5 fichiers runtime L1 · 3 fichiers runtime L2 · 1 800 fichiers YAML balayés par
`ASP-CI-11` · 1 814 par `ASP-CI-31` · 51 identifiants attestés · 1 fichier runtime M1 ·
4 automations · 7 fichiers de la couche d'intention.

> **[FAIT] Aucun des cinq constats ci-dessous n'est détecté par ce checker.** Pour
> chacun, le rapport indique pourquoi — périmètre de balayage, ou contrôle absent. Le
> résultat vert du checker et les constats de ce rapport **ne se contredisent pas** :
> ils portent sur des objets différents.

---

## 2. Statut du document

**`AUDIT NON ARBITRÉ` — ce document consigne des constats proposés. Il ne modifie ni les
contrats, ni le registre des chantiers, ni l'état de clôture du domaine.**

| Ce que ce document est | Ce qu'il n'est pas |
|---|---|
| Un relevé de lecture statique, daté et rattaché à un SHA | Un contrat, un amendement, une clause opposable |
| Une proposition de qualification, constat par constat | Un arbitrage rendu |
| Une base de contre-vérification indépendante | Une preuve de non-conformité fonctionnelle |
| Un préalable **possible** à une inscription au registre | Une inscription au registre, ni un numéro de chantier |

> **Rappel doctrinal appliqué à ce rapport.**
> [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
> §2 distingue trois verdicts à ne jamais confondre, et pose `R-VERDICT-1` :
> *« Toute conclusion relevant du verdict 3 — non-conformité fonctionnelle — DOIT être
> étayée par une observation positive du comportement, jamais par une absence. »*
>
> **Cet audit est statique. Aucun de ses constats ne peut donc, en l'état, atteindre le
> verdict 3.** Les qualifications proposées au §4 relèvent au plus de l'**écart de
> conformité documentaire ou structurelle constaté en lecture**. Leur promotion en
> non-conformité fonctionnelle exige une observation terrain — chaque constat indique
> laquelle.

---

## 3. Conclusion générale proposée

> **Cette conclusion est celle de l'audit. Elle est proposée, non acquise.**

L'audit propose de distinguer deux propositions, vraies simultanément et à ne pas
substituer l'une à l'autre :

**a) Complétude fonctionnelle alléguée.** [FAIT] Les **huit lots** du découpage ratifié
`D-44` ([`10_LOTS.md`](../../02_conception/aspirateur/cadrage_l2_maintenance_ui/10_LOTS.md)
§2) sont présents dans le dépôt : `M0` (#734), `M1` (#735), `N1` (#736), `L2` (#738),
`U1` (#739), `U0` + `U2` (#740), `M2` (#748). Les trois écrans du domaine sont déclarés
(`18_lovelace/dashboards.yaml`) et rattachés à la navigation. Les 42 contrôles du checker
du domaine passent. Le moteur de mission implémente la séquence normative du chapitre
[`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) — ordre eau→aspiration,
double confirmation cartographique, exigence de publication fraîche (`ASP-INV-72`),
garde d'abstention de l'étape 5, revérification tardive intégrale, partition totale des
états.

**b) Absence de clôture contractuelle alléguée.** L'audit propose que le domaine **ne
soit pas considéré comme clos**, pour cinq motifs consignés au §4, dont **deux** portent
un effet opérateur allégué (`AUD-ASP-01`, `AUD-ASP-05`) et **trois** relèvent d'une
dérive entre le texte et ce qu'il décrit (`AUD-ASP-02`, `AUD-ASP-03`, `AUD-ASP-04`).
S'y ajoutent les éléments déjà déclarés ouverts au §5, qui **ne sont pas des écarts** et
que l'audit ne requalifie pas.

> **Ce que cette conclusion n'affirme pas.** Elle n'affirme pas que le domaine est
> défaillant, ni qu'une mission serait mal exécutée : **aucun constat de ce rapport ne
> porte sur la chaîne d'émission d'une commande**, que l'audit a trouvée conforme au
> chapitre `07` sur tous les points examinés. Les constats portent sur la **frontière
> UI**, sur la **restitution** et sur la **cohérence documentaire**.
>
> **Elle n'affirme pas davantage que la liste du §4 est exhaustive.** Le périmètre
> partiellement examiné du §1.1 n'a pas été déplié ; d'autres écarts peuvent exister
> dans les fichiers non lus.

---

## 4. Constats

**Identifiants locaux `AUD-ASP-01` à `AUD-ASP-05`.**

> ⚠️ **Ces identifiants sont internes à ce rapport.** Ils ne sont **ni** des invariants
> contractuels, **ni** des codes de refus, **ni** des identifiants CI, **ni** des IDs
> d'automatisation, **ni** des numéros de chantier. Ils n'ont d'autre fonction que de
> permettre une confrontation constat par constat lors de la contre-vérification et de
> l'arbitrage. **Ils ne doivent pas être promus tels quels** : une éventuelle
> inscription au registre relève d'un geste opérateur distinct, postérieur à
> l'arbitrage, et attribuera ses propres identifiants.

---

### `AUD-ASP-01` — Coexistence de deux notions de « mission ouverte », et garde des gestes de conduite sur la mauvaise

**Constat proposé.** Le domaine porte **deux** notions distinctes de « mission
ouverte », introduites par deux chapitres différents. Le backend de conduite garde sur
l'une ; l'interface garde sur l'autre. Les deux ne coïncident pas, et le contrat établit
lui-même qu'elles divergent.

**Fichiers, blocs et ancres examinés** *(lignes données à la révision auditée, avec
ancre symbolique stable)* :

| Fichier | Ancre symbolique | Ligne |
|---|---|---|
| `12_template_sensors/aspirateur/etat_canonique.yaml` | attribut `mission_ouverte` du capteur `aspirateur_etat_canonique`, dérivé de `binary_sensor.roborock_q7_max_nettoyage` | 96-98 |
| `10_scripts/aspirateur/conduire_mission.yaml` | garde d'entrée `{{ states('input_text.aspirateur_mission_verdict') not in verdict_ouvert }}` → `stop:` | 255-262 |
| `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` | bloc `4️⃣ CONDUITE` : condition `or` de section, puis conditions par bouton, toutes sur `sensor.aspirateur_etat_canonique` (état et attribut `mission_ouverte`) | 624-745 |
| `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` | tuile de lecture `name: Mission`, `attribut: mission_ouverte` | 142-156 |
| `11_automations/aspirateur/notification_mission.yaml` | déclencheur `entity_id: input_text.aspirateur_mission_verdict` | 186 |

**Clauses et invariants invoqués :**

- [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 et `ASP-INV-68` —
  le dixième état canonique **Mission ouverte** « ne dérive **pas** de l'état machine
  mais du **témoin de session** ».
- [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2, `ASP-INV-87` —
  « Une mission Arsenal est ouverte **si et seulement si** le verdict appartient à la
  classe O […]. Aucun témoin natif — état machine, témoin de session, entité `vacuum` —
  ne l'établit ni ne s'y substitue. »
- [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §3 — le témoin de
  session est établi **faux dans les deux sens**, avec trois reproductions du cas
  sous-inclusif en `returning_home` (53 s, 25 s, puis 28,3 s consignées dans l'en-tête
  de `10_scripts/aspirateur/lancer_mission.yaml`).
- `ASP-INV-48` — un geste sans sens physique « n'est **pas** présenté comme disponible
  […] il n'est pas non plus « proposé puis ignoré » ».
- `ASP-INV-50` — « un refus muet, un **bouton inerte** […] sont **non conformes** ».
- `ASP-INV-43` — « En cas de doute, on **n'empêche pas** l'arrêt. »
- `ASP-INV-91` — un refus de geste n'écrit aucun verdict ; le motif est rendu par
  « journal et trace Home Assistant ».
- [`11`](../../../contrats/aspirateur/11_frontiere_ui.md) §2 — interdit de « présenter
  comme disponible un geste sans sens physique ».

**Scénarios opérateur allégués** — [HYP], non observés :

- **(a) Mission externe.** Un cycle lancé depuis l'application Roborock porte
  `sensor.roborock_q7_max_etat = segment_cleaning` → `etat_canonique = nettoyage_reel`
  et `mission_ouverte = oui`. La section Conduite et les boutons *Mettre en pause*,
  *Arrêter la mission* et *Renvoyer à la base* s'affichent. Le verdict n'étant pas de
  classe O, `conduire_mission.yaml` s'arrête à sa garde d'entrée sans rien écrire.
  Le capteur `sensor.aspirateur_motif_lisible`, seul canal de restitution du panneau,
  reste sur sa valeur antérieure.
- **(b) Mission Arsenal en retour au dock.** Sur une mission ouverte par Arsenal
  (verdict `LANCEE/DEMARRAGE_OBSERVE`, classe O), l'entrée en `returning_home` fait
  passer le témoin de session à `off` — fait établi par le chapitre `08` §3 — donc
  `mission_ouverte = non` et `etat_canonique = retour_base`. Aucun des trois termes de
  la condition `or` de section n'est satisfait : **la section Conduite entière
  disparaît**, en-tête compris, alors que le verdict reste de classe O et que la garde
  d'arrêt du chapitre `15` §3.1 est « mission ouverte » nue.

**Effets allégués :**

- (a) trois boutons présentés comme disponibles et sans effet observable pour
  l'opérateur — la situation que `ASP-INV-48` et `ASP-INV-50` décrivent comme non
  conforme ;
- (b) perte du geste d'arrêt pendant le retour, alors que `ASP-INV-43` demande de ne
  jamais le contraindre plus que le lancement ;
- (c) **divergence de restitution à un même instant** : dans le scénario (b), la
  notification persistante de cycle — pilotée par le verdict — annonce une mission en
  cours, la tuile *Mission* du panneau affiche « Aucune », et les gestes ont disparu.

**Qualification proposée par l'audit :** écart de conformité **structurel**, de portée
frontière UI ↔ backend. **Cause proposée** : le chapitre `15` a introduit une seconde
autorité de « mission ouverte » sans que le chapitre `08`, le capteur dérivé, ni le
panneau soient réconciliés. **Priorité proposée : la plus haute des cinq.**

**Pourquoi la CI ne le voit pas.** [FAIT] `ASP-CI-23` **impose** au contraire la
dérivation par le témoin de session : `ETAT_ORTHOGONAL = "mission_ouverte"` avec le
commentaire *« dérive du TÉMOIN DE SESSION, pas de l'état machine »*
(`check_aspirateur_contracts.py`, constantes du contrôle `check_etat_canonique_rendu`).
Aucun contrôle ne confronte les conditions Lovelace de la section Conduite à
`ASP-INV-87`.

**Interprétation contractuelle engagée.** [LECTURE] Le constat retient qu'`ASP-INV-87`
s'impose à la **projection UI**, et pas seulement aux écrivains du verdict (§7.2). Cette
lecture est **infirmable par arbitrage** : retenue autrement, le constat se réduit au
scénario (b) — la perte du geste d'arrêt — voire disparaît. L'audit **ne tranche pas**
entre le témoin de session, le verdict et un éventuel second attribut : ce choix reste
celui de l'opérateur.

**Preuve terrain manquante.** Les deux scénarios sont [HYP] et **non observés** :
l'affichage effectif de la section Conduite dans chacun des deux états, et l'effet
visible d'une pression sur les boutons. Questions `T-1`, `T-2` et `T-4` du §6.3. Leur
absence signifie **preuve absente**, jamais constat infirmé ni confirmé (`R-VERDICT-1`).

**À contre-vérifier :**

1. Le témoin de session vaut-il bien `off` en `returning_home` sur l'instance courante,
   et la section Conduite disparaît-elle effectivement ? *(observation terrain)*
2. La garde d'arrêt de `conduire_mission.yaml` accepte-t-elle bien un `arret` sur
   verdict `LANCEE/DEMARRAGE_OBSERVE` avec `etat_canonique = retour_base` ? *(lecture
   ou essai)*
3. Le scénario (a) est-il **hors périmètre assumé** — le contrat n'ayant jamais promis
   de conduire une mission externe (`ASP-INV-87`, « aucune mission externe n'est
   adoptée ») — auquel cas l'écart se réduit à *ne pas afficher* les boutons, sans
   toucher au backend ?
4. Les deux notions doivent-elles fusionner, ou coexister sous **deux noms distincts** ?
   Le chapitre `08` interdit un second code pour un même état ; il ne dit rien de deux
   états sous un même nom.

**Absence d'arbitrage.** Aucune correction n'est proposée ici, et le choix entre
« dériver `mission_ouverte` du verdict », « ajouter un second attribut » et « regarder
le verdict depuis le panneau » **n'est pas tranché** : il engage `ASP-CI-23`, le
chapitre `08` et le chapitre `15`, et relève de l'opérateur.

---

### `AUD-ASP-02` — Profils Serpillière présentés sans projection de leur prérequis matériel

**Constat proposé.** Les deux profils avec eau, et le raccourci qui en pose un, sont
présentés sans aucune condition sur le témoin de serpillière — et aucun objet du domaine
ne projette ce prérequis.

**Fichiers, blocs et ancres examinés :**

| Fichier | Ancre symbolique | Ligne |
|---|---|---|
| `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` | bloc `⚙️ Profil de nettoyage`, cartes `name: Serpillière moyenne` et `name: Serpillière intensive` — aucune `condition` | 435, 442 |
| `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` | raccourci `name: RDC — serpillière complète`, `data: raccourci: rdc_serpilliere` — aucune `condition` | 550, 558 |
| `12_template_sensors/aspirateur/conditions_lancement_hors_carte.yaml` | bloc `🧩 PÉRIMÈTRE` et attribut `hors_perimetre: "contexte cartographique, serpilliere"` — exclusion **délibérée** | 15-24, 100 |
| `10_scripts/aspirateur/lancer_mission.yaml` | `ÉTAPE 3 bis`, refus `REFUS/PREREQUIS_MATERIEL_ABSENT` — **présent et correct** | 511-551 |

**Clauses et invariants invoqués :**

- `ASP-INV-13` ([`03`](../../../contrats/aspirateur/03_profils_metier.md) §4) —
  « **Symétrie obligatoire** […] : aucun chemin — ni raccourci, ni UI, ni appel direct
  au moteur — ne présente ces profils comme lançables lorsque le prérequis est absent.
  Une impossibilité physique n'admet **aucun** override. »
- [`11`](../../../contrats/aspirateur/11_frontiere_ui.md) §2 — interdit de « présenter
  comme disponible […] un profil dont le prérequis matériel est absent ».
- [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md) §6.1 —
  symétrie des impossibilités de catégorie A.

**Scénario opérateur allégué** — [HYP] : serpillière non posée
(`binary_sensor.roborock_q7_max_serpilliere_fixee = off`). Les deux profils Serpillière
et le raccourci « RDC — serpillière complète » restent sélectionnables. L'opérateur
compose, presse *Lancer la mission*, et le moteur refuse en
`REFUS/PREREQUIS_MATERIEL_ABSENT`.

**Effet allégué.** Aucun risque d'exécution : le refus backend est présent, correct, et
son motif est restitué par `sensor.aspirateur_motif_lisible` — l'opérateur est informé.
L'effet est un **geste perdu** et une clause de symétrie UI non tenue.

**Qualification proposée par l'audit :** écart de conformité **à la frontière UI**, sans
effet sur la sûreté. Distinct de `AUD-ASP-01` : ici le refus **est** restitué.

**Point de lecture, à ne pas trancher ici.** [LECTURE] `ASP-INV-13` écrit « présente ces
profils comme **lançables** ». Sélectionner un profil n'est pas lancer — la lecture
stricte pourrait donc borner l'invariant au seul bouton de lancement. Le chapitre `11`
§2 est en revanche rédigé sans ce qualificatif : « présenter comme **disponible** […] un
profil dont le prérequis matériel est absent ». **L'audit ne tranche pas entre les deux
lectures.**

**Pourquoi la CI ne le voit pas.** [FAIT] Aucun contrôle ne confronte les cartes de
sélection de profil au témoin de serpillière ; `ASP-CI-7` balaie Lovelace à la recherche
d'entités natives d'action, ce qui est un autre objet.

**Interprétation contractuelle engagée.** [LECTURE] Celle de la rubrique *Point de
lecture* ci-dessus : « disponible » ([`11`](../../../contrats/aspirateur/11_frontiere_ui.md)
§2) et « lançables » (`ASP-INV-13`) porteraient la **même** exigence. Retenue autrement,
le constat disparaît — seul le bouton de lancement serait concerné, et il est
correctement gardé côté backend (§7.2). Le refus
`REFUS/PREREQUIS_MATERIEL_ABSENT` reste, lui, **constaté et non requalifié**.

**Preuve terrain manquante.** Aucune observation n'établit **sous quelle forme** les
deux profils Serpillière et le raccourci « RDC — serpillière complète » sont
effectivement rendus lorsque le prérequis est absent — présentés actifs, désactivés, ou
masqués. Question `T-5` du §6.3. L'audit **ne présume pas** ce que cette observation
montrerait.

**À contre-vérifier :**

1. Quelle lecture d'`ASP-INV-13` prévaut, au regard de `11` §2 ?
2. Si la symétrie est due : porte-t-elle sur le **masquage**, sur une **désactivation
   visible**, ou sur un simple **avertissement** ? Le chapitre ne le dit pas.
3. Faut-il alors **étendre** `conditions_lancement_hors_carte.yaml` — ce que son propre
   en-tête exclut explicitement, la serpillière dépendant de l'intention et non de
   l'appareil seul — ou créer un objet distinct ?
4. Le masquage d'un profil est-il compatible avec `ASP-INV-16` (« la sélection UI
   représente l'intention, pas l'appareil ») ?

**Absence d'arbitrage.** L'audit ne propose aucune des trois formes, et note que la
troisième question ouvre un conflit possible entre `ASP-INV-13` et `ASP-INV-16`.

---

### `AUD-ASP-03` — Dérive documentaire « cinq profils », et en-tête périmé de `appliquer_raccourci.yaml`

**Constat proposé.** L'amendement du chapitre `03` portant la table à **six** profils n'a
pas été propagé aux chapitres qui la citent, ni au motif rendu à l'opérateur. En
parallèle, l'en-tête de `appliquer_raccourci.yaml` décrit un contenu que le corps du
fichier n'a plus.

**Volet A — le décompte « cinq », après l'amendement à six.**

| Fichier | Ancre symbolique | Ligne | Texte constaté |
|---|---|---|---|
| `00_documentation_arsenal/contrats/aspirateur/03_profils_metier.md` | §1, table canonique | 22 | « **Six profils, et six seulement.** » — **source amendée** |
| `.../contrats/aspirateur/README.md` | table « Structure du dossier », ligne `03_profils_metier.md` | 61 | « Les **cinq** profils arrêtés » |
| `.../contrats/aspirateur/05_intention_de_mission.md` | §4, table des régimes, ligne `Profil` | 83 | « L'un des **cinq** » |
| `.../contrats/aspirateur/09_refus_et_diagnostics.md` | §2, catalogue, ligne `PROFIL_INCONNU` | 55 | « n'appartient pas aux **cinq** profils arrêtés » |
| `.../contrats/aspirateur/12_identifiants_a_fournir.md` | §2.1, rôle `‹intention_profil›` | 32 | « parmi les **cinq** arrêtés » |
| `12_template_sensors/aspirateur/motif_lisible.yaml` | dictionnaire `motifs`, clé `'PROFIL_INCONNU'` | 113 | « ne fait pas partie des **cinq** profils du domaine » |

[FAIT] Le runtime, lui, porte bien **six** profils : table `profils` de
`lancer_mission.yaml` (l. 277-283), table de traduction de `composer_intention.yaml`
(l. 74-80), et six cartes dans le bloc `⚙️ Profil de nettoyage` du panneau.

**Volet B — en-tête de `10_scripts/aspirateur/appliquer_raccourci.yaml`.**

| Ancre symbolique | Ligne | Constat |
|---|---|---|
| Bloc `🎯 RÔLE` | 6 | « un des **cinq** raccourcis » |
| Bloc `🔒 CE QUE CE SCRIPT NE FAIT JAMAIS` | 22 | « les **cinq** raccourcis sont mono-carte » |
| Bloc `🔑 CHAMP FERMÉ raccourci — CINQ VALEURS, ET CINQ SEULEMENT` | 28-40 | énumère `rdc_complet`, `entree_escaliers_wc_rdc`, `sejour_seul`, `etage_complet`, `annexe_complete` |
| Bloc `🔗 ÉCRIT — DEUX FAMILLES DE HELPERS, PAS TROIS` | 42-45 | n'annonce que `input_select.aspirateur_intention_carte` et `input_boolean.aspirateur_segment_*` |
| `fields: raccourci: description:` | 58-62 | « `rdc_aspiration`, `rdc_serpilliere`, `etage_aspiration` » — **à jour** |
| Bloc `variables: raccourcis:` | 88-105 | **trois** clés : `rdc_aspiration`, `rdc_serpilliere`, `etage_aspiration` |
| Écritures effectives | 137-186 | `intention_carte`, `aspirateur_segment_*`, **`intention_profil`**, **`intention_passages`** — quatre entités, trois familles |

**Clauses et invariants invoqués :**

- [`entetes_fichiers.md`](../../../architecture/03_doctrines/entetes_fichiers.md) —
  l'en-tête de fichier vaut **contrat local**.
- `ASP-INV-50` — un motif est intelligible s'il permet de savoir quoi faire ; un
  diagnostic faux est proscrit au même titre qu'un refus muet
  ([`09`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) §1).
- `ASP-INV-52` — l'extension du vocabulaire est un acte contractuel impliquant la mise à
  jour du catalogue **et** du chapitre porteur.
- `ASP-INV-57` — créer, modifier ou supprimer un raccourci est un acte contractuel.

**Scénario opérateur allégué** — [HYP], pour le seul volet A : un profil absent ou hors
table produit `REFUS/PROFIL_INCONNU`, et le panneau affiche « Le profil demandé ne fait
pas partie des **cinq** profils du domaine » alors que six sont exposés juste au-dessus,
dans la même carte.

**Effets allégués :** un motif opérateur factuellement faux (volet A, `motif_lisible`) ;
quatre chapitres contractuels dont le décompte contredit leur propre source (volet A) ;
un contrat local décrivant cinq raccourcis inexistants et sous-déclarant les écritures
du script (volet B).

**Qualification proposée par l'audit :** écart **documentaire**, sans effet fonctionnel —
la validation runtime porte sur la table à six, non sur la prose. **Le seul point à
effet opérateur est la chaîne du `motif_lisible`.**

**Pourquoi la CI ne le voit pas.** [FAIT] `ASP-CI-21` confronte la table du chapitre `03`
au référentiel embarqué du moteur — donc les **valeurs**, pas la **prose** ni les
décomptes en toutes lettres. Aucun contrôle ne confronte un en-tête de script au corps
du même fichier.

**Interprétation contractuelle engagée.** [LECTURE] **Aucune n'est nécessaire pour
établir la dérive textuelle** : les six emplacements du volet A et les blocs du volet B
sont des **faits de texte**, relevés littéralement. Une lecture n'est engagée que par la
**qualification** : le chapitre `03` étant désigné source unique, l'audit **penche pour**
un décompte rédactionnel plutôt que normatif — **sans trancher** (question 1 ci-dessous,
§7.2).

**Preuve terrain manquante.** **Sans objet — constat de texte entièrement vérifiable en
lecture statique**, pour la dérive elle-même. Ce « sans objet » **ne couvre pas** la
conséquence opérateur alléguée — le motif faux rendu par `motif_lisible` —, qui reste
une [HYP] et resterait à établir par observation si elle était invoquée.

**À contre-vérifier :**

1. Le décompte en toutes lettres dans `05`, `09`, `12` et le `README` est-il **normatif**
   ou **rédactionnel** ? Le chapitre `03` étant désigné source unique, l'audit penche
   pour rédactionnel — **sans trancher**.
2. La correction relève-t-elle d'un amendement contractuel (`ASP-INV-52`) ou d'une
   simple passe rédactionnelle sans changelog ?
3. Une garde CI sur les décomptes en toutes lettres est-elle souhaitable, ou
   introduirait-elle une fragilité de rédaction comparable au piège d'`ASP-CI-3`
   documenté en [`10_LOTS.md`](../../02_conception/aspirateur/cadrage_l2_maintenance_ui/10_LOTS.md)
   §3.5 ?
4. Volet B : l'en-tête doit-il être réaligné, ou le champ fermé revenir à cinq
   raccourcis ? La table du chapitre `10` §3.1 en arrête **trois** — l'audit lit donc le
   corps comme juste et l'en-tête comme périmé, **sans trancher**.

**Absence d'arbitrage.** Aucune reformulation n'est proposée, et l'audit ne préjuge pas
du véhicule contractuel de la correction.

---

### `AUD-ASP-04` — En-tête périmé de `notification_mission.yaml` : une « conséquence assumée » que le moteur ne produit plus

**Constat proposé.** L'en-tête de l'automation de projection de cycle déclare comme
défaut assumé et non corrigeable un scénario que la garde d'entrée du moteur, livrée
dans **le même commit**, rend inatteignable.

**Fichiers, blocs et ancres examinés :**

| Fichier | Ancre symbolique | Ligne |
|---|---|---|
| `11_automations/aspirateur/notification_mission.yaml` | bloc `🕳️ CE QUE LE choose NE COUVRE PAS`, alinéa `CONSÉQUENCE ASSUMÉE, ÉCRITE PLUTÔT QUE MASQUÉE` | 141-151 |
| `10_scripts/aspirateur/lancer_mission.yaml` | bloc `🛡️ ÉTAPE 0a — MISSION DÉJÀ OUVERTE : SE TAIRE, ET NE RIEN ÉCRIRE`, `choose` → `stop:` avant toute écriture | 314-360 |

[FAIT] Texte constaté dans l'en-tête : *« Si le moteur est appelé alors qu'une mission
est ouverte, il écrit d'abord sa valeur de validation — de classe H — puis son refus :
la mémoire de mission est alors perdue par le verdict lui-même, et cette projection ne
peut plus éteindre la notification […]. Le corriger exigerait de rouvrir le vocabulaire
ou la séquence du moteur, ce que ce lot ne fait pas. »*

[FAIT] L'étape 0a de `lancer_mission.yaml` s'arrête **avant** l'écriture de
`VALIDATION_EN_COURS` lorsque le verdict courant appartient à `verdict_ouvert` — les
neuf valeurs de classe O et O-R.

[FAIT] `git log -S` situe les **deux** blocs dans le même commit : `89d05f9` —
*feat(aspirateur)+ci: conduite et supervision de mission, chapitre 15 (lot L2) (#738)*.

**Clauses et invariants invoqués :**

- [`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §1, *Amendement `L2` — le
  moteur se tait sur une mission déjà ouverte* — la garde est **contractualisée**.
- `ASP-INV-87` et `D-08` — le verdict de classe O est la seule mémoire de mission ; rien
  ne l'écrase.
- [`entetes_fichiers.md`](../../../architecture/03_doctrines/entetes_fichiers.md) —
  l'en-tête vaut contrat local.

**Scénario opérateur allégué :** **aucun.** Ce constat n'a pas d'effet d'exécution : il
porte sur un texte, non sur un comportement.

**Effet allégué.** Un lecteur du fichier — humain ou session ultérieure — conclut qu'un
défaut connu subsiste et qu'il n'est pas corrigeable, alors que le dépôt le referme
quelques fichiers plus loin. Risque de travail redondant, ou d'un chantier ouvert sur un
défaut inexistant.

**Qualification proposée par l'audit :** écart **documentaire**, de sévérité proposée la
plus faible des cinq, sans effet fonctionnel.

**Pourquoi la CI ne le voit pas.** [FAIT] Aucun contrôle ne confronte la prose d'un
en-tête d'automation à la séquence d'un script tiers.

**Interprétation contractuelle engagée.** [LECTURE] **Aucune.** L'existence de l'en-tête
périmé est un **fait textuel** : le texte de l'en-tête et la séquence de l'étape 0a sont
relevés littéralement, et leur appartenance au même commit est établie par `git log -S`.
Une lecture n'est engagée que par la **qualification** proposée — « écart documentaire »,
sévérité proposée la plus faible des cinq —, jamais par le fait lui-même.

**Preuve terrain manquante.** **Sans objet — constat de texte entièrement vérifiable en
lecture statique.** Ce constat ne porte sur aucun comportement, et **ne s'étend à aucun
autre en-tête du domaine** : l'audit ne les a pas cherchés (question 3 ci-dessous).

**À contre-vérifier :**

1. L'étape 0a couvre-t-elle **exactement** le scénario décrit par l'en-tête, ou en
   subsiste-t-il un résidu — par exemple un verdict de classe O écrasé par une voie
   autre que le moteur ?
2. La garde étant **postérieure en lecture** mais **contemporaine en commit**, l'en-tête
   décrit-il un état antérieur à une révision de la PR, jamais réaligné ?
3. Existe-t-il d'autres en-têtes du domaine décrivant des défauts refermés depuis ?
   **L'audit ne l'a pas cherché** — seul ce fichier a été examiné sous cet angle.

**Absence d'arbitrage.** L'audit ne propose aucune réécriture et ne se prononce pas sur
la question 1, qui exige une relecture ciblée du chemin d'écriture du verdict.

---

### `AUD-ASP-05` — Refus muets du parcours Entretien

**Constat proposé.** Les gardes d'entrée de la déclaration d'entretien s'arrêtent sans
écrire aucune valeur, et la carte d'action ne masque délibérément aucun bouton : une
déclaration refusée ne produit aucune restitution visible.

**Fichiers, blocs et ancres examinés :**

| Fichier | Ancre symbolique | Ligne |
|---|---|---|
| `10_scripts/aspirateur/declarer_entretien.yaml` | `ÉTAPE 1 — Poste connu ?` → `stop:` « Poste d'entretien inconnu » | 218-220 |
| `10_scripts/aspirateur/declarer_entretien.yaml` | `ÉTAPE 2a — La mesure doit être NUMÉRIQUE` → `stop:` « Mesure d'entretien non évaluable » | 254-255 |
| `10_scripts/aspirateur/declarer_entretien.yaml` | `ÉTAPE 2b — La remise à zéro doit avoir un OBJET` → `stop:` « Compteur déjà au plafond » | 270-271 |
| `18_lovelace/includes/cartes/aspirateur/entretien_action.yaml` | bloc `🚦 CE QUE L'UI FAIT, ET NE FAIT PAS` : « ne masque aucun bouton et ne présume d'aucune échéance » | 22-26 |

**Clauses et invariants invoqués :**

- `ASP-INV-50` ([`09`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) §1) —
  « Toute demande qui n'aboutit pas produit un **motif lisible** […]. Un refus muet, un
  **bouton inerte** ou une commande avalée sans trace sont **non conformes**. »
- [`14`](../../../contrats/aspirateur/14_entretien.md) §7, *Un refus n'écrit rien* — les
  trois gardes d'entrée « s'arrêtent **avant toute pression** […] : le verdict conserve
  la dernière déclaration réellement achevée ».
- `ASP-INV-77`, `ASP-INV-78` — geste opérateur explicite, pression unique, aucune
  relance automatique : **respectés**.

**Scénario opérateur allégué** — [HYP] : l'opérateur presse *Filtre* sur la carte de
déclaration, confirme la boîte de dialogue, et le compteur du filtre est déjà à son
plafond — ou sa mesure est indisponible. Le script s'arrête à sa garde. Aucun helper
n'est écrit, le verdict d'entretien conserve la déclaration précédente, et la carte ne
change pas.

**Effet allégué.** Un bouton confirmé qui ne produit aucun retour visible. La trace Home
Assistant porte le motif ; l'interface, non.

**Qualification proposée par l'audit :** **tension entre deux clauses du même domaine**,
plutôt qu'un écart franc. Le chapitre `14` §7 **autorise explicitement** l'absence
d'écriture ; `ASP-INV-50` proscrit le bouton inerte. L'audit propose de lire cela comme
un **trou de portée** — le canal de motif lisible du chapitre `09` n'a jamais été étendu
au périmètre Maintenance — et **non** comme une violation d'une clause par une autre.

**Pourquoi la CI ne le voit pas.** [FAIT] `ASP-CI-40` à `ASP-CI-42` contrôlent la forme
du script, le champ fermé, les branches, la séquence et l'appel exclusif depuis l'écran.
Aucun ne porte sur la restitution d'un refus de déclaration.

**Interprétation contractuelle engagée.** [LECTURE] Le constat retient un **trou de
portée contractuelle allégué** — le canal de motif lisible du chapitre
[`09`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) n'ayant jamais été étendu
au périmètre Maintenance — et **non** une violation acquise d'`ASP-INV-50` par le
chapitre [`14`](../../../contrats/aspirateur/14_entretien.md). **La rédaction de ce
rapport n'étend pas `ASP-INV-50` au parcours Entretien** : sa portée reste la question
`C-8`, ouverte. Retenue autrement, le constat disparaît — le chapitre `14` §7 autorise
alors pleinement le silence (§7.2).

**Preuve terrain manquante.** Le scénario est [HYP] : aucune observation n'établit qu'une
pression sur un poste refusé ne produit **effectivement** aucune restitution visible.
Question `T-3` du §6.3.

**À contre-vérifier :**

1. `ASP-INV-50` a-t-il vocation à s'appliquer hors du périmètre mission ? Sa place au
   chapitre `09` — dont l'objet est le catalogue des refus **de mission** — plaide pour
   une portée bornée. **L'audit ne tranche pas.**
2. Si la restitution est due : par quel canal ? Un motif lisible d'entretien serait un
   **objet nouveau**, ce que le chapitre `14` interdit hors des rôles qu'il nomme.
3. Le rôle `‹issue_remise_a_zero›` peut-il porter un refus ? Le chapitre `14` §7 le
   décrit comme le verdict de la dernière déclaration **achevée**, et pose que les
   refus le laissent intact — l'y écrire contredirait le texte.
4. Le masquage conditionnel des boutons — écarté délibérément par l'en-tête de
   `entretien_action.yaml` — est-il l'alternative ? Elle rejoint alors la question 2 de
   `AUD-ASP-02` sur la forme de la symétrie UI.

**Absence d'arbitrage.** Les quatre voies sont mutuellement exclusives et engagent le
chapitre `14` ; aucune n'est recommandée ici.

---

## 5. Éléments ouverts mais **non qualifiés comme écarts**

> **Cette section n'est pas une liste de constats.** Elle recense ce qui est **déjà
> déclaré ouvert** par le dépôt lui-même. L'audit **ne requalifie aucun de ces
> éléments** et ne les promeut pas au §4.

| # | Élément | Source déclarante | Statut déclaré |
|---|---|---|---|
| 1 | **Validations terrain de `C42`** — effet réel de la pression sur le micrologiciel, valeur remontée après remise à zéro, délai de propagation, évolution de `M1`, disparition effective de la notification | `REGISTRE_CHANTIERS.md`, entrée `C42` | Ouvert (2026-08-30) — runtime, UI et CI livrés ; validation terrain due |
| 2 | **Étiquette `script:execution`** à appliquer au registre d'entités pour `script.aspirateur_declarer_entretien` | `REGISTRE_CHANTIERS.md`, `C42` ; en-tête de `declarer_entretien.yaml`, bloc `🏷️ ÉTIQUETTE` | Geste opérateur dans le registre d'entités, **non versionné** |
| 3 | **`CANAL_INDISPONIBLE`** — code du catalogue jamais écrit par un writer du domaine ; appartient à l'appelant qui observe l'erreur de transport | [`09`](../../../contrats/aspirateur/09_refus_et_diagnostics.md) §3 ; en-tête de `04_input_texts/aspirateur/mission.yaml` (« 2 codes du catalogue en sont ABSENTS ») ; en-tête de `lancer_mission.yaml` | **Documenté et assumé** |
| 4 | **`COMMANDE_REJETEE`** — non atteignable en L1 : distinguer un rejet d'une interruption d'exécution exigerait un observateur survivant à l'appel | mêmes sources | **Documenté et assumé** |
| 5 | **`QO-1`** — segments `2_17` (`Ext`) et `2_18` (`Chambre1`) de l'Annexe, hors référentiel V1 | [`13`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md) §3 | Question ouverte, non tranchée, non normée |
| 6 | **`QO-2`** — `mapStatus` comme confirmation protocolaire indépendante | `13` §3 ; `ASP-INV-30` | Question ouverte |
| 7 | **`QO-3`** — comportement multi-cartes | `13` §3 | Question ouverte |
| 8 | **`QO-4`** — saturation multi-cartes et stabilité des index de segments | `13` §3 ; `ASP-INV-9` | Question ouverte |
| 9 | **`QO-5`** — historisation | `13` §3 ; [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §6 | Question ouverte |
| 10 | **`QO-6`** — divergences de casse et de pluriel entre référentiels | `13` §3 ; `ASP-INV-8` | Question ouverte |
| 11 | **`ARB-1`** — acceptation d'un lancement hors base, non prouvée ; qualification au runtime exigée | `13` §2 ; [`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5.5 | Arbitrage rendu, **qualification terrain due** |
| 12 | **`ARB-2`** — session inachevée, robot inactif ⇒ refus ; alternative ouverte à révision **sur preuve terrain** | `13` §2 ; `07` §5.4 | Arbitrage rendu, révisable sur preuve |
| 13 | **`ARB-4`** — `×3` par déduction protocolaire, **non testée par Arsenal**, acceptée explicitement par l'opérateur | `13` §2 ; [`04`](../../../contrats/aspirateur/04_nombre_de_passages.md) §1 | Arbitrage rendu, niveau de preuve inférieur assumé |

> **Note de traçabilité — action mécanique due avant tout commit.** [FAIT] Ce rapport
> n'est **pas** référencé dans [`../../index.md`](../../index.md), section
> *Rapports → Aspirateur*. Cette absence est **détectée et refusée** par la gate
> `DOC-CI-3` (`scripts/docs_lint/docs_ci_orphan_report.py`, câblée sans
> `continue-on-error` dans `.github/workflows/docs.yml`), qui sort en erreur sur tout
> rapport orphelin :
>
> ```
> DOC-CI-3  00_documentation_arsenal/audits/01_rapports/aspirateur/audit_conformite_domaine_post_integration.md
>           rapport orphelin : non référencé dans 00_documentation_arsenal/audits/index.md
> ```
>
> **L'inscription à l'index est donc une obligation mécanique, non un choix.** Elle
> n'est pas faite dans cette passe, dont la consigne borne l'écriture à un fichier
> unique : elle est **due avant tout commit**, et relève d'un geste distinct. Inscrire
> un rapport à l'index de navigation **n'arbitre aucun de ses constats**.

---

## 6. Questions à soumettre à la contre-vérification

> Ces questions sont destinées à une **session indépendante**, qui doit pouvoir
> confirmer, nuancer ou infirmer chaque constat **sans reprendre les conclusions de ce
> rapport**. Le niveau de solvabilité proposé suit l'échelle L1–L5 de
> [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
> §1 ; **ces qualifications sont proposées, non arbitrées**.

### 6.1 Questions factuelles — vérifiables par lecture du dépôt (solvabilité **L1**, statique)

| # | Question | Rattachement |
|---|---|---|
| F-1 | L'attribut `mission_ouverte` de `sensor.aspirateur_etat_canonique` dérive-t-il exclusivement de `binary_sensor.roborock_q7_max_nettoyage` ? | `AUD-ASP-01` |
| F-2 | La garde d'entrée de `conduire_mission.yaml` porte-t-elle exclusivement sur `input_text.aspirateur_mission_verdict` ? | `AUD-ASP-01` |
| F-3 | Les conditions du bloc `4️⃣ CONDUITE` du panneau portent-elles **toutes** sur `sensor.aspirateur_etat_canonique`, et **aucune** sur le verdict ? | `AUD-ASP-01` |
| F-4 | Existe-t-il, dans `check_aspirateur_contracts.py`, un contrôle confrontant ces conditions Lovelace à `ASP-INV-87` ? | `AUD-ASP-01` |
| F-5 | Les cartes des deux profils Serpillière et le raccourci `rdc_serpilliere` portent-ils une `condition` quelconque ? | `AUD-ASP-02` |
| F-6 | Un objet du domaine projette-t-il l'état de `binary_sensor.roborock_q7_max_serpilliere_fixee` vers l'interface ? | `AUD-ASP-02` |
| F-7 | Le décompte « cinq » subsiste-t-il **exactement** dans les six emplacements listés au volet A, et le runtime porte-t-il **six** profils dans ses trois tables ? | `AUD-ASP-03` |
| F-8 | Le corps de `appliquer_raccourci.yaml` porte-t-il trois clés, et écrit-il quatre entités sur trois familles ? | `AUD-ASP-03` |
| F-9 | L'étape 0a de `lancer_mission.yaml` s'arrête-t-elle **avant** toute écriture, sur les neuf valeurs de `verdict_ouvert` ? | `AUD-ASP-04` |
| F-10 | Les deux blocs — en-tête de `notification_mission.yaml` et étape 0a — appartiennent-ils bien au même commit `89d05f9` ? | `AUD-ASP-04` |
| F-11 | Les trois gardes d'entrée de `declarer_entretien.yaml` s'arrêtent-elles sans écrire aucun helper ? | `AUD-ASP-05` |
| F-12 | Le checker passe-t-il **vert** à la révision auditée, sans modification ? | tous |

### 6.2 Questions contractuelles — relevant d'une lecture, puis d'un arbitrage

| # | Question | Rattachement |
|---|---|---|
| C-1 | Le chapitre `08` §1 / `ASP-INV-68` et le chapitre `15` §2 / `ASP-INV-87` définissent-ils **deux notions distinctes** sous un même nom, ou l'un prime-t-il sur l'autre ? | `AUD-ASP-01` |
| C-2 | `ASP-INV-87` (« aucun témoin natif ne l'établit ni ne s'y substitue ») s'applique-t-il **aussi** à la projection UI, ou seulement aux écrivains du verdict ? | `AUD-ASP-01` |
| C-3 | La garde de sens physique d'`ASP-INV-48` doit-elle se lire sur le verdict, ou sur l'état canonique ? | `AUD-ASP-01` |
| C-4 | `ASP-INV-13` (« lançables ») et `11` §2 (« disponible ») portent-ils la même exigence ? | `AUD-ASP-02` |
| C-5 | Une symétrie UI sur le prérequis matériel est-elle compatible avec `ASP-INV-16` ? | `AUD-ASP-02` |
| C-6 | Le décompte en toutes lettres d'un chapitre citant une table est-il normatif, ou rédactionnel ? | `AUD-ASP-03` |
| C-7 | Le réalignement d'un en-tête de fichier relève-t-il de `ASP-INV-52` / `ASP-INV-57`, ou d'une passe rédactionnelle ? | `AUD-ASP-03`, `AUD-ASP-04` |
| C-8 | `ASP-INV-50` porte-t-il au-delà du périmètre mission, jusqu'au périmètre Maintenance ? | `AUD-ASP-05` |
| C-9 | Si oui, par quel canal, sans créer un objet que le chapitre `14` n'autorise pas ? | `AUD-ASP-05` |

### 6.3 Questions terrain — non résolubles par lecture (solvabilité **L5** proposée : observation opérateur)

| # | Question | Rattachement | Pourquoi L5 |
|---|---|---|---|
| T-1 | Sur une mission Arsenal entrant en `returning_home`, la section Conduite disparaît-elle effectivement du panneau ? | `AUD-ASP-01` | Rendu Lovelace conditionnel — non historisé, non reconstructible |
| T-2 | Sur un cycle lancé depuis l'application Roborock, les trois boutons de conduite s'affichent-ils, et leur pression laisse-t-elle le motif lisible inchangé ? | `AUD-ASP-01` | idem, plus une pression réelle |
| T-3 | Une pression sur un poste d'entretien déjà au plafond produit-elle une restitution visible quelconque ? | `AUD-ASP-05` | idem |
| T-4 | Le témoin de session vaut-il `off` pendant le retour au dock sur l'instance courante ? | `AUD-ASP-01` | **Nuance L2** — potentiellement reconstructible si l'entité est inscrite au Recorder ; à qualifier contre le contrat Recorder avant d'exiger une observation |
| T-5 | Lorsque le prérequis serpillière est absent, **sous quelle forme** les deux profils Serpillière et le raccourci « RDC — serpillière complète » sont-ils rendus — présentés actifs, désactivés, ou masqués ? | `AUD-ASP-02` | Rendu Lovelace conditionnel — non historisé, non reconstructible |

> **Précaution d'emploi de ces questions.** `R-VERDICT-1` de
> [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
> §2 s'applique : une impossibilité de trancher T-1 à T-5 signifie **preuve absente**,
> jamais constat infirmé — ni constat confirmé.

---

## 7. Limites

### 7.1 Ce qui n'a **pas** été vérifié sur le terrain

**Rien ne l'a été.** [FAIT] Cette passe est intégralement statique : aucun accès à
l'instance Home Assistant, aucun appel de service, aucune lecture d'état réel, aucun
essai. En particulier :

- **aucun** des scénarios opérateur des cinq constats n'a été observé — tous sont [HYP] ;
- le rendu réel des cartes `conditional` de Lovelace n'a pas été constaté ;
- aucune valeur d'entité native Roborock n'a été lue à l'instant de l'audit ;
- le comportement de `stop:` dans un script appelé depuis une carte à confirmation n'a
  pas été observé — l'audit s'appuie sur la lecture du contrat (`ASP-INV-91` : le motif
  vit « dans la réponse au caller », journal et trace) et non sur une constatation.

### 7.2 Ce qui dépend d'une interprétation contractuelle

Trois constats reposent, en tout ou partie, sur une lecture qu'un arbitrage peut
infirmer — elles sont marquées [LECTURE] dans le corps :

| Constat | Lecture engagée | Si l'arbitrage la retient autrement |
|---|---|---|
| `AUD-ASP-01` | `ASP-INV-87` s'impose à la projection UI, et pas seulement aux écrivains du verdict | Le constat se réduit au scénario (b) — la perte du geste d'arrêt — voire disparaît |
| `AUD-ASP-02` | « disponible » (`11` §2) et « lançables » (`ASP-INV-13`) portent la même exigence | Le constat disparaît : seul le bouton de lancement serait concerné, et il est correctement gardé côté backend |
| `AUD-ASP-05` | `ASP-INV-50` porte au-delà du périmètre mission | Le constat disparaît : le chapitre `14` §7 autorise alors pleinement le silence |

`AUD-ASP-03` et `AUD-ASP-04` ne dépendent d'aucune interprétation quant à **l'existence**
de l'écart — les textes constatés sont factuels ; ils en dépendent quant à sa
**qualification** et à son véhicule de correction.

### 7.3 Ce qui ne peut être conclu de la seule lecture statique

- **Aucune non-conformité fonctionnelle** au sens de
  [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
  §2, verdict 3 : celui-ci exige une observation positive du comportement.
- **Aucune sévérité réelle** : la gêne opérateur alléguée n'a pas été mesurée, et la
  fréquence des scénarios est inconnue.
- **Aucune conclusion sur les fichiers non lus** du §1.1 — en particulier la logique
  interne de `supervision_mission.yaml` et de `notification_entretien.yaml`, et les
  auto-tests du checker.
- **Aucune preuve d'exhaustivité** : l'absence d'autres écarts n'est pas établie, elle
  n'a pas été recherchée sur le périmètre non lu.

### 7.4 Hypothèses de l'audit, explicitement posées

| # | Hypothèse | Effet si fausse |
|---|---|---|
| H-1 | Les faits terrain consignés par les chapitres `08` §3 et par l'en-tête de `lancer_mission.yaml` — témoin de session `off` en `returning_home`, trois reproductions — sont **exacts et toujours valides** sur l'appareil et la version en service | `AUD-ASP-01`, scénario (b), tombe |
| H-2 | Une carte Lovelace `conditional` dont la condition est fausse **n'est pas rendue** | `AUD-ASP-01`, scénario (b), tombe |
| H-3 | Un `stop:` dans un script appelé par `carte_action_standard` **ne produit aucune restitution visible** sur le panneau | `AUD-ASP-01` scénario (a) et `AUD-ASP-05` s'atténuent fortement |
| H-4 | `sensor.aspirateur_motif_lisible` est le **seul** canal de restitution d'un refus sur le panneau opérationnel | `AUD-ASP-01`, `AUD-ASP-05` s'atténuent |
| H-5 | Une mission lancée depuis l'application Roborock porte bien `sensor.roborock_q7_max_etat` en classe A et le témoin de session à `on` | `AUD-ASP-01`, scénario (a), tombe |
| H-6 | Le périmètre de balayage du checker relevé au §1.3 est complet — aucun contrôle non lu ne couvre l'un des cinq constats | les mentions « pourquoi la CI ne le voit pas » sont à réviser constat par constat |

> **H-2 et H-3 sont des hypothèses sur le comportement de Home Assistant**, non sur le
> dépôt. Elles n'ont **pas** été établies par lecture du code source de la plateforme
> dans cette passe — à la différence de plusieurs faits que le domaine consigne, eux,
> avec leur référence de version.

---

## Renvois

- Contrat du domaine : [`../../../contrats/aspirateur/README.md`](../../../contrats/aspirateur/README.md)
- Audit factuel antérieur : [`audit_faisabilite_roborock_q7_max.md`](audit_faisabilite_roborock_q7_max.md)
- Relevé d'attestation Maintenance : [`releve_entites_entretien.md`](releve_entites_entretien.md)
- Cadrage ratifié `D-44` : [`../../02_conception/aspirateur/cadrage_l2_maintenance_ui/README.md`](../../02_conception/aspirateur/cadrage_l2_maintenance_ui/README.md)
- Découpage en lots : [`../../02_conception/aspirateur/cadrage_l2_maintenance_ui/10_LOTS.md`](../../02_conception/aspirateur/cadrage_l2_maintenance_ui/10_LOTS.md)
- Registre des chantiers (entrée `C42`) : [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Doctrine de solvabilité probatoire : [`../../../architecture/03_doctrines/solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
- Doctrine des en-têtes de fichiers : [`../../../architecture/03_doctrines/entetes_fichiers.md`](../../../architecture/03_doctrines/entetes_fichiers.md)
- Doctrine de commandabilité : [`../../../architecture/03_doctrines/commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)
- Index des audits : [`../../index.md`](../../index.md)
