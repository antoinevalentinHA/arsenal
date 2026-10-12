# Audit — Latence du désarmement automatique au retour

> **NAVIGATION — NON NORMATIF, NON DÉCISIONNEL.** Rapport d'audit probatoire. N'amende aucun contrat, ne modifie aucun YAML, ne décide rien.
> Index audits : [`../../index.md`](../../index.md) · Registre : [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
> Documents de famille faisant foi : [`contrats/alarme/30_decision_centrale.md`](../../../contrats/alarme/30_decision_centrale.md) · [`contrats/presence.md`](../../../contrats/presence.md) · [`contrats/mobile.high_accuracy.contextuel.md`](../../../contrats/mobile.high_accuracy.contextuel.md)

| Champ | Valeur |
|---|---|
| **Nature** | Diagnostic probatoire **L4** hors ligne ([`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)). Lecture seule. Aucune proposition implémentée. |
| **Date** | 2026-10-12 (dépôt de référence `origin/main` = `5e7cefe2`). |
| **Sources** | Sauvegarde Recorder du 2026-10-12 (HA 2026.10.1, fenêtre de 31 jours) et sept sauvegardes antérieures (couverture continue sur 105 jours) ; registres `.storage` de la même sauvegarde. |
| **Version intégrale** | `arsenal-runtime/analyses/alarme_latence_desarmement_20261012/` (hors dépôt gouverné) : `RAPPORT.md`, scripts relançables, `resultats.txt`. |
| **Rattachement** | Aucun chantier ouvert par ce rapport. Candidats : dossier dormant **D-PRES** (domaine présence) et **C1** (test S3) — cf. §9. |

> **Version publiée, volontairement agrégée.** Ce dépôt est public. La version versionnée ici ne contient **aucune date ni heure de retour**, **aucune fenêtre d'absence**, **aucun identifiant d'utilisateur ou d'appareil réseau**, **aucune coordonnée** et **aucun état opérationnel courant** de l'alarme. Seules figurent des distributions agrégées, des mécanismes et des décisions. Le détail retour par retour reste dans la version intégrale, hors dépôt.

---

## 1. Question et réponse courte

**Question.** Le désarmement automatique au retour intervient parfois après l'expiration du délai d'entrée de 60 s. L'opérateur refuse d'allonger le délai sans connaître l'origine de la latence.

**Réponse courte.**

1. **Arsenal ne coûte que 15,0 s, toujours exactement.** C'est le `delay_on` de `binary_sensor.presence_famille_securite_confirmee_alarme` (contrat 30). Le reste de la chaîne prend moins de 10 ms dans 86 retours sur 86 : décision centrale, `alarme_desarmer`, `alarm_disarm` et transition du panneau.
2. **Toute la variabilité est en amont** : il faut que Home Assistant reçoive une position du téléphone dans le rayon de `zone.maison_securite` (40 m). Pour les retours dont le délai a expiré, le signal brut passe durablement à `on` **60 s après l'ouverture en médiane** (de 46 à 91 s), contre 17 s pour les retours désarmés à temps.
3. **Quatre mécanismes**, mesurés sur 15 retours expirés :

| Mécanisme | Retours | Signature |
|---|---|---|
| **(a)** Fix « dans la zone » tardif, côté téléphone | 5 (tous P2) | fix pris 47 à 71 s après l'ouverture, à moins de 3 m du centre, livré en moins de 5 s |
| **(b)** Livraison retardée d'un fix déjà pris | 6 (dont 3 P1) | fix pris autour de l'ouverture, reçu par HA 40 à 113 s plus tard |
| **(c)** Position reçue hors du rayon effectif | 2 | géofence du téléphone reçue avant l'ouverture, mais à 65–70 m du centre : HA ne compte pas la présence |
| **(d)** Retombée sur une position périmée | 2 | une position récente fait passer le brut à `on` ; une position vieille d'environ 2 min, livrée dans la même rafale, le fait retomber ; le `delay_on` repart de zéro (+56 à +68 s) |

4. **La haute précision arrive trop tard.** Elle s'ouvre sur l'entrée géométrique en zone d'approche telle que HA la voit, donc sur une position déjà livrée. Sa fenêtre de 8 min n'était active à l'ouverture que pour 4 retours expirés sur 15.
5. **Le phénomène est ancien et stable** : 29 expirations sur 78 démarrages du délai sur 105 jours, soit 37 %.

P1 et P2 désignent les deux téléphones de la famille, dans l'ordre de `person.parent_1` et `person.parent_2`.

---

## 2. Méthode et sources

### 2.1 Reconstruction

Le Recorder applique sa liste blanche aux états **et** aux événements. Il n'y a donc ni `automation_triggered` ni `script_started` en base. En revanche, tous les événements `call_service` sont conservés, avec leurs données et leurs contextes. Ce sont eux qui portent la preuve (`R-L2-1`).

| Élément de la chaîne | Historisé ? | Reconstruction |
|---|---|---|
| Contacts d'accès (entrée, garage) | non | **oui** : `script.reconciliation_traiter_source` porte la source, l'état précédent et le nouvel état à chaque transition |
| `timer.delai_entree` | non | **oui** : `timer.start` (durée passée), `timer.cancel`, notification de fin de délai |
| Position du téléphone (`device_tracker.*`, `person.*`) | **non** | **partielle** : événements `android.zone_entered` / `android.zone_exited` de l'application Companion. Ils portent l'heure du **fix** (`time`) et la précision ; leur `time_fired` est l'heure de **réception** par HA |
| Activation de la haute précision | non | **oui** : appel `script.mobile_high_accuracy_on` |
| `binary_sensor.presence_wifi_maison`, capteurs BSSID | **non** | **non** |
| `binary_sensor.presence_famille_securite` (brut) | **oui** | — |
| `binary_sensor.presence_famille_securite_confirmee_alarme` | non | **indirecte** : son front `on` déclenche `script.alarme_decision_centrale` dans le contexte qui appelle aussi `alarm_disarm` |
| `alarm_control_panel.alarme_maison` | **oui** | — |

La causalité est suivie par les contextes : décision, désarmement et `alarm_disarm` partagent le même `context_id`, et la décision porte en `context_parent_id` le changement d'état déclencheur.

### 2.2 Définitions

- **Retour** : transition du panneau de `armed_away` à `disarmed` par la décision `PRESENCE`. 86 retours sur la fenêtre ; les désarmements `VISITEUR_PRESENT` et dashboard sont exclus.
- **T0** : première transition `off → on` d'un contact d'accès après l'armement. 73 retours sur 86 ont une ouverture observée ; les 13 autres sont des désarmements sans retour physique.
- **Front décisif** : dernier passage `off → on` du brut avant le désarmement, celui qui tient 15 s.

### 2.3 Limites

1. **Wi-Fi.** Ni les capteurs BSSID ni `presence_wifi_maison` ne sont historisés. Un front décisif sans géofence concomitante (4 retours expirés sur 15) peut venir du Wi-Fi ou d'une mise à jour de position hors géofence. Ce n'est **pas tranchable**.
2. **Branche du brut.** Le brut passe à `on` soit par `person.* == 'Maison securite'` (zone de 40 m), soit par la distance comparée à `input_number.zone_securite_radius`. La valeur de ce dernier n'est pas observable dans la sauvegarde.
3. **Horloge du téléphone.** L'écart fix → réception mélange retard de livraison et décalage d'horloge (borné à environ 2 s par le minimum observé).
4. **Autres sources locales.** Aucune source Bluetooth, routeur ou ping ne vise les téléphones (trackers `ping` désactivés, capteurs BLE de l'application désactivés, aucun `private_ble_device`).

---

## 3. Délais par étape

Valeurs en secondes relatives à T0 (négatif = avant l'ouverture), min / médiane / max. **E** = 15 retours expirés ; **A** = 19 retours désarmés pendant le délai ; **B** = 39 retours désarmés avant l'ouverture.

| # | Étape | E | A | B |
|---|---|---|---|---|
| 1 | Ouverture → démarrage du délai | 0,0 / 0,0 / 0,3 | 0,0 / 0,0 / 0,0 | — |
| 2a | Fix de la géofence d'approche (400 m), heure téléphone | −1361 / **−78** / +34 | −6556 / −93 / −16 | −1492 / −231 / −80 |
| 2b | Réception HA de la géofence d'approche | −1362 / **−0,8** / +74 | −6436 / −93 / +30 | −1426 / −173 / −46 |
| 2d | Fix de la géofence `maison_securite` (40 m), heure téléphone | −92 / **+11** / +71 | −68 / −12 / +41 | −777 / −108 / −20 |
| 2e | Retard fix → réception (`maison_securite`) | −1,7 / 4,4 / **116,7** | — | −1,9 / −0,5 / 100,7 |
| 2f | Réception HA de la géofence `maison_securite` | −75 / **+54** / +74 | −45 / +13 / +42 | −777 / −108 / −21 |
| 3b | Front `on` décisif du brut (tenu) | **+46 / +60 / +91** | −13 / +17 / +42 | −280 / −76 / −7 |
| 4 | Front décisif → décision `DISARMED` | 15,0 / 15,0 / 15,0 | idem | idem |
| 5–6 | Décision → `alarm_disarm` → panneau `disarmed` | < 10 ms | idem | idem |
| — | **Bout en bout, ouverture → `disarmed`** | **61,1 / 75,4 / 105,7** | 1,6 / 32,1 / 57,0 | −265 / −61 / +8 |

**Lecture.** L'écart entre E et A se forme **entièrement aux étapes 2d à 3b**, avant que HA ne reçoive une position dans les 40 m. Les étapes 4 à 6 sont identiques au dixième de seconde.

**Désarmement acquis**, sur 73 retours avec ouverture observée :

| au plus tard à | T0 | +30 s | +45 s | +60 s | +75 s | +90 s | +105 s | +120 s |
|---|---|---|---|---|---|---|---|---|
| retours | 38 | 48 | 53 | **58** | 64 | 71 | 72 | 73 |

**Différences entre téléphones** (géofences sur toute la fenêtre) :
- retard médian de livraison : **P1 18,6 à 32,6 s** (plus de 30 s dans un cas sur deux à un cas sur trois), **P2 environ 0 s** ; les deux ont des queues jusqu'à 120–237 s ;
- distance au centre au moment du fix d'entrée en `maison_securite` : P1 49 m en médiane (jusqu'à 78 m), P2 26 m ; précision médiane 12–13 m. La géofence du téléphone se déclenche donc souvent au-delà des 40 m que HA retient.

---

## 4. Faits établis et hypothèses

**Faits établis (L4).**
- **F1.** Arsenal apporte 15,0 s fixes et moins de 10 ms de traitement (86 retours).
- **F2.** Les retours expirés et ceux désarmés à temps se séparent avant HA, à l'arrivée d'une position dans les 40 m.
- **F3.** La livraison des géofences de P1 est lente ; celle de P2 est quasi immédiate, mais son fix « maison » est tardif.
- **F4.** La géofence du téléphone se déclenche régulièrement entre 40 et 78 m, là où HA ne compte pas encore la présence.
- **F5.** Les 18 paliers `on` interrompus du brut durent tous **moins de 15 s** (0 à 14,9 s, médiane 6,0 s) : le `delay_on` les a tous filtrés, **aucun faux désarmement**. Deux retours ont expiré à cause d'une retombée sub-seconde liée à une position périmée.
- **F6.** Fréquence stable : 37 % des démarrages du délai expirent, sur 105 jours.
- **F7.** Un contact d'accès resté bloqué à `on` empêche le délai d'entrée de démarrer (un cas observé).

**Hypothèses (non tranchées).**
- **H1.** Le retard de livraison de P1 vient de l'optimisation batterie ou du *batching* des géofences. Il faudrait un relevé des réglages du téléphone (L5).
- **H2.** Les retombées sub-seconde viennent d'une livraison hors d'ordre (position récente puis position périmée), et non du template. Il faudrait l'historique attributaire de `device_tracker.*` (L2).
- **H3.** Les fronts décisifs sans géofence viennent du Wi-Fi ou d'une position hors géofence. Il faudrait historiser temporairement les capteurs BSSID et `presence_wifi_maison` (L2).
- **H4.** Le fix tardif de P2 s'explique par une arrivée en voiture au garage : géofence évaluée à basse fréquence en mouvement, puis fix pris à l'arrêt.

---

## 5. Ce que le mode test neutralise

`input_boolean.mode_test_alarme` fait bifurquer, au titre du contrat 50 §I2, toutes les voies qui produiraient `triggered` : fin de délai (`10020000000032`), mouvement (`10020000000009`), autres ouvrants (`10020000000007`). Il neutralise aussi la sirène forte (`10020000000011`), tous les bips et, depuis C54, les scripts sonores (contrat 70, verrou *fail-open*). La décision centrale, l'armement, le désarmement, les timers et la haute précision **ne sont pas** neutralisés.

**Conséquence probatoire.** Sur la période étudiée, les expirations du délai ont toutes eu lieu en mode test. Elles sont donc observées jusqu'à la bifurcation (« fin de délai simulée »), mais jamais jusqu'à `triggered`. La garantie positive `ALM-CRIT-2` reste à établir par le test S3, **hors mode test** (cf. §7 et la rectification de [`cloture_ch1_alarme.md`](../../05_clotures/alarme/cloture_ch1_alarme.md) §10).

**Conditions à réunir avant de désactiver le mode test** (liste, sans recommandation) :
1. un délai d'entrée compatible avec la latence mesurée (queue à 105,7 s), ou une latence réduite et mesurée ;
2. aucun armement possible avec des occupants dans la maison : la période montre des armements sur fausse absence (visiteur ou garde d'enfants déclarés après l'armement, occupant à la frontière des 40 m) ;
3. le cas du contact d'accès bloqué qualifié au contrat `51_ouvrants_entree` ;
4. C54 : constat L5 du silence au désarmement depuis le dashboard, puis réserves R2/R3 (efficacité et payload du `stop`) ;
5. C54 : réserve R4 (visibilité de l'état du mode test) ;
6. C1 : le test S3, qui ne peut se faire qu'hors mode test et dans un cadre autorisé ;
7. la cohérence `sirene_max_duration` / `trigger_time` du contrat 70, vérifiée sur l'appareil ;
8. l'information du foyer.

---

## 6. Instrumentation qui lèverait les hypothèses

Une instrumentation **temporaire**, au sens du contrat Recorder (§ Instrumentation temporaire, six champs obligatoires), portant sur `binary_sensor.presence_wifi_maison`, les capteurs BSSID des deux téléphones et `binary_sensor.presence_famille_securite_confirmee_alarme`. L'historisation des `device_tracker.*` enregistrerait des coordonnées : c'est une donnée sensible, à arbitrer explicitement. Une vingtaine de retours suffiraient. Son admissibilité relève du propriétaire du contrat Recorder.

---

## 7. Propositions (non implémentées)

| | Contenu | Gain mesuré ou attendu | Risque principal |
|---|---|---|---|
| **P1** | Percevoir l'arrivée plus vite : demande de position aux téléphones à l'ouverture ; rayon effectif réexaminé ; réglages Companion de P1 | agit sur (a), (b), (c) — la cause mesurée | le rayon touche le signal de présence partagé ; la demande de position dépend de l'acheminement et de la batterie, sans risque de faux désarmement |
| **P2** | Réduire les 15 s de stabilisation quand l'ouverture est déjà constatée | 6 retours expirés sur 15 seraient passés sous 60 s | avec 5 s, 11 des 18 paliers filtrés auraient tenu : risque de faux désarmement ; valeur normative du contrat 30 |
| **P3** | Délai d'entrée adaptatif, allongé seulement si une approche d'un téléphone de la famille est connue | approche connue avant l'ouverture dans 7 retours expirés sur 15 | fenêtre d'intrusion plus longue ; décision introduite dans une automation qui « ne décide rien » |

---

## 8. Décisions restant à l'opérateur

1. Rattachement : D-PRES, C1, ou un chantier dédié (règles du registre).
2. Choix parmi P1, P2, P3 (combinables), ou statu quo motivé.
3. Instrumentation temporaire (§6).
4. Relevé des réglages Companion des deux téléphones (L5).
5. Statut d'usage du mode test.
6. Qualification des armements sur fausse absence et du contact bloqué.

---

## 9. Rattachement — éléments pour l'arbitrage

- **D-PRES** ([`cadrage_dette_modelisation_presence.md`](../../02_constats/transverses/cadrage_dette_modelisation_presence.md)) est l'autorité thématique de la cause mesurée : il décrit déjà la haute précision « asservie à l'état de l'alarme » (R4), la piste P-D (« rebrancher la haute précision sur un signal d'approche neutre ») et la question §9-6 (« quelqu'un rentre » comme état d'anticipation). Son déclencheur de réveil (« ouverture explicite d'une question d'arbitrage ») est un acte de l'opérateur.
- **C1** dépend de ce constat : S3 exige un mode test désactivé, donc une latence maîtrisée (condition 1 du §5).
- **C54** n'est pas concerné par la latence.

---

*Rapport d'audit. Lecture seule ; aucun runtime, contrat, checker ni registre modifié par ce document.*
