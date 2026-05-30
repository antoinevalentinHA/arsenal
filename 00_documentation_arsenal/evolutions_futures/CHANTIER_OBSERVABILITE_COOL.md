# CHANTIER OBSERVABILITÉ COOL — PLAN DE CONCEPTION

> Périmètre : D1, D2, D3, D6, D7. Interdit : D4, D9, H1, H2, H3, HEAT, DRY, chauffage.
> Objectif unique : supprimer toute situation « runtime vrai / UI faux » sur le COOL.
> Aucun patch ici. Aucune modification de décision, automatisme ou script.

---

## 0. Définition du périmètre « observabilité » (fondation du chantier)

Le mot « runtime » dans les interdictions désigne les entités **porteuses de décision**
(autorisations, admissibilité, `target_mode`, besoins, seuils), les **automatisations**
et les **scripts**. Ce chantier n'en touche **aucun**.

Les trois capteurs édités (`clim_raison_decision`, `clim_bloquee`,
`clim_action_en_cours`) sont des **capteurs de diagnostic** : la recherche de
consommateurs renvoie **zéro consommateur décisionnel** — ils ne sont lus que par des
cartes UI. Les éditer ne modifie donc ni une décision, ni un automatisme, ni un script.
C'est exactement la nature du chantier : aligner les artefacts d'observabilité sur la
vérité que la chaîne de décision produit déjà.

**Preuve d'innocuité (à rejouer avant exécution) :**
```
grep -rln "clim_raison_decision|clim_bloquee|clim_action_en_cours" --include="*.yaml" . \
  | grep -vE "12_template_sensors/climatisation/(decision|blocages)" \
  | grep -vE "18_lovelace|19_button_card"
# → doit rester vide
```

---

## 1. SOURCE DE VÉRITÉ (NE PAS MODIFIER)

`binary_sensor.autorisation_clim_cool` définit la totalité des causes de non-action COOL :

```
COOL autorisé  ⇔   temperature_jardin ≥ clim_seuil_temperature_exterieure_minimum
              ET  clim_blocage_aeration_etage_reel = off
              ET  fenetre_ouverte_maison_avec_delai = off
              ET  clim_blocage_horaire_reel = off
              ET  clim_extinction_absence_prolongee_autorisee = off
```

Donc l'ensemble **exact** des causes COOL = { température extérieure trop basse,
aération étage, fenêtre maison (temporisée), blocage horaire, absence prolongée }.
Quatre sont des capteurs binaires discrets déjà exposés ; la cinquième est un seuil.
**Toute l'observabilité COOL doit refléter ce jeu, ni plus ni moins.**

---

## 2. CARTOGRAPHIE ACTUELLE (les mensonges)

```
DÉCISION (vérité)                         OBSERVABILITÉ (mensonges)
─────────────────                         ─────────────────────────
autorisation_clim_cool ──┐
  • temp_ext ≥ seuil      │  raison_decision   : ✗ ignore aération_étage
  • ¬aération_étage       │                       ✗ ignore absence_prolongée
  • ¬fenêtre_AVEC_DELAI   │                       ✗ ignore temp_ext
  • ¬horaire_reel         │                       ✗ lit fenêtre BRUTE (≠ décision)
  • ¬absence_prolongée    │                       → tombe à « aucune_demande »
                          │
  → besoin_admissible     │  clim_bloquee      : ✗ ignore aération_étage
  → target_mode (cool)    │                       ✗ ignore absence_prolongée
                          │                       ✗ FAUX POSITIF fenêtre ÉTAGE
                          │                       ✗ lit fenêtre BRUTE
                          │
                          │  action_en_cours   : ✗ poêle → « bloquee » même
                          │                         pendant un COOL actif
                          │
                          │  carte synthese_xl : ✗ n'affiche qu'horaire + post-aér.
                          │                       ✗ recalcule l'horaire en JS (horloge
                          │                         du navigateur) → D6
                          │                       → « Aucun blocage » à tort
                          │
                          │  status_72         : hérite des mensonges de raison
                          │  carte_clim_decision: verdict de cohérence recalculé en JS (D6)
```

### Mensonges recensés (exhaustif, périmètre COOL)
- **Capteurs qui mentent** : `clim_raison_decision` (D1, D2), `clim_bloquee` (D3),
  `clim_action_en_cours` (D7).
- **Cartes qui mentent** : `clim_blocages_synthese_xl` (D3 + D6), `carte_clim_decision`
  (D6), `clim_decision_synthetique_72` (hérite de raison).
- **Raisons incomplètes** : aération étage, absence prolongée, température extérieure
  absentes de la cascade ; fenêtre lue en version brute au lieu de temporisée.
- **Agrégations incomplètes** : `clim_bloquee` agrège un sous-ensemble faux (manque
  aération étage ; inclut fenêtre étage inerte) ; la carte synthèse n'agrège que 2 causes.

---

## 3. CARTOGRAPHIE CIBLE (l'UI reflète la décision)

```
autorisation_clim_cool (INCHANGÉE)
        │  mêmes entrées …
        ▼
clim_raison_decision   → cascade COOL complète :
                          horaire → aération_étage → fenêtre_AVEC_DELAI
                          → [cool_adm / dry_adm / heat_adm]
                          → absence_prolongée → temp_ext_trop_froid
                          → aucune_demande   (mode-aware : aucun faux DRY/HEAT)

clim_bloquee           → OU des prohibitions discrètes actives :
                          poêle(heat) ∨ post-aération(heat) ∨ horaire_reel
                          ∨ aération_étage ∨ fenêtre_AVEC_DELAI
                          (fenêtre ÉTAGE supprimée)

clim_action_en_cours   → état réel d'abord :
                          cool→cool_actif / dry→dry_actif / heat→heat_actif
                          / (poêle ∧ clim off)→bloquee / sinon arret

synthese_xl (carte)    → liste les prohibitions lues depuis les capteurs backend ;
                          état horaire = clim_blocage_horaire_reel (plus d'horloge client)

status_72 (carte)      → traduit TOUS les codes de raison (anciens + 3 nouveaux)
carte_clim_decision    → cohérence = clim_incoherence_decision_reel (plus de JS)
```

Principe directeur : la vérité mode-aware et fine vit dans `clim_raison_decision` ;
le voyant binaire `clim_bloquee` ne porte que les **prohibitions non ambiguës**
(absence/temp_ext restent dans la raison, pour éviter un faux « verrou » en hiver).

---

## 4. PLAN DE MODIFICATION — FICHIER PAR FICHIER

### F1 — `12_template_sensors/climatisation/decision/raison.yaml` (D1, D2)
**Quoi.** Compléter la cascade. Ajouter, dans l'ordre de priorité d'affichage :
- avant les `*_adm` : branche `clim_blocage_aeration_etage_reel == on → blocage_aeration_etage` ;
- remplacer `fenetre_ouverte_maison` (brut) par `fenetre_ouverte_maison_avec_delai` ;
- après les `*_adm` : `clim_extinction_absence_prolongee_autorisee == on → absence_prolongee` ;
  puis `temperature_jardin < clim_seuil_temperature_exterieure_minimum → exterieur_trop_froid`.
Les branches `blocage_poele` / `blocage_aeration` (contexte HEAT) restent **inchangées**.

**Pourquoi.** Quand COOL est bloqué par l'aération étage ou l'absence prolongée, la raison
tombe aujourd'hui sur `aucune_demande_admissible` ; la fenêtre est lue avec un timing
différent de la décision.

**Mensonge supprimé.** « Aucune condition ne justifie une action » alors qu'une cause
existe (D1) ; divergence raison↔décision sur la fenêtre (D2).

**Pourquoi pas DRY/HEAT.** Les deux causes COOL-seules (absence, temp_ext) sont placées
**après** `dry_adm`/`heat_adm` → jamais affichées quand DRY/HEAT est admissible. La fenêtre
temporisée est aussi celle que lisent les autorisations HEAT/DRY → alignement, pas
modification de leur décision.

**Innocuité runtime.** Capteur diagnostic, zéro consommateur décisionnel. Aucune entité de
décision touchée. `float()` de repli sur temp_ext/seuil (miroir de l'autorisation) pour ne
jamais casser le rendu.

---

### F2 — `12_template_sensors/climatisation/blocages/diagnotic.yaml` (D3)
**Quoi.** Dans `clim_bloquee` :
- **ajouter** `clim_blocage_aeration_etage_reel` ;
- **remplacer** `fenetre_ouverte_maison` (brut) par `fenetre_ouverte_maison_avec_delai` ;
- **supprimer** `fenetre_ouverte_etage`.
Conserver `blocage_clim_poele` et `chauffage_blocage_aeration` (prohibitions HEAT réelles).

**Pourquoi.** Le voyant ignore l'aération étage (faux négatif), inclut une fenêtre d'étage
qui ne bloque rien (faux positif), et lit la fenêtre au mauvais timing.

**Mensonge supprimé.** Voyant « déverrouillé » alors que l'aération étage bloque (D3) ;
voyant « verrouillé » pour une fenêtre d'étage inerte (D3).

**Innocuité runtime.** Capteur diagnostic pur. `fenetre_ouverte_etage` n'a aucun rôle dans
les autorisations (vérifié) ; le retirer ne change aucune décision.

---

### F3 — `12_template_sensors/climatisation/decision/action_en_cours.yaml` (D7)
**Quoi.** Réordonner : tester `climate.clim` (cool/dry/heat) **avant** le poêle. Ne
renvoyer `bloquee` que si `blocage_clim_poele == on` **et** la clim est éteinte.

**Pourquoi.** Le poêle ne bloque que le HEAT ; aujourd'hui il force `bloquee` même pendant
un refroidissement actif.

**Mensonge supprimé.** « Bloquée » pendant un COOL actif (D7), propagé à la carte diagnostic.

**Innocuité runtime.** Capteur diagnostic. Aucune logique HEAT ajoutée : on lit simplement
l'état réel d'abord ; la branche poêle subsiste uniquement quand la clim est off.

---

### F4 — `…/40_contraintes/clim_blocages_synthese_xl.yaml` (D3, D6)
**Quoi.** Réécrire la carte pour qu'elle **lise les capteurs backend** au lieu de recalculer :
- état horaire = `binary_sensor.clim_blocage_horaire_reel` (plus de `new Date()` client) ;
- ajouter l'affichage de `binary_sensor.clim_blocage_aeration_etage_reel` ;
- conserver post-aération ; la plage `hOn/hOff` reste affichée à titre **informatif** mais
  ne décide plus de l'état actif ;
- « Aucun blocage » uniquement si tous les capteurs de prohibition sont off.

**Pourquoi.** La carte n'affiche que 2 causes et recalcule l'horaire côté navigateur
(dépend de l'horloge/fuseau client).

**Mensonge supprimé.** « Aucun blocage en cours » alors que l'aération étage bloque (D3) ;
logique métier horaire dans l'UI (D6).

**Innocuité runtime.** Carte button-card (UI pure). Elle ne fait plus que lire des capteurs
existants.

---

### F5 — `…/20_statut_metier/clim_decision_synthetique_72.yaml` (suite D1)
**Quoi.** Ajouter la traduction des 3 nouveaux codes de raison
(`blocage_aeration_etage`, `absence_prolongee`, `exterieur_trop_froid`) + un libellé de
repli pour tout code inconnu. Conserver les codes existants.

**Pourquoi.** F1 introduit de nouveaux codes ; sans cette mise à jour la carte afficherait
le code brut.

**Mensonge supprimé.** Empêche que la correction de raison (F1) produise un affichage illisible.

**Innocuité runtime.** Carte UI pure.

---

### F6 — `…/30_diagnostic/carte_clim_decision.yaml` (D6)
**Quoi.** Remplacer le verdict de cohérence recalculé en JS par la lecture de
`binary_sensor.clim_incoherence_decision_reel` (vérité backend existante). Gérer les
nouveaux codes de raison (ou s'appuyer entièrement sur le capteur d'incohérence).

**Pourquoi.** La carte recalcule en JS un verdict cohérence raison↔action, redondant avec
le capteur backend, et adossé à une raison auparavant fausse.

**Mensonge supprimé.** Verdict de cohérence dérivé d'entrées fausses + logique métier en UI (D6).

**Innocuité runtime.** Carte UI pure ; `clim_incoherence_decision_reel` existe déjà et n'est
pas modifié.

> Hors périmètre explicite : `18_lovelace/dashboards/diagnostics/climatisation.yaml`
> (tuile `clim_synthese_status_72`) relève de la dette D-tuile (P2), **pas** de ce chantier.
> Ne pas y toucher ici.

---

## 5. RISQUES

| Risque | Niveau | Mitigation |
|---|---|---|
| Mauvaise **priorité** d'affichage si plusieurs causes COOL actives | Faible | Ordre figé dans F1 (horaire > aération étage > fenêtre > absence > temp_ext) ; n'affecte que l'affichage |
| Mislabel DRY/HEAT par les nouvelles branches | Faible | Causes COOL-seules placées après `dry_adm`/`heat_adm` ; branches HEAT inchangées |
| Code de raison non traduit → affichage brut | Moyen | F5 + F6 déployés **avec** F1 ; libellé de repli |
| Erreur de template si entités indisponibles | Faible | `float()`/`is_state` de repli, miroir de l'autorisation |
| Régression visuelle des cartes (mise en forme) | Faible | UI pure ; contrôle visuel post-déploiement |
| Un consommateur décisionnel insoupçonné des 3 capteurs | Très faible | Preuve grep (§0) à rejouer avant exécution |
| Suppression de `fenetre_ouverte_etage` masque une info utile | Faible | Elle ne bloque rien (vérifié) ; sa présence était le faux positif |

Aucun risque ne porte sur la décision : par construction, rien dans ce plan n'écrit dans
la chaîne autorisation → admissibilité → target_mode → exécution.

---

## 6. ORDRE D'IMPLÉMENTATION RECOMMANDÉ

1. **F2 — `clim_bloquee`** : autonome, gain D3 immédiat, aucune dépendance de mapping.
2. **F3 — `action_en_cours`** : autonome, gain D7 immédiat.
3. **F1 + F5 + F6 ensemble** : F1 introduit les nouveaux codes ; F5 (status_72) et F6
   (carte_decision) doivent les traduire/consommer **dans le même déploiement** pour qu'aucun
   code brut n'apparaisse. Backend (F1) chargé avant rechargement des cartes.
4. **F4 — `clim_blocages_synthese_xl`** : autonome, gain D3/D6 ; lit des capteurs existants.

Vérification finale après chaque étape : provoquer chaque cause COOL (aération étage,
fenêtre, horaire, absence prolongée, temp ext) et confirmer que raison, voyant et carte
disent désormais **la même chose que `autorisation_clim_cool`**. Tant que l'un d'eux
diverge, le mensonge subsiste.

---

## 7. DIAGNOSTIC FINAL DU CHANTIER

Le mensonge est **structurel et localisé** : l'observabilité COOL a été construite à partir
d'un jeu de signaux distinct de celui qui décide réellement (versions brutes des fenêtres,
oubli de l'aération étage et de l'absence prolongée, blocage poêle mal contextualisé,
recalcul horaire côté client). La décision, elle, est correcte.

Le chantier consiste donc **uniquement** à reconnecter 6 artefacts d'observabilité (3
capteurs diagnostic + 3 cartes) aux mêmes entrées que `autorisation_clim_cool`. Aucune
entité de décision, aucun automatisme, aucun script n'est touché ; la preuve d'innocuité
runtime est rejouable (§0). À l'issue, toute situation « runtime vrai / UI faux » sur le
COOL disparaît, sans qu'aucune dette nouvelle ne soit ouverte.
