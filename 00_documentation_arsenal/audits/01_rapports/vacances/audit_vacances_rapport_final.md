# Audit Arsenal — Mode maison `Vacances`

> Type : rapport d'audit architectural — version finale officielle
> Portée : domaine `vacances` (5 niveaux : paramétrage, support temporel, demande, effectivité, application) et ses consommateurs (chauffage, ECS, UI, contrôleur CI)
> Mode : lecture seule — aucun runtime, contrat ou UI modifié ; aucun patch produit ; `git status` propre à l'ouverture et à la fermeture
> Référence dépôt : branche `main`, HEAD `c20d9ee`
> Principe directeur : « le runtime est la référence, le contrat documente le runtime »

---

## 1. Contexte

Le domaine `Vacances` gouverne un contexte global d'absence prolongée dans Arsenal. Il est régi par le contrat normatif `00_documentation_arsenal/contrats/vacances.md` (v1.4.0, statut *Normatif — Clos*), qui formalise une architecture en **cinq niveaux** strictement séparés : paramétrage, support temporel, demande calculée, effectivité métier, application de contexte. Le contrat pose des invariants forts, notamment la séparation demande/effectivité, l'interdiction de `now()` dans les templates du domaine, le caractère *boot-proof* des automations critiques, et la règle de consommation par couche (chaque sous-système consomme la couche qui lui correspond).

Cet audit a été demandé pour déterminer comment le mode `Vacances` est réellement implémenté, cartographier ses dépendances, reconstituer son comportement effectif et identifier tout écart entre le runtime, les contrats et les interfaces. Le présent document est le livrable d'archivage : il reprend **exclusivement** les constats démontrés pendant l'audit, sans réévaluation de gravité, sans nouveau constat, sans correctif ni plan d'action.

---

## 2. Périmètre

**Inclus :**

- Contrat de référence : `contrats/vacances.md` (v1.4.0).
- Couche paramétrage : `06_input_selects/modes/mode_maison.yaml`, `07_input_datetimes/vacances/vacances.yaml`, `05_input_booleans/modes/vacances/{demande_manuelle,fenetre_active,mode_auto}.yaml`.
- Couche support temporel : `11_automations/modes/vacances/programmation/orchestrateur.yaml`.
- Couche demande : `12_template_sensors/modes/{vacances_planifiees_actives,vacances_demandees}.yaml`.
- Couche effectivité : `12_template_sensors/modes/{vacances_actives,vacances_raison}.yaml`.
- Couche application & projection : `programmation/{activation,desactivation}.yaml`, `application_debut.yaml`, `application_fin.yaml`, `start_timer_ecs_desinfection.yaml`, `modes/normal.yaml`.
- Intégrité paramétrique : `12_template_sensors/system/integrite_reglages/vacances.yaml`, `02_groups/parametres_invalides.yaml`.
- Consommateurs aval : chauffage (`10_scripts/chauffage/decision_centrale.yaml`, `12_template_sensors/chauffage/diagnostic/{mode,raison}.yaml`, contrats `chauffage/{65,66,80}`), ECS (`08_timers/ecs/desinfection_vacances.yaml`, `12_template_sensors/ecs/desinfection_vacances_autorisee.yaml`, `11_automations/ecs/{desinfection_retour_vacances,veilles/veille_chauffe_ponctuelle}.yaml`).
- Vérification : `scripts/arsenal_contracts/check_vacances_contracts.py`, `.github/workflows/contracts_vacances.yml`.
- UI : `19_button_card_templates/40_dashboards/modes/{10_action,30_diagnostic,40_info}/`.

**Exclus :** runtime live (états instantanés Home Assistant non observés), historisation (`recorder`), domaines non couplés à `Vacances`.

---

## 3. Méthode

Procédure strictement en lecture seule :

1. Clone local du dépôt (branche `main`, HEAD `c20d9ee`) ; `git status` initial → *working tree clean*.
2. Recensement exhaustif de l'empreinte `vacances` sur l'ensemble du dépôt.
3. Lecture du contrat normatif comme référence d'intention.
4. Lecture de l'implémentation couche par couche selon les 5 niveaux du contrat.
5. Résolution des références (entités, scripts, timers) pour vérifier leur existence effective.
6. Traçage des *writers/readers* des entités sensibles (`mode_maison`, `vacances_*`, `ecs_blocage_planifiee`, `timer.vacances_longues_ecs`).
7. Confrontation contrat ↔ implémentation ↔ contrôleur CI ↔ cartes UI, et vérification croisée avec les contrats du domaine chauffage consommant `Vacances`.
8. Exécution (lecture seule) du contrôleur `check_vacances_contracts.py` pour observer son verdict réel.
9. `git status` final → *working tree clean*, `git diff` vide.

Chaque constat est démontré par un élément présent dans le dépôt, jamais par hypothèse. Les rares zones d'incertitude (sémantique runtime Home Assistant non tranchable depuis le seul dépôt) sont signalées comme telles.

---

## 4. Cartographie synthétique du domaine

Le domaine est implémenté **conformément à l'architecture en 5 niveaux** annoncée. Toutes les entités canoniques existent et le découpage est respecté.

| Niveau | Entités | Définition / source |
|---|---|---|
| 1 — Paramétrage | `input_select.mode_maison` (`Normal`/`Vacances`) · `input_datetime.debut_vacances` / `fin_vacances` (date+heure) · `input_boolean.mode_vacances_auto` · `input_boolean.vacances_demande_manuel` | `06_input_selects/modes/`, `07_input_datetimes/vacances/`, `05_input_booleans/modes/vacances/` |
| 2 — Support temporel | `input_boolean.vacances_fenetre_active` | Orchestrateur `programmation/orchestrateur.yaml` (ID `10090000000012`, 6 déclencheurs : `start`, 4 × `state`, 2 × `time`) |
| 3 — Demande | `binary_sensor.vacances_planifiees_actives` ← `mode_vacances_auto` ∧ `parametres_invalides_vacances=off` ∧ `vacances_fenetre_active` · `binary_sensor.vacances_demandees` ← `vacances_demande_manuel` ∨ `vacances_planifiees_actives` | `12_template_sensors/modes/` |
| 4 — Effectivité | `binary_sensor.vacances_actives` ← `vacances_demandees` ∧ `presence_famille_unifiee=off` ∧ `visite_en_cours=off` · `sensor.vacances_raison` (6 états priorisés) | `12_template_sensors/modes/` |
| 5 — Application | Projection : `activation.yaml` (ID `1009000000004`) / `desactivation.yaml` (ID `1009000000005`) — seuls writers légitimes de `mode_maison` · Application effective : `application_debut.yaml` (ID `1009000000006`, sur `vacances_actives`) / `application_fin.yaml` (ID `10090000000013`) · Restauration : `normal.yaml` (ID `1009000000007`, sur `mode_maison → Normal`) · Support ECS : `start_timer_ecs_desinfection.yaml` + `timer.vacances_longues_ecs` (144 h) | `11_automations/modes/` |

**Intégrité paramétrique :** `binary_sensor.parametres_invalides_vacances` (`system/integrite_reglages/vacances.yaml`), correctement agrégé dans `group.parametres_invalides_domaines`.

**Consommateurs aval identifiés :**

- **ECS** — `ecs_blocage_planifiee` (lu par `veille_chauffe_ponctuelle.yaml`), `ecs_desinfection_active`, `mode_vaisselle`, chaîne désinfection retour (`desinfection_vacances_autorisee.yaml` → `desinfection_retour_vacances.yaml`).
- **Chauffage** — `decision_centrale.yaml`, `diagnostic/{mode,raison}.yaml`, contrats `chauffage/{65,66,80}`, scripts `consigne_vacances` / `consigne_fin_vacances`.
- **UI** — cartes `19_button_card_templates/40_dashboards/modes/{10_action,30_diagnostic,40_info}/`.
- **Vérification** — `check_vacances_contracts.py` + workflow `contracts_vacances.yml` (sur push/PR).

Toutes les entités, scripts et timers référencés **existent** : aucune référence cassée détectée dans le cœur du domaine.

---

## 5. Constats détaillés

### 5.1 Points conformes (à préserver)

Le noyau du domaine est sain et fidèle au contrat. Constats conformes établis par lecture directe :

- Architecture en 5 niveaux respectée ; entités canoniques toutes présentes.
- Séparation **demande / effectivité** effective : `vacances_actives` lit la demande consolidée, jamais directement `mode_maison`.
- Boucle logique correctement brisée : `vacances_demandees` ne dépend pas de `mode_maison` ; la fin de fenêtre planifiée provoque bien le retour à `Normal`.
- Orchestrateur de fenêtre **boot-proof** : déclencheur `homeassistant: start` inconditionnel, `now()` utilisé uniquement sur déclenchement explicite, borne de fin exclusive `[debut ; fin[`.
- Intégrité paramétrique en **échec prudent** : indisponibilité ou `fin ≤ debut` ⇒ paramètres invalides ⇒ planification retombée à `off`.
- `sensor.vacances_raison` couvre les 6 états contractuels (§4.4), gardes de vérité terrain incluses.

### 5.2 Constats démontrés par le dépôt

*Établis par lecture directe des fichiers. La preuve est le code. Statut : CONFIRMÉ (dépôt), sauf réserve explicite.*

#### 🔴 Critique

**Aucun constat critique.** Le domaine fonctionne sur son chemin nominal : ni perte de donnée, ni boucle bloquante, ni rupture de sécurité, ni référence cassée dans le noyau. L'absence de constat critique est consignée explicitement.

#### 🟠 Important

| ID | Constat | Gravité | Preuve |
|---|---|---|---|
| **VAC-IMP-1** | Le chauffage consomme la **projection** (`mode_maison = Vacances`) et non l'**effectivité** (`vacances_actives`) pour sélectionner le régime `reduced`/`comfort`. Le contrat Vacances §10 impose `binary_sensor.vacances_actives` **uniquement** pour la logique d'absence effective (ECS, chauffage, présence). Le contrat `66_adaptation_consigne_vacances.md` respecte cette règle (adaptation numérique de consigne sur `vacances_actives`), mais la Décision Centrale arbitre sur `mode_maison`. Contradiction inter-contrats : `80_table_decision_canonique.md` vs Vacances §10. | 🟠 | `decision_centrale.yaml` l.211 et 253 (raison `mode_maison_vacances`) ; `diagnostic/{mode.yaml l.89, raison.yaml l.90/94}` ; `80_table…md` l.97-98 et 138 ; `vacances.md` §10 ; `66_adaptation…md` l.53/77/89/111 |
| **VAC-IMP-2** | **Asymétrie d'application du blocage ECS** : `ecs_blocage_planifiee` est posé sur la couche effectivité (`application_debut`, déclenché par `vacances_actives → on`) mais n'est levé que par la couche projection (`normal.yaml`, déclenché par `mode_maison → Normal`). `application_fin` ne touche pas à l'ECS. Lorsqu'un occupant revient pendant une demande active (`vacances_actives=off`, `mode_maison` reste `Vacances`), `application_fin` retire la consigne réduite mais laisse `ecs_blocage_planifiee=on` : l'eau chaude reste planifiée-bloquée alors que la maison est occupée. Le consommateur exige `ecs_blocage_planifiee=off` pour chauffer. | 🟠 | `application_debut.yaml` l.65-66/89-92 ; `application_fin.yaml` (absence ECS) ; `normal.yaml` l.86-98 ; `veille_chauffe_ponctuelle.yaml` l.47-50 |
| **VAC-IMP-3** | Le **contrôleur CI ne scrute pas les templates réels du domaine**. `VACANCES_TEMPLATE_PATHS` vise `12_template_sensors/vacances`, répertoire **inexistant** ; les capteurs métier sont dans `12_template_sensors/modes/`. Le TEST 2 (interdiction `now()`/`today_at`, invariant §12) ne couvre donc que `integrite_reglages/vacances.yaml`. Les 4 capteurs métier ne sont jamais analysés. Garde-fou de l'invariant le plus structurant inopérant. | 🟠 | `check_vacances_contracts.py` (`VACANCES_TEMPLATE_PATHS`) ; absence du répertoire `12_template_sensors/vacances` ; capteurs réels sous `12_template_sensors/modes/` ; exécution observée : verdict `✅ CONTRAT VACANCES CONFORME`, exit 0 |
| **VAC-IMP-4** | **Cartes de diagnostic UI désalignées** : elles mappent une raison `mode_maison_normal` que `sensor.vacances_raison` n'émet jamais, et n'ont aucune entrée pour `aucune_demande`, `presence_indisponible`, `visite_indisponible`. À l'état `aucune_demande`, la carte « décision » affiche `'—'` et la carte « justification » la clé brute. Les deux états de garde — que le contrat §4.4 qualifie d'« essentielle pour le diagnostic UI » — ne sont pas restitués. `mode_maison_normal` est un vestige d'un ancien `vacances_raison` indexé sur `mode_maison`. | 🟠 | `carte_vacances_decision.yaml` l.58-65 ; `carte_vacances_justification.yaml` l.52-58 ; états réels de `vacances_raison.yaml` |
| **VAC-IMP-5** | **Désinfection au retour : dépendance d'ordonnancement non garantie.** `desinfection_retour_vacances` (trigger `mode_maison: Vacances → Normal`, condition `ecs_desinfection_retour_vacances_autorisee=on`) et `start_timer_ecs_desinfection` (trigger sur tout changement de `mode_maison`, `timer.cancel`) réagissent à la même transition. L'une lit l'autorisation issue du timer, l'autre annule ce timer ; aucun `for:` ni séquencement explicite. La fragilité d'ordonnancement est démontrée ; le sens exact de l'échec dépend de la sémantique de `timer.cancel` sur l'attribut `remaining`, non tranchable depuis le seul dépôt (réserve). | 🟠 | `desinfection_retour_vacances.yaml` ; `start_timer_ecs_desinfection.yaml` ; `desinfection_vacances_autorisee.yaml` (`idle` ∧ `remaining == '0:00:00'`) |

#### 🟡 Mineur

| ID | Constat | Gravité | Preuve |
|---|---|---|---|
| **VAC-MIN-1** | **Dérive de l'attribut d'intégrité** : le contrat §5.3 et le critère de clôture §14 déclarent un attribut `fenetre_inversee` ; l'implémentation expose `fenetre_invalide` + `cause` (dont la valeur peut être `fenetre_inversee`), sans clé d'attribut `fenetre_inversee`. Le TEST 6 du contrôleur passe uniquement par correspondance de sous-chaîne sur la valeur, non sur le nom d'attribut. Contrat ≠ implémentation ≠ test. Aucun consommateur ne lit cet attribut hors du contrôleur ; impact fonctionnel nul, critère §14 non littéralement satisfait. | 🟡 | `vacances.md` §5.3/§14 ; `integrite_reglages/vacances.yaml` (`fenetre_invalide`, `cause`) ; `check_vacances_contracts.py` TEST 6 |
| **VAC-MIN-2** | `mode_vaisselle` est éteint à l'entrée (`application_debut`) mais **jamais restauré** à la sortie, ni par `application_fin` ni par `normal.yaml`. Asymétrie silencieuse, non documentée. | 🟡 | `application_debut.yaml` l.94 ; absence dans `application_fin.yaml` et `normal.yaml` |
| **VAC-MIN-3** | **Sémantique du timer ECS vs sa documentation** : `timer.vacances_longues_ecs` est piloté sur `mode_maison` (projection/demande), mais le commentaire du fichier annonce une mesure de la « durée continue des vacances » avec « toute interruption des vacances remet le compteur à zéro ». Un retour d'occupant (`vacances_actives=off`) ne réinitialise pas le compteur tant que la demande persiste. Règle métier annoncée non tenue au sens de l'absence réelle. Dette documentaire/sémantique. | 🟡 | `start_timer_ecs_desinfection.yaml` (déclencheur `mode_maison`) ; en-tête commenté du fichier |
| **VAC-MIN-4** | **Réconciliation au boot : `delay` placé après la condition de garde.** Dans `application_debut`/`application_fin`, le `delay 00:00:20` de stabilisation est interne à l'action, donc postérieur à l'évaluation de `vacances_actives`. Si l'état est encore `unknown` à l'instant de `start`, la garde échoue sans re-évaluation. Structure en retrait de la doctrine *boot-proof* affichée (l'orchestrateur de fenêtre, lui, est inconditionnel au boot). Fragilité structurelle ; occurrence réelle non démontrable depuis le seul dépôt (dépend du timing d'évaluation des template sensors au démarrage) — réserve. | 🟡 | `application_debut.yaml` et `application_fin.yaml` (ordre condition → `delay`) ; contraste avec `orchestrateur.yaml` (boot inconditionnel) |

#### 🟢 Amélioration

| ID | Observation | Gravité | Preuve |
|---|---|---|---|
| **VAC-AME-1** | Le contrôleur repose sur des **correspondances de sous-chaînes** plutôt que sur des vérifications structurelles : TEST 4 cherche le commentaire « Orchestrateur fenêtre planifiée », TEST 6 cherche une valeur et non un nom d'attribut. | 🟢 | `check_vacances_contracts.py` (TEST 4, TEST 6) |
| **VAC-AME-2** | **Hétérogénéité de syntaxe** `service:` vs `action:` au sein du domaine (ex. `desinfection_retour_vacances.yaml` emploie `service:`). Sans impact fonctionnel. | 🟢 | `desinfection_retour_vacances.yaml` vs automations récentes du domaine |
| **VAC-AME-3** | Le vocabulaire de couche **diverge entre contrats** : `80_table_decision_canonique.md` n'explicite pas son écart vis-à-vis de Vacances §10, et Vacances §10 ne reconnaît pas l'arbitrage chauffage sur `mode_maison`. Observation documentaire (cf. VAC-IMP-1). | 🟢 | `80_table…md` ; `vacances.md` §10 |

---

## 6. Analyse des impacts

**Le noyau métier est sain ; la dette se concentre aux frontières de consommation.** L'effet commun de VAC-IMP-1 et VAC-IMP-2 est une **divergence de couche entre la projection (`mode_maison`) et l'effectivité (`vacances_actives`)** : plusieurs consommateurs n'écoutent pas la couche que le contrat leur assigne.

- **Confort et ECS en cas de divergence demande/présence.** Quand une demande Vacances est projetée mais que la famille est réellement présente, le chauffage applique le régime Vacances `reduced` (VAC-IMP-1) et le blocage ECS persiste (VAC-IMP-2) — alors même que `vacances_actives=off`. C'est précisément le scénario que la séparation demande/effectivité visait à empêcher. Conséquences observables : chauffage réduit et eau chaude planifiée-bloquée pour des occupants présents, jusqu'à la fin réelle de la demande.

- **Assurance de conformité supérieure à la réalité.** VAC-IMP-3 (CI aveugle aux templates du domaine) et VAC-MIN-1 (test par sous-chaîne) donnent un verdict `CONFORME` qui ne garantit pas l'invariant `now()` ni le nom d'attribut contractuel. Un écart futur sur la couche calculée ne serait pas détecté.

- **Observabilité métier dégradée.** VAC-IMP-4 prive l'utilisateur des libellés pour l'état le plus fréquent (`aucune_demande`) et pour les deux états de garde (`presence_indisponible`, `visite_indisponible`), que le contrat tient pourtant pour essentiels au diagnostic.

- **Fragilité d'ordonnancement.** VAC-IMP-5 rend l'issue de la désinfection au retour dépendante d'un ordre d'exécution non garanti et d'une sémantique runtime non fixée dans le dépôt.

- **Dette documentaire/sémantique bornée.** VAC-MIN-2, VAC-MIN-3 et VAC-MIN-4 constituent des asymétries et désalignements localisés, sans rupture fonctionnelle prouvée, mais en retrait de la doctrine affichée.

Les réserves explicites (VAC-IMP-5, VAC-MIN-4) délimitent ce qui relève du comportement runtime Home Assistant, non tranchable depuis le seul dépôt.

---

## 7. Conclusion générale

Le domaine `Vacances` est **structurellement solide et fidèle à son contrat sur le cœur** : architecture en 5 niveaux respectée, entités canoniques toutes présentes, séparation demande/effectivité effective, boucle logique correctement brisée, orchestrateur de fenêtre robuste au boot, intégrité paramétrique en échec prudent. **Aucun défaut critique** et aucune référence cassée dans le noyau.

La dette se situe **aux frontières de consommation aval et dans les outils de surveillance**, là où plusieurs consommateurs n'écoutent pas la couche que le contrat leur assigne : le chauffage (VAC-IMP-1) et la levée du blocage ECS (VAC-IMP-2) s'appuient sur la projection `mode_maison` au lieu de l'effectivité `vacances_actives`, réintroduisant le couplage que la séparation en couches visait à éliminer ; les garde-fous périphériques (CI en VAC-IMP-3, cartes UI en VAC-IMP-4) sont partiellement inopérants ; la chaîne de désinfection au retour (VAC-IMP-5) repose sur un ordonnancement non garanti.

En résumé : **le moteur métier est sain ; ce sont les contrats de consommation aval et les outils de surveillance qui ont dérivé par rapport au contrat v1.4.0.** Au sens strict du §14, le domaine n'est pas « propre et clos » (attribut `fenetre_inversee` non littéralement présent ; couches de consommation non conformes au §10). Les écarts sont réversibles et bien circonscrits, sans urgence de sécurité ; VAC-IMP-1 et VAC-IMP-2 produisent toutefois des comportements observables divergents de l'intention contractuelle.

---

*Audit en lecture seule — aucun fichier du dépôt modifié ni créé pendant la phase d'audit. Ce rapport est un livrable d'archivage : il ne contient ni correctif, ni plan d'action, et ne réévalue aucune gravité.*
