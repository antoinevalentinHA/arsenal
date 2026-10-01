# 🧠 ARSENAL — CONTRAT
## Imprimerie — Surveillance d'ambiance des stocks

**Version** : v2.0.0
**Domaine** : Imprimerie — alerte de dépassement des conditions de stockage
**Date** : 2026-10-01
**Statut** : normatif

---

## 1. Objet

Une **alerte simple et rare** : prévenir quand la température ou l'humidité
relative d'une zone de stockage reste hors plage pendant **24 h d'affilée**.
Rien de plus.

| Zone | Température | Humidité relative |
|---|---|---|
| Stock carton | `sensor.temperature_stock_carton` | `sensor.humidite_relative_stock_carton` |
| Stock produits finis | `sensor.temperature_stock_pf` | `sensor.humidite_relative_stock_pf` |

Sources SwitchBot Cloud, ni définies ni modifiées par ce domaine.

---

## 2. Rôle de Home Assistant

> **SAS-1.** Home Assistant **mesure et alerte**. Il est **hors du système
> qualité** : ni enregistrement, ni preuve, ni indicateur qualité. Toute
> validation qualité est faite séparément, par l'opérateur, hors de ce dépôt.

---

## 3. Règle

> **SAS-2 — Plages (bornes incluses).** Température 10 – 35 °C ; humidité
> relative 30 – 80 %. Écrites dans l'automation ; les changer = modifier ce
> contrat et l'automation dans la même PR.

> **SAS-3 — Alerte.** Une mesure **numérique** strictement hors plage pendant
> **24 h sans interruption** ⇒ **une** notification mobile (parent 1, via
> `script.notification_envoyer`). Un pic bref ne notifie jamais.

> **SAS-4 — Sobriété.** Aucune autre notification : pas de message de
> retour dans la plage, pas d'alerte d'indisponibilité capteur, pas de mode
> essai, aucun helper, aucun template sensor dédié. La surveillance de
> l'intégration SwitchBot Cloud reste portée par
> [`resilience_integrations.md`](../resilience_integrations.md).

> **SAS-5 — Redémarrage (compromis assumé).** Le décompte des 24 h repart à
> zéro à chaque redémarrage ou rechargement des automations : l'alerte peut
> être retardée, jamais inventée.

---

## 4. Implémentation

| Élément | Fichier |
|---|---|
| Automation `10180000000007` | [`11_automations/imprimerie/stock/surveillance_conditions.yaml`](../../../11_automations/imprimerie/stock/surveillance_conditions.yaml) |

ID retiré, jamais réutilisable : `10180000000008` (ancienne automation
d'indisponibilité des mesures, v1.x).

---

## Historique de version

- **v1.0** — création : seuils réglables, mémoire persistante, alarme de
  dépassement prolongé, retour, indisponibilité par capteur, ESSAI.
- **v1.0.1** — correctif du script de notification (champs facultatifs).
- **v2.0.0** — **simplification**, demandée par l'opérateur le 2026-10-01 :
  la v1 produisait des notifications fréquentes (indisponibilité / mesure
  rétablie sur les aléas du cloud SwitchBot) et des avertissements YAML
  « duplicate key » (ancres `<<:` surchargées). Besoin réel : une alerte
  simple et rare. Toute la chaîne v1 (11 fichiers : helpers de paramètres,
  de suivi, d'essai et d'horodatage, 3 fichiers de template sensors,
  2 scripts, automation `10180000000008`) est supprimée ; il reste une
  automation `numeric_state` à 24 h.

---

## Navigation

- [Contrats Imprimerie](README.md)
- [Hub de navigation du domaine](../../navigation/domaines/imprimerie.md)
