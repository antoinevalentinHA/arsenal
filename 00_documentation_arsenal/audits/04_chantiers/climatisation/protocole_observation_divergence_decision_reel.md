# Protocole d'observation — divergence décision ↔ état réel Climatisation (C30, Lot 1)

| Champ | Valeur |
|---|---|
| **Objet** | Recueillir, lors d'une **prochaine occurrence naturelle**, les faits permettant de qualifier une divergence entre la décision publiée par la chaîne Climatisation et l'état physique réel de l'équipement. |
| **Chantier** | **C30** — [`chantier_convergence_decision_execution_climatisation.md`](chantier_convergence_decision_execution_climatisation.md) (source faisant foi). |
| **Nature** | **Observation en lecture seule.** Non normatif. Ne propose aucun réglage, aucun correctif, aucune architecture. |
| **Exécutant** | **L'opérateur.** Aucun relevé n'est produit automatiquement à ce stade. |
| **Statut** | **Aucune preuve recueillie.** Trace §6 vide. |

> **⚠️ Aucune panne fabriquée.** Ce protocole ne demande **aucune dégradation artificielle**, aucun forçage
> d'état, aucune manipulation risquée de l'équipement ou de l'intégration. L'occurrence doit être
> **naturelle et non provoquée**. Un relevé obtenu par forçage est **irrecevable** et doit être marqué
> comme tel.

---

## 0. Prérequis et rappels

- Outils : **Outils de développement → États** de Home Assistant. Lecture seule.
- **⚠️ L'Historique n'est PAS un instrument disponible pour ce protocole** *(établi 2026-07-19)* :
  `climate.clim` et `sensor.fujitsu_age_donnees` sont **absents du Recorder** (allowlist stricte par
  entité). Ils sont donc inatteignables en base courante **comme** en sauvegarde hors ligne. Les relevés
  du §1 sont **exclusivement en temps réel**, avant tout rechargement.
- Ne rien redémarrer, ne rien recharger avant d'avoir consigné les relevés du §1 : **un rechargement
  détruit l'état observable**.
- Le déclencheur d'observation est un **doute**, pas une certitude : toute situation où la restitution
  annonce `À l'arrêt` alors qu'un doute existe sur la marche réelle de l'appareil justifie un relevé.

---

## 1. Relevés à consigner — au moment de l'occurrence

À relever **dans cet ordre**, avant toute action correctrice :

| # | Élément | Pourquoi |
|---|---|---|
| **1** | Constat physique direct (l'appareil souffle-t-il ? bruit, air, voyant) | **Seule preuve indépendante de l'intégration.** Sans elle, le relevé ne prouve rien. |
| **2** | `climate.clim` — état **et** `last_changed` | Cœur de C30-O1 / C30-O2. |
| **3** | `switch.clim_power` — état et `last_changed` | Seconde condition de la commande d'arrêt. |
| **4** | `sensor.clim_target_mode` — état et `last_changed` | Décision exécutable publiée. |
| **5** | `sensor.clim_action_en_cours` et `sensor.clim_raison_decision` | Restitution affichée (C30-O3). |
| **6** | `sensor.clim_mode_local` et `binary_sensor.clim_incoherence_decision_reel` | Détecteur de divergence (C30-O5). |
| **7** | `input_boolean.clim_execution_echec` et le compteur de budget de reprise | Vérifie C30-O4 : un échec est-il latché ? |
| **8** | `sensor.fujitsu_age_donnees`, `binary_sensor.gel_avere_airstage` | Fraîcheur de l'état rapporté (axe A3). |
| **9** | Consommation instantanée / cumul du jour (`…/consommation/`) | **N'est PAS un contre-signal indépendant** *(établi 2026-07-19)* : la chaîne dérive intégralement de `sensor.clim_mode_local`, donc de l'état rapporté. Elle **confirmerait** un `off` faux. Relevé pour contexte uniquement. |
| **10** | Contexte : fenêtre ouverte concernée, présence, mode nuit, rechargement ou redémarrage récent | Qualifie la situation. |

### Niveau de preuve (obligatoire)

Chaque relevé porte l'une de ces quatre valeurs. **Un relevé sans niveau de preuve est inexploitable.**

| Niveau | Signification |
|---|---|
| **P0 — HA seulement** | États lus dans HA, sans constat physique. **Ne prouve pas la divergence.** |
| **P1 — HA + constat physique** | États HA **et** vérification directe de la marche de l'appareil. **Niveau minimal pour qualifier une divergence.** |
| **P2 — P1 + contre-signal concordant** | S'ajoute une grandeur indépendante cohérente avec le constat physique. **⚠️ INATTEIGNABLE EN L'ÉTAT** *(établi 2026-07-19)* : aucune grandeur indépendante de l'intégration n'existe — aucun capteur de puissance physique, et la consommation estimée dérive de `sensor.clim_mode_local`. |
| **P3 — non confirmé** | Doute non levé, relevé incomplet, ou occurrence provoquée. **Irrecevable comme preuve.** |

---

## 2. Observation O1 — divergence constatée

Situation : constat physique = appareil **en marche**, restitution = `À l'arrêt`.

À qualifier : `climate.clim` rapporte-t-il `off`, `unknown`, `unavailable`, ou un mode actif ?
C'est ce point qui départage **« intégration qui rapporte faux »** de **« commande émise et non suivie
d'effet »** — la question ouverte centrale du chantier.

---

## 3. Observation O2 — abstention silencieuse

Situation : la décision exige l'arrêt, l'appareil tourne, et **aucun échec n'est latché**.

À consigner : `input_boolean.clim_execution_echec` à `off` **et** absence de notification. C'est la
signature de C30-O1 / C30-O4. Noter l'horodatage du dernier déclenchement connu de l'automation
d'application, s'il est lisible dans l'historique.

---

## 4. Observation O3 — comportement du détecteur

À consigner : `binary_sensor.clim_incoherence_decision_reel` est-il passé à `on` ? Après combien de temps ?
S'il est resté `off` alors que la divergence durait plus d'une minute, le noter explicitement — c'est un
fait sur le filet, distinct de la divergence elle-même.

---

## 5. Grille d'interprétation honnête

- **L'absence d'erreur ne prouve rien.** C'est la propriété défaillante décrite en C30-O1 : le silence
  est le symptôme, pas un verdict de conformité.
- **Un relevé P0 ne qualifie aucune divergence** : sans constat physique, la restitution et l'état
  rapporté peuvent être tous deux justes.
- **Une occurrence unique ne suffit pas à établir une cause.** Elle établit un fait daté.
- **Aucun verdict « conforme » ne peut être prononcé sur la seule non-reproduction.**
- Un relevé qui infirme une hypothèse du §3 du chantier est **aussi précieux** qu'un relevé qui la confirme,
  et doit être consigné avec le même soin.

---

## 6. Trace terrain *(à remplir par l'opérateur)*

> **Vide à ce jour.** Aucune occurrence consignée.
>
> **Les axes A3 et A4 de C30 ne sont pas clôturables tant que cette section reste vide.**
>
> **A5 et A6 ne dépendent pas de cette trace** : leurs constats sont démontrés statiquement (A5 non
> faisable avec les signaux existants ; A6 arbitré sur table de vérité). A1 est livré et A2 requalifié.

| Date/heure | Niveau de preuve | Constat physique | `climate.clim` | `switch.clim_power` | `clim_target_mode` | `action_en_cours` / `raison` | `incoherence_decision_reel` | `execution_echec` | Fraîcheur Airstage | Consommation | Contexte | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *(à compléter)* | | | | | | | | | | | | |

---

## 7. Décision différée

Aucune décision **relative aux axes A3 et A4** n'est prise avant qu'au moins un relevé de niveau **P1**
figure au §6. Ces deux axes restent ouverts jusque-là.

**A1, A2, A5 et A6 ne sont pas concernés** : ils ont été tranchés sur preuves statiques ou requalifiés
comme non solvables en l'état.

---

## 8. Renvois

- Chantier : [`chantier_convergence_decision_execution_climatisation.md`](chantier_convergence_decision_execution_climatisation.md)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Précédent de protocole d'observation du domaine : [`protocole_observation_seuils_cool.md`](protocole_observation_seuils_cool.md)
