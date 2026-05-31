# Revue critique — Audit Arsenal « Mode maison Vacances »

> Type : revue critique contradictoire d'un rapport d'audit — livrable d'archivage
> Objet revu : `00_documentation_arsenal/audits/01_rapports/vacances/audit_vacances_rapport_final.md`
> Portée : les 13 constats du rapport (1 absence de critique, 5 importants, 4 mineurs, 3 améliorations) + ses points conformes et sa cartographie
> Mode : lecture seule — aucun runtime, contrat ou UI modifié ; aucun fichier du dépôt créé ou modifié ; `git status` propre à l'ouverture et à la fermeture
> Référence dépôt : branche `main`, HEAD `b542bda` (le runtime audité est identique à `c20d9ee`, référence du rapport d'origine — voir §2)
> Posture : contradictoire. La revue ne cherche pas à défendre le rapport ; elle cherche à le casser, puis consigne ce qui résiste.

---

## Note de périmètre et de méthode

Cette revue n'est **pas** un nouvel audit du domaine Vacances. C'est une **contre-expertise du rapport d'audit existant** : pour chaque constat, elle vérifie l'exactitude factuelle dans le dépôt, l'adéquation entre la preuve avancée et la conclusion tirée, les hypothèses non démontrées, les faux positifs et les erreurs de raisonnement éventuels, puis statue.

Procédure suivie, strictement en lecture seule :

1. Clone local du dépôt, `git status` initial → *working tree clean*.
2. Lecture du rapport d'audit à réviser, puis du contrat normatif `vacances.md` (v1.4.0) comme référence d'intention.
3. Confrontation de chaque constat aux fichiers réellement présents (capteurs, automations, scripts, cartes UI, contrôleur CI, contrats consommateurs).
4. Exécution **en lecture seule** du contrôleur `scripts/arsenal_contracts/check_vacances_contracts.py` pour observer son verdict réel.
5. Pour les constats reposant sur une hypothèse historique, recours à l'historique `git` (recherche `git log -S`), sans aucune écriture.
6. `git status` final → *working tree clean*, `git diff` vide, aucun fichier non suivi.

**Note de version.** Le rapport d'origine déclare avoir été produit sur `HEAD c20d9ee`. Le HEAD courant de `main` est `b542bda` ; le seul commit intercalaire est l'ajout du rapport lui-même. Le **code runtime est strictement identique** entre les deux états : la revue est donc pleinement comparable au périmètre du rapport.

**Limite assumée.** Les comportements dynamiques de Home Assistant (ordre d'exécution de deux automations sur un même événement, instant de recalcul des template sensors, sémantique exacte d'attributs runtime) ne sont pas tranchables depuis le seul dépôt. Là où une conclusion en dépend, la revue le signale explicitement plutôt que de trancher.

---

## Légende

### Statut de revue

| Statut | Signification |
|--------|---------------|
| **VALIDÉ** | Le constat est factuellement exact ; la preuve démontre la conclusion ; aucune objection substantielle. |
| **VALIDÉ AVEC RÉSERVE** | Les faits tiennent, mais la conclusion est conditionnée (sémantique runtime, interprétation d'un texte ambigu, ou poids/portée à relativiser). |
| **NON DÉMONTRÉ** | Le dépôt ne suffit pas à établir le constat. *(Aucun constat n'est classé ainsi.)* |
| **INFIRMÉ** | Un élément du constat est contredit par le dépôt. *(Un seul sous-élément l'est : l'étiologie de VAC-IMP-4.)* |

### Niveau de confiance final

| Niveau | Signification |
|--------|---------------|
| **Élevé** | Fait reproductible, preuve directe, conclusion non remise en cause par la revue. |
| **Moyen** | Fait établi, mais conclusion suspendue à une sémantique runtime ou à une interprétation. |
| **Réservé** | Le fait tient, mais le constat *tel qu'énoncé* (sa cause, son poids ou sa portée) est partiellement remis en cause. |

> Les **gravités d'origine** du rapport (🔴 critique · 🟠 important · 🟡 mineur · 🟢 amélioration) sont **reproduites telles quelles** et **non modifiées** par cette revue. Le statut de revue et le niveau de confiance sont des axes distincts, ajoutés sans toucher à la gravité attribuée par l'audit.

---

## Rappel du domaine (pour lecteur n'ayant pas vu l'audit)

Le domaine **Vacances** gouverne un contexte global d'absence prolongée, structuré par le contrat `vacances.md` (v1.4.0) en **cinq niveaux séparés** :

1. **Paramétrage** — helpers de configuration (`input_datetime.debut_vacances`/`fin_vacances`, `input_boolean.mode_vacances_auto`, `input_boolean.vacances_demande_manuel`).
2. **Support temporel** — `input_boolean.vacances_fenetre_active`, matérialisé par un orchestrateur dédié.
3. **Demande** (calcul) — `binary_sensor.vacances_planifiees_actives`, puis `binary_sensor.vacances_demandees` (demande consolidée).
4. **Effectivité** (calcul) — `binary_sensor.vacances_actives` (vérité terrain) et `sensor.vacances_raison` (6 états explicatifs).
5. **Application** (action) — projection dans `input_select.mode_maison` (automations `activation`/`desactivation`), application/fin de contexte (`application_debut`/`application_fin`), restauration (`normal.yaml`), support ECS (`start_timer_ecs_desinfection` + `timer.vacances_longues_ecs`).

Le contrat pose notamment : séparation stricte **demande ↔ effectivité**, interdiction de `now()` dans les templates du domaine, caractère *boot-proof*, et **consommation par couche** (chaque sous-système lit la couche qui lui est assignée — §10).

Le rapport d'audit conclut que **le noyau métier est sain** et que la dette se concentre **aux frontières de consommation aval** (chauffage, ECS) et **dans les outils de surveillance** (CI, cartes UI). La présente revue teste cette conclusion constat par constat.

---

## Synthèse

| ID | Constat (résumé) | Gravité d'origine | Statut de revue | Confiance |
|----|------------------|:-----------------:|-----------------|:---------:|
| Conformes §5.1 | Noyau fidèle au contrat (5 niveaux, séparation, boot-proof, échec prudent) | — | **VALIDÉ** | Élevé |
| Aucun critique | Pas de défaut critique ni de référence cassée dans le noyau | 🔴 (absent) | **VALIDÉ** | Élevé |
| **VAC-IMP-1** | Chauffage arbitre sur la projection `mode_maison`, pas sur `vacances_actives` | 🟠 | **VALIDÉ** (faits) | Élevé (faits) · cadrage à nuancer |
| **VAC-IMP-2** | Blocage ECS posé sur l'effectivité, levé sur la projection (asymétrie) | 🟠 | **VALIDÉ** | Élevé |
| **VAC-IMP-3** | Le contrôleur CI ne scrute pas les templates métier du domaine | 🟠 | **VALIDÉ** | Élevé · portée préventive |
| **VAC-IMP-4** | Cartes UI désalignées (clé morte + états manquants) | 🟠 | **VALIDÉ AVEC RÉSERVE** + **INFIRMÉ** (étiologie) | Élevé (fonctionnel) · étiologie infirmée |
| **VAC-IMP-5** | Désinfection retour : dépendance d'ordonnancement non garantie | 🟠 | **VALIDÉ AVEC RÉSERVE** | Moyen |
| **VAC-MIN-1** | Attribut `fenetre_inversee` contractuel absent de l'implémentation | 🟡 | **VALIDÉ** | Élevé |
| **VAC-MIN-2** | `mode_vaisselle` éteint à l'entrée, jamais restauré à la sortie | 🟡 | **VALIDÉ** | Élevé |
| **VAC-MIN-3** | Timer ECS piloté sur `mode_maison` vs documentation « durée continue » | 🟡 | **VALIDÉ AVEC RÉSERVE** | Moyen |
| **VAC-MIN-4** | `delay` de stabilisation placé après la garde au boot | 🟡 | **VALIDÉ AVEC RÉSERVE** | Réservé (risque surévalué) |
| **VAC-AME-1** | Contrôleur reposant sur des correspondances de sous-chaînes | 🟢 | **VALIDÉ** | Élevé |
| **VAC-AME-2** | Hétérogénéité de syntaxe `service:` vs `action:` | 🟢 | **VALIDÉ** | Élevé |
| **VAC-AME-3** | Vocabulaire de couche divergent entre contrats (80 ↔ §10) | 🟢 | **VALIDÉ** | Élevé |

---

## Revue détaillée par constat

### Points conformes (§5.1) — **VALIDÉ** · confiance Élevé

**Vérifié.** Les 4 capteurs métier ne lisent jamais `mode_maison` (`vacances_actives` = `vacances_demandees ∧ presence off ∧ visite off` ; `vacances_demandees` = manuel ∨ planifiées). L'orchestrateur possède `homeassistant: start` inconditionnel, confine `now()` à l'action sur déclenchement explicite, et applique une borne de fin exclusive (`maintenant_ts < fin_ts`). L'intégrité paramétrique retombe en `true` (invalide) sur indisponibilité ou `fin ≤ debut`. `vacances_raison` couvre les 6 états contractuels.

**Tentative de cassure (infructueuse).** Recherche d'un écrivain caché de `mode_maison` : `decision_centrale.yaml` est un **faux positif** — ses `select_option` ciblent `input_select.chauffage_mode_session`, il ne fait que *lire* `mode_maison`. Les seuls écrivains restent `activation`/`desactivation`. La claim « seuls writers légitimes » tient.

### Aucun constat critique — **VALIDÉ** · confiance Élevé

Aucune perte de donnée, boucle bloquante ou référence cassée détectée dans le noyau. Conforme à la lecture de revue.

---

### VAC-IMP-1 — Chauffage sur projection `mode_maison` (🟠) — **VALIDÉ** (faits) · confiance Élevé sur les faits ; cadrage normatif à nuancer

**Énoncé d'origine.** La Décision Centrale chauffage sélectionne le régime `reduced`/`comfort` sur `mode_maison = Vacances` (projection), alors que le contrat Vacances §10 assigne `binary_sensor.vacances_actives` à la « logique d'absence effective : ECS, chauffage, présence ». Contradiction inter-contrats : `80_table_decision_canonique.md` vs Vacances §10.

**Vérifié et confirmé.** `decision_centrale.yaml` arbitre `comfort`/`reduced` sur `is_state('input_select.mode_maison','Vacances')` ; `vacances_actives` n'y est jamais lu (uniquement par le pré-confort). Le contrat 66 utilise bien `vacances_actives` et interdit explicitement `mode_maison`. **Impact comportemental démontré** : la branche `mode_maison==Vacances` précède la branche `presence_famille_unifiee==on` ; donc demande active + famille présente → `reduced` imposé à des occupants présents.

**Nuance de revue.** La « contradiction inter-contrats » est exacte **à la lettre** (le contrat 80 impose l'arbitrage sur `mode_maison`, « quelle que soit l'activité de `vacances_actives` » ; §10 nomme « chauffage » dans la ligne `vacances_actives uniquement »). En revanche le terme **« dérive »** est contestable : le contrat 80 est une **décision normative explicite et assumée**, pas un glissement silencieux. La divergence est donc **documentaire et non réconciliée** (ce que le rapport loge lui-même en VAC-AME-3), plus qu'une « violation » univoque. La gravité 🟠 reste défendable car le comportement observable est réel ; un override manuel (`mode_confort_chauffage`) offre une échappatoire qui tempère légèrement.

---

### VAC-IMP-2 — Asymétrie du blocage ECS (🟠) — **VALIDÉ** · confiance Élevé

**Énoncé d'origine.** `ecs_blocage_planifiee` est posé sur la couche effectivité (`application_debut`, sur `vacances_actives→on`) mais levé uniquement par la couche projection (`normal.yaml`, sur `mode_maison→Normal`). `application_fin` ne touche pas l'ECS : au retour d'un occupant pendant une demande active, l'eau chaude reste planifiée-bloquée alors que la maison est occupée.

**Vérifié et confirmé.** `application_debut` pose `ecs_blocage_planifiee=on` ; `normal.yaml` est le seul à le lever ; `application_fin` ne touche pas l'ECS. **Scénario atteignable** : occupant revient → `presence=on` → `vacances_actives=off`, mais `vacances_demandees` reste `on` → `desactivation` ne se déclenche pas → `mode_maison` reste `Vacances` ; `application_fin` retire la consigne réduite et laisse `ecs_blocage_planifiee=on`. **Consommateur confirmé** : `veille_chauffe_ponctuelle.yaml` exige `ecs_blocage_planifiee=off` en condition — c'est l'unique lecteur-condition de ce booléen. La preuve démontre la conclusion.

---

### VAC-IMP-3 — CI aveugle aux templates métier (🟠) — **VALIDÉ** · confiance Élevé · portée préventive

**Énoncé d'origine.** `VACANCES_TEMPLATE_PATHS` vise `12_template_sensors/vacances`, répertoire inexistant ; les capteurs métier sont dans `12_template_sensors/modes/`. Le TEST 2 (interdiction `now()`/`today_at`) ne couvre donc que `integrite_reglages/vacances.yaml` ; les 4 capteurs métier ne sont jamais analysés. Verdict observé : `✅ CONTRAT VACANCES CONFORME`, exit 0.

**Vérifié et confirmé.** Le répertoire cible est inexistant ; le filtre de portée ne renvoie `True` que pour ce chemin fantôme ou le fichier d'intégrité ; TEST 2 ne scrute que ce dernier. **Exécution reproduite** : `✅ CONTRAT VACANCES CONFORME`, exit 0.

**Nuance de revue.** Le garde-fou est inopérant, mais **aucune violation actuelle n'existe** (les 4 capteurs n'emploient ni `now()` ni `today_at`). L'impact est donc **purement préventif/latent** : un écart futur sur la couche calculée ne serait pas détecté. La gravité 🟠 porte sur l'*assurance de conformité*, pas sur un défaut runtime présent — à lire comme tel.

---

### VAC-IMP-4 — Cartes de diagnostic désalignées (🟠) — **VALIDÉ AVEC RÉSERVE** (fonctionnel) + **INFIRMÉ** (étiologie) · confiance Élevé sur le fonctionnel

**Énoncé d'origine.** Les cartes mappent une raison `mode_maison_normal` que `sensor.vacances_raison` n'émet jamais, et n'ont aucune entrée pour `aucune_demande`, `presence_indisponible`, `visite_indisponible`. À l'état `aucune_demande`, la carte « décision » affiche `'—'` et la carte « justification » la clé brute. L'audit ajoute que `mode_maison_normal` serait « un vestige d'un ancien `vacances_raison` indexé sur `mode_maison` ».

**Vérifié et confirmé (cœur fonctionnel).** Les deux cartes mappent `mode_maison_normal`, `presence_famille`, `visite_en_cours`, `vacances_actives`. Or `vacances_raison` émet `aucune_demande`, `presence_indisponible`, `visite_indisponible`, `presence_famille`, `visite_en_cours`, `vacances_actives`. Donc : `mode_maison_normal` est une clé **morte** ; `aucune_demande`/`presence_indisponible`/`visite_indisponible` sont **absentes des maps** → carte décision `'—'` (fallback `|| '—'`), carte justification clé brute (fallback `|| entity.state`). Les deux gardes que le contrat §4.4 dit « essentielles pour le diagnostic UI » ne sont pas restituées.

**Élément INFIRMÉ.** L'étiologie « vestige d'un ancien `vacances_raison` indexé sur `mode_maison` » est **contredite par l'historique git** : la recherche de `mode_maison_normal` dans l'historique de `vacances_raison.yaml` ne renvoie **rien** — la chaîne n'a **jamais** figuré dans ce capteur ; elle n'a existé que dans les cartes UI (et la baseline). Il ne s'agit donc pas d'un vestige d'un état de capteur supprimé, mais d'un **désalignement carte/capteur dès l'origine**. La phrase causale doit être retirée ; le constat fonctionnel, lui, est solide.

**Gravité.** 🟠 portant sur la lisibilité diagnostique (aucune conséquence runtime ou de sécurité).

---

### VAC-IMP-5 — Désinfection retour : ordonnancement (🟠) — **VALIDÉ AVEC RÉSERVE** · confiance Moyen

**Énoncé d'origine.** `desinfection_retour_vacances` (trigger `mode_maison Vacances→Normal`, condition `…autorisee=on`) et `start_timer_ecs_desinfection` (trigger sur tout changement de `mode_maison` → `timer.cancel`) réagissent à la même transition. L'une lit l'autorisation issue du timer, l'autre annule ce timer ; aucun `for:` ni séquencement. Réserve d'origine : le sens exact de l'échec dépend de la sémantique de `timer.cancel`, non tranchable depuis le dépôt.

**Vérifié et confirmé.** Les deux automations réagissent bien à la même transition ; le capteur d'autorisation = `timer idle ∧ remaining=='0:00:00'` (timer arrivé à terme naturellement). La fragilité structurelle (aucun séquencement, l'un lit une autorisation dérivée du timer que l'autre annule) est démontrée par le code.

**Nuance de revue.** La réserve d'origine est juste mais sous-spécifiée : l'aléa est **triple** et non tranchable depuis le dépôt — (1) ordre de déclenchement des deux automations sur le même événement ; (2) instant de recalcul du template `…autorisee` après `timer.cancel` ; (3) sémantique de l'attribut `remaining` après `cancel` vs après fin naturelle. La conception est par ailleurs astucieuse (`remaining=='0:00:00'` distingue « terme atteint » d'un reset). Réserve maintenue.

---

### VAC-MIN-1 — Attribut d'intégrité `fenetre_inversee` (🟡) — **VALIDÉ** · confiance Élevé

**Énoncé d'origine.** Le contrat §5.3/§14 déclare un attribut `fenetre_inversee` ; l'implémentation expose `fenetre_invalide` + `cause` (dont la valeur peut être `fenetre_inversee`), sans clé d'attribut `fenetre_inversee`. Le TEST 6 passe par sous-chaîne sur la valeur. Impact fonctionnel nul ; critère §14 non littéralement satisfait.

**Vérifié et confirmé.** Clés d'attributs réellement exposées : `fenetre_invalide`, `debut_indisponible`, `fin_indisponible`, `cause` ; **aucune** clé `fenetre_inversee` (présente seulement en *valeur* de `cause` et en commentaire). TEST 6 passe par recherche de sous-chaîne sur l'ensemble du YAML. **Aucun consommateur** ne lit cet attribut → impact fonctionnel nul ; le critère de clôture §14 n'est pas littéralement satisfait. Triple écart contrat ≠ implémentation ≠ test confirmé.

---

### VAC-MIN-2 — `mode_vaisselle` non restauré (🟡) — **VALIDÉ** · confiance Élevé

**Énoncé d'origine.** `mode_vaisselle` est éteint à l'entrée (`application_debut`) mais jamais restauré à la sortie, ni par `application_fin` ni par `normal.yaml`. Asymétrie silencieuse, non documentée.

**Vérifié et confirmé.** `application_debut` éteint `mode_vaisselle` ; ni `application_fin` ni `normal.yaml` ne le rallument. Une hypothèse d'innocuité (drapeau transitoire auto-rétabli) a été testée et **réfutée** : les automations vaisselle **lisent** `mode_vaisselle` en *condition*, elles ne l'écrivent pas. C'est donc une **préférence utilisateur persistante** ; après un cycle Vacances elle reste `off` jusqu'à réactivation manuelle, et les cycles vaisselle planifiés restent inhibés. L'asymétrie est réelle et non auto-cicatrisante — d'autant plus visible que `ecs_desinfection_active`, lui, *est* restauré par `normal.yaml`.

---

### VAC-MIN-3 — Sémantique du timer ECS vs documentation (🟡) — **VALIDÉ AVEC RÉSERVE** · confiance Moyen

**Énoncé d'origine.** `timer.vacances_longues_ecs` est piloté sur `mode_maison` (projection/demande), mais le commentaire annonce une mesure de la « durée continue des vacances » où « toute interruption des vacances remet le compteur à zéro ». Un retour d'occupant (`vacances_actives=off`) ne réinitialise pas le compteur tant que la demande persiste. Dette documentaire/sémantique.

**Vérifié et confirmé (mécanique).** L'automation démarre le timer sur `mode_maison=Vacances` et l'annule sinon ; un retour d'occupant (`vacances_actives=off`) ne réinitialise pas le compteur tant que `mode_maison` reste `Vacances`.

**Nuance de revue.** Qualifier cela de « règle métier non tenue » dépend de l'interprétation de l'en-tête (« interruption des vacances »). Si « les vacances » désigne le **contexte** `mode_maison`, le commentaire est *exact* ; le rapport choisit la lecture « absence réelle » (`vacances_actives`). L'ambiguïté est documentaire. L'angle hygiène ECS donne néanmoins du fond à la lecture du rapport : compter une « durée continue d'absence » sur la projection plutôt que sur l'absence effective peut surévaluer la stagnation réelle de l'eau. 🟡 cohérent.

---

### VAC-MIN-4 — `delay` après la garde au boot (🟡) — **VALIDÉ AVEC RÉSERVE** · confiance Réservé (risque surévalué)

**Énoncé d'origine.** Dans `application_debut`/`application_fin`, le `delay 00:00:20` de stabilisation est postérieur à l'évaluation de la garde `vacances_actives`. Si l'état est encore `unknown` à l'instant de `start`, la garde échoue sans re-évaluation. Structure en retrait de la doctrine *boot-proof* (l'orchestrateur, lui, est inconditionnel au boot). Réserve d'origine : occurrence réelle non démontrable depuis le dépôt.

**Vérifié (observation structurelle exacte).** La condition est bien évaluée avant le `delay` interne à l'action ; contraste réel avec l'orchestrateur (boot inconditionnel).

**Nuance de revue — risque surévalué.** L'affirmation « la garde échoue **sans re-évaluation** » néglige le mécanisme de rattrapage : chaque automation possède **aussi** un trigger d'état (`vacances_actives→on` / `→off for 1min`) sans filtre `from:`. Une transition `unknown→on` (resp. `→off`) **redéclenche** l'automation une fois le capteur résolu, et applique alors le contexte. Le domaine est donc **auto-cicatrisant** : l'application est différée, non perdue. Le risque fonctionnel est largement théorique ; il s'agit avant tout d'une **incohérence de style boot-proof** (réelle, mineure), pas d'un trou de réconciliation. La réserve d'origine couvrait l'incertitude de timing mais **omettait ce chemin de rattrapage**, qui est le mitigant décisif.

---

### VAC-AME-1 — Contrôleur par correspondances de sous-chaînes (🟢) — **VALIDÉ** · confiance Élevé

**Vérifié et confirmé.** TEST 4 valide l'écriture de `vacances_fenetre_active` en cherchant la sous-chaîne de commentaire « Orchestrateur fenêtre planifiée » ; TEST 6 cherche une valeur, non un nom d'attribut. Vérifications structurelles absentes, comme énoncé.

### VAC-AME-2 — Hétérogénéité `service:` vs `action:` (🟢) — **VALIDÉ** · confiance Élevé

**Vérifié et confirmé.** `desinfection_retour_vacances` et `veille_chauffe_ponctuelle` emploient `service:` ; des automations plus récentes du domaine emploient `action:`. Sans impact fonctionnel.

### VAC-AME-3 — Vocabulaire de couche divergent entre contrats (🟢) — **VALIDÉ** · confiance Élevé

**Vérifié et confirmé.** Le contrat 80 n'explicite pas son écart vis-à-vis de Vacances §10, et §10 ne reconnaît pas l'arbitrage chauffage sur `mode_maison`. Observation documentaire cohérente avec VAC-IMP-1.

---

## Éléments infirmés (consolidé)

Un seul élément, et un seul, est **INFIRMÉ** par le dépôt :

- **VAC-IMP-4 — assertion causale.** « `mode_maison_normal` est un vestige d'un ancien `vacances_raison` indexé sur `mode_maison` » est **faux** : l'historique git montre que cette chaîne n'a jamais existé dans `vacances_raison.yaml` ; elle n'a vécu que dans les cartes UI. À reformuler en « désalignement carte/capteur d'origine ». **Le constat fonctionnel de VAC-IMP-4 reste, lui, entièrement valide.**

Aucun constat n'est classé **NON DÉMONTRÉ**.

---

## Nuances transverses apportées par la revue

Ces nuances ne créent aucun nouveau constat et ne modifient aucune gravité ; elles précisent le cadrage de constats déjà existants.

1. **Cadrage normatif (VAC-IMP-1, VAC-AME-3).** La divergence chauffage relève d'une **décision normative explicite et non réconciliée** (contrat 80 assumé) plutôt que d'une « dérive » silencieuse. Les faits tiennent ; le qualificatif gagne à être présenté comme tel.
2. **Portée préventive (VAC-IMP-3).** Le contrôleur est inopérant sur les templates métier, mais **aucune violation actuelle** n'existe ; la gravité porte sur l'assurance de conformité future.
3. **Interprétation documentaire (VAC-MIN-3).** Le caractère « non tenu » de la règle dépend d'une lecture d'un commentaire ambigu.
4. **Auto-cicatrisation au boot (VAC-MIN-4).** Les triggers d'état neutralisent l'essentiel de la « fragilité boot » ; le constat est à lire comme une incohérence de doctrine.

### Imprécisions de forme du rapport (sans incidence sur les conclusions)

- **Décompte des déclencheurs de l'orchestrateur.** La cartographie écrit « 6 déclencheurs : start, 4×state, 2×time » — soit arithmétiquement **7**. L'implémentation a effectivement 7 entités de déclenchement (le trigger d'état inclut `parametres_invalides_vacances`, au-delà des 6 listés au §4.1.1). Le déclencheur supplémentaire est bénéfique ; seule l'étiquette « 6 » est imprécise, et la conformité §14 reste satisfaite.
- **Numéros de ligne.** Quelques décalages cosmétiques (condition ECS de `veille_chauffe_ponctuelle` ; localisation `desired_mode` vs `reason` dans `decision_centrale`). Sans incidence.

---

## Niveau de confiance final global

Le rapport d'audit Vacances est jugé **globalement solide et honnête** : ses constats factuels sont presque tous reproductibles dans le dépôt, ses réserves sont posées aux bons endroits, et aucune fabrication de preuve n'a été détectée. La distinction démontré ↔ théorique est correctement tenue, sauf sur VAC-MIN-4.

- **8 constats VALIDÉS** sans objection substantielle (Conformes, Aucun critique, VAC-IMP-2, VAC-IMP-3, VAC-MIN-1, VAC-MIN-2, VAC-AME-1, VAC-AME-2, VAC-AME-3) — confiance Élevé. *(VAC-IMP-1 est VALIDÉ sur les faits, confiance Élevé, avec une nuance de cadrage normatif.)*
- **3 constats VALIDÉS AVEC RÉSERVE** (VAC-IMP-5, VAC-MIN-3, VAC-MIN-4) — la réserve porte sur une sémantique runtime, une interprétation documentaire, ou un poids surévalué, non sur l'existence des faits.
- **1 sous-élément INFIRMÉ** (l'étiologie de VAC-IMP-4), le constat fonctionnel correspondant restant valide.
- **Aucun constat NON DÉMONTRÉ.**

La conclusion d'ensemble du rapport — **noyau métier sain, dette concentrée aux frontières de consommation et dans les outils de surveillance** — résiste à la contre-expertise.

---

*Revue critique en lecture seule — aucun fichier du dépôt modifié ni créé pendant la phase de revue. Ce document est un livrable d'archivage : il formalise une contre-expertise déjà réalisée. Il ne contient ni nouveau constat, ni réévaluation de gravité, ni correctif, ni plan d'action.*
