# Cadrage architectural — Dette de modélisation de la présence

> **NAVIGATION — NON NORMATIF, NON DÉCISIONNEL.** Constat transverse consigné. N'amende aucun contrat, ne modifie aucun YAML, ne décide rien.
> Registre transverse : [`registre_anomalies_transverses.md`](registre_anomalies_transverses.md) · Index audits : [`../../index.md`](../../index.md)
> Hubs concernés : [`navigation/domaines/presence.md`](../../../navigation/domaines/presence.md) · [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)
> Documents de famille faisant foi : [`contrats/presence.md`](../../../contrats/presence.md) · [`architecture/presence/presence.md`](../../../architecture/presence/presence.md)

---

> **Statut** : Cadrage — *non normatif*, *non décisionnel*
> **Classement (2026-06-17)** : **dossier d'arbitrage dormant** — *ce n'est pas un chantier à planifier*. La dette est structurellement réelle (cf. §4–§7) mais **non ordonnançable en l'état** : aucune des 6 questions du §9 n'est ouverte pour décision, et l'incident révélateur (clim) est élucidé et mitigé par ailleurs (signal `presence_confort_thermique_stabilisee`, confiné COOL/DRY). **Réveil sur déclencheur** : un incident reproductible sur un consommateur de présence **brute** (chauffage / HEAT / éclairage / vacances), ou l'ouverture explicite d'une question d'arbitrage. Suivi d'état : [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (« À arbitrer / dormants »).
> **Nature** : Document de problématisation. Il ne corrige rien, ne modifie aucun YAML, n'amende aucun contrat métier.
> **Objet** : Poser proprement une dette de modélisation révélée par un incident climatisation, en distinguant les notions, en classant les risques, et en ouvrant des pistes — sans en choisir aucune.
> **Périmètre** : Domaine Présence (sécurité, confort, preuves, haute précision GPS, zones). Le domaine Climatisation n'apparaît qu'à titre de **cas révélateur**.

---

## 0. Ce que ce document n'est pas

- Il ne propose **aucun patch** ni aucune modification runtime.
- Il ne modifie **aucun contrat** (`presence.md`, `zones.md`, `mobile.high_accuracy.contextuel.md`, `bouclage.md`…).
- Il ne hiérarchise **pas définitivement** les pistes : il les expose comme options à arbitrer.
- Il ne fixe **aucun planning** ni aucune décision technique immédiate.
- Il ne ré-ouvre **pas** l'incident clim : celui-ci est considéré comme élucidé (cf. §2) et n'est plus le sujet.

---

## 1. Résumé exécutif

Un arrêt transitoire de la climatisation (décision `cool → off → cool` en ~7 s) a été tracé jusqu'à une chute de la présence confort canonique (`binary_sensor.presence_famille_unifiee`), elle-même conforme à sa définition (`delay_off: 30s`), elle-même causée par une perte de présence **brute** d'environ 34 s lors d'un retour domicile.

L'enquête a successivement écarté la couche clim, puis la couche décisionnelle, puis le capteur unifié, pour aboutir à un constat plus profond : **la présence n'est pas modélisée avec une séparation stable entre, d'une part, des *preuves de présence* neutres (GPS, Wi-Fi, zones) et, d'autre part, des *vérités de présence* propres à chaque domaine (sécurité vs confort).**

Les symptômes périphériques (gating de la haute précision GPS sur l'état d'alarme, divergences de nommage des zones) sont des **amplificateurs** ou des **manifestations** de cette racine, non la racine elle-même.

**Verdict de cadrage** : dette de modélisation, surfaçant comme **conséquence émergente** d'un assemblage *localement cohérent* mais *globalement sous-séparé*. Aucune décision corrective n'est prise ici.

---

## 2. Cas révélateur : l'incident climatisation (condensé)

> Rattachement : ce cadrage est issu d'une enquête partie du domaine [Climatisation](../../../navigation/domaines/climatisation.md). La clim est le **témoin**, pas le sujet. Référence dynamique antérieure côté clim : [`investigation_historique_clim_30j.md`](../../01_rapports/climatisation/investigation_historique_clim_30j.md) (où l'hypothèse « présence = cause » avait été *infirmée* sur 30 j ; le présent cadrage en précise le mécanisme exact via les seuils).

Chaîne causale établie, du métier vers la cause (sens de lecture : effet ← cause) :

```
clim arrêtée
  ← sensor.clim_target_mode = off
      ← input_boolean.besoin_clim_cool_admissible = off  (extinction besoin, porte 1)
          ← binary_sensor.besoin_clim_cool = off
              ← bascule du seuil appliqué (sensor.seuil_allumage/extinction_clim_applique)
                  ← binary_sensor.presence_famille_unifiee = off   ◄── PIVOT
                      ← brut false ≥ 30 s (delay_off honoré)
                          ← perte de présence BRUTE ~34 s pendant un retour domicile
```

Faits saillants :

- Le `delay_off: 30s` du capteur unifié **a fonctionné** : il a confirmé une absence longue, il ne l'a pas fabriquée. La fenêtre publiée de ~7 s est la queue d'un épisode brut de ~34 s.
- La décision clim est **saine** : elle a suivi fidèlement la présence confort. Le problème n'est ni dans la clim, ni dans le capteur unifié.
- Le pivot est `presence_famille_unifiee`. **Tout le cadrage porte sur ce qui se trouve en amont de ce pivot.**

> L'incident clim n'est donc qu'un **témoin**. N'importe quel domaine consommant la présence confort (chauffage, éclairage de confort) est exposé à la même classe de perturbation.

---

## 3. Le problème de fond

L'architecture Présence mélange deux responsabilités qui devraient être étagées :

1. **Acquérir et qualifier des preuves de présence** (où sont les personnes, selon GPS / Wi-Fi / zones / signaux contextuels) — responsabilité *neutre*, partageable.
2. **Décider d'une vérité de présence par domaine** (le foyer est-il « présent » au sens *alarme* ? au sens *confort* ?) — responsabilité *métier*, propre à chaque domaine, avec des exigences **opposées** de réactivité et de tolérance.

Dans l'état actuel :

- Il n'existe **pas de couche explicite « preuves neutres »**. Chaque vérité de domaine ré-agrège directement des sources brutes, à sa manière.
- La **vérité confort** (`presence_famille_unifiee`) consomme directement la **vérité sécurité** (`presence_famille_securite`) via un `OR`. La canonique d'un domaine devient un *intrant* d'un autre domaine.
- En conséquence, les caractéristiques de réglage propres à l'alarme (nervosité, rayon serré, absence de temporisation — toutes *appropriées* côté sûreté) **fuient** vers le confort, où elles sont *inappropriées*.

Ce n'est pas une erreur ponctuelle : c'est une **absence de frontière** entre la couche preuve et la couche vérité.

---

## 4. Taxonomie clarifiée

Cette section **distingue** les notions. Elle décrit l'état observé (factuel) et l'intention contractuelle, sans rien réformer.

### 4.1 Preuves neutres de présence (couche évidence — *implicite aujourd'hui*)

Signaux bruts, sans sémantique métier propre :

- Trackers `device_tracker.*` derrière `person.valentin` / `person.constance` (qualité variable : fix GPS vs repli réseau/cellulaire).
- Distance géométrique au domicile (`distance(tracker, zone.maison_securite)`).
- Appartenance aux zones (`zone.home`, `zone.maison_securite`, `zone.approche_securite`).
- Présence Wi-Fi par BSSID (`binary_sensor.presence_wifi_maison`).
- Présences contextuelles explicites (`binary_sensor.presence_enfants`, `input_boolean.presence_visiteur`).

**Constat** : ces preuves n'ont **pas d'entité de couche dédiée**. Elles sont consommées directement par les vérités de domaine, sans normalisation intermédiaire. Leur **diversité de mode de panne** n'est pas exploitée : GPS et distance dérivent de la *même* position rapportée ; seul le Wi-Fi diffère réellement, mais il ne couvre que la proximité immédiate.

### 4.2 Présence sécurité (vérité du domaine alarme)

- Entité canonique : `binary_sensor.presence_famille_securite`.
- Intention contractuelle ([`architecture/presence/presence.md`](../../../architecture/presence/presence.md)) : conservatrice, **stricte**, **réservée à la sûreté**, *interdite pour tout calcul de confort thermique*.
- Réglage cohérent avec l'alarme : rayon serré (`input_number.zone_securite_radius`, plage 20–150 m), **aucune temporisation propre** *(au niveau du signal brut ; voir note d'état post-correctif ci-dessous)*, doit chuter dès la sortie réelle.
- Comportement *attendu et normal* : lors d'un retour, une séquence `ON → OFF → ON` (entrée pour désarmer, ressortie pour stationner, ré-entrée) est **nominale** côté alarme — le domaine alarme l'absorbe sans se réarmer.

> **Note d'état (post-correctif alarme, 2026-06-20).** Le signal brut `binary_sensor.presence_famille_securite` **reste sans temporisation propre**. En revanche, le **chemin de désarmement de l'alarme** ne le consomme plus directement : il lit désormais une **projection confirmée dédiée** `binary_sensor.presence_famille_securite_confirmee_alarme` (`delay_on 15 s`), introduite pour absorber des blips de présence brute à proximité du domicile que l'alarme **n'absorbait pas** nativement (à proximité, sous bruit GPS/BSSID, contrairement à ce que laisse entendre la description ci-dessus). L'**armement** est désormais fondé sur la projection confirmée d'absence `binary_sensor.presence_famille_securite_absence_confirmee_alarme` (`delay_on 5 min`, atomique) ; l'ancien `binary_sensor.presence_famille_securite_absent_depuis_5_min` a été supprimé (phase 2, v16.3.1). Cette mitigation est **locale au domaine alarme** — **précédent partiel de la piste P-F (§8)** — et **ne résout pas** la dette structurelle (R1–R8) ni l'arbitrage ex-C4 / §9 q5 côté confort/clim. Réf. contrat : `../../../contrats/alarme/30_decision_centrale.md`.

### 4.3 Présence confort (vérité du domaine thermique)

- Entité canonique : `binary_sensor.presence_famille_unifiee`.
- Intention contractuelle : **permissive**, **stable**, anti-fluctuation, destinée au chauffage / clim / éclairage de confort ; *interdite pour l'armement de l'alarme*.
- Réglage : `delay_on: 3s`, `delay_off: 30s` — **seul point de temporisation** de toute la chaîne présence.
- **Composition réelle** : `presence_famille OR presence_famille_securite`. La vérité confort **importe la vérité sécurité**. C'est le couplage central de ce cadrage.

### 4.4 Stratégies de haute précision GPS (infrastructure transverse)

- Activation (`high_accuracy_on.yaml`) : à l'entrée dans `zone.approche_securite` (400 m), via *trigger de zone* (robuste au nommage), **sous condition `alarm_control_panel.alarme_maison == 'armed_away'`**.
- Borne : `timer.high_accuracy_securite` (8 min).
- **Constat de modélisation** : un besoin de *qualité de preuve* transverse (densifier le GPS à l'approche, utile à *toute* présence) est **asservi à l'état de l'alarme**. Lors d'un retour où l'alarme n'est pas `armed_away`, la densification ne s'active pas → preuve GPS grossière à l'approche. Référence : [`contrats/mobile.high_accuracy.contextuel.md`](../../../contrats/mobile.high_accuracy.contextuel.md).

### 4.5 Divergences de nommage zones / contrats / runtime

Trois conventions coexistent pour les mêmes zones, **aucune** ne correspondant au nom réel rapporté par `person.*` :

| Source | Chaîne utilisée | Nom réel de zone (`17_zones/`) | Correspond ? |
|---|---|---|---|
| `presence_famille` | `Maison – Sécurité`, `Approche – Sécurité` | `Maison securite`, `Approche securite` | ❌ |
| `presence_famille_securite` | `Zone maison` | `Maison securite` | ❌ |
| `approche.yaml` | `Zone approche securite` | `Approche securite` | ❌ |
| Contrat [`presence.md`](../../../contrats/presence.md) (normatif) | `Maison – Sécurité` | `Maison securite` | ❌ |

Effet : toutes les projections `person.*`-par-zone sont **mortes**, sauf `home`. Les vérités de présence se replient donc sur les sources les plus bruitées (distance GPS, Wi-Fi), exactement celles qui défaillent ensemble en régime basse précision. [`zones.md`](../../../contrats/zones.md) §3.3 qualifie d'avance une telle divergence d'« **incohérence structurelle à arbitrer** ».

---

## 5. Cartographie des couplages actuels (factuelle)

```
            [ device_tracker / person.* ]      [ Wi-Fi BSSID ]   [ enfants / visiteur ]
                       │  │                            │                 │
        distance ──────┘  └──── zones (home/maison/approche)             │
                       │            │ (projections mortes sauf 'home')   │
                       ▼            ▼                  ▼                  ▼
        ┌──────────────────────────┐      ┌────────────────────────────────────────┐
        │ presence_famille (confort)│     │ presence_famille_securite (SÉCURITÉ)     │
        │  ≈ person ∈ home(≈824m)   │     │  ≈ dist<rayon serré OR Wi-Fi OR enfants  │
        └─────────────┬─────────────┘     └───────────────┬──────────────────────────┘
                      │            OR  ◄──────────────────┘  ◄── COUPLAGE INTER-DOMAINE
                      ▼
        ┌─────────────────────────────────────────┐        ┌───────────────────────────┐
        │ presence_famille_unifiee (CONFORT)       │        │  Domaine ALARME           │
        │  delay_on 3s / delay_off 30s             │        │  (consomme sécurité)      │
        └─────────────┬────────────────────────────┘        └───────────────────────────┘
                      ▼
        Chauffage · Climatisation · Éclairage de confort · (historiquement ECS, cf. §6)
```

Points de lecture :

- **C1** — La canonique confort `OR`-e la canonique sécurité. La vérité d'un domaine alimente la vérité d'un autre (tension avec la séparation déclarée).
- **C2** — Les deux bras du `OR` partagent la **même racine** (position rapportée par rapport au domicile). La redondance du `OR` est *apparente* : elle ne diversifie pas les modes de panne.
- **C3** — La haute précision (qualité de preuve) est branchée sur l'**alarme**, pas sur un signal d'approche neutre.
- **C4** — La couche « preuves neutres » est absente : chaque vérité ré-agrège les sources directement.

> Note d'honnêteté logique : le `OR` étant additif, une transition **sécurité seule** `ON→OFF→ON` (si `presence_famille` reste `ON`) **n'impacte pas** le confort. L'impact n'apparaît que lorsque les deux bras tombent — ce qui, du fait de C2, est précisément le mode de panne courant. Le défaut n'est donc pas « la sécurité tire le confort vers le bas », mais « le confort n'a aucune source dont la panne soit indépendante de la géométrie GPS ».

---

## 6. Indice que la dette est déjà rencontrée (sans avoir été nommée)

Le contrat [`bouclage.md`](../../../contrats/bouclage.md) documente le **cas miroir** côté ECS : la présence confort unifiée y a été jugée *trop lâche* (« inclut la projection Approche – Sécurité, inadaptée à la qualification d'un usage ECS »), et a été **délibérément remplacée** par `presence_famille_securite OR presence_visiteur`, retirant `presence_famille_unifiee` de la composition `bouclage_autorise`.

Lecture de cadrage : différents domaines **piochent ad hoc** dans différentes projections de présence selon leurs besoins ponctuels (l'ECS se rabat sur la *sécurité* faute de mieux ; la clim souffre d'être couplée à la *sécurité*). C'est le symptôme classique d'une **couche de preuve manquante** : en son absence, chaque domaine bricole sa source. La dette n'est pas hypothétique ; elle a déjà produit des contournements locaux.

---

## 7. Registre des risques (classés, sans décision)

Échelle de gravité indicative : 🟥 élevé · 🟧 moyen · 🟨 faible. Statut : *avéré* (observé), *actif* (présent et exploitable), *latent* (présent, non encore déclenché).

| ID | Risque | Nature | Domaines exposés | Gravité | Statut |
|----|--------|--------|------------------|---------|--------|
| R1 | La canonique confort consomme la canonique sécurité (`OR`) | Couplage inter-domaine contraire à la séparation déclarée | Chauffage, Clim, Éclairage confort | 🟥 | avéré |
| R2 | Les deux sources confort partagent la racine GPS (pas d'indépendance de panne) | Redondance illusoire | Confort thermique | 🟥 | avéré |
| R3 | Divergence triple de nommage zones/contrats/runtime → projections `person.*` mortes | Incohérence structurelle | Présence (toutes vérités) | 🟧 | actif |
| R4 | Haute précision GPS gatée sur `armed_away` | Besoin transverse asservi à un domaine | Présence à l'approche (retour non armé) | 🟧 | actif |
| R5 | Absence de couche « preuves neutres » → choix de projection ad hoc par domaine | Dette de structure | Tous consommateurs de présence | 🟥 | avéré (cf. §6) |
| R6 | Tolérance au bruit portée par un unique `delay_off 30s`, sans debounce par source | Point de filtrage unique | Confort thermique | 🟧 | actif |
| R7 | `person.*` dépend de la qualité du tracker (repli réseau possible) | Racine de panne commune | Présence (toutes vérités) | 🟧 | latent |
| R8 | `presence_famille_securite` joue deux rôles (vérité alarme + preuve confort) | Ambiguïté d'identité d'entité | Sécurité + Confort | 🟥 | avéré |

Observations transverses :

- **R1 + R8** forment le cœur conceptuel (identité et couplage de `presence_famille_securite`).
- **R2 + R7** forment le cœur *physique* (toutes les preuves remontent à une position GPS unique).
- **R3 + R4** sont les amplificateurs : ils ne créent pas la dette, ils en augmentent la fréquence d'expression.
- **R5** est le risque englobant : il *explique* l'existence des autres.

---

## 8. Pistes possibles (ouvertes — aucune n'est retenue)

Chaque piste est exposée avec ce qu'elle adresserait et ses contreparties. **Aucune n'est recommandée ni priorisée ici.** Elles ne sont pas exclusives entre elles ; certaines sont incompatibles. Le but est de baliser l'espace de décision futur.

### P-A — Introduire une couche explicite de preuves neutres
- *Adresse* : R5, R8 (sépare preuve et vérité).
- *Contrepartie* : entité(s) intermédiaire(s) supplémentaire(s) ; révision de la gouvernance contractuelle ; effort de migration des consommateurs.
- *Prérequis* : définir le contrat de la couche preuve avant tout code.

### P-B — Découpler la vérité confort de la vérité sécurité
- *Adresse* : R1, R8 (cesser que le confort consomme la sécurité).
- *Contrepartie* : le confort perdrait son « filet » Wi-Fi/sécurité s'il n'est pas recomposé sur des preuves neutres → dépend de P-A ou d'une source de remplacement.
- *Risque induit* : si mal fait, réduit la couverture confort.

### P-C — Diversifier les modes de panne du confort
- *Adresse* : R2, R7 (ajouter une preuve non strictement GPS : activité domestique, occupation, Wi-Fi élargi…).
- *Contrepartie* : nouvelles sources = nouvelle complexité ; risque de faux positifs de présence.

### P-D — Rebrancher la haute précision sur un signal d'approche neutre
- *Adresse* : R4 (densifier le GPS au retour, indépendamment de l'alarme).
- *Contrepartie* : impact batterie à évaluer ; interactions avec le contrat `mobile.high_accuracy.contextuel`.

### P-E — Réconcilier le référentiel de nommage des zones
- *Adresse* : R3 (un nom de zone fait foi, propagé aux contrats et aux templates).
- *Contrepartie* : décider *quel* nom fait référence (runtime vs contrat) ; revue de tous les consommateurs `person.*`.
- *Sensibilité* : touche à `presence.md` et `zones.md` → relève d'une évolution contractuelle, non d'un patch.

### P-F — Stabilisation par domaine plutôt qu'au point unifié
- *Adresse* : R6 (debounce propre au confort, dimensionné pour le thermique).
- *Contrepartie* : duplication de logique de temporisation ; risque d'oscillations si mal coordonné avec `delay_off`.

### P-G — Statu quo assumé et documenté
- *Adresse* : aucune correction ; on **reconnaît** le comportement comme dette acceptée et on le documente comme attendu.
- *Contrepartie* : l'incident reste reproductible ; tout domaine confort reste exposé.
- *Intérêt* : option de référence pour mesurer le coût/bénéfice des autres pistes.

---

## 9. Questions ouvertes à arbitrer (avant toute décision technique)

1. **Identité de `presence_famille_securite`** : est-ce une *vérité d'alarme* (donc interdite au confort, par contrat) ou un *agrégat de preuves* réutilisable ? Le système la traite aujourd'hui comme les deux. Trancher cette identité conditionne P-A/P-B.
2. **Légitimité du `OR` confort ⊃ sécurité** : la composition actuelle est-elle une violation de la séparation `presence.md`, ou une exception assumée ? Le contrat dit « interdite pour tout calcul de confort thermique ».
3. **Référentiel de nommage faisant foi** : le runtime (`Maison securite`) ou les contrats (`Maison – Sécurité`) ? L'un des deux doit céder.
4. **Nature de la haute précision** : infrastructure neutre (déclenchée par l'approche) ou service de sûreté (déclenchée par l'alarme) ? La réponse re-catégorise R4.
5. **Niveau de stabilisation** : la tolérance au bruit doit-elle rester unique (au pivot confort) ou être distribuée par domaine ?
6. **Objectif métier « quelqu'un rentre »** : doit-il être un *état de présence* à part entière (anticipation), ou rester une émergence des zones ? Aujourd'hui il n'est porté explicitement par aucune vérité.

---

## 10. Synthèse de cadrage

- **Sujet principal** : séparation entre *preuves de présence neutres* et *vérités de présence par domaine* (R5, englobant).
- **Cœur conceptuel** : `presence_famille_securite` à double rôle, et son import par la canonique confort (R1, R8).
- **Cœur physique** : toutes les preuves remontent à une position GPS unique (R2, R7).
- **Amplificateurs** : gating haute précision sur l'alarme (R4), divergences de nommage (R3).
- **Cas révélateur** : incident clim — témoin, non cause.
- **Décision** : aucune, par construction. Ce document **pose** le problème ; il ne le résout pas.

---

## 11. Références (état du dépôt au moment du cadrage)

**Implémentation**
- `12_template_sensors/presence/global.yaml` — `presence_famille_unifiee` (OR ; delay_on 3s / delay_off 30s)
- `12_template_sensors/presence/famille.yaml` — `presence_famille`
- `12_template_sensors/presence/securite/presence.yaml` — `presence_famille_securite`
- `12_template_sensors/presence/securite/approche.yaml` — `approche_securite_*` (chaîne morte)
- `12_template_sensors/presence/securite/wifi.yaml` — `presence_wifi_maison`
- `12_template_sensors/climatisation/seuils_on_off/cool/on.yaml`, `off.yaml` — seuils appliqués (présence/absence)
- `11_automations/presence/high_accuracy_on.yaml`, `high_accuracy_off.yaml` — gating `armed_away`
- `08_timers/presence/high_accuracy_securite.yaml` — borne 8 min
- `17_zones/maison_securite.yaml` (40 m), `17_zones/approche_securite.yaml` (400 m)
- `03_input_numbers/presence/radius_zone_securite.yaml` — `zone_securite_radius` (20–150 m)

**Contrats / architecture (cités, non modifiés)**
- [`architecture/presence/presence.md`](../../../architecture/presence/presence.md) — typologie sécurité/confort, non-interchangeabilité
- [`contrats/presence.md`](../../../contrats/presence.md) — projections valides (normatif)
- [`contrats/zones.md`](../../../contrats/zones.md) — référentiel zones ; clause d'incohérence structurelle
- [`contrats/bouclage.md`](../../../contrats/bouclage.md) — cas miroir ECS (preuve de la dette)
- [`contrats/mobile.high_accuracy.contextuel.md`](../../../contrats/mobile.high_accuracy.contextuel.md) — référence haute précision

**Cas révélateur (côté climatisation)**
- Hub : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)
- Investigation dynamique antérieure : [`investigation_historique_clim_30j.md`](../../01_rapports/climatisation/investigation_historique_clim_30j.md)

---

*Fin du cadrage. Aucune action technique n'est engagée par ce document.*
