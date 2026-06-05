# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — AUTORISATION THERMOSTAT LOGIQUE (V3 PRO) · Amendement : modulation de sobriété météo (suspension_relance_meteo)
#
# 📌 STATUT :
#   AMENDEMENT au contrat pivot `70_autorisation_thermostat.md`
#
# 🎯 OBJET :
#   Contractualiser la modulation météo présente dans le capteur
#   `sensor.chauffage_autorisation_cible`, en tant que modulation
#   de sobriété contextuelle de registre STABILISATION, et lever
#   l'interdiction trop large « ne s'adapte jamais à une
#   anticipation » qui englobait abusivement ce mécanisme.
#
# 🔒 SUBORDINATION :
#   • 00_gouvernance_chauffage.md (+ amendement)
#   • 01_doctrine_registres.md
#   Cohérent avec : 30, 60, 80, 90 (+ leurs amendements/réécritures)
#
# ==========================================================

---

## 1. Objet et portée

Cet amendement précise `70` sur un point : la couche d'autorisation contient,
en sortie du calcul thermique local, une **modulation de sobriété fondée sur
la météo**, désignée canoniquement `suspension_relance_meteo` (cf. `90`).

`70` n'était pas fautif sur le fond — l'autorisation produit une intention,
jamais une décision. Mais sa rédaction interdisait « toute anticipation » de
façon trop large, englobant un mécanisme qu'elle ne visait pas. Cet amendement
distingue les deux natures et contractualise la modulation météo.

---

## 2. Distinction : anticipation temporelle vs modulation contextuelle

> **R-70.1 — Deux natures à ne pas confondre.**
> La couche d'autorisation doit distinguer :
>
> - **l'anticipation temporelle prédictive** (pré-confort retour vacances,
>   stratégies fondées sur des dates ou des horaires de retour) : elle reste
>   **interdite** dans la couche d'autorisation locale, conformément à `70`
>   §7. L'autorisation locale ne connaît jamais les dates, ne prépare jamais
>   un retour, ne s'adapte jamais à un horizon temporel ;
>
> - **la modulation contextuelle instantanée** (météo favorable *au moment
>   présent*) : elle est **autorisée** comme modulation de sobriété, car elle
>   ne repose sur aucune prédiction temporelle, mais sur un fait contextuel
>   instantané.

Cette distinction reformule, sans l'abroger, l'interdiction de `70` §7 :
l'interdiction visait les mécanismes **prédictifs temporels** ; elle ne
s'applique pas à une modulation contextuelle instantanée.

---

## 3. Définition de la modulation `suspension_relance_meteo`

> **R-70.2 — Nature et effet.**
> `suspension_relance_meteo` est une **modulation de sobriété de registre
> stabilisation** (cf. `01` D4), vivant dans la couche d'autorisation, en
> sortie du capteur `sensor.chauffage_autorisation_cible`.
>
> Son effet est strictement borné : lorsqu'une cible d'autorisation `comfort`
> serait produite, mais que la météo favorable rend une relance inutile (un
> réchauffement passif est attendu), la modulation transforme cette intention
> en `neutre`.
>
> Il s'agit d'une **suspension de relance**, non d'une interdiction : le
> système s'abstient (`neutre`) plutôt que d'engager une chauffe rendue
> superflue par le contexte météo.

---

## 4. Bornes strictes de la modulation (invariants de comportement)

> **R-70.3 — Transition unique autorisée.**
> La modulation météo ne peut produire qu'une seule transition :
> `comfort → neutre`. Elle ne peut JAMAIS :
> - produire `reduced` ;
> - dégrader un `neutre` ou un `reduced` existant ;
> - produire une interdiction ou un blocage ;
> - remonter en décision centrale ou en sécurité système.

> **R-70.4 — Dépendances closes.**
> La modulation dépend EXACTEMENT de deux entrées :
> - `input_boolean.chauffage_anticipation_meteo` (activation de la modulation) ;
> - `binary_sensor.meteo_favorable_chauffage` (fait contextuel météo).
>
> Aucune autre entrée n'entre dans cette modulation. Elle ne lit ni date, ni
> horaire, ni horizon prédictif.

> **R-70.5 — Position et subordination.**
> La modulation s'applique en sortie du calcul thermique local, en aval de
> celui-ci et en amont de la Décision Centrale. Elle ne s'applique que si la
> cible locale calculée est `comfort`. Elle reste entièrement écrasable : la
> Décision Centrale demeure souveraine en aval, et toute priorité supérieure
> ignore l'intention produite.

---

## 5. Traçabilité conceptuelle (doctrine immédiate, runtime différé)

> **R-70.6 — Distinction conceptuelle des `neutre`.**
> Un `neutre` issu d'une zone morte thermique (calcul local d'hystérésis) et
> un `neutre` issu d'une `suspension_relance_meteo` sont **conceptuellement
> distincts**, bien qu'ils produisent tous deux une abstention identique pour
> le moteur décisionnel.
>
> Cette distinction est **normative dès maintenant** : toute lecture
> diagnostique ou explicative doit reconnaître que la cause d'un `neutre` peut
> être thermique ou météo.
>
> La **matérialisation runtime** de cette distinction (attribut de traçabilité
> sur le capteur, ou raison dédiée) constitue une **amélioration différée**,
> non ouverte par le présent amendement — exactement comme le traitement
> réservé à `input_boolean.blocage_geofencing` (cf. `60` §8.2). Jusqu'à ce
> chantier, la modulation reste transparente côté runtime mais distincte côté
> doctrine.

---

## 6. Cohérence avec la doctrine des registres

- la modulation météo ne produit qu'une abstention renforcée (`neutre`), jamais
  une sobriété active imposée (`reduced`) : elle reste donc une **stabilisation
  douce**, jamais un blocage (cohérent `01` D0/D4) ;
- elle vit dans la couche autorisation et ne remonte jamais : pas de violation
  D3 ;
- elle ne compose aucun capteur de sécurité : pas de violation D1.

---

## 7. Interdictions explicites

La modulation `suspension_relance_meteo` ne doit JAMAIS :

- produire `reduced` ou une interdiction ;
- s'appliquer à une cible autre que `comfort` ;
- introduire une dépendance temporelle / prédictive ;
- remonter en décision centrale ou composer un capteur de sécurité ;
- être réinterprétée comme une anticipation temporelle.

---

## 8. Invariants exposés (CI)

- **INV-METEO-1** — La modulation météo ne produit que `comfort → neutre` ;
  jamais `reduced`, jamais dégradation de `neutre`/`reduced`.
- **INV-METEO-2** — Dépendances exactes :
  `input_boolean.chauffage_anticipation_meteo` et
  `binary_sensor.meteo_favorable_chauffage` ; aucune autre entrée.
- **INV-METEO-3** — Vit dans `sensor.chauffage_autorisation_cible`, en aval du
  calcul thermique local, en amont de la décision ; ne remonte jamais.
- **INV-METEO-4** — Écrasable : ne s'applique que si la cible locale est
  `comfort` ; la décision centrale reste souveraine.
- **INV-METEO-5** — Distinction conceptuelle `neutre` thermique / `neutre`
  météo actée en doctrine ; matérialisation runtime différée.

---

## 9. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) (+ amendement) ·
[`01_doctrine_registres.md`](01_doctrine_registres.md)

**Utilisé par :** [`30_decision_centrale.md`](30_decision_centrale.md) (consomme l'intention produite)

**Complémentaire de :** [`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md) ·
`80_table_decision_canonique` (+ réécriture partielle) ·
[`90_semantique_thermique.md`](90_semantique_thermique.md) (+ amendement — terme canonique)

**Gouverne directement :** la post-règle de modulation météo du capteur
`sensor.chauffage_autorisation_cible`.

---

## 10. Portée

Cet amendement précise `70` sans en réécrire la doctrine. Il prend effet avec
l'amendement de `90` (qui porte le terme canonique). Aucun patch runtime n'est
ouvert par cet amendement.

# ==========================================================
