# Audit Arsenal — Températures intérieures / façades thermiques internes

> Type : rapport d'audit architectural — version finale officielle
> Portée : capteurs de température intérieure, façades par zone, agrégats min/max,
>          consommateurs (chauffage, climatisation, aération), diagnostics, UI
> Mode : lecture seule — aucun runtime, contrat ou UI modifié ; aucun patch produit
> Principe directeur : « le runtime est la référence, le contrat documente le runtime »

---

## 1. Résumé exécutif

**Signal net.** L'axe température intérieure est **bien architecturé par zone** :
chaîne souveraine `brut → consolidée → stabilisée → façade`, chacune avec
validation, plausibilité, mémoire TTL 1800 s et **doctrine d'abstention explicite
(`unknown`)**. Les consommateurs décisionnels (chauffage, climatisation, aération)
possèdent **tous** une garde d'indisponibilité correcte.

**Risque principal — réponse à la question centrale : OUI.** Le système dépend de
deux **agrégats** supposés disponibles qui peuvent masquer une indisponibilité
réelle : `sensor.temperature_min_chambres` et `sensor.temperature_max_chambres`.
Lorsque toutes les chambres deviennent indisponibles, ces agrégats **republient
leur dernière valeur (`{{ last }}`) sans aucun TTL ni `time_pattern`** — donc ils
ne passent jamais à `unknown` en régime établi. Les gardes d'abstention (par
ailleurs correctes) de chauffage / clim / aération sont alors **neutralisées**, et
ces domaines peuvent décider sur une température intérieure **gelée indéfiniment**.

**Criticité globale : ÉLEVÉE-LOCALISÉE.** La faille n'est pas dans les façades par
zone (saines), mais dans la **couche d'agrégation**, qui réintroduit une mémoire
non bornée, en contradiction avec la doctrine d'abstention que l'axe applique une
couche plus bas.

**Conclusion architecturale.** `temperature_min_chambres` /
`temperature_max_chambres` sont les **références thermiques de décision de facto**
(aucune entité « référence chauffage/clim » nommée n'existe), mais elles ne sont
**ni souveraines ni contractualisées** quant à leur mémoire. C'est l'écart à
corriger.

---

## 2. Périmètre analysé

**Fichiers inspectés (clés) :**

- Contrats : `contrats/meteo/axe_temperature.md`,
  `contrats/meteo/temperature_interieure/{consolidation,stabilisation}.md`,
  `gouvernance.md`, `validation.md`
- Implémentation par zone :
  `12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/{consolidation,stabilisation,facade}.yaml`
- Agrégats :
  `12_template_sensors/meteo/mesures/temperature/chambres/min/{valeur,nom}.yaml`,
  `chambres/max/global/{valeur,nom}.yaml`, `chambres/max/rdc/valeur.yaml`
- Consommateurs : `chauffage/autorisation_cible_selon_temperature.yaml`,
  `chauffage/ecart_consigne/*`, `chauffage/diagnostic_thermique/*`,
  `climatisation/seuils_on_off/{cool,heat}/*`, `aeration/conseillee/etage.yaml`,
  `10_scripts/aeration/m1_debut_episode.yaml`

**Domaines couverts :** chauffage, climatisation, aération, UI/diagnostics.
**Exclusions :** humidité intérieure (hors axe température), extérieur (audit
précédent).

---

## 3. Cartographie des capteurs intérieurs

| Entité | Type | Rôle | Disponibilité réelle | Comportement dégradé |
|---|---|---|---|---|
| `sensor.temperature_<zone>_1` | brute (HomeKit) | source primaire par zone | Faillible (pont HomeKit) | exclue si `unknown`/`unavailable`/hors `[5;45]` |
| `sensor.temperature_<zone>_2` | brute (Zigbee) | source secours par zone | Faillible (coordinateur) | idem |
| `sensor.temperature_brute_consolidee_<zone>` | consolidée | fusion 2 sources + mémoire | Dérivée | `unknown` (abstention) si 2 invalides sans mémoire ≤ 1800 s |
| `sensor.temperature_stabilisee_<zone>` | stabilisée | EWMA α=0.35, δ_max=0.3 | Dérivée | suit l'abstention amont |
| `sensor.temperature_<zone>` | **façade UI** | projection LTS, availability-gated | Façade | passe **`unavailable`** si stabilisée indispo |

Zones (`<zone>`) : `chambre_arnaud`, `chambre_matthieu`, `chambre_parents`,
`sejour`, `entree`, `petite_maison`.

---

## 4. Façades et agrégats thermiques

### 4.1 Façades par zone — **SAINES**

`interieur_multi_capteurs/facade.yaml` : « Façade UI (LTS ready) », projection pure,
`availability` filtrant `unknown/unavailable/none`, `state` toujours numérique.
Conforme à la doctrine : quand la zone tombe, la façade `sensor.temperature_<zone>`
passe honnêtement à `unavailable`.

### 4.2 Agrégats min/max — **RUPTURE DE DOCTRINE**

- `sensor.temperature_min_chambres` (`chambres/min/valeur.yaml`) — chambre la plus
  froide ; attribut `chambre_la_plus_froide` ; sources = façades
  arnaud/matthieu/parents.
- `sensor.temperature_max_chambres` (`chambres/max/global/valeur.yaml`) — chambre
  la plus chaude ; attribut `chambre_la_plus_chaude`.
- Logique commune : `valides = … selectattr('is_number')` ; **si `valides` vide →
  `{{ last }}`** (republie `this.state`). Déclencheurs = `state` des trois façades +
  `homeassistant start`, **sans `time_pattern`**.

Conséquence : pas de borne temporelle sur la mémoire, pas de ré-évaluation
périodique. Une fois toutes les chambres indisponibles, l'agrégat **fige sa
dernière valeur** et n'émet jamais `unknown`. Il n'existe **aucune entité de
référence chauffage/clim distincte** : ces agrégats jouent ce rôle.

---

## 5. Vérification factuelle ligne par ligne (agrégats min/max)

Fichiers cités :

- **MIN** — `12_template_sensors/meteo/mesures/temperature/chambres/min/valeur.yaml`
- **MAX** — `12_template_sensors/meteo/mesures/temperature/chambres/max/global/valeur.yaml`

### 5.1 Branche `{{ last }}` — confirmée

MIN, lignes 53–58 :

```
53:  {% set last = this.state %}
55:  {% if valides %}
56:    {{ (valides | sort(attribute=1))[0][1] | float | round(1) }}
57:  {% else %}
58:    {{ last }}
```

MAX, lignes 52–57 :

```
52:  {% set last = this.state %}
54:  {% if valides %}
55:    {{ (valides | sort(attribute=1))[-1][1] | float | round(1) }}
56:  {% else %}
57:    {{ last }}
```

Dans les deux cas, `last = this.state` (ligne 53 / 52) et la branche `{% else %}`
(faute de valeurs valides) republie `{{ last }}` (ligne 58 / 57).

### 5.2 Calcul de `valides` — identique

MIN ligne 52 / MAX ligne 51, à l'identique :

```
{% set valides = brut.items() | selectattr('1', 'is_number') | list %}
```

`valides` ne retient que les façades numériques. Si toutes les chambres sont
`unavailable`/`unknown`, `valides` est vide → `{% if valides %}` faux → branche
`{{ last }}`.

### 5.3 Aucun TTL appliqué — confirmé

Recherche de `last_changed` / `as_timestamp` / `TTL` / `1800` dans les deux
fichiers : **aucune occurrence**. `last = this.state` est utilisé brut, sans
comparaison d'âge. La valeur gelée n'expire donc jamais.

> À comparer avec `interieur_multi_capteurs/consolidation.yaml`, qui calcule
> `age_ok = (now_ts - last_changed_ts) <= 1800` et applique une expiration TTL.

### 5.4 Aucun `time_pattern` — confirmé

Triggers déclarés — MIN lignes 29–36 / MAX lignes 28–35 :

```
- trigger:
    - platform: state
      entity_id:
        - sensor.temperature_chambre_arnaud
        - sensor.temperature_chambre_matthieu
        - sensor.temperature_chambre_parents
    - platform: homeassistant
      event: start
```

Deux déclencheurs seulement : changement d'état des trois façades, et démarrage HA.
**Aucun `platform: time_pattern`** (recherche vide). Une fois toutes les façades
indisponibles et l'agrégat figé, plus aucun trigger ne se déclenche tant qu'une
façade ne revient pas → pas de ré-évaluation périodique, pas d'expiration possible.

### 5.5 Identité min / max — confirmée

Comportement **identique** pour min et max : même calcul de `valides`, même
`last = this.state`, même branche `{{ last }}`, mêmes deux triggers sans
`time_pattern`, aucun TTL. Seules différences : l'index de tri (`[0]` pour le min,
`[-1]` pour le max) et le nom de l'attribut (`chambre_la_plus_froide` /
`chambre_la_plus_chaude`).

---

## 6. Chaînes de dépendance

**Chaîne par zone (souveraine, conforme) :**
`temperature_<zone>_1/_2 (brut)` →
`temperature_brute_consolidee_<zone> (validation [5;45], fusion 0.8 °C, mémoire TTL 1800 s, time_pattern /5, abstention unknown)` →
`temperature_stabilisee_<zone> (EWMA 0.35)` →
`temperature_<zone> (façade availability-gated)`.

**Chaîne d'agrégation (rupture de doctrine) :**
`temperature_chambre_arnaud / _matthieu / _parents (façades)` →
**`temperature_min_chambres` / `temperature_max_chambres` (mémoire `{{ last }}` non bornée, sans TTL, sans time_pattern)`** →
`chauffage / climatisation / aération`.

La propriété d'abstention, garantie en amont, est **perdue** précisément à la
jonction « façades → agrégats ».

---

## 7. Consommateurs par domaine — gardes correctes mais neutralisées

**Chauffage.** `autorisation_cible_selon_temperature.yaml`
(`cold = temperature_min_chambres | float(99)` → `if cold == 99 → cible 'unknown'`) ;
`ecart_consigne/{ecart_instantane,ecart_confort,ecart_doux,ecart_froid}.yaml` ;
nombreux `diagnostic_thermique/*` (inertie arrêt/reprise, cycles présence, plancher,
stabilisation absence).

**Climatisation.**
`seuils_on_off/cool/{seuil_allumage_cool_atteint,seuil_extinction_cool_atteint}.yaml`,
`heat/{seuil_allumage_heat_atteint,seuil_extinction_heat_atteint}.yaml` (gardes
explicites `in ['unknown','unavailable','']`).

**Aération.** `conseillee/etage.yaml` (`t_in = temperature_max_chambres`, garde
`reject in ['unknown','unavailable','None']`) ;
`10_scripts/aeration/m1_debut_episode.yaml`.

**Dérivé.** `meteo/mesures/point_de_rosee/etages/etage.yaml`
(`temperature_max_chambres`).

**UI / diagnostics.**
`19_button_card_templates/40_dashboards/arsenal/30_diagnostic/carte_temperature_{min,max}_chambres.yaml` ;
cartes `climatisation/50_eligibilite/*`.

**Point essentiel.** Les gardes des consommateurs sont **bien écrites**. Elles
échouent uniquement parce que l'agrégat ne leur transmet jamais le signal
d'indisponibilité : une valeur gelée reste un nombre, donc ni `float(99)==99`, ni
`is not none` faux, ni `in ['unknown','unavailable','']`, ni `reject in [...]` ne se
déclenchent. Le défaut est unique et en amont.

---

## 8. Analyse unknown/unavailable

| Maillon | Si source(s) indispo | Verdict |
|---|---|---|
| `temperature_brute_consolidee_<zone>` | `unknown` après expiration TTL 1800 s ; time_pattern /5 garantit l'expiration | **Correct** |
| `temperature_<zone>` (façade) | `unavailable` (availability) | **Correct** |
| `temperature_min_chambres` / `_max_chambres` | **gèle `{{ last }}`**, jamais `unknown`, pas de TTL, pas de time_pattern | **Défaillant** |
| chauffage `autorisation_cible` | abstient (`cible='unknown'`) seulement si `min_chambres == 99` → ne se déclenche pas sur valeur gelée | Garde **neutralisée** |
| chauffage `ecart_instantane` | garde `is not none` → valeur gelée = nombre → poursuit | Garde **neutralisée** |
| clim `seuil_*_atteint` | garde `in ['unknown','unavailable','']` → valeur gelée ≠ ces états → poursuit | Garde **neutralisée** |
| aération `conseillee/etage` | garde `reject in [...]` → `max_chambres` gelé = nombre → poursuit | Garde **neutralisée** |

Cas favorable : au démarrage HA (agrégat à `unknown` tant qu'aucune façade n'a
publié), les gardes fonctionnent ; le risque concerne la **panne en régime établi**
(toutes chambres tombant alors que HA tourne).

---

## 9. Écarts et dettes

**Dette runtime (critique).** `temperature_min_chambres` /
`temperature_max_chambres` : mémoire `{{ last }}` non bornée, sans TTL ni
`time_pattern`, en contradiction directe avec la doctrine d'abstention de
`temperature_interieure/consolidation.md §6` (qui impose `{{ 'unknown' }}`, interdit
la continuité non bornée, et rend `time_pattern /5` obligatoire pour l'expiration).

**Dette contractuelle.**

1. Plausibilité intérieure : `axe_temperature.md §3` déclare **8–40 °C**, alors que
   `temperature_interieure/consolidation.md` **et** le runtime utilisent
   **5–45 °C**. Contradiction interne entre deux contrats ; `axe_temperature.md`
   est l'obsolète.
2. `contrat_fallback.md` référencé par `axe_temperature.md §7` — **inexistant**
   (même dette que l'axe extérieur).
3. **Aucun contrat ne régit les agrégats `min/max_chambres`** : ils sont seulement
   *déclarés en entrée* par des contrats consommateurs
   (`chauffage/15_capteurs/01_capteurs_decision.md`, etc.), jamais gouvernés quant à
   leur mémoire.

**Dette diagnostic.** La consolidation/stabilisation exposent une riche
observabilité (`mode_resolution`, `source_active`, `ecart_sources`,
`mode_stabilisation`, `delta_*`). Les agrégats n'exposent que
`chambre_la_plus_froide/chaude` (avec repli texte `Mémoire`) — **aucun statut, âge
mémoire, ni signal « toutes chambres indisponibles »**. Le gel est invisible à la
supervision.

**Dette UI.** Mineure : les cartes `carte_temperature_{min,max}_chambres`
afficheraient la valeur gelée comme si elle était vivante — symptôme du défaut
runtime sous-jacent, pas une faute UI propre.

---

## 10. Risques réels

1. **Chauffage sur donnée gelée.** Panne simultanée HomeKit + Zigbee (ou stalle du
   pipeline) → `min_chambres` figé → `autorisation_cible` poursuit comme si l'info
   était fraîche ; risque de sur/sous-chauffe silencieuse, sans abstention ni
   alerte.
2. **Climatisation sur seuils gelés.** `seuil_allumage_heat/cool_atteint` évalués
   sur valeur figée → décisions on/off potentiellement erronées.
3. **Aération sur `max_chambres` gelé.** Recommandation calculée sur un intérieur
   fantôme.
4. **Invisibilité.** Le seul indice est l'attribut passant à `Mémoire` ; l'état
   numérique reste « sain », donc aucune supervision active ne détecte la panne.
5. **Asymétrie trompeuse.** Tout l'étage inférieur respecte l'abstention
   souveraine ; l'agrégat la rompt — un lecteur du système suppose légitimement que
   la propriété se propage, ce qui n'est pas le cas.

---

## 11. Recommandations architecturales (sans code)

- **Propager la souveraineté jusqu'aux agrégats.** `min/max_chambres` doivent
  hériter de la même doctrine que `consolidation.md` : abstention explicite
  (`unknown`) quand toutes les sources sont indisponibles, mémoire **bornée par
  TTL**, et déclenchement permettant l'expiration. Le repli `{{ last }}` non borné
  est à proscrire.
- **Signal d'indisponibilité agrégée.** Exposer un statut/âge sur l'agrégat (sur le
  modèle `mode_resolution`/`source_active`) pour qu'une indisponibilité totale soit
  observable et alertable.
- **Réconcilier la plausibilité.** Aligner `axe_temperature.md §3` (8–40) sur le
  runtime / `consolidation.md` (5–45), ou statuer formellement sur la borne retenue.
- **Contractualiser les agrégats.** Créer un contrat d'agrégation chambres
  (référence min/max), aujourd'hui absent, définissant mémoire, abstention et rôle
  de référence chauffage/clim.
- **Conserver les gardes consommateurs.** Elles sont correctes ; une fois l'agrégat
  rendu honnête (`unknown` sur panne totale), elles fonctionneront comme prévu sans
  modification de leur logique.

*Le présent rapport ne propose aucun code correctif : il caractérise et localise le
défaut. Les modalités d'implémentation relèvent d'un plan d'action et des arbitrages
ci-dessous.*

---

## 12. Arbitrages humains

1. **Borne de plausibilité intérieure :** 5–45 (runtime) ou 8–40
   (`axe_temperature.md`) — laquelle devient la norme, et quel contrat est corrigé ?
2. **TTL des agrégats :** reprendre 1800 s (cohérent avec la consolidation) ou
   définir un TTL propre aux agrégats (plus court, car ils dépendent déjà d'entités
   elles-mêmes mémorisées) ?
3. **Sur panne totale des chambres :** le chauffage/clim doivent-ils *abstenir*
   (cible `unknown`), *se replier* sur une consigne de sécurité, ou *geler mais
   alerter* ? Choix de politique métier.
4. **Référence de décision :** officialiser `min/max_chambres` comme références
   contractuelles, ou introduire une entité de référence dédiée par domaine ?
5. **Périmètre des agrégats :** la variante `chambres/max/rdc/valeur.yaml` et les
   zones hors chambres (`sejour`, `entree`, `petite_maison`) doivent-elles entrer
   dans une référence de zone élargie ?
