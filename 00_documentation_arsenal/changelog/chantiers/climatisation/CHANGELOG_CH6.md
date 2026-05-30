# Arsenal — Changelog du chantier CH-6

**Chantier** : CH-6 — Éclatement des registres UI + promotion `confort_suffisant` (Chauffage)
**Domaine** : Chauffage
**Date** : 2026-05-30
**État** : clos — dette D4 soldée, 0 modification de comportement runtime, 0 invariant CI

---

## Résumé architectural

CH-6 solde la dette **D4** : registres UI du chauffage aplatis (causes hétérogènes
affichées sous un libellé générique « Bloqué ») et `confort_suffisant` resté
libellé plutôt que catégorie.

Le chantier introduit une **source unique de correspondance** côté UI — le socle
de données `chauffage_registres_raison` — consommée par les trois briques
pivots, supprimant les mappings divergents. Il aligne la taxonomie UI sur la
doctrine des registres (`01_doctrine_registres.md`, D4) et sur la charte couleur
(`ui/couleurs/`), inscrit l'**invariant couleur** comme référence d'interprétation,
éclate les causes Sécurité, retire les branches UI mortes héritées de CH-2, et
corrige une mention de commentaire périmée dans `raison.yaml`.

Chantier **UI / documentaire** : **sans CI** (aucun invariant ajouté) et **sans
modification de comportement runtime** (seule édition en arbre runtime : un
commentaire). Les couleurs des jetons vivants sont iso à l'existant, à l'unique
exception voulue de `pre_confort_vacances`.

---

## 1. Source unique de correspondance — socle `chauffage_registres_raison`

### Nouveau socle de données
`19_button_card_templates/40_dashboards/chauffage/00_donnees/chauffage_registres_raison.yaml`

Template button-card **sans rendu propre**, portant un bloc `variables` statique :
un objet `registre_chauffage` indexé par jeton de raison, chaque entrée valant
`{ registre, libellé court, libellé long, icône, couleur }`. Valeurs littérales,
aucune expression `[[[ ]]]` : table de correspondance pure, ni calcul ni décision.

Couverture **exacte** des douze jetons émis par `sensor.chauffage_raison_calculee` :
`confort_force`, `aeration_en_cours`, `blocage_aeration_en_cours`,
`fenetre_ouverte_maison`, `mode_maison_vacances`, `pre_confort_vacances`,
`poele_actif`, `stabilisation_absence`, `besoin_thermique`, `confort_suffisant`,
`presence_on`, `absence`.

Objectif métier : définir **une seule fois** côté UI la traduction d'une raison
en libellé/icône/couleur, et faire consommer cette table par les briques via
l'héritage `template: [...]`.

---

## 2. Invariant couleur (référence d'interprétation de la table)

Inscrit en en-tête du socle **et** dans le présent changelog :

> **La couleur traduit la nature métier observable du chauffage pour
> l'utilisateur. Elle ne traduit ni le registre, ni le contexte, ni le
> `desired_mode`.**

Illustrations portées par la table :
- `mode_maison_vacances` et `pre_confort_vacances` partagent le registre
  « Contexte majeur » mais diffèrent en couleur (Bleu vs Vert) ;
- `stabilisation_absence` et `besoin_thermique` produisent tous deux
  `desired_mode = comfort` mais diffèrent en couleur (Bleu vs Vert).

---

## 3. Migration des trois briques pivots

Chaque brique hérite désormais du socle (`template: [socle_visuel,
chauffage_registres_raison]`) et lit `variables.registre_chauffage`. Aucune map
de libellés inline ne subsiste.

### `chauffage_diagnostic_global_compact`
Icône, libellé court (`state_display`), libellé long (`label`) et couleur tirés
de la table. Surcouche **indisponibilité** (gris `0.1`, prioritaire) conservée.

### `carte_chauffage_decision`
Libellé de raison (`reason_txt`) et couleur tirés de la table. Surcouche propre
**cohérence intention ≠ réel → rouge** (prioritaire, `05_regles.md`) conservée à
l'identique.

### `carte_chauffage_synthese`
Libellés (`state_display`, `label`) tirés de la table ; surcouches **brûleur**,
**programme** et **consigne** préservées ; icône d'activité (brûleur/programme)
conservée hors table. La **couleur** reste portée par le bloc `state` button-card,
strictement **alignée** sur la table : ce bloc encode une précédence propre à
synthese (brûleur > raison > programme) validée en production, non collapsée
dans un template socle par choix de sécurité (option B retenue à l'arbitrage).
Conséquence assumée : la couleur est définie une fois pour `compact` et
`decision`, et reste alignée mais inline pour `synthese`.

---

## 4. Éclatement des causes Sécurité

Les trois causes Sécurité — `aeration_en_cours` (« Aération »),
`blocage_aeration_en_cours` (« Post-aération ») et `fenetre_ouverte_maison`
(« Fenêtre ouverte ») — sont désormais affichées **distinctement** sur les trois
briques. Le libellé générique « Bloqué » est supprimé.

Cet éclatement est rendu observable par le runtime corrigé en CH-2 : la cascade
émet `blocage_aeration_en_cours` (branche ranimée), permettant au cas
post-aération d'apparaître comme tel et non sous une étiquette d'interdiction.

---

## 5. Retrait des branches UI mortes

Les branches `chauffage_non_autorise` / `securite_systeme` sont retirées des
trois briques. Le jeton `chauffage_non_autorise` n'est **plus émis depuis CH-2** ;
ces branches étaient donc structurellement présentes mais logiquement
inatteignables — pendant UI de la pathologie D2. Leur retrait ne modifie aucun
rendu atteignable (iso pour les jetons vivants).

---

## 6. Couleur — alignement doctrine D4 + charte

- Abandon de la taxonomie parallèle `securite_systeme` / `securite_limite`, qui
  n'existait pas dans la doctrine ; ralliement au registre **Sécurité** unique
  (les trois causes restant distinguées par le **libellé**, pas par des registres
  parallèles).
- Couleurs strictement issues de `ui/couleurs/02_palette.md` ; priorités de
  `05_regles.md` respectées (indisponibilité prioritaire ; incohérence rouge).
- **`pre_confort_vacances` promu Bleu → Vert** selon la nature métier observable :
  lorsqu'il est émis, `desired_mode = comfort` — le chauffage **remonte
  activement vers le confort** en anticipation du retour, un état favorable
  engagé, distinct du régime réduit passif de `mode_maison_vacances` (qui reste
  Bleu). Conforme à l'invariant couleur (§2).
- `confort_suffisant` est présenté comme **catégorie nominale propre** (déjà le
  cas dans `compact`, généralisé via la table).

---

## 7. Runtime

Aucun fichier de logique runtime n'est modifié : `10_scripts/chauffage/`,
`11_automations/chauffage/` et la logique des `12_template_sensors/chauffage/`
sont intacts.

**Seule édition en arbre runtime** : le commentaire d'en-tête de
`12_template_sensors/chauffage/diagnostic/raison.yaml` (bloc « Hiérarchie des
causes »), où la mention résiduelle « Chauffage non autorisé système » devient
« (Niveau 1 réservé — aucune cause émise) ». La cascade `state` est inchangée
octet pour octet ; `sensor.chauffage_raison_calculee` émet des états identiques.
Aucun effet thermique ni comportemental.

---

## 8. Hors périmètre (explicite)

- **`carte_chauffage_intention.yaml`** : non touché — ne porte ni bloc « Bloqué »
  ni branche morte ; il contextualise seulement l'intention Eco.
- **Gris indisponibilité** (`synthese`, `decision`) : non-conformité préexistante
  (`05_regles.md`) **non régressée** par CH-6 et **non corrigée** ici — versée à
  une **dette UI distincte**, à traiter séparément (`compact` y est déjà conforme).
- **Garde CI d'exhaustivité** (tout jeton de `raison.yaml` couvert par la table) :
  **différée** — CH-6 reste un chantier UI/documentaire, sans CI.
- **`decision_centrale.yaml` (commentaire résiduel `chauffage_non_autorise`)** :
  même nature que le commentaire de `raison.yaml` mais **hors périmètre** —
  versé au lot « dérive documentaire » distinct.
- **Fixture D2** (`d2_reason_pre_correction.yaml`) : conserve volontairement
  `chauffage_non_autorise` (contrôle positif gelé de R-COV-1/R-CAUSE-1) — intacte.
- **Charte `ui/couleurs/`** : non modifiée ; l'invariant couleur est inscrit
  uniquement dans le socle et dans ce changelog.

---

## État de validation

- **C1** (socle), **C2** (`compact`), **C3** (`decision`), **C4** (`synthese`),
  **C5** (commentaire `raison.yaml`) appliqués et poussés.
- **C2, C3, C4 validés en rendu réel Home Assistant** : héritage multi-template et
  lecture de la variable-objet opérationnels ; libellés éclatés ; `pre_confort`
  vert ; surcouches brûleur/programme/consigne, cohérence-KO et indisponibilité
  préservées ; aucune anomalie visuelle ; aucun `undefined`.
- **C5** : diff limité à un commentaire ; cascade `state` prouvée identique octet
  pour octet ; capteur inchangé.
- YAML valide sur les quatre fichiers UI ; couverture exacte des douze jetons ;
  aucune map de libellés inline résiduelle dans les briques.
- Runtime, fixture D2, contrats, CI : intacts.

---

## Clôture du chantier CH-6

CH-6 est clos. La dette D4 est soldée : les registres UI du chauffage sont
éclatés, `confort_suffisant` est une catégorie, et la traduction
raison → libellé / icône / couleur est définie une seule fois via le socle
`chauffage_registres_raison`, consommé par les trois briques. Les branches UI
mortes sont retirées, la taxonomie et les couleurs sont alignées sur la doctrine
D4 et la charte, et l'invariant couleur est inscrit comme référence
d'interprétation. Le runtime est inchangé hors une correction de commentaire.

Trois frontières restent ouvertes, toutes versées à des dettes distinctes et
non bloquantes : le gris indisponibilité (`synthese`, `decision`), la garde CI
d'exhaustivité de la table, et le commentaire résiduel de `decision_centrale.yaml`.
La couleur de `synthese` demeure portée par son bloc `state` (alignée sur la
table) : la complétion du single-source couleur n'a pas été poursuivie, par
choix de sécurité assumé.
