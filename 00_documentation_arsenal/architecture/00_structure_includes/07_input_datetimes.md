# Structure — 07_input_datetimes

## Rôle

Déclaration de helpers temporels persistants Home Assistant.

Les `input_datetime` servent à stocker :
- des horodatages de référence,
- des repères temporels,
- des cadres horaires,
- des mémoires événementielles,
- des timestamps transactionnels,
- des bornes de planification,
- des références temporelles de pipeline.

Un `input_datetime` n’effectue aucun calcul temporel.

---

## Doctrine Arsenal

Les `input_datetime` constituent une couche de mémoire temporelle persistante.

Un `input_datetime` est un repère temporel, pas un ordonnanceur.

Ils ne doivent contenir :
- ni logique métier,
- ni calcul temporel,
- ni comportement autonome,
- ni décision.

La signification métier de l’horodatage est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
input_datetime: !include_dir_merge_named 07_input_datetimes/
```

---

## Structure

```yaml
<nom_helper>:
  name: <nom_lisible>
  has_date: <true|false>
  has_time: <true|false>
```

---

## Clés courantes

- name
- has_date
- has_time
- icon
- initial

---

## Typologies Arsenal

Un `input_datetime` peut représenter :

- un horodatage de référence,
- une mémoire événementielle,
- un repère temporel de pipeline,
- une borne de planification,
- une fenêtre horaire,
- une référence transactionnelle,
- une mémoire de fraîcheur,
- un timestamp de diagnostic.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de calcul temporel autonome
- Pas de décision locale
- Pas d’action directe sur un équipement
- Toute écriture automatisée doit être traçable
- Toute signification temporelle doit être explicitement documentée
- Aucun `input_datetime` ne constitue à lui seul une autorité décisionnelle
- Toute utilisation comme déclencheur direct doit être explicitement justifiée

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — INPUT_DATETIME
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Stocker une référence temporelle persistante utilisée
#   par le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   - Mémoire temporelle persistante uniquement
#   - Aucun calcul temporel autonome
#   - Aucune logique métier locale
#   - Aucun comportement autonome
#
# 🔖 NATURE
#   <Horodatage de référence | Mémoire événementielle
#    | Repère de pipeline | Borne de planification
#    | Fenêtre horaire | Référence transactionnelle
#    | Mémoire de fraîcheur | Timestamp de diagnostic>
#
# 📋 MODE
#   has_date: <true|false> — has_time: <true|false>
#
# 🚫 INTERDITS
#   - Confondre mémoire temporelle et décision
#   - Constituer à lui seul une autorité décisionnelle
#   - Écrire sans traçabilité vers l'auteur de l'écriture
#   - Utiliser comme déclencheur direct sans justification explicite
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```