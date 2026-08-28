# Références aux contrats Arsenal — **V3**

Chemins **relatifs à la racine du dépôt Arsenal**, à la révision
`112ad3c3d64a619f8ec883dcd645ec0187d884bb`.

> **Corrections V2.** Deux contrôles manquaient à la table (`ASP-CI-19`, et les
> deux checkers transverses du registre de couverture et des clés initiales) ;
> la portée exacte de chaque contrôle est désormais énoncée ; et la
> « conclusion opposable » du §3, juste pour la conduite, était **fausse pour
> la Maintenance**.

> **Corrections V3.** `ASP-INV-65` était **mal attribué** — l'atteignabilité
> relève de `ASP-CI-18`, pas d'un invariant (`N-4`) ; la portée de `ASP-CI-11`
> était **sur-déclarée** (`N-5`) ; `ASP-CI-3` est ajouté à la table, et son piège de
> rédaction est porté au lot L2.

---

## 1. Contrat du domaine Aspirateur

Répertoire : `00_documentation_arsenal/contrats/aspirateur/`
Quatorze fichiers, dont un index.

| Fichier | Ce qu'il fixe, utile ici |
|---|---|
| `01_finalite_et_perimetre.md` | Finalité, gestes obligatoires, autorité du mouvement |
| `02_referentiel_cartes_et_pieces.md` | Table canonique des segments — **quatorze commandables** : 4 pour la carte 0, 8 pour la carte 1, 2 pour la carte 2 |
| `03_profils_metier.md` | **Cinq profils** ; prérequis matériel de la serpillière |
| `04_nombre_de_passages.md` | Convention de passages, arbitrage `ARB-4` |
| `05_intention_de_mission.md` | Atomicité de l'intention |
| `06_integrite_mono_carte.md` | `ASP-IMC-1` — confirmation cartographique avant chaque mission |
| `07_moteur_de_mission.md` | Séquence, partition d'états §5.0, valeurs nominales des témoins d'erreur §5.2, fenêtres §3.1, **conduite §7**, **reprise §7.1** |
| `08_etats_et_observation.md` | Dix états canoniques, autorité des témoins §2, témoin de session §3, sens physique §4, **§6 : exclusion des consommables** |
| `09_refus_et_diagnostics.md` | **Catalogue opposable — 18 codes** |
| `10_raccourcis.md` | **Cinq raccourcis** ; `ASP-INV-56` |
| `11_frontiere_ui.md` | Interdits et obligations opposables à l'interface |
| `12_identifiants_a_fournir.md` | Rôles abstraits ; `ASP-INV-58`, `ASP-INV-59` |
| `13_hors_perimetre_arbitrages_et_questions_ouvertes.md` | `ARB-1` à `ARB-5`, `QO-1` à `QO-6` |

### Invariants mobilisés par ce cadrage

| Invariant | Ce qu'il impose, en une ligne |
|---|---|
| `ASP-INV-6` | Un segment se désigne par une **paire carte/segment**, jamais un index nu |
| `ASP-INV-7` | Aucun libellé issu de l'appareil n'est restitué |
| `ASP-INV-13` | Un profil dont le prérequis matériel manque n'est pas proposé |
| `ASP-INV-14` | Les réglages sont écrits **avant chaque mission** |
| `ASP-INV-15` | La trace d'intention n'est jamais relue depuis l'appareil |
| `ASP-INV-16` | L'interface représente l'**intention**, jamais l'état de l'appareil |
| `ASP-INV-23` | L'intention est **atomique** — quatre champs reçus ensemble |
| `ASP-INV-31` | **Écrivain unique** vers l'appareil |
| `ASP-INV-38` | L'acceptation d'une commande n'est **jamais** un démarrage |
| `ASP-INV-39` | Aucune réémission ; la relance est un geste opérateur |
| `ASP-INV-42` | Les gestes de conduite passent **exclusivement** par le moteur |
| `ASP-INV-43` | Asymétrie arrêt/lancement — on n'empêche pas l'arrêt |
| `ASP-INV-44` | Les dix états sont exposés **distinctement**, sans agrégation |
| `ASP-INV-45` | L'indisponibilité est un **état**, pas un trou |
| `ASP-INV-46` | La garde anti-double-lancement s'appuie sur l'**état machine** |
| `ASP-INV-47` | Le témoin de session n'est **jamais** une preuve de mouvement |
| `ASP-INV-48` | Un geste n'est proposé que s'il a un **sens physique** |
| `ASP-INV-49` | **Aucun silence** — toute mission produit une issue explicite |
| `ASP-INV-50` | Le refus est un **livrable**, avec motif lisible |
| `ASP-INV-52` | Le vocabulaire ne s'étend que par acte contractuel |
| `ASP-INV-56` | Un raccourci ne présume **ni** le profil **ni** les passages |
| `ASP-INV-58` | **Aucun identifiant inventé** par le contrat |
| `ASP-INV-59` | Le préfixe d'identifiant d'automation relève d'un geste opérateur |
| `ASP-INV-60` | Une valeur d'état non classée **refuse** par défaut |
| `ASP-INV-62` | **Reprise autorisée sous garde fermée** — seule voie de `vacuum.start` |
| `ASP-INV-64` | Arbitrage déterministe entre deux refus concurrents |
| `ASP-INV-65` | **Le catalogue est total sur l'état machine** — c'est son énoncé réel |
| `ASP-INV-68` | Le modèle d'états est **total** sur la partition |
| `ASP-INV-69` | **Deux constantes temporelles**, et deux seulement |
| `ASP-INV-70` | Vocabulaire de cycle de vie du verdict, **fermé, énuméré au runtime et mécaniquement confronté**, et **distinct** du catalogue |

### Trois exigences à ne jamais confondre — **corrigé en V3**

> La V2 énonçait `ASP-INV-65` comme « le vocabulaire fermé doit être
> intégralement atteignable ». **C'est faux** : cet invariant dit tout autre
> chose, et le mot « atteignable » n'apparaît dans aucun des quatorze fichiers
> du contrat au sens où la V2 l'employait.
>
> Le point est **matériel**, non cosmétique : toute la thèse de l'arbitrage
> **A-9** repose sur la distinction entre obligation **contractuelle** et
> exigence **mécanique de CI**. Attribuer à un invariant ce qui relève d'un
> checker affaiblissait précisément cette thèse.

| Exigence | Où elle vit | Ce qu'elle dit exactement |
|---|---|---|
| **`ASP-INV-65`** | Contrat, chapitre `09` | **Totalité du catalogue sur l'état machine** — aucune valeur d'état ne reste sans motif |
| **`ASP-INV-70`** | Contrat, chapitre `12` | Le vocabulaire de cycle de vie est **fermé**, **énuméré au runtime** et **mécaniquement confronté** ; il ne se confond jamais avec le catalogue |
| **`ASP-CI-18`** | Checker, **pas le contrat** | **Exigence mécanique d'atteignabilité** : toute valeur déclarée doit être **effectivement écrite**. C'est un contrôle, et son ancre contractuelle — s'il en faut une — est `ASP-INV-70`, jamais `ASP-INV-65` |
| `ASP-IMC-1` | Intégrité mono-carte |

### Arbitrages et questions ouvertes du contrat, cités ici

| Réf. | Objet |
|---|---|
| `ARB-1` | Partition fermée des états de lancement |
| `ARB-2` | Session inachevée, robot inactif ⇒ refus |
| `ARB-3` | Les deux fenêtres temporelles, **déclarées** par l'opérateur, non mesurées |
| `ARB-5` | Valeurs nominales des témoins d'erreur — `none` robot, `ok` dock, **déclarées** |
| `QO-1` | Deux segments de la carte 2 hors référentiel |
| `QO-5` | Historisation — arbitrage optionnel |

> `ARB-3` et `ARB-5` définissent le **régime de preuve par déclaration
> opérateur**, auquel se rattache la décision D-12 sur le vidage.

---

## 2. Contrats transverses

| Chemin | Ce qui est mobilisé |
|---|---|
| `00_documentation_arsenal/contrats/notifications.md` | Typologie état/événement ; correspondance canal ; test de recalculabilité forte ; événement déguisé ; format normatif du titre ; identité et unicité |
| `00_documentation_arsenal/architecture/03_doctrines/id_automatisations.md` | Structure préfixe + suffixe ; attribution avant codage ; jamais de recyclage |
| `00_documentation_arsenal/architecture/03_doctrines/prefixe_domaine_automatisations.md` | Contrat préfixe ↔ domaine propriétaire |
| `06_input_selects/system/prefix_id.yaml` | **Registre des préfixes, source de vérité de la doctrine.** Il porte déjà l'entrée du domaine `aspirateur` : l'identifiant acquis `10280000000001` est donc **bien formé** au regard des deux doctrines d'identifiants. *(Vérification ajoutée en V2 : la V1 ne la faisait pas.)* |
| `00_documentation_arsenal/architecture/03_doctrines/nommage_entites.md` | Nommage par représentation |
| `00_documentation_arsenal/architecture/03_doctrines/commandabilite.md` | §6.1 — un geste sans effet possible n'est pas présenté |
| `00_documentation_arsenal/architecture/03_doctrines/entetes_fichiers.md` | En-tête comme contrat local |
| `00_documentation_arsenal/architecture/03_doctrines/principes_generaux.md` | §6 et §8 — indisponibilité |
| `00_documentation_arsenal/ui/architecture_transverse.md` | Symétrie backend décide / interface rend |
| `00_documentation_arsenal/navigation/carte_domaines.md` | Registre des domaines — **non modifié** (décision D-35) |
| `00_documentation_arsenal/audits/REGISTRE_COUVERTURE_VERIFICATION.md` | Porte les compteurs de fichiers confrontés mécaniquement. **Un chapitre de contrat nouveau le fait dériver et casse la CI s'il n'est pas mis à jour dans le même lot** |

---

## 3. Contrôles de CI concernés

| Chemin | Rôle vis-à-vis de ce cadrage |
|---|---|
| `scripts/arsenal_contracts/check_aspirateur_contracts.py` | 27 contrôles. Voir le détail ci-dessous : `ASP-CI-7`, `10`, `11`, `14`, `18`, `19`, `20`, `21` |
| `scripts/arsenal_contracts/check_ci_coverage_registry.py` | **Compte les `.md` sous `00_documentation_arsenal/contrats/`** et confronte ce nombre aux chiffres en gras du registre de couverture. Toute dérive est une erreur dure. **Concerne directement le lot M0** |
| `scripts/arsenal_contracts/check_initial_key_contracts.py` | **`HINIT-002` interdit `initial` sur tout `input_boolean`**, en erreur dure et sans exception. **Ferme la voie native de remise à zéro des quatorze booléens de segment** |
| `scripts/arsenal_contracts/check_notifications_contracts.py` | `T1` emoji de tête · `T2` séparateur demi-cadratin · `T3` pas de formulation événementielle · `T4` pas de référence temporelle dans le bloc de création · `T5` unicité d'identifiant de notification · `T6` emoji des titres mobiles |
| `scripts/arsenal_contracts/check_lovelace_navigation_contracts.py` | `R1` clés de dashboard · `R2` cohérence du bouton retour · `R3` culs-de-sac |
| `scripts/arsenal_contracts/check_lovelace_no_inline_templating_contracts.py` | Applicable à la future carte Aspirateur |
| `scripts/arsenal_contracts/check_lovelace_grid_contracts.py` | idem |
| `scripts/arsenal_contracts/check_lovelace_section_headers_contracts.py` | idem |
| `scripts/arsenal_contracts/check_automation_ids_contracts.py` | Applicable aux futures automations |
| `.github/workflows/contracts_all.yml` | Enregistre le checker du domaine |

### Détail des contrôles du domaine, avec leur **portée exacte**

| Contrôle | Ce qu'il fait | Portée |
|---|---|---|
| **`ASP-CI-3`** | Refuse tout jeton entre accents graves de la forme `[A-Z][A-Z_]{4,}` **absent du catalogue** | les quatorze chapitres de contrat |
| **`ASP-CI-7`** | Refuse les entités natives d'**action** du robot et les noms de service | **`18_lovelace/` et `19_button_card_templates/` uniquement** |
| **`ASP-CI-10`** | Balaie les durées de **tous les chapitres** du domaine et n'admet que **30 s** et **60 s** | les quatorze chapitres de contrat |
| **`ASP-CI-11`** | Refuse, hors des cinq fichiers L1, les deux helpers de mission **et** les lignes `action:` / `service:` valant littéralement `vacuum.<x>` ou `roborock.<x>` | **1 772 fichiers sur 1 794** — voir l'encadré de portée ci-dessous |
| **`ASP-CI-14`** | Refuse un jeu fermé de voies interdites, dont la primitive de démarrage | **les cinq fichiers L1 uniquement** |
| **`ASP-CI-18`** | Ferme le vocabulaire de verdict, **recalcule le décompte** et le confronte au texte du fichier L1 ; exige `sorted(cycle) == CYCLE_DE_VIE` ; exige que **toute valeur soit atteignable**, c'est-à-dire réellement écrite | fichier L1 du vocabulaire + moteur |
| **`ASP-CI-19`** | Exige la traduction en motif lisible des **18 codes du catalogue et des 4 valeurs de cycle de vie** figées en constante de module | fichier L1 du motif lisible |
| **`ASP-CI-20`** | Trois fenêtres de 30 s et une de 60 s dans le moteur, et aucune autre temporisation | **les cinq fichiers L1 uniquement** |
| **`ASP-CI-21`** | Recalcule la marge de capacité et **confronte la table embarquée du moteur** aux tables du chapitre `02` | moteur |

### Portée réelle du balayage — **corrigé en V3**

Le chargeur employé par `ASP-CI-11` n'itère **que** les répertoires de premier
niveau dont le nom correspond à `^\d{2}_`.

| Mesure | Valeur |
|---|---|
| Fichiers YAML balayés | **1 772** |
| Fichiers YAML du dépôt | **1 794** |
| Répertoires hors balayage | `blueprints/` · `custom_components/` · `esphome/` · `zigbee2mqtt/` · `tools/` · `scripts/` |
| Fichiers de racine | **hors balayage** |

> **Conséquence sur l'arbitrage A-14.** Elle va dans le sens du constat de la
> V2 — mais l'**élargit** : le trou de contrôle ne se limite pas à la pression
> de bouton sur une entité native. **Tout appel d'appareil logé hors des
> répertoires balayés échappe également à `ASP-CI-11`.** La garde à concevoir
> doit donc être qualifiée en connaissance de cette portée réelle.
>
> *La V2 écrivait « tout le YAML du dépôt » — dans le tableau même qu'elle
> introduisait pour donner « la portée exacte de chaque contrôle ».*

### Conclusion opposable — **restreinte en V2, portée précisée en V3**

> **Pour le lot de conduite et de supervision.** Un fichier nouveau appelant un
> service `vacuum.*` serait **refusé** par `ASP-CI-11` et **ignoré** par
> `ASP-CI-14`. L'amendement doit donc **ouvrir le premier et étendre le
> périmètre du second** — sinon la primitive de démarrage, que le contrat
> n'autorise que sous garde fermée, circulerait sans contrôle.
>
> **Mais l'amendement de CI ne suffit pas** : `ASP-INV-31` et `ASP-INV-42`
> énumèrent nommément l'interruption et le retour à la base parmi les écritures
> réservées au moteur unique. **L'acte est contractuel avant d'être
> mécanique** — arbitrage **A-9**.

> **Pour le lot Maintenance, la conclusion est inverse — correction V2.**
> La V1 affirmait que ce lot dépendait aussi de l'amendement parce que
> « la CI refuse tout appel d'appareil hors des cinq fichiers L1 ».
> **C'est faux.** La remise à zéro passe par une pression de bouton sur une
> entité native `button.…`, qui n'est ni `vacuum.<x>` ni `roborock.<x>` :
> `ASP-CI-11` ne l'attrape pas, et `ASP-CI-7` ne balaie pas les scripts.
>
> **Le lot Maintenance n'a donc besoin d'aucun amendement — et la seule
> primitive irréversible du périmètre circule sans aucune garde.**
> Arbitrage **A-14**.

### Fichiers L1 réellement touchés par un élargissement du vocabulaire

| Fichier L1 | Pourquoi il est touché |
|---|---|
| `04_input_texts/aspirateur/mission.yaml` | `ASP-CI-18` confronte le **décompte écrit dans son en-tête** au vocabulaire. Son en-tête déclare en outre « écrivain unique … aucune automation, aucune UI, aucun autre script n'écrit ici » — déclaration à amender |
| `12_template_sensors/aspirateur/motif_lisible.yaml` | `ASP-CI-19` exige la traduction des valeurs ; les valeurs nouvelles n'auraient sinon **aucune obligation de motif lisible**, alors que `ASP-INV-50` en fait un livrable |

**Conséquence d'ordonnancement.** `ASP-CI-18` exige que toute valeur du
vocabulaire soit **effectivement écrite** par un writer. Porter la constante
sans livrer conjointement les fichiers qui écrivent les valeurs nouvelles fait
**échouer la CI immédiatement**. Un lot de CI seul est donc impossible :
**l'acte contractuel, l'amendement de CI, les deux fichiers L1 et le runtime L2
sont indissociables.**

---

## 4. Fichiers de runtime L1 existants

| Chemin | Rôle |
|---|---|
| `04_input_texts/aspirateur/mission.yaml` | Verdict et trace ; **vocabulaire fermé de dix-huit valeurs** |
| `10_scripts/aspirateur/lancer_mission.yaml` | Moteur de mission, écrivain unique, quatorze étapes |
| `12_template_sensors/aspirateur/etat_canonique.yaml` | Projection des dix états |
| `12_template_sensors/aspirateur/motif_lisible.yaml` | Traduction **totale** des dix-huit codes du catalogue |
| `12_template_sensors/aspirateur/conditions_lancement_hors_carte.yaml` | Garde de lancement |

---

## 5. Références d'interface

| Chemin | Rôle |
|---|---|
| `18_lovelace/dashboards/navigation.yaml` | Porte le bouton NAS à remplacer |
| `18_lovelace/dashboards/systeme/principal.yaml` | Cible du déplacement NAS ; porte le patron de carte de santé de pont |
| `18_lovelace/dashboards/systeme/nas.yaml` | Dashboard NAS existant ; badges génériques |
| `18_lovelace/includes/navigation/` | **Précédent** : cartes opérationnelles déjà hébergées dans Navigation |
| `19_button_card_templates/00_socles/action/socle_action_script_confirme.yaml` | Socle d'action avec confirmation |
| `19_button_card_templates/20_transverses/navigation/bouton_navigation_dynamique.yaml` | Bouton de navigation coloré par un capteur d'état |
| `10_scripts/system/notifications_mobiles.yaml` | Couche d'abstraction des notifications mobiles — **passage obligé** |
| `11_automations/electromenager/lave_vaisselle/notification_persistante.yaml` | **Patron de référence** de projection persistante |
