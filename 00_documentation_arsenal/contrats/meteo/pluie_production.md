# pluie_production.md
<!-- Arsenal — Domaine : Météo / Production des signaux de précipitation -->
<!-- Version : 1.0 -->
<!-- Statut : Normatif — à respecter avant toute modification YAML -->

> Ce contrat **est** le « contrat météo distinct » auquel
> [`volets_pluie.md`](../volets_pluie.md) §5.2 délègue la **production** de ses
> signaux de frontière (`pluie_en_cours`, `intention_pluie_forte`). Il gouverne la
> **production / qualification** des signaux de précipitation ; il **ne gouverne
> pas** la réaction des ouvrants, qui reste régie par `volets_pluie.md`.

---

## 1. Objet

Définir le comportement normé de la **couche de production des signaux de
précipitation** d'Arsenal : l'**acquisition** des sources, leur **sécurisation**,
et les **qualifications métier** qui en dérivent. Ce contrat formalise l'existant
(dont l'évidence consolidée livrée par C16) et fixe la cible (sécurisation locale,
lot 2 du chantier C17).

## 2. Périmètre

| Inclus | Exclu |
|---|---|
| Acquisition des sources pluie (Netatmo, SNZB-05, prévision) | Réaction des ouvrants (→ `volets_pluie.md`) |
| Qualifications : détectée / en cours / forte / récente / prévue / cumuls | Décision d'équipement (toujours externe) |
| Sécurisation locale des sources de décision (cible) | Palmarès pluie (→ `pluie_palmares.md`) |
| Régimes dégradés (source absente / incohérente) | Vent, température, autres axes météo |

## 3. Positionnement dans le référentiel météo

La **précipitation constitue un axe météo distinct**, à part entière, mais **hors
du modèle de** [`capteurs_meteo.md`](../../architecture/capteurs_meteo.md) : celui-ci
régit les **grandeurs continues** (température, humidité relative, humidité absolue,
humidex) via le pipeline *mesure → filtrage → agrégation → seuils → décision
externe*. La précipitation est **épisodique et cumulative** (détection d'occurrence,
intensité, cumuls glissants) et suit son **propre pipeline** : *acquisition →
sécurisation → qualification → décision externe*. Le présent contrat en fait foi ;
`capteurs_meteo.md` reste inchangé et **n'a pas autorité** sur la précipitation.

## 4. Couches

| Couche | Rôle | Autorité |
|---|---|---|
| **Acquisition** | Sources physiques brutes (Netatmo cloud, SNZB Zigbee, prévision Met.no) | intégrations HA |
| **Sécurisation** | Façade locale robuste des sources de décision (cible — lot 2) | ce contrat |
| **Qualification** | Signaux métier dérivés (§5) | ce contrat |
| **Décision** | Réaction, orchestration | **externe** (`volets_pluie.md`, aération, arrosage…) |

## 5. Qualifications canoniques

Chaque qualification est un **concept métier distinct**. Elles sont **plurielles par
design** (INV-PROD-2) : aucune n'est réductible à une autre.

| Entité | Concept | Objectif métier | Source(s) | Seuil | Consommateurs |
|---|---|---|---|---|---|
| `binary_sensor.pluie_evidence_active` | **Évidence any-rain** | socle d'acquisition consolidé, honnête sur la disponibilité | Netatmo ∪ SNZB borné ∪ injection | intensité `> 0` | écrivains de `pluie_en_cours` |
| `input_boolean.pluie_en_cours` | **Épisode en cours** | protéger une **fenêtre ouverte** d'une entrée d'eau (chambres) | dérivé de l'évidence | — | volets chambres, aération |
| `binary_sensor.intention_pluie_forte` | **Pluie forte** | fermeture **préventive** du volet séjour, **baie même fermée** | **Netatmo seul** (mesure quantitative) | `≥ seuil_pluie_fermeture_volets` (2,5 mm) | volets séjour |
| `binary_sensor.pluie_recente` | **Pluie récente (≤ 1 h)** | contexte « il a plu récemment » | Netatmo `last_hour` | `> 0` | aération, affichage |
| `sensor.pluie_prevue` | **Pluie prévue** | présomption d'horizon (jamais un fait) | prévision Met.no | horizon réglable | arrosage (prudence), affichage |
| `sensor.pluie_cumul_{24,48,72}h`, `sensor.pluie_journaliere` | **Cumuls / mesure** | mémoire quantitative | `sensor.pluie_total_local` | — | arrosage, palmarès, UI |

## 6. Distinction métier structurante — chambres ≠ séjour

**Opposable.** Les deux chaînes poursuivent des objectifs **différents** ; elles ne
doivent pas être unifiées :

| | **Chambres** | **Séjour** |
|---|---|---|
| Protection | **Fenêtre ouverte** (entrée d'eau) | **Ouvrant / façade** (préventif), baie même fermée |
| Déclencheur | détection précoce **+ fenêtre concernée ouverte** | **pluie forte** (indépendante de l'ouverture) |
| Signal | `pluie_en_cours` (any-rain) | `intention_pluie_forte` (pluie forte) |
| Premières gouttes | **déterminantes** | **non pertinentes** |

## 7. Invariants (normatifs, opposables)

- **INV-PROD-1 — Production ≠ réaction.** Aucun signal de ce contrat ne pilote un
  équipement ni n'émet de notification ; la réaction relève de contrats externes.
- **INV-PROD-2 — Qualifications plurielles par design.** *Détectée / en cours /
  forte / récente / prévue* sont des concepts distincts, **non fusionnables**.
- **INV-PROD-3 — Source légitime par qualification.** « Pluie forte » ne peut être
  qualifiée que par une **mesure quantitative** (pluviomètre) ; un détecteur binaire
  (SNZB-05) **ne qualifie jamais** « forte ». L'évidence *any-rain* peut être
  multi-source.
- **INV-PROD-4 — Distinction ouvrants (chambres ≠ séjour).** §6 est opposable :
  chambres = fenêtre ouverte (any-rain) ; séjour = préventif (pluie forte).
- **INV-PROD-5 — Trois régimes explicites.** Chaque source traite *nominal /
  absent / incohérent* (`principes_generaux.md` §6) ; **aucune indisponibilité de
  source ne fige un état**. En particulier, la sortie d'épisode ne dépend pas de la
  seule validité d'une source (correctif C16).
- **INV-PROD-6 — Disponibilité honnête.** Une qualification non calculable s'expose
  `unavailable` (`availability`), jamais une valeur factice.
- **INV-PROD-7 — Présomption ≠ fait.** `pluie_prevue` est une présomption : prévision
  absente ⇒ `unknown`, **jamais** 0 ; elle n'est **jamais** consommée comme pluie
  tombée.
- **INV-PROD-8 — Acquisition sécurisée (cible).** Toute qualification décisionnelle
  doit, à terme, consommer une **source sécurisée localement**
  (`securisation_capteurs_externes.md`), à l'image des cumuls (`pluie_total_local`).
  *Écart temporaire assumé* : les qualifications lisent encore les sources brutes ;
  résorption au **lot 2 du chantier C17**.
- **INV-PROD-9 — Frontière contractuelle.** Ce contrat est l'autorité de production
  des signaux de frontière de `volets_pluie.md` §5.2.

## 8. Régimes dégradés (référence)

| Situation | Comportement attendu |
|---|---|
| Netatmo absent, SNZB exploitable | l'évidence reste calculable ; l'épisode peut s'ouvrir/se fermer (pas de collage — INV-PROD-5) |
| SNZB mouillé prolongé (> fenêtre de fraîcheur) | présumé bloqué ; cesse d'être une évidence (borne) |
| Toutes sources réelles absentes | évidence `unavailable` ; backstop dégradé borné referme l'épisode |
| Prévision absente/vide | `pluie_prevue = unknown` (INV-PROD-7) |

## 9. Conformité / vérification

Vérifié mécaniquement par
[`check_pluie_production_contracts.py`](../../../scripts/arsenal_contracts/check_pluie_production_contracts.py)
(workflow `contracts_pluie_production.yml`) : présence des qualifications
canoniques, source quantitative exclusive de « pluie forte » (INV-PROD-3),
disponibilité honnête de l'évidence (INV-PROD-6), non-repli à 0 de la prévision
(INV-PROD-7), et **verrou anti-régression du correctif C16** (sortie d'épisode
consommant l'évidence + réconciliation démarrage + backstop dégradé — INV-PROD-5).

## 10. Renvois

- Réaction (frontière) : [`volets_pluie.md`](../volets_pluie.md) (§2, §5.2).
- Doctrine : [`securisation_capteurs_externes.md`](../../architecture/securisation_capteurs_externes.md), [`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md) (§6), [`capteurs_meteo.md`](../../architecture/capteurs_meteo.md) (périmètre distinct — §3).
- Chantier : [`cadrage_autorite_unique_precipitations.md`](../../audits/02_conception/meteo/cadrage_autorite_unique_precipitations.md) (C17), [`REGISTRE_CHANTIERS.md`](../../audits/REGISTRE_CHANTIERS.md).
- Palmarès (hors périmètre) : [`pluie_palmares.md`](pluie_palmares.md).
