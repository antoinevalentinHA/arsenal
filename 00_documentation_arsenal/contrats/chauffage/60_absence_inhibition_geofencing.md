# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE (RÉÉCRITURE V3 PRO) · CHAUFFAGE — ABSENCE & INHIBITION GÉOFENCING · Régulation de stabilisation thermique en absence
#
# 📌 STATUT :
#   CONTRAT NORMATIF DE DOMAINE — STRATÉGIE THERMIQUE D'ABSENCE
#   NATURE : réécriture intégrale (remplace la version antérieure)
#
# 🔒 AUTORITÉ :
#   Ce document définit le comportement normatif du mécanisme
#   d'inhibition du géofencing du sous-système Chauffage Arsenal.
#
#   Il est OPPOSABLE à toute implémentation : helpers, capteurs de
#   qualification, automatismes de mémoire, lectures par la
#   Décision Centrale.
#
#   Subordonné à :
#     • 00_gouvernance_chauffage.md
#     • 00_gouvernance_chauffage__amendement.md
#     • 01_doctrine_registres.md
#
#   Utilisé directement par :
#     • 30_decision_centrale.md (+ amendement)
#
#   Complémentaire de :
#     • 70_autorisation_thermostat.md
#     • 80_table_decision_canonique (+ réécriture partielle)
#
# ==========================================================

---

## 0. Note de révision (opposable)

Cette version **remplace intégralement** la version antérieure de `60`. Elle
corrige des invariants devenus faux à la lumière de la doctrine des registres
(`01`) et de l'objectif métier réel du mécanisme.

**Clauses abrogées de la version antérieure :**

- « une seule activation par cycle d'absence » — **ABROGÉE**. C'était un
  anti-invariant : il empêchait la réactivation légitime lors d'une longue
  absence où la zone froide redescend après une première inhibition. La
  régulation d'absence doit être réactivable.
- « aucune mémoire inter-cycle » au sens absolu — **REFORMULÉE**. Le *capteur
  de qualification* n'a aucune mémoire ; le *helper d'état* matérialise
  l'hystérésis. La distinction de couche est désormais explicite (§4, §6).

**Clauses confirmées et renforcées :**

- finalité = optimisation de la dynamique de reprise + sobriété ;
- exclusion explicite de toute sémantique de sécurité (protection du bâti,
  hors-gel) ;
- subordination stricte à toute priorité supérieure.

---

## 1. Objet du contrat

Ce contrat définit le comportement normatif du mécanisme d'inhibition du
géofencing en régime d'absence.

Il formalise : l'objectif thermique réel du mécanisme, son registre
doctrinal, les rôles respectifs de la qualification thermique et de l'état
mémorisé, la responsabilité du gating absence, les garde-fous de sobriété, et
le statut des helpers associés.

---

## 2. Registre doctrinal et finalité

> **Registre — STABILISATION THERMIQUE** (cf. `01` D4).
> L'inhibition du géofencing est un mécanisme de **stabilisation thermique**.
> Elle n'appartient PAS au registre sécurité système. Elle est subordonnée,
> écrasable, et se résout par hystérésis — jamais par dominance hiérarchique.

**Finalité réelle (confirmée) :**

L'inhibition du géofencing vise exclusivement :

- empêcher qu'une zone froide ne descende trop bas en absence ;
- préserver une inertie thermique exploitable ;
- garantir une reprise en confort **douce et suffisamment rapide** au retour ;
- limiter les appels de puissance violents ;
- éviter le pompage thermique au retour en présence.

> **Exclusion normative explicite (sécurité).**
> L'inhibition du géofencing NE vise PAS, et ne doit JAMAIS viser :
> la protection du bâti, la prévention du gel (hors-gel), la sécurité
> matérielle, la continuité de confort en absence.
>
> Aucune sémantique de sécurité ne peut être introduite dans ce mécanisme.
> Si un hors-gel ou une protection du bâti devenaient souhaités, ils
> constitueraient un **mécanisme séparé, de registre sécurité système**,
> susceptible de composer `binary_sensor.chauffage_autorise_systeme` — et en
> aucun cas une extension de l'inhibition du géofencing. Mélanger les deux
> registres dans le présent mécanisme constituerait une violation de D0/D1.

---

## 3. Positionnement architectural

Le mécanisme :

- s'applique en régime **absence** (gating garanti en aval — voir §5) ;
- ne modifie PAS le régime de référence ;
- ne modifie PAS la hiérarchie métier ;
- ne court-circuite PAS la Décision Centrale ;
- ne pilote JAMAIS directement le matériel.

Il agit exclusivement sur l'**autorisation simulée de confort en absence**,
via la couche d'autorisation définie dans `70`.

### Séparation avec les mécanismes d'anticipation

L'inhibition du géofencing est strictement distincte du pré-confort retour
vacances et de toute stratégie temporelle prédictive. Elle ne connaît jamais
les dates de retour, ne prépare jamais un retour utilisateur, et ne s'active
que par risque thermique immédiat (zone froide). Ces mécanismes sont
architecturalement orthogonaux et ne produisent aucun effet combiné (cf. §7,
et `80` interdiction du double confort absence).

---

## 4. Architecture en deux couches (qualification / état)

Le mécanisme repose sur une séparation stricte de deux couches, conforme à la
doctrine (le capteur qualifie, le helper mémorise).

### 4.1 Couche de qualification thermique — `_requise`

`binary_sensor.chauffage_inhibition_geofencing_requise` est une
**qualification thermique pure** :

- il calcule, par hystérésis, si une inhibition est REQUISE physiquement,
  selon l'écart à la consigne confort et les offsets configurés ;
- il est en **lecture pure** : il ne mémorise rien, n'écrit aucun helper, ne
  décide aucun mode ;
- il ne connaît NI la présence, NI le régime, NI les blocages, NI le matériel.

> **Invariant de pureté.** Le capteur `_requise` ne lit jamais la présence ni
> le régime. Il ne doit jamais être durci pour intégrer une condition de
> régime : le gating absence n'est pas de sa responsabilité (§5).

### 4.2 Couche d'état mémorisé — `chauffage_inhibition_geofencing`

`input_boolean.chauffage_inhibition_geofencing` matérialise l'**état métier**
de l'inhibition :

- il est piloté EXCLUSIVEMENT par l'automation de mémoire d'hystérésis, qui
  reflète fidèlement `_requise` ;
- il constitue la **mémoire d'hystérésis** du mécanisme ;
- il est lu par la Décision Centrale comme un fait, jamais comme une décision.

> **Distinction de mémoire (reformulation de l'ancienne clause).**
> Le *capteur de qualification* n'a aucune mémoire propre. Le *helper d'état*
> est, par nature, une mémoire d'hystérésis. « Aucune mémoire inter-cycle »
> ne s'applique donc qu'à la qualification, jamais à l'état — qui doit
> mémoriser pour porter l'hystérésis.

---

## 5. Gating absence — responsabilité de la Décision Centrale

> **Règle de responsabilité (opposable).**
> Le gating « actif uniquement en absence » n'est PAS porté par le mécanisme
> d'inhibition lui-même. Il est garanti **en aval, par la Décision Centrale**,
> dont l'ordre d'évaluation place la présence réelle avant l'inhibition
> géofencing.
>
> Conséquence : en présence réelle, l'inhibition géofencing est sans effet
> décisionnel, car la branche présence (Niveau 3a) est évaluée et résolue
> avant la branche inhibition (Niveau 3b). L'inhibition n'a d'effet que dans
> le sous-espace « absence réelle, aucune priorité supérieure active ».

Cette délégation est **intentionnelle et opposable** :

- elle préserve la pureté du capteur `_requise` (pas de condition de régime
  dans une qualification thermique) ;
- elle concentre l'arbitrage de contexte dans l'unique autorité décisionnelle.

> **Couplage explicite à surveiller.** Cette propriété dépend de l'ordre des
> branches de la Décision Centrale. Tout futur refactor de cet ordre doit
> préserver l'antériorité de la présence sur l'inhibition, sous peine de
> casser silencieusement la sobriété. Un invariant CI (INV-GEO-3) verrouille
> cette propriété.

---

## 6. Hystérésis & réactivabilité

Le mécanisme est **hystérésé et réactivable**.

- l'entrée en inhibition et la sortie sont gouvernées par deux seuils
  distincts (offsets ON / OFF), garantissant une zone morte anti-battement ;
- le mécanisme peut se **réactiver** autant de fois que nécessaire durant une
  même absence : si la zone froide redescend après une première inhibition et
  sa levée, une nouvelle inhibition est légitime ;
- aucun comptage d'activations, aucun latch par cycle d'absence.

> **Invariant d'hystérésis.** La zone de sortie (OFF) doit être strictement
> plus permissive que la zone d'entrée (ON) : les offsets ne se chevauchent
> pas. Cette non-superposition est la garantie structurelle anti-battement.

---

## 7. Garde-fous de sobriété

- **maintien conditionnel par hystérésis thermique, sans temporisation
  maximale implicite** : l'inhibition ne se maintient que tant que la
  condition thermique reste vraie. La borne effective de l'inhibition est le
  **franchissement de la zone de sortie (OFF)**, pas une durée ;
- hystérésis thermique obligatoire (§6) ;
- anti-rebond obligatoire (porté par la Décision Centrale) ;
- **sortie automatique garantie par l'hystérésis** : dès que la zone froide
  remonte dans la zone OFF (écart au-dessus du seuil de sortie), l'état revient
  automatiquement à l'absence d'inhibition. Aucun maintien ne survit à la
  disparition de la condition thermique ;
- interdiction de maintien prolongé en confort.

> **Note normative — absence de borne temporelle.**
> Le mécanisme ne comporte AUCUNE durée d'inhibition maximale. Cette absence
> est intentionnelle et conforme au runtime : la sortie est garantie par la
> physique (remontée thermique au-dessus du seuil OFF), non par un compteur de
> temps. Aucune promesse de « durée bornée » ne doit être lue dans ce contrat.
>
> Si une borne temporelle explicite devait être souhaitée un jour (p. ex.
> durée maximale d'inhibition indépendante de la température), elle
> constituerait un **mécanisme séparé à contractualiser**, distinct de
> l'hystérésis thermique — et non une réinterprétation du présent mécanisme.

### Interdiction de cumul avec le pré-confort

L'inhibition du géofencing et le pré-confort retour vacances ne peuvent jamais
produire un effet combiné. Aucun pré-confort ne peut prolonger, renforcer ou
être déclenché par une inhibition (et réciproquement). Le double confort
d'absence est interdit (cf. `80` cas interdits formellement).

---

## 8. Statut des helpers associés

### 8.1 `chauffage_inhibition_geofencing` — état normatif

État métier matérialisé, piloté exclusivement par l'automation de mémoire
d'hystérésis (source : `_requise`). Lu par la Décision Centrale. Observable en
diagnostic. **Normatif et opposable.**

### 8.2 `input_boolean.blocage_geofencing` — helper DÉPRÉCIÉ, non normatif

> **Statut : DÉPRÉCIÉ — sans autorité décisionnelle.**
>
> `input_boolean.blocage_geofencing` est un helper **orphelin** : défini et
> exposé en UI de réglages, mais **lu par aucune logique décisionnelle** du
> domaine Chauffage.
>
> Règles cardinales :
> - il ne porte AUCUNE autorité décisionnelle ;
> - il ne doit JAMAIS être considéré comme preuve d'activation ou
>   d'inhibition du géofencing ;
> - il ne doit JAMAIS être lu par la Décision Centrale, un capteur de
>   qualification, ou une automation de mémoire ;
> - aucune nouvelle dépendance ne doit être créée vers ce helper.
>
> Son sort (suppression propre, ou réintégration comme interrupteur maître
> d'activation de l'inhibition) relève d'un **chantier séparé** et n'est pas
> tranché par le présent contrat. Jusqu'à ce chantier, il demeure inerte et
> non normatif.
>
> Ne pas confondre avec `input_boolean.chauffage_inhibition_geofencing`
> (§8.1, état normatif réel) ni avec tout autre helper au vocabulaire proche.

---

## 9. Interdictions formelles

L'inhibition du géofencing ne doit JAMAIS :

- forcer un régime présence ;
- maintenir un confort permanent en absence ;
- court-circuiter une priorité supérieure (sécurité, poêle corroboré,
  Vacances) ;
- introduire une sémantique de sécurité (hors-gel, protection du bâti) ;
- composer un capteur de sécurité système (violation D1) ;
- écrire une consigne ou piloter directement le matériel ;
- intégrer une condition de régime dans le capteur de qualification `_requise`.

---

## 10. Invariants du mécanisme (exposés CI)

- **INV-GEO-1** — Hystérésis cohérente : zone OFF strictement plus permissive
  que zone ON (offsets non chevauchants).
- **INV-GEO-2** — Subordination : l'inhibition est sans effet en présence
  d'une priorité supérieure active (sécurité, poêle corroboré, Vacances).
- **INV-GEO-3** — Gating absence délégué : dans la Décision Centrale, la
  branche inhibition n'est atteignable qu'après résolution de la présence
  réelle (présence évaluée avant inhibition).
- **INV-GEO-4** — Réactivabilité : aucun latch « une seule activation par
  cycle » ; aucune limitation du nombre d'inhibitions par absence.
- **INV-GEO-5** — Pureté de qualification : `_requise` ne lit ni présence ni
  régime ; il ne mémorise rien.
- **INV-GEO-6** — Pas de cumul avec le pré-confort (double confort absence
  interdit).
- **INV-GEO-7** — `blocage_geofencing` n'est lu par aucune logique
  décisionnelle ; aucune dépendance ne pointe vers lui.
- **INV-GEO-8** — Sortie par hystérésis pure : la chaîne d'inhibition ne
  comporte aucun timer, delay ou durée maximale ; la sortie OFF dépend
  exclusivement du franchissement du seuil thermique de sortie.

---

## 11. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) ·
[`00_gouvernance_chauffage__amendement.md`](00_gouvernance_chauffage__amendement.md) · [`01_doctrine_registres.md`](01_doctrine_registres.md)

**Utilisé par :** [`30_decision_centrale.md`](30_decision_centrale.md) (+ amendement)

**Complémentaire de :** [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md) ·
`80_table_decision_canonique` (+ réécriture partielle)

**Gouverne directement :**
- `binary_sensor.chauffage_inhibition_geofencing_requise` (qualification) ;
- `input_boolean.chauffage_inhibition_geofencing` (état) ;
- l'automation de mémoire d'hystérésis associée ;
- les capteurs de seuils de zone froide.

**Déclare déprécié (non normatif) :** `input_boolean.blocage_geofencing`.

---

## 12. Portée et stabilité

Ce contrat est stratégique dans l'architecture Chauffage, stable long terme,
modifié uniquement lors d'évolutions majeures, versionné explicitement, et
opposable à toute implémentation.

Il constitue la **stratégie officielle anti-pompage et de confort différé en
absence du Chauffage Arsenal V3 PRO**, de registre **stabilisation thermique**.

# ==========================================================
