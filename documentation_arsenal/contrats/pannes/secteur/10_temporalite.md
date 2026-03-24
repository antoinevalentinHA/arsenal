# ⏱️ Arsenal — Temporalité de la résilience électrique

**Version :** 1.0  
**Compatible :** Arsenal v6+  
**Statut :** Document normatif actif

**Historique :**
- v1.0 : création — durées de confirmation entrée/sortie de panne secteur

---

## 🎯 Objet

Ce document définit les **durées de confirmation normatives** utilisées pour la qualification des transitions d'état de panne secteur.

Il est référencé comme document NORMATIF par le contrat socle :

`/documentation_arsenal/contrats/resilience_electrique/00_panne_secteur_socle.md`

Toute durée de confirmation non issue de ce document est invalide.

---

## ⏱️ Durées normatives

### Confirmation d'entrée en panne

| Paramètre | Valeur | Implémentation |
|---|---|---|
| Délai de confirmation | `00:00:30` | Implémentation typique : paramètre `for:` sur trigger `binary_sensor.coupure_secteur` `off → on` |

**Justification :** exclut les micro-coupures et sauts de tension transitoires non significatifs. Une coupure inférieure à 30 secondes n'est pas qualifiée comme épisode de panne.

---

### Confirmation de sortie de panne

| Paramètre | Valeur | Implémentation |
|---|---|---|
| Délai de confirmation | `00:05:00` | Implémentation typique : paramètre `for:` sur trigger `binary_sensor.coupure_secteur` `on → off` |

**Justification :** implémente la monotonicité contractuelle. Garantit que le retour secteur est stable avant clôture de l'épisode. Empêche toute oscillation rapide entre états "panne" et "normal" après rétablissement du secteur. Élimine les faux retours et rebonds post-coupure.

---

## 🔒 Invariants

- Ces valeurs sont les seules durées normatives autorisées pour la qualification de panne secteur.
- Toute modification de ces valeurs constitue une révision normative de ce document et doit être tracée dans l'historique.
- Les automations d'entrée et de sortie de panne doivent référencer ces valeurs. Toute divergence est un écart contractuel.

---

## 🔗 Références

- Contrat socle : `00_panne_secteur_socle.md`
- Automation d'entrée : `ID 1004000000001`
- Automation de sortie : `ID 1004000000002`
