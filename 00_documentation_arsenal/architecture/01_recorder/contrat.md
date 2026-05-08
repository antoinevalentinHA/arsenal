# Arsenal — Contrat Recorder Home Assistant

## Objectif

Définir un usage strict, minimal et maîtrisé du Recorder.

Le Recorder est un socle fonctionnel nécessaire, un outil d'analyse, et un vecteur majeur de visibilité indirecte (logbook). Il n'est ni un logger, ni un dump système.

> Le recorder n'est pas une source de vérité complète. Il est une projection volontairement réduite et gouvernée du système.

---

## Principe fondamental

> Toute entité enregistrée doit être utile **et** acceptable en lecture.

Chaque entité doit satisfaire les deux conditions :

**1. Utilité temporelle** — *"Cette donnée est-elle utile à relire dans le temps ?"*

**2. Acceptabilité logbook** — *"Est-ce que j'accepte de voir cette donnée apparaître dans l'activité ?"*

Le Recorder assure le stockage ; le Logbook assure la narration. Le Recorder constitue une source majeure d'alimentation des vues temporelles de Home Assistant et, en pratique, du logbook visible à l'utilisateur — sans relation exclusive ni garantie d'exhaustivité dans un sens ou dans l'autre. Toute entité recordée est susceptible d'apparaître dans l'activité ; toute entité bavarde devient une nuisance UX. Le Recorder doit donc être conçu comme un filtre de visibilité. Le choix d'inclusion engage simultanément performance, lisibilité et qualité du journal.

❌ Si une seule réponse est `non` → exclusion, **sauf contrainte technique avérée**.

**Contrainte technique avérée** = exclusion du recorder provoquant une perte fonctionnelle observée, une perte statistique observée, l'indisponibilité d'une carte / helper / dashboard effectivement utilisé, ou une régression documentée d'un usage Arsenal existant. Une compatibilité théorique ou un usage futur hypothétique ne constituent pas une contrainte avérée.

**Exception assumée** : les entités Population A peuvent générer du bruit logbook. C'est un coût accepté, documenté, non maîtrisable sans casser la fonctionnalité.

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
| `platform: statistics` | L'entité **source** de chaque capteur `platform: statistics` actif | Sans historique de la source, la fenêtre glissante ne peut pas être reconstruite après redémarrage ou purge — le capteur statistics opère sur une fenêtre tronquée sans signal explicite |

**Règle** : ces entités sont listées explicitement dans la configuration, taguées `# OBLIGATOIRE — contrainte HA`, et non soumises au filtre discrétionnaire.

> ⚠️ La Population A ne peut pas s'étendre librement. L'appartenance à cette population doit rester exceptionnelle, justifiée par dépendance réelle et active, et ne peut pas servir à contourner les exigences de la Population B. Une entité compatible avec une contrainte HA mais non utilisée reste en Population B.

> ⚠️ `platform: statistics` et `history_stats` relèvent de la même catégorie de dépendance recorder : dans les deux cas, la fonctionnalité dépend de l'historique enregistré de l'entité source. L'absence d'enregistrement de la source dégrade silencieusement la fenêtre temporelle sans erreur visible.

---

### 🎯 Population B — Discrétionnaires Arsenal

Toutes les autres entités. C'est ici que s'applique le contrat strict.

#### ✅ Éligibles

| Catégorie | Exemples |
|---|---|
| Données physiques | Température, humidité, CO₂, pression — variation lente ou interprétable |
| États métier stables | Modes globaux, états consolidés, décisions finales (pas intermédiaires) — voir contraintes de fréquence et de cardinalité ci-dessous |
| Marqueurs structurants | Timers significatifs, input_datetime métier, début/fin de cycle (peu fréquents) |

**Contrainte de cardinalité** : tout état métier eligible doit présenter une cardinalité finie, explicitement énumérable et stable dans le temps. Sont autorisés : les états binaires (`on`/`off`, `true`/`false`), les ensembles finis de modes nommés (`home`/`away`/`sleeping`, `eco`/`comfort`/`boost`), les codes d'état à valeurs fixes et documentées. Sont exclus : tout état à valeur textuelle libre ou semi-libre, tout état dont le nombre de valeurs possibles n'est pas borné par conception, toute valeur numérique continue non agrégée.

#### ❌ Non éligibles

| Catégorie | Exemples |
|---|---|
| Technique / pipeline | Capteurs intermédiaires, routage, états transitoires |
| Trop fréquents | Capteurs dépassant le seuil de fréquence défini ci-dessous |
| Debug / introspection | Raisons calculées, états verbeux, messages explicatifs |
| Helpers techniques | input_number de travail, input_text technique, booléens internes |
| UI | Entités purement visuelles |
| Cardinalité non bornée | Texte libre, valeurs continues non agrégées, états à valeurs illimitées |

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
   → vérifier le critère de fréquence (→ voir seuil opposable)
   → vérifier le critère de cardinalité (→ voir contrainte de cardinalité)
   → non-conformité sur l'un ou l'autre : exclusion ou transformation

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

Une entité utile mais incompatible avec le recorder (fréquence, instabilité, verbosité, cardinalité non bornée) ne doit pas être enregistrée telle quelle.

Elle doit être remplacée par une entité dérivée stable :

- **agrégation métier** — valeur résumée sur une fenêtre temporelle
- **état consolidé** — décision finale après réconciliation
- **trigger conditionnel** — enregistrement uniquement sur événement significatif
- **sentinel** — état figé représentatif
- **marqueur d'événement** — horodatage de transition, pas d'état continu, fréquence faible et contrôlée

> Une donnée utile mais bruyante doit être transformée, jamais tolérée brute.

---

## Seuil de fréquence opposable (Population B)

> Une entité qui change plus de **5 fois par heure** est **présumée non éligible**.

Ce seuil est opposable. Il constitue une présomption d'exclusion, non une règle absolue. La présomption peut être levée uniquement par une **dérogation explicite**, formulée selon le format suivant dans la configuration :

```yaml
# DÉROGATION FRÉQUENCE — [nom entité]
# Fréquence observée : [N] changements/heure (dépasse seuil de 5)
# Justification métier : [raison pour laquelle la fréquence est acceptable]
# Critère d'acceptabilité logbook confirmé : oui
# Validé le : [date]
```

Toute inclusion au-dessus du seuil sans dérogation documentée est réputée non conforme.

---

## Rétention

**Purge activée.** La durée de rétention maximale des données brutes du Recorder est fixée contractuellement à **90 jours**. Toute valeur supérieure est considérée comme une dérive et doit être justifiée explicitement.

L'objectif est la lecture utile sur horizon opérationnel, pas l'archivage. Si un besoin d'historique long terme est identifié, il doit être adressé par les long-term statistics (Population A) ou par un outil dédié, pas par extension de la rétention recorder.

> Les long-term statistics (Population A) ne sont pas affectées par la purge — elles sont stockées indépendamment par HA et ne sont jamais purgées par le Recorder.

---

## Invariant fondamental — Indépendance fonctionnelle

Aucune logique métier d'Arsenal ne doit dépendre du Recorder pour fonctionner.

Le système doit rester intégralement opérationnel :
- en l'absence d'historique enregistré
- après purge complète de la base recorder
- après redémarrage avec base vide

Toute automatisation, script, décision ou calcul métier dont le fonctionnement correct est conditionné à la présence de données dans le Recorder constitue une **violation de cet invariant**.

**Exception strictement encadrée** : les fonctionnalités Population A dépendent structurellement du Recorder par conception HA. Cette dépendance est acceptée, documentée, et ne peut pas être étendue par analogie à d'autres entités ou usages.

> Le Recorder est une projection de l'état du système à des fins d'analyse et de visibilité. Il n'est pas un composant d'exécution. Toute architecture qui en fait un composant d'exécution est incorrecte.

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

## Statut

| Champ | Valeur |
|---|---|
| Type | Contrat opposable |
| Portée | Globale |
| Évolution | Rare, argumentée |