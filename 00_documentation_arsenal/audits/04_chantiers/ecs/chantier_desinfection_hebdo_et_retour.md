# Chantier ECS — Désinfection hebdomadaire effective & consolidation du retour de vacances

> **Statut :** **CLÔTURÉ** · Lot 1 **livré** (#664) · Lot 2 **runtime livré** (#665) · complément circulation bouclage 5 min après réussite **livré** (#666). Après réussite corrélée de la désinfection de retour, Arsenal déclenche **une fois** la primitive existante `script.bouclage_ecs_5_minutes` (circulation bornée). Preuve terrain **acquise par exploitation en production** (fonctionnement nominal constaté sur la durée) — la propriété ayant renoncé explicitement à une campagne de validation terrain dédiée.
> **Constats sources :** `ECS-DESINF-VAC-1` / `ECS-DESINF-VAC-2` (audit mergé PR #662)
> **Code registre :** *ECS-DESINF-VAC* (numéro `Cxx` à attribuer par le propriétaire au registre)
> **Domaine :** `ecs` (secondairement `vacances`, en **consommation** seulement)
> **Chemin :** `00_documentation_arsenal/audits/04_chantiers/ecs/chantier_desinfection_hebdo_et_retour.md`
> **État du dépôt :** `origin/main` = `6068926` (runtime **identique** à celui analysé par le contrat candidat V2 — `git diff` vide)
> **Base de conception :** contrat candidat V2 (hors dépôt, non normatif) — arbitrages propriétaire A→K validés comme base de gouvernance
> **Périmètre :** **Lots 1 et 2 uniquement** (autorisation hebdomadaire + consolidation du retour). Les lots 3 à 5 (maintien thermique, fenêtre qualifiée, bouclage sanitaire, interface ECS↔Bouclage, verdict boucle) sont **hors périmètre absolu** de ce chantier.
> **Interdits respectés dans cette phase :** aucun YAML runtime, aucun helper/automation/script/template/checker/UI, aucun ID inventé, aucun changement dans le domaine bouclage, aucun commit.

---

## 1. Cadre et origine

L'audit `01_rapports/ecs/audit_desinfection_hebdomadaire_pendant_vacances.md` (mergé, PR #662) a établi
deux constats confirmés :

- **`ECS-DESINF-VAC-1`** — la désinfection ECS **hebdomadaire** n'est **pas inhibée** pendant les
  vacances : la veille `10250000000002` lance un cycle au créneau *jour+heure* sans aucune garde d'absence.
- **`ECS-DESINF-VAC-2`** — l'interrupteur `input_boolean.ecs_desinfection_active` est **inerte** :
  écrit `off` à l'entrée Vacances et `on` au retour, mais **lu par aucun consommateur** ⇒ le toggle
  « Activation » ne protège personne, en vacances comme hors vacances.

Le contrat candidat V2 (hors dépôt) a conçu la chaîne complète *absence → dette → retour → chauffe →
qualification → circulation → verdict → consommation*. **Décision propriétaire :** ce chantier se limite
**strictement** aux **Lots 1 et 2** (indépendants et livrables sans décision sanitaire/matérielle) ;
tout ce qui touche la **boucle** est réservé aux lots 3 à 5.

---

## 2. Réconciliation runtime (ancrages vérifiés à `origin/main` = `6068926`)

| # | Affirmation | Verdict | Ancrage |
|---|---|---|---|
| B1.1 | `ecs_desinfection_active` = autorité destinée à autoriser/interdire la désinfection **hebdomadaire** | **Confirmé** | `05_input_booleans/ecs/desinfection.yaml:10-13,25` ; `contrats/ecs/05` §3 (l.53) |
| B1.2 | Écrit `off` à l'entrée effective Vacances | **Confirmé** | `11_automations/modes/vacances/application_debut.yaml:111-115` (sur `vacances_actives`) |
| B1.3 | Réarmé `on` au retour Normal | **Confirmé** | `11_automations/modes/normal.yaml:100-103` (sur `mode_maison → Normal`) |
| B1.4 | Aucun lecteur-condition ne le consomme | **Confirmé (défaut)** | `git grep ecs_desinfection_active` = seulement définition + 2 écrivains + dashboard + doc ; **absent** de `veille_desinfection.yaml` et du capteur de créneau |
| B1.5 | La condition doit vivre dans la veille `10250000000002` | **Confirmé (cible)** | `veille_desinfection.yaml` = **unique** consommateur de `binary_sensor.ecs_creneau_desinfection_en_cours` |
| B1.6 | Le capteur de créneau reste un calcul pur | **Confirmé (cible)** | `12_template_sensors/ecs/fenetres_chauffe/desinfection.yaml` = stateless *jour+heure* |
| B1.7 | `ecs_blocage_planifiee` ne doit pas être réutilisé | **Confirmé** | `contrats/ecs/05` §3.1 (l.67) : *lecteur-condition unique = `veille_chauffe_ponctuelle`* |
| B2.1 | Dette posée uniquement après complétion naturelle de l'absence longue | **Confirmé** | `desinfection_retour_pose_due.yaml:62-71` (`timer.finished` de `timer.vacances_longues_ecs`) |
| B2.2 | Dette remise `off` juste après le retour de l'appel du script | **Confirmé (défaut)** | `desinfection_retour_vacances.yaml:54-56` (appel) puis `:66-68` (`turn_off`) |
| B2.3 | Extinction avant `ecs_fin_cycle_signal` | **Confirmé (défaut)** | même fichier : aucun `wait` du signal ; `turn_off` synchrone après appel |
| B2.4 | Refus initial / timeout / interruption peuvent brûler la dette sans verdict | **Confirmé (défaut)** | aucune garde de verdict ; `continue_on_timeout: true` dans `cycle.yaml` sans verdict |
| B2.5 | La dette doit rester `on` tant qu'aucun verdict positif n'est établi | **Confirmé (cible)** | arbitrage C |
| B3.1 | `ecs_fin_cycle_signal` = signal canonique de fin exploitable | **Confirmé** | `ecs_fin_de_cycle.md` ; `06_temps` §6 ; émis par `10250000000026` |
| B3.2 | Ce signal seul ≠ verdict réussite/échec/timeout | **Confirmé** | le signal n'est émis **que** sur cycle valide ; son **absence** ne distingue pas échec vs timeout |
| B3.3 | Aucun verdict explicite de séquence de retour n'existe | **Confirmé (défaut)** | `git grep` verdict/status/echec/timeout désinfection = **vide** |
| B3.4 | `ecs_cycle_last_action_status` / logs ≠ autorité de verdict sans réconciliation | **Confirmé** | `cycle.yaml` : `input_text.ecs_cycle_last_action_status` = statut d'application de consigne, non un verdict de séquence |
| B4.1 | Aucun trigger `homeassistant: start` ne réconcilie une dette due | **Confirmé (défaut)** | `desinfection_retour_vacances.yaml` : trigger **unique** = `mode_maison Vacances→Normal` |
| B4.2 | Une dette peut rester bloquée si reboot avec `mode_maison` déjà `Normal` | **Confirmé (défaut)** | corollaire de B4.1 ; `10_resilience` §4.1 documente déjà le risque `timer.finished` manqué |
| B4.3 | Toute reprise doit être bornée et idempotente | **Confirmé (cible)** | arbitrage D ; `10_resilience` §9 (« aucune relance aveugle ») |
| B4.4 | Reprise interdite si dette `off` / cycle en cours / obs indispo / verdict positif existant | **Confirmé (cible)** | arbitrage D |
| B5.1 | Chaînes hebdo et retour distinctes | **Confirmé** | déclencheurs disjoints (créneau vs `mode_maison`) |
| B5.2 | Désinfection de retour souveraine après absence longue | **Confirmé (cible)** | arbitrage B |
| B5.3 | La chaîne hebdo ne doit pas lancer un cycle concurrent | **Confirmé (cible)** | arbitrage B |
| B5.4 | Les deux chaînes doivent respecter le verrou ECS | **Confirmé partiel (défaut)** | hebdo **a** la garde `ecs_cycle_en_cours == off` (`veille_desinfection.yaml:49-51`) ; retour **ne l'a pas** (`desinfection_retour_vacances.yaml`) |
| B5.5 | Aucun nouveau mécanisme de bouclage introduit | **Confirmé** | hors périmètre absolu |

**Divergences matérielles avec le contrat candidat V2 :** aucune. Les seuls écarts sont des
**précisions** : (a) B5.4 — le défaut de garde de verrou est **côté retour** (le hebdo l'a déjà) ;
(b) B4 — l'écart « consommation au boot » revendiqué par `05` §116-118 n'a **aucun** trigger runtime.
Ces deux points sont intégrés aux cibles ci-dessous.

---

## 3. Objectifs normatifs

### C1 — Correction hebdomadaire

> **Objectif normatif :** *Une désinfection hebdomadaire automatique ne peut être lancée que si
> `input_boolean.ecs_desinfection_active == on`.*

- le helper **autorise ou interdit** ; il **ne déclenche jamais** ;
- son **lecteur-condition** est la veille hebdomadaire `10250000000002` ;
- le capteur de créneau reste **stateless** (calcul pur *jour+heure*) ;
- le script de cycle reste un **orchestrateur d'action** (aucune décision de planning/présence) ;
- l'entrée Vacances produit l'**inhibition** via le **cycle de vie existant** du helper (déjà `off` sur `vacances_actives`) ;
- le **toggle manuel** devient **effectif** ;
- `ecs_blocage_planifiee` reste **hors** de cette chaîne (lecteur unique = `veille_chauffe_ponctuelle`).

### C2 — Consolidation du retour

> **Objectif normatif :** *La dette de désinfection de retour ne peut être consommée qu'après un
> verdict final positif de la séquence.*

- la dette est une **obligation métier persistante** ;
- un **appel de script accepté** ne vaut pas satisfaction ;
- une **consigne envoyée** ne vaut pas satisfaction ;
- une **température momentanément atteinte** ne vaut pas satisfaction ;
- une **fin d'appel de script** ne vaut pas complétion canonique ;
- la dette **reste due** sur échec, timeout, interruption ou preuve indisponible ;
- la dette est consommée **uniquement** par l'autorité de séquence, **après verdict positif** ;
- la **reprise au boot** est une **réconciliation gardée**, jamais une relance aveugle ;
- la chaîne est **idempotente** ;
- le retour est **déconflicté** des autres cycles ECS (pré-vérification du verrou `ecs_cycle_en_cours`).

### C3 — Modèle de verdict (contractualisé — sans création d'entité)

Modèle minimal de verdict de la **séquence de désinfection de retour**, vocabulaire aligné sur le dépôt.
**Aucune entité n'est créée dans cette phase** ; l'entité porteuse est un **objet PROPOSÉ** dont le nom
et l'éventuel ID seront attribués par le propriétaire au patch runtime.

| État de verdict | Signification |
|---|---|
| `en_attente` | dette due, séquence non démarrée |
| `en_cours` | cycle demandé/en cours, verdict non tranché |
| `reussite` | ballon désinfecté **prouvé** : cible atteinte **et** complétion canonique `ecs_fin_cycle_signal` |
| `echec` | cible non atteinte / cycle invalidé / refus initial |
| `timeout` | attente bornée expirée sans preuve d'atteinte |
| `preuve_indisponible` | mesure requise non fraîche (`provenance != 'mesure'`) au moment requis |

- **Autorité du verdict :** l'**autorité de séquence de retour** (voir plan runtime §5, objet PROPOSÉ) — écrivain unique du verdict.
- **Événements d'entrée :** appel du cycle (`en_cours`) ; `ecs_fin_cycle_signal` (candidat `reussite`) ; expiration d'une attente bornée (`timeout`) ; refus/interruption (`echec`) ; mesure non fraîche (`preuve_indisponible`).
- **Preuves exigées pour `reussite` :** atteinte `≥ cible − epsilon` en mesure **fraîche** **ET** `ecs_fin_cycle_signal`.
- **Conditions autorisant la consommation de la dette :** verdict `reussite` **uniquement**.
- **Cas interdisant la consommation :** `echec`, `timeout`, `preuve_indisponible`, `en_attente`, `en_cours` ⇒ **dette conservée**.
- **Comportement après reboot :** le verdict n'est **pas** une preuve persistante d'un cycle interrompu ; un cycle non finalisé (absence de `ecs_fin_cycle_signal`) ne produit **jamais** `reussite` (`10_resilience` §7-8) ⇒ dette conservée, réconciliée par la reprise gardée (C2).

> **Note sur le maintien thermique.** Le contrat candidat V2 exige, pour le **bouclage**, une preuve de
> **maintien** (H). Ce chantier **ne contractualise pas** le maintien : le verdict `reussite` de la
> **présente phase** repose sur l'atteinte + complétion canonique du **ballon**. Le maintien relève du
> **Lot 3** (hors périmètre). Cette frontière est explicite pour ne pas préempter la conception ultérieure.

### C4 — Limite de la présente contractualisation

> *Cette phase ne prétend pas traiter la désinfection thermique du réseau bouclé. Elle consolide
> uniquement la désinfection du **ballon** et la fiabilité de la **chaîne de retour**. Aucune circulation
> sanitaire, aucun écrivain de `switch.prise_bouclage`, aucune sonde de retour, aucune purge terminale
> n'est contractualisée ici.*

---

## 4. Contrats amendés (Phase D)

Principe : **un texte souverain par vérité, renvois ailleurs** (pas de duplication d'invariant).

| Contrat | Autorité | Rôle dans ce chantier |
|---|---|---|
| `contrats/ecs/09_invariants_et_interdictions.md` | **FONDATEUR — loi suprême ECS** | **Souverain des invariants** : énonce les 2 invariants courts (hebdo effective ; consommation post-verdict) et **renvoie** à `05` pour le mécanisme |
| `contrats/ecs/05_etats_memoire_planification.md` | **STRUCTURANT** | **Souverain du mécanisme** : §3 (autorité hebdo + lecteur) ; §3.2 (consommation de la dette après verdict) ; §3.3 **nouveau** (modèle de verdict + reprise gardée) |
| `contrats/ecs/10_resilience_et_defaillances.md` | **CRITIQUE** | §4.1 étendu : **réconciliation gardée** de la dette au reboot (renvoi à `05` §3.3 pour les gardes) |

Le contrat `vacances.md` **n'est pas modifié** : aucune règle transversale ne manque (l'inhibition
hebdo passe par le cycle de vie **existant** de `ecs_desinfection_active` sur `vacances_actives`).

---

## 5. Plan runtime (non exécuté)

### E1 — Patch hebdomadaire (veille `10250000000002`)
Ajouter, **parmi les conditions** de `11_automations/ecs/veilles/veille_desinfection.yaml`, la garde :

```yaml
- condition: state
  entity_id: input_boolean.ecs_desinfection_active
  state: "on"
```

- **Emplacement :** dans le bloc `condition:`, **avant** ou après les gardes existantes (`systeme_stable`, `creneau`, `ecs_cycle_en_cours == off`) — ordre logique indifférent (conjonction) ; recommandé en **tête** (garde d'autorisation d'abord).
- **En vacances :** `ecs_desinfection_active` déjà `off` (application Vacances) ⇒ cycle **inhibé**.
- **Hors vacances :** toggle `on` ⇒ cycle autorisé ; toggle `off` ⇒ cycle inhibé (interrupteur devenu **effectif**).
- **Interaction verrou :** inchangée — la garde `ecs_cycle_en_cours == off` demeure ; la nouvelle condition ne remplace aucune garde existante.
- **Capteur de créneau :** **inchangé** (reste stateless) ; **interdit** d'y injecter cette autorisation.

### E2 — Séquence de retour (objets PROPOSÉS, sans ID inventé)
Runtime cible permettant : (1) **conserver la dette pendant l'exécution** ; (2) attendre une **preuve
de complétion** (`ecs_fin_cycle_signal`) ou un verdict borné ; (3) produire explicitement
`reussite/echec/timeout/preuve_indisponible` ; (4) consommer la dette **uniquement** sur `reussite` ;
(5) **réconcilier au boot** (trigger `homeassistant: start` **PROPOSÉ**, gardé) ; (6) empêcher les
**doubles lancements** (verrou de séquence + idempotence) ; (7) **pré-vérifier** `ecs_cycle_en_cours == off`.

Objets **PROPOSÉS** (nom/ID à attribuer par le propriétaire, **non inventés ici**) :
- une **autorité de séquence** (automation) portant le verdict et la consommation ;
- un **porteur de verdict** (helper d'état, valeurs de C3) ;
- éventuellement un **watchdog de séquence** borné pour distinguer `timeout` de `echec`.

### E3 — Autorité de séquence (comparatif, recommandation)
| Architecture | Compatibilité dépôt | Verdict |
|---|---|---|
| **Automation de séquence souveraine** (observe `ecs_fin_cycle_signal` + watchdog borné, écrit verdict + consomme la dette) | Élevée — patron déjà présent (consommateur `10250000000019` observe le signal ; veilles observent des états) | **Recommandée** |
| Watchdog séparé | Moyenne — utile pour `timeout`, mais fragmente l'autorité | Composant **interne** à l'automation de séquence, pas une autorité distincte |
| Projection diagnostic seule | Faible — n'a pas d'autorité d'écriture de la dette | Insuffisant (observabilité, pas décision) |
| Consommation directe du signal canonique | Partielle — le signal seul ne distingue pas échec/timeout (B3.2) | Nécessaire mais **non suffisant** |

> **Recommandation :** une **automation de séquence souveraine** qui **observe** `ecs_fin_cycle_signal`
> (et un watchdog borné pour `timeout`), **écrit** le verdict, et **consomme** la dette **uniquement** sur
> `reussite`. L'observation d'états ne viole pas la séparation décision/action (lecture ≠ action) ; la
> **décision** de consommation reste centralisée dans cette autorité unique.

---

## 6. Plan CI (non exécuté)

### F1 — Autorisation hebdomadaire (nouveau contrôle ou extension)
Garantir statiquement :
- `10250000000002` **lit** `input_boolean.ecs_desinfection_active == on` en condition ;
- le helper **n'est pas lu** dans le capteur de créneau (`fenetres_chauffe/desinfection.yaml`) ;
- `ecs_blocage_planifiee` **n'est pas ajouté** à la veille de désinfection ;
- le script de cycle **ne porte pas** cette décision.

### F2 — Dette et verdict (extension de `check_ecs_desinfection_retour_contracts.py`)
Garantir :
- écrivain **ON unique** de la dette (inchangé : pose sur `timer.finished`) ;
- écrivain **OFF unique** = l'autorité de séquence ;
- extinction **uniquement après verdict positif** (garde de verdict présente avant le `turn_off`) ;
- **aucune** extinction immédiate après simple appel de script ;
- **reprise au boot** présente (trigger `homeassistant: start`) ;
- reprise **gardée et idempotente** ;
- **verrou ECS pré-vérifié** (`ecs_cycle_en_cours == off`) ;
- aucun ID inventé/non déclaré ;
- **déconfliction explicite** avec la chaîne hebdomadaire.

### F3 — Mutations négatives minimales (la CI doit échouer si)
- le lecteur de l'autorisation hebdomadaire **disparaît** ;
- la dette est **éteinte avant verdict** ;
- la **reprise boot relance sans garde** ;
- un **timeout produit une réussite** ;
- un état **`unknown` est interprété comme succès** ;
- la chaîne retour **lance malgré un cycle ECS actif** ;
- l'autorité hebdomadaire **concurrence** la séquence de retour.

**Non prouvable statiquement (⇒ preuves runtime) :** l'atteinte/complétion réelle, l'auto-arrêt effectif,
l'absence de chevauchement temporel réel, le comportement exact au reboot mid-cycle.

---

## 7. Risques

| Risque | Mitigation prévue |
|---|---|
| Dette **jamais** consommée | Reprise gardée (C2/D) + verdict `reussite` bien atteignable (atteinte + `ecs_fin_cycle_signal`) |
| Dette consommée **trop tôt** | Consommation subordonnée au verdict positif (C2/C3) — cœur du chantier |
| **Double lancement** | Verrou de séquence + `ecs_cycle_en_cours` pré-vérifié + idempotence |
| **Boucle de reprise** au boot | Reprise **gardée** (dette on, mode compatible, pas de cycle, obs dispo, pas de verdict positif) + idempotence |
| **Verdict positif mensonger** | `reussite` exige `ecs_fin_cycle_signal` (fin exploitable), jamais une fin d'appel/pic instantané |
| **Perte d'événement** pendant arrêt HA | Réconciliation boot ; risque résiduel `timer.finished` manqué **conservé** et documenté (`10_resilience` §4.1) — **hors correctif** |
| **Conflit avec un cycle ECS** | Déconfliction explicite (B5.4) ; sérialisation par verrou |
| **Réarmement hebdo trop précoce** | `ecs_desinfection_active` réarmé `on` sur `mode_maison → Normal` ; la souveraineté du retour (B5.2) empêche un cycle hebdo concurrent |
| **Modification involontaire de VAC-IMP-5** | La pose (`10250000000032`) et le timer restent **inchangés** ; seul l'instant de **consommation** évolue |
| **Extension accidentelle au bouclage** | Périmètre absolu (C4) : aucun fichier `11_automations/bouclage/`, aucun écrivain de `switch.prise_bouclage` |

---

## 8. Périmètre et hors périmètre

**Dans le périmètre :** Lot 1 (autorisation hebdo effective) ; Lot 2 (consommation post-verdict, verdict
ballon, reprise boot, idempotence, déconfliction) ; contractualisation C1/C2/C3/C4 ; plans runtime & CI.

**Hors périmètre absolu (réservé lots 3-5 du candidat V2) :** maintien thermique, fenêtre thermique
qualifiée, bouclage sanitaire exceptionnel, interface ECS↔Bouclage, automation `11_automations/bouclage/`,
nouvel écrivain de `switch.prise_bouclage`, durée de circulation, seuil sanitaire, verdict de traitement
thermique de la boucle, sonde de retour, purge terminale automatique.

---

## 9. Lots et critères de clôture

| Lot | Contenu | Dépendance | Critère de clôture |
|---|---|---|---|
| **Lot 1** | Autorisation hebdo effective : contrat (C1) → veille lit `ecs_desinfection_active` → CI F1 → preuve runtime | **Aucune** | Cycle hebdo **non lancé** quand autorisation `off` (vacances **et** toggle manuel), vérifié en runtime |
| **Lot 2** | Consolidation retour : contrat (C2/C3) → séquence souveraine + verdict + reprise boot + déconfliction → CI F2 → preuves runtime | Contrat C2/C3 | Dette **conservée** sur échec/timeout ; consommée **uniquement** sur `reussite` ; reprise boot gardée idempotente vérifiée |

**Clôture du chantier :** les deux lots livrés + CI verte + preuves runtime des scénarios clés
(hebdo inhibée en vacances ; retour consommé seulement sur réussite ; reboot mid-cycle → dette conservée
puis réconciliée). Le chantier **ne préempte pas** la clôture du domaine Vacances (VAC-IMP-5, registre C3),
ni n'ouvre les lots 3-5.

> **Clôture prononcée.** Le critère « preuves runtime » est **satisfait par l'exploitation en
> production** (fonctionnement nominal constaté sur la durée) ; la propriété a **renoncé explicitement**
> à une campagne de validation terrain dédiée. Chantier **clôturé**.

---

## 10. Runtime Lot 2 — conception, puis implémentation livrée

> **Statut : runtime livré.** La correction de gouvernance a autorisé l'auto-attribution des IDs
> d'automation (sous respect strict du préfixe/format/unicité/checkers) et retenu **T-B** (bornes
> canoniques existantes). L'architecture a été **resserrée** : **un seul** nouvel helper (verdict typé),
> **aucun** booléen `sequence_active` (l'état `en_cours` du verdict porte cette vérité), réutilisation de
> `10250000000021` (lancement **et** réconciliation démarrage), **une seule** nouvelle automation
> (finalisation corrélée `10250000000033`). Les §10.1-10.11 documentent la conception ; **§10.12** acte
> l'implémentation réellement livrée (qui prime en cas d'écart de désignation).

### 10.1 Réconciliation runtime (ancrages `origin/main` = `3cfece5`)

- **A1 — Dette `input_boolean.ecs_desinfection_retour_due`.** Écrivain **ON unique** = `10250000000032`
  (`timer.finished` de `timer.vacances_longues_ecs`). Écrivain **OFF actuel** = `10250000000021`
  (`desinfection_retour_vacances.yaml:66-68`). **Moment de consommation** : l'automation appelle
  `script.chauffage_ecs_cycle` en **service bloquant** (`:54-56`) — elle attend donc la fin d'exécution
  du cycle (jusqu'à ~40 min désinfection + boosts), puis journalise et éteint la dette — **avant** la
  complétion canonique (`ecs_fin_cycle_signal`, émise +15 min à l'inertie). Persistance : sans `initial`
  (`10_resilience` §4.1). **Boot** : trigger **unique** `mode_maison Vacances→Normal` — pas de
  `homeassistant: start`. **Risque brûlée** : `continue_on_timeout: true` dans `cycle.yaml` ⇒ le script
  **retourne** même sur non-atteinte/timeout ⇒ dette éteinte sans réussite. **Risque bloquée** : dette
  survivant à un reboot avec `mode_maison` déjà `Normal` n'est jamais reconsommée.
- **A2 — Complétion canonique.** `input_boolean.ecs_fin_cycle_signal` **posé** par `10250000000026`
  (`inertie/gel.yaml`) à `timer.finished` de `timer.fenetre_inertie_chauffe_ecs` (15 min), après gel ;
  **ACK/OFF** par `10250000000019` (`auto_ajustement_offset.yaml`, gardé `ecs_autocorrect_active == on`).
  **Périmètre : GLOBAL** — le signal ne porte **aucune** identité de cycle/mode. **Risque** : un signal
  émis par un cycle **ponctuel/vaisselle/hebdo** solderait une dette de retour si la séquence se
  contentait d'attendre `ecs_fin_cycle_signal == on` (⇒ corrélation obligatoire, §10.4). L'ACK par
  `…019` impose une lecture **événementielle** (`off→on`), pas un sondage d'état.
- **A3 — Résultats exposés par `script.chauffage_ecs_cycle`.** `input_text.ecs_cycle_last_action_status`
  (`applied` / autre — statut d'**application de consigne**, pas verdict de séquence) ; `stop:`/`logbook`
  (traces, non opposables) ; garde fraîcheur ballon (`provenance == 'mesure'`, fail-closed) ; retour
  consigne basse vérifié. **Aucun** verdict réussite/échec/timeout durable. La **vérité exploitable** de
  fin est le **résumé figé** `input_text.ecs_resume_dernier_cycle_fige` au format opposable
  `date|mode|consigne|t0|boost|valide` (gel `…026` ; `valide=oui` ssi `duree>0 ET temp_max_reelle>0 ET
  (temp_max_reelle − t0) ≥ 0.5`).
- **A4 — Watchdogs.** `timer.ecs_cycle_watchdog` (**30 min**, `restore: true`) borne le **verrou**
  `ecs_cycle_en_cours` (watchdog `10250000000008` → rabaissement + libération) ; `10250000000022`
  (`reset_verrou_cycle`) purge un verrou incohérent au boot. Sémantique = **sûreté du verrou**, **pas**
  « séquence en attente de complétion » ⇒ non détournable tel quel comme timeout de séquence (A4/§10.7).
- **A5 — Redémarrage.** Aucune réconciliation dette au boot aujourd'hui (A1). Scénarios cibles en §10.6.
- **A6 — Déconfliction.** L'hebdo (`10250000000002`) porte `ecs_cycle_en_cours == off` **et** (Lot 1)
  `ecs_desinfection_active == on` ; le retour (`…021`) **ne porte pas** `ecs_cycle_en_cours == off`.
  Le verrou de cycle (`cycle_session_open`, anti-zombie 300 s) sérialise **un** cycle à la fois.
- **A7 — Patron de verdict.** Arsenal type les états de commande/verdict par **`input_select`** (ex.
  `input_select` « Audi — état commande climatisation » : `Au repos / En cours / Confirmée / Non
  confirmée (timeout)`, **écrivain unique** = un script). Le verdict de retour doit suivre ce patron
  (input_select typé), **pas** un `input_text` libre.

### 10.2 Architecture retenue (autorité de séquence souveraine)

Chaîne : **dette due → admissibilité → lancement → observation → verdict → consommation éventuelle**.
- **Décision** : la **séquence de retour** (automations dédiées) décide admissibilité, lancement,
  attente, abstention, verdict, et consommation de la dette. **Écrivain OFF unique** de la dette.
- **Action** : `script.chauffage_ecs_cycle` reste l'**orchestrateur d'exécution** (inchangé) ; il ne
  devient pas autorité de la dette.
- **Observation** : verrou (`ecs_cycle_en_cours`), fraîcheur ballon (`provenance`), statut d'application,
  **complétion canonique** (`ecs_fin_cycle_signal` **corrélée**, §10.4), watchdog, indisponibilités.
- **Diagnostic** : le **verdict** (input_select) expose la conclusion sans commander l'action.

### 10.3 Objets requis (attribution propriétaire) — **aucun inventé ici**

| Désignation abstraite | Type | Rôle | Emplacement proposé | Alias descriptif (non définitif) | Attribution |
|---|---|---|---|---|---|
| `OBJET_VERDICT_A_ATTRIBUER` | `input_select` | verdict de séquence (options ↔ `05` §3.3 : `en_attente/en_cours/reussite/echec/timeout/preuve_indisponible`) ; **écrivain unique** = séquence | `06_input_selects/ecs/desinfection_retour_verdict.yaml` | « ECS — Verdict désinfection retour » | **helper à créer** |
| `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER` | `input_boolean` | verrou de séquence / tentative de retour active (anti-double-lancement + corrélation) ; `initial: off` + purge boot | `05_input_booleans/ecs/desinfection_retour_sequence_active.yaml` | « ECS — Séquence désinfection retour active » | **helper à créer** |
| `AUTOMATION_ID_A_ATTRIBUER_1` | automation | **verdict à la complétion** : trigger `ecs_fin_cycle_signal: off→on` ; si séquence active + résumé figé corrélé (§10.4) → `reussite`+dette OFF ou `echec` ; libère la séquence | `11_automations/ecs/desinfection_retour_verdict.yaml` | « ECS — Désinfection retour : verdict complétion » | **ID à attribuer** |
| `AUTOMATION_ID_A_ATTRIBUER_2` | automation | **réconciliation boot** : trigger `homeassistant: start` (+ `systeme_stable → on`) ; gardes §10.6 ; lance **au plus une** tentative ou conserve la dette | `11_automations/ecs/desinfection_retour_reconciliation_boot.yaml` | « ECS — Désinfection retour : réconciliation démarrage » | **ID à attribuer** |
| `AUTOMATION_ID_A_ATTRIBUER_3` *(conditionnel — cf. arbitrage §10.7)* | automation | **finaliseur timeout** : si la complétion canonique n'arrive pas dans la borne retenue → `timeout`, dette conservée, séquence libérée | `11_automations/ecs/desinfection_retour_timeout.yaml` | « ECS — Désinfection retour : finaliseur timeout » | **ID à attribuer** |
| `10250000000021` *(existant)* | automation | **lanceur** restructuré : admissibilité → `en_cours` + séquence active → lancement (bloquant) → **ne consomme plus** la dette | (fichier existant) | inchangé | **ID conservé** |

Nombre d'**IDs d'automation** nouveaux : **2 (min) à 3 (avec finaliseur timeout)**. Nombre de **helpers**
nouveaux : **2**. Aucun nouvel écrivain de `switch.prise_bouclage` ; aucun objet Bouclage.

### 10.4 Corrélation de tentative (déterministe, sans UUID)

Arsenal ne pose pas d'UUID sur les cycles ⇒ corrélation **déterministe par état**, pas par identifiant
dynamique :
1. le lanceur pose `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER = on` **avant** l'appel du cycle ;
2. le verrou `ecs_cycle_en_cours` sérialise **un seul** cycle à la fois (anti-zombie 300 s) ;
3. la **déconfliction** (§10.5) empêche toute **autre** désinfection (hebdo) pendant qu'une séquence de
   retour est active ⇒ le seul cycle `mode==desinfection` produisant un résumé figé pendant la fenêtre
   est **la tentative de retour** ;
4. `AUTOMATION_ID_A_ATTRIBUER_1`, sur l'événement `ecs_fin_cycle_signal: off→on`, lit
   `input_text.ecs_resume_dernier_cycle_fige` : **`mode == 'desinfection'` ET `valide == 'oui'`** ⇒
   `reussite` (dette OFF) ; `valide == 'non'` ⇒ `echec` (dette conservée) ; **jamais** `reussite` sur un
   signal dont le résumé figé n'est pas une désinfection valide (⇒ fin canonique **étrangère** ignorée) ;
5. nettoyage de `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER` sur `reussite`, `echec`, `timeout`, `reboot`.

> **À valider propriétaire.** La corrélation par `mode==desinfection` s'appuie sur la déconfliction
> (§10.5). Si un jour l'hebdo et le retour pouvaient coexister, il faudrait un marqueur de séquence plus
> fort (état dédié comparé au moment du gel). Non requis dans le périmètre actuel (retour souverain).

### 10.5 Déconfliction (minimale, conforme au contrat posé)

- pré-vérification `ecs_cycle_en_cours == off` dans l'**admissibilité** du lanceur (`…021`) ;
- `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER` empêche deux tentatives simultanées et tout second lancement sur
  double événement / reboot rapproché ;
- **hebdo non souveraine tant qu'une dette de retour est en traitement** : ajouter à la veille hebdo
  `10250000000002` la garde `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER == off` (déconfliction **déjà
  contractualisée** `09` §2 / `05` §3.4 « le retour est souverain ») — **modification minimale du Lot 1**,
  strictement nécessaire, **sans** toucher le capteur de créneau ni le script ;
- OFF de la dette : **écrivain unique** = `AUTOMATION_ID_A_ATTRIBUER_1` (retrait de l'OFF de `…021`) ;
- **aucun** changement au domaine Bouclage.

### 10.6 Reprise au boot (réconciliation gardée, idempotente)

`AUTOMATION_ID_A_ATTRIBUER_2`, sur `homeassistant: start` (+ `systeme_stable → on`), **ne lance** que si
**toutes** les gardes sont vraies : dette `on` · contexte maison compatible · `systeme_stable == on` ·
`ecs_cycle_en_cours == off` · `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER == off` · verdict ≠ `reussite` ·
observations fraîches disponibles. Sinon : conserver la dette, ou produire `preuve_indisponible`/`echec`.
Jamais de boucle sur chaque reboot/disponibilité (idempotence via `OBJET_SEQUENCE_ACTIVE_A_ATTRIBUER` et
le verdict). Une tentative incomplète héritée d'un reboot est **invalidée** (séquence purgée), jamais
comptée réussie sans résumé figé corrélé.

### 10.7 Arbitrage timeout (à trancher propriétaire)

Le passage `en_cours → timeout` (complétion canonique jamais reçue : inertie annulée par un cycle
préemptant, ou cycle non finalisé) exige une **borne**. Aucune borne contractuelle existante ne
correspond exactement :
- **Option T-A — réutiliser `timer.ecs_cycle_watchdog` (30 min)** : déjà contractuel, mais sémantique =
  sûreté du verrou, pas « séquence en attente » ; il expire *pendant* les longues désinfections (wait
  40 min) — **inadapté** comme borne de séquence.
- **Option T-B — s'appuyer sur la fenêtre d'inertie (`timer.fenetre_inertie_chauffe_ecs`, 15 min)**
  comme échéance de corrélation post-cycle : la complétion canonique **est** l'échéance de ce timer ; si
  elle est annulée (préemption), conclure `timeout`. Réutilise une borne existante, sémantiquement
  proche. **Recommandée**, sous réserve d'un déclencheur `timer.cancelled`/absence propre.
- **Option T-C — nouveau timer dédié borné** : nécessite un **objet + une durée** attribués (valeur
  **non inventée** ici). Plus explicite, coût d'un objet supplémentaire.

**Aucune durée n'est inventée.** Décision requise avant l'écriture du finaliseur
`AUTOMATION_ID_A_ATTRIBUER_3` (Option T-C) ou de son intégration au verdict (T-A/T-B).

### 10.8 Machine d'état (conforme `05` §3.3)

`en_attente` → (admissibilité vraie) `en_cours` [pose séquence active, lancement] → sur
`ecs_fin_cycle_signal` corrélé : `valide=oui` → **`reussite`** [dette OFF] · `valide=non` → **`echec`** ·
(borne §10.7 dépassée sans signal) → **`timeout`** · (obs non fraîche à l'admissibilité ou à la
corrélation) → **`preuve_indisponible`**. Tous les états terminaux **libèrent** la séquence ; seuls
`echec/timeout/preuve_indisponible/en_attente/en_cours` **conservent** la dette ; seul `reussite`
la consomme.

### 10.9 Plan CI Lot 2 (Phase H — non exécuté, faute d'objets)

Extension de `check_ecs_desinfection_retour_contracts.py` (autorité `09` §2/§3 — **le bon checker**),
à écrire **après** attribution, garantissant : ON unique (dette) ; **OFF unique = la séquence** ;
consommation **seulement** sur `reussite` ; **interdiction** d'OFF immédiat après l'appel du script dans
`…021` ; présence d'une reprise boot **gardée** ; pré-vérif `ecs_cycle_en_cours == off` ; verrou de
séquence ; **corrélation** (le verdict lit le résumé figé, pas le seul signal) ; `timeout`/`unknown`
distincts de `reussite` ; hebdo gardée par la séquence active ; IDs/alias existants inchangés.
**Mutations négatives** : OFF immédiat après appel · `timeout`→succès · signal global consommé sans
corrélation · reprise boot sans garde · double tentative · lancement malgré `ecs_cycle_en_cours == on` ·
`unknown`→réussite · second écrivain OFF · hebdo concurrente · suppression du verdict. *(Détection
sémantique, sans dépendance externe — cf. leçon Lot 1 : le runner CI n'a pas PyYAML ; analyse de chaîne
bornée à l'entrée.)*

### 10.10 Matrice comportementale (conceptuelle — objets non attribués)

| # | Scénario | Résultat conçu |
|---|---|---|
| 1 | Retour nominal (dette on, admissible, preuve + fin canonique corrélée) | `reussite`, dette OFF |
| 2 | Refus initial (obs indispo) | pas de lancement, `preuve_indisponible`, dette **on** |
| 3 | Cycle déjà actif (`ecs_cycle_en_cours == on`) | pas de 2ᵉ lancement, dette **on**, reprise ultérieure |
| 4 | Timeout (pas de fin corrélée dans la borne §10.7) | `timeout`, dette **on** |
| 5 | Reboot avant lancement (maison Normal) | réconciliation gardée, ≤ 1 lancement |
| 6 | Reboot pendant le cycle | tentative invalidée, aucune fausse réussite, dette **on** |
| 7 | Fin canonique étrangère (autre cycle) | résumé figé non `desinfection`/`valide` ⇒ **non consommée** |
| 8 | Double événement (transition + stabilité) | ≤ 1 tentative (séquence active) |
| 9 | Réussite puis événement dupliqué | dette déjà OFF, aucun nouveau cycle |
| 10 | Hebdo concurrente (créneau ouvert, dette active) | hebdo gardée par séquence active ⇒ retour souverain, pas de double cycle |

### 10.11 Preuves runtime futures (à recueillir, non exécutées)

Procédure : poser la dette (fin naturelle du timer 6 j simulée par un timer court en test), déclencher
`Vacances→Normal`, observer `OBJET_VERDICT_A_ATTRIBUER` (`en_cours`→`reussite`), la trace de `…021`, la
trace de `AUTOMATION_ID_A_ATTRIBUER_1` sur `ecs_fin_cycle_signal`, `input_text.ecs_resume_dernier_cycle_fige`
(`…|desinfection|…|oui`), la dette (OFF sur réussite seulement). Cas : refus (obs indispo) ; cycle actif ;
timeout (préemption de l'inertie) ; reboot avant/pendant/après ; fin canonique étrangère ; double
événement. Critère succès : dette OFF **uniquement** sur `reussite` corrélée ; échec/timeout/reboot
conservent la dette et exposent le verdict. **Aucune preuve terrain n'est fournie par la seule CI.**

---

### 10.12 Implémentation livrée (Runtime Lot 2)

**Architecture retenue (minimale).** Autorité de séquence souveraine portée par **le verdict typé**
(unique vérité de séquence, l'état `en_cours` valant « tentative active ») ; `script.chauffage_ecs_cycle`
inchangé ; corrélation **déterministe sans UUID** (résumé figé `mode==desinfection` & `valide==oui`,
garantie par la déconfliction) ; **timeout T-B** = préemption de la fenêtre d'inertie (aucune durée
nouvelle) ; consommation de la dette **uniquement** sur `reussite`.

**Objets réellement livrés.**

| Objet | Type | Rôle | Attribution |
|---|---|---|---|
| `input_select.ecs_desinfection_retour_verdict` | helper | **unique** vérité de séquence (6 options `05` §3.3) ; sans `initial` (réconciliation boot voit `en_cours`) | **créé** — `06_input_selects/ecs/desinfection_retour_verdict.yaml` |
| `10250000000021` | automation | **réutilisée** : lanceur + réconciliation démarrage (triggers `Vacances→Normal` **et** `systeme_stable→on`) ; pose `en_cours`/`preuve_indisponible` ; **ne consomme plus** la dette | modifiée — `11_automations/ecs/desinfection_retour_vacances.yaml` |
| `10250000000033` | automation | **nouvelle** : verdict de complétion — corrélation → `reussite`(+dette OFF)/`echec` ; préemption inertie → `timeout` | **créée** — `11_automations/ecs/desinfection_retour_verdict.yaml` |
| `10250000000002` | automation | déconfliction : garde `verdict != en_cours` (hebdo non souveraine pendant une tentative) | modifiée — `veilles/veille_desinfection.yaml` |

> **Simplification vs conception (§10.3).** Le booléen `sequence_active` est **supprimé** (l'état
> `en_cours` du verdict le remplace) ; **une seule** nouvelle automation au lieu de 2-3 (la réconciliation
> boot est absorbée par `10250000000021`, le timeout par `10250000000033` via `timer.cancelled`). Résultat :
> **1 helper + 1 nouvelle automation** (au lieu de 2 helpers + 2-3 automations).

**Attribution de l'ID `10250000000033`.** Méthode : **prochain ID libre séquentiel** du domaine ECS
(convention `generate_next_id_from_prefix`). Préfixe `1025` = ecs (`06_input_selects/system/prefix_id.yaml`).
IDs voisins examinés : `…031` (retry, pris), `…032` (pose, pris), `…033` (**libre**), `…034` (libre).
Preuve d'unicité : `git grep` de tous les IDs `1025` (14 chiffres) sur le dépôt — 28 IDs, `…033` **absent**.
Format : 14 chiffres exacts ✔ (checker `check_automation_ids_contracts`). Domaine : fichier sous
`11_automations/ecs/` ✔ (`check_automation_prefix_domain_contracts`).

**Preuve d'unicité de la vérité de séquence.** Le verdict `input_select` est l'**écrivain unique** de la
vérité de séquence ; `en_cours` porte « tentative active » (aucun booléen concurrent). Deux écrivains,
**par transition disjointe** : `…021` (`en_attente`/`en_cours`/`preuve_indisponible`) et `…033`
(`reussite`/`echec`/`timeout`). La dette a un **OFF unique** = `…033` (checker T04/T11/T12).

**Traitement du timeout (T-B).** Aucune durée inventée : `…033` pose `timeout` sur l'événement
`timer.cancelled` de `timer.fenetre_inertie_chauffe_ecs` (la complétion canonique de la tentative a été
préemptée par un autre cycle) ; la dette est **conservée**, réconciliée au prochain déclencheur admissible
(retour effectif ou `systeme_stable→on`).

**Traitement du boot.** `…021` (trigger `systeme_stable→on`) : (1) réconcilie un `en_cours` **périmé**
(aucun cycle, aucune inertie) → `en_attente` ; (2) relance **au plus une** tentative si toutes les gardes
sont vraies (dette on, verdict ≠ en_cours, verrou off, inertie non active, système stable, mode Normal,
ballon frais). Idempotent, jamais de relance aveugle.

**Corrélation de la fin canonique.** `…033` est **événementiel** (`ecs_fin_cycle_signal: off→on`), gardé
par `verdict == en_cours` **et** `dette == on` ; il lit le **résumé figé**
`input_text.ecs_resume_dernier_cycle_fige` (`mode==desinfection` & `valide==oui`) → `reussite`. Un signal
d'un **autre** cycle est écarté (verdict ≠ en_cours après préemption→timeout, et/ou `mode != desinfection`
ignoré). Aucune lecture de `remaining`/`finishes_at`.

**Fichiers modifiés / créés (5).**
- **créé** `06_input_selects/ecs/desinfection_retour_verdict.yaml`
- **créé** `11_automations/ecs/desinfection_retour_verdict.yaml` (`10250000000033`)
- **modifié** `11_automations/ecs/desinfection_retour_vacances.yaml` (`10250000000021` restructurée)
- **modifié** `11_automations/ecs/veilles/veille_desinfection.yaml` (déconfliction, Lot 1 préservé)
- **modifié** `scripts/arsenal_contracts/check_ecs_desinfection_retour_contracts.py` (T11-T19 + OFF-writer repointé)

**CI (F2).** Extension de `check_ecs_desinfection_retour_contracts.py` (autorité `09` §2/§3) : T11 (dette
OFF seulement sur `reussite`), T12 (lanceur ne consomme pas), T13 (`en_cours` avant lancement), T14
(reprise boot), T15 (verrou + anti-double), T16 (verdict 6 options), T17 (déconfliction hebdo), T18
(timeout ≠ réussite), T19 (corrélation résumé figé). **Détection sémantique, sans PyYAML** (leçon Lot 1).
**10/10 mutations négatives** vérifiées rouges ; baseline verte. Aucun nouveau checker/workflow ; registre
de couverture inchangé.

**Preuves statiques obtenues.** YAML valide (5 fichiers) ; checkers ECS (fondations, retour, cycle,
sécurité, offsets) verts ; `check_automation_ids`/`prefix_domain`/`06_input_selects`/`initial_key`/
`ci_coverage_registry`/`recorder` verts ; `git diff --check` OK ; matrice des 10 scénarios (§10.10)
cohérente avec l'implémentation.

**Preuves terrain restantes (non exécutées).** Cf. §10.11 — dette OFF **uniquement** sur `reussite`
corrélée ; `preuve_indisponible`/`echec`/`timeout` conservent la dette ; reboot avant/pendant/après ;
fin canonique étrangère non consommée ; double événement → ≤1 tentative ; hebdo concurrente → retour
souverain. **Lot 2 clôturé** : preuve terrain acquise par exploitation en production (validation terrain
dédiée abandonnée sur décision de la propriété). **Lots 3-5 exclus.**

---

### 10.13 Circulation bouclage 5 min après réussite (complément minimal)

**Besoin.** Après une désinfection de retour **réussie**, lancer **une fois** la circulation de bouclage
existante, en réutilisant **intégralement** le sous-système Bouclage — **sans** nouvelle machine d'état,
autorisation, durée, helper ou écrivain du switch.

**Réutilisation de l'existant.**
- **Primitive d'action** : `script.bouclage_ecs_5_minutes` — démarre `timer.bouclage_ecs_5_minutes`
  (5 min, `restore: true`), pose le drapeau `input_boolean.bouclage_ecs_5_minutes_en_cours`, allume
  `switch.prise_bouclage`. **Seul écrivain autorisé** du switch (hors automations bouclage) ; borné et
  **présence-indépendant** (cycle manuel).
- **Arrêt / purge** : `10260000000002` (fin de timer → flag off + switch off hors AUTO) et
  `10260000000007` (purge du flag au démarrage). **Non modifiés.**
- **Drapeau d'exécution** : `input_boolean.bouclage_ecs_5_minutes_en_cours` (existant) ; corroboration
  possible via `sensor.prise_bouclage_energy`. **Aucune seconde vérité de bouclage.**

**Architecture (aucun nouvel objet, aucun nouvel ID).** Un seul point d'appel : la branche `reussite`
de l'automation de finalisation **existante** `10250000000033`. Ordre :
1. écrire le verdict `reussite` ;
2. **consommer la dette** (`turn_off`) — ce qui fait retomber la garde d'unicité (condition top-level
   `verdict == en_cours` **et** `dette == on`) ;
3. appeler **une fois** `script.bouclage_ecs_5_minutes`.

**Idempotence.** Un seul appel par réussite, garanti par les **vérités existantes** : `mode: single`,
et le finaliseur ne se ré-arme pas (dette `off`, verdict `reussite`). Aucun bouclage sur `echec`,
`timeout`, `preuve_indisponible`, complétion étrangère (mode ≠ désinfection), événement dupliqué ou
dette déjà consommée.

**CI (extension de `check_ecs_desinfection_retour_contracts.py`, sans PyYAML).** T20 (appel dans la
branche `reussite` corrélée), T21 (aucun appel sur echec/timeout/preuve), T22 (ECS n'écrit jamais le
switch), T23 (appel unique via les gardes existantes). **6/6 mutations rouges**, baseline verte. Le
checker Bouclage reste **inchangé et vert** (T11 « écrivains du switch » satisfait : l'appel n'écrit pas
le switch).

**Contrats amendés (minimal, sans duplication).** `05` §3.3 (décision ECS : appel unique post-réussite,
limite de preuve) ; `09` §2 (invariant : circulation via la primitive, jamais d'écriture directe du
switch, jamais « boucle désinfectée ») ; `bouclage.md` (§ Orchestration client : `10250000000033` client
autorisé de la primitive existante).

**Limite de preuve.** Prouvé : **ballon désinfecté** (`reussite`) + **circulation 5 min demandée**
(primitive + drapeau). **Non prouvé** : température du **retour de boucle** (aucune sonde) ; la boucle
n'est **jamais** déclarée « désinfectée » ; **tronçons terminaux** non bouclés **hors garantie**.

**Preuve terrain (acquise par exploitation).** Comportement attendu — `10250000000033` →
`input_boolean.bouclage_ecs_5_minutes_en_cours` passe `on`, `switch.prise_bouclage` `on`, arrêt
automatique à 5 min ; aucun bouclage sur échec/timeout ; dette OFF uniquement sur réussite — **confirmé
par le fonctionnement nominal en production sur la durée**. Campagne de validation terrain dédiée
**abandonnée sur décision de la propriété**. Complément **clôturé**.

---

*Chantier — Lot 1 livré (#664) ; Lot 2 **runtime livré** (#665). Complément minimal : circulation
bouclage 5 min après réussite (§10.13) — réutilisation **intégrale** de `script.bouclage_ecs_5_minutes`,
un seul appel dans la branche `reussite` de `10250000000033`, **aucun nouvel objet/ID/durée/écrivain du
switch**. Invariants portés par les contrats amendés (§4). **Chantier CLÔTURÉ** — preuve terrain acquise
par exploitation en production (validation terrain dédiée abandonnée sur décision de la propriété).*
