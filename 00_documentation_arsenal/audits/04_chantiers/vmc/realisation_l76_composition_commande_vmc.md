# Réalisation L7.6 — composition et commande (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.3 |
| **Lot** | **L7.6 — composition et commande** |
| **Statut** | **Préparé sur branche** |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.3** — §5.1, §5.2, §5.3, §8.2, §8.4, §10.4, §12.3. **Non modifié par ce lot** |

> **Périmètre strict, quatre objets** : vérifier la chaîne décision → commande →
> relais ; traiter `vmc_co2_seuil_off` ; vérifier que `gestion_auto.yaml` ne
> reconstruit aucune décision ; instruire l'ajout Recorder minimal pour L8.
>
> **L'arbitrage sur l'exposabilité du cas 4 n'est pas rouvert.**

---

## 1. La chaîne décision → commande → relais

**Relevé exhaustif des entités lues par chaque maillon :**

| Maillon | Lit | Écrit |
|---|---|---|
| `gestion_auto.yaml` | `binary_sensor.vmc_haute_vitesse_requise`, `input_number.vmc_duree_min_haute`, `input_boolean.systeme_stable` | appelle les deux scripts |
| `script.vmc_haute_vitesse` / `basse_vitesse` | `switch.vmc_l1`, `switch.vmc_l2`, `binary_sensor.vmc_coherence_physique` | les deux relais |
| `synchro_booleen.yaml` | `switch.vmc_l1`, `switch.vmc_l2` | `input_boolean.vmc_haute_vitesse` |

**La chaîne est cohérente et à sens unique :**

- la commande **ne lit aucune mesure**, aucune frontière, aucun paramètre de
  décision — elle lit **le seul verdict agrégé** ;
- les scripts **ne lisent aucune grandeur métier** : relais et cohérence
  électrique uniquement ;
- le reflet est écrit **depuis les relais**, jamais l'inverse. Le **§8.4** est
  respecté : le sens est unique, et **aucune décision ne lit l'état physique de
  l'actionneur** — ce que le §12.3 range parmi les non-conformités.

**`input_boolean.vmc_haute_vitesse`** n'est écrit que par `synchro_booleen` ;
partout ailleurs — UI, `recorder.yaml` — il est **lu seulement**.

---

## 2. `gestion_auto.yaml` ne reconstruit aucune décision

**Vérifié, et désormais gardé en CI.**

Un **test 9** interdit à la couche de commande de lire **tout ingrédient de la
décision** : mesure de pièce, CO₂, référence glissante, frontière modulée,
seuils, bornes, états de besoin, besoins eux-mêmes, verdict d'aération. Il
exige en outre qu'elle lise **bien** le verdict agrégé — une commande rattachée
à aucune décision serait tout aussi fautive — et qu'elle **ne lise pas le
reflet** (§8.4).

**Preuve négative établie** : faire lire `sensor.co2_sejour` à la commande fait
échouer le checker.

> **Pourquoi une garde plutôt qu'un simple constat.** Une vérification qui n'est
> pas mécanisée se périme au premier lot suivant. C'est la leçon que L6 avait
> tirée du critère de clôture 8, « qui ne se vérifie pas seul ».

### 2.1 Un point résiduel, signalé et non traité

`gestion_auto.yaml` emploie `| int(15)` sur la durée minimale : un **repli
numérique silencieux**, contraire à la doctrine arrêtée en passe 5.

Il est **antérieur** à ce lot, ne concerne **pas la décision** mais un paramètre
**exécutif**, et le corriger sortirait du périmètre strict. **Il est donc
signalé et laissé en l'état** — à traiter en **L7.7**, avec les autres points
d'intégrité.

---

## 3. `vmc_co2_seuil_off` — une vraie libération CO₂

### 3.1 Le contrat tranche, et il est explicite

| Clause | Contenu |
|---|---|
| **§5.1** | tout besoin a une frontière d'entrée, une condition de maintien, **une frontière de libération** et **un état booléen** **propres** |
| **§5.3** | la voie CO₂ = **un besoin unique (séjour)**, avec **un état booléen** |

**La voie CO₂ était pourtant restée un comparateur** logé dans l'agrégation :
une seule frontière, aucun état, aucune libération. Et
`input_number.vmc_co2_seuil_off` était **déclaré, exposé en UI, contrôlé en
intégrité — et consommé par rien**, ce que le **§10.4** qualifie de
non-conformité.

> **L'alternative « supprimer le helper » aurait été plus simple et
> contractuellement fausse** : elle aurait laissé la voie CO₂ sans frontière de
> libération, en contradiction directe avec le §5.1.

### 3.2 Ce qui est créé

| Objet | Rôle |
|---|---|
| `input_boolean.vmc_etat_besoin_co2_sejour` | porte l'état booléen du besoin CO₂ |
| `binary_sensor.vmc_besoin_co2_sejour` | expose l'état et l'explicabilité |
| Automatisation `10190000000010` | machine hystérétique : entrée ≥ `co2_seuil_on`, libération ≤ `co2_seuil_off`, maintien entre les deux |

**Même forme que les besoins de pièce** : réévaluation au démarrage (§9.1 cas 1
à 3), maintien sur mesure ou frontière inexploitable (§4.4), attributs
d'explicabilité, `mesure_exploitable`, `maintenu_faute_de_mesure`,
`maintenu_faute_de_frontiere`.

**Autonomie des voies (§5.2)** : cette machine **ne lit aucun état de besoin
humidité**, et aucun besoin humidité ne lit le sien.

**Le repli `| float(1000)` disparaît** : une frontière inexploitable rend le
besoin indisponible avec une cause énumérée.

L'alerte de maintien prolongé de L7.5 couvre désormais la voie CO₂ : un besoin
CO₂ maintenu sur panne durable est un cas de **risque R4** au même titre.

### 3.3 Conséquence sur l'écart n° 3

**L'écart n° 3 — « aucun besoin hystérétique, comparateur à frontière
unique » — n'était pas entièrement résorbé par L7.4**, contrairement à ce qui
avait été inscrit : la voie CO₂ demeurait un comparateur.

> **Il l'est maintenant.** La correction est consignée plutôt que passée sous
> silence.

### 3.4 L'agrégation devient une composition pure

`binary_sensor.vmc_haute_vitesse_requise` **ne lit plus aucune mesure ni aucune
frontière** — vérifié : plus une seule référence à `sensor.` ou `input_number.`
dans le fichier. Il compose **trois besoins homogènes**, et rien d'autre. Le
**§2.4** est servi sans réserve.

L'invariant d'intégrité `vmc_co2_seuil_on > vmc_co2_seuil_off`, jusqu'ici
contrôlé pour une valeur inutilisée, **prend enfin son sens**.

---

## 4. Ajout Recorder minimal pour L8

Le solde de L5 avait établi, en balayant les 38 bases, qu'**une seule entité de
la chaîne de décision sur onze** était historisée — d'où deux constats : la
règle en vigueur n'était **pas rejouable**, et la corroboration décision →
commande → relais était **impossible**. C'est le **risque R1**, avéré puis clos
par constat.

**Six entités le lèvent pour l'avenir :**

| Entité | Pourquoi elle est nécessaire |
|---|---|
| `binary_sensor.vmc_haute_vitesse_requise` | sans elle, L8 ne compare que des **commutations**, jamais des **décisions** |
| `input_boolean.vmc_etat_besoin_sdb_parents` / `_sdb_enfants` / `_co2_sejour` | ils portent la **couverture par pièce et par voie** — la grandeur même de la comparaison avant / après **fixée au solde de L5** |
| `sensor.vmc_frontiere_liberation_sdb_parents` / `_enfants` | sans leur valeur courante, une libération ne peut pas être **rattachée à son point de comparaison**, et le **§15.1** ne peut pas être vérifié |

**Volontairement exclus** : les frontières fixes et les paramètres — versionnés
ou réglables, ils se lisent dans le dépôt ; les capteurs d'observation
glissante — dérivables des sources déjà historisées ; les capteurs de
diagnostic — ils n'entrent dans aucune comparaison.

> **Aucune augmentation de `purge_keep_days` n'est demandée.** La contrainte du
> §6 du chantier — « aucune augmentation permanente et large de la rétention »
> — est respectée : six entités ciblées, non un élargissement de périmètre.

Chaque bloc porte une **bannière Population B** conforme à la doctrine
`recorder.yaml` : rôle, utilité, logbook, cardinalité, fréquence. Le contrat
recorder est conforme.

---

## 5. Contrôles exécutés

**86 checkers `arsenal_contracts` exécutés**, tous passent — dont les **neuf
tests** du contrat VMC et le contrat recorder. Les fichiers runtime sont
**valides au parseur YAML**. Les **gates documentaires** passent.

**Un ajustement de CI était requis** : le test 6 exigeait les exigences 11 à 19
du §10.2 de **tout** besoin. Or le §5.2 pose que « les voies peuvent avoir des
critères internes différents », et le §10.2 conditionne ces exigences au cas
« **lorsqu'un critère d'évolution est retenu** ». La voie CO₂ n'en a pas : les
lui imposer serait exiger l'exposition d'un critère **inexistant**. Le test est
donc **borné à la voie humidité**.

> **Deux échecs demeurent, ANTÉRIEURS** : `lovelace_no_inline_templating` et
> `vacances`. Ni causés, ni aggravés. Un avertissement `T14` sur
> `input_boolean.vmc_haute_vitesse` est lui aussi **antérieur** — vérifié en
> rejouant le checker sans les modifications.

---

## 6. Ce que ce lot ne fait pas

- il **ne modifie ni `/config` ni le contrat** ;
- il **ne rouvre pas** l'arbitrage sur l'exposabilité du §9.1 cas 4 ;
- il **ne corrige pas** le repli `| int(15)` de la couche de commande —
  signalé, renvoyé à L7.7 ;
- il **n'expose aucun paramètre en UI** ;
- il **ne recalibre rien** : les seuils CO₂ sont ceux déjà en place ;
- il **ne clôt pas C35**.

---

## 7. État des écarts contractuels

| # | Écart | État |
|---|---|---|
| 1 | verdict d'aération décisionnel | ✅ résorbé (L7.2) |
| 2 | frontières de libération non consommées | ✅ résorbé — **complété ici** par la libération CO₂ |
| 3 | aucun besoin hystérétique | ✅ résorbé — **complété ici** pour la voie CO₂ |
| 4 | aucun état humidité par pièce | ✅ résorbé (L7.4) |
| 5 | restauration et indisponibilité | ⚠️ **partiel** — exposabilité du §9.1 cas 4 non servie, arbitrage en attente |
| 6 | intention divergente (§11.2) | ✅ résorbé (L7.1) |

**Prochain jalon : L7.7 — UI, intégrité et CI**, obligatoire et final. Il aura à
traiter, outre son périmètre propre : le repli `| int(15)` (§2.1), le sort de
`vmc/delta_humidite_absolue_favorable.yaml` au regard du critère de clôture 8,
et l'exposition en UI des paramètres désormais consommés.
