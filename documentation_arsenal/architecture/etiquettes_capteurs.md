# CONTRAT — Système de labels capteurs Arsenal
**Version** : 1.0.1
**Domaine** : Gouvernance / Modèle interne
**Statut** : Normatif

---

## Changelog

| Version | Modification |
|---|---|
| 1.0.1 | Recorder sur `decision_input` : obligation → recommandation déléguée au contrat Recorder. `diagnostic` : invariant absolu → reclassement obligatoire si usage décisionnel. `I6` : reformulation pour lever la contradiction avec les proxies stricts. |
| 1.0.0 | Version initiale. |

---

## 1. Objectif

Ce contrat définit le système de labels applicable aux entités de type `sensor` dans Arsenal.

Son périmètre est strictement architectural : navigation, audit, cohérence Recorder/Logbook, traçabilité des décisions. Il ne régit pas le comportement des capteurs.

---

## 2. Labels définis

Quatre labels. Aucun autre n'est autorisé.

| Label | Rôle |
|---|---|
| `sensor:decision_input` | Alimente directement une décision |
| `sensor:diagnostic` | Observabilité, debug, états techniques |
| `sensor:derived` | Transformation métier, non utilisé en décision |
| `sensor:raw` | Représentation directe du réel, sans transformation métier |

---

## 3. Définitions normatives

### `sensor:decision_input`
Tout capteur dont la valeur est consommée par une automation `signal:decision` ou un script `script:decision`.

**Invariants :**
- Prioritaire et exclusif sur tous les autres labels.
- Un capteur dérivé promu en entrée de décision perd le label `sensor:derived` et acquiert `sensor:decision_input`. Les deux labels ne coexistent jamais.
- Toute modification de valeur nominale, d'unité ou de fréquence de mise à jour est un changement de contrat. Elle exige une revue explicite des automations et scripts consommateurs.
- Inclusion dans le périmètre Recorder fortement recommandée, mais laissée à l'appréciation du contrat Recorder.

### `sensor:diagnostic`
Capteur d'observabilité pure : ACK, watchdog, états de bridge, compteurs techniques.

**Invariants :**
- Ne doit pas être utilisé comme entrée de décision.
- Si un capteur `sensor:diagnostic` est utilisé comme condition dans une automation `signal:decision` ou un script `script:decision`, il doit être reclassé en `sensor:decision_input`. L'usage décisionnel implicite est interdit ; l'usage explicite impose le reclassement.
- Exclusion du Recorder admise et recommandée par défaut.

### `sensor:derived`
Capteur issu d'une transformation métier (agrégation, lissage, projection, indicateur intermédiaire) non utilisé en décision.

**Invariants :**
- Incompatible avec `sensor:decision_input`. L'exclusivité est absolue.
- Si un capteur `sensor:derived` est détecté dans une automation `signal:decision`, c'est une violation de contrat. Le label doit être promu ou la consommation supprimée.

### `sensor:raw`
Capteur représentant directement le réel sans transformation métier.

Périmètre :
- ✅ capteur Zigbee, MQTT natif, API
- ✅ template proxy strict (renommage, correction d'unité, cast de type)
- ❌ toute agrégation, lissage, seuil ou logique conditionnelle

**Invariants :**
- La frontière est l'absence totale de transformation métier. Dès qu'une logique est introduite, le label est invalide.
- Un proxy template qui ajoute la moindre condition bascule hors de ce label.

---

## 4. Règles d'exclusivité et de complétude

**Un capteur porte au maximum un label.**
Le multi-label est interdit.

**L'absence de label est une déclaration intentionnelle.**
Un capteur non tagué est neutre : aucun rôle architectural critique, aucun invariant à respecter, aucun engagement de stabilité, hors périmètre d'audit obligatoire.

L'absence de label n'est pas une dette. On ne cherche pas la complétude.

---

## 5. Gouvernance du tagage

**Le tagage est manuel. C'est la source de vérité.**

Les outils d'audit (détection d'usage, analyse de dépendances, graphe de consommation) sont autorisés à formuler des **suggestions uniquement**.

**Interdit :**
- Auto-tagging
- Correction automatique de label

La décision finale appartient à l'architecte. L'intention et la responsabilité architecturale ne sont pas déléguables à un outil.

---

## 6. Périmètre d'audit

Seuls les capteurs tagués entrent dans le périmètre d'audit obligatoire.

Priorité d'audit :
1. `sensor:decision_input` — cohérence consommateurs, stabilité, couverture Recorder
2. `sensor:diagnostic` — absence de consommation décisionnelle implicite
3. `sensor:derived` — absence de consommation décisionnelle, promotion éventuelle
4. `sensor:raw` — conformité frontière (absence de transformation métier)

---

## 7. Invariants globaux

```
I1 — Un capteur porte au maximum un label.
I2 — sensor:decision_input est exclusif et prioritaire sur sensor:derived.
I3 — sensor:diagnostic et sensor:decision_input sont mutuellement exclusifs.
I4 — Un capteur non tagué est neutre intentionnel. L'absence de label n'est pas auditée.
I5 — Le tagage est manuel. Aucun outil ne peut poser ou corriger un label.
I6 — sensor:raw exclut toute transformation métier.
      Les templates proxy stricts (renommage, cast, unité) sont autorisés.
```

---

## 8. Évolution

Tout ajout de label requiert :
- un objectif d'usage explicite documenté
- la mise à jour de ce contrat
- une revue des invariants existants

L'inflation de labels est une violation de l'esprit de ce contrat.