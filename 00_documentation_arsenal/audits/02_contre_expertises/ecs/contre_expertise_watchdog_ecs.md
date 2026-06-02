# Contre-expertise — ECS-WD-1 (watchdog ECS : doctrine et survie du cycle)

> **Statut :** contre-expertise de constat — `ECS-WD-1` **requalifié 🔴 Haute → INFIRMÉ comme violation de contrat** ; lecture « cycle = script orchestrateur » **invalidée** ; doctrine réelle établie = **watchdog = filet de sûreté terminal** (rabaissement + libération du verrou) ; dette résiduelle 🟡 documentaire sur `06` §4.2 (gated) + constat distinct `ECS-WD-2` (cohérence orchestrateur/watchdog) versé au backlog ; domaine **ECS NON clôturé**.
> **Domaine :** `ecs` — orchestration de cycle thermique, sécurité active, gestion du temps.
> **Destination d'archivage :** `00_documentation_arsenal/audits/02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/01_rapports/ecs/audit_ecs_domaine.md`
> - `00_documentation_arsenal/contrats/ecs/06_temps_timers_watchdogs.md`
> - `00_documentation_arsenal/contrats/ecs/07_gardiens_et_securite_active.md`
> - `00_documentation_arsenal/contrats/ecs/05_etats_memoire_planification.md`
> - `00_documentation_arsenal/changelog/changelogs/v00/v0_2.md`, `v11/v11.md`, `v11/v11_beta.md`, `v11/v11_beta_3.md`, `v11/v11_beta_4.md`, `v11/v11_beta_5.md`
> **État du dépôt à la rédaction :** `origin/main` = `f6efd6a`.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Réexaminer `ECS-WD-1` (« le watchdog est une borne absolue ; l'implémentation ne la respecte pas »), statuer sur la validité de sa prémisse — que la phrase `06` §4.2 « aucun cycle ne survit à son watchdog » reflète l'intention architecturale — et déterminer la doctrine réelle du watchdog ECS. Acte documentaire — aucune modification runtime, contrat ou CI.

---

## 2. Constat initial (rappel)

`ECS-WD-1` affirmait : `06_temps_timers_watchdogs.md` §4.1/§4.2 fait du watchdog une « durée maximale absolue / limite infranchissable » dont « aucun cycle ne survit » ; or `ecs_cycle_watchdog` dure `00:30:00` tandis que la branche désinfection de `cycle.yaml` peut nominalement courir ≈ 66 min ; l'automation `10250000000008` ne fait que rabaisser à 10 °C et libérer le verrou, sans pouvoir arrêter le script orchestrateur ; donc le cycle « survit » à son watchdog. Gravité **Haute**, qualifiée **violation de contrat**.

---

## 3. Hypothèse infirmée

La **prémisse centrale** — « `06` §4.2 décrit l'intention architecturale du watchdog ECS, lue comme : le watchdog doit mettre fin au processus de cycle » — est **fausse**. L'audit initial a érigé un slogan abstrait (`06` §4.2) en invariant opérationnel, en lisant « cycle » comme « script orchestrateur ». La définition concrète opposable du watchdog (`07` §6) et la trajectoire historique du composant établissent l'inverse : le watchdog ECS est un **filet de sûreté terminal** dont le périmètre assuré est le rabaissement et la **libération du verrou** — jamais l'arrêt du script.

---

## 4. Preuves (dépôt `f6efd6a` + changelogs)

| # | Source | Fait |
|---|--------|------|
| P1 | `contrats/ecs/07_gardiens_et_securite_active.md` §6 « Watchdog terminal » | Périmètre assuré **énuméré** : « rabaissement forcé — libération unilatérale du verrou — restauration nominale — indépendance totale des mécanismes temporels secondaires ». **Pas** d'arrêt de processus. |
| P2 | `11_automations/ecs/consigne_10/watchdog.yaml` (id `10250000000008`) | À `timer.finished` : bridge → 10 °C + `turn_off ecs_cycle_en_cours`. Implémente exactement P1. |
| P3 | `10_scripts/ecs/cycle_session_open.yaml` (L12-15, L57, L69) | « cycle actif » y est **strictement** `input_boolean.ecs_cycle_en_cours == on` (« inspecter le verrou de cycle », « refuser si cycle actif légitime », « activer le verrou cycle »). |
| P4 | `contrats/ecs/05_etats_memoire_planification.md` §2.1 | Section intitulée « Verrou de cycle » — le corpus assimile « cycle » au verrou/session, non au script. |
| P5 | `changelog/v00/v0_2.md` (« Domaine ECS — cycle, watchdog, modes ») | Origine du watchdog : « reset automatique si verrou bloqué > 5 min », « abaissement confirmé à 10 °C » ; risque visé « surveillance fantôme (watchdog non annulé) ». Sémantique verrou/chaudière. |
| P6 | `changelog/v11/v11.md` (§158-162) | « Watchdog fin de cycle » : rabaissement via `ecs_appliquer_consigne_bridge` + « libération du verrou `ecs_cycle_en_cours` **garantie inconditionnellement** (bloc séparé) ». Identique au runtime actuel ; **aucun** arrêt de script. |
| P7 | `changelog/v11/v11_beta.md` | « gardiens et watchdogs … reconfirment des consignes avec vérification » — couche de correction, pas autorité terminale sur l'exécution. |
| P8 | `changelog/v11/v11_beta_5.md` (L109, L271) + `v11/v11.md` (L266) | Un **autre** watchdog (couche Exécution, contexte clim/chauffage) est « contractualisé, **non encore implémenté** », hiérarchie cible « Sécurité → Watchdog → Exécution ». La tonalité « souverain/infranchissable » appartient à ce concept planifié, distinct du watchdog ECS déployé. |
| P9 | `changelog/v11/v11_beta_4.md` (L95-97, L112) | La refonte de la section 6 du contrat ECS (hiérarchie « absolue », formulation §4) date de cette version — d'où l'import probable du vocabulaire abstrait dans `06` §4.2. |

**Conclusion de chaîne :** sous l'acception du corpus (P3-P4 : « cycle » = verrou), `06` §4.2 « aucun cycle ne survit à son watchdog » est **VRAIE et implémentée** (P1-P2-P6 : le verrou est libéré inconditionnellement). La contradiction n'apparaît que sous une acception (« cycle » = script orchestrateur) que ni `07` §6, ni `05` §2.1, ni aucun changelog n'autorisent.

---

## 5. Analyse (réponses aux questions de gouvernance)

- **A. La phrase `06` §4.2 reflète-t-elle l'intention architecturale, ou une rédaction devenue inexacte ?** Inexacte **par ambiguïté**, non par erreur de fond : c'est un slogan abstrait (hérité de la refonte v11 beta 4, P9, possiblement teinté par le watchdog Exécution non déployé, P8) qui, lu littéralement avec « cycle = script », surdimensionne ce que `07` §6 définit sobrement.
- **B. Intention originale : (a) sécurité chaudière + verrou, ou (b) souverain capable de tuer le cycle complet ?** **(a)**, sans discontinuité de v0.2 (P5) à v11 (P6) jusqu'au contrat `07` §6 (P1). Aucune source ne soutient (b) pour le watchdog ECS.
- **C. L'écart provient-il du runtime ou du contrat ?** **Du contrat** — précisément d'une ambiguïté terminologique dans `06` §4.2. Le runtime est conforme à la définition concrète (`07` §6) et à l'intention documentée.
- **D. La qualification « Haute / violation de contrat » est-elle défendable ?** **Non.** Elle reposait sur la lecture infirmée. À retirer.
- **E. Reste-t-il un résidu réel ?** **Oui, distinct** (`ECS-WD-2`) : l'orchestrateur n'est pas *watchdog-aware* et peut, à l'étape 7 (boost), ré-appliquer une consigne haute après le passage du watchdog. Ce **n'est pas** une violation de `06`/`07` (aucun contrat n'assigne au watchdog le devoir d'empêcher l'orchestrateur de poursuivre). C'est une question de **cohérence comportementale**, à arbitrer — pas un bug contractuel.

---

## 6. Nouvelle qualification proposée

**`ECS-WD-1` : 🔴 Haute → INFIRMÉ comme violation de contrat.** Énoncé requalifié : « Doctrine du watchdog ECS = filet de sûreté terminal (rabaissement + libération du verrou), conforme runtime ↔ `07` §6 ; `06` §4.2 emploie une formulation abstraite ambiguë (« cycle ») à désambiguïser. » Dette résiduelle : **🟡 documentaire** sur `06` §4.2 (modification **M2**, gated sur la décision doctrinale).

**`ECS-WD-2` (nouveau) :** « Orchestrateur non *watchdog-aware* : ré-application possible d'une consigne haute post-watchdog (cycle.yaml étape 7). » Gravité **à fixer après arbitrage** ; versé au backlog ECS. Non bloquant, non contractuel.

Comparaison des options pour `ECS-WD-1` : **maintien Haute** — non soutenable (prémisse infirmée) ; **clôture sèche** — perdrait la dette `06` §4.2 et le résidu `ECS-WD-2` ; **infirmation + scission** — retenue.

---

## 7. Détermination doctrinale (arbitrage rendu à l'architecte)

La doctrine **réelle** est tranchée par les preuves : **(a) watchdog = filet de sûreté terminal**. En revanche, la doctrine **cible** — faut-il faire évoluer le watchdog vers (b) « borne du processus complet », rendant l'orchestrateur watchdog-aware ? — **n'est pas tranchée ici** : c'est une décision d'architecture qui appartient à l'architecte.

- Si **(a) confirmée (statu quo)** : `06` §4.2 doit être désambiguïsé (**M2**) pour aligner le contrat sur le runtime (principe directeur). Aucune action runtime. `ECS-WD-2` reste un point de cohérence à surveiller.
- Si **(b) choisie** : ce n'est plus une correction documentaire mais l'ouverture d'un **chantier d'architecture** (rendre l'orchestrateur conscient de l'expiration watchdog) ; `06` §4.2 deviendrait alors la cible normative, non l'erreur. Hors périmètre de la présente contre-expertise.

---

## 8. Verdict

**`ECS-WD-1` infirmé comme violation de contrat** (preuves P1→P6) : le runtime est conforme à la définition opposable `07` §6 et à l'intention historique (a) ; l'écart est **contractuel et terminologique** (`06` §4.2). La qualification initiale « 🔴 Haute » était une **sur-lecture**, retirée. Dette résiduelle : **🟡 documentaire** (M2, gated) + constat distinct **`ECS-WD-2`** (cohérence orchestrateur/watchdog, backlog, gravité à fixer après arbitrage). Aucune correction runtime requise ni proposée. Domaine **ECS non clôturé**.

---

*Contre-expertise `ECS-WD-1`. Établie en lecture du dépôt (`origin/main` = `f6efd6a`) et de la trajectoire des changelogs. Acte documentaire — aucune modification runtime, aucun contrat, aucune CI.*
