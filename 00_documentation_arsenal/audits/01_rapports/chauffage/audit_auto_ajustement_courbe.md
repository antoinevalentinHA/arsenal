# 🧠 ARSENAL — RAPPORT D'AUDIT
## Chauffage — Auto-ajustement de la courbe de chauffe

| Champ | Valeur |
|---|---|
| **Type** | Rapport d'audit |
| **Domaine** | Chauffage / Auto-ajustement courbe (pente & parallèle) |
| **Statut** | ✅ CLÔTURÉ |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Méthode** | Audit d'architecte sur état réel du dépôt, revue contradictoire itérative |
| **Autorité de référence** | Le dépôt. Le runtime fait foi sur le comportement. |

---

## 1. Contexte

Le sous-système Chauffage Arsenal embarque un mécanisme d'**auto-ajustement de la courbe de chauffe** : il propose puis fige, à cadence lente, des corrections de la **pente** et du **parallèle** de la loi d'eau, à partir des écarts thermiques mesurés, dans l'objectif d'obtenir une température intérieure conforme à la consigne sans intervention humaine.

Cet audit vise à déterminer si ce système est réellement robuste, observable, cohérent métier, et capable de démontrer son efficacité — et non à produire une revue de code.

## 2. Périmètre

**Inclus :** chaîne détection → analyse → suggestion → décision → application → exécution de la courbe ; capteurs d'écart et de proposition ; helpers de consigne et d'activation ; verrous de qualification (représentativité thermique, immunité poêle) ; protections contextuelles (fenêtre, aération) ; observabilité (historisation, traces).

**Exclus :** audit global du chauffage central, gouvernance, CI, conformité documentaire en tant que telles (abordées uniquement là où elles éclairent le comportement). La couche d'exécution transactionnelle (boiler bridge MQTT) n'est examinée que pour sa sûreté, jugée saine et non rouverte.

## 3. Méthode

L'audit a procédé par **revue contradictoire itérative** : chaque constat fort a été soumis à une contre-vérification exigeante (preuves par recherche, chemins, extraits), avec obligation de distinguer absence dans le dépôt, câblage indirect possible et câblage indirect prouvé. Plusieurs conclusions initiales ont été infirmées ou déclassées au cours de ce processus. Le présent rapport conserve volontairement la **trace du cheminement** : c'est une partie essentielle de sa valeur.

## 4. Constats initiaux (hypothèses de départ)

L'examen de premier passage a établi une asymétrie de qualité nette :

- **Couche d'exécution : excellente.** Scripts d'application transactionnels (request_id, ACK corrélé, bornes physiques, nettoyage, échec sûr si bridge indisponible). Découplage décision/action propre via écriture d'un helper de consigne.
- Et une série de constats critiques annoncés :
  - **C-GAP-1 / D-CRIT-1** — Représentativité thermique non câblée : `input_select.chauffage_representativite_thermique` écrit mais jamais lu par la décision.
  - **D-CRIT-2** — Boucle ouverte : aucune mesure du résultat d'un ajustement avant l'ajustement suivant.
  - **D-CRIT-3** — Effet : effacité indémontrable, faute d'historisation des variables de décision.
  - **C-GAP-2 / D-CRIT-4** — Immunité poêle jugée « partielle / insuffisante » (ne bloquant que les baisses).
  - **D-IMP-1** — Aucun garde-fou fenêtre/aération dans l'automation décisionnelle.

> ⚠️ Ces constats initiaux sont conservés ici **tels qu'émis**, pour mémoire. Plusieurs ont été corrigés par la suite (sections 5 et 6).

## 5. Révisions successives (cheminement intellectuel)

### 5.1 Découverte d'un câblage indirect (revue contradictoire)

La contre-vérification a **prouvé** une protection indirecte ignorée au premier passage :

> fenêtre ouverte (avec délai) / aération / blocage poêle actif → la décision centrale impose le **mode réduit** → la consigne appliquée devient `réduite` (12–20 °C) ≠ `confort` (17–25 °C) → la garde des capteurs d'écart `consigne_appliquee == consigne_confort` devient fausse → **les capteurs d'écart cessent d'échantillonner (gel).**

Conséquence : l'apprentissage **ne se pollue pas** pendant les fenêtres ouvertes / aérations / blocages poêle, contrairement au risque annoncé en D-IMP-1.

### 5.2 Qualification architecturale du câblage indirect

Ce gel n'est **pas une protection conçue pour l'auto-ajustement**. La garde « consigne = confort » existe pour une raison **sémantique** (ne mesurer l'erreur qu'en mode confort) ; le gel sous mode réduit en est une **conséquence**, pas un invariant possédé. Classé : **effet de bord bénéfique tenant lieu de protection → dépendance fragile**, révocable par une évolution distante (décision centrale ou garde d'écart) **sans signal**.

### 5.3 Correction métier majeure — l'asymétrie poêle

L'analyse métier a révélé que le traitement « ne bloquer que les baisses » est **correct**, pas déficient :

- Le poêle peut créer une **fausse surchauffe** → il doit interdire surtout la **baisse** de courbe.
- Une **sous-chauffe malgré poêle récent** reste significative (la chaudière est réellement insuffisante) → la **hausse** doit rester permise.

Le runtime implémente exactement cette asymétrie (garde baisse conditionnée à `poele_en_fonction_stable = off` ; hausse toujours permise ; gel bidirectionnel pendant le blocage actif). **Ce sont les contrats qui sont métier-faux** en exigeant une « suspension totale ».

### 5.4 Modèle physique de la représentativité

Reconstitué : la représentativité n'est pas un simple verrou de sécurité mais un **test de validité du signal**. Elle combat le **biais de chaleur gratuite** (soleil, apports internes, inertie, poêle) qui réchauffe la pièce sans que la courbe ait travaillé et pousse, presque toujours, à **baisser** la courbe à tort. Sans elle, le risque théorique est une **dérive lente descendante** du paramètre, plus fréquente que sa correction par les vraies journées froides.

### 5.5 Gravité réelle de la dérive — bornée

Confrontée à l'algorithme réel et au climat bordelais :

- La **pente** n'apprend que sous 5 °C extérieurs → **quasi structurellement immunisée** contre la dérive douce dans ce climat. Le biais ne peut toucher, en pratique, **que le parallèle**.
- Le parallèle est fortement amorti : signal sur `temperature_min_chambres` (pièce la plus froide, conservatrice), bande morte ±0,4 (seuil dur), pas ±1, bornes [-8 ; +8], et **rappel auto-limitant** sur les vraies journées froides.
- Bordeaux offre **beaucoup d'occasions** (demi-saisons douces/ensoleillées dominantes), mais l'amortissement **interdit l'emballement** : au pire, un **affaissement saisonnier borné**, conditionné au couplage du bâtiment à la chaleur gratuite.
- **Origine prophylactique** : le mécanisme a été introduit en v11 (co-conçu avec la machinerie de courbe), **sans trace d'une dérive observée**.

→ Verdict intermédiaire de gravité : **MOYENNE**.

### 5.6 Audit du proxy de représentativité — déclassement

Examen du signal lui-même (`pourcentage_consigne_eco_24h` = part des 24 h en mode Eco ; hystérésis 40/55) :

- Il mesure un **rapport cyclique de la demande de confort**, pas le **travail de la chaudière sous charge propre**.
- Il est **aveugle** à tous les déterminants physiques de la représentativité : froid réel, durée brûleur, énergie injectée, modulation, soleil, apports internes, inertie, poêle.
- **Faux positifs nombreux** : journée douce/ensoleillée/inertielle en confort → Eco% bas → déclarée représentative à tort — c'est-à-dire **précisément les journées à arrêter**.
- **Faux négatifs coûteux** : absence diurne + soirée froide en confort → Eco% haut → **rejet d'une donnée rare et précieuse**.
- **Pouvoir discriminant marginal FAIBLE** : redondant avec la garde confort + bande morte là où il fonctionne, aveugle là où le biais résiduel vit, et destructeur de bonnes journées.

→ Le brancher tel quel constituerait un **filtre médiocre**.

## 6. Constats invalidés ou déclassés

| Constat initial | Issue | Motif |
|---|---|---|
| **D-IMP-1** — « aucun garde-fou fenêtre/aération » | **Nuancé / risque infirmé** | Protection prouvée par câblage indirect (5.1). Le constat littéral (l'automation ne lit pas les fenêtres) reste vrai, mais le **risque** annoncé ne se matérialise pas. |
| **D-CRIT-4** — immunité poêle « partielle / insuffisante » | **Infirmé dans sa formulation** | L'asymétrie baisse-uniquement est l'invariant métier **correct** (5.3). |
| **C-GAP-2** — « le runtime sous-implémente le contrat » | **Sens inversé** | Les contrats sur-spécifient une suspension totale **métier-fausse** ; le runtime est plus correct (5.3). La divergence demeure, le tort change de camp. |
| **D-CRIT-2** — « boucle ouverte = défaut critique » | **Reformulé** | La boucle ouverte est intentionnelle (calibration lente, non adaptative). Le résidu réel n'est pas l'ouverture, mais la faiblesse d'instrumentation de la supervision (→ rejoint D-CRIT-3). |
| **Représentativité = manque critique** | **Déclassé à MINEUR** | Le proxy disponible est médiocre (5.6) ; le brancher n'apporterait quasiment rien et coûterait des faux négatifs. |

## 7. Constats confirmés

- **Couche d'exécution saine et fail-safe** (confirmé, non rouvert).
- **Découplage décision / action propre** (confirmé).
- **Représentativité non câblée** : confirmé de façon exhaustive (écrite par son automate, lue par aucune décision, aucun substitut indirect).
- **Protections fenêtre/aération/poêle-actif réelles mais empruntées** : confirmé, qualifié de dépendance fragile non possédée (5.2).
- **Asymétrie poêle correcte** : confirmé, métier-valide (5.3).
- **Dérive possible mais bornée**, pente quasi-immune en climat doux, parallèle seul exposé, sans emballement, non démontrée empiriquement (5.5).
- **Auto-ajustement aveugle sur ses propres variables** : les valeurs de courbe appliquées, les suggestions, la raison des refus ne sont pas historisées ni lisibles ; seuls quelques indicateurs de régulation (oscillation, overshoot, cycles) le sont. L'effet d'un ajustement n'est donc pas attribuable causalement.

## 8. Analyse finale

Le système se comporte bien et **ne peut pas diverger dangereusement** : exécution sûre, asymétrie métier correcte, amortissements multiples bornant toute dérive. Ses deux véritables limites ne sont **pas** des défauts de comportement présent :

1. **Aveuglement** — le système ne peut ni montrer ni prouver ce qu'il fait à la courbe dans le temps, alors qu'il se présente comme une calibration *supervisée*.
2. **Sûreté empruntée** — ses protections critiques fonctionnent via un effet de bord de la consigne appliquée, révocable sans alarme.

La représentativité, dans l'absolu, répond à un besoin physique réel ; mais le **signal actuellement conçu pour la porter est faible**, ce qui retire à son absence le caractère de gravité d'abord supposé.

## 9. Reclassification finale des risques

| Constat | Classe | Justification concise |
|---|---|---|
| Auto-ajustement aveugle sur ses propres variables | **Important** | Boucle la plus impactante, non observable d'elle-même ; préalable à toute certitude. |
| Protections fenêtre/aération/poêle-actif empruntées | **Important (non urgent)** | Fonctionne aujourd'hui ; fragilité latente révocable sans signal. |
| Représentativité non câblée | **Mineur** | Absence faible ; le proxy disponible (Eco%) est médiocre. |
| Pente quasi inerte en climat doux | **Sans action** | Prudence cohérente : peu d'occasions = peu de risque et peu de bénéfice. |
| Asymétrie poêle non formalisée comme invariant explicite | **Mineur** | Comportement correct ; manque seulement une formalisation de confort. |
| Divergences contrats (75/06) | **Mineur** | Le runtime est plus juste ; risque = confusion future, pas comportement. |
| Clamp domaine non tracé | **Sans action** | Cosmétique au regard du reste. |

**Maturité du système : globalement sain** — ni fragile/immature (pas d'emballement possible, gros œuvre sérieux), ni robuste au sens plein (aveugle sur lui-même, sûreté partiellement empruntée).

## 10. Décision de clôture

**Audit CLÔTURÉ.**

- Les questions initiales ont reçu une réponse ; les risques ont été reclassifiés ; les constats consolidés ; les priorités identifiées.
- Aucun besoin d'investigation supplémentaire n'est ouvert.
- La remédiation est tracée séparément (chantier + backlog) et **ne maintient pas l'audit ouvert**.
- Point arrêté comme indécidable en l'état : l'existence d'une dérive réelle ne pourra être tranchée qu'une fois l'observabilité livrée (cf. chantier).

**Suite documentaire :**
- Chantier : `04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md`
- Backlog : `04_chantiers/chauffage/backlog_auto_ajustement_courbe.md`

---
*Fin du rapport — audit clôturé le 2026-06-03.*
