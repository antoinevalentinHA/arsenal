# ARSENAL — État de couverture normative des domaines fonctionnels

- **Périmètre :** `00_documentation_arsenal/contrats/` × domaines fonctionnels runtime (`10_scripts/`, `11_automations/`, `12_template_sensors/`, `14/15_mqtt_*`, `18_lovelace/`)
- **Type :** audit documentaire de couverture normative — **lecture seule**
- **Branche / commit observé :** `main` @ `20d909dff6bd87472fed20e4556abfc245c3055f` (2026-06-06)
- **Date du rapport :** 2026-06-07
- **Méthode :** inventaire `contrats/` (chemins, tailles, statuts déclarés) → inventaire des domaines runtime → croisement couverture/normatif → audit des marqueurs non-normatifs et des fichiers vides. Aucun fichier modifié, créé ou supprimé hors le présent rapport ; aucun contrat touché ; aucun patch de correction produit.

---

## 1. Périmètre

**Dépôt audité :** `https://github.com/antoinevalentinHA/arsenal.git`
**Branche / commit :** `main` @ `20d909df` (working tree propre au moment de l'audit).

**Périmètres comparés :**
- la **documentation normative** : arborescence `00_documentation_arsenal/contrats/` ;
- la **réalité runtime** : domaines effectivement présents dans `10_scripts/`, `11_automations/`, `12_template_sensors/`, `14_mqtt_sensors/`, `15_mqtt_binary_sensors/`, `18_lovelace/`, `19_button_card_templates/`.

**Distinction des natures de documentation** (axe central de cet audit) :
- **Documentation normative** = un contrat opposable situé dans `contrats/`, doté d'un statut (`normatif`, `opposable`, `clos`). Seule cette nature qualifie une couverture.
- **Documentation d'architecture** = `00_documentation_arsenal/architecture/` (descriptif, non opposable).
- **Navigation** = `contrats/index.md`, `contrats/README.md`, `00_documentation_arsenal/navigation/` (indice de couverture, **jamais** preuve normative).
- **Preuve runtime** = présence d'automations / scripts / template_sensors / entités. Prouve l'**existence** d'un domaine, pas sa documentation.

**Note de vérification :** tous les éléments de l'audit précédent ont été re-contrôlés sur le `main` actuel (`20d909df`). Aucun ne se révèle invalide ou contredit. Les comptages de lignes/octets et les statuts cités ci-dessous proviennent de ce commit.

---

## 2. Synthèse exécutive

**Niveau global de couverture : élevé et sain.** La quasi-totalité des domaines fonctionnels actifs dispose d'un contrat normatif et opposable. Aucun trou critique sur un domaine de sûreté (chauffage, ECS, alarme, boiler, pannes, climatisation sont tous couverts).

**Principaux trous documentaires (preuve forte d'absence) :**
- `reveils` (dont `babyphone`) — aucune documentation ;
- `electromenager` — aucune documentation ;
- `boutons` physiques — aucune documentation dédiée.

**Domaines partiellement / indirectement couverts :** `poele` (détection contractée côté chauffage, cycle propre non contracté), `couleurs` (documenté en `architecture/` et `ui/`, hors `contrats/`), `modes/normal` (couvert indirectement par `vacances.md`), `statistiques` (couche transversale sans contrat dédié).

**Documents draft / pré-normatifs :** `sante/sommeil.md` (v0.9 draft), `meteo/extrema_jour_courant.md` (pré-normatif v0.1.0), `meteo/fallback.md` (à consolider) ; plus deux stubs/TODO localisés (`chauffage/15_capteurs/12_capteurs_observabilite_pure.md`, section 12 de `deshumidificateur/guard.md`).

**Fichiers vides ou placeholders :** un seul cas trompeur réel — `chauffage/15_capteurs/05_capteurs_parametrage_canonique.md` (titre seul).

**Faux positifs assumés :** renvois explicites (`chauffage/45_aeration.md`, `alarme/51_ouvrants_entree.md`) et contrats courts mais complets (`climatisation/11_perimetre_exclu.md`, `energie.md`) — à ne pas traiter comme anomalies.

---

## 3. Domaines correctement couverts

Domaines disposant d'une couverture normative suffisante dans `contrats/` :

chauffage (52 fichiers) · ECS (28) · bouclage (`bouclage.md`, contrat canonique) · climatisation (39) · alarme (15) · aération (`aeration_blocage_chauffage/` + `aeration_recommandation.md`) · météo (16 ; axes, palmarès chaud/froid `normatif`, validation, gouvernance) · éclairage (5) · boiler (7) · présence · vacances · visite · babysitting · simulation_presence · mobile high-accuracy contextuel · bssid · zones · ouvertures (3) · pannes (internet + secteur) · VMC · volets/pluie · déshumidificateur (couvre la cave) · voiture · bluetti (`energie_chaudiere`) · batteries · cumulus petite-maison/studio · energie · switchbot · notifications · homekit_diagnostic · ups · ping_lan · mouvements · imprimerie (bruit machines Baillet) · arsenal_nas · arsenal_self · ressources_lovelace · parametres_invalides · publication/sécurité Git.

---

## 4. Domaines partiellement ou indirectement couverts

| Domaine | Preuve runtime | Documentation existante | Limite constatée | Décision / action recommandée |
|---|---|---|---|---|
| **poele** | `11_automations/poele/` (6 automations : `activation/extinction_memoire_24h`, `application_duree_blocage_poele`, `blocage_chauffage`, `fin_blocage_chauffage`, `securite_demarrage`) + `12_template_sensors/poele/` (`detection`, `capteur_stabilise`) | Détection et signature contractées **côté chauffage** : `chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_en_fonction.md` et `signature_thermique_poele.md` (30 fichiers `contrats/` mentionnent le poêle) | Le cycle de vie propre du poêle (mémoire 24 h, sécurité démarrage, durée de blocage) n'a **pas de contrat souverain** ; il n'est documenté que depuis le consommateur chauffage | **P2** — soit créer un contrat souverain `poele.md`, soit acter formellement la couverture indirecte par un renvoi explicite depuis le chauffage |
| **couleurs** | `12_template_sensors/couleurs/` (boiler_modulation, redondance_contacts, intégrations, meteo, sante, systeme, temperature_ecs, uptime) | `architecture/capteurs_couleur.md` + `ui/couleurs/` | Documenté **hors `contrats/`** ; cartographie descriptive, non opposable | **P3** — décision : maintien assumé en `architecture/` (probable) + renvoi depuis `contrats/index.md` ; pas de contrat métier requis |
| **modes/normal** | `11_automations/modes/normal.yaml` (« Restauration du contexte global » en sortie de Vacances) | Couvert fonctionnellement par `vacances.md` (le mode Normal réactive ce que Vacances suspend) | Pas de contrat « modes » dédié ; couverture par effet de bord du contrat vacances | **P4** — ajouter un renvoi explicite depuis `vacances.md` ; pas de contrat séparé nécessaire |
| **statistiques** | `12_template_sensors/statistiques/` (`filtres/`, `seuils_dynamiques/`) + `13_sensor_platforms/statistics/` | Aucune documentation dédiée | Couche transversale ; impossible de trancher gap métier vs infrastructure sans analyse complémentaire | **P3** — qualifier (infra transversale vs domaine) avant de décider d'un contrat |

---

## 5. Domaines non documentés

| Domaine | Preuve runtime | Documentation | Priorité | Action recommandée |
|---|---|---|---|---|
| **reveils / babyphone** | `11_automations/reveils/` : `compteurs/{matthieu,arnaud}.yaml`, `babyphone/{matthieu,arnaud}.yaml`, `reset/{matthieu,arnaud}.yaml` | **0 mention** dans `contrats/` (ni `reveil`, ni `babyphone`) | **P1** | Créer un contrat racine `reveils.md` ; prioriser le sous-domaine `babyphone` (surveillance, potentiellement sensible) |
| **electromenager** | `11_automations/electromenager/` : `buanderie/`, `lave_vaisselle/`, `yaourts_3h.yaml` | **0 mention** dans tout `00_documentation_arsenal/` | **P2** | Créer un contrat léger `electromenager.md` (faible criticité, mais domaine actif non documenté) |
| **boutons** (physiques) | `11_automations/boutons/` : `cuisine.yaml`, `entree.yaml`, `sdb.yaml` | Aucune doc dédiée ; recouvrement indirect possible avec l'éclairage | **P3** | Rattacher explicitement aux contrats `eclairage/` concernés, ou créer un stub de renvoi |

---

## 6. Contrats draft / non normatifs / à compléter

| Chemin | Indice détecté | Diagnostic | Priorité | Action recommandée |
|---|---|---|---|---|
| `contrats/sante/sommeil.md` | L1 : `# CONTRAT_SOMMEIL_WITHINGS — v0.9 (draft, non validé)` | Draft explicite porté par le titre ; contrat de fond substantiel (211 l) mais non validé | **P2** | Valider et figer en v1.0, ou marquer chantier ouvert et tracer dans l'index |
| `contrats/meteo/extrema_jour_courant.md` | L4 : `Statut : pré-normatif — à figer avant toute phase d'implémentation` (v0.1.0) | Pré-contrat assumé, complet (509 l), en attente de promotion | **P2** | Promouvoir en v1.0 après / pendant l'implémentation ; statut intentionnel |
| `contrats/meteo/fallback.md` | L4 : `Le contenu normatif détaillé reste à consolider.` | Stub de continuité créé pour la navigation ; squelette + références | **P2** | Consolider, ou fusionner dans `meteo/validation.md` / `meteo/gouvernance.md` |
| `contrats/chauffage/15_capteurs/12_capteurs_observabilite_pure.md` | L3–4 : `Statut : fichier vide détecté lors du lint documentaire. Contenu à compléter ou suppression à arbitrer` | Stub auto-déclaré vide (honnête) | **P3** | Arbitrer : compléter le contenu ou supprimer dans un chantier dédié |
| `contrats/sante/cardio_nuit.md` | L4 : `Statut : READY FOR IMPLEMENTATION` (v2.0.2) ; L23 : renvoi `CONTRAT_ALERTE_SANTE.md, à créer` | Contrat complet mais statut pré-implémentation, non « normatif/clos » ; renvoi vers un contrat inexistant | **P3** | Figer le statut (clos/normatif) et créer ou retirer le renvoi `CONTRAT_ALERTE_SANTE.md` |
| `contrats/deshumidificateur/guard.md` | L184 : `## 12. Helpers diagnostiques à créer` | Section TODO (table d'`input_text`) au sein d'un contrat par ailleurs actif | **P3** | Créer les helpers listés ou les marquer explicitement optionnels |
| `contrats/climatisation/capteurs/{admissibilite manquant→}{autorisations,besoins,blocages,coherence,decision}/90_observations.md` (×5) | L4 : `> **Document non-normatif.**` | Annexes d'observation **non-normatives par design** | **P4** | Conserver ; statut assumé, pas une anomalie |
| `contrats/chauffage/60_absence_inhibition_geofencing.md` | L247/266/327 : `non normatif` | Déclaration de **dépréciation** d'un helper (`input_boolean.blocage_geofencing`) | faux positif | Conserver ; déclaration normative correcte |
| `contrats/meteo/palmares_chaleur.md`, `palmares_froid.md` | Changelog : `Brouillon … initial` | Mention **historique** en changelog ; en-tête courant = `Statut : normatif` (v1.2 / v1.0.2) | faux positif | Aucune action |

---

## 7. Fichiers vides / quasi vides / placeholders

| Chemin | Taille / lignes utiles | Diagnostic | Recommandation |
|---|---|---|---|
| `contrats/chauffage/15_capteurs/05_capteurs_parametrage_canonique.md` | 38 o / 1 ligne / **0 utile** (titre seul) | **Vide réel — fausse impression de couverture** ; cas connu confirmé | Compléter, **ou** supprimer / transformer en stub assumé avec statut clair (à l'image du fichier `12`) |
| `contrats/chauffage/15_capteurs/12_capteurs_observabilite_pure.md` | 169 o / 3 lignes / ~0 utile | Placeholder auto-déclaré (statut « fichier vide ») | Arbitrer : compléter ou supprimer dans un chantier dédié |
| `contrats/meteo/fallback.md` | 503 o / 16 lignes / ~6 utiles | Stub de continuité, contenu normatif non consolidé | Consolider ou fusionner |
| `contrats/chauffage/45_aeration.md` | 276 o / 7 lignes | Renvoi explicite (« ne constitue plus une source contractuelle active ») | Conserver comme renvoi (voir §8) |
| `contrats/alarme/51_ouvrants_entree.md` | 565 o / 21 lignes | Renvoi canonique vers `ouvertures/` | Conserver comme renvoi (voir §8) |
| `contrats/climatisation/11_perimetre_exclu.md` | 630 o / 20 lignes | Contrat court mais **complet et normatif** (v1.2) | Conserver — faux positif (voir §8) |
| `contrats/energie.md` | 907 o / 32 lignes | Contrat court mais **complet et normatif** | Conserver — faux positif (voir §8) |

---

## 8. Faux positifs / fichiers courts assumés

| Chemin | Pourquoi ce n'est pas une anomalie | Décision recommandée |
|---|---|---|
| `contrats/chauffage/45_aeration.md` | Renvoi explicite : le contrat normatif a été externalisé vers `aeration_blocage_chauffage/` ; le fichier déclare ne plus être une source contractuelle active | Conserver tel quel (renvoi assumé) |
| `contrats/alarme/51_ouvrants_entree.md` | Renvoi canonique : la définition normative des ouvrants est centralisée dans `ouvertures/` ; le fichier l'affirme et interdit toute norme locale | Conserver tel quel (renvoi assumé) |
| `contrats/climatisation/11_perimetre_exclu.md` | Contrat « périmètre exclu » v1.2 complet : énonce explicitement ce que le système ne fait pas. Court ≠ incomplet | Conserver (normatif) |
| `contrats/energie.md` | Contrat court mais complet : intention, règle fonctionnelle, sources interdites, invariant « non négociable » | Conserver (normatif) |
| `contrats/climatisation/capteurs/*/90_observations.md` (×5) | Annexes d'observation explicitement marquées non-normatives ; couche descriptive par design | Conserver (statut assumé) |
| `contrats/publication/securite_publication_git.md` | Le terme `placeholder` y est du **vocabulaire métier** (détection de secrets factices par le scanner), pas un statut de document | Aucune action |

---

## 9. Priorisation des prochains chantiers

**P1 — trous normatifs réels ou fichiers trompeurs :**
1. `chauffage/15_capteurs/05_capteurs_parametrage_canonique.md` : supprimer la fausse couverture (compléter, supprimer, ou stub assumé).
2. `reveils.md` (dont `babyphone`) : créer le contrat racine du domaine non documenté.

**P2 — contrats draft ou domaines partiellement couverts :**
3. `sante/sommeil.md` v0.9 → figer en v1.0.
4. `meteo/extrema_jour_courant.md` → promouvoir après implémentation.
5. `meteo/fallback.md` → consolider ou fusionner.
6. `electromenager.md` : créer un contrat léger.
7. `poele` : contrat souverain `poele.md` **ou** renvoi explicite acté depuis le chauffage.

**P3 — consolidation / clarification :**
8. `deshumidificateur/guard.md §12` : créer les helpers ou les marquer optionnels.
9. `sante/cardio_nuit.md` : figer le statut + traiter le renvoi `CONTRAT_ALERTE_SANTE.md`.
10. `couleurs`, `boutons`, `statistiques` : acter le rattachement (architecture / éclairage / infra) ou poser des stubs de renvoi.

**P4 — faux positifs ou faible urgence :**
11. `modes/normal` : simple renvoi depuis `vacances.md`.
12. Renvois et contrats courts du §8 : aucune action (à exclure des futurs lints comme assumés).

**Vérifications à lancer ensuite :**
- Étendre le lint documentaire (qui a déjà détecté `12_capteurs_observabilite_pure`) pour flaguer tout `.md` de `contrats/` ≤ 2 lignes utiles **hors renvoi explicite déclaré**.
- Croiser en CI `11_automations/<domaine>/` ↔ `contrats/index.md` : tout sous-dossier d'automation sans entrée d'index → warning (aurait capté `electromenager`, `reveils`).

---

## 10. Listes compactes finales

### A. `DOMAINES_NON_DOCUMENTES`

```
P1 | reveils (dont babyphone) | 11_automations/reveils/{compteurs,babyphone,reset}/{matthieu,arnaud}.yaml | 0 mention dans contrats/ | creer contrat racine reveils.md, prioriser babyphone
P2 | electromenager           | 11_automations/electromenager/{buanderie,lave_vaisselle,yaourts_3h} | 0 mention dans 00_documentation_arsenal/ | creer contrat leger electromenager.md
P2 | poele                    | 11_automations/poele/* + 12_template_sensors/poele/* | detection contractee cote chauffage, cycle propre non contracte | contrat souverain poele.md OU renvoi explicite acte
P3 | couleurs (capteurs UI)   | 12_template_sensors/couleurs/* | documente en architecture/+ui/, hors contrats/ | acter localisation + renvoi depuis index
P3 | boutons physiques        | 11_automations/boutons/{cuisine,entree,sdb} | aucune doc dediee | rattacher a eclairage ou stub de renvoi
P3 | statistiques             | 12_template_sensors/statistiques/{filtres,seuils_dynamiques} | aucune doc dediee | qualifier infra vs domaine
P4 | modes/normal             | 11_automations/modes/normal.yaml | couvert indirectement par vacances.md | renvoi explicite depuis vacances.md
```

### B. `CONTRATS_DRAFT_OU_NON_NORMATIFS`

```
P2 | contrats/sante/sommeil.md                                          | "v0.9 (draft, non valide)" (L1)            | draft explicite, contrat actif    | valider/figer v1.0 ou tag chantier
P2 | contrats/meteo/extrema_jour_courant.md                             | "Statut: pre-normatif — a figer" (L4)      | pre-contrat assume v0.1.0         | promouvoir v1.0 apres implementation
P2 | contrats/meteo/fallback.md                                         | "reste a consolider" (L4)                  | stub de continuite                | consolider/fusionner
P3 | contrats/chauffage/15_capteurs/12_capteurs_observabilite_pure.md   | "fichier vide ... a completer ou suppression a arbitrer" | stub declare vide   | arbitrer completer/supprimer
P3 | contrats/sante/cardio_nuit.md                                      | "READY FOR IMPLEMENTATION" + renvoi mort   | statut pre-impl + lien inexistant | figer statut + creer/retirer renvoi
P3 | contrats/deshumidificateur/guard.md                                | "## 12. Helpers diagnostiques a creer" (L184) | TODO dans contrat actif        | creer helpers ou marquer optionnels
P4 | contrats/climatisation/capteurs/*/90_observations.md (x5)          | "Document non-normatif." (L4)              | annexes non-normatives par design | conserver (faux positif)
```

### C. `FICHIERS_VIDES_OU_PLACEHOLDERS`

```
P1 | contrats/chauffage/15_capteurs/05_capteurs_parametrage_canonique.md | 38 o / 1 ligne / 0 utile      | titre seul, fausse couverture | completer OU supprimer/stub assume
P3 | contrats/chauffage/15_capteurs/12_capteurs_observabilite_pure.md    | 169 o / 3 lignes / ~0 utile   | placeholder auto-declare       | arbitrer completer/supprimer
P2 | contrats/meteo/fallback.md                                         | 503 o / 16 lignes / ~6 utiles | stub draft                     | consolider/fusionner
P4 | contrats/chauffage/45_aeration.md                                  | 276 o / 7 lignes              | renvoi assume (source inactive)| conserver comme renvoi
P4 | contrats/alarme/51_ouvrants_entree.md                              | 565 o / 21 lignes             | renvoi canonique assume        | conserver
-- | contrats/climatisation/11_perimetre_exclu.md                       | 630 o / 20 lignes             | complet normatif               | FAUX POSITIF — conserver
-- | contrats/energie.md                                                | 907 o / 32 lignes             | complet normatif               | FAUX POSITIF — conserver
```

---

*Audit en lecture seule. Aucun contrat modifié, aucun fichier vide corrigé, aucun script touché, aucun contrat métier créé. Le présent rapport est le seul fichier ajouté.*
