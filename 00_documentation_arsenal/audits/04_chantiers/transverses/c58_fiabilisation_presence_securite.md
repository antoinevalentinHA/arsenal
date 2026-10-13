# Chantier TRANSVERSE (C58) — Fiabilisation de la présence sécurité et du cycle désarmement / réarmement

| Champ | Valeur |
|---|---|
| **Chantier** | Rendre fiable et rapide le cycle **présence → désarmement → absence → réarmement** de l'alarme, en traitant les causes de latence et d'incohérence dans les **sources de présence**, sans complexifier la décision. |
| **Domaine** | Transverse — présence (sécurité) ; consommateur principal : alarme. |
| **Statut** | **Ouvert (2026-10-13) — lot 1 (Wi-Fi) préparé, non déployé.** |
| **Priorité** | P1 |
| **Ouvert le** | 2026-10-13, par promotion partielle du dossier dormant **D-PRES** sur décision de l'opérateur. |
| **Dossier d'origine** | [`cadrage_dette_modelisation_presence.md`](../../02_constats/transverses/cadrage_dette_modelisation_presence.md) (D-PRES) — questions §9-1, §9-4 et §9-6, risques R4, R7, R8. Le reste de D-PRES demeure dormant. |
| **Constat d'entrée** | [`audit_latence_desarmement_automatique.md`](../../01_rapports/alarme/audit_latence_desarmement_automatique.md) |
| **Registre** | Ligne **C58**, ① Actifs, [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). Ce document est la source faisant foi. |
| **Dépendances** | **C1** dépend de C58 : le test positif S3 exige une latence de désarmement maîtrisée. **C54** conserve son périmètre propre. |

> **Confidentialité.** Le dépôt est public. Ce document ne contient ni BSSID, ni coordonnée, ni horaire de déplacement, ni information d'absence, ni état opérationnel courant de l'alarme. Les mesures détaillées restent hors dépôt (`arsenal-runtime/analyses/`).

---

## 1. Orientation de l'opérateur (2026-10-13)

1. **L'alarme est un dispositif de confort et de dissuasion**, pas une télésurveillance. Priorités, dans l'ordre : désarmement rapide et automatique à l'arrivée, réarmement fiable au départ, aucun déclenchement sonore intempestif, architecture simple et robuste.
2. **Désarmement transitoire de proximité accepté.** Un téléphone de la famille passant près du domicile peut désarmer l'alarme. Ce n'est pas un faux désarmement à éliminer, à condition que l'alarme se **réarme** lorsque les conditions d'armement sont de nouveau réunies.
3. **Inacceptable** : qu'une information périmée, un équipement inutilisé ou un défaut de réconciliation laisse **durablement** l'alarme dans un état incohérent.
4. **Wi-Fi maintenu.** La présence sécurité peut être établie par le GPS **ou** par le Wi-Fi domestique, sans confirmation simultanée des deux sources.
5. **Ordre de priorité** : (1) remettre le Wi-Fi en fonctionnement ; (2) optimiser les réglages du téléphone de Parent 2, puis de Parent 1 ; (3) retirer l'appareil inutilisé des sources de Parent 1 ; (4) mesurer ; (5) étudier des améliorations GPS supplémentaires seulement si elles restent utiles.
6. **Inchangés jusqu'à nouvel arbitrage** : réglages de fonctionnement de l'alarme, temporisations (`delay_on` 15 s du désarmement, 5 min de l'absence confirmée), délai d'entrée, politique d'armement. Le rayon de `zone.maison_securite` n'est pas intangible, mais ne change pas sans étude des consommateurs.

---

## 2. Défauts confirmés

| Id | Défaut | Preuve | Impact |
|---|---|---|---|
| **D1** | **Branche Wi-Fi inerte depuis le 2026-03-31.** `binary_sensor.presence_wifi_maison` comparait le référentiel canonique (12 hex) au BSSID brut Companion (`aa:bb:…`) sans normaliser ce dernier, en violation de `bssid.md` §6/§11. `binary_sensor.wifi_nouveau_bssid` normalisait correctement. | lecture du code ; format du référentiel vérifié dans les sauvegardes ; test de rendu (l'ancien template échoue sur 9 cas sur 14) | le Wi-Fi, conçu comme source rapide et indépendante du GPS, n'a contribué à aucune présence ; plus de fausses absences au domicile |
| **D2** | **Aucune protection contre un BSSID figé.** Le capteur BSSID n'est publié qu'au changement ; une transition perdue fige la valeur sans expiration. | code Companion (`NetworkSensorManager`) et HA (`mobile_app`) | sans correction, D1 corrigé seul aurait pu maintenir une présence fictive |
| **D3** | **Appareil inutilisé dans les sources de `person.parent_1`.** Un appareil rangé reste un tracker actif de la personne ; HA retient le tracker GPS le plus récent. | registre `person` | chemin potentiel de présence fictive pour Parent 1 (terme `person.parent_1 == 'Maison securite'`) |
| **D4** | **Divergence contrat / code sur `person.*`.** `presence.md` affirme que la présence sécurité ne consomme aucune projection `person.*` ; `presence.yaml` teste `person.parent_* == 'Maison securite'`. | lecture | ambiguïté sur les sources autorisées ; D3 n'est un risque que parce que ce terme existe |
| **D5** | **Haute précision tardive et neutralisée.** Activée par HA sur l'approche vue par HA (donc après une livraison parfois retardée), envoyée sans priorité FCM, et désactivée en totalité par `turn_off` à chaque désarmement. | contrat `mobile.high_accuracy.contextuel`, code Companion | la densification GPS n'aide presque jamais au moment de l'arrivée (cf. constat d'entrée) |
| **D6** | **Détection d'arrivée GPS sur une géofence de 40 m**, sous le minimum recommandé par Android (100 à 150 m). | doc Android ; distances mesurées | cause structurelle de la latence GPS (constat d'entrée) |

---

## 3. Lots

| Lot | Contenu | Nature | État |
|---|---|---|---|
| **L1** | Wi-Fi : normalisation des deux côtés + règle de fraîcheur (`bssid.md` §11.1) ; contrôles T16/T17 ; test de rendu | runtime + contrat + CI | **préparé (PR), non déployé** |
| **L2** | Réglages des téléphones (Parent 2 prioritaire, puis Parent 1), relevé de l'historique de localisation Companion | acte opérateur sur les téléphones | à faire |
| **L3** | Retrait de l'appareil inutilisé des trackers de `person.parent_1`, après inventaire des dépendances | configuration HA (interface Personnes) | à faire, sur GO |
| **L4** | Mesure avant / après (analyse hors ligne d'une sauvegarde) | analyse | après L1–L3 |
| **L5** | Améliorations GPS conditionnelles : anneau d'approche haute précision natif Companion (exige la fin du `turn_off` Arsenal, amendement `mobile.high_accuracy.contextuel`), et/ou rayon de `zone.maison_securite` | contrat + runtime | conditionnel aux résultats de L4 |
| **L6** | Alignement contractuel des sources de présence sécurité (D4) | contrat | sur arbitrage |

### 3.1 Lot 1 — Wi-Fi (préparé)

- **Normalisation** : référentiel **et** valeur observée passés par `lower | replace(':','') | replace('-','')`, validation 12 hex, conformément à `bssid.md` §6. La sémantique OU est conservée : un seul téléphone en Wi-Fi domestique suffit.
- **Fraîcheur** (`bssid.md` §11.1) : le Wi-Fi d'un téléphone ne compte plus si le GPS **du même téléphone** est passé à `not_home` **après** le dernier changement de son BSSID. La source la plus récente l'emporte. Un GPS muet ne retire jamais le Wi-Fi. Aucune expiration temporelle (limite assumée, §11.1).
- **Effets attendus** :
  - le Wi-Fi redevient une source de présence, indépendante du GPS, typiquement à la porte ;
  - une fausse absence au domicile devient plus rare, ce qui réduit les armements avec occupants quand un téléphone est connecté ;
  - un téléphone resté au domicile en Wi-Fi maintient la présence, ce qui empêche l'armement automatique. C'est cohérent avec la règle « GPS OU Wi-Fi ».
- **Consommateurs du signal brut** concernés par la remise en service : désarmement et armement automatiques (via les projections confirmées, contrat 30), présence confort (`presence_famille_unifiee`), et les consommateurs directs du brut (ECS / bouclage, volets, éclairage jardin). Tous en lecture du même signal ; l'effet est une présence au domicile plus continue.
- **Aucun ID créé, aucun alias ni entité renommés.** Déploiement : `template.reload`.

---

## 4. Critères de clôture

1. L1 déployé, puis la présence Wi-Fi constatée en conditions réelles (un téléphone connecté au Wi-Fi domestique produit `binary_sensor.presence_wifi_maison = on`), et la règle de fraîcheur constatée au départ.
2. L2 et L3 réalisés et consignés (sans données sensibles).
3. Mesure L4 : la part des retours désarmés avant l'échéance du délai d'entrée progresse nettement par rapport au constat d'entrée, **sans** état incohérent durable (absence persistante non reconnue, présence fictive durable, réarmement manqué).
4. Le cycle de réarmement est démontré pour les scénarios de l'analyse de cycle (passage à proximité, arrivée puis départ, perte de Wi-Fi au domicile, arrêt de transmission, position périmée, départ d'un seul parent, appareil inutilisé, sources contradictoires).
5. L5 instruit : retenu, ou abandonné par décision motivée.
6. D4 tranché et le contrat `presence.md` aligné.

---

*Chantier ouvert le 2026-10-13. Source faisant foi pour la ligne C58 du registre.*
