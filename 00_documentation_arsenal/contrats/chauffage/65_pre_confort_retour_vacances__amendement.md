# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — PRÉ-CONFORT RETOUR VACANCES (V3 PRO) · Amendement : subordination de l'effet à l'autorité thermique
#
# 📌 STATUT :
#   AMENDEMENT au contrat de domaine [`65_pre_confort_retour_vacances.md`](65_pre_confort_retour_vacances.md)
#
# 🎯 OBJET :
#   Lever l'ambiguïté établie par l'audit
#   [`audit_pre_confort_vacances_saisonnalite.md`](../../audits/01_rapports/chauffage/audit_pre_confort_vacances_saisonnalite.md)
#   (consigné en `main` par la PR #695) : la règle cardinale de `65` §5
#   (« déclenché exclusivement par une anticipation temporelle de retour,
#   jamais par un seuil thermique ») était lisible comme autorisant la
#   production de `comfort` INDÉPENDAMMENT de l'autorité thermique du
#   domaine chauffage.
#
#   Cet amendement sépare explicitement le DÉCLENCHEMENT du mécanisme
#   (temporel, inchangé) de l'AUTORISATION DE SON EFFET (thermique,
#   désormais opposable), sans créer aucune autorité nouvelle.
#
# 🔒 SUBORDINATION :
#   • [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) (+ amendement)
#   • [`01_doctrine_registres.md`](01_doctrine_registres.md)
#   Opposable à : [`30_decision_centrale.md`](30_decision_centrale.md) ·
#   [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md) ·
#   [`80_table_decision_canonique.md`](80_table_decision_canonique.md)
#   (+ [`réécriture partielle`](80_table_decision_canonique__reecriture_partielle.md))
#   sur la SEULE ligne pré-confort (cf. §6).
#
# ==========================================================

---

## 1. Objet et portée

`65` n'est pas réécrit. Cet amendement précise **un seul point** : ce que le
mécanisme de pré-confort est autorisé à **produire**, une fois sa fenêtre
temporelle ouverte.

Il ne modifie ni la finalité du pré-confort (`65` §2), ni son positionnement
architectural (`65` §3), ni sa subordination à la souveraineté opérateur
(`65` §3bis), ni la détermination de sa fenêtre (`65` §5bis / §5ter), ni ses
garde-fous d'anti-rebond (`65` §7).

**Portée strictement bornée.** Cet amendement ne traite pas — et ne rouvre
pas — l'écart de couche historique `65`/`70` relevé en `#361 §6.3` et
reconfirmé par `#695 §C/T4`. Il n'introduit aucune injection de
`input_boolean.pre_confort_actif_calcule` dans
`sensor.chauffage_autorisation_cible`, et ne crée aucune « autorisation
forcée ». Voir §6.2.

---

## 2. Doctrine — déclenchement ≠ autorisation de l'effet

> **D-PCV-0 — Deux questions distinctes.**
> Le mécanisme de pré-confort répond à la question *« sommes-nous dans la
> période d'anticipation du retour ? »*. Il ne répond pas, et ne doit jamais
> répondre, à la question *« le chauffage est-il thermiquement pertinent
> maintenant ? »*.

La doctrine cible se formule ainsi :

> 🧠 **Le pré-confort est une exception au contexte d'absence Vacances.
> Il n'est pas une exception à la pertinence thermique du chauffage.**

Ou, en termes métier :

> 🧠 **Le retour des occupants justifie l'anticipation du confort,
> mais ne crée pas à lui seul un besoin de chauffage.**

### 2.1 Ce qui reste purement temporel

> **R-65.1 — Déclenchement temporel préservé.**
> La règle cardinale de `65` §5 est **conservée dans son intention
> historique** et s'applique désormais explicitement au seul
> **déclenchement** : la fenêtre de pré-confort, et donc l'état
> `input_boolean.pre_confort_actif_calcule`, sont déterminés
> **exclusivement** par l'anticipation temporelle du retour. Aucun seuil
> thermique ne peut ouvrir, fermer, avancer, retarder ou prolonger cette
> fenêtre.
>
> Le pré-confort ne devient pas un thermostat. Il ne calcule aucun besoin
> thermique, ne lit aucune température, n'applique aucun seuil.

### 2.2 Ce qui devient thermiquement opposable

> **R-65.2 — Autorisation de l'effet subordonnée.**
> La production effective d'une décision `comfort` **au titre du
> pré-confort** est subordonnée à l'autorité thermique existante du domaine
> chauffage. La fenêtre ouverte rend `comfort` **envisageable** ; elle ne le
> rend pas **légitime** à elle seule.

**Lecture corrigée de `65` §5.** La formulation « jamais par un seuil
thermique » ne signifie **pas** — et n'a jamais signifié — « `comfort` est
autorisé indépendamment de l'état de l'autorité thermique ». Elle interdit au
pré-confort de **se déclencher** sur un critère thermique. Elle ne lui confère
aucune immunité thermique sur son effet. Toute lecture contraire est abrogée
par le présent amendement.

---

## 3. Autorité thermique opposable

> **R-65.3 — Autorité unique, consommée et non recalculée.**
> L'autorité de pertinence thermique opposable au pré-confort est
> **exclusivement** :
>
> ```
> sensor.chauffage_autorisation_cible
> ```
>
> Elle est **consommée** par la Décision Centrale, jamais recalculée par
> elle, jamais dupliquée.

**Interdictions corollaires (opposables) :**

- ❌ aucun test direct de température extérieure ou intérieure ailleurs que
  dans `sensor.chauffage_autorisation_cible` ;
- ❌ aucune duplication des seuils `input_number.chauffage_seuil_ext_on` /
  `_off` hors de ce capteur ;
- ❌ aucune garde calendaire fondée directement sur `input_select.saison`
  comme garde primaire de cette règle ;
- ❌ aucune autorité nouvelle de type « saison de chauffe » ;
- ❌ aucun détournement de `binary_sensor.chauffage_autorise_systeme`, qui
  demeure un **hook réservé du registre sécurité** (cf. `30` §4 Niveau 1,
  `30__amendement` R-30.1/R-30.2, `01` D0/D1) et n'a aucun rôle ici ;
- ❌ aucune logique Vacances introduite dans la couche d'autorisation locale
  (`70` §7 intégralement préservé — voir §6.2).

**Pourquoi cette autorité et pas la saison.** `sensor.chauffage_autorisation_cible`
porte déjà la garde extérieure (`ext ≥ chauffage_seuil_ext_off → reduced`) et
la modulation `suspension_relance_meteo` (`70__amendement` R-70.2). Elle est
plus précise qu'un découpage calendaire `Été` / non-`Été`, elle existe déjà,
elle est déjà consommée par la Décision Centrale au Niveau 3a. La retenir
n'ajoute ni entité, ni concept, ni source de vérité.

---

## 4. Règle normative de décision

> **R-65.4 — Règle du pré-confort (opposable, univoque, testable).**
>
> Soit le contexte : `binary_sensor.vacances_actives = on`,
> `input_boolean.pre_confort_actif_calcule = on`, aucune cause de rang
> supérieur active (Niveau 0 override ; Niveau 1 ; sécurités de
> `80…__reecriture` §4.1 ; poêle corroboré au sens `40__amendement`
> D-POELE-1).
>
> L'exception pré-confort **se déclenche si et seulement si** :
>
> ```
> states('sensor.chauffage_autorisation_cible') == 'comfort'
> ```
>
> — égalité stricte sur le jeton canonique.
>
> - **Si elle se déclenche** → décision `comfort`, raison
>   `pre_confort_vacances`.
> - **Si elle ne se déclenche pas** → la règle Vacances s'applique
>   **inchangée** → décision `reduced`, raison `mode_maison_vacances`.

**Aucun mode nouveau, aucun jeton nouveau.** La règle n'introduit ni valeur de
`desired_mode` hors `{comfort, reduced, neutre}`, ni raison hors des 12 jetons
de `30` §10. Le vocabulaire décisionnel est strictement inchangé.

**Le `neutre` n'est pas produit par cette branche.** L'abstention forcée sur
autorisation `neutre` (`80` §8) gouverne le **chemin d'opportunité thermique**
(Niveau 3a, présence réelle). La branche Vacances relève d'un **contexte
imposé** (« sobriété maximale imposée », `80` §4) : lorsque l'exception ne se
déclenche pas, c'est la règle de contexte qui s'applique, non une opportunité
thermique qui s'évalue. Cette distinction est normative.

---

## 5. États non exploitables de l'autorité thermique

> **R-65.5 — Aucun fallback silencieux.**
> `unknown` ≠ `false` ≠ `reduced` ≠ `comfort`. Un état non exploitable de
> `sensor.chauffage_autorisation_cible` n'est **jamais** interprété comme une
> autorisation `comfort`, et n'est **jamais** requalifié en `reduced`.

**Mécanique normative — le test est positif, donc fail-closed par construction.**
R-65.4 n'énumère aucune valeur dégradée et n'applique aucune valeur par
défaut : il exige l'**établissement positif** du jeton `comfort`. En
conséquence, tout état autre — `unknown`, `unavailable`, chaîne vide, jeton
hors `{comfort, neutre, reduced}`, entité absente — laisse simplement la
condition permissive **non établie**.

> **R-65.6 — Distinction impérative.**
> Lorsque l'autorité thermique est non exploitable, la décision `reduced` qui
> s'applique **n'est pas déduite de l'autorité thermique**. Elle est celle que
> le **contexte d'absence Vacances imposait déjà** en l'absence d'exception.
> Le système ne conclut rien sur la thermique : il constate qu'aucune
> exception n'est établie.

C'est cette distinction qui rend la règle conforme à l'interdiction
d'assimilation silencieuse : Arsenal ne transforme pas `unknown` en `reduced`,
il refuse de lever une réduction déjà en vigueur sans preuve positive.

**Cohérence de doctrine.** Ce fail-closed est le même que celui posé par le
chantier C21 côté climatisation — *« toute valeur autre qu'un `on` franc est
traitée comme "pas de préparation" ⇒ le veto tient (fail-closed, sobriété par
défaut, pas de fallback silencieux) »* (I-C21-2 / §3) — et le même que celui
de `66` §*Conditionnement saisonnier*, qui traite explicitement le cas
`unknown`/`unavailable` par abstention tracée.

**Interdiction de forme (opposable au futur runtime) :** la garde ne doit
comporter ni valeur par défaut (`| default('comfort')`, `| default(...)`), ni
filtre de repli, ni énumération de valeurs dégradées, ni négation d'un jeton
(`!= 'reduced'`). Seule l'égalité positive au jeton `comfort` est admise.

---

## 6. Supersessions explicites

Conformément au précédent de `40__amendement` A4 (dont la règle de
comportement remplace les formulations antérieures de `40` **et** de `80`),
le présent amendement abroge nommément les formulations suivantes, **sur la
seule ligne pré-confort**.

### 6.1 Contrat `30` — Décision Centrale

**Abrogé :** `30` §4, Niveau 2, la puce

> « absence effective Vacances (`vacances_actives = on`) → `reduced`,
> **sauf exception normative explicite** : pré-confort retour vacances actif
> (`input_boolean.pre_confort_actif_calcule`) → `comfort` »

**Remplacé par :** R-65.4.

**Inchangé et confirmé :** `30` §4 Niveau 2, phrase suivante — *« La Décision
Centrale est l'unique arbitre du contexte Vacances […] Aucune autre couche
(capteur d'autorisation thermique, miroir de diagnostic) ne porte de logique
Vacances. »* Cet amendement la **renforce** : l'arbitrage reste entier à la
Décision Centrale, qui se contente de lire une autorité qu'elle consommait
déjà.

**Inchangée :** la table des raisons de `30` §10. La sémantique du jeton
`mode_maison_vacances` est étendue de « absence effective Vacances sans
pré-confort » à « absence effective Vacances sans exception pré-confort
**établie** » — ce qui couvre à la fois le pré-confort inactif et le
pré-confort actif mais thermiquement non permis. Aucun renommage.

### 6.2 Contrat `70` — Autorisation thermostat

**Abrogé :** `70` §2, section *« Autorisations forcées amont »*, la puce
`- pré-confort retour vacances.` (l. 88), en tant que le pré-confort y est
rangé parmi les sources d'autorisation forcée soumises à la règle cardinale
*« toute autorisation forcée est strictement équivalente à une autorisation
locale `comfort` »* (l. 92).

**Motif :** cette qualification est doublement caduque. **(a) Factuellement** :
l'audit `#695` établit qu'aucune injection de `pre_confort_actif_calcule` dans
`sensor.chauffage_autorisation_cible` n'a jamais existé au runtime. **(b)
Normativement** : sous R-65.4, le pré-confort est **subordonné** à
l'autorisation locale, non **substitué** à elle — l'exact inverse d'une
autorisation forcée.

**Ce que cette abrogation ne fait pas.** Elle ne résout pas, ne traite pas et
ne rouvre pas l'écart de couche `65`/`70` (`#361 §6.3`), qui **demeure ouvert
et hors périmètre**. Elle n'ajoute aucune autorisation forcée. Elle ne fait
disparaître aucune autre source de la liste (`mode_confort_chauffage`,
inhibition géofencing restent inchangées).

**Renforcé, non modifié :** `70` §7 et sa section *« Neutralité vis-à-vis des
autorisations automatiques »* — l'autorisation locale continue d'ignorer
totalement les vacances, le pré-confort et toute anticipation temporelle. Le
sens de lecture est désormais **univoque et à sens unique** : la couche `70`
produit une intention ; la Décision Centrale la consomme ; le pré-confort n'y
écrit rien. Aucune autre disposition de `70` ni de son amendement n'est
touchée.

### 6.3 Contrat `80` — Table de décision canonique

**Abrogés :**

- `80` §4, **ligne 6\*** de la table des blocages, et son paragraphe
  d'explicitation *« Exception normative Vacances (ligne 6\*) »* ;
- `80…__reecriture_partielle` §4.2, deuxième ligne de la table *« Contexte
  majeur Vacances — effet conditionnel »* (« pré-confort actif → `comfort`
  *(exception normative)* »).

**Remplacés par :** la table canonique de §7 ci-dessous.

**Tension `80` §9 — résolue pour cette ligne.** L'interdiction formelle
*« Confort sans autorisation ❌ — Violation séparation faits / décision »*
(`80` §9 ; `80…__reecriture` §9) et l'exception ligne 6\* étaient en
contradiction apparente, l'exception l'emportant par *lex specialis*. Sous
R-65.4, **la contradiction disparaît** : le pré-confort ne produit plus jamais
`comfort` sans autorisation thermique. L'interdiction §9 redevient vraie sans
réserve **sur cette ligne**.

> ⚠️ **Bornage explicite.** Les autres dérogations à `80` §9 — Niveau 0
> (`mode_confort_chauffage`) et Niveau 3b (inhibition géofencing), qui
> produisent `comfort` sans consulter `sensor.chauffage_autorisation_cible` —
> sont **hors périmètre** de cet amendement et demeurent en l'état. Le présent
> document ne prétend pas rendre `80` §9 universellement vrai.

**Inchangée :** `80` §6, *« Note sur le pré-confort retour vacances »*
(l'exception n'est pas évaluée en régime absence standard). Elle reste
intégralement valide et s'ajoute à R-65.4.

---

## 7. Table canonique de la ligne pré-confort

Contexte commun à toutes les lignes : override opérateur inactif · Niveau 1
inactif · aucune sécurité de `80…__reecriture` §4.1 active · aucun poêle
corroboré.

| `vacances_actives` | `pre_confort_actif_calcule` | `sensor.chauffage_autorisation_cible` | Décision | Raison |
|---|---|---|---|---|
| `on` | `on` | `comfort` | **`comfort`** | `pre_confort_vacances` |
| `on` | `on` | `reduced` | **`reduced`** | `mode_maison_vacances` |
| `on` | `on` | `neutre` | **`reduced`** | `mode_maison_vacances` |
| `on` | `on` | `unknown` / `unavailable` / hors-jeton | **`reduced`** | `mode_maison_vacances` |
| `on` | `off` | `comfort` | **`reduced`** | `mode_maison_vacances` |
| `on` | `off` | `reduced` | **`reduced`** | `mode_maison_vacances` |
| `on` | `off` | `neutre` / non exploitable | **`reduced`** | `mode_maison_vacances` |

**Lecture.** Une seule cellule produit `comfort` : les deux axes doivent être
satisfaits **simultanément** — exception de contexte (`pré-confort actif`)
**et** autorité thermique permissive (`comfort`). C'est la matérialisation des
deux axes exigés : l'exception au contexte Vacances, et l'autorité thermique
toujours opposable.

**Les lignes `pré-confort off` sont inchangées** par cet amendement : elles
rappellent que l'autorité thermique seule ne crée jamais de confort en absence
Vacances (`80` §6). La symétrie est volontaire — aucun des deux axes ne suffit
seul.

---

## 8. Conséquences comportementales assumées

Cet amendement a des effets **au-delà du seul cas estival** qui l'a révélé.
Ils sont énumérés ici pour être assumés explicitement, non découverts plus
tard.

1. **Été / mi-saison douce.** `ext ≥ chauffage_seuil_ext_off` → cible
   `reduced` → pré-confort sans effet. C'est le cas fondateur.
2. **Maison déjà chaude.** `sensor.temperature_min_chambres ≥ consigne + offset_off`
   → cible `reduced` → pré-confort sans effet. Cohérent : il n'y a rien à
   préparer.
3. **Météo favorable.** La modulation `suspension_relance_meteo`
   (`70__amendement` R-70.2) transforme une cible `comfort` en `neutre`
   lorsqu'un réchauffement passif est attendu → pré-confort sans effet.
   **Conséquence nouvelle et voulue** : l'anticipation météo devient opposable
   au pré-confort. Elle ne l'était pas.
4. **Poêle corroboré.** Déjà interdit par `40__amendement` A4 ; désormais
   **également** neutralisé par la cible (`poele → reduced`). Les deux
   mécanismes convergent — l'un ne remplace pas l'autre, aucune règle n'est
   modifiée ici.
5. **Hiver franc, maison froide.** Cible `comfort` → **le pré-confort conserve
   intégralement sa fonction**. La finalité de `65` §2 (réduire la violence
   thermique de la reprise) est préservée dans tous les cas où elle a un sens
   physique.

> **Point d'attention pour l'exploitant.** Le pré-confort devient un mécanisme
> **conditionnel**. Une fenêtre peut s'ouvrir, consommer son droit de cycle
> (`65` §7) et ne produire aucun effet. C'est le comportement voulu : le droit
> de cycle protège contre la répétition, pas contre l'inutilité.

---

## 9. Observabilité — limite connue, matérialisation différée

Sous R-65.4, deux situations distinctes produisent la même raison
`mode_maison_vacances` : *« pas de pré-confort »* et *« pré-confort actif mais
thermiquement non permis »*.

> **R-65.7 — Distinction conceptuelle actée.**
> Ces deux causes sont **conceptuellement distinctes** bien qu'elles
> produisent une décision identique. Toute lecture diagnostique doit
> reconnaître cette distinction.
>
> Sa **matérialisation runtime** (état dédié de `sensor.pre_confort_raison`,
> ou attribut de traçabilité) constitue une **amélioration différée**, **non
> ouverte** par le présent amendement.

Ce traitement est exactement celui réservé à `suspension_relance_meteo`
(`70__amendement` R-70.6) et à `input_boolean.blocage_geofencing` (`60` §8.2) :
distinction normative immédiate, matérialisation différée.

**Interdiction associée (anti-causalité menteuse, `01` D1/D3).** La raison
`pre_confort_vacances` ne doit **jamais** être émise lorsque la décision
produite n'est pas `comfort` au titre de l'exception. Émettre le jeton d'une
exception qui ne s'est pas déclenchée serait une causalité menteuse au sens de
la pathologie D1/D2.

---

## 10. Invariants exposés (CI)

- **INV-PCV-1** — Aucune décision `comfort` n'est produite sous
  (`vacances_actives = on` ∧ `pre_confort_actif_calcule = on`) sans que
  `sensor.chauffage_autorisation_cible` vaille exactement `comfort`.
- **INV-PCV-2** — La garde est une **égalité positive** au jeton `comfort` :
  aucune valeur par défaut, aucun filtre de repli, aucune énumération de
  valeurs dégradées, aucune négation de jeton.
- **INV-PCV-3** — La raison `pre_confort_vacances` est émise **si et seulement
  si** la décision produite est `comfort` au titre de l'exception pré-confort.
- **INV-PCV-4** — L'orchestrateur de pré-confort (fenêtre, timers, mémoire de
  cycle) ne lit **aucune** grandeur thermique et ne consomme pas
  `sensor.chauffage_autorisation_cible` : la fenêtre demeure purement
  temporelle (R-65.1).
- **INV-PCV-5** — La composition de `sensor.chauffage_autorisation_cible` est
  **inchangée** : elle ne lit ni `binary_sensor.vacances_actives`, ni
  `input_boolean.pre_confort_actif_calcule`, ni `input_datetime.fin_vacances`
  (`70` §7 préservé).
- **INV-PCV-6** — La garde thermique est posée **à l'intérieur** de la
  sous-cascade Vacances des deux axes (`desired_mode` et `reason`), et
  **identiquement** sur les deux. Aucune branche de tête n'est ajoutée,
  retirée ni réordonnée : **R-ISO-1 / INV-30-5 restent satisfaits**, la règle
  ne portant pas sur la profondeur des sous-cascades.
- **INV-PCV-7** — Aucune entité, aucun helper, aucun jeton de raison, aucun
  mode décisionnel n'est créé par cette règle.

---

## 11. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) (+ amendement) ·
[`01_doctrine_registres.md`](01_doctrine_registres.md)

**Amende :** [`65_pre_confort_retour_vacances.md`](65_pre_confort_retour_vacances.md) (§4, §5, §6)

**Opposable à :** [`30_decision_centrale.md`](30_decision_centrale.md) (§4 Niveau 2) ·
[`70_autorisation_thermostat.md`](70_autorisation_thermostat.md) (§2, *Autorisations forcées amont*) ·
[`80_table_decision_canonique.md`](80_table_decision_canonique.md) (§4 ligne 6\*, §9) ·
[`80_table_decision_canonique__reecriture_partielle.md`](80_table_decision_canonique__reecriture_partielle.md) (§4.2, §9)

**Cohérent avec :** [`66_adaptation_consigne_vacances.md`](66_adaptation_consigne_vacances.md)
(un mécanisme chauffage lié aux Vacances peut être subordonné à la pertinence
de la période de chauffe) · [`40_blocages__amendement.md`](40_blocages__amendement.md) A4 ·
[`70_autorisation_thermostat__amendement.md`](70_autorisation_thermostat__amendement.md) ·
chantier **C21** climatisation (la préparation du retour neutralise l'absence
et les Vacances, **jamais** la garde de température extérieure).

**Doctrine transverse consolidée par ces trois précédents :**

> 🧠 **Préparation du retour ≠ suppression des gardes physiques propres au
> système concerné.**

**Gouverne directement :** la branche Vacances de la Décision Centrale sur la
ligne pré-confort, et tout futur mécanisme d'anticipation de retour du domaine
chauffage.

---

## 12. Portée et stabilité

Cet amendement précise `65` sans en réécrire la doctrine. Il est structurant,
stable long terme, opposable, et versionné avec `65`.

**Aucun patch runtime n'est ouvert par cet amendement.** La mise en conformité
du runtime constitue un lot distinct, soumis à la garde de re-vérification
**R-30.7** (`30__amendement` §10) : le graphe de dépendances de
`decision_centrale.yaml` est re-vérifié sur le runtime courant avant tout
patch, et le changement de garde est appliqué **identiquement aux deux axes**
`desired_mode` et `reason` (R-ISO-1).

Tant que ce lot runtime n'est pas livré, le runtime demeure **en écart connu
et documenté** avec le présent amendement — écart tracé par l'audit `#695` et
par le présent document, et non par une dérive silencieuse.

# ==========================================================
