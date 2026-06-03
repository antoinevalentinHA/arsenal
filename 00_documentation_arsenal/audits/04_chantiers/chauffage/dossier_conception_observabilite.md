# 🧩 ARSENAL — DOSSIER DE CONCEPTION
## Observabilité de l'auto-ajustement de la courbe de chauffe

| Champ | Valeur |
|---|---|
| **Type** | Dossier de conception (décisions amont) |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Conception — clôture des points ouverts CR-1…CR-10 |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Amont figé** | `architecture/.../observabilite_auto_ajustement_courbe.md` ; `architecture/.../revue_architecturale_...md` |
| **Aval** | Contrat `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` (à rédiger après ce dossier) |
| **Cadre** | Aucun YAML, aucun code, aucun runtime, aucun contrat rédigé — décisions de conception uniquement |

> **But du dossier :** transformer l'architecture en spécification constructible, et répondre à : *« reste-t-il une décision structurante non tranchée avant l'écriture du contrat 76 ? »*

---

# 1. Résolution des points ouverts (CR-1 à CR-10)

Chaque point est **tranché** : rappel → options → compromis → décision → justification.

### CR-1 — Cardinalité de l'identifiant de corrélation
- **Problème.** Un cycle quotidien produit jusqu'à deux applications (pente, parallèle), chacune avec son identifiant d'exécution boiler. Relation un-à-plusieurs non résolue.
- **Options.** (a) un seul identifiant = celui d'exécution ; (b) identifiant **de décision** par cycle, parent de 0..2 exécutions ; (c) identifiant par (cycle × paramètre).
- **Compromis.** (a) ne sait pas représenter un cycle refusé/abstenu (aucune exécution) ni grouper pente+parallèle. (c) perd le regroupement de cycle, pourtant la maille naturelle du superviseur. (b) représente tout cycle, y compris sans exécution.
- **Décision.** **(b)** — un **identifiant de décision** émis une fois par cycle quotidien, parent ; chaque application porte (identifiant de décision, paramètre, identifiant d'exécution) où l'identifiant d'exécution **réutilise l'existant boiler** (aucun système d'identifiant parallèle).
- **Justification.** La question du superviseur est par cycle ; refus/abstentions doivent être représentables sans exécution ; la réutilisation de l'identifiant boiler évite la redondance (R-REDOND-2).

### CR-2 — Valeur effective : inférée ou mesurée
- **Problème.** « Confirmée par acquittement » ≠ « relue sur l'appareil ».
- **Options.** (a) trajectoire sur valeur intentionnelle brute ; (b) sur intentionnel-confirmé ; (c) sur effectif-mesuré (relecture appareil).
- **Compromis.** (a) inclut des écritures rejetées/timeout → faux. (c) idéal mais suppose un signal de relecture de la **courbe** dont l'existence n'est pas acquise. (b) toujours disponible et fiable.
- **Décision.** Trajectoire = **intentionnel-confirmé par défaut**. Si un signal de relecture de courbe existe, le **promouvoir** en effectif-mesuré, l'historiser en canal séparé, et exposer un **indicateur de divergence** confirmé↔mesuré. Si absent, étiqueter explicitement la trajectoire « intentionnel confirmé » et consigner la limite : un changement externe au boiler est invisible.
- **Justification.** Ne jamais faire confiance à une valeur non acquittée ; ne jamais nommer « effectif » un simple « envoi confirmé ». Conception robuste aux deux cas (détail §3).

### CR-3 — Couture avec le diagnostic chauffage existant
- **Problème.** Métriques de régulation existantes : référencées en place ou réimportées ?
- **Décision.** **Référencées en place.** L'observabilité **lit** oscillation / overshoot / cycles comme entrées externes de sa couche effet ; elle ne les recalcule pas. Dépendance déclarée ; indisponibilité gérée sans faux zéro.
- **Justification.** Éviter deux sources de vérité pour la qualité de régulation (R-REDOND-1). Le coût (une dépendance) est acceptable et déclaré.

### CR-4 — Effet : unité d'attribution
- **Problème.** Ajustements chevauchants → attribution par ajustement impossible.
- **Décision.** Unité de supervision = **fenêtre régime** (multi-jours, appariée au régime : froid pour la pente, global pour le parallèle), restreinte aux **jours apprenants représentatifs**. La **cohorte** d'ajustements de la fenêtre est un contexte, jamais un score individuel. Effet lu **après délai de stabilisation** (détail §5).
- **Justification.** C'est le plafond honnête : tendance au niveau fenêtre, jamais oracle par ajustement (R-FONC-1). Constructible.

### CR-5 — Budget d'observabilité
- **Problème.** « Additif/read-only » présenté comme gratuit ; coût réel (base, événements, recompute) non borné.
- **Décision.** Budget à trois niveaux (indispensable/souhaitable/rejeté, §6) + principe de volume : **privilégier les événements (épars, à changement) aux capteurs scrutés haute fréquence**, et les **agrégats long terme** aux séries brutes.
- **Justification.** L'observabilité a un coût ; on le borne par conception (R-SUR-OBS-1/2).

### CR-6 — Complétude
- **Problème.** Indéfinissable pour les événements continus.
- **Décision.** Complétude restreinte au **flux périodique du cycle quotidien** (cadence attendue ~1/jour → jour manquant = trou détectable). Les événements continus (suggestion modifiée) ne sont pas soumis à complétude.
- **Justification.** La complétude exige une cadence de référence ; seul le cycle quotidien en a une.

### CR-7 — Typage nominal/anomal & persistance
- **Problème.** Une cause nominale brève est saine ; persistante, elle ne l'est plus.
- **Décision.** Garder le tag **nominal/anomal statique par événement** (fait immuable) **et** ajouter une dimension **persistance/fréquence** dérivée : une cause nominale qui dépasse un seuil de durée/récurrence lève un drapeau séparé « **nominal persistant → à surveiller** ». On ne re-type jamais l'événement.
- **Justification.** Sépare le fait (cet événement était nominal) de la préoccupation émergente (nominal mais installé).

### CR-8 — Modèle de rétention
- **Problème.** Besoin saisonnier vs Recorder ~30 jours.
- **Décision.** Trois classes de conservation (détail §4) : **court terme détaillé** (~30 j, événements bruts) ; **long terme agrégé** (≥ saison, séries à faible cadence ~1/jour) ; **perdable** (haute fréquence intra-journalière).
- **Justification.** Ce qui franchit la frontière saisonnière est **à faible cadence et agrégé** → pas de gonflement ; aucune modification globale de la politique Recorder forcée (R-DETTE-1 + R-SUR-OBS-1).

### CR-9 — Cycle de vie en simulation
- **Problème.** Une décision simulée n'a ni application, ni acquittement, ni effet.
- **Décision.** Cycle simulé **explicitement tronqué** : `suggéré → décision simulée {appliquerait / refuserait / s'abstiendrait}` puis arrêt. Marqué `mode = simulation`, **exclu** de : trajectoire, effet, complétude des cycles réels, drapeaux d'anomalie d'exécution. Vue « ce qui se serait passé » optionnelle et séparée.
- **Justification.** La simulation répond aux questions « proposé/décidé/pourquoi », jamais à « appliqué/effet ». Troncature propre.

### CR-10 — Séquencement doctrine vs local
- **Problème.** Écrire `76` puis le refactorer sous une doctrine transversale → churn.
- **Décision.** **Local d'abord, doctrine extraite ensuite.** Rédiger `76` **autosuffisant** après ce dossier ; structurer sa grammaire générique en **sections délimitées mappant 1:1 la future doctrine**, pour une extraction mécanique une fois ECS confirmé (cf. note de généralisation, « confirmer avant de canoniser »).
- **Justification.** Ne pas bloquer le build chauffage sur une doctrine qui exige un second domaine ; éviter la canonisation prématurée ; la délimitation rend le refactor futur trivial (R-DOC-1).

---

# 2. Modèle de corrélation (synthèse CR-1)

Hiérarchie à trois niveaux, suffisante pour reconstruire tout événement sans ambiguïté :

```
CYCLE (identifiant de décision, 1/jour)
 ├─ contexte d'entrée complet (snapshot)
 ├─ PARAMÈTRE = pente
 │    └─ issue ∈ { appliqué → (identifiant d'exécution boiler → acquittement)
 │                | refusé(raison) | abstenu(cause) }
 └─ PARAMÈTRE = parallèle
      └─ issue ∈ { appliqué → (identifiant d'exécution boiler → acquittement)
                 | refusé(raison) | abstenu(cause) }
```

- **Granularité de corrélation : le cycle.** L'identifiant de décision est la clé maîtresse ; le paramètre est la sous-clé ; l'identifiant d'exécution (existant) est la feuille, **présent uniquement pour les applications**.
- Un cycle refusé/abstenu existe pleinement (identifiant de décision + contexte), **sans feuille d'exécution**.
- Tout événement référence l'identifiant de décision → reconstruction non ambiguë du cycle complet.

---

# 3. Valeur effective (synthèse CR-2)

Trois notions distinctes, rôles tranchés :

| Notion | Définition | Observée | Historisée | Trajectoire |
|---|---|---|---|---|
| **Intentionnelle** | Valeur que le domaine a voulu appliquer | oui (transitoire) | non (seule l'issue compte) | non |
| **Intentionnelle confirmée** | Valeur au moment de l'acquittement `applied` | **oui** | **oui (toujours)** | **oui (référence par défaut)** |
| **Effective mesurée** | Relecture de la courbe sur l'appareil | oui **si signal disponible** | oui (canal séparé) si disponible | **promue référence si disponible** |

Règles :
- La trajectoire de dérive se construit **exclusivement** sur des valeurs **confirmées appliquées** (jamais sur des écritures rejetées/timeout).
- Si l'effectif-mesuré existe : il devient la référence de trajectoire, et un **indicateur de divergence** confirmé↔mesuré est exposé (détecte un changement externe).
- Sinon : la trajectoire est **étiquetée « intentionnel confirmé »** et la limite (cécité aux changements externes) est consignée — **pas de promesse d'effectif non tenue**.

---

# 4. Modèle de rétention (synthèse CR-8)

Politique de conservation par **classe de donnée**, sans implémentation :

| Classe | Contenu | Conservation | Raison |
|---|---|---|---|
| **Court terme détaillé** (~30 j) | Événements bruts du cycle de vie, contexte complet, issues d'exécution | Recorder existant | Analyse fine récente, post-mortem |
| **Long terme agrégé** (≥ 1 cycle saisonnier) | Trajectoire confirmée de la courbe (~1/jour), erreurs lissées journalières, taux de jours apprenants, compteurs d'ajustements par sens, agrégats d'effet par fenêtre régime, transitions de représentativité | Stockage long terme à faible cadence | Voir la dérive/affaissement saisonnier ; faible volume car ~1/jour |
| **Perdable** | Événements « suggestion modifiée » haute fréquence, snapshots redondants, détail intra-journalier des écarts (déjà sources des stats existantes) | Non conservé au-delà du court terme | Seul leur résultat journalier porte du sens |

**Principe directeur :** ce qui franchit la frontière saisonnière **doit être à faible cadence et agrégé**. Les variables de décision (courbe confirmée, erreur journalière, registre d'ajustements) sont nativement ~1/jour → conservables une saison **sans gonflement**. Le détail coûteux reste court terme. Aucune modification de la politique Recorder globale n'est requise.

---

# 5. Effet — unité d'analyse (synthèse CR-4)

- **Mesurable :** au niveau **fenêtre régime** (apparié froid/global, jours apprenants représentatifs uniquement) — la **tendance** de l'erreur lissée et des métriques de régulation, mise en regard de la **trajectoire confirmée** de la courbe sur la même fenêtre. Formulation type : *« sur la fenêtre F en régime R, l'erreur a-t-elle tendu vers 0 pendant que la courbe évoluait dans le sens D ? »* — une **corrélation de fenêtre**.
- **Non mesurable :** l'effet causal d'un **ajustement isolé** (« le +0,1 du jour N a amélioré le confort de X »). Exclu par construction.
- **Unité de supervision retenue :** la **fenêtre régime**, la cohorte d'ajustements servant de contexte.
- **Délai de stabilisation :** l'effet d'une cohorte n'est lu qu'après une fenêtre de stabilisation **≥ horizon de réponse thermique du bâtiment**. Valeur exacte **non figée ici** (calibrable seulement une fois l'observabilité en place) ; défaut conservateur de plusieurs cycles, marqué **paramétrable**. Règle absolue : ne jamais lire l'effet dans une fenêtre encore en cours de stabilisation.

---

# 6. Budget d'observabilité (synthèse CR-5)

| Niveau | Éléments |
|---|---|
| **Indispensable** | Événement de cycle (contexte + corrélation) ; issues appliqué/refusé/abstenu typées ; issue d'exécution ; trajectoire confirmée ; registre d'ajustements ; indicateur de complétude (cycle) ; taux de jours apprenants |
| **Souhaitable** | Indicateur de convergence par fenêtre régime ; compteur de réversions ; drapeau « nominal persistant » ; indicateur de divergence confirmé↔mesuré (si relecture dispo) ; vue simulation |
| **Rejeté** | Historisation longue des suggestions haute fréquence ; multiplication d'indicateurs non rattachés aux critères d'acceptation ; recalcul de métriques de régulation déjà existantes ; scoring d'effet par ajustement |

**Principe :** tout indicateur doit se rattacher à un **critère d'acceptation** (§7). Sans rattachement → rejeté.

---

# 7. Critères d'acceptation (liste fermée, opposable)

À la fin du chantier, pour toute période, un superviseur **doit** pouvoir répondre — et **seulement** à ceci :

1. **Quelles valeurs le système a-t-il proposées**, et quelle erreur les a motivées ?
2. **Qu'a décidé le système** à chaque cycle (appliqué / refusé / abstenu, par paramètre et par sens) ?
3. **Pourquoi** (raison typée nominal/anomal + contexte d'entrée complet) ?
4. **Quelle valeur la chaudière a-t-elle confirmé appliquer** (intentionnel-confirmé ; effectif-mesuré si disponible), et l'application a-t-elle réussi (acquittement) ?
5. **Comment la régulation a-t-elle évolué** après les ajustements, **au niveau fenêtre régime** (tendance, jamais score par ajustement) ?
6. **La courbe a-t-elle dérivé** dans le temps (trajectoire confirmée sur ≥ une saison) ?
7. **La trace est-elle complète** sur la période, et quels cycles furent **gelés / non apprenants** ?
8. **Un état nominal s'est-il installé durablement** au point de devenir suspect (gel persistant, refus récurrent) ?

Cette liste est **fermée** : aucun composant d'observabilité ne se justifie hors d'elle.

---

# 8. Préparation du contrat futur « 76 »

Répartition du contenu, sans rédiger le contrat :

| Destination | Contenu |
|---|---|
| **Contrat `76` (local, opposable)** | Liste fermée des événements obligatoires *chauffage* ; vocabulaire fermé des raisons *chauffage* (typées) ; contexte minimal obligatoire ; les **8 critères d'acceptation** ; politique de rétention par classe ; définition de la trajectoire (intentionnel-confirmé, promotion conditionnelle) ; unité d'effet (fenêtre régime) ; invariants locaux (read-only, étanchéité, no-causal) |
| **Conception (reste ici, non contractuel)** | Analyses de compromis ; options écartées ; **valeurs paramétriques provisoires** (délai de stabilisation, seuils de persistance) tant que non calibrées par les données ; registre de décisions |
| **Doctrine transversale (futur)** | Grammaire générique : corrélation parent/enfant ; triade intentionnel/confirmé/mesuré ; refus vs abstention ; nominal/anomal + persistance ; complétude sur flux périodique ; pipeline étanche ; cadre des questions. **Extraite de `76` après confirmation ECS** |

---

# 9. Réponse à la question finale

> **« Après ce dossier, reste-t-il une décision structurante non tranchée avant l'écriture du contrat 76 ? »**

**Non.** Toutes les décisions **structurantes** sont tranchées : modèle de corrélation (CR-1), sémantique de la valeur effective et base de trajectoire (CR-2), couture diagnostic (CR-3), unité d'effet (CR-4), budget (CR-5), périmètre de complétude (CR-6), persistance (CR-7), politique de rétention (CR-8), cycle simulation (CR-9), séquencement doctrine (CR-10).

Ne subsistent que **deux items non structurants**, qui **ne bloquent pas** `76` :

- **Paramètres calibrables a posteriori** — le délai de stabilisation et les seuils de persistance ne peuvent être fixés qu'une fois l'observabilité productrice de données (problème d'amorçage assumé). `76` les nomme comme **paramètres à défaut conservateur**, pas comme inconnues bloquantes.
- **Un fait à vérifier, non une décision** — l'existence d'un signal de relecture de la courbe (CR-2). La conception est **robuste aux deux cas** (défaut intentionnel-confirmé ; promotion si disponible) ; `76` spécifie les deux chemins. Aucune décision n'en dépend.

**Conclusion :** le chantier peut entrer en **phase contrat**. `76` est rédigeable immédiatement sur la base de ce dossier ; l'implémentation suivra le contrat ; les deux paramètres se calibreront pendant la phase de validation. Aucune décision structurante ne reste ouverte.

---
*Dossier de conception — 2026-06-03. Décisions amont closes. Prochaine étape : rédaction du contrat `76`.*
