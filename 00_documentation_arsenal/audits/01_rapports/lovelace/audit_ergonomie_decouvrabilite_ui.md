# Audit ergonomie & découvrabilité UI Arsenal — constat empirique

**Périmètre** : expérience perçue de l'UI Lovelace Arsenal — navigation, découvrabilité des destinations, prévisibilité des interactions, cohérence visuelle entre information / navigation / commande / décision / diagnostic. Distinct de la conformité structurelle du graphe de navigation (`navigation_path`, retours, culs-de-sac), déjà traitée par [`audit_navigation_ui_lovelace.md`](audit_navigation_ui_lovelace.md) — voir §7 pour la délimitation exacte.
**Base d'analyse** : exploration live d'une instance Home Assistant Arsenal (session Chrome authentifiée, réseau local) recoupée avec le dépôt `C:\dev\arsenal`, HEAD `b90c6d0a` (2026-09-20).
**Nature** : audit en **lecture seule**, méthode empirique (navigation à froid, puis confrontation au dépôt, puis cartographie systématique). Aucune action à effet réel n'a été déclenchée lorsqu'elle pouvait modifier un état du système (bascules Automatique/Manuel, calibration, redémarrage HA, etc.) ; les seules interactions exécutées sont des navigations, des ouvertures de fenêtre « plus d'infos », et une consultation de notification.
**Statut** : **constat historique non arbitré**. Ne crée aucune exigence, aucune doctrine, aucun chantier. N'est pas une contre-expertise ni un remplacement de `navigation.md` ou de `navigation_topology.yaml`.

---

## 0. Verdict en une phrase

Côté dépôt, la navigation Arsenal est **gouvernée et intégralement classée** (95 dashboards, chacun rattaché à une classe A–E déclarée, aucun orphelin structurel) ; côté usage perçu, cette gouvernance **ne produit aucun signal visible dans l'interface** — la classe d'un dashboard, la nature d'une tuile (information, lien, commande) et l'existence même de 73 des 95 dashboards ne sont perceptibles qu'après exploration, tap expérimental ou recherche par mot-clé.

---

## 1. Méthode d'audit

L'audit s'est déroulé en trois temps distincts, dans cet ordre, sans retour en arrière sur l'ordre :

1. **Exploration à froid** — navigation dans l'UI Home Assistant vécue (dashboards, dialogues « plus d'infos », recherche Ctrl+K), **avant** toute lecture du dépôt, dans le but de capturer les hésitations, incompréhensions et fausses pistes d'un premier regard non informé par l'architecture interne.
2. **Confrontation aux contrats et à l'architecture** — lecture de `CLAUDE.md`, des doctrines (`separation_decision_action.md`, `commandabilite.md`), du socle UI (`ui/socle_ui/`) et de la charte couleurs (`ui/couleurs/`), pour requalifier chaque observation à froid comme incohérence réelle, complexité légitime, ou problème d'exposition.
3. **Cartographie systématique du graphe réel** — confrontation directe de `18_lovelace/dashboards.yaml`, `00_documentation_arsenal/ui/navigation.md`, `navigation_topology.yaml` et des fichiers de bandeaux/badges, avec vérification croisée en direct sur l'instance (clics test, comparaison URL/`navigation_path`).

**Restriction volontaire** : aucun bouton à effet réel (bascule de mode, calibration, redémarrage, commande de volet/lumière/chauffage) n'a été actionné. Les seules confirmations obtenues sur des actions à confirmation obligatoire (`Reset Calibration Zigbee`, `Reboot HA`) proviennent de la lecture du YAML source, pas d'un déclenchement.

---

## 2. Grille de lecture des constats

Chaque affirmation de ce document est étiquetée selon sa nature :

- **[live]** — observé directement dans l'interface Home Assistant durant les passes d'exploration.
- **[dépôt]** — constaté dans le code ou la documentation du dépôt (fichier et ligne cités).
- **[doctrine]** — règle ou taxonomie déjà normative, citée telle quelle, non réinterprétée.
- **[UX]** — interprétation ergonomique tirée des observations [live]/[dépôt], opposable comme lecture mais pas comme fait brut.
- **[non vérifié]** — hypothèse ou observation ponctuelle non confirmée exhaustivement ; ne doit pas être traitée comme un défaut acquis.

---

## 3. Topologie réelle — chiffres vérifiés

**[doctrine]** La taxonomie utilisée ci-dessous est celle déjà normative de `00_documentation_arsenal/ui/navigation.md` §6 (classes A–E) et de sa déclaration machine-readable `00_documentation_arsenal/ui/navigation_topology.yaml`. Ce document n'introduit aucune classe, aucun critère de classification nouveau.

**[dépôt]** `18_lovelace/dashboards.yaml` déclare **95 entrées** de dashboard (comptage `grep -c` vérifié deux fois par des méthodes indépendantes). **1 seule** porte `show_in_sidebar: true` : `arsenal-dashboard` (Accueil). Les 94 autres sont absentes de la barre latérale native Home Assistant par construction.

**[dépôt]** Répartition des 95 dashboards, reconstruite par résolution des `navigation_path` dans `18_lovelace/dashboards/navigation.yaml`, `navigation_topology.yaml` et les 5 fichiers de bandeaux (`18_lovelace/includes/navigation/{meteo,ecs,aspirateur,voiture,imprimerie}.yaml`), puis vérifiée par différence d'ensembles (aucun dashboard enregistré ne reste hors classification) :

| Classe (doctrine) | Définition (résumé, cf. `navigation.md` §6) | Effectif | Part |
|---|---|---|---|
| Hubs racines | Arsenal (sidebar) + Navigation (le Menu lui-même) — hors les 20 tuiles qu'ils exposent | 2 | 2 % |
| **A — Racine** | Exposé directement comme tuile dans `navigation-dashboard` | 20 | 21 % |
| **B — Sous-dashboard hiérarchique** | Parent fonctionnel unique déclaré dans `navigation_topology.yaml` (réglages/diagnostics de domaine + feuilles rattachées à Système) | 48 | 51 % |
| **C — Facette latérale** | Relié par un bandeau de bascule (météo, ECS, aspirateur, voiture, imprimerie) ; 27 dashboards au total dans ces 5 bandeaux, dont 4 sont déjà comptés en classe A (`ecs-dashboard`, `aspirateur-dashboard`, `audi-dashboard`, `imprimerie-dashboard`, qui sont aussi le point d'ancrage de leur propre bandeau) | 23 nets | 24 % |
| **D — Ressource partagée** | Aucun parent unique ; Accueil + Navigation suffisent (`reglages-meteo-dashboard`, `meteo-backups-dashboard`) | 2 | 2 % |
| **Total** | | **95** | **100 %** |

Vérification d'exhaustivité : `95 (registre) − [20(A) + 48(B) + 23(C net) + 2(D) + 2(hubs)] = 0`. Aucun résidu non classé.

**Conséquence directe, vérifiée par ce calcul et non par estimation** : **20 dashboards sur 95 (21 %) apparaissent comme tuile dans le Menu** ; **73 sur 95 (77 %)** — la totalité des classes B, C (nette) et D — **n'y apparaissent jamais**, quelle que soit leur importance fonctionnelle (NAS, UPS, Boiler, Rain Bird, réglages et diagnostics de chaque domaine en font partie).

**[doctrine]** Ce chiffre ne doit pas être lu comme une anomalie en soi : `navigation.md` §6.1 autorise explicitement une facette de classe C à être « volontairement non exposée dans Navigation (place limitée, importance fonctionnelle secondaire) sans devenir, de ce seul fait, un sous-dashboard hiérarchique » — cas cité nommément : `ecs-petite-maison-dashboard`.

### Chemins d'accès réels aux 73 dashboards hors Menu

- **Classe B (48)** : atterrir sur le dashboard de classe A du domaine, puis taper l'icône ⚙ (Réglages) ou 🩺 (Diagnostics) de son en-tête — badges factorisés par template (`bouton_parametres_badge_carre`, `bouton_diagnostics_badge_carre`, `19_button_card_templates/20_transverses/navigation/badges/`), **non labellisés à l'écran**. **[dépôt]** vérifié sur `18_lovelace/dashboards/chauffage/principal.yaml` (tap vers `/reglages-chauffage-dashboard` et `/diagnostics-chauffage-dashboard`) et `18_lovelace/dashboards/ecs/principal.yaml`. **[live]** vérifié pour Chauffage, ECS, Température (icône ⚙ → Calibration).
  - **13 des 48** ont pour parent déclaré `system-dashboard` directement (compté précisément dans `navigation_topology.yaml` : `nas-dashboard`, `ups-dashboard`, `bluetti-dashboard`, `diagnostics-boiler-dashboard`, `diagnostics-rain-bird-dashboard`, `diagnostics-zigbee-dashboard`, `diagnostics-bluetooth-dashboard`, `diagnostics-netatmo-dashboard`, `diagnostics-netatmo-wifi-dashboard`, `diagnostics-batteries-dashboard`, `diagnostics-automatisations-dashboard`, `id-automatisations-dashboard`, `reglages-telephones-dashboard`) ; n'ont **pas** de dashboard de domaine propre, ils remontent directement à la page Système, atteints en tapant une de ses tuiles. À noter : deux des trois dashboards portant « Boiler » dans leur titre (`diagnostics-boiler-chauffage-dashboard`, `diagnostics-boiler-ecs-dashboard`) sont en réalité rattachés respectivement à `diagnostics-chauffage-dashboard` et `diagnostics-ecs-dashboard`, pas à Système — seul `diagnostics-boiler-dashboard` remonte directement à `system-dashboard`. **[live]** vérifié pour `nas-dashboard` : tap sur la tuile « NAS » de la page Système → navigation effective ; bouton retour → `system-dashboard`, conforme à l'exemple cité par `navigation.md` §6.5 (« conforme, PR #828 »).
- **Classe C nette (23)** : bandeau de bascule propre au domaine déjà ouvert (icônes sans label). **[dépôt]** confirmé pour météo (9 icônes, `includes/navigation/meteo.yaml`), ECS (icône maison verte, `includes/navigation/ecs.yaml`), aspirateur, voiture et imprimerie (fichiers correspondants, non revérifiés en direct pour voiture/imprimerie cette passe — **[non vérifié]** pour ces deux derniers en live).
- **Classe D (2)** : Accueil + Navigation suffisent par doctrine ; en pratique atteints via l'icône ⚙ d'un domaine du même cluster (Calibration météo via l'icône ⚙ de la page Température).

**[live]** Le bandeau météo (9 icônes persistantes) n'apparaît, par grep confirmé, **que** sur Accueil, Menu et les pages météo elles-mêmes (`arsenal.yaml`, `navigation.yaml`, `18_lovelace/dashboards/meteo/*.yaml`) — il n'est **pas** présent sur Chauffage, Volets, VMC, etc. Une observation de première passe le décrivant comme « persistant partout » est corrigée ici : sa portée réelle est le cluster météo + les deux hubs, pas l'ensemble du système.

**[dépôt]** Un écart de Retour est déjà documenté et tracé comme non conforme, sans correction prévue par ce document : `meteo-min-max-temperature-dashboard` (classe B, parent `meteo-temperature-dashboard`) — `navigation.md` §6.5 : « ❌ non conforme — correction runtime différée ». Ce n'est pas une découverte de cet audit ; elle est reprise ici pour mémoire.

**[dépôt] Précision sur les segments d'URL.** Les URLs observées en direct portent un suffixe (`/nas-dashboard/0`, `/navigation-dashboard/home`) alors que la doctrine (`navigation.md` §4) interdit `/<dashboard-key>/0` dans un `navigation_path`. Vérification : les valeurs de `navigation_path` dans le YAML (ex. `/chauffage-dashboard`, `/nas-dashboard`) sont bien sous forme canonique, sans suffixe. **[live]** confirmé en navigant directement vers `http://192.168.1.117:8123/nas-dashboard` (sans suffixe) : Home Assistant résout et affiche `/nas-dashboard/0` dans la barre d'adresse. Le suffixe est un artefact d'affichage du routeur HA au moment de résoudre une vue unique, pas une violation du contrat `R-LL-NAV-1` (qui porte sur le `navigation_path` déclaré, pas sur l'URL résolue affichée).

---

## 4. Constats UX consolidés

### 4.1 Point d'entrée du Menu non labellisé
**[live]** L'icône en grille sous l'en-tête d'Accueil, seul chemin vers `navigation-dashboard`, ne porte aucun texte ni tooltip visible avant le tap. **[dépôt]** confirmé : le template `bouton_navigation_badge_carre` (`19_button_card_templates/20_transverses/navigation/badges/bouton_navigation_badge_carre.yaml`) ne définit qu'une icône, `navigation_path: /navigation-dashboard/home`, sans `name`. **[UX]** C'est le seul point d'entrée vers l'intégralité de la classe A (20 domaines) et vers Système : sa non-découvrabilité conditionne celle de tout le reste.

### 4.2 Mécanismes de navigation secondaires non labellisés (généralisé)
**[dépôt] + [live]** Les badges Réglages (⚙) et Diagnostics (🩺) de chaque domaine, ainsi que les bandeaux latéraux (météo, ECS, aspirateur, voiture, imprimerie), sont tous des icônes seules, sans texte. Ce n'est pas un oubli isolé : `navigation.md` §7 les décrit comme des points d'accès « invariants » sans jamais prescrire de label visible. **[UX]** Le mécanisme est cohérent et généralisé — mais sa découvrabilité dépend entièrement d'un apprentissage par essai, domaine par domaine.

### 4.3 Deux grilles de lecture de la maison, non annoncées comme telles
**[live]** La navigation par domaine (Menu, 20 tuiles fonctionnelles) et la navigation par grandeur physique (bandeau météo, 9 icônes : température, humidité relative/absolue, humidex, CO₂, bruit, précipitations, pression, météo publique) coexistent sur les mêmes écrans (Accueil, Menu) sans qu'aucun texte ne les distingue l'une de l'autre. **[UX]** Un utilisateur peut chercher « la météo » dans la grille de domaines (où elle n'apparaît qu'indirectement via « Rec. météo ») sans percevoir que le second bandeau, juste au-dessus, est la véritable porte d'entrée météo.

### 4.4 Dashboards structurellement rattachés mais difficilement découvrables
**[dépôt]** Confirmé au §3 : 73/95 dashboards (77 %) n'ont aucune tuile Menu. **[live]** Pour un sous-ensemble testé (NAS, Calibration météo, ECS Petite Maison), l'accès existe et fonctionne, mais seulement après avoir déjà atteint la bonne page parente et reconnu la bonne icône. **[UX]** « Structurellement rattaché » (vrai, cf. §3) ne veut pas dire « perceptiblement rattachable » pour un utilisateur qui ne connaît pas déjà l'arborescence.

### 4.5 Ambiguïté d'affordance : information, « plus d'infos », navigation, action
**[live]** Sur la page Système, la tuile « Secteur » (verte, « OK ») ouvre une fenêtre native « plus d'infos » (historique, entité `binary_sensor.coupure_secteur`) ; la tuile « NAS » (rouge, « Critique »), de style rigoureusement identique, navigue vers un dashboard entier (`/nas-dashboard`). **[UX]** Rien dans le rendu de la tuile — couleur, taille, icône, disposition — ne signale laquelle des deux natures s'applique avant le tap.

### 4.6 Actions à conséquence significative en habillage neutre ou en habillage avertissant, selon les cas
**[dépôt] confirmé et corrigé par rapport à une restitution précédente.** Deux cas distincts, à ne pas confondre :
- `Reboot HA` (`18_lovelace/dashboards/navigation.yaml`, section « ⚙️ Système » sous le Menu) utilise le template générique `bouton_navigation` (icône grise neutre `mdi:restart`), visuellement indiscernable d'un lien de navigation ordinaire jusqu'au tap. **Correction** : contrairement à une description antérieure de cet audit, l'action **n'est pas dépourvue de garde-fou** : `tap_action` porte `confirmation: { text: "❓ Redémarrer Home Assistant maintenant ?" }` avant l'appel à `homeassistant.restart`.
- `Reset Calibration Zigbee` (`18_lovelace/dashboards/meteo/reglages.yaml`) utilise le template `carte_action_standard_warning` (fond orange/pêche, icône `mdi:restart-alert`) et porte lui aussi une confirmation explicite (« ⚠️ Réinitialiser la calibration des capteurs Zigbee ? ») avant `script.turn_on`. **Correction** : une observation antérieure qualifiait cette tuile de « visuellement identique à une tuile de lecture » — c'est inexact : son fond orangé la distingue déjà des tuiles neutres voisines ; l'imprécision portait sur l'interprétation de cette couleur en direct, pas sur l'absence réelle de signal.
**[UX]** Le point qui subsiste : ces deux actions restent atteignables au bout d'un chemin de navigation non labellisé (Menu → défilement → Reboot HA ; Température → ⚙ → Calibration), et seule `Reset Calibration Zigbee` porte un habillage visuel distinct avant le tap — `Reboot HA` n'en porte aucun avant sa propre confirmation.

### 4.7 Collision visuelle commande / décision sur Modes
**[live]** Sur `modes-dashboard`, la section « Activation manuelle » affiche une tuile « Vacances : Désactivé » (bascule) et la section « Décision Vacances », juste en dessous, affiche une tuile « Vacances : Vacances inactives » (état calculé, lecture seule) — même mot, styles de tuile visuellement proches. **[dépôt]** Les deux tuiles proviennent de templates différents (`carte_mode_babysitting`/`carte_vacances_demande_manuelle` pour l'activation manuelle, vs un template de décision distinct) ; ce n'est donc pas une confusion de code, mais un rapprochement visuel de deux natures différentes sur le même écran. **[UX]** C'est précisément l'ambiguïté que la doctrine `separation_decision_action.md` (§ « Lisibilité UI ») demande d'éviter : « les dashboards peuvent afficher l'intention, l'état réel, l'écart éventuel sans ambiguïté ».

### 4.8 Divergences et collisions de titres visibles dans Ctrl+K
**[live]** La recherche Ctrl+K sur « Aération » retourne 3 résultats « Naviguer » au libellé identique. **[dépôt]** confirmé : `aeration-dashboard`, `reglages-aeration-dashboard` et `diagnostics-aeration-dashboard` portent chacun `title: Aération` (`18_lovelace/dashboards.yaml` lignes 15-20, 433-438, 568-573) ; deux des trois partagent en plus la même icône (`mdi:window-open-variant`). **[dépôt]** Ce n'est pas un cas isolé : le même patron (dashboard principal, réglages, diagnostic partageant le même `title`) s'observe pour Alarme, Chauffage, Climatisation, ECS, VMC, Volets, Ouvertures, Arrosage, Sommeil, et pour Boiler (3 dashboards `title: Boiler`). **Exception positive confirmée** : `diagnostics-eclairage-dashboard` porte un titre distinct, « Simulation de présence ». **[UX]** L'effet en surface (recherche, distinction) est le même que le titre soit dupliqué par convention systématique ou par oubli isolé.

### 4.9 Absence d'état visible sur certaines surfaces de commande
**[live] observation.** Sur `ouvertures-dashboard`, les tuiles (Garage, Porte, Fenêtre, numérotées « 1 »–« 4 » pour le Séjour) n'affichent que le nom, sans texte d'état ; l'état (« Fermé ») n'apparaît qu'après tap, dans la fenêtre « plus d'infos » (vérifié sur `binary_sensor.contact_entree_porte` → « Fermé »). Sur `volets-dashboard`, seules des commandes « Ouvrir »/« Fermer » sont présentes, sans aucun indicateur d'état ouvert/fermé, sur aucune tuile de la page. **[UX] appréciation, à distinguer de l'observation ci-dessus.** Ce silence est cohérent avec la nature de chaque page : `ouvertures-dashboard` est nommé comme une page d'état (son nom même évoque un diagnostic), ce qui rend l'absence de texte d'état plus saillante que sur `volets-dashboard`, conçu comme un panneau de commande pure où l'absence de retour d'état est un choix de conception plus défendable. Les deux observations sont factuelles ; seule l'appréciation de leur gravité relève d'un jugement UX.

### 4.10 Rupture d'expérience créée par le dashboard Énergie natif
**[dépôt]** La tuile Menu « Énergie » cible `navigation_path: /energy` (`18_lovelace/dashboards/navigation.yaml` ligne 234) — une URL native Home Assistant, hors registre `dashboards.yaml` (Énergie n'a pas de clé `dashboard` propre). **[live]** confirmé : la page affiche l'interface native HA (barre d'icônes différente : `+`, recherche, Assist, crayon d'édition — aucune icône Accueil/Menu Arsenal), sans données (« Il n'y a pas de données à afficher », 0 Wh partout). **[UX]** C'est le seul point du système testé où le changement de langage visuel est total et immédiat, sans transition ni signal préalable sur la tuile Menu elle-même.

### 4.11 Différences de vocabulaire pour une même réalité
**[live]** Le même équipement onduleur apparaît sous « UPS » (page Système, anglais) et sous « Onduleur » (page Prises, français) ; le libellé de tuile Menu « Rec. météo » cible un dashboard dont le titre propre est « Palmarès météo » (`18_lovelace/dashboards.yaml` ligne 281, cible `meteo-palmares-dashboard`). **[non vérifié]** Le rapprochement entre « Lampe Enfants » (Éclairage) et « Chambre Enfants » (Prises) comme désignant potentiellement le même dispositif n'a pas été vérifié au niveau `entity_id` ; il reste une hypothèse.

### 4.12 Jargon technique brut exposé
**[live]** Page NAS : champ « Dernier démarrage » affichant un horodatage ISO 8601 brut (`2026-09-13T19:38:14+00:00`), non mis en forme. Page Système : tuile « Ping LAN synthese » affichant le texte `esp32_critical: 2_proxies_ko`. **[UX]** Ces deux cas contrastent avec d'autres pages du même système (§5) qui traduisent des diagnostics techniques en phrases lisibles.

### 4.13 Absence constatée d'une synthèse « qu'est-ce qui réclame mon attention maintenant »
**[live]** Testé par recherche Ctrl+K du mot « critique » : les résultats retournés sont des entités et automatisations à l'identifiant brut (`UPS - Arret Home Assistant sur autonomie critique`, `binary_sensor.bluetti_batterie_critique`…), sans hiérarchisation ni regroupement. **[non vérifié]** L'absence d'une vue de synthèse dédiée n'a été vérifiée que par cette méthode et par un parcours manuel de la page Système ; l'existence d'un mécanisme équivalent non découvert ailleurs dans le système ne peut être exclue avec certitude.

---

## 5. Bons modèles internes

Ce document n'est pas uniquement négatif : plusieurs écrans confirmés font correctement la démonstration de ce que la doctrine `separation_decision_action.md` demande.

### Chauffage, Climatisation, VMC — **[live], motif confirmé sur les trois**
Chacun des trois dashboards de domaine (`chauffage-dashboard`, `clim-dashboard`, `vmc-dashboard`) présente le même patron, vérifié en direct et confirmé dans le YAML source (badges + cartes `carte_*_etat`) :
- **Autorité** : section « Autorité & reprise en main » avec deux tuiles mutuellement exclusives, icône robot (Automatique, fond bleu quand actif) / icône main (Manuel, fond orange quand actif) — répond immédiatement à « qui décide ? ».
- **Reprise en main** : sur Climatisation, observé en mode Manuel, une rangée de commandes (Arrêt / Froid / Déshum. / Chaud) n'apparaît que dans ce mode, avec la commande active surlignée.
- **Décision et motif** : bloc « Décision exécutoire : Arrêt commandé — Mode imposé à l'exécution » (Climatisation) ; « Intention chauffage : Sobriété thermique » puis « Chauffage – État réel : Réduit actif — Intention : Eco — Confort OK » (Chauffage) — la justification textuelle du pourquoi accompagne systématiquement l'état.

### Alarme — **[live]**
« Intention système : Désarmer » puis « Alarme Maison : Désarmée — Décision : Désarmer — Présence détectée » : la raison de l'état courant est donnée en une phrase, sans avoir à naviguer ailleurs.

### Aspirateur — **[live]**
Le champ « Dernier motif » traduit un échec technique en phrase complète et compréhensible : « Mission terminée : le cycle est allé à son terme, mais le robot n'a pas pu regagner sa base sur cette carte. » — à l'opposé du jargon relevé en §4.12 sur la page Système, dans le même système global.

### Volets — **[live]**
Verbes français explicites (« Ouvrir », « Fermer »), sans icône seule à interpréter : la surface de commande la plus immédiatement lisible rencontrée dans cet audit, malgré l'absence d'état relevée en §4.9.

**[UX]** Ces exemples montrent que le système sait déjà produire, à l'intérieur de lui-même, les patrons attendus par sa propre doctrine (autorité, motif, traduction en langage humain) — un point de référence interne pour toute évolution future, sans avoir besoin d'un modèle externe.

---

## 6. Points explicitement non conclus

- **Comportement du badge de notification après « Ignorer »** — une observation de première passe a suggéré qu'il pouvait persister après action, mais cela n'a pas été vérifié par un test répété et contrôlé. **[non vérifié]**.
- **Conformité des couleurs observées à la charte `ui/couleurs/`** — plusieurs hypothèses de sens ont été formées en direct (fraîcheur d'intégration, ampleur d'un écart, état réel) mais **aucune confrontation exhaustive** aux règles de `02_palette.md`, `02_1_palette_etiquettes.md`, `03_exceptions.md` et `05_regles.md` n'a été menée — la charte prévoit explicitement des exceptions contrôlées (HVAC, thermique, NAV) qui pourraient couvrir plusieurs cas observés. Ce travail est **hors périmètre** de cet audit, sur instruction explicite.
- **Comportements potentiellement natifs Home Assistant** — l'icône de recherche, l'icône Assist, le comportement de la fenêtre « plus d'infos », et la page Énergie relèvent en tout ou partie du cœur Home Assistant plutôt que d'un choix Arsenal ; ce document ne préjuge pas de la marge de manœuvre réelle sur ces éléments.
- **Caractère volontaire ou non de certains choix** — en particulier la non-exposition de 73 dashboards dans le Menu (partiellement couverte, documentée et assumée par la doctrine pour la classe C, cf. §3), le choix du template neutre pour `Reboot HA`, et l'absence de titre distinct sur la majorité des paires réglages/diagnostics. Aucun de ces points n'est traité ici comme un défaut confirmé nécessitant correction — seulement comme un écart entre gouvernance déclarée et perception, à arbitrer.
- **Domaines de classe C non revérifiés en direct cette passe** : Voiture et Imprimerie (bandeaux confirmés uniquement par lecture du dépôt, pas par navigation live).

---

## 7. Relation avec l'audit antérieur

[`audit_navigation_ui_lovelace.md`](audit_navigation_ui_lovelace.md) (Révision v2, clos) traite la **conformité structurelle** du graphe de navigation : liens cassés, forme canonique des `navigation_path`, cohérence des retours, absence de cul-de-sac — vérifiée par résolution statique des `!include` et confirmée en CI par `R-LL-NAV-1`. Son verdict (§0) : l'ossature est saine, les seuls défauts prouvés (P0/P1) sont corrigés et le chantier est clos.

Ce document ne rouvre pas ce périmètre et n'en contredit aucun constat. Il traite un objet différent : la **perception** de cette ossature par un usage réel — découvrabilité, affordance, cohérence visuelle entre les natures d'écran — qui n'était pas dans le périmètre de l'audit structurel (son §1 exclut explicitement toute conclusion qui ne serait pas résolue au niveau du code). Un nouveau document a donc été créé plutôt qu'un ajout à l'audit existant, celui-ci étant explicitement scellé comme « constat historique […] en lecture seule » à un HEAD daté, non conçu pour recevoir des ajouts postérieurs sur un autre objet.

---

## 8. Conclusion

La navigation Arsenal repose sur une taxonomie à cinq classes intégralement déclarée et vérifiable (`navigation_topology.yaml`), gardée en CI (`R-LL-NAV-1`), et dont l'exhaustivité a été revérifiée ici : **aucun des 95 dashboards enregistrés n'est orphelin au sens architectural** — chacun a une classe et un chemin d'accès documenté.

La dette observée par cet audit ne porte donc pas sur l'architecture de navigation elle-même, mais sur l'écart entre cette gouvernance et sa **perception** : un utilisateur qui découvre l'interface sans connaître au préalable sa structure interne ne dispose d'aucun signal — label, couleur distincte, tooltip — pour reconnaître qu'une tuile est une porte vers un autre écran plutôt qu'une simple donnée, ni pour anticiper la nature de ce qui se trouve derrière une icône non labellisée (⚙, 🩺, bandeau, grille du Menu). Le Menu n'a pas vocation, ni obligation doctrinale, à exposer l'intégralité des 95 dashboards — la classe C existe précisément pour organiser une exposition volontairement partielle. La question qui reste ouverte n'est donc pas « combien de portes existent » mais **la capacité de l'utilisateur à reconnaître qu'une porte est une porte, sa nature, et sa destination probable avant de l'ouvrir**.

Ce constat n'appelle, à ce stade, aucune correction : il est déposé pour arbitrage.

---

## Statut

- Portée : UI Lovelace Arsenal — expérience perçue, non conformité structurelle.
- Nature : audit empirique, lecture seule, constat historique au HEAD `b90c6d0a` (2026-09-20).
- Aucun runtime, dashboard, template, contrat, checker, registre ou changelog modifié par ce document.
- Suite éventuelle : arbitrage propriétaire, hors périmètre de ce document.
