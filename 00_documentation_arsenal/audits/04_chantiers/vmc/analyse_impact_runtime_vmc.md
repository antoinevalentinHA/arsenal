# Analyse d'impact runtime, UI et CI — Lot 6 (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Lot** | **L6 — analyse d'impact.** Audit du propriétaire autoritatif des paramètres, structure des helpers, effets sur les entités, dépendances, migration, ordre des lots runtime |
| **Nature** | **Analyse.** **Aucun patch n'est produit à ce stade** (verrou de séquence du §5 du chantier) |
| **Statut** | **Préparé sur branche** |
| **Entrée** | L2b soldé côté calibration ([`arbitrage_parametres_provisoires_vmc.md`](arbitrage_parametres_provisoires_vmc.md), PR #522) : tous les paramètres disposent d'une valeur provisoire arbitrée |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §2.2, §2.2 bis, §2.3, §2.4, §4.4, §4.4 bis, §6, §7.4 bis, §8, §9.1, §9.1 bis, §10.2, §10.4, §11.2, §12.3, §14. **Non modifié par ce lot** |

> **Aucun runtime, contrat, UI, checker ni CI modifié dans ce lot.** Aucune
> entité créée, renommée ni supprimée. Les identifiants, chemins et lignes cités
> sont **relevés dans le dépôt**, jamais supposés.

---

## 1. Surface VMC constatée

Relevé exhaustif dans `C:\dev\arsenal`, branche `main` au commit du présent lot.

| Couche | Fichiers | Lignes |
|---|---|---|
| Paramètres | `03_input_numbers/vmc/duree_haute_vitesse.yaml`, `seuils/humidite.yaml`, `seuils/co2.yaml` | 148 |
| Reflet UI | `05_input_booleans/vmc/haute_vitesse.yaml` | 24 |
| Exécution | `10_scripts/vmc/haute_vitesse.yaml`, `basse_vitesse.yaml` | 154 |
| Automatisations | `11_automations/vmc/gestion_auto.yaml`, `synchro_booleen.yaml`, `watchdog.yaml`, `alerte_nc_decision.yaml` | 312 |
| Décision et diagnostic | `12_template_sensors/vmc/haute_vitesse_requise.yaml`, `conformite_decision.yaml`, `coherence.yaml`, `intention.yaml`, `delta_humidite_absolue_favorable.yaml` | 431 |
| Intégrité des réglages | `12_template_sensors/system/integrite_reglages/vmc.yaml` | 120 |
| UI | `18_lovelace/dashboards/vmc/{principal,diagnostic,reglages}.yaml` + 5 templates `19_button_card_templates/40_dashboards/vmc/` | 268 + cartes |
| Rétention | `recorder.yaml` — **une seule entité VMC** : `input_boolean.vmc_haute_vitesse` (ligne 780) | 1 ligne |
| CI | `scripts/arsenal_contracts/check_vmc_contracts.py`, `.github/workflows/contracts_vmc.yml`, allowlist de `check_aeration_recommandation_contracts.py` | — |

**Entités décisionnelles et d'exécution :** `binary_sensor.vmc_haute_vitesse_requise` · `switch.vmc_l1` / `switch.vmc_l2` · `script.vmc_haute_vitesse` / `script.vmc_basse_vitesse` · automatisations `10190000000001` (gestion), `10190000000004` (synchro), `10190000000005` (alerte NC).

---

## 2. Propriétaire autoritatif des paramètres

### 2.1 État constaté

Cinq `input_number`, **tous sans clé `initial:`** — commentée dans les trois fichiers ([`humidite.yaml:45`](../../../../03_input_numbers/vmc/seuils/humidite.yaml), [`:55`](../../../../03_input_numbers/vmc/seuils/humidite.yaml), [`duree_haute_vitesse.yaml:44`](../../../../03_input_numbers/vmc/duree_haute_vitesse.yaml)) : la valeur est **persistée par HA**, l'utilisateur est le seul auteur d'écriture, et aucune automatisation ne les modifie.

| Helper | Plage | Consommé par une décision ? |
|---|---|---|
| `input_number.vmc_seuil_on` | 50–90 % | **oui** — `haute_vitesse_requise.yaml:49` |
| `input_number.vmc_co2_seuil_on` | *(cf. `seuils/co2.yaml`)* | **oui** — `haute_vitesse_requise.yaml:50` |
| `input_number.vmc_duree_min_haute` | 5–60 min | **oui** — `gestion_auto.yaml:61` |
| `input_number.vmc_seuil_off` | 40–85 % | **NON** |
| `input_number.vmc_co2_seuil_off` | — | **NON** |

### 2.2 Constat n° 1 — deux frontières déclarées, exposées, contrôlées, et consommées par rien

`vmc_seuil_off` et `vmc_co2_seuil_off` n'apparaissent que dans quatre fichiers : leur propre déclaration, le capteur d'intégrité, le dashboard de réglages et une carte de diagnostic. **Aucun n'est une décision.** Le fichier décisionnel l'écrit lui-même : « Les seuils OFF ne sont pas lus ici » ([`haute_vitesse_requise.yaml:26`](../../../../12_template_sensors/vmc/haute_vitesse_requise.yaml)).

**C'est l'écart n° 2 du chantier, ici quantifié**, et c'est une **non-conformité au §10.4** : deux réglages sont affichés et modifiables sans effet sur le comportement.

**Aggravation constatée en UI.** La carte de réglages promet explicitement le comportement absent : « passage en haute vitesse au-dessus du seuil de déclenchement, **retour sous le seuil d'arrêt** » ([`reglages.yaml:75-78`](../../../../18_lovelace/dashboards/vmc/reglages.yaml)). La carte de diagnostic `vmc_capteur` colore en outre la valeur **par rapport à `seuil_off`** lorsque la VMC est en haute vitesse : elle **restitue visuellement une règle que le système n'applique pas**. C'est le critère de clôture 7 du chantier.

### 2.3 Constat n° 2 — les valeurs de repli masquent l'indisponibilité

Le capteur décisionnel emploie `| float(70)` et `| float(1000)` ([`:49-50`](../../../../12_template_sensors/vmc/haute_vitesse_requise.yaml)), l'automatisation `| int(15)` ([`gestion_auto.yaml:61`](../../../../11_automations/vmc/gestion_auto.yaml)).

> Ce style est **incompatible avec la doctrine de garde arrêtée en passe 5** :
> une frontière dont le paramètre est indisponible doit devenir **non
> calculable** et être **exposée comme telle**, jamais silencieusement remplacée.

**Le capteur d'intégrité fait déjà l'inverse et donne le modèle à suivre** : il traite toute source indisponible comme rendant les invariants violés, « pas d'optimisme silencieux » ([`integrite_reglages/vmc.yaml:15-16`](../../../../12_template_sensors/system/integrite_reglages/vmc.yaml)), et emploie `| float(none)` plutôt qu'un défaut numérique. **La cible existe déjà dans le dépôt** ; il ne s'agit pas d'inventer une pratique.

### 2.4 Dénombrement des paramètres de la machine cible

| Portée | Paramètres | Nombre |
|---|---|---|
| Par pièce (parents, enfants) | `S`, `W`, `D`, `A`, `B`, `H`, borne basse, borne haute | 8 × 2 = **16** |
| Voie CO₂ (séjour) | `co2_seuil_on`, `co2_seuil_off` | **2** |
| Exécutif | `duree_min_haute` | **1** |
| | **Total** | **19** |

**Aujourd'hui : 5.** L'écart n'est pas un détail d'implémentation : il détermine la structure de stockage.

### 2.5 Ce que le contrat impose, et ce qu'il laisse ouvert

**Imposé.** Le §7.4 bis condition 1 exige que les bornes de la frontière modulée soient « **configurables et exposables** » — les deux bornes par pièce **doivent** donc être des helpers, non des constantes de fichier. Le §10.4 impose que toute frontière **exposée** soit celle qui est **consommée**.

**Ouvert.** Rien n'impose que `A`, `B` et `H` soient réglables par l'utilisateur. Trois structures sont possibles :

| | Tout en `input_number` | `A`, `B`, `H` en constantes de fichier | Structure mixte |
|---|---|---|---|
| Nombre de helpers | **19** | 5 + bornes = **9** | à arbitrer |
| Modifiable sans redéploiement | oui | non | partiel |
| Risque de réglage incohérent | **élevé** — 19 curseurs, invariants croisés | faible | moyen |
| Traçabilité de la décision de calibration | **faible** — la valeur arbitrée est écrasable sans trace | **forte** — la valeur vit dans le dépôt versionné | moyenne |
| Charge d'exposition §10.2 | identique | identique | identique |

> **Observation, non décision.** Les valeurs arrêtées en passe 5 sont des
> **paramètres de calibration**, pas des préférences d'usage. Les loger dans des
> curseurs les rend écrasables sans qu'aucune trace ne subsiste de l'arbitrage —
> ce que la doctrine Arsenal du paramètre autoritatif cherche précisément à
> éviter. **L'arbitrage appartient au propriétaire** et relève de L7.1.

**Point dur, quelle que soit la structure retenue :** un `input_number` sans `initial:` est `unknown` **à sa première apparition**. Sans repli — et la passe 5 les interdit — la machine serait **non calculable au premier démarrage suivant le déploiement**. C'est un **point de migration obligatoire** (§13).

---

## 3. La grandeur modulante n'est pas une mesure brute

**Constat structurant de ce lot.**

`sensor.temperature_jardin` **n'est pas un capteur** : c'est une **façade de publication** ([`12_template_sensors/meteo/mesures/temperature/jardin/facade.yaml`](../../../../12_template_sensors/meteo/mesures/temperature/jardin/facade.yaml)). Elle publie l'état persistant `input_number.temperature_jardin_etat_publie`, avec :

- une **disponibilité conditionnée** : `mem_ok AND (cible_disponible OR age ≤ 1800 s)` (`:56-68`) ;
- un **mode de publication** exposé — `fusion`, `memoire` ou `abstention` (`:88-94`) ;
- un **capteur de statut** associé, `sensor.temperature_jardin_statut`, exposant `nominal`, `memoire`, `degrade`, `suspect_chaud`, `incoherence_retenue` ou `inconnu`, avec une **cause énumérée** (`:112-178`).

### 3.1 Ce que cela apporte

> **La garde arrêtée en passe 5 est implémentable sans rien inventer.**

Le §7.4 bis condition 4 exige de détecter que la grandeur modulante est inexploitable. **La façade le publie déjà** : `unavailable` est une condition **contractualisée** de l'axe météo, et `temperature_jardin_statut` en fournit la **raison**, ce que l'exigence 24 du §10.2 demande explicitement. Aucun capteur, aucun helper, aucun mécanisme de détection n'est à créer pour la garde elle-même.

### 3.2 Ce que cela ouvre

Le §6.4 et le §7.4 bis parlent d'une « **mesure physique instantanée** extérieure au logement ». La valeur publiée peut provenir d'une **mémoire de 30 minutes** (mode `memoire`). Deux lectures :

| Lecture | Conséquence |
|---|---|
| **La mémoire est celle de l'axe météo, pas du besoin VMC** | Le §2.2 vise la mémoire *du besoin* — épisode, pic, historique de la mesure de la pièce. La façade ne mémorise rien du besoin ni de la pièce. **Aucun obstacle** |
| **« Instantanée » qualifie la valeur consommée** | La VMC consommerait une valeur d'âge borné mais non nul. **La qualification serait à préciser** |

> **La première lecture paraît la bonne**, et la seconde ne change pas le
> mécanisme : dans les deux cas la frontière reste une **fonction de l'état
> courant publié**, sans mémoire propre au besoin. **Ce lot ne tranche pas** :
> il signale que la qualification mérite une ligne explicite, et qu'aucun
> co-changement contractuel ne paraît nécessaire pour l'obtenir.

**Point de cohérence probatoire, à porter au crédit du dispositif :** la calibration de la passe 5 a été conduite sur l'historique Recorder de `sensor.temperature_jardin` — c'est-à-dire **sur la façade elle-même**, avec ses modes `memoire` et ses indisponibilités. **Le runtime consommerait exactement l'objet qui a été calibré.** Les 3,60 % d'indisponibilité mesurés sont ceux de la façade, pas d'un capteur brut sous-jacent.

---

## 4. Observation glissante — moyen d'implémentation disponible

Le critère d'entrée (§2.2 bis) exige, par pièce, le **minimum sur une fenêtre glissante** de 20 ou 30 minutes, plus la **profondeur réellement disponible** (§10.2, exigences 11 à 19).

**La plateforme `statistics` est un motif établi du dépôt** — `13_sensor_platforms/statistics/`, avec `max_age` et `sampling_size` documentés et justifiés fichier par fichier ([`meteo/humidite_relative.yaml`](../../../../13_sensor_platforms/statistics/meteo/humidite_relative.yaml)). Une caractéristique de minimum sur `max_age: 00:20:00` fournirait la valeur de référence sans aucune mémoire écrite par le domaine VMC.

**Deux points à vérifier en L7, non affirmés ici :**

1. les attributs de couverture temporelle exposés par la plateforme `statistics` — nécessaires aux exigences 12, 17 et 19 — doivent être **constatés sur l'instance** avant d'être promis en UI ;
2. **tension à qualifier avec le §9.1 bis.** Le contrat pose que l'observation glissante « **n'est pas restaurée, elle repart vide** ». Or `recorder.yaml` documente la contrainte inverse pour cette plateforme : « **sans historique de la source, la fenêtre glissante est tronquée après purge/redémarrage** » (`recorder.yaml:11-14`), ce qui implique qu'elle **se recharge** depuis l'historique. Une fenêtre pleine dès le démarrage **ne crée aucun faux besoin** et ne contredit aucun invariant du §9.1 bis — mais elle **dépasse** ce que le contrat décrit. **À qualifier, sans urgence : l'écart va dans le sens conservateur.**

**Dépendance Recorder favorable.** Les quatre sources nécessaires sont **déjà** dans l'allowlist : `humidite_relative_sdb_parents` (ligne 210), `sdb_enfants` (211), `sejour` (205), `co2_sejour` (241), `temperature_jardin` (21). **Aucun élargissement de rétention n'est requis pour la décision** — la contrainte du §6 du chantier est respectée sans arbitrage.

---

## 5. État par pièce, restauration et agrégation

| Exigence | Contrat | Moyen disponible |
|---|---|---|
| État de besoin **par pièce** | §2.3 | un porteur d'état booléen par pièce |
| **Restauré** au redémarrage | §9.1 cas 3 | restauration native des `input_boolean` |
| Ne restaure **ni instant, ni durée, ni valeur** | §9.1 invariant | un booléen ne peut structurellement rien porter d'autre |
| Confronté **immédiatement** aux mesures | §9.1 cas 1 et 2 | déclencheur `homeassistant.start`, motif déjà employé (`gestion_auto.yaml:45`, `synchro_booleen.yaml:39`) |
| Agrégation **sans état** | §2.4 | `binary_sensor.vmc_haute_vitesse_requise` devient un **OU pur** des besoins de pièce |

**Conséquence sur le capteur décisionnel.** Son `entity_id` doit être **conservé** : il est référencé par `gestion_auto.yaml`, `conformite_decision.yaml`, `intention.yaml`, le dashboard de diagnostic et le **test 1 du checker de contrat**. Sa **nature** change — de comparateur à agrégation — mais **aucun renommage n'est nécessaire ni souhaitable**.

**Un besoin doit devenir un état écrit, non un état calculé.** C'est la conséquence architecturale la plus lourde de L7 : un capteur `template` ne peut pas porter d'hystérésis persistante. La machine par pièce relève donc d'une **automatisation** écrivant un **porteur d'état**, les capteurs `template` restant en **exposition pure**. Cette répartition est **exactement** celle que le domaine pratique déjà entre `gestion_auto` et `haute_vitesse_requise` ; elle est **étendue**, non inventée.

---

## 6. Impact UI

| Élément | Impact |
|---|---|
| `reglages.yaml` — 4 tuiles de seuils | **refonte** : de 5 à 19 paramètres, ou moins selon l'arbitrage du §2.5 |
| `reglages.yaml:75-78` — texte promettant le retour sous seuil d'arrêt | **à réécrire** : la libération devient une frontière **modulée** ; le texte actuel deviendrait faux d'une seconde manière |
| `vmc_capteur` — coloration par `seuil_off` | **à réécrire** : doit colorer d'après la **frontière courante réellement consommée** (§10.4) |
| `diagnostic.yaml` | **à étendre** : exigences 20 à 24 du §10.2 — grandeur modulante, valeur, frontière courante, bornes, statut calculable et sa raison |
| `principal.yaml` — reflet `input_boolean.vmc_haute_vitesse` | **inchangé** — reflet d'exécution, hors décision |
| `binary_sensor.delta_ha_favorable_etage` en carte « Extraction » | **à requalifier** (§10.5) : contexte non décisionnel, à présenter comme tel |
| `sensor.vmc_intention` | **à réaligner** — voir ci-dessous |

**Non-conformité déjà présente dans `intention.yaml`.** Le fichier annonce lui-même que sa cause est calculée sur `delta_humidite_absolue > 0` « pour une meilleure lisibilité humaine » et « **peut diverger du capteur métier** » (`:13-19`). Le **§11.2** l'interdit sans ambiguïté : « Une approximation retenue pour la lisibilité, susceptible de diverger de la décision réelle, est **interdite**. »

> **C'est un sixième écart contractuel formel**, distinct des cinq énumérés au §2
> du chantier, et **antérieur** à la mise en conformité. Il est **déjà** non
> conforme au contrat v2.2 en vigueur.

---

## 7. Impact CI et checkers

| Contrôle | Impact |
|---|---|
| `check_vmc_contracts.py` **test 1** — présence du capteur décisionnel | **inchangé**, l'`entity_id` étant conservé |
| **test 2** — scripts VMC sans logique métier (`humidite`, `co2`, `aeration_preferable`, `vmc_seuil`) | **inchangé** ; contraint les futurs fichiers sous `10_scripts/vmc/` à rester purs — ce qui est la cible |
| **test 3** — automatisations VMC avec `mode:` | **contrainte à respecter** par toute nouvelle automatisation de besoin |
| **couverture** | Les trois tests sont **structurels**. Aucun ne vérifie l'hystérésis, l'état par pièce, la restauration ni les expositions 20 à 24. **Un renforcement est opportun**, à instruire en L7 |
| `check_aeration_recommandation_contracts.py` **T10** — allowlist | **`haute_vitesse_requise.yaml` doit sortir de la liste** (`:56`) après L7.2. Attention : l'y **laisser ne fait pas échouer le contrôle** — le checker n'interdit que les consommateurs **non listés**. Le critère de clôture 8 ne se vérifiera donc **pas tout seul** |
| `intention.yaml` et `delta_humidite_absolue_favorable.yaml` dans la même allowlist (`:55`, `:57`) | **restent légitimes** — lecture non décisionnelle (§4.3, §10.5) — mais `intention.yaml` doit être réaligné au titre du §11.2 (§6) |
| `binary_sensor.parametres_invalides_vmc` — invariants | **obsolètes** : l'invariant `vmc_seuil_on > vmc_seuil_off` perd son objet. Invariants de remplacement à définir : `borne_basse < borne_haute`, **`S > borne_haute`** — faute de quoi la bande morte de la voie de niveau est nulle ou négative, ce que la passe 5 a précisément mis en évidence —, `H > 0`, `co2_seuil_on > co2_seuil_off` |
| `.github/workflows/contracts_vmc.yml` | **inchangé** — invoque le checker sans énumérer de fichiers |
| Gates documentaires | **inchangées** — aucun impact runtime sur `docs_lint` et les cinq contrôles `DOC-CI` |

---

## 8. Recorder et preuve L8

Une **seule** entité VMC est historisée : `input_boolean.vmc_haute_vitesse` (`recorder.yaml:780`). C'est la trace déclarative sur laquelle L5 a travaillé.

**La comparaison avant / après (L8) exigera d'historiser au minimum :** l'état de besoin **par pièce**, et la **valeur courante de la frontière modulée** — sans quoi l'effet du changement resterait aussi peu vérifiable qu'aujourd'hui, ce qui est le **risque R1** du chantier.

**Compatible avec la contrainte du §6** — « aucune augmentation permanente et large de la rétention » : trois à cinq entités ciblées, non un élargissement de périmètre. **Aucune décision n'est prise ici** ; le besoin est établi et chiffré.

---

## 9. Dépendances et ordre des lots runtime

Le découpage L7.1 à L7.6 arrêté en passe 1 **reste valide**. Ce lot en précise les **préalables** et une **dépendance non vue jusqu'ici**.

| Lot | Objet | Préalable établi par ce lot |
|---|---|---|
| **L7.1** | besoins locaux et paramètres par pièce | **arbitrage préalable de la structure de stockage** (§2.5) et **plan de migration** (§10). Sans eux, L7.1 fixe la structure par défaut, sans décision |
| **L7.2** | retrait du veto d'aération | modification de `haute_vitesse_requise.yaml:60` + **retrait de l'entrée d'allowlist** (§7), qui ne se signalera pas seule |
| **L7.3** | critère d'entrée dynamique et observabilité | capteurs `statistics` par pièce ; **sources déjà historisées** (§4) ; vérification des attributs de couverture sur l'instance |
| **L7.4** | machine hystérétique et libération | **était bloqué** par l'absence de mécanisme de libération. **Le blocage est levé** : le mécanisme est arbitré et calibré. Dépend de la disponibilité de `sensor.temperature_jardin_statut` pour la garde |
| **L7.5** | restauration et indisponibilité | dépend du porteur d'état choisi en L7.1 |
| **L7.6** | composition et commande | agrégation sans état ; `gestion_auto.yaml` **peu impacté** — sa logique exécutive reste valide |

**Deux ajouts proposés, à arbitrer :**

- **L7.0 — propriétaire des paramètres et migration**, en préalable de L7.1. Ce n'est pas un lot de confort : sans lui, la première application après déploiement porte sur des helpers `unknown` ;
- **L7.7 — UI, intégrité et CI**, en aval : refonte du dashboard de réglages, réécriture du texte trompeur, remplacement des invariants du capteur d'intégrité, réalignement de `sensor.vmc_intention` au §11.2, retrait de l'allowlist. **Ces éléments ne sont couverts par aucun lot existant** et portent trois des critères de clôture du chantier (7, 8 et la non-conformité §11.2 relevée au §6).

---

## 10. Migration

| # | Point | Nature |
|---|---|---|
| 1 | **Helpers nouveaux à `unknown`** faute de clé `initial:` | **Bloquant.** Aucun repli silencieux n'étant admis, la machine serait non calculable au premier démarrage. Une amorce explicite est requise, ou une exception motivée à la doctrine `initial:` |
| 2 | **`vmc_seuil_off` et `vmc_co2_seuil_off`** | À **supprimer ou requalifier** : leur suppression retire des entités que l'utilisateur voit et a réglées. Non destructif pour le comportement — **elles ne sont consommées par rien** (§2.2) |
| 3 | **Reflet `input_boolean.vmc_haute_vitesse`** | **Conservé.** Écrit depuis les relais (`synchro_booleen.yaml`), c'est la trace historisée sur laquelle repose la référence L5 : la rompre **détruirait la comparabilité avant / après** |
| 4 | **`entity_id` du capteur décisionnel** | **Conservé.** Aucun renommage, donc **aucune migration d'historique** |
| 5 | **Ordre de déploiement** | L'état intermédiaire à l'issue de L7.3 est **temporaire et non conforme** — déjà consigné en passe 1, inchangé |
| 6 | **Fenêtre glissante au déploiement** | Les capteurs `statistics` se remplissent depuis l'historique existant (§4) : **aucune période aveugle attendue**, à confirmer |

---

## 11. Risques propres à l'implémentation

| # | Risque | Portée |
|---|---|---|
| **I1** | **19 paramètres exposés sans garde-fous croisés** produiraient des combinaisons incohérentes silencieuses — `S ≤ borne_haute` annule la bande morte de la voie de niveau | L7.1, capteur d'intégrité |
| **I2** | **Le style de repli actuel** (`\| float(70)`, `\| int(15)`) est contraire à la doctrine de garde. Reproduit par mimétisme dans les nouveaux fichiers, il **réintroduirait le fallback silencieux** que la passe 5 interdit | Tous les lots L7 |
| **I3** | **Le critère de clôture 8 ne se vérifie pas seul** : laisser l'entrée d'allowlist ne fait échouer aucun contrôle | L7.2, L7.7 |
| **I4** | **`sensor.vmc_intention` est déjà non conforme au §11.2** et n'est rattaché à aucun lot | L7.7 proposé |
| **I5** | **Sans ajout Recorder ciblé, L8 sera aussi peu concluant que L5** — c'est le risque R1 du chantier, ici rendu actionnable | L7, L8 |
| **I6** | **La qualification de la grandeur modulante** (§3.2) reste à écrire noir sur blanc, faute de quoi elle ressurgira en revue | L7.4 |

---

## 12. Ce que ce lot établit

1. **Deux frontières sont exposées, réglables et consommées par rien** — écart n° 2 quantifié, non-conformité §10.4, avec une UI qui en **promet le comportement** ;
2. **la grandeur modulante n'est pas un capteur brut** mais une façade à mémoire bornée et statut publié : **la garde du §7.4 bis est implémentable sans rien créer**, et le runtime consommerait **exactement l'objet calibré** ;
3. **l'observation glissante dispose d'un motif établi** dans le dépôt, et **toutes les sources sont déjà historisées** : aucun élargissement Recorder n'est requis pour la décision ;
4. **un besoin doit devenir un état écrit**, non calculé — conséquence architecturale majeure de L7 ;
5. **`sensor.vmc_intention` est un sixième écart contractuel formel**, antérieur au chantier et rattaché à aucun lot ;
6. **le critère de clôture 8 ne se vérifiera pas tout seul** ;
7. **la structure de stockage des 19 paramètres est un arbitrage propriétaire**, préalable à L7.1, avec un **point de migration bloquant** sur l'absence de clé `initial:`.

---

## 13. Ce que ce lot ne décide pas

- il **ne produit aucun patch** et ne modifie aucun fichier runtime, UI ou CI ;
- il **ne choisit pas** la structure de stockage des paramètres — helpers, constantes ou mixte ;
- il **ne recalibre rien** : les valeurs de la passe 5 sont inchangées ;
- il **ne modifie aucun contrat** et **ne conclut à aucun co-changement nécessaire** ;
- il **ne solde pas L5**, et **n'autorise pas L7** : la séquence probatoire prime ;
- il **n'affirme pas** que les attributs de couverture de la plateforme `statistics` sont disponibles : il désigne le point comme **à constater sur l'instance**.
