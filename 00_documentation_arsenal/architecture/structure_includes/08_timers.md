# Structure — 08_timers

## Rôle

Déclaration de temporisateurs persistants Home Assistant.

Les `timer` servent à représenter :
- des fenêtres temporelles,
- des délais d’attente,
- des bornes de fonctionnement,
- des échéances de pipeline,
- des cadres temporels transitoires,
- des temporisations de protection,
- des contextes temporels d’orchestration.

Un `timer` ne prend aucune décision.

---

## Doctrine Arsenal

Les `timer` constituent une couche de contexte temporel transitoire.

Un `timer` définit une fenêtre temporelle, pas une action.

Ils ne doivent contenir :
- ni logique métier,
- ni comportement autonome,
- ni pilotage matériel,
- ni décision locale.

La signification métier de l’état temporel est définie ailleurs :
automatisations, scripts, templates ou contrats.

---

## Include

```yaml
timer: !include_dir_merge_named 08_timers/
```

---

## Structure

```yaml
<nom_timer>:
  name: <nom_lisible>
  duration: "HH:MM:SS"
  restore: <true|false>
```

---

## Clés courantes

- name
- duration
- restore
- icon

---

## Typologies Arsenal

Un `timer` peut représenter :

- une fenêtre temporelle,
- un délai de protection,
- une échéance de pipeline,
- une borne de fonctionnement,
- une temporisation anti-rebond,
- une orchestration temporelle,
- une fenêtre d’autorisation,
- un contexte temporel transitoire.

Le type réel doit être explicité dans l’en-tête du fichier.

---

## Invariants

- Pas de logique métier
- Pas de décision locale
- Pas d’action directe sur un équipement
- L’expiration d’un timer ne constitue pas à elle seule une autorité décisionnelle
- Toute action déclenchée à expiration doit être explicitement portée ailleurs
- Toute utilisation de `restore` doit être justifiée
- Toute durée dynamique doit être explicitement documentée

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — TIMER
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Représenter une fenêtre temporelle utilisée par
#   le système Arsenal.
#
# 🧩 PÉRIMÈTRE
#   Nature de la temporalité :
#   - Délai de protection
#   - Fenêtre d’autorisation
#   - Échéance de pipeline
#   - Temporisation anti-rebond
#
# 📡 SOURCES
#   - Automatisations, scripts ou templates externes
#
# 🚫 INTERDITS
#   - Introduire une logique métier locale
#   - Déclencher directement une action
#   - Confondre temporalité et décision
# ==========================================================
```