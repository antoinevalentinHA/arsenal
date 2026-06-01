# Dossier de conception — CH-1 Alarme

> **Chantier :** CH-1 — Sémantique des ouvrants d'entrée & confirmation d'intrusion
> **Périmètre :** **ALM-CRIT-1**, **ALM-CRIT-2** (cœur) ; **ALM-MIN-5** (corollaire de la chaîne sirène)
> **Sources :** `01_rapports/alarme/audit_alarme_rapport_officiel.md`, `03_plans_action/alarme/plan_action_alarme.md`, `04_chantiers/alarme/backlog_alarme.md`
> **État du dépôt à la rédaction :** `origin/main` = `99cbc0b` (post-CH-2)
> **Nature :** dossier de conception — **analyse et options uniquement**. Aucun patch, aucun YAML, aucune correction. Les arbitrages restent ouverts.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet et délimitation

Ce dossier analyse **exclusivement** la voie d'accès principale (porte d'entrée, garage) et la chaîne « ouverture → délai d'entrée → confirmation d'intrusion → sirène ». Il cartographie les flux réels au runtime, isole les producteurs/consommateurs/dépendances, explique le mécanisme précis des deux défauts critiques, et propose les options architecturales possibles. Il ne tranche pas et ne produit aucune modification.

Hors périmètre explicite : la décision d'armement (cerveau, CH-2/CH-3), le clavier PIN (ALM-CRIT-3 / CH-6), le babysitting (ALM-IMP-1 / CH-3), l'auto-extinction sirène (ALM-IMP-3 / CH-4). La chaîne sirène n'est traitée ici que pour le point d'entrée « fin de délai » (MIN-5).

---

## 2. Cartographie des flux

### 2.1 Vue d'ensemble (état armé `armed_away`)

```
   Ouverture porte/garage (physique : *_1 / *_2)
        │
        ├──► [chaîne réconciliée]  capteurs_redondants.yaml
        │        └─ binary_sensor.contact_entree_porte / contact_garage
        │              └─► AUTO 1002000000007  autres.yaml  (chemin IMMÉDIAT)
        │                     garde : delai_desarmement_en_cours == off
        │                     └─► alarm_trigger ──► state "triggered"
        │
        └──► [chaîne permissive]  ouvrants_entree.yaml
                 └─ binary_sensor.alarme_ouverture_entree / alarme_ouverture_garage
                       └─► AUTO 10020000000031  delai_entree_start.yaml  (front off→on)
                              garde : armed_away + timer idle
                              └─► timer.start(timer.delai_entree, durée=input_number.alarme_delai_entree)
                                     └─ binary_sensor.delai_desarmement_en_cours = (timer == active)
                                            │
                  désarmement ─► AUTO 10020000000033 timer_cancel ─► timer.cancel ─► (plus de finished)
                                            │
                              timer.finished
                                     └─► AUTO 10020000000032  delai_entree_fin.yaml
                                            garde : systeme_stable + armed_away
                                                    + ouverture_qualifiee_maison == on   ◄── CRIT-2
                                            └─► alarm_trigger ──► "triggered"
                                            └─► script.sirene_brutale (DIRECT)            ◄── MIN-5

   state "triggered"
        └─► AUTO 1002000000011  sirene_forte.yaml  (garde : mode test off)
               └─► script.sirene_brutale ──► MQTT zigbee2mqtt/sirene/set (burglar/very_high)
```

### 2.2 Ouvrants d'entrée — deux abstractions de la même réalité physique

Les contacts physiques redondants `contact_entree_porte_1/_2` et `contact_garage_1/_2` alimentent **deux chaînes de templates distinctes** :

- **Chaîne réconciliée** (`12_template_sensors/ouvertures/capteurs_redondants.yaml`) → `binary_sensor.contact_entree_porte`, `binary_sensor.contact_garage`. Logique de réconciliation avec quarantaine/divergence (corroboration des deux sources). **Consommée par le chemin immédiat** (`autres.yaml`).
- **Chaîne permissive** (`12_template_sensors/alarme/ouvrants_entree.yaml`) → `binary_sensor.alarme_ouverture_entree`, `binary_sensor.alarme_ouverture_garage`. Logique « 1 source à on suffit », signal *stateful* explicitement non-preuve d'intrusion, à consommer **sur front montant**. **Consommée par le chemin temporisé** (`delai_entree_start.yaml`).

> **Constat de conception :** le chemin immédiat et le chemin temporisé n'observent **pas le même signal**, alors qu'ils décrivent la **même ouverture physique**. Leurs transitions `→ on` ne sont pas garanties simultanées (réconciliation stricte vs OR permissif). C'est l'une des racines de la course de CRIT-1.

### 2.3 Délai d'entrée

- **Démarrage** — `delai_entree_start.yaml` (`10020000000031`, `single`) : front `off→on` sur `alarme_ouverture_entree`/`alarme_ouverture_garage`, si `armed_away` et `timer.delai_entree` `idle`. Pose `timer.delai_entree` (durée = `input_number.alarme_delai_entree`, 10–120 s, défaut 30) ; bip hors mode test.
- **État dérivé** — `binary_sensor.delai_desarmement_en_cours = is_state('timer.delai_entree','active')` (`12_template_sensors/alarme/delai_desarmement.yaml`). Sert de garde anti-déclenchement aux chemins immédiat et mouvement.
- **Annulation** — `timer_cancel.yaml` (`10020000000033`) : sur `disarmed`, si timer actif → `timer.cancel`.
- **Fin** — `delai_entree_fin.yaml` (`10020000000032`, `single`) : sur `timer.finished`, si `systeme_stable` + `armed_away` + `ouverture_qualifiee_maison == on` → `alarm_trigger` + notif + `sirene_brutale`. En-tête du fichier : **dette §9 assumée** (court-circuit du pipeline canonique).

### 2.4 Intrusion — chemins immédiat / confirmé / mouvement

| Chemin | Automation | Déclenche `alarm_trigger` si… | Inhibition pendant le délai |
|--------|-----------|-------------------------------|------------------------------|
| Immédiat (ouvertures) | `autres.yaml` `1002000000007` | ouverture surveillée + `armed_away` + `delai_desarmement_en_cours == off` | via le garde `delai_desarmement_en_cours` |
| Confirmé (fin de délai) | `delai_entree_fin.yaml` `10020000000032` | `timer.finished` + `systeme_stable` + `armed_away` + `ouverture_qualifiee_maison == on` | — (s'exécute à l'expiration) |
| Mouvement | `mouvement.yaml` `1002000000009` | mouvement zone + `armed_away` + **NOT** `timer.delai_entree active` + robot off | via condition `NOT timer active` |

`ouverture_qualifiee_maison` (`12_template_sensors/ouvertures/ouverture_qualifiee_maison.yaml`) = `contact_entree_fenetre`, `contact_chambre_arnaud`, `contact_chambre_matthieu` (immédiats) **OU** `fenetre_sejour_ouverte_avec_delai`, `fenetre_chambre_parents_ouverte_avec_delai` (confirmés). **Ni porte d'entrée, ni garage.** Sémantique documentée : « autorise une suspension M5 » (aération), **pas** une preuve d'intrusion.

### 2.5 Déclenchement sirène

- Chemin canonique : `state → triggered` → `sirene_forte.yaml` (`1002000000011`, garde mode test off) → `script.sirene_brutale` → MQTT `zigbee2mqtt/sirene/set` (mode `burglar`, `very_high`, durée = `number.sirene_max_duration`).
- `script.sirene_brutale` (`10_scripts/alarme/sirene/brutale.yaml`) : terminal, non conditionnel, idempotent (publication MQTT unique).
- `autres.yaml` et `mouvement.yaml` n'appellent **pas** la sirène directement : ils passent par `alarm_trigger` → `triggered` → `sirene_forte`. **Seul** `delai_entree_fin.yaml` appelle `sirene_brutale` en direct **en plus** de `alarm_trigger` → d'où la double invocation (MIN-5).

---

## 3. Producteurs / Consommateurs / Dépendances

### 3.1 Producteurs (signaux & états)

| Entité produite | Producteur | Sémantique |
|-----------------|-----------|------------|
| `binary_sensor.contact_entree_porte` / `contact_garage` | `capteurs_redondants.yaml` | ouverture réconciliée (quarantaine/divergence) |
| `binary_sensor.alarme_ouverture_entree` / `alarme_ouverture_garage` | `ouvrants_entree.yaml` | signal permissif dédié au délai (non-preuve) |
| `timer.delai_entree` | `delai_entree_start` (start) / `timer_cancel` (cancel) / fin native | fenêtre temporelle d'entrée |
| `binary_sensor.delai_desarmement_en_cours` | `delai_desarmement.yaml` | projection « délai actif » |
| `binary_sensor.ouverture_qualifiee_maison` | `ouverture_qualifiee_maison.yaml` | **sémantique aération/M5** (réutilisée comme garde intrusion) |
| `alarm_control_panel.alarme_maison` (état `triggered`) | service `alarm_trigger` (panneau) | état d'alarme déclenchée |

### 3.2 Consommateurs

| Consommateur | Lit | Effet |
|--------------|-----|-------|
| `autres.yaml` | `contact_*` (réconciliés), `delai_desarmement_en_cours`, `armed_away`, mode test | `alarm_trigger` immédiat |
| `delai_entree_start.yaml` | `alarme_ouverture_*`, `armed_away`, `timer idle` | `timer.start`, bip |
| `delai_entree_fin.yaml` | `timer.finished`, `systeme_stable`, `armed_away`, `ouverture_qualifiee_maison` | `alarm_trigger` + sirène directe |
| `mouvement.yaml` | `mouvement_*`, `armed_away`, `timer active`, robot | `alarm_trigger` |
| `timer_cancel.yaml` | `disarmed`, `timer active` | `timer.cancel` |
| `sirene_forte.yaml` | `state triggered`, mode test | `sirene_brutale` |

### 3.3 Dépendances structurelles

- **Couplage par course** entre la chaîne `timer/delai_desarmement_en_cours` et la chaîne immédiate `autres.yaml` (cf. §4.1).
- **Dépendance sémantique croisée** : un capteur d'**aération** (`ouverture_qualifiee_maison`, M5) sert de garde d'**intrusion** (cf. §4.2).
- **Dépendance externe** : domaine **ouvertures** (réconciliation, contacts redondants, capteurs « avec délai » séjour/parents).
- **Dépendance amont** : doctrine helpers stabilisée par **CH-2** (autorité d'écriture, raison décisionnelle observable).
- **Dépendance latérale** : **CH-4** (chaîne sirène / auto-extinction) — point de contact via MIN-5.
- **Contrats concernés** : `50_intrusion_detection`, `51_ouvrants_entree`, `60_delais_et_blocages`, `contrats/ouvertures/{…}` ; alignement attendu après arbitrage.

---

## 4. Analyse précise des constats critiques

### 4.1 ALM-CRIT-1 — Faux positif à l'entrée légitime (course non déterministe)

**Mécanisme.** À l'ouverture de la porte en `armed_away`, le même événement physique (`contact_entree_porte_1/_2 → on`) déclenche **deux chaînes en parallèle** :

1. Chaîne réconciliée → `contact_entree_porte → on` → déclenche `autres.yaml`. Sa **seule** protection contre le déclenchement immédiat est la condition `delai_desarmement_en_cours == off`.
2. Chaîne permissive → `alarme_ouverture_entree → on` → déclenche `delai_entree_start` → `timer.start` → (réévaluation du template) `delai_desarmement_en_cours → on`.

La protection (1) ne devient effective qu'**après** que (2) ait : exécuté `timer.start`, fait passer `timer.delai_entree` à `active`, **et** propagé la réévaluation du template `delai_desarmement_en_cours`. Si `autres.yaml` évalue ses conditions **avant** la fin de cette propagation, le garde est encore `off` → `alarm_trigger` immédiat → `triggered` → `sirene_forte` → sirène. **Déclenchement réel à l'entrée légitime, non déterministe**, dépendant de l'ordonnancement HA et de la latence relative des deux chaînes de templates.

**Aggravation.** Les deux chemins consomment des **abstractions différentes** du même contact (réconciliée vs permissive). Leurs transitions `→ on` ne sont pas garanties simultanées ; la réconciliation (quarantaine/divergence) peut même stabiliser `contact_entree_porte` à un instant distinct de `alarme_ouverture_entree`.

**Écart contractuel.** Le contrat `50` prescrit que `autres.yaml` déclenche « **hors ouvrants d'entrée** ». Or porte et garage **sont** dans ses déclencheurs. Le chemin immédiat ne devrait pas voir les ouvrants d'entrée : ceux-ci sont, par conception, couverts par le délai.

**Effet net.** Perte de confiance : une entrée normale peut déclencher la sirène de façon aléatoire. Sévérité critique (faux positif sur la voie principale).

### 4.2 ALM-CRIT-2 — Faux négatif à l'expiration du délai (garde structurellement aveugle)

**Mécanisme.** Intrusion par la porte/garage en `armed_away` :

1. `delai_entree_start` pose `timer.delai_entree` (délai actif).
2. Pendant le délai : `autres.yaml` est inhibé (`delai_desarmement_en_cours == on`) **et** `mouvement.yaml` est inhibé (`NOT timer active`). La maison est volontairement « silencieuse » le temps du désarmement.
3. Pas de désarmement → le timer va jusqu'à `timer.finished`.
4. `delai_entree_fin` s'exécute, **mais** son garde exige `ouverture_qualifiee_maison == on`. Ce capteur **exclut structurellement porte et garage**. Si la seule ouverture est la voie d'entrée (souvent refermée derrière l'intrus, et de toute façon **absente** du capteur), le garde est `off` → **aucun `alarm_trigger`**.

**Double défaut.**
- **Sémantique** : usage d'un capteur d'aération (M5) comme preuve d'intrusion. Les ouvrants qui **démarrent** le délai sont précisément ceux que le garde **ne voit pas**.
- **Instantanéité** : le garde lit un **état courant** à l'expiration, sans **mémoire** de l'ouverture survenue pendant la fenêtre. Même une ouverture qualifiée refermée avant l'échéance serait manquée.

**Couverture résiduelle.** Seul `mouvement.yaml`, **après** expiration du délai (timer non actif), peut encore déclencher. Un intrus restant hors champ des détecteurs, ou la moindre lacune de couverture mouvement, laisse l'intrusion par la voie principale **non sanctionnée**.

**Observation décisive pour les options.** `timer_cancel` annule le timer au désarmement. Donc **atteindre `timer.finished` encode déjà** : « un ouvrant d'entrée a démarré le délai en `armed_away` **et** aucun désarmement n'a eu lieu ». Le garde `ouverture_qualifiee_maison` n'apporte aucune information utile et en retranche une (il **bloque** la sanction légitime).

---

## 5. Corollaire — ALM-MIN-5 (double sirène en fin de délai)

`delai_entree_fin` appelle `alarm_trigger` (→ `triggered` → `sirene_forte` → `sirene_brutale`) **et** `sirene_brutale` en direct : double invocation. Effet pratique négligeable (`mode: single`, MQTT idempotent), mais c'est l'expression de la **dette §9** : le chemin de fin de délai court-circuite le pipeline canonique. Toute refonte de la confirmation d'intrusion doit converger vers **un chemin sonore unique** (`triggered → sirene_forte`).

---

## 6. Invariants de sécurité à préserver

- **I-1** : une entrée légitime ne doit **jamais** déclencher immédiatement ; le délai doit « gagner la course » de façon **déterministe**.
- **I-2** : une intrusion par la voie principale doit être **sanctionnée à l'expiration** du délai (élimination du faux négatif).
- **I-3** : bifurcation **mode test** préservée sur tous les chemins (aucun effet réel en test).
- **I-4** : sémantique **front montant** (un état restauré `on` au reboot ≠ nouvelle ouverture) ; garde `systeme_stable` post-reboot conservé.
- **I-5** : réconciliation/quarantaine des contacts redondants **non régressée**.
- **I-6** : couverture **mouvement** au moins équivalente (pas de fenêtre aveugle nouvelle).
- **I-7** : doctrine **écrivain unique** (CH-2) respectée si un état « intrusion confirmée » est introduit.
- **I-8** : `mode: single`/idempotence de la sirène ; pas de double émission.

---

## 7. Options architecturales

### 7.A — Traiter CRIT-1 (faux positif immédiat)

- **A1 — Sortir les ouvrants d'entrée du chemin immédiat.** Retirer `contact_entree_porte`/`contact_garage` des déclencheurs de `autres.yaml` ; les ouvrants d'entrée ne sont plus traités que par le délai. *Aligne le contrat 50 (« hors ouvrants d'entrée »), supprime la course à la racine.* Contre : repose entièrement sur la justesse du chemin temporisé → **doit être couplé au traitement de CRIT-2**.
- **A2 — Durcir le garde anti-course (timing).** Conserver les ouvrants d'entrée dans `autres.yaml` mais rendre le garde déterministe (ex. `for:` de stabilisation, ou garde sur un état posé atomiquement avec l'ouverture). Contre : solution **temporelle fragile**, lutte contre l'asynchronisme HA, maintient l'écart au contrat 50. Déconseillé comme socle.
- **A3 — Unifier la source observée.** Faire consommer aux deux chemins le **même** signal d'ouverture d'entrée (supprime la divergence réconciliée/permissive). Réduit une cause de course mais ne suffit pas seul.

> **Orientation préférentielle 7.A :** **A1** (éventuellement complété de A3 pour la cohérence des sources), couplé à 7.B.

### 7.B — Traiter CRIT-2 (faux négatif à l'expiration)

- **B1 — Garde dédié « intrusion d'entrée », incluant porte/garage + mémoire.** Remplacer `ouverture_qualifiee_maison` par un état dédié qui (a) **inclut** les ouvrants d'entrée et (b) **mémorise** qu'une ouverture d'entrée a eu lieu **pendant** la fenêtre de délai (verrou posé au démarrage, consommé/réinitialisé à l'expiration ou au désarmement). *Sémantiquement correct, observable.* Contre : introduit un mécanisme de mémoire (helper dédié) à concevoir.
- **B2 — Faire confiance au cycle de vie du timer (supprimer le garde d'ouverture).** Puisque le délai ne démarre que sur ouverture d'entrée en `armed_away` et que `timer_cancel` l'annule au désarmement, **`timer.finished` prouve déjà l'intrusion**. Conserver les gardes `systeme_stable` + `armed_away`, retirer `ouverture_qualifiee_maison`. *Le plus simple, sémantiquement le plus juste (un intrus qui referme la porte sans désarmer reste un intrus).* Contre : à valider sur les bords (restore/reboot couvert par `systeme_stable` ; s'assurer qu'aucun autre chemin ne pose le timer).
- **B3 — Matérialiser « intrusion confirmée » comme état contractuel (cible §9).** État persisté, **écrivain unique**, alimenté par les détections (immédiate non-entrée + expiration de délai) ; panneau et sirène déclenchés **depuis cet état** via le pipeline canonique. *Résout aussi MIN-5, aligne la doctrine Arsenal.* Contre : surface la plus large.

> **Orientation préférentielle 7.B :** **B2** si l'audit des bords du timer le confirme (le plus sobre et le plus correct) ; **B1** si l'on veut un état d'intrusion explicitement observable ; **B3** comme **cible** à moyen terme (absorbe MIN-5 et la dette §9).

### 7.C — Convergence sirène (MIN-5)

- **C1 — Chemin sonore unique** : retirer l'appel direct `sirene_brutale` de `delai_entree_fin` et ne conserver que `alarm_trigger → triggered → sirene_forte`. *Cohérent avec B3 (déclenchement depuis l'état).* C'est le geste minimal résorbant la double invocation.

### 7.D — Combinaison cible recommandée (synthèse, non tranchée)

1. **A1** (+ A3) : les ouvrants d'entrée quittent le chemin immédiat → la course CRIT-1 disparaît.
2. **B2** ou **B1** : la fin de délai sanctionne réellement l'intrusion d'entrée → CRIT-2 résorbé.
3. **C1** (idéalement via **B3**) : chemin sonore unique → MIN-5 résorbé, dette §9 soldée.
4. Alignement des contrats `50`/`51`/`60` sur la frontière retenue.

---

## 8. Questions ouvertes / à confirmer en runtime

- **Q1 (CRIT-1)** : mesurer la latence relative réelle des deux chaînes (réconciliée vs permissive) et la fréquence effective du faux positif (le rapport classe l'effet « à confirmer en runtime »).
- **Q2 (B2)** : recenser **tous** les chemins qui peuvent poser/laisser `timer.delai_entree` actif ; confirmer qu'aucun ne produit un `timer.finished` non intrusif hors fenêtre `systeme_stable`.
- **Q3 (B1)** : définir la portée du verrou mémoire (porte + garage ; faut-il y adjoindre d'autres ouvrants « avec délai » ?) et sa règle de réinitialisation.
- **Q4 (frontière)** : statuer sur le sort des ouvertures « avec délai » séjour/parents — restent-elles dans la confirmation d'intrusion, et par quel chemin ?
- **Q5 (sémantique)** : `ouverture_qualifiee_maison` est consommé par M5 (aération) ; vérifier qu'aucun autre consommateur d'intrusion n'en dépend avant de le dissocier.

---

## 9. Dépendances inter-chantiers

- **Amont** : **CH-2** (soldé) — doctrine d'écriture stabilisée ; prérequis si B3 introduit un état « intrusion confirmée » à écrivain unique.
- **Latéral** : **CH-4** (sirène / auto-extinction) — converge avec C1/MIN-5.
- **Externe** : domaine **ouvertures** — toute redéfinition de garde touche la réconciliation et les capteurs « avec délai ».
- **Aval documentaire** : **CH-5** — alignement des contrats `50`/`51`/`60` une fois la frontière arbitrée.

---

*Dossier de conception CH-1 Alarme. Établi en lecture du dépôt (`origin/main` = `99cbc0b`). Analyse et options uniquement — aucun patch, aucun YAML, aucune correction. Arbitrages laissés ouverts.*
