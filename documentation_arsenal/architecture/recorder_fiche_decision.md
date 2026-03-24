# Arsenal — Fiche de décision Recorder

---

## ⚡ Flash — Décision en 10 secondes

```
1. Contrainte HA réelle et active ?
   → OUI ──────────────────────────────── INCLURE  [Population A]

2. Acceptable dans le logbook ?
   → NON ──────────────────────────────── EXCLURE

3. Utile à relire dans le temps ?
   → NON ──────────────────────────────── EXCLURE

4. Cardinalité finie (pas de texte libre, pas de valeur continue brute) ?
   → NON ──────────────────────────────── TRANSFORMER

5. ≤ 5 changements / heure ?
   → OUI ──────────────────────────────── INCLURE  [Population B]
   → NON → dérogation justifiée ?
            → NON ─────────────────────── EXCLURE
            → OUI ─────────────────────── INCLURE  [Population B — dérogation]

6. Justification documentée dans la config ?
   → NON ──────────────────────────────── NON CONFORME
   → OUI ──────────────────────────────── OK

⚠️  GARDE-FOU — avant toute inclusion :
   Cette entité est-elle lue via son historique
   dans une automation, un script ou une décision métier ?
   → OUI ──────────────────────────────── INTERDIT  (violation de contrat)
   → NON ──────────────────────────────── OK
```

---

## ☑️ Checklist terrain

### Population A
- [ ] Dépendance HA réelle, active, constatée → inclusion automatique

### Population B — 4 critères, tous obligatoires
- [ ] Utile dans le temps
- [ ] Acceptable dans le logbook
- [ ] Cardinalité finie
- [ ] Fréquence ≤ 5 / heure

**4 / 4 → INCLURE · Sinon → EXCLURE ou TRANSFORMER**

---

## 🔥 Règle radicale

> Si ça pollue → ça dégage  
> Si c'est flou → ça dégage  
> Si c'est verbeux → ça dégage  
> Si c'est fréquent → ça dégage  
> Sinon → ça reste

---

## 🔁 Données utiles mais non éligibles — TRANSFORMER

Ne pas inclure brute. Créer une entité dérivée :

| Problème | Solution |
|---|---|
| Valeur trop fréquente | moyenne / min / max sur fenêtre temporelle |
| État verbeux ou texte libre | état consolidé à cardinalité finie |
| Valeur continue non agrégée | agrégation métier ou sentinel |
| Changement sans valeur d'analyse | marqueur d'événement (timestamp de transition) |

> Une donnée utile mais bruyante doit être transformée, jamais tolérée brute.

---



### Inclusion standard — Population B

```yaml
# RECORDER — Population B
# Rôle      : [rôle métier de l'entité]
# Utilité   : [ce qu'on relit dans le temps]
# Logbook   : acceptable
# Cardinalité : finie — [exemples de valeurs]
# Fréquence : ≤ 5/h
```

### Inclusion obligatoire — Population A

```yaml
# RECORDER — Population A — OBLIGATOIRE contrainte HA
# Contrainte : [energy dashboard / history_stats / statistics_graph / long-term stats]
# Entité source de : [helper ou card concerné]
```

### Dérogation fréquence — Population B

```yaml
# RECORDER — Population B — DÉROGATION FRÉQUENCE
# Fréquence observée : ~[N]/h (dépasse seuil de 5)
# Justification métier : [raison explicite]
# Logbook   : acceptable
# Validé le : [YYYY-MM-DD]
```

---

## Référence contrat

| Règle | Valeur opposable |
|---|---|
| Seuil de fréquence | > 5 changements/heure → présomption d'exclusion |
| Rétention maximale | 90 jours |
| Cardinalité | Finie, énumérable, stable — texte libre interdit |
| Filtrage | Allowlist stricte — tout exclu par défaut |
| Population A | Dépendance réelle et active uniquement |
| Logique métier | Aucune dépendance au Recorder autorisée |

---

*Fiche opérationnelle — Arsenal Recorder Contract*
