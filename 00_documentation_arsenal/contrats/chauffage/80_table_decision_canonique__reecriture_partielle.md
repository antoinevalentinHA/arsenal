# ARSENAL — Contrat Normatif Formel
## Chauffage — Table de Décision Canonique V3 (réécriture partielle)

**Statut :** Contrat normatif formel — spécification ultime de décision — opposable
**Subordonné à :** `00_gouvernance_chauffage.md` · `01_doctrine_registres.md`
**Implémenté par :** `30_decision_centrale.md`
**Complémentaire de :** `40_blocages.md` · `50_standby_hysteresis.md` · `60_absence_inhibition_geofencing.md` · `70_autorisation_thermostat.md`
**Nature de la révision :** réécriture partielle — passage d'une logique d'**ordre** à une logique de **comportement** sur l'axe blocages, en application de la doctrine des registres (D1, D2).

---

## 0. Note de révision (opposable)

Cette révision modifie la **forme** de la table des contextes contraignants,
pas seulement son contenu.

La version antérieure exprimait les blocages sous forme de **rangs**
(ordre 1 à 6, le poêle en rang 5, Vacances en rang 6/6\*). Cette forme
laissait croire que le conflit poêle / Vacances se résolvait par l'ordre
d'évaluation. La doctrine des registres établit qu'il n'en est rien : le poêle
est un mécanisme de **stabilisation** (`01` D4), dont les conflits se résolvent
par la **qualité du signal** (`01` D2), non par le rang.

La table des blocages est donc reformulée en **règles de comportement
opposables**. Les sécurités conservent une dominance d'ordre (elles relèvent
de D1) ; le poêle, mécanisme de stabilisation, est exprimé en termes de
corroboration, ce qui rend son rang relatif à Vacances **indifférent**.

Les sections 5, 6, 7 (tables présence / absence / inhibition) ne sont pas
modifiées par cette révision et demeurent en vigueur.

---

## 1. Objet (inchangé)

Ce contrat définit la table de décision canonique du Chauffage Arsenal :
l'ensemble des cas décisionnels légitimes, leurs états finaux autorisés, les
interdictions explicites, les règles d'abstention, et la cohérence globale du
moteur. Il est la spécification finale opposable du comportement décisionnel.

---

## 2. Principes généraux (précisés)

- la table est évaluée de haut en bas ;
- la première règle applicable est souveraine ;
- toute décision est déterministe ;
- aucun cas implicite n'est autorisé.

**Précision de registre (nouvelle).** L'ordre d'évaluation est un mécanisme de
**sécurité** : il garantit qu'une interdiction de sécurité écrase tout. Il
n'est **pas** l'outil d'arbitrage entre mécanismes de stabilisation. Lorsque
deux mécanismes de stabilisation pourraient entrer en conflit, la résolution
se fait par la **qualité / corroboration du signal**, et l'ordre relatif de
leurs branches est sans effet comportemental.

---

## 3. Axes d'évaluation (inchangés, avec précision poêle)

Les axes demeurent : blocages et contextes contraignants ; régime global
(présence / absence / vacances) ; autorisation thermique locale
(`comfort` / `neutre` / `reduced`) ; sources d'autorisation amont (override
opérateur, inhibition géofencing, pré-confort Vacances) ; état actuel du
programme.

**Précision poêle.** L'axe « poêle actif / mémoire poêle » est désormais lu au
sens de `40` D-POELE-1 : **poêle corroboré** (signature thermique ∧ signal non
thermique). Une signature seule n'arme jamais cet axe au niveau décisionnel.

---

## 4. Contextes contraignants — table de comportement (réécrite)

**Exception souveraine (inchangée) :** lorsque
`input_boolean.mode_confort_chauffage` est actif, la présente section n'est pas
évaluée ; la décision finale imposée est `comfort`, sans contourner les
sécurités matérielles hors périmètre Arsenal.

Hors override opérateur, les règles de comportement suivantes s'appliquent.
Elles sont classées par **registre**, ce qui détermine leur mode de résolution.

### 4.1 Sécurités système — dominance d'ordre (registre sécurité, D1)

Ces causes relèvent de la sécurité système. Elles écrasent toute autorisation
et toute opportunité de confort. Leur dominance par l'ordre est légitime et
maintenue.

| Cause active (sécurité)                       | Décision finale | Justification              |
|-----------------------------------------------|-----------------|----------------------------|
| Chauffage non autorisé système                | Abstention      | Interdiction système       |
| Fenêtre ouverte (avec délai)                  | `reduced`       | Chauffe vers l'extérieur interdite |
| Aération en cours et confirmée                | `reduced`       | Respect inertie / purge    |
| Blocage post-aération actif                   | `reduced`       | Interdiction reprise prématurée |

> `binary_sensor.chauffage_autorise_systeme`, capteur de sécurité système pur
> (cf. `30`, `50`), porte l'interdiction système et le blocage post-aération.
> Il ne porte **aucune** cause de stabilisation.

### 4.2 Contexte majeur Vacances — effet conditionnel (registre sécurité/contexte)

| Contexte                                          | Décision finale | Justification                  |
|---------------------------------------------------|-----------------|--------------------------------|
| Absence effective Vacances (`vacances_actives = on`), pré-confort inactif | `reduced`       | Sobriété maximale imposée      |
| Absence effective Vacances (`vacances_actives = on`), pré-confort actif   | `comfort` *(exception normative)* | Exception bornée au contexte d'effectivité Vacances |

L'exception pré-confort demeure interne à l'absence effective Vacances et soumise à la
validation complète de la Décision Centrale (cf. `40 §6.1`). La projection
`input_select.mode_maison` ne porte plus, à elle seule, l'effet de régime
(cf. `vacances.md` §10).

### 4.3 Poêle — règle de comportement par corroboration (registre stabilisation, D2)

Le poêle n'est plus exprimé comme un rang. Il est exprimé comme une **règle de
comportement fondée sur la corroboration** :

> **Règle POÊLE (opposable).**
> Aucune décision `comfort` n'est émise en présence d'un **poêle corroboré**
> (signature thermique ∧ signal non thermique, cf. `40` D-POELE-1), **y
> compris** dans le contexte Vacances + pré-confort.
>
> Un poêle **non corroboré** (signature seule) ne constitue pas un poêle actif
> et n'a aucun effet décisionnel.

Conséquence formelle : **l'ordre relatif des branches « poêle » et
« Vacances + pré-confort » est indifférent.** Que l'implémentation évalue le
poêle avant ou après Vacances, le comportement est identique dès lors que la
corroboration est respectée. Toute formulation antérieure exprimant une
priorité d'ordre entre poêle et Vacances est abrogée et remplacée par la
présente règle de comportement.

### 4.4 Règles générales (précisées)

- toute autorisation ordinaire est ignorée en présence d'une **sécurité**
  active ou d'un **poêle corroboré** ;
- toute inhibition géofencing est sans effet en présence d'une sécurité active
  ou d'un poêle corroboré ;
- les sécurités système (4.1) sont souveraines par dominance d'ordre en régime
  automatique.

---

## 5. Régime présence — table principale

*(inchangée — demeure en vigueur dans sa version V3)*

---

## 6. Régime absence — table principale

*(inchangée — demeure en vigueur dans sa version V3)*

Rappel de cohérence avec `60` (réécriture séparée) : l'inhibition géofencing
est une régulation de stabilisation hystérésée et réactivable ; son effet
décisionnel n'existe qu'en l'absence de présence réelle, garanti par l'ordre
d'évaluation de la Décision Centrale (présence évaluée avant l'inhibition).

---

## 7. Absence avec inhibition géofencing active

*(inchangée — demeure en vigueur dans sa version V3)*

---

## 8. Cas d'abstention forcée (inchangé)

Abstention obligatoire, hors override opérateur, lorsque : programme actuel
`unknown` ; mode désiré = programme actuel ; autorisation `neutre` ;
anti-rebond actif ; verrou géolocalisation actif.

---

## 9. Cas interdits formellement (précisés au registre)

Les cas suivants demeurent strictement interdits en régime automatique, hors
override opérateur. La justification est désormais explicitée par registre.

| Cas | Interdiction | Registre / justification |
|-----|--------------|--------------------------|
| Confort en Vacances hors pré-confort autorisé | ❌ | Sobriété maximale |
| Confort avec fenêtre ouverte | ❌ | Sécurité — chauffe absurde |
| Confort pendant aération | ❌ | Sécurité — violation inertie |
| Confort avec **poêle corroboré** (préconfort inclus) | ❌ | Stabilisation — anti-empilement |
| Confort sans autorisation | ❌ | Séparation faits / décision |
| Reprise automatique post-blocage | ❌ | Anti-oscillation |
| Maintien confort prolongé en absence | ❌ | Dérive énergétique |
| Confort par pré-confort hors contexte Vacances | ❌ | Exception bornée à Vacances |
| Pré-confort cumulé avec inhibition géofencing produisant un double confort | ❌ | Double confort absence interdit |
| Composition d'un capteur de sécurité par une cause de stabilisation | ❌ | D1 / D3 — inversion de registre |

> **Note sur le poêle non corroboré.** Le cas « confort avec poêle non
> corroboré » n'est plus un cas interdit : un poêle non corroboré n'est pas un
> poêle actif. Cette ligne, présente dans les versions antérieures sous une
> forme absolue, est remplacée par la règle de corroboration.

Lorsque `mode_confort_chauffage` est actif, ces interdictions sont
contournables (choix opérateur explicite, raison `confort_force`, blocages
contournés identifiables) — **à l'exception** des sécurités matérielles hors
périmètre Arsenal.

---

## 10. Règles de transition & stabilité (inchangées)

Toute transition déclenche un anti-rebond ; aucune transition silencieuse ou
sans raison métier ; priorité à la stabilité sur la réactivité.

---

## 11. Invariants canoniques (complétés)

- une seule règle applicable à un instant donné ;
- une seule décision possible ;
- aucun cas implicite ;
- aucune ambiguïté tolérée ;
- **(nouveau)** l'ordre d'évaluation est réservé à la dominance des sécurités ;
  les conflits de stabilisation se résolvent par corroboration, non par rang ;
- **(nouveau)** aucune cause de stabilisation ne compose un capteur de
  sécurité système.

---

## 12. Invariants exposés (CI)

- **INV-TBL-1** — Toute branche `comfort` de la table est gardée par une
  condition excluant : sécurité active, et poêle corroboré.
- **INV-TBL-2** — La table ne contient aucune règle exprimant une priorité
  d'ordre entre poêle et Vacances (la résolution est par corroboration).
- **INV-TBL-3** — Cohérence avec `40` : la lecture « poêle actif » de la table
  correspond exactement à la qualification corroborée de `40` D-POELE-1.

*(Les invariants INV-POELE-1/2, INV-D1/D3 portés par `40` et `01` s'appliquent
également à cette table.)*

---

## 13. Dépendances & portée

**Subordonné à :** `00_gouvernance_chauffage.md` · `01_doctrine_registres.md`
**Implémenté par :** `30_decision_centrale.md`
**Complémentaire de :** `40_blocages.md` · `50_standby_hysteresis.md` ·
`60_absence_inhibition_geofencing.md` · `70_autorisation_thermostat.md`

Cette réécriture partielle est la référence ultime du comportement
décisionnel sur l'axe blocages. Elle est stable long terme, opposable, et
gouverne toute transition de programme chauffage et toute évolution future du
moteur.

# ==========================================================
