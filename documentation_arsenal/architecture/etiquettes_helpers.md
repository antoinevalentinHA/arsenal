# CONTRAT — Système de labels helpers Arsenal
**Version** : 1.0.1
**Domaine** : Gouvernance / Modèle interne
**Statut** : Normatif

---

## Changelog

| Version | Modification |
|---|---|
| 1.0.1 | Ordre de priorité : pédagogique par défaut, arbitrage exceptionnel uniquement. `helper:context` : cycle de vie borné/réconciliable élevé en invariant dur. Section 12 (ordre de déploiement) déplacée en annexe non normative. |
| 1.0.0 | Version initiale. |

---

## 1. Objectif

Ce contrat définit le système de labels applicable aux entités helpers Arsenal :

- `input_boolean`
- `input_number`
- `input_text`
- `input_datetime`
- `input_select`
- `counter`
- `timer`

Son objet est strictement architectural : distinguer les helpers de gouvernance des helpers purement techniques, éviter la confusion entre décision, paramétrage, mémoire et contexte, améliorer l'audit des couches décision / exécution / remédiation, empêcher qu'un helper critique soit traité comme un simple stockage.

Ce contrat ne régit pas le comportement métier des helpers.

---

## 2. Principe directeur

> **Un helper est classé selon ce qu'il représente, jamais selon son type Home Assistant.**

Un `input_boolean` n'est pas automatiquement décisionnel.
Un `timer` n'est pas automatiquement technique.
Un `input_number` n'est pas automatiquement paramétrage.

La seule question valable est :

> **Quelle est la nature architecturale de la vérité portée par ce helper ?**

---

## 3. Labels définis

Quatre labels. Aucun autre n'est autorisé.

| Label | Rôle |
|---|---|
| `helper:decision` | Vérité de gouvernance ou état d'autorité |
| `helper:parameter` | Réglage opérateur ou paramètre de politique |
| `helper:context` | Contexte d'exécution ou état de session/campagne |
| `helper:memory` | Mémoire technique, trace, compteur, persistance interne |

---

## 4. Définitions normatives

### `helper:decision`

Helper représentant une vérité de gouvernance utilisée pour statuer sur le comportement d'un domaine.

Exemples typiques : mode actif, autorisation, inhibition, blocage métier, état canonique de domaine.

Exemples Arsenal plausibles :
- `input_boolean.mode_confort_chauffage`
- `input_boolean.chauffage_inhibition_geofencing`
- `input_select.chauffage_dernier_mode_decide`

**Invariants :**
- Porte une vérité métier, pas un artefact technique.
- Toute écriture constitue un acte de gouvernance.
- Toute modification exige une revue explicite des automations `signal:decision` et scripts `script:decision` consommateurs.
- Ne doit pas servir de cache, de transit ou de stockage opportuniste.

---

### `helper:parameter`

Helper représentant un réglage opérateur, une consigne de politique ou un paramètre configurable.

Exemples typiques : seuil, offset, durée configurable, plage horaire, consigne opérateur.

Exemples Arsenal plausibles :
- `input_number.clim_offset_on`
- `input_number.meteo_horizon_prevision_heures`
- `input_datetime.clim_heure_blocage_autom_on`

**Invariants :**
- Exprime une politique, une préférence ou un réglage, jamais un état constaté.
- Sa valeur peut être consommée par des décisions sans devenir elle-même décisionnelle.
- Toute mutation automatique d'un `helper:parameter` doit être explicitement justifiée par contrat.

---

### `helper:context`

Helper représentant un contexte temporaire d'exécution, de session, de campagne ou d'armement.

Exemples typiques : pipeline en cours, cycle en cours, session ouverte, verrou de campagne, timer de procédure.

Exemples Arsenal plausibles :
- `input_boolean.ecs_pipeline_en_cours`
- `input_boolean.ecs_cycle_en_cours`
- `timer.reboot_box`

**Invariants :**
- Ne porte pas une décision métier autonome.
- Matérialise un état temporaire de procédure, de flux ou de coordination.
- Peut conditionner des guards ou des exécutions sans devenir une vérité de gouvernance.
- Son cycle de vie doit être explicable, borné et réconciliable après redémarrage. Un contexte permanent, non borné ou non réconciliable est une violation de contrat.

---

### `helper:memory`

Helper servant à la persistance technique interne : mémoire, trace, corrélation, compteur, dernier état connu, résumé figé.

Exemples typiques : compteur de tentatives, request_id, dernière action, résumé de cycle, timestamp mémorisé, dernière valeur figée.

Exemples Arsenal plausibles :
- `input_text.boiler_req_dhw_set_setpoint`
- `input_text.ecs_cycle_last_action_status`
- `counter.reboot_box_tentatives`
- `input_text.ecs_resume_dernier_cycle_fige`

**Invariants :**
- Ne décide rien.
- Conserve une trace ou une donnée technique utile aux autres couches.
- Peut être critique pour la robustesse sans devenir décisionnel.
- S'il commence à représenter une autorisation, un mode ou un blocage métier, son classement est faux.

---

## 5. Règles d'exclusivité

**Un helper porte au maximum un label.**
Le multi-label est interdit.

### Ordre d'arbitrage

L'ordre suivant est pédagogique. Il guide la qualification manuelle et sert de règle d'arbitrage en cas d'ambiguïté résiduelle uniquement. Il ne dispense pas du découpage ni de la qualification manuelle.

```
1. helper:decision
2. helper:parameter
3. helper:context
4. helper:memory
```

### Règle d'interprétation

- Si le helper représente une vérité de gouvernance → `helper:decision`
- Sinon, s'il représente un réglage opérateur → `helper:parameter`
- Sinon, s'il représente un état temporaire de procédure → `helper:context`
- Sinon, s'il persiste une trace ou une mémoire technique → `helper:memory`

---

## 6. Cas limites et résolutions

| Situation | Résolution |
|---|---|
| `input_boolean` utilisé comme verrou de cycle | `helper:context` |
| `input_boolean` représentant un mode métier actif | `helper:decision` |
| `input_number` contenant une consigne opérateur | `helper:parameter` |
| `input_number` contenant une valeur figée post-cycle | `helper:memory` |
| `input_text` contenant un request_id MQTT | `helper:memory` |
| `timer` de watchdog ou de cadence | `helper:context` |
| `counter` de tentatives de remédiation | `helper:memory` |
| `input_select` portant le mode officiel d'un domaine | `helper:decision` |
| `input_datetime` servant de borne horaire paramétrable | `helper:parameter` |
| `input_datetime` servant de timestamp mémorisé | `helper:memory` |

---

## 7. Interdictions formelles

- ❌ Ne pas classer `helper:decision` un helper qui ne représente qu'un verrou technique, une session ou un pipeline
- ❌ Ne pas classer `helper:memory` un helper qui porte une autorisation, un mode ou un blocage métier
- ❌ Ne pas classer `helper:parameter` un helper qui reflète un état constaté du système
- ❌ Ne pas utiliser `helper:context` comme catégorie poubelle pour tout booléen "en cours"
- ❌ Ne pas faire varier le label selon l'automatisation consommatrice
- ❌ Ne pas laisser croire qu'un type HA (`input_boolean`, `timer`, etc.) détermine à lui seul la catégorie

---

## 8. Obligation de tagage

**Tout helper Arsenal doit porter un label.**

Un helper sans label est non classifié et doit être audité.

Cette règle est asymétrique par rapport au contrat sensors, où l'absence de label est une neutralité intentionnelle. Les helpers sont des constructions Arsenal volontaires à forte charge architecturale. Un helper non classé est en pratique une dette ou une ambiguïté.

---

## 9. Gouvernance du tagage

**Le tagage est manuel. C'est la source de vérité.**

Les outils d'audit peuvent : détecter les consommateurs, suggérer une catégorie, signaler des incohérences.

Ils ne peuvent pas : poser un label, corriger un label, arbitrer un cas limite.

La décision finale appartient à l'architecte.

---

## 10. Périmètre d'audit

Priorité d'audit :

1. `helper:decision` — consommateurs connus, autorité métier claire, pas d'usage comme cache technique
2. `helper:context` — cycle de vie borné, réconciliation après redémarrage, pas de confusion avec gouvernance
3. `helper:parameter` — réglage explicite, pas de dérive vers état constaté, mutations automatiques justifiées
4. `helper:memory` — sémantique de trace claire, pas de détournement en décision, horizon de conservation cohérent

---

## 11. Invariants globaux

```
I1 — Un helper porte au maximum un label.
I2 — helper:decision prime en cas d'ambiguïté résiduelle.
I3 — helper:parameter exprime une politique ou un réglage, jamais un état constaté.
I4 — helper:context exprime un état temporaire de procédure à cycle de vie borné et réconciliable. Un contexte permanent, non borné ou non réconciliable après redémarrage est une violation.
I5 — helper:memory conserve une trace ou une persistance technique, jamais une décision.
I6 — Tout helper doit être tagué. L'absence de label est une dette, pas une neutralité.
I7 — Le tagage est manuel. Aucun outil ne peut poser ou corriger un label.
```

---

## Annexe — Guide de déploiement (non normatif)

Ordre conseillé pour un premier tagage Arsenal :

1. `helper:decision` — révèle immédiatement les erreurs de mélange gouvernance/technique
2. `helper:context` — isole les états de procédure mal qualifiés
3. `helper:parameter` — clarifie les réglages confondus avec des états constatés
4. `helper:memory` — classe le reste par élimination

Cet ordre n'est pas contractuel. Il reflète le retour sur investissement d'audit le plus rapide.
