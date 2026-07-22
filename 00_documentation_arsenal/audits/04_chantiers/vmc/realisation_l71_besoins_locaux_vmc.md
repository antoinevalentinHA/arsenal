# Réalisation L7.1 — besoins locaux et paramètres par pièce (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Lot** | **L7.1 — besoins locaux et paramètres par pièce.** Premier lot qui **modifie le comportement** du système |
| **Statut** | **Préparé sur branche** |
| **Préalable** | [`realisation_l70_parametres_vmc.md`](realisation_l70_parametres_vmc.md) — les paramètres par pièce existent et sont initialisables |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §2.3, §2.4, §4.4, §10.2, §10.3, §14.1. **Non modifié par ce lot** |

> **Ce lot change ce que fait la VMC.** Les six lots précédents ne touchaient
> pas au comportement ; celui-ci le modifie sur deux points, énoncés au §3.

---

## 1. La voie humidité devient locale

**Deux besoins par pièce sont créés**, chacun ne lisant que la mesure de sa
propre pièce (§2.3) :

| Entité | Pièce | Paramètre consommé |
|---|---|---|
| `binary_sensor.vmc_besoin_humidite_sdb_parents` | salle de bain parents | `input_number.vmc_seuil_on_sdb_parents` |
| `binary_sensor.vmc_besoin_humidite_sdb_enfants` | salle de douche enfants | `input_number.vmc_seuil_on_sdb_enfants` |

Fichiers :
[`humidite_sdb_parents.yaml`](../../../../12_template_sensors/vmc/besoins/humidite_sdb_parents.yaml)
· [`humidite_sdb_enfants.yaml`](../../../../12_template_sensors/vmc/besoins/humidite_sdb_enfants.yaml)

**`binary_sensor.vmc_haute_vitesse_requise` cesse d'être un comparateur et
devient une agrégation** ([`haute_vitesse_requise.yaml`](../../../../12_template_sensors/vmc/haute_vitesse_requise.yaml)) :
il ne lit plus aucune mesure de pièce, n'applique plus aucune frontière propre
et se contente de composer des besoins formés ailleurs — ce que le **§2.4**
exige d'un niveau d'agrégation. Son `entity_id` est **conservé** : sa nature
change, pas son nom, et aucune migration d'historique n'est nécessaire.

---

## 2. Explicabilité — ce qui est exposé dès maintenant

| §10.2 | Élément | Où |
|---|---|---|
| 1 | état du besoin | l'état de chaque `binary_sensor` de besoin |
| 2 | condition justifiant l'entrée | attribut `condition_entree`, **formulé comme une condition d'état** et jamais comme un récit (§10.3) |
| 5 | valeurs mesurées | attribut `mesure_locale` |
| 6 | frontières réellement utilisées | attribut `frontiere_entree` — **celle qui est consommée**, §10.4 |
| 7 | pièce à l'origine du besoin | attribut `piece`, et attributs `besoin_sdb_*` de l'agrégation |
| 8 | abstention distincte de l'état métier | attributs `calculable`, `cause_indisponibilite`, et `besoins_non_calculables` sur l'agrégation |
| 9 | composition globale | attribut `composition` de l'agrégation |

**Aucun repli silencieux n'est introduit.** Mesure ou frontière inexploitable
rend le besoin **indisponible**, avec une cause énumérée — jamais une valeur
fabriquée. Le style `| float(0)` de l'ancien comparateur, qui faisait lire zéro
à un capteur en panne, **disparaît de la voie humidité**.

---

## 3. Ce que le comportement gagne et perd

### 3.1 Le séjour quitte la voie humidité

L'ancien comparateur déclenchait sur `max(parents, enfants, séjour) ≥ seuil`.
**Le séjour n'y contribue plus.**

**Motif** — arbitrage de la passe 1, appuyé sur L5 : le corpus ne justifie pas
de conférer au séjour un besoin humidité **local autonome**, ses montées suivant
temporellement celles des salles de bain. **Son rattachement définitif à un
objectif du contrat n'est pas prononcé**, et ne l'est pas davantage ici.

**Effet attendu, à ne pas minorer** : une humidité élevée du seul séjour ne
déclenchera plus la haute vitesse par la voie humidité. La voie CO₂ du séjour
est inchangée.

### 3.2 Les frontières deviennent celles de la calibration

Chaque pièce compare désormais à **son** paramètre, amorcé à 74 % par L7.0. La
valeur du helper global historique `vmc_seuil_on` n'est plus consommée par la
voie humidité.

> **Cet écart n'est pas chiffrable ici.** L5 a établi que
> `input_number.vmc_seuil_on` **n'est pas historisé** : sa valeur en vigueur ne
> peut pas être connue depuis le dépôt. Si elle diffère de 74 %, le
> déclenchement change d'autant, et la notification émise par L7.0 en donne la
> valeur au moment de la bascule.

---

## 4. Ce qui n'est délibérément pas fait

| Élément | Report | Motif |
|---|---|---|
| **Retrait du verrou d'aération** | **L7.2** | Il est **déplacé, non conservé par choix** : il vivait dans l'agrégation, il vit désormais dans les deux besoins locaux, où L7.2 le supprimera. Le déplacer d'abord permet de le retirer **là où il doit l'être**, pièce par pièce |
| **Voie d'évolution** (`W`, `D`) | **L7.3** | Les helpers existent, ils ne sont pas encore consommés |
| **Hystérésis et libération modulée** (`A`, `B`, `H`, bornes) | **L7.4** | Voir §5 |
| **Maintien sur mesure inexploitable** (§4.4) | **L7.5** | Un besoin indisponible n'est pas compté comme actif — c'est **l'écart n° 5**, inchangé |
| **Exposition UI** des paramètres et des besoins | **L7.7** | Le §10.4 impose que toute frontière exposée soit celle qui est consommée |
| ~~Réalignement de `sensor.vmc_intention`~~ | **fait ici** | Voir §6 — une divergence introduite par ce lot ne peut pas être réparée plus tard |

---

## 5. Les besoins ne sont pas encore hystérétiques — et c'est assumé

À ce stade, **entrée et libération partagent la même frontière de niveau** :
les besoins reproduisent la sémantique en vigueur, mais **par pièce**.

> **Conséquence sur le §9.1.** Tant qu'il n'existe **aucune bande morte**, la
> restauration au redémarrage **n'a pas d'objet** : les cas 1 et 2 du §9.1
> couvrent tout l'espace des mesures, et un état restauré serait immédiatement
> écrasé par la mesure courante. Le cas 3 — « dans la bande morte, l'état
> restauré est conservé » — n'a pas de domaine d'application.

**C'est pourquoi les besoins sont des capteurs `template` et non des états
écrits à ce stade.** L6 a établi qu'un capteur `template` ne peut pas porter
d'hystérésis **persistante** ; la question se pose **à L7.4**, quand la bande
morte apparaît, et c'est là qu'elle sera tranchée.

> **Précision par rapport à L6.** Le dépôt pratique déjà une hystérésis en
> `template` via `is_state(this.entity_id, …)` — par exemple
> `binary_sensor.besoin_clim_cool`. Cet idiome tient l'hystérésis **en session**
> mais **ne survit pas au redémarrage**. Le constat de L6 vaut donc pour la
> **persistance** exigée par le §9.1, non pour l'hystérésis en général. L7.4
> devra choisir entre cet idiome et un état écrit, en connaissance de cause.

---

## 6. L'écart n° 6 est corrigé dans ce lot, et non reporté

`sensor.vmc_intention` calculait sa cause **indépendamment de la décision** :
il lisait les **trois** mesures de pièce, dont le séjour, et le helper
**global** `vmc_seuil_on`. C'est l'**écart n° 6**, relevé par L6 au titre du
**§11.2**, qui interdit toute approximation susceptible de diverger de la
décision réelle.

> **Ce lot rendait la divergence certaine, et non plus seulement possible** :
> l'intention aurait désigné **« Séjour »** comme cause alors que le séjour ne
> décide plus rien, et comparé à une frontière **que le système ne consomme
> plus** (§10.4).
>
> **Une divergence introduite aujourd'hui ne peut pas être réparée plus tard.**
> Elle est donc supprimée **à la source**, dans le lot qui la crée.

### 6.1 Ce qui change

**La cause est désormais dérivée de l'attribut autoritatif `composition`** de
`binary_sensor.vmc_haute_vitesse_requise`. Le capteur d'intention **ne
recalcule plus rien** : il ne lit aucune mesure de pièce, aucune frontière, et
n'applique aucune comparaison. Le §11.2 est satisfait **par construction**, la
cause étant calculée à partir de la décision elle-même.

`unique_id` inchangé : **`entity_id` conservé**, aucune migration.

**Quatre attributs sont retirés** — `humidite_max`, `piece_dominante`,
`co2_sejour`, `delta_humidite_absolue` : chacun constituait un **recalcul
indépendant de la décision**. Aucun n'était consommé par l'UI, qui ne lit que
`cause` — vérifié dans `carte_vmc_intention.yaml`. **Il ne s'agit donc pas
d'une modification d'UI**, réservée à L7.7.

Quatre attributs les remplacent, tous dérivés de la source autoritative :
`composition_autoritative`, `source_disponible`, `cause_indisponibilite`, et la
`cause` elle-même.

### 6.2 Comportement quand la source manque

**Aucun repli silencieux** : la situation est **nommée**, jamais remplacée par
une cause plausible.

| Situation | `state` | `cause` |
|---|---|---|
| Décision `on`, composition exposée | Extraction utile demandée | `Besoin actif – <composition>` |
| Décision `off` | Fonctionnement nominal demandé | `Aucun besoin identifié` |
| Composition **absente ou vide** | selon la décision | `Composition non exposée par la décision` |
| Décision `unavailable` / `unknown` | **Intention indisponible** | `Décision indisponible` |

Dans les deux derniers cas, **aucune pièce n'est nommée** — c'est testé.

### 6.3 Effet de bord

`intention.yaml` **ne lit plus `aeration_preferable_etage`** et **sort** de la
liste des consommateurs légitimes du checker d'aération. C'est un pas de plus
vers le **critère de clôture 8**, obtenu sans lot dédié.

---

## 7. Contrôles exécutés

**86 checkers `arsenal_contracts` exécutés**, tous passent. Les quatre fichiers
runtime modifiés ou créés sont **valides au parseur YAML**.

### 7.1 Tests ciblés du §11.2

`check_vmc_contracts.py` reçoit un **test 4** dédié à l'invariant de
non-divergence. Le contrôle est **comportemental** : le gabarit Jinja de
`cause` est **extrait du fichier contrôlé** puis **évalué**.

> **Aucune logique n'est reproduite dans le test** — une copie du gabarit le
> rendrait aveugle à toute dérive du fichier contrôlé.

| Contrôle | Objet |
|---|---|
| **4a** | la cause ne lit **aucune** source indépendante de la décision : mesure de pièce, frontière, CO₂, verdict d'aération |
| **4b** | la cause **dérive** de l'attribut `composition` |
| **4c** | comportement évalué sur quatre compositions — une pièce, deux pièces, une composition contenant le séjour, décision `off` : la cause **restitue** la composition autoritative et **ne mentionne jamais une pièce que celle-ci ne contient pas** |
| **4d** | comportement défini quand la source manque — composition absente, composition vide, décision `unavailable`, décision `unknown` : la cause est **non vide** et **n'invente aucune pièce** |

**Preuve négative établie** : un gabarit muté pour recalculer la cause depuis
`sensor.humidite_relative_sejour` fait **échouer le checker** — 6 erreurs, dont
la mention interdite de « Séjour » et la lecture d'une source indépendante. Le
test n'est donc pas décoratif.

Le workflow `contracts_vmc.yml` installe désormais `pyyaml` et `jinja2`,
nécessaires à cette évaluation.

### 7.2 Liste des consommateurs d'aération

**Deux modifications de checker étaient mécaniquement requises.**

**La première** : le verrou
d'aération ayant quitté `haute_vitesse_requise.yaml` pour les deux besoins
locaux, la liste des consommateurs légitimes de
`check_aeration_recommandation_contracts.py` a été mise à jour en conséquence —
`haute_vitesse_requise.yaml` **en sort**, les deux besoins **y entrent à titre
explicitement temporaire**, leur retrait constituant la **preuve du lot L7.2**
et servant le **critère de clôture 8**.

**La seconde** : `intention.yaml` **ne lit plus** le verdict d'aération depuis
sa correction (§6) et **sort** donc de cette liste.

Seul `delta_humidite_absolue_favorable.yaml` **y reste** : sa lecture est
**non décisionnelle** (§4.3, §10.5).

> **Deux échecs de checkers demeurent, ANTÉRIEURS à ce lot** et vérifiés comme
> tels : `lovelace_no_inline_templating` et `vacances`. Ni causés, ni aggravés,
> hors périmètre de C35.

Les **gates documentaires** passent.

---

## 8. Ce que ce lot ne fait pas

- il **ne modifie pas `/config`** : le dépôt est le miroir versionné, son
  déploiement est un acte distinct ;
- il **ne recalibre rien** ;
- il **n'introduit ni hystérésis, ni voie d'évolution, ni frontière modulée** ;
- il **ne retire pas le verrou d'aération** — il le déplace ;
- il **n'applique pas le §4.4** ;
- il **n'expose rien de nouveau en UI** ;
- il **ne prononce pas** le rattachement définitif du séjour ;
- il **ne clôt pas C35** — les écarts n° 1, 3 et 5 demeurent, les écarts n° 2 et
  4 sont **partiellement traités** — l'état par pièce existe, les frontières de
  libération ne sont toujours pas consommées — et l'**écart n° 6 est résorbé**
  (§6).

---

## 9. Prochain jalon

**L7.2 — retrait du verrou d'aération.** Son périmètre est désormais réduit et
localisé : deux lignes dans deux fichiers, et deux entrées d'allowlist. C'est
l'écart n° 1, et le critère de clôture 8.
