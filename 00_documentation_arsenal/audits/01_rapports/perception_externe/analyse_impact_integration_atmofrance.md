# 🌫️ ARSENAL — ANALYSE D'IMPACT — Intégration **Atmo France** (qualité de l'air extérieur)

> **Trace d'analyse documentaire, lecture seule.** Aucune correction runtime : ni script, ni
> automation, ni template, ni registre, ni contrat, ni checker, ni UI, ni recorder modifiés.
> Aucune entité créée, renommée ou supprimée. **Aucun patch produit à ce stade.**
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse · **[RECO]** recommandation.

| Champ | Valeur |
|---|---|
| **Déclencheur** | Installation de l'intégration `atmofrance` (commit [`0a48ce0`](#) — `chore(atmofrance): installation de l'intégration`) |
| **Nature** | **Analyse d'impact transverse.** Où cette perception externe *peut* jouer un rôle, et à quelles conditions contractuelles |
| **Posture** | **Lecture seule assumée** — la remontée est consommée par aucun domaine Arsenal à ce jour |
| **Sources normatives touchées** | [`aeration_recommandation.md`](../../../contrats/aeration_recommandation.md) · [`vmc.md`](../../../contrats/vmc.md) v2.6 · [`resilience_integrations.md`](../../../contrats/resilience_integrations.md) |
| **Composant** | `custom_components/atmofrance/` (v2.1.2, `iot_class: cloud_polling`, `codeowner @sebcaps`) |

---

## Verdict

**Perception externe pertinente, mais à brancher avec discernement — un seul domaine l'accueille
sans friction contractuelle (l'aération–recommandation) ; le second visé (la VMC) entre en collision
frontale avec un invariant délibéré du contrat en vigueur.**

- **[FAIT] Aération — Recommandation : terrain d'accueil naturel.** La recommandation d'aération est
  précisément un conseil d'**ouvrir les fenêtres**, c.-à-d. d'exposer l'intérieur à l'air extérieur.
  Y introduire un critère « air extérieur dégradé » comme **inhibiteur** est *dans le périmètre* du
  contrat — mais exige, per son §PORTÉE, **un nouveau contrat ou une fusion contractuelle explicite**,
  et l'arbitrage sanitaire **pollution ↔ CO₂** doit être tranché ouvertement.
- **[FAIT] VMC : l'idée « rester en vitesse lente en cas de pic particulaire » n'est pas implémentable
  sous le contrat v2.6 en l'état.** Elle heurte l'**invariant de hiérarchie §1.2** (O1/O2 humidité +
  voie CO₂ prioritaires) et surtout l'**interdiction déguisée §7.4** : un modulateur qui, sur une
  plage de conditions **durables** (un épisode de fumées d'incendie dure des jours), rendrait la voie
  humidité **inopérante**, est *contractuellement interdit*. Le besoin exprimé est **physiquement
  fondé** (VMC simple flux sans filtration, §1.4) mais requiert une **évolution de contrat arbitrée**,
  pas un réglage.
- **[FAIT] La donnée est un indice composite, prévisionnel, à maille commune et à rafraîchissement
  horaire** — pas une mesure physique instantanée in situ. Cette nature conditionne *tout* usage
  décisionnel (voir §3.2 et §5.2).
- **[FAIT] Le composant masque ses propres pannes en `0` (« Indisponible »)** — un piège classique au
  regard de la doctrine de résilience : `0` n'est **pas** « bon », c'est « pas de donnée ».

**Gravité globale : P2** — aucune anomalie runtime (rien n'est branché), mais une décision
d'architecture et un arbitrage sanitaire sont requis avant tout branchement, et un point de résilience
est à traiter dès qu'une entité `atmofrance` devient une entrée décisionnelle.

---

## 1. Ce que l'intégration expose réellement

### 1.1 Entités (device « Atmo France - Bordeaux », 12 entités)

**[FAIT]** Six polluants « jour courant » + six prévisions « J+1 » (`const.py::POLLUTION_SENSORS`,
`sensor.py`) :

| Grandeur | Nom d'entité (capture) | `entity_id` vraisemblable **[HYP]** | `device_class` |
|---|---|---|---|
| Dioxyde d'azote (NO₂) | `Dioxyde d'azote-Bordeaux` | `sensor.dioxyde_d_azote_bordeaux` | `AQI` |
| Dioxyde de soufre (SO₂) | `Dioxyde de soufre-Bordeaux` | `sensor.dioxyde_de_soufre_bordeaux` | `AQI` |
| Ozone (O₃) | `Ozone-Bordeaux` | `sensor.ozone_bordeaux` | `AQI` |
| Particules PM10 | `PM10-Bordeaux` | `sensor.pm10_bordeaux` | `AQI` |
| Particules PM2.5 | `PM25-Bordeaux` | `sensor.pm25_bordeaux` | `AQI` |
| **Indice global** | `Qualité globale-Bordeaux` | `sensor.qualite_globale_bordeaux` | *(aucune)* |

Plus les variantes prévisionnelles `…-Bordeaux-J+1` (`entity_id` en `…_bordeaux_j_1` **[HYP]**).

> **[FAIT] Les `entity_id` exacts relèvent du registre Home Assistant, non du dépôt.** Ils sont donnés
> ici en hypothèse (slugification standard). **Tout branchement futur devra relever l'identifiant
> réel**, jamais le supposer — conformément à la doctrine Arsenal « identifiants relevés, jamais
> supposés ».

### 1.2 Sémantique de l'état — un **indice ATMO 0–7**, pas une concentration

**[FAIT]** L'état de chaque capteur est un **code entier** de l'échelle ATMO
(`const.py::POLLUTION_LEVEL`), et non un µg/m³ :

| Code | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Libellé | **Indisponible** | Bon | Moyen | Dégradé | **Mauvais** | Très mauvais | Extrêmement mauvais | Évènement |

Attributs exposés : `Libellé` (texte) et `Couleur` (hex). Rafraîchissement `REFRESH_INTERVALL = 60`
(minutes) ; `cloud_polling`.

**[FAIT] Ancrage terrain (captures du 30/07).** Au moment de l'installation :
`PM10-Bordeaux = 4`, `PM25-Bordeaux = 4`, `Qualité globale-Bordeaux = 4` (**Mauvais**),
`Ozone = 2`, `NO₂ = 1`. Cohérent avec l'épisode de fumées d'incendie décrit — c'est très exactement
le cas d'usage qui motive l'analyse.

### 1.3 Piège de résilience : `0` = panne masquée

**[FAIT]** En cas d'échec de récupération, `sensor.py::native_value` **force la valeur à `0`**
(log : *« Unable to get value … Force value to 0 »*). Or `0` porte le libellé **« Indisponible »**.

> **Conséquence normative.** Un consommateur naïf qui lirait `state | int` et testerait
> `>= seuil` verrait `0` comme *meilleur que « Bon »* — une panne réseau serait silencieusement
> interprétée comme « air parfait ». C'est l'exact anti-pattern que la doctrine VMC (§4.4 : *une mesure
> inexploitable ne doit jamais être assimilée à une valeur numérique de repli*) et l'audit
> [`resilience_integrations`](../resilience_integrations/audit_resilience_integrations_domaine.md)
> (non-substitution) proscrivent. **[RECO]** Tout template consommateur doit d'abord neutraliser
> `unknown` / `unavailable` **et** le code `0`, et traiter ce triplet comme « donnée non exploitable »
> — jamais comme une valeur basse.

---

## 2. Cartographie d'impact par domaine

Recensement : **aucune** occurrence de `atmofrance` / qualité d'air / PM dans `12_template_sensors`,
`11_automations`, `06_input_selects`, `18_lovelace` (grep du dépôt). **[FAIT] L'intégration est
aujourd'hui totalement débranchée de la logique Arsenal** — état attendu d'une installation en lecture
seule.

| # | Domaine | Rôle possible | Friction contractuelle | Prio |
|---|---|---|---|---|
| **D1** | **Aération — Recommandation** | Inhibiteur « air extérieur dégradé » dans la hiérarchie de décision | **Faible** — dans le périmètre ; exige nouveau contrat/fusion + arbitrage CO₂ | **P2** |
| **D2** | **VMC** | *Idée utilisateur* : forcer la basse vitesse en pic particulaire | **Bloquante** — heurte §1.2 + §7.4 (interdiction déguisée) ; nécessite évolution de contrat | **P2** |
| **D3** | **Climatisation** | Propagation *transitive* via l'inhibiteur d'aération déjà consommé | Nulle (hérite de D1) | P3 |
| **D4** | **Notifications** | Avertissement « épisode de pollution, garder fermé » | Moyenne — **ne peut pas** dériver de l'état d'aération (interdit §INVARIANTS) ; domaine propre requis | P3 |
| **D5** | **Résilience des intégrations** | Inscrire `atmofrance` au registre ; gérer le `0` masqué | Faible — dette d'intégration à déclarer | P2 |
| **D6** | **Rétention / recorder** | Décision d'inclusion des 12 entités | Nulle — housekeeping | P3 |

---

## 3. D1 — Aération : le terrain d'accueil naturel

### 3.1 Où le critère s'insère **[FAIT]**

Le moteur `binary_sensor.aeration_preferable_etage`
(`12_template_sensors/aeration/conseillee/etage.yaml`) décide selon une **hiérarchie ordonnée**
(contrat §PRÉCÉDENCE, rappelée dans le code `:243-259`) :

| Rang | Condition actuelle | Motif |
|---|---|---|
| 1 | données critiques indisponibles | `inconnue` |
| 2 | `CO₂ ≥ seuil fort` | `co2_priorite` |
| 3 | canicule active **et** `CO₂ < seuil` | `canicule` |
| 4 | pluie en cours | `pluie_recente` |
| 5 | `ΔHA < seuil` | `seuil_ha_non_atteint` |
| 6 | `ΔT < seuil` | `seuil_dt_non_atteint` |
| 7 | sinon | `aeration_ok` |

**[FAIT] Il n'existe aucun terme « qualité de l'air extérieur ».** Un inhibiteur pollution
s'insérerait comme un rang **bloquant** supplémentaire (nouveau motif, p.ex. `air_exterieur_degrade`),
au même titre structurel que `pluie_recente` — un contexte extérieur qui rend l'ouverture
contre-productive. L'implémentation suivrait exactement le patron existant de `pluie` : un booléen
dérivé + un rang dans l'ordre + un motif + une icône + l'attribut `decision`.

### 3.2 L'arbitrage à trancher **ouvertement** : pollution vs CO₂

C'est le **cœur** de la décision, pas un détail :

- Le rang 2 (`co2_priorite`) **prime aujourd'hui sur tout**, y compris la pluie (§PRÉCÉDENCE
  CO₂ vs PLUIE). Le CO₂ pousse à **ouvrir** ; la pollution particulaire pousse à **fermer**. Ce sont
  **deux impératifs sanitaires antagonistes**.
- **[HYP → à arbitrer]** Où placer `air_exterieur_degrade` ?
  - **au-dessus** du CO₂ → on refuse d'aérer même à CO₂ fort quand l'air extérieur est mauvais
    (on préfère un CO₂ élevé transitoire à l'inhalation de PM2.5). Cohérent en pic « Très mauvais/
    Évènement » ; discutable en simple « Dégradé ».
  - **en-dessous** du CO₂ → la priorité sanitaire CO₂ l'emporte, la pollution ne bloque que hors
    dérogation CO₂. Plus proche de l'esprit actuel (le CO₂ est « prioritaire absolu »).
  - **modulé par niveau** → pollution « Mauvais » (4) bloque sauf CO₂ fort ; « Très mauvais »/
    « Évènement » (5-7) bloque *aussi* le CO₂. C'est l'option la plus fidèle à l'échelle ATMO.
- Ce choix est un **arbitrage propriétaire**, exactement le genre que la doctrine impose de rendre
  explicite (jamais tranché implicitement par l'implémentation).

### 3.3 Contraintes de forme héritées du contrat **[FAIT]**

- **UI uniquement, aucune notification.** Le §INVARIANTS ABSOLUS interdit *toute* notification liée à
  l'état de recommandation — y compris indirecte. Un « prévenez-moi qu'il ne faut pas aérer » **ne peut
  pas** être bâti sur ce capteur (voir D4).
- **Tolérance `unknown`/`unavailable`** obligatoire (§ROBUSTESSE) — et ici, en plus, le **`0` masqué**
  (§1.3) doit être neutralisé.
- **J ou J+1 ?** La recommandation est instantanée ; le capteur « jour courant » est l'entrée
  naturelle. Le « J+1 » relèverait d'une logique d'anticipation — hors esprit « observation du présent »
  du domaine.

> **[RECO] D1 est le premier pas raisonnable, en lecture seule d'abord :** afficher l'indice extérieur
> comme **contexte** sur la carte d'aération (sans effet décisionnel) permet d'observer la donnée en
> situation *avant* d'ouvrir le contrat. Le branchement décisionnel vient ensuite, via contrat.

---

## 4. D2 — VMC : pourquoi « rester en vitesse lente » heurte le contrat

### 4.1 Le besoin est physiquement fondé **[FAIT]**

Le §1.4 établit un réseau **simple flux, moteur unique, deux régimes**, sans filtration. Physiquement,
la haute vitesse **accroît la dépression** et **aspire davantage d'air extérieur** par les entrées
d'air — donc davantage de particules non filtrées en épisode de fumées. L'intuition « ne pas
sur-ventiler avec de l'air extérieur pollué » est **correcte en physique**.

### 4.2 Mais trois barrières contractuelles s'y opposent **[FAIT]**

1. **Invariant de hiérarchie §1.2.** O1/O2 (limiter condensation/humidité **à la source**) sont
   *prioritaires* ; O3 (assèchement global, confort) est secondaire. *« Un critère servant O3 ne peut
   être employé comme condition d'autorisation d'une extraction locale. »* La qualité de l'air extérieur
   relève au mieux de O3 : la subordonner à O1/O2 est explicitement proscrit — c'est d'ailleurs déjà le
   motif par lequel le §4.3 **écarte** `aeration_preferable_etage` de toute voie décisionnelle VMC.

2. **Interdiction déguisée §7.4.** *« Un modulateur qui, dans une plage de conditions durables — une
   saison, une plage horaire récurrente, un régime météorologique courant — rendrait la voie humidité
   inopérante, constitue une interdiction déguisée et est contractuellement interdit. »* Un épisode de
   fumées d'incendie **dure des jours** : c'est une condition durable. Un verrou « basse vitesse tant
   que PM élevé » **rendrait la voie humidité (et la voie CO₂) inopérante** pendant tout l'épisode →
   interdiction déguisée caractérisée (§12.3).

3. **Nature de la grandeur modulante §6.4 / §4.3.** Le seul assouplissement admis (§7.4 bis) est la
   modulation d'une **frontière de libération** par une **mesure physique instantanée brute
   extérieure** — *« ni à un verdict composite relevant d'un objectif secondaire »*. Or
   `Qualité globale` **est** un verdict composite ; même `PM25` est un **indice** (0-7), pas une
   concentration, et de surcroît **prévisionnel à maille commune, rafraîchi à l'heure** — l'antithèse
   d'une « mesure physique instantanée ». Il n'est pas éligible comme grandeur modulante au sens strict.

### 4.3 Ce qui, en revanche, est admissible **[FAIT/RECO]**

- **[FAIT] Pur affichage informatif — déjà prévu.** La refonte UI VMC du 2026-07-25 (§16.6) a introduit
  une section **« Conditions actuelles »** exposant *humidité SDB, CO₂ et **air extérieur*** en régime
  automatique. Le §10.5 autorise explicitement une information contextuelle **présentée comme telle**,
  sans rôle décisionnel. **C'est le point d'accroche naturel et immédiat de `atmofrance` sur la VMC** :
  y refléter l'indice extérieur, sans qu'aucune décision n'en découle.
- **[FAIT] Le levier utilisateur existe déjà : l'autorité de domaine (§16).** En épisode de pollution,
  l'utilisateur peut **passer la VMC en régime manuel** et imposer `basse` — c'est précisément la
  « révocabilité de la délégation » du §16.1. Le besoin exprimé est donc **déjà couvert** par une prise
  de main manuelle, sans toucher au contrat.
- **[HYP → arbitrage lourd] Automatiser réellement le comportement** supposerait une **évolution de
  contrat (v2.7)** qui : (a) reconnaisse un objectif sanitaire « import de pollution » ; (b) le concilie
  avec O1/O2/CO₂ sans les rendre inopérants (donc **jamais** un verrou dur, au plus un modulateur
  **borné** ne pouvant rendre une voie impossible, §7.4) ; (c) statue sur la contradiction directe avec
  la **voie CO₂ de sécurité** (piéger 1200 ppm de CO₂ pour éviter des PM extérieures est un arbitrage
  santé-vs-santé). Ce n'est pas un réglage : c'est un arbitrage de conception, à ouvrir comme tel.

> **Synthèse D2.** L'idée n'est pas rejetée sur le fond ; elle est **hors d'atteinte du contrat actuel**
> et son automatisation demanderait de rouvrir des invariants délibérés. Le besoin immédiat
> (« en ce moment, à cause des incendies ») se traite **aujourd'hui** par la prise de main manuelle
> (§16) et l'**affichage** de l'air extérieur (§10.5, déjà en place).

---

## 5. Domaines périphériques

### 5.1 D3 — Climatisation (transitif)
**[FAIT]** `binary_sensor.aeration_preferable_etage` est déjà consommé par la climatisation comme
**inhibiteur** (veto cool/dry, contrat aération §PÉRIMÈTRE TRANSVERSE). Si D1 introduit un terme
pollution *dans* la recommandation, l'effet se **propage transitivement** à la clim sans câblage
nouveau. À garder en tête lors de l'arbitrage D1 : bloquer l'aération pour cause de pollution ne doit
pas, par ricochet indésirable, débloquer la clim de façon incohérente. À vérifier au moment du branchement.

### 5.2 D4 — Notifications (domaine **propre** requis)
**[FAIT]** Le §INVARIANTS de l'aération–recommandation **interdit toute notification** dérivée de son
état, *« y compris de manière indirecte ou via un autre domaine »*. Un avertissement « pic de pollution,
gardez fermé » est légitime **mais** doit constituer un **domaine de notification autonome**, branché
**directement** sur les capteurs `atmofrance` (p.ex. transition vers indice ≥ 5), **jamais** sur
`binary_sensor.aeration_*`. À concevoir séparément si souhaité.

### 5.3 D5 — Résilience des intégrations (à traiter dès le premier branchement)
**[FAIT]** `atmofrance` (`cloud_polling`, dépendance WAN) **n'est pas** au registre
`resilience_integrations_registre.yaml`. Deux points :
- **[RECO]** L'inscrire (classe `cloud_wan`) le jour où une entité devient une **entrée décisionnelle**
  — tant que c'est purement informatif, la dette est mineure.
- **[FAIT]** Le **`0` masqué** (§1.3) est un cas de non-substitution : à neutraliser côté consommateur.
  À noter, l'axe « fraîcheur » de l'audit résilience est ici **inopérant en l'état** : le composant
  réécrit `0` au lieu de passer `unavailable`, donc `last_reported` continue de bouger même en panne —
  la panne ne se *voit* que par la valeur `0`, pas par l'âge. Argument de plus pour neutraliser `0`.

### 5.4 D6 — Rétention / recorder (housekeeping)
**[FAIT]** Le commit d'installation n'a **pas** touché `recorder.yaml` : les 12 entités suivent la
politique par défaut du recorder. Indices journaliers/commune à faible cardinalité → coût de rétention
négligeable. **[RECO]** Décider explicitement de l'inclusion (utile pour historiser les épisodes) au
moment d'un éventuel branchement ; sans objet tant que rien ne consomme la donnée.

---

## 6. Caveats de qualité de donnée (transverses)

**[FAIT]** À intégrer à *tout* usage décisionnel :

1. **Indice, pas concentration** — échelle 0-7, non linéaire ; les seuils métier se raisonnent en
   codes ATMO, pas en µg/m³.
2. **Maille commune (Bordeaux)** — pas une mesure au jardin ; représentativité locale limitée (un feu
   très proche peut être sous-représenté par un indice communal, ou l'inverse).
3. **Jour courant + J+1 prévisionnel** — le « jour courant » est déjà en partie un modélisé/prévu, non
   une mesure in situ à la minute.
4. **Rafraîchissement horaire, cloud** — latence et dépendance WAN ; inadapté à une boucle de décision
   rapide (ce qui, incidemment, renforce l'inéligibilité VMC du §4.2-3).
5. **`0` = Indisponible masqué** (§1.3) — le piège le plus important.

---

## 7. Recommandation de séquence (aucune action appliquée — arbitrage propriétaire requis)

**Phase 0 — lecture seule (immédiat, sans contrat) :**
1. **Afficher** l'indice extérieur en **contexte** sur les cartes Aération et VMC (§10.5 VMC déjà prêt).
   Aucun effet décisionnel. Observer la donnée en épisode réel (l'épisode en cours est une occasion).
2. Neutraliser dès ce stade `unknown`/`unavailable`/`0` dans tout template d'affichage.

**Phase 1 — aération décisionnelle (P2, via contrat) :**
3. Ouvrir un **nouveau contrat** (ou une **fusion explicite** dans `aeration_recommandation.md`) actant
   le critère `air_exterieur_degrade`, son **rang** vs CO₂ (§3.2) et sa modulation par niveau ATMO.
4. Implémenter sur le patron `pluie` (booléen + rang + motif + icône + `decision`), avec checker/CI
   aligné comme pour les autres critères d'aération.
5. Vérifier la **non-régression clim** (§5.1).

**Phase 2 — VMC (P2, arbitrage lourd, optionnel) :**
6. **Ne rien automatiser** sans évolution de contrat (§4.3). D'ici là, le besoin « rester en lent
   pendant l'épisode » se satisfait par la **prise de main manuelle** (§16). Si une automatisation est
   voulue, ouvrir un **arbitrage de conception VMC v2.7** traitant frontalement §1.2, §7.4 et la
   collision avec la voie CO₂ de sécurité.

**Phase 3 — annexes (P3) :** notifications pollution en domaine propre (§5.2) ; inscription résilience
(§5.3) ; décision recorder (§5.4).

---

## 8. Statut

- Analyse : **lecture seule** — aucun runtime, contrat, UI, recorder, registre ou checker modifié.
- **D1 (aération)** : accueil naturel, **arbitrage sanitaire pollution↔CO₂ ouvert** — P2.
- **D2 (VMC)** : **non implémentable sous v2.6** (collision §1.2 + §7.4) ; couvert dans l'immédiat par
  l'autorité manuelle (§16) et l'affichage contextuel (§10.5) — P2 si automatisation souhaitée.
- **D3-D6** : effets transitifs, notifications propres, résilience et rétention — P3, sauf `0` masqué
  (P2 dès branchement).
- Suite : **arbitrage propriétaire requis** avant toute Phase 1+.
