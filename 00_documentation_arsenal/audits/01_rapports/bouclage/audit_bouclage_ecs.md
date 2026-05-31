# 🚿 ARSENAL — Audit Bouclage ECS — RAPPORT FINAL
*Clôture. Remplace les livrables intermédiaires (Phases 1-4, protocoles). Aucune formulation hypothétique : chaque point porte un statut défini. Les vérifications runtime intrusives ont été écartées par décision d'exploitation — choix retenu et acté ici comme légitime, le bouclage fonctionnant correctement en service.*

---

## 0. Verdict d'ensemble

Le domaine Bouclage ECS est **architecturalement sain et fonctionnellement correct** : séparation des couches nette (perception → qualification → autorisation → action → projection), discipline d'écriture de l'actionneur respectée, kill-switch et indépendance du cycle manuel correctement implémentés, cycle manuel borné, flag à non-survie garantie. **Aucun dysfonctionnement métier n'est observé ni démontré.**

La dette réelle est **entièrement documentaire et contractuelle** : la prose normative et l'architecture décrivent un runtime qui a évolué sans elles. Le runtime est juste ; ce sont les documents qui ont dérivé.

---

## 1. Constats démontrés par le dépôt
*Établis par lecture directe des fichiers. La preuve est le code. Statut : **CONFIRMÉ (dépôt)**.*

| ID | Constat | Gravité | Preuve |
|---|---|---|---|
| **BCL-01** | Les IDs d'automation documentés sont faux. Le contrat cite `…0001` (AUTO démarrage), `…0002` (AUTO extinction), `…0003` (fin manuel). Le runtime porte `…0004` (auto_demarrage), `…0005` (auto_extinction), `…0002` (stop_bouclage = **fin manuel**), `…0006` (notification), `…0007` (securite_demarrage). `…0001` et `…0003` n'existent pas. L'ID `…0002`, présenté par le contrat comme « AUTO extinction (front descendant) », porte en réalité la fin de cycle manuel. Les renvois du contrat à « l'automation 10260000000002 (front descendant) » (l.125, 360, 456) sont factuellement faux : c'est `…0005` qui réalise cette coupure. | 🔴 | `contrats/bouclage.md` vs `11_automations/bouclage/*.yaml` ; checker T06 (aligné, lui, sur le runtime) |
| **BCL-02** | Le nom du script manuel est faux dans le contrat. `script.bouclage_ecs_manuel` (Écrivains, transitions 2 & 7, changelog) n'existe pas ; l'entité réelle est `script.bouclage_ecs_5_minutes`. Le contrat est incohérent en interne (sa section Invariants emploie le bon nom). | 🟠 | `contrats/bouclage.md` l.279/351/356/525 vs `10_scripts/bouclage/cycle.yaml` |
| **BCL-03** | Un contrat v1 obsolète subsiste sans marquage. `04_bouclage_ecs_sous_systeme.md` décrit encore plages horaires, `presence_famille_unifiee` (interdite en v3), `bouclage_plage_active` + datetimes (supprimés), et « AUTO > MANUEL » (contredit la doctrine v2.3.0). | 🔴 | `04_bouclage_ecs_sous_systeme.md` l.106-160 |
| **BCL-04** | L'architecture normative est de millésime v1. `architecture/bouclage.md` (l.222-223) cite `…0001` « Bouclage automatique programmé » et `…0002` « Arrêt automatique fin timer ». | 🟡 | `architecture/bouclage.md` l.222-223 |
| **BCL-05a** | Les seuils thermiques ne sont pas contractualisés. `ecs_disponible` lit `input_number.bouclage_ecs_seuil_on/off` ; le contrat documente des valeurs fixes (45/40, hystérésis 5 °C) et ne mentionne ces helpers ni comme objets structurants ni dans la table d'observabilité. | 🟡 | `12_template_sensors/bouclage/ecs_disponible.yaml` ; `03_input_numbers/bouclage/seuils.yaml` ; `contrats/bouclage.md` |
| **BCL-07** | La chaîne de décision n'est pas observable, par configuration. `bouclage_autorise`/`ecs_disponible` ne figurent sur aucune dashboard YAML, et `recorder.yaml` (inclus par `configuration.yaml` l.44, stratégie `include` seule, 179 entités, sans `domains`/`entity_globs`) ne les liste pas — pas plus que `bouclage_auto_active`, le timer, le flag ou l'état du switch. Seuls `ecs_temperature_ballon_securisee` et `prise_bouclage_energy` sont historisés. | 🟠 | `recorder.yaml` ; `configuration.yaml` l.44 ; absence sous `18_lovelace/`. *Réserve unique : non recoupé avec l'onglet History live ni avec d'éventuelles dashboards en mode storage — recoupement passif non réalisé.* |
| **BCL-06a** | Le diagnostic d'intégrité des seuils n'est surfacé nulle part. `binary_sensor.parametres_invalides_bouclage_ecs` existe et est agrégé dans le groupe `parametres_invalides_domaines`, mais ni le capteur ni le groupe ne sont affichés sur une dashboard ou consommés par une notification. *(Correction d'une affirmation de la Phase 4 qui créditait à tort une atténuation d'observabilité.)* | 🟡 | `02_groups/parametres_invalides.yaml` ; absence de référence sous `18_lovelace/` et `11_automations/` |
| **BCL-08a** | La réconciliation post-boot n'est pas contractualisée. `auto_demarrage`/`auto_extinction` portent un second déclencheur `input_boolean.systeme_stable → on` (barrière one-shot +45 s, `stabilisation_post_demarrage.yaml`) absent du contrat, qui ne décrit que les fronts et la purge du flag. | 🟡 | `11_automations/bouclage/auto_*.yaml` vs `contrats/bouclage.md` |
| **BCL-10** | Le checker a des angles morts. T11 ne scanne que `10_scripts/` (aveugle à un écrivain automation illégitime) ; il valide des déclarations, pas des invariants comportementaux ; et ses IDs codés en dur sur le runtime le rendent **structurellement incapable de détecter BCL-01**. | 🟡 | `scripts/arsenal_contracts/check_bouclage_contracts.py` |

### Points conformes (à préserver)
`bouclage_autorise` implémente exactement la définition v3 (court-circuit kill-switch, ET thermique, OU occupation stricte) ; T07/T08 verrouillent la composition et interdisent `presence_famille_unifiee`. Aucun écrivain illégitime de `switch.prise_bouclage`. Indépendance du cycle manuel respectée. AUTO sans timer ; manuel borné (5 min, `restore: true`). Non-survie du flag garantie (purge inconditionnelle + purge boot si timer idle) — remédiation effective du bug v2.2.0. SUPERPOSITION correcte.

---

## 2. Constats confirmés par les vérifications passives
*Validés par relevés runtime non intrusifs déjà réalisés. Statut : **CONFIRMÉ (dépôt + runtime passif)**.*

| ID | Constat | Preuve passive |
|---|---|---|
| **BCL-05b** | La documentation des seuils diverge **déjà** de la réalité. Le contrat affirme `seuil_off = 40 °C` et hystérésis 5 °C ; le runtime montre `seuil_on = 45`, `seuil_off = 39`, soit une **hystérésis effective de 6 °C**. La valeur documentée n'est pas seulement mutable en théorie : elle est, à l'instant du relevé, inexacte. | R1 : `seuil_on=45.0`, `seuil_off=39.0` |
| **Conformité fonctionnelle au repos** | État IDLE cohérent : à 31,3 °C (< seuil_off), `ecs_disponible=off` et `bouclage_autorise=off` corrects (le ET thermique invalide, malgré `auto_active=on`) ; switch/flag/timer cohérents. La composition ET/OU et l'hystérésis se comportent comme spécifié. | État au repos fourni |
| **Capteur d'intégrité opérationnel (cas nominal)** | Pour une config valide (45 > 39), `parametres_invalides_bouclage_ecs=off`, `cause=none`. Le capteur lit correctement en nominal. | `parametres_invalides=off`, `cause=none` |

---

## 3. Scénarios théoriques non retenus comme anomalies
*Le mécanisme existe dans le code (fait dépôt), mais aucune manifestation réelle n'est observée et la provocation artificielle d'états limites a été écartée par décision d'exploitation. Statut : **NON RETENU comme anomalie** — caractéristique de conception connue, pas un défaut.*

| ID | Caractéristique de conception (fait dépôt) | Pourquoi non retenu |
|---|---|---|
| **BCL-09** | La borne d'AUTO repose **uniquement** sur une lecture thermique fraîche. Aucun garde de péremption nulle part dans la chaîne : source MQTT `boiler_dhw_temperature` sans `expire_after` ni `availability` ; `ecs_temperature_ballon_securisee` conserve la dernière valeur sur source non numérique, sans expiration ; aucun watchdog de durée max sur la pompe en AUTO (cohérent avec l'interdiction contractuelle de timer AUTO). | Aucune défaillance source observée en exploitation. Le bridge boiler fournit une mesure en service. Scénario (bridge mort + dernière valeur chaude + présence) non manifesté → non qualifié d'anomalie. **À connaître**, non à corriger en urgence. |
| **BCL-08b** | Un cycle manuel à cheval sur un redémarrage HA verrait, à +45 s, la réconciliation `…0005` couper le switch tandis que flag et timer (restaurés) poursuivent jusqu'à expiration — divergence transitoire switch `off` / flag `on`. | Conjonction rare (reboot pendant les 5 min d'un cycle manuel avec AUTO non autorisé). Aucune occurrence rapportée. État éventuellement cohérent à l'expiration. Non retenu comme anomalie. |
| **BCL-06b** | Une configuration `seuil_off ≥ seuil_on` (atteignable : plages [35;60]/[30;50] sans garde croisé) force `ecs_disponible=off` et désactive AUTO ; seule trace = le diagnostic non surfacé (BCL-06a). | Requiert une mésaisie utilisateur. Config courante valide (cf. §2). Non manifesté → non retenu comme anomalie active. Le garde croisé reste une amélioration optionnelle. |

> Note de méthode : ces trois points ne sont **pas infirmés** (le code les porte) ; ils ne sont **pas retenus comme anomalies** faute de manifestation et par choix de ne pas forcer d'état limite. C'est une qualification définitive, pas une incertitude résiduelle.

---

## 4. Actions retenues — documentaires & contractuelles

Toutes indépendantes de tout runtime. Ordre suggéré : du factuellement faux (priorité) vers l'amélioration.

### 4.1 Réconcilier `contrats/bouclage.md` avec le runtime
- **IDs d'automation** — remplacer dans la section *Écrivains officiels*, le corps et le changelog :
  - `10260000000001` (AUTO démarrage) → **`10260000000004`** (`auto_demarrage.yaml`)
  - `10260000000002` (AUTO extinction) → **`10260000000005`** (`auto_extinction.yaml`)
  - `10260000000003` (fin manuel) → **`10260000000002`** (`stop_bouclage.yaml`)
  - corriger les renvois l.125 / 360 / 456 « automation 10260000000002 (front descendant) » → **`10260000000005`**
  - **ajouter** comme objets officiels : `10260000000006` (notification, projection UI) et `10260000000007` (securite_demarrage, purge flag boot) — déjà décrits en prose, à rattacher à leur ID.
- **Nom du script** — remplacer toutes les occurrences de `script.bouclage_ecs_manuel` → **`script.bouclage_ecs_5_minutes`** (l.279, 351, 356, 525).
- **Réconciliation** — documenter le second déclencheur `systeme_stable → on` des automations AUTO (BCL-08a) comme mécanisme de re-synchronisation post-boot.

### 4.2 Aligner la documentation des seuils (BCL-05)
- Remplacer la table à valeurs fixes par la mention des helpers `input_number.bouclage_ecs_seuil_on` / `…_seuil_off` comme **objets structurants** ; indiquer les valeurs comme **configurables** (valeurs courantes 45 / 39, hystérésis 6 °C) et non comme constantes.
- Ajouter à la table d'observabilité : les deux helpers de seuil et `binary_sensor.parametres_invalides_bouclage_ecs`.
- Mentionner l'invariant gardé par le capteur d'intégrité : `seuil_on > seuil_off`.

### 4.3 Marquer le contrat v1 comme remplacé (BCL-03)
- En-tête de `04_bouclage_ecs_sous_systeme.md` : bandeau **⚠️ OBSOLÈTE — SUPERSEDED par `contrats/bouclage.md` v2.3.0**, avec date. Alternative : suppression si plus référencé par la chaîne pipeline ECS (à vérifier avant suppression).

### 4.4 Réaligner l'architecture (BCL-04)
- `architecture/bouclage.md` § écrivains : mêmes corrections d'IDs qu'en 4.1 ; retirer le vocabulaire v1 (« programmé »).

### 4.5 Renforcer le checker (BCL-10, optionnel mais recommandé)
- **Anti-dérive documentaire** (clôt la cause-racine de BCL-01) : ajouter un test qui extrait les IDs cités dans `contrats/bouclage.md` et vérifie qu'ils correspondent aux IDs réellement déclarés dans `11_automations/bouclage/`. C'est le seul ajout qui aurait empêché la dérive.
- Étendre T11 à `11_automations/` (détecter un écrivain automation illégitime de `prise_bouclage`).
- Ajouter des tests d'invariants comportementaux : `…0005` réagit au front descendant ; `…0002` éteint le flag inconditionnellement ; `…0007` purge si timer idle ; `script.bouclage_ecs_5_minutes` ne lit pas `bouclage_auto_active` (indépendance manuelle) ; `ecs_disponible` consomme bien les helpers de seuil.

### 4.6 Observabilité (optionnel, à votre discrétion — BCL-06a / BCL-07)
Décision d'exploitation, pas correction : si la traçabilité post-incident vous importe, ajouter `bouclage_autorise`, `ecs_disponible`, le flag et le timer au `recorder.yaml`, et surfacer `parametres_invalides_domaines` sur une vue diagnostic. Sinon, documenter explicitement le choix d'un recorder volontairement épuré.

---

## 5. Tableau de synthèse final

| ID | Objet | Statut final |
|---|---|---|
| BCL-01 | IDs d'automation documentés faux | **Confirmé (dépôt)** → action 4.1 |
| BCL-02 | Nom du script manuel faux | **Confirmé (dépôt)** → action 4.1 |
| BCL-03 | Contrat v1 obsolète non marqué | **Confirmé (dépôt)** → action 4.3 |
| BCL-04 | Architecture v1 | **Confirmé (dépôt)** → action 4.4 |
| BCL-05 | Seuils non contractualisés (a) + doc divergente (b) | **Confirmé (dépôt + passif)** → action 4.2 |
| BCL-06a | Diagnostic intégrité non surfacé | **Confirmé (dépôt)** → action 4.6 |
| BCL-07 | Chaîne de décision non observable (config) | **Confirmé (dépôt)**, réserve History/storage → action 4.6 |
| BCL-08a | Réconciliation post-boot non documentée | **Confirmé (dépôt)** → action 4.1 |
| BCL-10 | Angles morts du checker | **Confirmé (dépôt)** → action 4.5 |
| BCL-06b | Désactivation AUTO sur seuils invalides | **Non retenu comme anomalie** (config valide, non manifesté) |
| BCL-08b | Coupure cycle manuel au reboot | **Non retenu comme anomalie** (non manifesté) |
| BCL-09 | Borne thermique tributaire d'une lecture fraîche | **Non retenu comme anomalie** (aucune défaillance source observée) — caractéristique à connaître |

*Fin du rapport.*
