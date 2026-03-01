# ARSENAL — AUDIT DE COHÉRENCE ET LACUNES
## Domaine : Aération → Blocage Chauffage
### Périmètre audité : Contrat Ouvertures + Socle Transversal + Machine M0→M6

---

## MÉTHODE

Audit conduit par lecture séquentielle des contrats normatifs dans l'ordre de dépendance. Chaque observation est classée selon sa criticité et son type. Les observations résolues par des contrats ultérieurs sont signalées.

---

## CLASSIFICATION DES OBSERVATIONS

| Criticité | Définition |
|-----------|-----------|
| **CRITIQUE** | Violation d'invariant, comportement incorrect documenté, risque fonctionnel direct |
| **STRUCTURELLE** | Incohérence inter-contrats, lacune de couverture, ambiguïté normative |
| **DOCUMENTAIRE** | Divergence de formulation, absence de justification explicite, désalignement sémantique |

---

## 1. LACUNES INTER-CONTRATS SYSTÉMATIQUES

### OBS-001 — CRITIQUE
**Entités `fenetre_ouverte_maison` et `fenetre_ouverte_maison_avec_delai` absentes du contrat Ouvertures**

Le contrat Ouvertures définit `binary_sensor.contact_fenetres_maison` (N2) comme agrégat canonique. Il ne définit ni `fenetre_ouverte_maison` ni `fenetre_ouverte_maison_avec_delai`. Ces deux entités sont pourtant consommées dans au moins cinq mécanismes : sécurité démarrage, détecteur KO, mini-guard, M0 Cas A, M0 Cas B. Le contrat d'interfaces externes les déclare comme interfaces consommées depuis le contrat Ouvertures — mais ce contrat ne les produit pas.

Trois résolutions possibles, aucune documentée :
- alias non déclaré de `contact_fenetres_maison`,
- entités définies dans une partie non partagée du contrat Ouvertures,
- entités définies dans ce domaine en violation de l'interdit de duplication.

Le contrat Ouvertures étant clos et figé, toute résolution nécessite soit un avenant, soit une clarification de portée.

---

### OBS-002 — STRUCTURELLE
**`aeration_confirmee` : autorité de reset non reconnue par le contrat Ouvertures**

Le contrat Ouvertures déclare `aeration_confirmee` comme fait métier posé par ce contrat, resetté par M2 et M0. Le contrat Ouvertures est clos et figé et ne mentionne pas M0 comme autorité de reset autorisée. M0 Cas B remet ce flag à off — action contractuellement légitime dans le domaine Aération, mais non reconnue par le contrat producteur.

---

### OBS-003 — DOCUMENTAIRE
**`aeration_confirmee` : sémantique divergente entre contrats**

Le contrat Ouvertures qualifie `aeration_confirmee` de "fait métier". Le contrat M2 Reset confirmation le qualifie de "signal événementiel d'entrée, non indicateur persistant d'état". Un fait métier a une sémantique d'état persistant ; un signal événementiel est consommable. Ces deux qualifications ne sont pas équivalentes et créent une ambiguïté sur le comportement attendu en cas de lecture concurrente.

---

### OBS-004 — STRUCTURELLE
**`binary_sensor.tentative_aeration_en_grace` classé N0 de façon incorrecte**

Ce capteur est une combinaison logique de deux entités N1 (`contact_sejour`, `contact_chambre_parents`) et de deux timers de grâce. La définition N0 du contrat Ouvertures désigne exclusivement les sources brutes matérielles. Ce capteur est conceptuellement un N2 qualifié ou un canon. La classification N0 crée une ambiguïté taxonomique avec le contrat Ouvertures.

---

### OBS-005 — STRUCTURELLE
**Timers de grâce (`timer.fenetre_sejour_ouverte_grace`, `timer.fenetre_chambre_parents_grace`) sans contrat amont**

Ces timers sont des dépendances structurelles de `tentative_aeration_en_grace` mais n'apparaissent dans aucun contrat partagé. Leur déclenchement, durée, et annulation sont indéfinis contractuellement dans le périmètre audité.

---

### OBS-006 — STRUCTURELLE
**Asymétrie des entités d'ouverture dans la machine à états**

M1 utilise `contact_fenetres_maison` (N2) pour vérifier l'enveloppe ouverte. M2 utilise `fenetres_maison_fermees_stable` (canon) pour vérifier l'enveloppe fermée. M3, M4, M5, M6 utilisent `contact_fenetres_maison` (N2). Les mécanismes de garde (sécurité démarrage, mini-guard, détecteur KO, M0) utilisent `fenetre_ouverte_maison` (interface externe). Quatre entités différentes couvrent conceptuellement la même notion d'état de l'enveloppe, sans documentation de cette hétérogénéité comme intentionnelle.

---

## 2. MACHINE À ÉTATS — LACUNES ET INCOHÉRENCES

### OBS-007 — CRITIQUE - APPLIQUÉE 
**M0 Cas C : condition trop permissive, risque de levée de blocage légitime**

La condition du cas C est "blocage ON + timer blocage idle". Cette condition est vraie pendant l'état canon M5 (suspension active, timer annulé, datetime valide). M0 déléguerait alors M4 sur un blocage légitime en cours de suspension. Trois préconditions manquantes :
- exclusion de `aeration_suspension_active = on`,
- vérification enveloppe fermée (M4 ne peut s'exécuter fenêtre ouverte),
- vérification que la datetime est neutralisée ou dépassée (éviter levée avant terme).

---

### OBS-008 — CRITIQUE - APPLIQUÉE 
**M4 : `aeration_suspension_active` non réinitialisé en clôture**

La séquence M4 et l'invariant post-M4 ne remettent pas `aeration_suspension_active` à off. Si M5 est exécuté et que le cycle se termine sans refermeture (chemin M0 Cas C → M4, ou tout autre chemin de remédiation contournant M6), `aeration_suspension_active` reste on après clôture complète. Ce résidu n'est détecté ni par le détecteur KO, ni par aucun mécanisme de remédiation identifié. L'état canon 1 (repos total) et l'état canon 7 (fin totale) ne l'incluent pas dans leurs conditions — l'incohérence est donc structurellement invisible.

---

### OBS-009 — CRITIQUE
**M4 : blocage orphelin non récupérable par expiration simultanée des deux timers**

Si `timer.aeration_blocage` et `timer.aeration_analyse_delta_t` expirent quasi-simultanément et que le pipeline traite `timer.aeration_blocage.finished` en premier, M4 est bloqué par la condition "timer analyse non actif = faux". Le blocage reste actif sans timer (incohérence A du détecteur KO). M3 doit ensuite s'exécuter pour neutraliser `analyse_deltat_disponible`, permettant ensuite M4 — mais il n'existe plus de déclencheur `timer.aeration_blocage.finished` pour relancer M4. Ce chemin produit un blocage orphelin non récupérable sans intervention de M0.

---

### OBS-010 — CRITIQUE - RÉSOLUE 
**M6 : échéance expirée pendant suspension → blocage orphelin sans déclencheur**

Si `fin_cible - now <= 0` lors de l'exécution de M6 (échéance expirée pendant la suspension M5), M6 ne redémarre pas le timer blocage (condition "durée strictement positive"). Le blocage reste actif sans timer — incohérence A. Aucun déclencheur ne peut alors activer M4. M6 devrait détecter ce cas et soit déclencher M4, soit émettre un signal de remédiation. Ni l'un ni l'autre n'est documenté.

---

### OBS-011 — STRUCTURELLE
**Fenêtres d'incohérence transitoire dans M1 et M2 non implémentables par le détecteur KO**

M1 pose `aeration_episode_en_cours = on` avant `aeration_pipeline_arme = on` — fenêtre où l'invariant "épisode actif ↔ pipeline armé" est violé. M2 pose `chauffage_blocage_aeration = on` avant les datetimes et les timers — fenêtre où le détecteur KO (incohérence C : blocage ON + datetime neutralisée) peut déclencher un faux positif. Ces fenêtres sont inhérentes à l'exécution séquentielle des scripts HA. L'incohérence 3 des états canons tente de les couvrir par la clause "ET aucune transition M2/M4 en cours" — mais cette clause n'est pas implémentable dans un template sensor sans connaissance de l'état d'exécution du script.

---

### OBS-012 — STRUCTURELLE
**M1 : armement pipeline en dernière position crée une incohérence détectable de l'extérieur**

Entre l'effet 1 (`aeration_episode_en_cours = on`) et l'effet 5 (`aeration_pipeline_arme = on`), une automation déclenchée sur le changement de `aeration_episode_en_cours` verra un état impossible (épisode ON, pipeline OFF). Ce risque est réel si des consommateurs externes observent `aeration_episode_en_cours` directement.

---

### OBS-013 — STRUCTURELLE - RÉSOLUE 
**M5 : "réouverture qualifiée" non définie contractuellement**

La condition pipeline de M5 mentionne "réouverture qualifiée détectée" sans définir l'entité porteuse de cette qualification. Le lien avec `aeration_confirmee` comme signal de réouverture pendant blocage est suggéré dans M2 mais non formalisé dans M5.

---

### OBS-014 — STRUCTURELLE - RÉSOLUE 
**M5 : comportement timer ambigu entre contrat timers et contrat M5**

Le contrat timers (section 8) décrit la suspension comme "timer annulé ou redémarré". Le contrat M5 décrit uniquement un redémarrage monotone. Ces deux descriptions ne sont pas alignées sur le chemin "annulation". Si M5 annule (sans redémarrer), M6 doit recalculer depuis la datetime. Si M5 redémarre toujours, M6 trouve un timer actif. La version normative n'est pas univoque.

---

### OBS-015 — STRUCTURELLE
**M6 : relance du timer analyse après M3 consommé non couverte**

Si M5 est déclenché après M3 (réouverture post-analyse), `analyse_deltat_disponible` est neutralisée. M6 ne redémarre pas le timer analyse (durée = 0 sur datetime neutralisée). Seul M4 est en attente. Si `timer.aeration_blocage` est également expiré, le système entre dans le cas OBS-010.

---

### OBS-016 — DOCUMENTAIRE
**Invariant post-M4 et état canon 7 : deux descriptions du même état sans lien explicite**

L'invariant post-M4 liste six conditions. L'état canon 7 liste un périmètre légèrement différent : il inclut `aeration_episode_en_cours = off` (absent de l'invariant M4) mais est moins précis sur les timers. Ces deux descriptions devraient être la même référence ou l'une devrait explicitement pointer vers l'autre.

---

## 3. SÉCURITÉ DÉMARRAGE & MÉCANISMES DE GARDE

### OBS-017 — CRITIQUE - APPLIQUÉE 
**Sécurité démarrage et mini-guard : datetimes non neutralisées post-exécution**

La sécurité démarrage (ID 10010000000022) et le mini-guard (ID 10010000000024) annulent les timers et désarment le pipeline mais ne neutralisent pas `chauffage_fin_blocage_aeration` ni `analyse_deltat_disponible`. L'état résultant n'est ni l'état canon 1 (repos total) ni l'état canon 7 (fin totale) — les deux exigent datetimes neutralisées. Ces deux mécanismes laissent donc le système dans un état non-canon après exécution.

---

### OBS-018 — STRUCTURELLE
**Lacune post-boot : incohérences préexistantes silencieuses au retour de `systeme_stable`**

Si une incohérence de type B, C ou D (détecteur KO) est présente avant un reboot et persiste au retour de `systeme_stable = on`, elle ne produit pas de front montant sur `coherence_ko`. Le signal recover n'est émis que sur front montant (passage off→on + 30s). L'incohérence reste silencieuse indéfiniment jusqu'au prochain changement d'état pertinent. La sécurité démarrage ne couvre que le blocage résiduel dépassé — pas les cas B, C, D.

---

### OBS-019 — STRUCTURELLE - APPLIQUÉE 
**Mini-guard et M0 Cas A : asymétrie sur l'annulation des timers**

Le mini-guard annule les timers avant de désarmer le pipeline. M0 Cas A désarme le pipeline sans annuler les timers. Si un timer résiduel est actif dans un état zombie, il survit à M0 Cas A. M0 assume implicitement que le mini-guard a déjà nettoyé les timers — dépendance implicite non documentée. Si M0 est la remédiation de dernier recours, il devrait être autonome.

---

### OBS-020 — STRUCTURELLE
**Détecteur KO : incohérences 4, 5 et 7 non couvertes**

En croisant les états impossibles (section 9 du contrat États canons) avec les incohérences couvertes par le détecteur :
- Incohérence 4 (timer actif + blocage OFF) : non couverte
- Incohérence 5 (analyse disponible valide + blocage OFF) : non couverte
- Incohérence 7 (blocage ON + enveloppe ON + suspension_active OFF) : non couverte

Ces cas ne sont couverts par aucun mécanisme identifié dans la documentation partagée.

---

### OBS-021 — STRUCTURELLE - APPLIQUÉE 
**Détecteur KO incohérence A : faux positif potentiel en M5**

L'incohérence A détecte "blocage ON + timer blocage idle". L'état canon 3 autorise timer idle si datetime valide future (cas M5 avec timer annulé). Le détecteur déclencherait un faux KO sur un état canon valide. La condition devrait exclure `aeration_suspension_active = on` ou vérifier que la datetime est également neutralisée.

---

### OBS-022 — STRUCTURELLE
**Signal recover : boucle infinie sur incohérence non résolvable par M0**

Si M0 pose `recover_requested = off` sans résoudre l'incohérence, le détecteur reste KO et réémet le signal après 30s. Ce comportement de retry implicite n'est pas borné. Sans limite de retry ou mécanisme d'escalade, une incohérence non résolvable par M0 produit une boucle infinie de signaux et d'exécutions M0 partielles.

---

## 4. HELPERS & PARAMÈTRES

### OBS-023 — STRUCTURELLE - RÉSOLUE 
**`input_boolean.blocage_chauffage_aeration_active` non documenté dans le contrat helpers**

Ce helper de gouvernance du pipeline maître apparaît dans le contrat M0 cadre général comme condition de routage, mais est absent du contrat helpers du socle transversal. Son rôle, son autorité d'écriture, et ses invariants ne sont pas définis dans le périmètre audité.

---

### OBS-024 — STRUCTURELLE
**`sensor.temperature_min_chambres` non contractualisé**

Ce capteur alimente `chute_temp_reference` via M1 snapshots. Son périmètre (quelles chambres), son mode de calcul (min strict ?), et sa robustesse à l'indisponibilité sont inconnus contractuellement. Son rôle dans la logique M3 est par ailleurs indéterminé — `chute_temp_reference` n'apparaît dans aucun contrat M3.

---

### OBS-025 — STRUCTURELLE
**`chute_temp_reference` : rôle déclaré sans consommateur identifié**

M1 snapshots déclare `chute_temp_reference` comme "référence unique pour toute analyse ΔT ultérieure". Aucun contrat M3 (orchestrateur, calcul ΔT, routage, prolonger, maintenir) ne consomme ce helper. Soit il est utilisé dans un mécanisme non partagé, soit la déclaration de M1 est inexacte.

---

### OBS-026 — DOCUMENTAIRE
**Ordre des seuils ΔT : invariant logique sans garde-fou d'exécution**

Le contrat helpers stipule `seuil_tiny < seuil_medium < seuil_high`. Le contrat M3 routage délègue la détection d'incohérence au "contrat Intégrité paramètres — Chauffage" non partagé. Si les seuils sont incohérents, M3 peut produire un routage incorrect sans détection dans le périmètre audité. Aucun garde-fou au démarrage ou à l'écriture n'est documenté ici.

---

### OBS-027 — DOCUMENTAIRE
**`aeration_debut` et `aeration_reouverture_last` : neutralisation non définie**

Ces deux datetimes figurent dans la liste fermée du contrat neutralisation mais sans règle de neutralisation définie. La liste fermée est contractuellement close — leur présence sans définition opérationnelle associée est une lacune interne à ce contrat.

---

## 5. ANALYSE ΔT

### OBS-028 — CRITIQUE - RÉSOLUE 
**Contradiction de définition ΔT entre contrat ΔT par pièce et contrat M3 calcul**

Le contrat ΔT par pièce définit : `ΔT = max(T_REF - T_ACTUELLE, 0)` (manque thermique, toujours ≥ 0). Le contrat M3 calcul ΔT décrit : "température courante − référence snapshot M1" (soit `T_ACTUELLE - T_REF`). Ces deux définitions sont opposées. Si la définition M3 est correcte, `delta_max` peut être négatif et la condition `delta_max < seuil_tiny` est systématiquement vraie — aucune prolongation n'est jamais produite. C'est la lacune à l'impact fonctionnel le plus direct de l'ensemble du domaine.

ERREUR DOCUMENTAIRE (M3)

---

### OBS-029 — STRUCTURELLE
**Biais silencieux cumulatifs sur les valeurs ΔT**

Deux biais silencieux s'accumulent sans détection :
1. Snapshot conservateur M1 : si `temperature_*` est indisponible, la valeur précédente est conservée — T_REF peut être celle d'un épisode antérieur.
2. Calcul ΔT : si `temperature_*` est indisponible en lecture, t = 0, produisant un ΔT artificiellement élevé égal à T_REF entière.

M3 consomme `delta_max` sans marqueur de validité permettant de distinguer une valeur calculée sur des données réelles d'une valeur issue d'indisponibilités capteurs.

---

### OBS-030 — STRUCTURELLE
**Absence de marqueur de validité des T_REF**

Le contrat ΔT stipule qu'un ΔT "n'a de sens contractuel que si les références ont été figées par M1". Les capteurs ΔT retournent toujours un numérique — même si M1 n'a jamais été exécuté et que les ref_temp sont à leur valeur initiale (typiquement 0). M3 n'a pas de moyen contractuel de distinguer un ΔT calculé sur des références valides d'un ΔT calculé sur des références non initialisées.

---

### OBS-031 — DOCUMENTAIRE - RÉSOLUE 
**`prolongation_heures` transmis comme float, normalisé comme int dans M3 prolonger**

Le contrat M3 orchestrateur précise que la valeur transmise est "en heures (fraction possible)". Le contrat M3 prolonger normalise `prolongation_heures | int(0)` — conversion entière tronquante. Une prolongation de 90 minutes (1.5h) devient 1h silencieusement. La perte de précision n'est pas documentée et le logbook affiche la valeur tronquée, rendant l'audit a posteriori inexact.

ERREUR DOCUMENTAIRE (M3)

---

## 6. NEUTRALISATION DATETIME

### OBS-032 — STRUCTURELLE
**Marqueur `00:00:00` : risque de collision avec une valeur légitime à minuit**

Si une échéance est calculée exactement à minuit, elle est interprétée comme neutralisée. La logique de calcul des échéances (M2 : `now + délai`) ne garantit pas contractuellement qu'aucune proposition ne tombe à `00:00:00`. Ce cas est improbable mais non exclu et non documenté.

---

### OBS-033 — DOCUMENTAIRE
**M2 : interdit "ne pas modifier les échéances une fois le blocage actif" — contradiction interne**

La séquence M2 pose le blocage (effet 2) avant de mettre à jour les datetimes (effet 4). M2 modifie donc les échéances alors que le blocage est déjà actif, en violation littérale de son propre interdit. La formulation visait probablement "M2 ne doit pas être rappelé une fois le blocage actif".

---

### OBS-034 — DOCUMENTAIRE
**Couplage `blocage_initial = délai_analyse + 1 minute` non documenté comme intentionnel**

La durée initiale du blocage est dérivée mécaniquement du délai d'analyse. Ce couplage n'est pas un paramètre indépendant. Ajuster `delai_stabilisation_capteurs` modifie simultanément la fenêtre d'analyse et la durée minimale de blocage — effet de bord non documenté.

---

## 7. CONTRATS NON PARTAGÉS RÉFÉRENCÉS

Les contrats suivants sont référencés dans la documentation auditée mais n'ont pas été partagés. Leur absence constitue des angles morts pour l'audit :

| Référence | Contexte |
|-----------|---------|
| `00_gouvernance_chauffage.md` | Hiérarchie supérieure déclarée dans le socle |
| Contrat Intégrité paramètres — Chauffage | Garde-fou seuils ΔT |
| Contrat Pipeline maître (ID 10010000000023) | Autorité centrale de routage M0→M6 |
| Définition complète `binary_sensor.fenetre_ouverte_maison` | Interface critique consommée par 5 mécanismes |
| Définition complète `binary_sensor.fenetre_ouverte_maison_avec_delai` | Interface critique consommée par 3 mécanismes |

---

## SYNTHÈSE PRIORISÉE

### Critiques — À résoudre en priorité

| ID | Sujet |
|----|-------|
| OBS-001 | Entités `fenetre_ouverte_maison` absentes du contrat Ouvertures |
| OBS-007 | M0 Cas C : condition trop permissive, levée de blocage légitime possible |
| OBS-008 | `aeration_suspension_active` non réinitialisé par M4 |
| OBS-009 | Blocage orphelin non récupérable sur expiration simultanée des deux timers |
| OBS-010 | M6 : échéance expirée → blocage orphelin sans déclencheur |
| OBS-017 | Sécurité démarrage et mini-guard : datetimes non neutralisées post-exécution |
| OBS-028 | Contradiction de définition ΔT entre deux contrats |

### Structurelles — À documenter ou corriger

| ID | Sujet |
|----|-------|
| OBS-002 | `aeration_confirmee` : autorité de reset non reconnue par contrat Ouvertures |
| OBS-004 | `tentative_aeration_en_grace` classé N0 incorrectement |
| OBS-011 | Fenêtres d'incohérence transitoire non implémentables par le détecteur KO |
| OBS-018 | Lacune post-boot : incohérences préexistantes silencieuses |
| OBS-019 | Mini-guard et M0 Cas A : asymétrie sur l'annulation des timers |
| OBS-020 | Détecteur KO : incohérences 4, 5 et 7 non couvertes |
| OBS-021 | Détecteur KO incohérence A : faux positif potentiel en M5 |
| OBS-022 | Signal recover : boucle infinie sur incohérence non résolvable |
| OBS-023 | `blocage_chauffage_aeration_active` non documenté |
| OBS-024 | `sensor.temperature_min_chambres` non contractualisé |
| OBS-025 | `chute_temp_reference` sans consommateur identifié |
| OBS-029 | Biais silencieux cumulatifs sur les valeurs ΔT |
| OBS-030 | Absence de marqueur de validité des T_REF |
| OBS-031 | `prolongation_heures` : perte de précision silencieuse int vs float |

### Documentaires — À aligner

| ID | Sujet |
|----|-------|
| OBS-003 | `aeration_confirmee` : sémantique divergente entre contrats |
| OBS-006 | Asymétrie des entités d'ouverture dans la machine à états |
| OBS-013 | M5 : "réouverture qualifiée" non définie |
| OBS-016 | Invariant post-M4 et état canon 7 : deux descriptions sans lien |
| OBS-026 | Ordre des seuils ΔT sans garde-fou d'exécution |
| OBS-027 | `aeration_debut` et `aeration_reouverture_last` : neutralisation non définie |
| OBS-032 | Marqueur `00:00:00` : risque de collision à minuit |
| OBS-033 | M2 : contradiction interne sur l'interdit de modification post-blocage |
| OBS-034 | Couplage `blocage_initial = délai_analyse + 1 min` non documenté |

---

*Audit produit sur la base des contrats normatifs partagés. Tout contrat non partagé constitue un angle mort explicite.*
