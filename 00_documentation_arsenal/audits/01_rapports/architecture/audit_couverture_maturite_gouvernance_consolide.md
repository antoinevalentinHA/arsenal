# Audit global — couverture, maturité et gouvernance (version consolidée)

**Périmètre** : dépôt `antoinevalentinHA/arsenal`, ensemble des couches d'implémentation et de gouvernance.
**Base d'analyse** : clone local, HEAD `899c172` (2026-06-04), branche par défaut.
**Nature** : audit d'architecture et de gouvernance en lecture seule. Descriptif. **Aucun plan d'action, aucune correction.**
**Statut** : version **consolidée** d'un audit de travail antérieur. Elle intègre des corrections factuelles vérifiées au HEAD courant et neutralise les qualificatifs non démontrés (voir §0). En cas de divergence, **cette version prévaut**.
**Méthode** : comptage par couche/domaine (`os.walk`), mapping explicite des 65 workflows et 62 validateurs, scan du cycle d'audit, lecture des doctrines `03_doctrines/`, exécution de `tools/arsenal_ci/tests/` (136 tests passés). Les 62 validateurs `scripts/arsenal_contracts/` **n'ont pas été exécutés**.

---

## 0. Corrections intégrées par rapport à l'audit de travail

Tracées explicitement, par souci d'honnêteté documentaire.

1. **Retrait d'une affirmation devenue fausse.** Un audit antérieur (`audits/01_rapports/documentation/audit_structure_00_documentation_arsenal.md`) signalait que `architecture/voiture.md` était une copie binaire de `aeration_recommandation.md`. **Vérification au HEAD `899c172` : md5 distincts (`4d20f29…` ≠ `8b139b9…`), et l'en-tête de `voiture.md` lit bien « ARCHITECTURE — VOITURE — Audi A3 e-tron ».** Le défaut n'existe plus ; toute mention en est retirée.
2. **Reclassement du poêle.** `poele` n'est pas un domaine nu. Il est **contractualisé comme entrée du chauffage** : `contrats/chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_en_fonction.md` et `signature_thermique_poele.md`. Il relève de la catégorie « gouverné par un autre domaine » (§2).
3. **Neutralisation du vocabulaire « dette » / « incomplet ».** La doctrine `03_doctrines/nommage_entites.md` est **normative pour les noms d'entités, pas pour les noms de dossiers**. Les divergences de nommage de dossiers ne sont donc confrontables à aucune règle interne : elles sont décrites comme *hétérogénéités non tranchées*, pas comme dette. Les dossiers `.gitkeep` vides sont décrits comme *squelettes provisionnés non remplis*, lecture neutre, sans présomption d'abandon.
4. **Distinction des statuts de gouvernance** (§1.2) : un contrat sans CI **reste** une gouvernance ; il ne doit pas être agrégé avec l'absence de gouvernance.

---

## 1. Cadre d'interprétation

### 1.1 Barèmes

Les comptages (§3) sont des **faits**. Les niveaux sont des **interprétations** dérivées d'un barème explicite.

- **Couverture** = largeur d'implémentation (perception, décision, exécution, helpers, UI). `Fort` ≥4 couches · `Moyen` 2–3 · `Faible` 1 · `Embryonnaire` entités éparses.
- **Maturité** = signaux d'itération/stabilisation (contrats, amendements, audits, clôtures, tests, historique). `Fort`/`Moyen`/`Faible`/`Embryonnaire`.
- **Gouvernance** = artefacts normatifs opposables + vérification automatisée. `Fort` (contrat + CI/validateur ou moteur dédié) · `Moyen` (contrat **ou** CI) · `Faible` (mention partielle) · `Absent`.

**Le barème ne présume pas qu'un domaine doive atteindre le maximum.** Un domaine peut être délibérément compact ou volontairement passif (perception pure). Un faible niveau **décrit l'ampleur des artefacts**, il ne porte aucun jugement sur l'adéquation au besoin.

### 1.2 Taxonomie des statuts de gouvernance (centrale dans cette version)

Pour éviter d'agréger des situations distinctes, chaque domaine est rangé dans **une** catégorie :

- **(A) Non documenté** — aucun contrat (dossier ou racine), aucune CI. *Vérifié : 0 occurrence dans `contrats/`.*
- **(B) Contractualisé, non validé en CI** — contrat présent, aucun workflow/validateur. *Gouverné, non automatisé.*
- **(C) Gouverné par un autre domaine** — pas de gouvernance propre ; entités contractualisées **à l'intérieur** d'un autre domaine.
- **(D) Gouvernance distribuée** — gouvernance propre **et** implémentation/contrats répartis sur plusieurs domaines ou plusieurs concepts transverses.
- **(E) Domaine autonome gouverné** — contrat(s) + CI/validateur (ou moteur) au sein d'un périmètre propre.

---

## 2. Classement des domaines par statut de gouvernance

> Faits (présence/absence d'artefacts, vérifiés). La catégorie est une lecture, pas un score.

| Catégorie | Domaines | Fait justificatif |
|---|---|---|
| **(A) Non documenté** | `reveils`, `electromenager`, `babyphone`, `statistiques` | 0 contrat (vérifié) ; `statistiques` = 12 sensors de perception pure, sans couche décision |
| **(B) Contractualisé, non validé CI** | `sante` (cardio_nuit, sommeil), `imprimerie` (bruit Bobst/Komori/média), `pannes` (internet, secteur), `bluetti`, `mouvements` | contrat présent, **aucun** workflow/validateur |
| **(C) Gouverné par un autre domaine** | `poele` (entrée de blocage du chauffage) | `contrats/chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_*.md` |
| **(D) Gouvernance distribuée** | `vacances` (chauffage + ecs), `system` (contrats transverses), `meteo` (gouvernance par axe), `presence` (autorité transverse), `modes` (babysitting/visite/simulation_presence) | gouvernance réelle non portée par un dossier homonyme |
| **(E) Autonome gouverné** | `chauffage`, `ecs`, `climatisation`, `aération`, `alarme`, `eclairage`, `boiler`, `deshumidificateur`, `vmc`, `ouvertures`, `bouclage`, `volets`, `voiture` | contrat + CI/validateur (ou moteur dédié) propres |

Cas particulier `boutons` : 2 références en contrat (non nul) mais pas de contrat dédié ni de CI — entre (A) et (B), signalé comme marginal. Cas `cumulus`/`cumulus_studio` : un contrat racine `cumulus_petite_maison.md`, pas de CI → (B), avec hétérogénéité de nommage signalée (§5).

---

## 3. Matrice de couverture (faits)

`auto`=`11_automations/`, `scr`=`10_scripts/`, `tmpl`=`12_template_sensors/`, `help`=helpers `03_`→`09_`, `contr`=contrats (dossier **ou** fichier racine **ou** intégrés à un autre domaine), `aud`=rapports+arbitrages+contre-expertises, `chan`=chantiers (`04_chantiers/`+`changelog/chantiers/`), `clot`=clôtures, `CI`=workflows, `val`=validateurs.

| Domaine | Cat. | auto | scr | tmpl | help | contr | aud | chan | clot | CI | val |
|---|:--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| chauffage | E | 19 | 8 | 39 | 35 | 51 | 3 | 4 | 1 | moteur dédié | — |
| ecs | E | 28 | 17 | 14 | 42 | 28 | 2 | 1 | 0 | 3 | 3 |
| climatisation | E | 20 | 5 | 34 | 25 | 38 | 1 | 8 | 0 | 2 | 2 |
| aération (+blocage) | E | 7 | 9 | 7 | 29 | 37+1 | 0 | 0 | 0 | 8 | 8 |
| meteo | D | 27 | 4 | 61 | 30 | 15 +`validation.md` | 1 | 0 | 0 | ~7 par axe | par axe |
| alarme | E | 14 | 9 | 5 | 11 | 15 | 1 | 6 | 4 | 1 | 1 |
| eclairage | E | 24 | 5 | 11 | 32 | 6 | 0 | 0 | 0 | 3 | 3 |
| system | D | 18 | 9 | 54 | 29 | transverses | 0 | 0 | 0 | éclatés | éclatés |
| ouvertures | E | 11 | 7 | 16 | 9 | 3 | 0 | 0 | 0 | 1 | 1 |
| voiture | E | 3 | 0 | 21 | 2 | 1 (racine) | 1 | 0 | 0 | 1 | 1 |
| deshumidificateur | E | 8 | 2 | 5 | 6 | 2 | 0 | 0 | 0 | 3 | 3 |
| boiler | E | 0 | 0 | 14 | 1 | 7 | 0 | 0 | 0 | 1 | 1 |
| presence | D | 8 | 0 | 8 | 9 | 1 (racine) | 0 | 0 | 0 | 1 | 1 |
| vmc | E | 4 | 2 | 5 | 4 | 1 (racine) | 0 | 0 | 0 | 1 | 1 |
| bouclage | E | 5 | 1 | 2 | 4 | 1 (racine) | 1 | 0 | 0 | 1 | 1 |
| modes | D | 13 | 0 | 4 | 7 | via babysitting/visite | 0 | 0 | 0 | 2 (indirect) | 2 |
| volets | E | 0 | 6 | 6 | 1 | 1 (volets_pluie) | 0 | 0 | 0 | 1 | 1 |
| imprimerie | B | 5 | 2 | 14 | 7 | 3 | 0 | 0 | 0 | 0 | 0 |
| sante | B | 4 | 1 | 8 | 8 | 2 | 0 | 0 | 0 | 0 | 0 |
| pannes (impl. `panne`) | B | 7 | 0 | 0 | 1 | 9 | 0 | 0 | 0 | 0 | 0 |
| poele | C | 6 | 0 | 2 | 4 | (dans chauffage) | — | — | — | (via chauffage) | — |
| vacances | D | 0 | 0 | 0 | 1 | 1 racine + chauffage/ecs | 1 | 2 | 2 | 1 | 1 |
| bluetti | B | 0 | 0 | 7 | 0 | 1 (racine) | 0 | 0 | 0 | 0 | 0 |
| mouvements | B | 0 | 0 | 3 | 0 | 1 (racine) | 0 | 0 | 0 | 0 | 0 |
| statistiques | A | 0 | 0 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| reveils | A | 6 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| electromenager | A | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| babyphone | A | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| boutons | A/B | 3 | 0 | 0 | 1 | 2 réf. | 0 | 0 | 0 | 0 | 0 |
| couleurs (UI) | E | 0 | 0 | 24 | 0 | via `ui/` | 0 | 0 | 0 | 2 | 2 |

**Gouvernance transverse** (27 contrats mono-fichier racine + validateurs, pattern **1 contrat ↔ 1 validateur ↔ 1 workflow**) : `batteries`, `bssid`, `notifications`, `redondance`, `simulation_presence`, `parametres_invalides`, `ups_arret_ha`, `mobile_high_accuracy`, `visite`, `babysitting`, `zones`, `arsenal_self`, `arsenal_nas`, `switchbot_transactionnel`, `garage_toggle`, `homekit_diagnostic`, `ping_lan_synthese`, `energie`, `ressources_lovelace`, `consolidation`, `stabilisation`, `recorder`, `counters`, `timers`, `input_*`, `01_customize`, `02_groups`, `19_button_card_templates`, `lovelace_includes`, `ui_couleurs`, `ui_runtime_colors`.

**Deux exceptions au pattern dominant** (faits) : `chauffage` est validé par le moteur dédié `tools/arsenal_ci/` (et non par un `check_chauffage_contracts.py`) ; `meteo` n'a pas de validateur unique mais des validateurs **par axe** (palmarès chaud/froid, jardin, HR, diagnostic_netatmo).

---

## 4. Constats robustes (haute confiance)

Constats inchangés car étayés par des faits reproductibles et peu sensibles aux biais identifiés au §6.

- **Cœur thermique + sécurité = noyau autonome gouverné.** `chauffage`, `ecs`, `climatisation`, `aération`, `alarme` cumulent contrat dédié + CI/validateur (ou moteur) + présence sur ≥4 couches. *Faits : §3.*
- **Pattern de gouvernance dominant 1↔1↔1** (62 contrats ↔ 62 validateurs ↔ 62 workflows), avec deux exceptions assumées (chauffage, meteo). *Fait reproductible.*
- **Cycle d'audit le plus abouti : `alarme`** (rapport + 2 contre-expertises + chantiers CH1/CH2 + 4 clôtures). *Fait : `audits/05_clotures/alarme/`.*
- **Validation la plus sophistiquée : `chauffage`** (moteur d'analyse de topologie d'appel, 136 tests passés). *Fait : exécution.*
- **Structures de contrats homogènes/exemplaires : `climatisation`** (`capteurs/` à patron répété), `aeration_blocage_chauffage` (machine d'états m0→m6), `chauffage` (amendements en fichiers séparés). *Lecture convergente avec `audit_structure_00_documentation_arsenal.md` §2.3.*
- **Existence réelle d'une catégorie (A) « non documenté »** : `reveils`, `electromenager`, `babyphone`, `statistiques` — 0 occurrence en contrat, vérifiée. C'est, au regard de la « règle d'or » du dépôt, le seul constat de non-couverture **démontré**.

---

## 5. Observations descriptives (confiance moyenne, formulation neutre)

- **Hétérogénéité de nommage de dossiers** (non confrontée à une règle interne, la doctrine de nommage ne portant que sur les entités) : `aeration` / `aeration_blocage_chauffage` ; `panne` / `pannes` ; `cumulus` / `cumulus_studio` / `cumulus_petite_maison`. **Interprétation alternative explicitement retenue** : ces écarts peuvent encoder une distinction couche-action vs couche-contrat, donc être intentionnels. Aucune qualification de « dette ».
- **Squelettes de cycle d'audit provisionnés** : `audits/{02_constats,03_plans_action,04_chantiers,05_clotures}/voiture/` ne contiennent que des `.gitkeep`. Lecture neutre : structure pré-instanciée non remplie ; ni « abandon » ni « inachèvement » ne sont démontrés.
- **Gouvernance distribuée vs absence** : `system` (54 sensors) n'a pas de contrat homonyme mais est couvert par ≥7 contrats transverses ; `meteo` est gouvernée par axe ; `vacances` est gouvernée intégralement alors que son implémentation vit dans `chauffage`/`ecs`. Ces situations relèvent de (D), **pas** d'un déficit de gouvernance.
- **Couche exécution hors dépôt** : `boiler` (perception+décision dans le dépôt ; exécution documentée dans `outils_externes/boiler_pi/`). Comportement non observable ici.

---

## 6. Robustesse méthodologique et limites renforcées

Cette section est volontairement étendue : elle conditionne la lecture des §3–§5.

**Biais structurels des barèmes** (à charge de l'audit lui-même) :
- **Biais de centralisation.** Les trois barèmes récompensent la concentration d'artefacts dans un dossier homonyme. Ils désavantagent mécaniquement les concepts transverses (vacances), les domaines compacts (vmc) et la gouvernance par axe (meteo). La catégorisation (A)–(E) du §1.2 a été introduite pour neutraliser ce biais, mais le comptage du §3 le conserve partiellement.
- **Biais de nomenclature.** Le rattachement CI↔domaine repose sur les noms de fichiers. Corrigé à la main pour meteo, system, aération, vacances, poele ; un résidu reste possible ailleurs.
- **Maturité = activité, pas qualité.** Le nombre d'audits/chantiers/clôtures mesure l'**intensité du travail de gouvernance**, non la **fiabilité du résultat**. Un domaine très « mature » à ce compte peut aussi être un domaine ayant beaucoup dérivé. Inversement, un domaine stable et correct peut n'avoir produit aucun audit.
- **Gouvernance = outillage, pas efficacité.** « Bien gouverné » signifie ici « doté d'un contrat et d'une CI », non « dont la CI capture effectivement les défauts ». Les 62 validateurs n'ont pas été exécutés ni inspectés en contenu ; seul le moteur chauffage l'a été (136 tests).
- **Volume ≠ maturité, simplicité ≠ immaturité.** Un faible volume (catégorie A) **n'implique pas** un domaine bâclé : il peut être volontairement minimal ou passif. L'audit ne dispose d'aucun élément pour distinguer « simple par choix » de « inachevé ».

**Limites de portée** :
- Audit **statique**, à `HEAD 899c172`, d'un dépôt à évolution quotidienne (v15.9). Toute conclusion se périme.
- La satisfaction des contrats par l'implémentation **n'est pas prouvée** (rôle des validateurs, non exécutés sauf chauffage).
- Les satellites (`boiler_pi`, NAS) sont attestés par documentation seule ; leur code et leur runtime sont hors champ.
- `custom_components/` (audiconnect, bluetti_bt, fujitsu_airstage, hacs) et `www/` sont **tiers** : leur présence ne reflète pas la maturité du domaine Arsenal correspondant.
- Aucune correction ni recommandation n'est formulée (hors mandat).

**Ce que cet audit peut affirmer / ne peut pas affirmer** :
- *Peut* : quels artefacts existent, où, en quelle quantité, et selon quel pattern ils s'organisent.
- *Ne peut pas* : si un domaine « fonctionne » correctement, si une CI est efficace, si un domaine simple est suffisant pour son besoin, ou si une hétérogénéité de nommage est voulue.

---

## 7. Synthèse transversale (prudente)

- **Mieux couverts** (largeur d'implémentation, fait) : chauffage, ecs, climatisation, meteo, puis system et eclairage.
- **Plus matures** (intensité de gouvernance, proxy) : alarme, ecs, chauffage, climatisation, vacances — *sous réserve que « mature » désigne l'activité de gouvernance, pas la fiabilité (§6)*.
- **Mieux gouvernés** (outillage présent, proxy) : chauffage, aération, ecs, climatisation, alarme, deshumidificateur, boiler.
- **Couverture la plus faible** : babyphone, mouvements, boutons, cumulus, statistiques.
- **Seule non-couverture documentée** (cat. A) : reveils, electromenager, babyphone, statistiques.
- **Gouvernés non automatisés** (cat. B, à ne pas confondre avec « non gouvernés ») : sante, imprimerie, pannes, bluetti, mouvements.
- **Structures exemplaires** : climatisation, chauffage, aeration_blocage_chauffage, alarme.
- **Principal déséquilibre robuste** : hétérogénéité du **dispositif de validation** — un pattern 1↔1↔1 dominant, deux exceptions explicites (moteur chauffage ; meteo par axe). *C'est un fait, non un défaut.*
- **Principal angle mort** : tout est statique ; l'existence d'un dispositif de gouvernance ne prouve ni son exécution ni son efficacité.

> Les anciens constats « gouvernance ≫ implémentation », « implémentation ≫ gouvernance », « dette de nommage » et « structures incomplètes » ne sont **pas** repris comme tels : ils confondaient soit activité et qualité, soit gouvernance distribuée et absence, soit hétérogénéité non tranchée et dette. Ils sont remplacés par la taxonomie (A)–(E) et les observations neutres du §5.

---

*Fin de l'audit consolidé. Document descriptif, lecture seule, sans plan d'action.*
*Archivage suggéré (non appliqué) : `00_documentation_arsenal/audits/01_rapports/` sous un sujet méta (p. ex. `transverse/`), parallèlement à `documentation/`.*
