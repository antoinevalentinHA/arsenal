# Dossier de conception — Lot L6
## Observabilité auto-ajustement courbe — Couche effet (fenêtre régime)

| Champ | Valeur |
|---|---|
| **Type** | Dossier de conception de lot (détaillé) |
| **Lot** | **L6** (phase **P6** du plan d'action) — *uniquement* |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Conception de lot — aucune implémentation |
| **Version** | 1.0 |
| **Date** | 2026-07-02 |
| **Amont figé** | `76_…md` (§3 Q5, §10 INV-4) ; `plan_action_…md` (P6) ; `dossier_conception_observabilite.md` (CR-3, CR-4) ; lots **L1–L5** livrés |
| **Cadre** | Lecture seule. Aucun YAML, code ou patch. Aucun document figé rouvert. **L7 à L9 non traités.** |

> **Objet :** spécifier, sans implémentation, la **couche effet** — répondre à la question opposable **Q5** (« comment la régulation a-t-elle évolué après les ajustements ? ») **au seul niveau fenêtre régime**, en **tendance bornée**, jamais comme un score causal par ajustement isolé (INV-4). C'est la couche **la moins confiante et la plus dépendante** ; elle est construite **en dernier** pour en cadrer les limites une fois le reste stable (plan §2). L'effet ne juge pas la décision : il l'éclaire, sous réserve.

---

## 1. Périmètre exact du lot L6

**Inclus (L6) :**
- **Unité d'effet = fenêtre régime** (CR-4) : apparier l'effet au régime (froid pour la **pente**, global pour le **parallèle**), restreint aux **jours apprenants représentatifs**.
- **Corrélation de fenêtre** (INV-4) : mettre en regard, sur une fenêtre, la **tendance de la qualité de régulation** (erreur lissée + métriques existantes) et la **trajectoire confirmée** de la courbe (dérive L5) — une **corrélation directionnelle**, jamais un oracle par ajustement.
- **Référencement en place** des métriques de régulation (CR-3) : l'effet **lit** oscillation / overshoot / cycles / erreur ; il ne les **recalcule pas** ; indisponibilité gérée **sans faux zéro**.
- **Délai de stabilisation** : l'effet n'est lu qu'après une fenêtre de stabilisation ≥ horizon de réponse thermique — paramètre à défaut conservateur (CR-4, conception §5).
- **Bornage explicite** de la sur-promesse (limites affichées) + persistance faible-cadence + extension de la **garde d'étanchéité** (liste fermée + allowlist).

**Explicitement hors L6 (différé) :**
- Tout **score d'effet par ajustement isolé** — **exclu par construction** (INV-4, R-FONC-1).
- **Dashboard / logbook de supervision** (assemblage lisible des 8 réponses) → **L7**.
- **Validation de conformité globale + calibration** des paramètres (délai de stabilisation, seuils) → **L8**. Clôture → **L9**.
- Toute **modification du comportement** de l'auto-ajustement ou des métriques de régulation (INV-1, CR-3).

---

## 2. Rappel de frontière (P5 déjà tranchée) et apport de L6

- **L5** a dérivé les **grandeurs propres de la courbe** (dérive nette, réversions, persistance) — *la courbe a-t-elle bougé, et comment ?* (Q6/Q8).
- **L6** met ces grandeurs **en regard de la régulation** — *après qu'elle a bougé, la régulation a-t-elle tendu à s'améliorer, au niveau fenêtre régime ?* (Q5). C'est **le seul maillon** qui touche aux métriques de régulation.
- La frontière est **non ambiguë** : L5 ne lit aucune métrique de régulation ; L6 les lit **en place** (CR-3) et ne les recalcule jamais.

---

## 3. Concept 1 — Unité d'effet : la fenêtre régime (CR-4)

### 3.1 Décision : apparier effet et régime
- **Problème.** Un effet global mélange des contextes thermiques hétérogènes ; les ajustements chevauchants rendent l'attribution par ajustement impossible.
- **Décision.** L'unité est la **fenêtre régime**, **appariée** :
  - **pente ↔ régime froid** (la pente agit d'abord par temps froid) → signal d'erreur `…_froid` ;
  - **parallèle ↔ régime global** (le parallèle décale toute la courbe) → signal d'erreur global.
  La fenêtre est **multi-jours**, restreinte aux **jours apprenants représentatifs** (statut L4 `apprenant` + représentativité REPRESENTATIF).
- **Justification.** C'est le **plafond honnête** (CR-4) : une tendance au niveau fenêtre, jamais un oracle par ajustement. Constructible sur les signaux régime existants.

### 3.2 Cohorte, pas ajustement
- La **cohorte** d'ajustements d'une fenêtre est un **contexte**, jamais un score individuel. L6 n'attribue aucun effet à un `decision_id` isolé.

---

## 4. Concept 2 — Signal d'effet référencé en place (CR-3)

### 4.1 Décision : lire, ne pas recalculer
- **Décision.** L6 **référence en place** les entités déjà historisées :
  - **erreur lissée** : `sensor.ecart_consigne_instantane_froid` (pente) et `sensor.ecart_consigne_instantane` (global) — proxys de qualité de suivi de consigne ;
  - **qualité de régulation** (contexte secondaire) : `amplitude_oscillation_cycle_*`, `amplitude_overshoot_arret_*`, `duree_overshoot_arret_*`, `nombre_cycles_*`, `duree_cycle_moyenne_*`.
  Aucune de ces grandeurs n'est **recalculée** ; L6 en dérive seulement des **tendances de fenêtre**.
- **Justification.** Évite deux sources de vérité (R-REDOND-1, CR-3). Le coût (dépendance déclarée) est acceptable.

### 4.2 Indisponibilité sans faux zéro
- **Décision.** Si un signal de régulation est indisponible (`unknown`/`unavailable`) sur la fenêtre, l'effet correspondant est **`indetermine`**, **jamais `0`** ni « amélioration ». Une absence de données n'est **pas** une absence d'effet.

---

## 5. Concept 3 — Corrélation de fenêtre & délai de stabilisation (INV-4)

### 5.1 Formulation opposable
- L'effet répond, par fenêtre régime, à : *« sur la fenêtre F en régime R, l'**erreur** a-t-elle **tendu vers 0** pendant que la **courbe** évoluait dans le sens D ? »* — une **corrélation directionnelle** à trois valeurs : **`amelioration`** / **`degradation`** / **`indetermine`**.
- **Décision.** L'effet croise deux tendances de la même fenêtre : le **sens de dérive** de la courbe (L5) et la **tendance de l'erreur lissée** (§4). `amelioration` si l'erreur tend vers 0 ; `degradation` si elle s'en éloigne ; `indetermine` si le signal manque, la fenêtre est trop courte, ou la tendance est sous un seuil de bruit.

### 5.2 Délai de stabilisation — règle absolue
- **Décision.** L'effet d'une cohorte n'est lu qu'**après** une fenêtre de stabilisation **≥ horizon de réponse thermique du bâtiment**. Valeur **non figée** (calibrable seulement une fois l'observabilité en place — CR-4/§5) ; **défaut conservateur de plusieurs cycles**, marqué **paramétrable**. **Règle absolue : ne jamais lire l'effet dans une fenêtre encore en cours de stabilisation.**

### 5.3 Jamais causal par ajustement (INV-4)
- L6 **n'affirme aucun** lien causal entre un ajustement donné et une amélioration. Le résultat est une **tendance de fenêtre corrélée**, présentée comme telle. C'est le point de sur-promesse que L6 **borne en le construisant en dernier** (plan §2, §5.risques).

---

## 6. Concept 4 — Bornage de la sur-promesse (limites explicites)

- **Décision.** Chaque indicateur d'effet **porte ses limites** en attribut/étiquette :
  - `niveau = fenetre_regime` (jamais par ajustement) ;
  - `nature = correlation` (jamais causalité) ;
  - `confiance` réduite si peu de jours apprenants, fenêtre courte, ou stabilisation incomplète ;
  - régime et fenêtre de référence explicités.
- **Justification.** INV-4 + budget §6 (« effet borné »). Un effet non qualifié serait une sur-promesse ; l'étiquetage rend la limite **lisible et opposable** (prépare la supervision L7).

---

## 7. Concept 5 — Étanchéité (INV-2, extension de la garde L5)

- **Décision.** Les dérivés d'effet **lisent** des métriques de régulation (entrées externes) et la trajectoire L5 ; ils **ne réentrent jamais** dans la décision. La **garde d'étanchéité** (`check_chauffage_courbe_etancheite_contracts.py`, livrée en L5) est **étendue** : les nouvelles entités d'effet rejoignent la **liste fermée**, et le(s) fichier(s) consommateur(s) d'effet rejoignent l'**allowlist**.
- **Justification.** Maintient INV-2 **opposable et bloquant** au fur et à mesure que la couche s'étend — cohérent avec la doctrine (la garde échoue si un dérivé d'effet est lu par la décision).

---

## 8. Persistance L6 (rétention, CR-8)

Miroir faible-cadence des blocs P3/P4/P5 (Population B) :

| Entité L6 (logique) | Classe | Cadence | Raison |
|---|---|---|---|
| Effet pente (régime froid) — corrélation directionnelle + confiance | **IMPORTANT** | fenêtre (rare) | Q5 requêtable a posteriori |
| Effet parallèle (régime global) — idem | **IMPORTANT** | fenêtre (rare) | Q5 requêtable a posteriori |

- Agrégats de **fenêtre** → nativement à faible cadence, conservables une saison **sans gonflement** (CR-8). Les signaux de régulation **restent référencés en place** (déjà historisés) — L6 n'en duplique aucun.

---

## 9. Critères de validation du lot L6

| # | Critère | Preuve attendue |
|---|---|---|
| V1 | **Niveau fenêtre régime** | L'effet n'est exposé qu'au niveau fenêtre régime ; **aucun** score par ajustement (INV-4) |
| V2 | **Appariement régime** | Pente ↔ erreur régime froid ; parallèle ↔ erreur globale (CR-4) |
| V3 | **Référencement en place** | Les métriques de régulation sont **lues**, non recalculées (CR-3) |
| V4 | **Pas de faux zéro** | Un signal indisponible donne `indetermine`, jamais `0`/`amelioration` (CR-3) |
| V5 | **Délai de stabilisation** | Aucun effet lu dans une fenêtre non stabilisée ; défaut conservateur, paramétrable |
| V6 | **Limites affichées** | Chaque effet porte `niveau=fenetre_regime`, `nature=correlation`, `confiance` |
| V7 | **Read-only / étanchéité** | Aucune entité lue par la décision n'est écrite par L6 ; garde d'étanchéité **étendue** et **mutation-testée** (INV-1/INV-2) |

La validation **fonctionnelle globale** (8 questions) reste **L8**. L6 livre la capacité de **Q5**, **bornée**.

---

## 10. Risques de régression

| ID | Risque | Prob. | Impact | Maîtrise |
|---|---|---|---|---|
| RR-1 | Effet interprété comme **causal par ajustement** | Moyenne | **Élevé** | INV-4 : niveau fenêtre uniquement ; `nature=correlation` ; construit en dernier (**V1/V6**) |
| RR-2 | **Faux zéro** sur signal manquant | Moyenne | Élevé | `indetermine` jamais `0` (**V4**) |
| RR-3 | Lecture d'effet en **fenêtre non stabilisée** | Moyenne | Moyen | Délai de stabilisation, règle absolue (**V5**) |
| RR-4 | **Recalcul** d'une métrique déjà existante | Faible | Moyen | Référencement en place (CR-3, **V3**) |
| RR-5 | Un dérivé d'effet **relu par la décision** | Faible | Élevé | Garde d'étanchéité étendue (**V7**) |
| RR-6 | Sur-confiance sur **peu de jours apprenants** | Moyenne | Moyen | `confiance` réduite ; restriction jours apprenants représentatifs |
| RR-7 | Paramètres (délai, seuils) non calibrés | Moyenne | Faible | Défauts conservateurs, **paramétrables**, calibrés P8 |

---

## 11. Démonstration de respect du contrat 76

| Obligation 76 | Contribution de L6 |
|---|---|
| §3 Q5 (évolution de la régulation) | **Satisfait, borné** : tendance de fenêtre régime, avec limites |
| §10 INV-4 (effet au niveau régime, jamais causal isolé) | **Respecté** : corrélation de fenêtre, `nature=correlation` |
| CR-3 (couture diagnostic, référencement en place) | **Respecté** : métriques lues, non recalculées ; indisponibilité gérée |
| CR-4 (unité d'attribution = fenêtre régime, délai de stabilisation) | **Satisfait** : appariement pente↔froid / parallèle↔global, stabilisation |
| §9/§10 INV-2 (étanchéité) | **Maintenu** : garde d'étanchéité étendue (Concept 5) |
| §3 Q6/Q8 | **Déjà couverts** (L5) — L6 s'y adosse sans les redériver |
| §11 Validation globale | **Non traité** (L8) — L6 fournit V1–V7 locaux |

L6 **n'introduit aucun concept** hors contrat ; il réalise la couche **effet**, la plus prudente, en dernier.

---

## 12. Démonstration INV-1, INV-2 et INV-4

**INV-1 — Read-only.** L6 **ne rouvre pas** `auto_ajustement.yaml` ; il dérive depuis l'historique (métriques de régulation existantes + trajectoire L5) via des capteurs/consommateurs distincts. Aucune entité écrite par L6 n'est une entrée de décision (V7).

**INV-2 — Étanchéité.** Sens unidirectionnel `capture → persistance → dérivation → effet`. Aucune grandeur L6 ne réentre dans la décision ; la frontière reste **opposable et bloquante** via la garde étendue (Concept 5, V7).

**INV-4 — Effet au niveau régime.** L'effet est **exclusivement** une **tendance de fenêtre régime** (V1/V2), **corrélation** et non causalité (V6), lue seulement après **stabilisation** (V5). Aucun effet n'est affirmé pour un ajustement isolé — la sur-promesse est **bornée par construction**.

---

## Rattachement

- **Réalise :** le lot **L6** (phase P6) du plan d'action, au service du contrat `76` (§3 Q5, §10 INV-4 ; CR-3/CR-4) — volet effet de l'écart **É-9**.
- **Diffère explicitement :** L7 (supervision/dashboard/logbook), L8 (validation globale + calibration), L9 (clôture).
- **Ne rouvre :** aucun document figé ; s'adosse à L5 (trajectoire) et aux métriques de régulation existantes, sans les modifier.
- **Lecture seule :** aucune entité créée, aucun fichier modifié par ce dossier ; fichiers vérifiés sur HEAD courant.

*Dossier de conception L6 — 2026-07-02. Couche effet (fenêtre régime) uniquement. Aucun patch, aucun YAML, aucun code.*
