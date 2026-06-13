# INVESTIGATION HISTORIQUE — CLIMATISATION ARSENAL (30 JOURS)
## Audit dynamique sur historique Recorder — constats factuels

> **Nature.** Investigation **empirique** (sur historique enregistré), en
> **complément** de l'audit **statique** [`audit_climatisation_arsenal.md`](audit_climatisation_arsenal.md)
> qui notait explicitement : « Home Assistant n'a pas été exécuté ; les
> comportements dynamiques sont déduits de la structure, pas observés. » Ce
> document **observe** le runtime via le Recorder ; il ne le remplace pas.
>
> **Statut.** Constats stabilisés. **Aucune modification fonctionnelle décidée,
> aucun réglage proposé.** Aucun contrat, automatisation, YAML ou runtime
> touché par cette investigation.
>
> **Runtime = référence.** Les seuils/consignes sont lus dans leur valeur
> courante et appliqués comme hypothèse de constance sur la fenêtre analysée.
>
> **Outil.** [`enquete_clim_historique.py`](../../../outils_externes/nas_arsenal/investigations/enquete_clim_historique.md)
> (NAS, REST API, lecture seule).

---

## 1. MÉTHODE D'AUDIT

### 1.1 Question d'investigation
Sur 30 jours, l'état réel du climatiseur est-il cohérent avec la décision que les
contrats prescriraient compte tenu des conditions réellement mesurées ? Où,
quand et pourquoi diverge-t-il ?

### 1.2 Chaîne d'analyse
1. Extraction **lecture seule** des primitives historisées (REST History API).
2. Lecture *live* des helpers de seuils/consignes (non historisés → hypothèse de
   constance, tracée).
3. **Timeline événementielle** : fusion des séries par changement d'état, maintien
   de la dernière valeur connue (cohérent avec la doctrine *event-based
   last-valid-state*).
4. **Reconstitution** des besoins bruts COOL/DRY (avec rétention d'hystérésis),
   seuils COOL appliqués (présence × helpers) et **autorisations observables**.
5. **Enveloppe de décision attendue** : `cool > dry > off` (ThermalPriorityPolicy
   v1). HEAT exclu (seuil dérivé d'une consigne non historisée).
6. Confrontation à l'état réel (`switch.clim_power` + `sensor.clim_mode_local`) et
   **qualification de l'écart** avec un niveau de confiance par ligne.

### 1.3 Posture épistémique
- La « décision attendue » est une **enveloppe instantanée**, pas une
  reconstitution de la mémoire d'admissibilité (verrou 2 portes, gardes 5 min).
- Un écart est un **candidat à instruire**, jamais une violation de contrat.
- Pondération **par durée**, pas par comptage de lignes.

---

## 2. LIMITES D'OBSERVABILITÉ (à lire avant tout constat)

Le `recorder.yaml` est en **liste blanche** : la chaîne décisionnelle n'est **pas
historisée**. Ne sont donc **pas observables** a posteriori :

| Entité / signal | Conséquence |
|---|---|
| `sensor.clim_target_mode` | La décision passée n'est pas lisible → reconstituée |
| `binary_sensor.besoin_clim_*` / `*_admissible` | Mémoire d'admissibilité non rejouable |
| `binary_sensor.autorisation_clim_*` | Recomposées partiellement (termes observables) |
| `sensor.seuil_*_clim_applique` | Recalculés depuis helpers |
| `binary_sensor.clim_blocage_horaire_reel` | **Non observable** (dépend d'`input_datetime`) |
| `binary_sensor.aeration_preferable_etage` | Terme inhibiteur non observable |
| `binary_sensor.fenetre_ouverte_maison_avec_delai` | Approximée **sans** temporisation |
| `timer.absence_longue_clim`, `input_boolean.blocage_clim_poele` | Non observables |
| `sensor.temperature_consigne_appliquee_locale` | HEAT non reconstituable → exclu |

> **Tout terme non observable ne peut pas être transformé en fait.** Les écarts
> imputables à ces signaux sont marqués `PARTIELLE` et restent des hypothèses.

---

## 3. RÉSULTATS FACTUELS

**Périmètre.** 24 156 lignes, 14/05/2026 → 13/06/2026 (≈ 720 h).

### 3.1 Conformité et écarts (pondéré durée)
| Écart | % temps | Confiance |
|---|---:|---|
| **OK** | **75,8 %** | — |
| CLIM_INACTIVE_vs_enveloppe | 15,7 % | **100 % PARTIELLE** |
| INDETERMINE_data (dont panne module 14–15/05) | 4,7 % | data/indispo |
| CLIM_ACTIVE_HORS_ENVELOPPE | 2,6 % | 90 % OBSERVABLE |
| DIVERGENCE cool↔dry | 1,2 % | 100 % PARTIELLE |

Confiance globale : 68 % `OBSERVABLE`, 31 % `PARTIELLE`, 0,9 % donnée manquante.
**Seul bloc sans excuse cachée possible** : `ACTIVE_HORS_ENVELOPPE` OBSERVABLE =
16,8 h / 720 (2,3 %), correspondant aux queues de refroidissement de fin de cycle.

### 3.2 Concentration temporelle
- **83 % du temps `CLIM_INACTIVE_vs_enveloppe` tombe entre 23 h et 06 h** (94,4 h
  sur 113,1 h), fenêtre fixe, bords nets à 23 h et 07 h. De jour, les écarts sont
  marginaux.
- Grappe d'écarts COOL/DRY concentrée sur l'épisode chaud **23–29/05** (ext.
  31–37 °C, chambres 25,6–26,6 °C).

### 3.3 Par dimension
- **COOL** : 1er poste d'écart (85 h). **DRY** : besoin humidex > seuil **149,6 h**,
  honoré 29,5 h en DRY + 51,2 h en COOL (priorité COOL). **HEAT** : quasi nul →
  **non évaluable** (hors saison).
- **Fenêtres** non contributives (0,1 h). **Absence** : tmax chambres n'a jamais
  atteint 27 °C (max 26,6) → la clim ne tourne presque pas hors présence.
- Écarts en **présence** : 146,8 h vs 27,4 h en absence (les besoins naissent en
  présence).

### 3.4 Court-cyclage COOL — diagnostic corrigé
Le diagnostic initial « 145 cycles, 69 % < 15 min » **surestimait** le phénomène.
Décomposition des 145 segments COOL contigus :
- **57 % (83) sont des blips < 1 min**, **non thermiques** : au moment du blip,
  tmax est en médiane **0,90 °C *sous* le seuil ON** (24 % seulement à ±0,5 °C).
  Signature de ré-assertions de contrôle / reflets du capteur de mode, pas d'une
  demande de froid.
- **Cycles substantiels (≥ 1 min)** : médiane **≈ 32 min** (présence), pas du
  court-cyclage. Temps COOL réel : 48 h présence vs 3,3 h absence.

### 3.5 Cohérence des seuils COOL (niveau)
- Allumages réels : tmax médian **25,0 °C** = seuil ON médian 25,0 °C.
- Extinctions réelles : tmin médian **24,5 °C** ≈ seuil OFF 25,0 °C.
- **Seuils cohérents en niveau** ; pas de dérive constatée.

---

## 4. HYPOTHÈSES VALIDÉES (par les données)

1. **Court-cyclage surestimé par un biais de comptage.** 57 % des segments COOL
   sont des blips non thermiques (tmax sous le seuil ON). *(§3.4)*
2. **Les cycles COOL substantiels durent en médiane ≈ 32 min** — pas du
   court-cyclage. *(§3.4)*
3. **Les seuils COOL sont cohérents en niveau** (allumage/extinction collés aux
   seuils). *(§3.5)*
4. **La présence est le *contexte* du refroidissement, pas sa *cause*** : les
   seuils absence (26/25) sont rarement atteints au vu du profil thermique. *(§3.3)*
5. **Le mécanisme dominant du cyclage résiduel** est la combinaison
   **bande d'hystérésis COOL de 1 °C × inertie thermique × arbitrage COOL↔DRY à
   proximité des seuils** (46,7 h où humidex et tmax sont simultanément à ≤ 0,5 °C
   de leurs seuils). *(§3.4)*

---

## 5. HYPOTHÈSES INVALIDÉES (par les données)

1. **« Le mode présence est la cause principale du court-cyclage. » → INFIRMÉE.**
   La présence est le régime où la clim refroidit (seuils absence rarement
   atteints), donc elle concentre les cycles ; mais les cycles présence
   substantiels durent ≈ 32 min. Le *mécanisme* de fragmentation est la bande
   étroite et l'arbitrage, pas le mode présence. *(§3.4, §4.4–4.5)*
2. **« Le “69 % < 15 min” reflète un court-cyclage thermique. » → INFIRMÉE.**
   Majoritairement des blips de contrôle/capteur. *(§3.4)*

---

## 6. HYPOTHÈSES OUVERTES (non tranchées — ne pas transformer en faits)

1. **Blocage horaire nocturne.** Le poste d'écart dominant (113 h, clim OFF) est à
   83 % nocturne avec une signature de fenêtre fixe. C'est **cohérent** avec un
   `clim_blocage_horaire_reel` actif la nuit, mais ce signal **n'est pas
   historisé** : l'hypothèse est **hautement probable mais non confirmée**.
2. **Nature exacte des blips** (ré-assertion watchdog/guard vs flottement du
   capteur de mode) : non résoluble sans historisation fine.
3. **Court-cyclage résiduel & arbitrage COOL↔DRY sans hystérésis** : observation à
   instruire, déjà adjacente au backlog hystérésis ouvert
   ([`backlog_climatisation_hysteresis.md`](../../04_chantiers/climatisation/backlog_climatisation_hysteresis.md)).
   **Aucune décision ni réglage n'est formulé ici.**

---

## 7. ENSEIGNEMENTS POUR LES FUTURES INVESTIGATIONS

1. **La liste blanche du Recorder détermine ce qui est auditable a posteriori.**
   Cartographier les angles morts **avant** de conclure ; ne jamais imputer un
   écart à un signal non historisé sans le marquer comme hypothèse.
2. **Distinguer l'artefact de comptage du phénomène physique.** Segmenter par
   durée **et** par transition (mode précédent/suivant) ; un « cycle » dont la
   température ne franchit pas le seuil n'est pas un cycle thermique.
3. **Enveloppe reconstituée ≠ décision.** Un écart `PARTIELLE` n'est pas une
   anomalie : il peut être expliqué par un blocage non observable ou par la
   mémoire d'admissibilité.
4. **Pondérer par durée, pas par lignes** (échantillonnage événementiel).
5. **Le gain d'observabilité le plus rentable** serait d'historiser les entités
   décisionnelles clés (`clim_target_mode`, `autorisation_clim_*`, seuils
   appliqués, `clim_blocage_horaire_reel`) pour transformer les 31 % `PARTIELLE`
   en observation directe et **confirmer ou infirmer** l'hypothèse nocturne (§6.1).
   *Constat d'observabilité — pas un réglage clim.*

---

## 8. DOCUMENTS ASSOCIÉS

- Audit statique (complété par cette investigation) :
  [`audit_climatisation_arsenal.md`](audit_climatisation_arsenal.md)
- Backlog dettes & hystérésis (ouvert) :
  [`backlog_climatisation_hysteresis.md`](../../04_chantiers/climatisation/backlog_climatisation_hysteresis.md)
- Chantier observabilité COOL (LIVRÉ v15.8.4, observabilité UI — périmètre distinct) :
  [`chantier_observabilite_cool.md`](../../04_chantiers/climatisation/chantier_observabilite_cool.md)
- Protocole d'observation seuils COOL (expérimental, en cours — utilise cette investigation comme référence « avant ») :
  [`protocole_observation_seuils_cool.md`](../../04_chantiers/climatisation/protocole_observation_seuils_cool.md)
- Outil d'investigation (NAS) :
  [`enquete_clim_historique.md`](../../../outils_externes/nas_arsenal/investigations/enquete_clim_historique.md)
- Hub de navigation : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)

---

*Investigation strictement descriptive. Runtime = référence. Aucun contrat,
automatisation, YAML ou réglage modifié. Les hypothèses non historisées restent
des hypothèses.*
