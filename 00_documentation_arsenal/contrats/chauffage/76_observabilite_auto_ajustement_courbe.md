# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
## CHAUFFAGE — OBSERVABILITÉ DE L'AUTO-AJUSTEMENT DE LA COURBE DE CHAUFFE

| Champ | Valeur |
|---|---|
| **Statut** | CONTRAT NORMATIF DE DOMAINE — OPPOSABLE |
| **Référence** | `76_observabilite_auto_ajustement_courbe.md` |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Subordonné à** | [`contrats/chauffage/75_auto_ajustement_courbe.md`](75_auto_ajustement_courbe.md) ; [`contrats/chauffage/00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) |
| **Source de conception** | `architecture/chauffage/observabilite_auto_ajustement_courbe.md` ; `…/revue_architecturale_…md` ; `…/conception/dossier_conception_observabilite.md` |
| **Nature** | Norme d'observabilité — **sans implémentation, sans stockage, sans paramètre** |

> Ce contrat définit, de manière **opposable**, les obligations d'observabilité du domaine d'auto-ajustement de la courbe de chauffe. Il permet de **vérifier qu'un système d'observabilité est conforme**. Il ne contient ni implémentation, ni YAML, ni code, ni choix technique, ni stratégie de stockage, ni paramètre de conception — ces éléments relèvent du dossier de conception et lui sont subordonnés.

---

## 1. Finalité

L'observabilité existe pour rendre l'auto-ajustement de la courbe de chauffe **explicable et supervisable a posteriori**.

Le domaine d'auto-ajustement est une calibration supervisée : sa supervision suppose qu'un humain puisse comprendre, sur preuves, ce que le système a proposé, décidé, appliqué, et avec quel effet. En l'absence d'observabilité, cette supervision est revendiquée mais impossible.

L'observabilité **DOIT** permettre :
- de comprendre chaque décision d'ajustement après coup ;
- de constater l'évolution de la courbe dans le temps ;
- de distinguer un silence sain d'une cécité ou d'un gel ;
- de fonder toute appréciation d'efficacité sur des faits, jamais sur des hypothèses.

L'observabilité **NE vise PAS** à corriger, optimiser ou piloter le domaine. Elle observe.

---

## 2. Périmètre

### Appartient au domaine
- La capture, la conservation, la dérivation et la présentation des **faits** du cycle de vie d'un ajustement (proposition, décision, application, acquittement, effet inféré).
- La mise à disposition des **questions opposables** (§3).
- Les **invariants** garantissant que l'observation n'altère jamais la décision (§9, §10).

### N'appartient pas au domaine
- Toute modification du comportement de l'auto-ajustement (logique de décision, garde-fous, bornes, pas, cadence, bande morte).
- Le câblage de la représentativité en verrou décisionnel.
- La couche d'exécution transactionnelle (régie par son propre contrat).
- Les **choix techniques, stratégies de stockage et paramètres** (délai de stabilisation, seuils de persistance) — régis par le dossier de conception.

---

## 3. Questions opposables

Un système d'observabilité conforme **DOIT** permettre de répondre, sur données et pour toute période, à la **liste fermée** suivante — et un composant d'observabilité ne se justifie **que** s'il sert l'une d'elles :

1. Quelles valeurs le système a-t-il **proposées**, et quelle erreur les a motivées ?
2. Qu'a **décidé** le système à chaque cycle (appliqué / refusé / abstenu, par paramètre et par sens) ?
3. **Pourquoi** (raison typée nominal/anomal + contexte d'entrée complet) ?
4. Quelle valeur la chaudière a-t-elle **confirmé appliquer** (intentionnel-confirmé ; effectif-mesuré si disponible), et l'application a-t-elle **réussi** (acquittement) ?
5. Comment la **régulation a-t-elle évolué** après les ajustements, **au niveau fenêtre régime** (tendance, jamais score par ajustement isolé) ?
6. La **courbe a-t-elle dérivé** dans le temps (trajectoire confirmée sur au moins un cycle saisonnier) ?
7. La **trace est-elle complète** sur la période, et quels cycles furent **gelés / non apprenants** ?
8. Un **état nominal s'est-il installé durablement** au point de devenir suspect (gel persistant, refus récurrent) ?

Cette liste est **fermée** et **opposable**. Aucune question hors liste n'est exigible ; aucune observabilité hors liste n'est justifiée.

---

## 4. Traçabilité minimale

Le système **DOIT** rendre **reconstituable** — sans imposer *comment* :

- le **cycle de vie complet** de tout cycle de décision (proposition → décision → issue → exécution) ;
- la **trajectoire des valeurs confirmées appliquées** de la courbe sur au moins **un cycle saisonnier** ;
- le **journal des décisions** (applications, refus, abstentions) avec leur raison ;
- les **épisodes de gel** et le **statut apprenant / non apprenant** de chaque cycle ;
- la distinction entre **intentionnel-confirmé** et **effectif-mesuré** lorsque ce dernier est disponible.

Chaque fait conservé **DOIT** être **autosuffisant** : relisible sans dépendre d'un état runtime ultérieurement écrasé.

---

## 5. Événements obligatoires

Le système **DOIT** produire un fait observable pour chacune des **catégories** suivantes — leur représentation n'est pas imposée :

1. **Cycle évalué** — à chaque cycle, quelle qu'en soit l'issue (y compris abstention et silence nominal), porteur du **contexte minimal obligatoire** (§5.1).
2. **Suggestion modifiée** — à tout changement d'une valeur suggérée.
3. **Ajustement appliqué** — par paramètre.
4. **Ajustement refusé** — par paramètre, avec raison (§6).
5. **Abstention / gel** — par cycle, avec cause (§6).
6. **Issue d'exécution** — résultat d'acquittement et valeur confirmée résultante.
7. **Transition de représentativité** — changement d'état (contexte).
8. **Épisode de gel d'apprentissage** — début / fin et cause.

### 5.1 Contexte minimal obligatoire
Tout fait de **cycle / décision DOIT** porter, au minimum :
- pente et parallèle **courants** ;
- valeurs **suggérées** et leur **erreur source** ;
- état de **représentativité** (en contexte) ;
- état **poêle stable**, **mode maison**, **auto actif** ;
- **mode** (simulation / réel) ;
- **référence de corrélation** (§7).

---

## 6. Raisons obligatoires (vocabulaire opposable, fermé et typé)

Le système **DOIT** qualifier chaque issue par une raison appartenant au **vocabulaire fermé** ci-dessous, chacune portant son type **`nominal | anomal`**. La **représentation** n'est pas imposée. **Refus et abstention NE DOIVENT JAMAIS être confondus.**

### Refus (une suggestion exploitable existait, la décision a décliné)
| Raison | Type |
|---|---|
| `suggestion_identique` | nominal |
| `bande_morte` | nominal |
| `baisse_bloquee_poele` | nominal |
| `hors_domaine` | anomal |

### Abstention / gel (aucun signal à décider)
| Cause | Type |
|---|---|
| `auto_desactive` | nominal |
| `hors_mode_normal` | nominal |
| `gel_apprentissage` (précisant : fenêtre / aération / poele_actif / absence / vacances) | nominal |
| `suggestion_indisponible` | anomal |

### Exécution
| Issue | Type |
|---|---|
| `applied` | nominal |
| `rejected` | anomal |
| `timeout` | anomal |
| `bridge_offline` / `hors_bornes_physiques` / `non_conforme_au_pas` | anomal |

### Annotation non bloquante
- `journee_non_representative` — **informe**, ne refuse jamais, ne verrouille jamais.

Une raison **nominale** ne constitue jamais une anomalie en soi ; sa **persistance** au-delà d'un seuil relève d'un signalement dérivé (§10, INV-8), sans re-typage du fait.

---

## 7. Corrélation

Le système **DOIT** garantir qu'un fait observable est **rattachable sans ambiguïté à son cycle de décision** — sans imposer la mécanique :

- la **maille de corrélation est le cycle** de décision, identifié de manière unique ;
- une **application** DOIT être rattachable à son **issue d'exécution** ;
- un cycle **refusé ou abstenu DOIT** être pleinement représentable **sans** issue d'exécution ;
- la reconstitution d'un cycle complet **NE DOIT** dépendre d'aucune inférence approximative.

---

## 8. Complétude

- Une trace est **complète** sur une période si **tout fait de cycle attendu** y figure.
- La complétude **s'apprécie sur le flux périodique du cycle** (cadence attendue régulière) ; elle ne s'applique pas aux faits continus dépourvus de cadence de référence.
- Un **trou de trace DOIT être distinguable** d'une absence légitime d'ajustement : l'absence de fait « non survenu » et l'absence de fait « non enregistré » ne doivent jamais être confondues.

---

## 9. Séparation runtime / diagnostic

Invariant fondateur : **l'observabilité ne doit jamais influencer la décision.**

- Le flux est **unidirectionnel** : capture → conservation → dérivation → présentation.
- La dérivation (diagnostic) **consomme l'historique** ; elle **NE DOIT** ni rétroagir sur le domaine, ni constituer une entrée de décision.
- **Aucune grandeur dérivée d'observabilité NE DOIT** redevenir une entrée de la cascade de décision.
- L'observabilité **NE DOIT** ni verrouiller, ni retarder, ni altérer une décision.

Toute violation de cette frontière constitue une **rupture de contrat**.

---

## 10. Invariants opposables

- **INV-1 — Read-only.** L'observabilité ne modifie aucun comportement du domaine.
- **INV-2 — Étanchéité.** Aucune grandeur de diagnostic ne redevient entrée de décision (§9).
- **INV-3 — Représentativité = contexte.** L'état de représentativité est une annotation ; il n'est **jamais** promu en verrou décisionnel.
- **INV-4 — Effet au niveau régime.** L'effet s'apprécie en **tendance de fenêtre régime** ; aucun effet n'est affirmé causal pour un ajustement isolé.
- **INV-5 — Distinctions opposables.** Refus ≠ abstention ; nominal ≠ anomal.
- **INV-6 — Trajectoire confirmée.** La trajectoire opposable repose **exclusivement** sur des valeurs **confirmées appliquées** ; le système **NE DOIT** présenter comme « effective » aucune valeur non confirmée (ou non relue sur l'appareil le cas échéant).
- **INV-7 — Pas d'observabilité orpheline.** Tout composant d'observabilité **DOIT** se rattacher à une question opposable (§3).
- **INV-8 — Complétude & persistance.** La complétude s'apprécie sur le flux périodique (§8) ; un état nominal **persistant** DOIT être signalable sans re-typer le fait (§6).

---

## 11. Validation

Un système d'observabilité est **conforme** s'il **permet de démontrer**, sur une période échantillon et sans hypothèse :

1. répondre aux **huit questions opposables** (§3) sur données ;
2. **reconstituer** tout cycle de décision sans ambiguïté via la corrélation (§7) ;
3. **distinguer** cycle apprenant, cycle gelé et trou de trace (§8) ;
4. présenter l'**effet** en tendance de fenêtre régime, avec ses **limites explicites** (§10, INV-4) ;
5. exposer la **trajectoire confirmée** de la courbe sur au moins un cycle saisonnier (§4, INV-6) ;
6. établir que l'**étanchéité** (INV-2) est respectée — aucune grandeur d'observabilité ne nourrit la décision.

La démonstration de ces six points constitue la **preuve de conformité** opposable.

---

## Dépendances contractuelles

- **Subordonné à** : [`75_auto_ajustement_courbe.md`](75_auto_ajustement_courbe.md) (domaine observé), [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md).
- **Référence** : la couche d'exécution (vocabulaire d'acquittement corrélé) ; le dossier de conception (mécaniques, stockage, paramètres — non opposables ici).
- **Vocation transversale** : les sections §6 à §10 constituent une **grammaire générique** délimitée, destinée à être extraite ultérieurement dans une doctrine transversale d'observabilité Arsenal, **après confirmation sur un second domaine** (ECS). Jusque-là, elles font autorité **localement**.

## Portée & stabilité

Contrat **stable**, opposable à toute implémentation d'observabilité du domaine. Les valeurs paramétriques (délai de stabilisation, seuils de persistance) et la stratégie de conservation **ne figurent pas ici** : elles relèvent du dossier de conception et se calibrent en phase de validation, sans rouvrir ce contrat.

# ==========================================================
