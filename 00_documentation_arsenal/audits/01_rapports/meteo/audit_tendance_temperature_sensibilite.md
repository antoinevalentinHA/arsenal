# Audit Arsenal — Tendance thermique des agrégats intérieurs / faux « stable »

> Type : rapport d'audit documentaire (lecture seule)
> Portée : famille « tendance thermique des agrégats intérieurs » (contrat
>          `tendance_temperature.md` v1.0), couche statistique + couche
>          d'interprétation, source agrégée, changelog v16.0.1.
> Mode : lecture seule — aucun code, contrat, runtime ou UI modifié dans cette passe.
> Principe directeur : en **audit**, le **runtime observé** est la **référence
>          factuelle** (ce que fait réellement le système) ; en **gouvernance
>          Arsenal**, le **contrat** reste l'**autorité normative** (ce que le
>          système *doit* faire). Ce rapport n'inverse pas cette hiérarchie : il
>          établit que le contrat v1.0 est **normativement insuffisant** et doit
>          être **amendé avant** toute correction runtime.
> Constat déclencheur : `sensor.tendance_temperature_max_chambres = stable` alors que
>          l'historique de `Température max Chambres` montre une hausse nette
>          (≈ 23,9 °C → 24,5 °C, pente récente positive).

---

## 1. Résumé exécutif

**Signal net.** La famille tendance est conforme à son contrat. Le runtime
implémente fidèlement la doctrine v1.0. Le faux « stable » **n'est pas un bug
d'implémentation** : c'est une **conséquence directe et déterministe de la
grandeur de décision imposée par le contrat §3.2**.

**Cause racine.** La grandeur de décision retenue —
`écart = valeur instantanée − moyenne glissante 60 min de la même source` — est un
**mauvais estimateur de tendance pour une rampe lente**. Sur une montée monotone,
cet écart **ne croît pas avec l'ampleur de la hausse** : il **sature** à
`pente × W/2`. Avec `W = 60 min`, le plafond d'écart vaut `pente × 30 min`. Pour
franchir `S_in = 0,4 °C`, la source doit donc monter à **≥ 0,8 °C/h soutenue**
(≈ 1,0 °C/h une fois pris en compte l'arrondi 0,1 °C de la source). Or une dérive
de confort intérieur perceptible se situe typiquement entre **0,2 et 0,6 °C/h** :
**toute la bande des tendances réellement utiles tombe à l'intérieur de la zone
morte** ⇒ « stable » permanent.

**Vérification quantitative** (rampe linéaire simulée, source arrondie 0,1 °C,
moyenne arithmétique 60 min) :

| Hausse totale | Durée | Pente | Écart en régime établi | Verdict moteur |
|---|---|---|---|---|
| +0,6 °C | 60 min | 0,60 °C/h | 0,30 °C | stable (faux négatif) |
| +0,6 °C | 90 min | 0,40 °C/h | 0,24 °C | stable (faux négatif) |
| +0,6 °C | 120 min | 0,30 °C/h | 0,19 °C | stable (faux négatif) |
| +0,8 °C | 60 min | 0,80 °C/h | 0,39 °C | stable (faux négatif) |
| +1,0 °C | 60 min | 1,00 °C/h | 0,49 °C | **hausse** |

Le scénario observé (+0,6 °C) **ne peut pas** produire « hausse » quelle que soit
sa durée : l'écart plafonne à ≈ 0,30 °C, toujours sous `S_in`.

**Criticité.** MODÉRÉE côté système (aucune décision, aucun pilotage ne dépend de
ce capteur — INV-TEND-12), mais **ÉLEVÉE côté usage** : l'organe est, en l'état,
inopérant pour son intention déclarée (§1 du contrat : « lecture utile et lisible
pendant la conduite »). Il affiche « stable » dans la quasi-totalité des situations
de confort réelles.

**Nature de la correction.** **Doctrinale, pas paramétrique.** Baisser simplement
`S_in` ne corrige pas la saturation : cela rapproche le seuil du plancher de bruit
sans rétablir une grandeur qui croît avec la tendance. La correction porte sur la
**grandeur de décision** (contrat §3.2 / §5 / §8), donc sur le contrat avant le
runtime.

---

## 2. Fichiers inspectés (liste exacte)

| Rôle | Chemin | Constat |
|---|---|---|
| Contrat normatif | `00_documentation_arsenal/contrats/meteo/tendance_temperature.md` (v1.0) | Porte la doctrine fautive (§3.2, §8). |
| Couche statistique | `13_sensor_platforms/statistics/meteo/tendance_temperature.yaml` | `statistics`/`mean`, `max_age: 60 min`, `sampling_size: 10000`. Conforme contrat. |
| Couche interprétation | `12_template_sensors/meteo/tendance/temperature.yaml` | Trigger template, écart vs moyenne 60 min, hystérésis 0,4/0,2, `time_pattern /5`. Conforme contrat. |
| Source agrégée (axe incriminé) | `12_template_sensors/meteo/mesures/temperature/chambres/max/global/valeur.yaml` | `sensor.temperature_max_chambres`, **arrondi `round(1)`** (quantification 0,1 °C). |
| Pattern statistique de référence | `13_sensor_platforms/statistics/meteo/temperature.yaml` | Confirme que `statistics`/`mean` est bien le motif maison (ici fenêtre 30 j). |
| Changelog | `00_documentation_arsenal/changelog/changelogs/v16/v16_0_1.md` (l. 130-131, 183-186, 257) | Introduction de la famille en v16.0.1 ; seuils 0,4/0,2 figés. |
| Docs liés (référencement only) | `contrats/meteo/README.md`, `navigation/domaines/meteo.md` | Référencent la famille ; ne portent aucune logique. |
| Checkers / tests | `tools/`, `scripts/`, `.github/` | **Aucun checker dédié** à la tendance température (grep négatif). |

---

## 3. Logique actuelle reconstituée (runtime = référence)

**Chaîne, par axe** `<axe> ∈ {min_chambres, moyenne_maison, max_chambres}` :

```
sensor.temperature_<axe>                      (agrégat source, arrondi 0,1 °C)
   │  lecture seule
   ▼
sensor.temperature_<axe>_moyenne_60_min       statistics / mean, max_age 60 min
   │  lecture
   ▼
sensor.tendance_temperature_<axe>             trigger template, état + icône
```

**Paramètres effectifs constatés** (identiques contrat ↔ runtime) :

| Élément | Valeur runtime |
|---|---|
| Source utilisée | `sensor.temperature_<axe>` (valeur instantanée) |
| Fenêtre de lissage `W` | 60 min (`max_age`) |
| Moyenne de référence | `statistics` / `state_characteristic: mean` (moyenne arithmétique des échantillons de la fenêtre) |
| Grandeur de décision | `ecart = round( source − moyenne_60_min , 2 )` |
| Seuil d'entrée `S_in` | 0,4 °C |
| Seuil de sortie `S_out` | 0,2 °C (hystérésis via `this.state`) |
| États possibles | `hausse \| baisse \| stable \| indisponible` (ensemble fermé) |
| Fallback | aucun (abstention : source non numérique ⇒ `indisponible`) |
| Déclencheurs | état source + état moyenne_60_min + `homeassistant start` + `time_pattern /5 min` |
| Fréquence MAJ effective | ≥ toutes les 5 min, plus à chaque changement de source/moyenne |
| Lissage réel | fort côté moyenne (60 min) ; **nul côté valeur instantanée** (un seul échantillon courant, arrondi 0,1 °C) |

**Règle d'état (verbatim logique)** :

```
ecart >= +0,4                         → hausse
ecart <= -0,4                         → baisse
prev == hausse  et  ecart > +0,2      → hausse   (maintien hystérésis)
prev == baisse  et  ecart < -0,2      → baisse   (maintien hystérésis)
sinon                                  → stable
source non numérique                   → indisponible
```

---

## 4. Pourquoi le runtime reste « stable » malgré une hausse visible

Cause par cause, au regard du dépôt réel.

### 4.1 Cause dominante — saturation structurelle de l'écart (grandeur de décision inadaptée)

La grandeur `valeur instantanée − moyenne glissante` mesure **« de combien suis-je
au-dessus de ma propre moyenne récente, là, maintenant »**. Pour une rampe
linéaire de pente `r`, la moyenne d'une fenêtre `[t−W, t]` vaut la valeur au
**milieu de fenêtre** (`t − W/2`). Donc :

```
ecart(t) ≈ valeur(t) − valeur(t − W/2) = r × (W/2)
```

L'écart **se stabilise** à `r × W/2` et **n'augmente plus**, même si la hausse se
poursuit pendant des heures. Avec `W = 60` : `ecart_plafond = r × 30 min`.

- Seuil d'entrée `S_in = 0,4 °C` ⇒ pente minimale détectable = `0,4 / 30 ≈ 0,0133 °C/min = 0,8 °C/h`.
- Scénario observé (+0,6 °C) ⇒ pente ≤ 0,6 °C/h ⇒ `ecart_plafond ≤ 0,30 °C` < 0,4 ⇒ **stable**, sans échappatoire.

C'est la cause **première et suffisante**. Elle est **inscrite dans le contrat
§3.2** : la doctrine, et non le code, est en cause.

### 4.2 Cause aggravante — calibrage seuil/fenêtre orienté « marche d'escalier »

`S_in = 0,4 °C` a été justifié (contrat §8.2) comme « dérive perceptible sur une
heure ». Ce raisonnement suppose implicitement que l'écart **égale** la dérive
horaire. Faux : à cause de §4.1, l'écart **vaut la moitié** de la dérive sur la
fenêtre. La zone morte effective est donc **deux fois plus large** que prévu : il
faut ≈ 0,8 °C de dérive horaire réelle pour la franchir.

### 4.3 Cause aggravante mineure — quantification 0,1 °C de la source

`sensor.temperature_max_chambres` est arrondi `round(1)`. Sur une rampe lente, la
valeur instantanée progresse par paliers de 0,1 °C, ce qui élève d'environ
0,1 °C/h supplémentaire la pente réellement nécessaire au franchissement (≈ 1,0 °C/h
constaté en simulation vs 0,8 °C/h théorique). Secondaire, mais réel.

### 4.4 Causes écartées (vérifiées, non responsables)

- **Arrondi de l'écart** (`round(2)`) : négligeable (0,30 vs 0,40 reste tranché).
- **Fréquence de trigger** (`/5 min` + changements) : suffisante ; la valeur ne
  « manque » pas le seuil par défaut de réévaluation.
- **`sampling_size: 10000`** : borné par `max_age 60 min`, généreux ; pas de
  troncature de fenêtre.
- **Retard / indisponibilité Recorder** : effet transitoire au redémarrage
  uniquement (backfill de la moyenne) ; n'explique pas un « stable » en régime
  permanent.
- **Moyenne trop inertielle** : la moyenne 60 min **est** inertielle, mais ce
  n'est pas le défaut en soi — le défaut est de **comparer la valeur à cette
  moyenne** plutôt que de mesurer une variation. Une moyenne plus courte
  atténuerait sans supprimer la saturation (§6).

**Conclusion §4 : faux « stable » = saturation déterministe de la grandeur de
décision (§4.1), amplifiée par un seuil calibré sur une sémantique de marche
(§4.2) et par la quantification source (§4.3).**

---

## 5. La doctrine actuelle répond-elle au besoin réel ?

**Non, pour l'intention déclarée.** Le contrat §1 vise une « lecture utile et
réactive pour le confort thermique » : hausse perceptible, baisse perceptible,
stable **seulement** si la température est réellement plate. Le contrat §1
hiérarchise toutefois « robustesse > lisibilité > stabilité » et déclare la
réactivité « explicitement secondaire ».

Le défaut est que l'implémentation actuelle **n'a pas sacrifié la réactivité au
profit de la robustesse** : elle a choisi une grandeur qui **ne mesure pas la
tendance**. Le résultat n'est pas « peu réactif mais juste » ; il est **faux** sur
la quasi-totalité de la plage de confort. Un organe qui répond « stable » à
+0,6 °C/h ne fournit aucune des trois informations promises.

La doctrine reste valable sur ses principes structurants (backend interprète, UI
restitue, hystérésis obligatoire, états fermés, indisponibilité honnête, lecture
seule des sources). **Seule la grandeur de décision §3.2 est à revoir.**

---

## 6. Doctrine corrigée — analyse (aucune décision figée ici)

Trois options, par ordre de robustesse croissante.

### Option A — Recalibrage seul (paramètres §8)

Garder la grandeur « valeur − moyenne », raccourcir `W` et baisser les seuils.
Ex. `W = 30 min`, `S_in ≈ 0,12 °C`, `S_out ≈ 0,06 °C`.
- **Effet** : abaisse le plancher de détection vers ≈ 0,5 °C/h.
- **Limite rédhibitoire** : on plonge dans le bruit. Source arrondie 0,1 °C +
  bruit capteur ±0,1–0,2 °C ⇒ `S_in` à 0,12 °C est **sous le bruit** ⇒ faux
  positifs et scintillement. **Ne traite pas la saturation, déplace le problème.**
  → **Écartée comme cible**, acceptable seulement en palliatif provisoire.

### Option B — Changer la grandeur pour une vraie variation (recommandée)

Remplacer `valeur − moyenne` par une grandeur qui **croît avec la tendance**, tout
en restant dans l'idiome maison `statistics`/`mean` (sans état, sans écrivain
souverain, sans automatisation — conforme INV-TEND-6 réinterprété « statistique
lissée », §5.1).

**B.1 — Double moyenne (moyenne courte − moyenne longue)** :

```
ecart_tendance = moyenne_glissante(W_court) − moyenne_glissante(W_long)
```

Pour une rampe : `ecart ≈ r × (W_long − W_court)/2`. Avec `W_long = 60`,
`W_court = 15` : `ecart ≈ r × 22,5 min`.
- Lissé **des deux côtés** ⇒ robuste au bruit (corrige le défaut de §4.3 mieux que
  la valeur instantanée).
- Croît avec la pente ⇒ supprime la saturation de §4.1.
- Candidats : `S_in ≈ 0,15 °C`, `S_out ≈ 0,08 °C`. Détecte ≈ 0,4 °C/h (+0,6 °C/h →
  ecart ≈ 0,225 °C > 0,15).
- Coût : un capteur `statistics` supplémentaire par axe (moyenne courte).

**B.2 — `statistics` / `change` (dernier − premier sur fenêtre)** :
`ecart = Δ source sur W`. Lisible (« +0,6 °C sur l'heure »), mais sensible à
l'échantillon de bord — défaut déjà identifié et écarté par le contrat §5.2.
Inférieure à B.1 sur la robustesse.

**B.3 — `sensor`/`derivative` ou `binary_sensor`/`trend`** : mesurent la pente,
mais (a) `trend` impose 2 binaires/axe + recombinaison (déjà écarté §5.2), (b)
`derivative` expose une unité de pente moins lisible. Conformes mais plus lourds
que B.1.

### Option C — Hystérésis sur la grandeur corrigée

Conserver l'hystérésis asymétrique (`S_out < S_in`, INV-TEND-7), appliquée à la
**nouvelle** grandeur. Préserve la stabilité d'icône en conduite, prérequis non
négociable (§1).

### Synthèse des risques

| Critère | A (recalibrage) | B.1 (double moyenne) | B.2 (change) |
|---|---|---|---|
| Supprime la saturation | Non | **Oui** | Oui |
| Robustesse au bruit | Faible | **Élevée** | Moyenne |
| Risque faux positifs | Élevé | Faible | Moyen |
| Lisibilité Android Auto | OK | **OK** (3 états inchangés) | OK |
| Conformité doctrine maison | Oui | **Oui** (`statistics`/`mean`) | Oui |
| Coût implémentation | Nul | +3 capteurs stat. | Nul |

**Impact UI / Android Auto** : dans tous les cas, l'interface reste inchangée —
même ensemble fermé d'états, mêmes icônes (§7 du contrat), même hystérésis pour
éviter le scintillement. Seule la **fréquence de bascule** augmente (l'organe
devient réellement informatif). Aucun changement de nommage, d'alias ou d'ID.

---

## 7. Recommandation argumentée

**Adopter l'Option B.1 (double moyenne courte/longue) avec hystérésis (Option C).**

Justification :
1. C'est la seule option qui **supprime la cause racine** (§4.1) au lieu de la
   déplacer (Option A) ou d'introduire une fragilité de bord (B.2).
2. Elle **reste dans l'idiome Arsenal éprouvé** (`statistics`/`mean`, sans état,
   sans automatisation, sans helper) — coût doctrinal minimal, INV-TEND-2/3/9/10/12
   préservés.
3. Le double lissage **améliore aussi la robustesse au bruit** par rapport à la
   valeur instantanée actuelle (traite §4.3).
4. L'UI et les Favoris Android Auto sont **invariants** : aucun renommage, aucun
   nouvel état, aucune icône nouvelle.

Réserve : **valider les seuils candidats (`S_in ≈ 0,15`, `S_out ≈ 0,08`, `W_court ≈
15 min`) sur données réelles** avant figement (cf. tests §9), le plancher de bruit
exact des trois agrégats n'étant pas encore mesuré dans ce rapport.

**Point doctrinal impératif** : la grandeur §3.2 du contrat doit être **amendée
avant** toute passe runtime. Le runtime actuel est conforme ; le corriger sans
amender le contrat créerait une non-conformité inverse.

---

## 8. Fichiers à modifier dans une future passe (hors de celle-ci)

Ordre d'autorité (contrat d'abord) :

1. `00_documentation_arsenal/contrats/meteo/tendance_temperature.md`
   — amender §3.2 (grandeur de décision : double moyenne au lieu de
   valeur−moyenne), §5.1/§5.2 (méthode retenue + arbitrage), §8 (seuils/fenêtres),
   §10 (attributs d'observabilité : exposer les deux moyennes), §16 (réécrire
   INV-TEND-6 pour autoriser la grandeur « écart entre deux statistiques lissées »).
   Incrémenter la version du contrat.
2. `13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`
   — ajouter la moyenne courte par axe (`..._moyenne_15_min` ou équivalent à
   nommer à l'implémentation, tracé changelog).
3. `12_template_sensors/meteo/tendance/temperature.yaml`
   — remplacer la grandeur de décision (`source − moyenne_60_min` →
   `moyenne_court − moyenne_long`), ajuster `S_in`/`S_out`, mettre à jour triggers
   (écouter la moyenne courte) et attributs d'observabilité.
4. Changelog `v16.x` — tracer le changement de doctrine et les nouveaux
   identifiants (INV-TEND : « toute modification de seuils tracée au changelog »).
5. `contrats/meteo/README.md`, `navigation/domaines/meteo.md` — mise en cohérence
   des renvois si la grammaire de §11 évolue.

**Aucun de ces fichiers n'est modifié dans la présente passe.**

---

## 9. Tests manuels Home Assistant à effectuer avant patch

À exécuter **avant** d'amender, pour mesurer la réalité runtime (le rapport
raisonne sur modèle, pas sur télémétrie réelle) :

1. **Mesure du plancher de bruit.** Sur 24 h température plate, relever
   `min/max` de `sensor.temperature_<axe>` et de `..._moyenne_60_min`
   (Developer Tools → Statistics / History). En déduire l'amplitude de bruit réelle
   par axe ⇒ borne basse acceptable de `S_in`.
2. **Confirmation de la saturation.** Sur un épisode de hausse documenté
   (ex. matinée chambres), tracer simultanément `sensor.temperature_max_chambres`,
   `..._moyenne_60_min` et l'attribut `ecart_c` de
   `sensor.tendance_temperature_max_chambres`. Vérifier que `ecart_c` plafonne
   < 0,4 °C alors que la courbe monte — validation empirique de §4.1.
3. **Test de la grandeur candidate (à blanc, Template Editor).** Dans Developer
   Tools → Template, calculer
   `mean_15min − mean_60min` à partir des historiques et comparer aux seuils
   candidats sur le même épisode — sans créer d'entité.
4. **Vérif indisponibilité.** Forcer une source non numérique (ou observer un
   redémarrage) ⇒ confirmer `indisponible` + `mdi:thermometer-off` (non-régression
   INV-TEND-5).
5. **Vérif anti-scintillement.** Sur une oscillation au voisinage du seuil,
   confirmer que l'hystérésis tient (pas de bascule hausse↔stable à chaque cycle)
   — à revérifier après recalibrage.

---

## 10. Validation de la passe

- **Fichiers inspectés** : §2 (8 entrées, chemins exacts, dépôt cloné depuis
  `github.com/antoinevalentinHA/arsenal`, `main` @ `56e6e5c`).
- **Logique actuelle résumée** : §3 (source instantanée vs moyenne 60 min, seuils
  0,4/0,2, hystérésis `this.state`, `time_pattern /5`, états fermés).
- **Raison la plus probable du faux « stable »** : §4.1 — saturation de l'écart
  `valeur − moyenne 60 min` à `pente × W/2` ; pente minimale détectable ≈ 0,8–1,0 °C/h,
  hors de la plage de confort réelle (0,2–0,6 °C/h).
- **Recommandation de nouvelle doctrine** : §6–§7 — remplacer la grandeur par une
  **double moyenne (courte − longue)** avec hystérésis ; recalibrer `S_in ≈ 0,15`,
  `S_out ≈ 0,08`, `W_court ≈ 15 min` après mesure du bruit.
- **Patch documentaire** : le présent rapport. **Aucune modification YAML, aucun
  patch runtime, aucune correction anticipée** dans cette passe (conforme à la
  consigne : amendement du contrat = passe ultérieure).

---

## Changelog (de ce rapport)

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-06-17 | Audit initial du faux « stable » de la tendance thermique intérieure. Cause racine identifiée : saturation de l'écart instantané vs moyenne 60 min (contrat §3.2). Recommandation : double moyenne + recalibrage, sous amendement contractuel préalable. Lecture seule, aucun runtime modifié. |
