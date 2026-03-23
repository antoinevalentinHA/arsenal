# Arsenal — Contrat Recorder Home Assistant

## Objectif

Définir un usage strict, minimal et maîtrisé du Recorder.

Le Recorder est un socle fonctionnel nécessaire, un outil d'analyse, et une surface visible indirecte (logbook). Il n'est ni un logger, ni un dump système.

> Le recorder n'est pas une source de vérité complète. Il est une projection volontairement réduite et gouvernée du système.

---

## Principe fondamental

> Toute entité enregistrée doit être utile **et** acceptable en lecture.

Chaque entité doit satisfaire les deux conditions :

**1. Utilité temporelle** — *"Cette donnée est-elle utile à relire dans le temps ?"*

**2. Acceptabilité logbook** — *"Est-ce que j'accepte de voir cette donnée apparaître dans l'activité ?"*

❌ Si une seule réponse est `non` → exclusion, **sauf contrainte technique avérée**.

**Contrainte technique avérée** = exclusion du recorder provoquant une perte fonctionnelle observée, une perte statistique observée, l'indisponibilité d'une carte / helper / dashboard effectivement utilisé, ou une régression documentée d'un usage Arsenal existant. Une compatibilité théorique ou un usage futur hypothétique ne constituent pas une contrainte avérée.

---

## Principe critique — Coût de visibilité

> Le Recorder est une exposition potentielle dans le logbook.

Toute entité recordée peut apparaître dans l'activité. Toute entité bavarde devient une nuisance UX. Le choix d'inclusion engage performance, lisibilité et qualité du journal.

---

## Deux populations d'entités

### 🔒 Population A — Obligatoires par contrainte HA

Ces entités sont requises soit par une fonctionnalité native active de Home Assistant, soit par une fonctionnalité Arsenal explicitement fondée sur cette dépendance. Les exclure casse un usage réel et constaté. On ne les touche pas. On les documente.

| Contrainte HA | Entités concernées | Pourquoi |
|---|---|---|
| Energy Dashboard | Capteurs `state_class: total` ou `total_increasing` **effectivement déclarés** dans le dashboard | Sans recorder, pas de statistiques, dashboard KO |
| Long-term statistics | Tout capteur `state_class: measurement / total / total_increasing` **effectivement utilisé** | HA compile les stats depuis le recorder |
| `history_stats` | L'entité **source** de chaque helper history_stats actif | Sans historique de la source, le helper renvoie 0 ou N/A |
| `statistics_graph` / `statistics` cards | Entités alimentant ces cards **effectivement déployées** | Dépendance directe aux short-term statistics |

**Règle** : ces entités sont listées explicitement dans la configuration, taguées `# OBLIGATOIRE — contrainte HA`, et non soumises au filtre discrétionnaire.

> ⚠️ La Population A ne peut pas s'étendre librement. L'appartenance à cette population doit rester exceptionnelle, justifiée par dépendance réelle et active, et ne peut pas servir à contourner les exigences de la Population B. Une entité compatible avec une contrainte HA mais non utilisée reste en Population B.

---

### 🎯 Population B — Discrétionnaires Arsenal

Toutes les autres entités. C'est ici que s'applique le contrat strict.

#### ✅ Éligibles

| Catégorie | Exemples |
|---|---|
| Données physiques | Température, humidité, CO₂, pression — variation lente ou interprétable |
| États métier stables à faible fréquence de transition et à cardinalité limitée | Modes globaux, états consolidés, décisions finales (pas intermédiaires) — pas de texte libre, pas de micro-variations, pas de capteurs quasi-continus |
| Marqueurs structurants | Timers significatifs, input_datetime métier, début/fin de cycle (peu fréquents) |

#### ❌ Non éligibles

| Catégorie | Exemples |
|---|---|
| Technique / pipeline | Capteurs intermédiaires, routage, états transitoires |
| Trop fréquents | Capteurs oscillants, variations rapides sans valeur d'analyse |
| Debug / introspection | Raisons calculées, états verbeux, messages explicatifs |
| Helpers techniques | input_number de travail, input_text technique, booléens internes |
| UI | Entités purement visuelles |

---

## Procédure de classification d'une entité

Toute entité candidate au recorder suit obligatoirement la procédure suivante :

```
1. Appartenance Population A ?
   → dépendance réelle et active confirmée
   → OUI : inclusion obligatoire, taguer # OBLIGATOIRE — contrainte HA

2. Évaluer les deux critères fondamentaux :
   → utilité temporelle
   → acceptabilité logbook
   → UN SEUL critère non satisfait : exclusion ou transformation (→ voir section suivante)

3. Les deux critères sont satisfaits :
   → vérifier le critère de fréquence
   → suspicion de bruit : justification obligatoire avant inclusion

4. Inclusion en Population B :
   → documenter la raison d'inclusion dans la configuration
   → voir Exigence de justification
```

---

## Exigence de justification

Toute entité incluse en Population B doit comporter une justification explicite dans la configuration.

Format minimal attendu :
- **rôle métier** de l'entité
- **raison de son inclusion** dans le recorder
- **confirmation implicite** de conformité aux deux critères fondamentaux

Une entité sans justification est réputée non conforme et doit être réévaluée.

---

## Cas des entités bruyantes mais utiles

Une entité utile mais incompatible avec le recorder (fréquence, instabilité, verbosité) ne doit pas être enregistrée telle quelle.

Elle doit être remplacée par une entité dérivée stable :

- **agrégation métier** — valeur résumée sur une fenêtre temporelle
- **état consolidé** — décision finale après réconciliation
- **trigger conditionnel** — enregistrement uniquement sur événement significatif
- **sentinel** — état figé représentatif
- **marqueur d'événement** — horodatage de transition, pas d'état continu, fréquence faible et contrôlée

> Une donnée utile mais bruyante doit être transformée, jamais tolérée brute.

---

## Critère indicatif d'exclusion (Population B)

> Une entité qui change typiquement plus de 3 à 5 fois par heure sans valeur métier directe est **présumée non éligible**.

Ce critère est un signal d'alerte, pas une loi absolue. Une entité peut changer fréquemment et rester légitime si elle est réellement métier. Une entité peu fréquente peut rester non éligible si elle est verbeuse ou sans valeur. La présomption d'exclusion peut être levée par justification explicite.

---

## Règle anti-dérive

Toute inclusion doit pouvoir être justifiée explicitement.

En absence de justification claire :
- l'entité est réputée non éligible
- ou doit être retirée du recorder

Toute extension injustifiée de la Population A est considérée comme une dérive contractuelle.

> Le contrat ne se défend pas par l'intention. Il se défend par la traçabilité des décisions.

---

## Réévaluation

Toute entité du recorder peut être remise en question à tout moment.

Déclencheurs de réévaluation :
- bruit logbook constaté
- inutilité observée
- évolution du système

→ L'entité doit être reclassifiée selon la procédure de classification. Une validation passée ne constitue pas une validation permanente.

---

## Principe de filtrage

**Allowlist stricte** : tout est exclu par défaut. Inclusion explicite uniquement, justification obligatoire.

Les entités Population A font l'objet d'une section `include` dédiée et commentée. Les entités Population B font l'objet d'une section `include` séparée.

---

## Rétention

Purge activée. Durée limitée. Objectif : lecture utile, pas archivage.

> Les long-term statistics (Population A) ne sont pas affectées par la purge — elles sont stockées indépendamment par HA et ne sont jamais purgées.

---

## Relation Recorder / Logbook

Le Recorder assure le stockage ; le Logbook assure la narration. Mais le Recorder influence directement le Logbook — il doit donc être conçu comme un filtre du Logbook.

**Exception assumée** : les entités Population A peuvent générer du bruit logbook. C'est un coût accepté, documenté, non maîtrisable sans casser la fonctionnalité.

---

## Règle d'or Arsenal

> Si une entité dégrade la lisibilité du logbook, elle n'a rien à faire dans le recorder — **sauf si elle est Population A**.

La règle d'or est une reformulation opérationnelle du principe fondamental. Toute interprétation divergente entre les deux est résolue en faveur du principe fondamental.

---

## Statut

| Champ | Valeur |
|---|---|
| Type | Contrat opposable |
| Portée | Globale |
| Évolution | Rare, argumentée |
