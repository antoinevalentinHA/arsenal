# CONTRAT ARSENAL — RESSOURCES LOVELACE

**Version :** 1.2
**Domaine :** Approvisionnement, figeage local et chargement des ressources frontend Lovelace (cartes custom)
**Statut :** Opposable

---

## 🎯 Rôle

Garantir que le frontend Arsenal est :

- **déterministe** : la version active est connue, figée, traçable
- **reproductible** : un retour arrière à un état stable est toujours possible
- **indépendant** des évolutions HACS : aucune mise à jour HACS ne peut altérer le runtime sans action explicite
- **opposable** : à tout instant, un audit permet de répondre à la question « quelle version de carte X tourne et pourquoi ? »
- **résilient** : la défaillance d'une ressource n'entraîne pas l'effondrement du frontend complet

---

## 🧨 Risques couverts

- Mise à jour HACS cassante (régression visuelle, erreur JS)
- Disparition ou renommage d'une ressource côté HACS
- Changement de nom du fichier JS principal entre deux versions (ex. ajout d'un suffixe `-bundle`)
- Cache navigateur servant un JS obsolète après mise à jour serveur
- Divergence silencieuse entre runtime, manifeste et `resources.yaml`
- Dépendance d'un dashboard critique cassée par un update non validé
- Effondrement complet du frontend faute de mode dégradé

---

## 🚫 Non-objectifs

- Automatiser la copie `community/` → `www/`
- Suivre en temps réel les releases HACS
- Optimiser la performance ou le poids du frontend
- Gérer les intégrations Python (`custom_components`) ou les thèmes — hors périmètre

---

## 1. Objet

Ce contrat formalise la gestion des ressources frontend Lovelace (cartes custom JS) au sein d'Arsenal. Il définit :

- la **séparation stricte** entre la source d'approvisionnement (HACS) et le runtime (Home Assistant frontend)
- la **structure canonique** des chemins de stockage local
- la **hiérarchie des sources de vérité** entre manifeste et `resources.yaml`
- les **invariants** garantissant la stabilité, la traçabilité et la reproductibilité du frontend
- la **procédure de mise à jour** d'une ressource
- la **procédure de rollback** en cas d'incident post-update
- la **procédure de mode dégradé** en cas de défaillance critique
- la **procédure d'audit** pour vérifier la conformité du système à tout instant

---

## 2. Principe directeur

> **HACS est une source d'approvisionnement, pas un runtime.**

Aucune ressource Lovelace référencée dans `resources.yaml` ne doit pointer vers `/hacsfiles/...` ni vers `/local/community/...`. Toute ressource active en production est servie depuis `/local/<nom_ressource>/`, c'est-à-dire `/homeassistant/www/<nom_ressource>/`.

Ce principe garantit :

- **Indépendance temporelle** : une mise à jour HACS n'altère jamais le runtime sans action explicite.
- **Reproductibilité** : la version active est figée et auditable.
- **Découplage** : HACS peut être désinstallé, désactivé ou défaillant sans casser le frontend.

---

## 3. Architecture canonique

### 3.1 Couches

```
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 1 — APPROVISIONNEMENT (HACS)                         │
│ /homeassistant/www/community/<ressource>/                   │
│ Géré par HACS. NON référencé en runtime. Versions mobiles.  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ copie manuelle contractualisée
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 2 — RUNTIME FIGÉ                                     │
│ /homeassistant/www/<ressource>/                             │
│ Source de vérité du frontend. Versions figées et opposables.│
└─────────────────────────────────────────────────────────────┘
                            │
                            │ référencement explicite
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 3 — DÉCLARATION                                      │
│ /homeassistant/lovelace/resources.yaml                      │
│ URLs en /local/<ressource>/<fichier>.js exclusivement.      │
│ Projection technique du manifeste (cf. INV-14).             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ inclusion
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 4 — ORCHESTRATION                                    │
│ /homeassistant/lovelace/lovelace_main.yaml                  │
│ resource_mode: yaml + !include resources.yaml               │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ inclusion racine
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 5 — CONFIGURATION RACINE                             │
│ /homeassistant/configuration.yaml                           │
│ lovelace: !include lovelace/lovelace_main.yaml              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Manifeste de version

le manifeste runtime du dossier /homeassistant/www est le **manifeste de version** du runtime frontend et la **source de vérité fonctionnelle** du sous-système (cf. INV-14).

Il liste **toutes** les ressources figées avec leur version exacte, leur chemin, leur fichier actif, leur statut, leur criticité et leur date de dernière mise à jour. Il est la **référence canonique opposable** du frontend.

Format obligatoire de chaque entrée :

```markdown
### <Nom ressource>
- version: vX.Y.Z
- chemin: /homeassistant/www/<ressource>/
- fichier: <nom_du_fichier>.js
- statut: actif | rollback | divergence_assumee | desactivee_mode_degrade
- derniere_mise_a_jour: YYYY-MM-DD
- criticite: critique | secondaire
- notes: <optionnel — divergence HACS, raison rollback, mode dégradé, etc.>
```

---

## 4. Invariants

### INV-1 — Séparation HACS / Runtime
Aucun chemin sous `/homeassistant/www/community/` n'apparaît dans `resources.yaml`. Aucune URL `/hacsfiles/...` n'apparaît dans `resources.yaml`.

### INV-2 — Préfixe d'URL canonique
Toute entrée de `resources.yaml` commence par `/local/`. Aucune autre origine n'est tolérée.

### INV-3 — Correspondance dossier ↔ URL
Pour toute entrée `url: /local/<dir>/<file>.js` dans `resources.yaml`, le fichier `/homeassistant/www/<dir>/<file>.js` existe et est lisible.

### INV-4 — Type explicite déclaré
Toute entrée de `resources.yaml` déclare un type explicite. La valeur par défaut est `module`. Toute déviation (`js`, `css`, etc.) doit être justifiée et documentée dans le manifeste, dans le champ `notes` de la ressource concernée.

### INV-5 — Manifeste exhaustif
Toute ressource présente dans `resources.yaml` est listée dans le manifeste runtime du dossier /homeassistant/www avec sa version exacte, son fichier cible et son statut. Réciproquement, toute ressource listée dans le manifeste avec un statut `actif` est référencée dans `resources.yaml`.

### INV-6 — Sauvegarde locale exploitable
Pour toute ressource ayant subi au moins une mise à jour, le dossier `/homeassistant/www/<ressource>/` contient une **sauvegarde locale exploitable** de la version précédente stable. La forme est libre (suffixe `.bak`, dossier versionné, archive `.tar.gz`, etc.) tant que :

- la sauvegarde est **immédiatement restaurable** sans téléchargement externe
- elle est **identifiable** (la version qu'elle représente est connue, soit par convention de nommage, soit par documentation)

Une ressource jamais mise à jour depuis son installation initiale est dispensée de cette obligation, à condition que ce statut soit explicite dans le manifeste.

### INV-7 — Atomicité de la mise à jour
Une mise à jour d'une ressource n'est considérée terminée que lorsque les **quatre** modifications suivantes sont effectuées et cohérentes entre elles :

1. fichiers copiés dans `/homeassistant/www/<ressource>/`
2. version, fichier cible et date mis à jour dans le manifeste runtime du dossier /homeassistant/www
3. (si l'URL ou le nom de fichier change) `resources.yaml` mis à jour
4. cache navigateur invalidé et chargement effectif du nouveau JS vérifié (cf. INV-11)

Un état partiel est une violation contractuelle.

### INV-8 — HACS auxiliaire
HACS reste installé et fonctionnel comme **outil de veille et d'approvisionnement**. Sa désactivation n'est pas un objectif, mais sa défaillance ne doit jamais affecter le runtime frontend.

### INV-9 — Pas de mise à jour automatique runtime
La copie de `community/<ressource>/` vers `www/<ressource>/` est **toujours manuelle et explicite**. Aucune automation, aucun script Home Assistant, aucun `shell_command` ne réalise cette opération.

### INV-10 — Versionnement explicite
Chaque entrée du manifeste indique la version exacte (ex. `v0.13.0`), pas une plage, pas un alias type `latest`.

### INV-11 — Cohérence cache frontend
Toute mise à jour de ressource doit être suivie d'un **chargement effectif du nouveau JS côté navigateur**. Le critère est **observable**, pas procédural : la version servie au client doit correspondre à la version attendue.

Le contrôle peut s'effectuer par tout moyen permettant de constater la concordance :

- variation de **taille** du fichier servi par rapport à la version précédente
- variation de **hash** (ETag, hash calculé)
- inspection du **contenu** (commentaire de version en en-tête, constante `VERSION` exposée par la lib, etc.)

Les gestes habituels (Ctrl+Shift+R, "Disable cache" dans DevTools) sont des **moyens** de produire ce résultat ; ils ne se substituent pas au constat.

Un état où :

- le fichier serveur est à jour (couches 2-3-4-5 cohérentes)
- mais le navigateur sert encore l'ancien JS depuis son cache

est considéré comme un **état incohérent** et constitue une violation contractuelle non close.

Le simple rechargement des ressources Lovelace côté Home Assistant ne suffit pas : il invalide le cache HA, pas le cache navigateur.

### INV-12 — Dépendance UI critique
Toute ressource utilisée dans :

- le dashboard principal
- la navigation globale
- les cartes pivot (synthèse, statut, vue d'ensemble Arsenal)

est marquée `criticite: critique` dans le manifeste.

Toute mise à jour d'une ressource critique impose, en plus de la procédure standard :

- une **validation frontend renforcée** (cf. §6) sur au moins un dashboard consommateur principal
- une **période d'observation adaptée au contexte**, **24 h recommandé** par défaut, ajustable selon les contraintes opérationnelles (ex. fenêtre courte assumée pour enchaîner plusieurs updates dans une session de maintenance)

La période d'observation est un **garde-fou recommandé**, pas un verrou bureaucratique. Toute réduction doit être consciente.

Les ressources non critiques (`criticite: secondaire`) suivent la procédure standard sans cette exigence renforcée.

### INV-13 — Traçabilité des régressions
Toute version retirée pour cause de régression est conservée avec un suffixe `.broken` (ou équivalent identifiable). Elle **ne doit jamais écraser** un `.bak`.

Le `.bak` reste la dernière version **stable connue**. Le `.broken` est une version **fautive conservée pour analyse**. Cette distinction est non négociable : la confondre détruit l'historique de stabilité.

### INV-14 — Source de vérité fonctionnelle unique
Le manifeste le manifeste runtime du dossier /homeassistant/www est la **source de vérité fonctionnelle** du sous-système ressources Lovelace.

`resources.yaml` est une **projection technique** de ce manifeste, requise par Home Assistant pour le chargement effectif des ressources mais subordonnée au manifeste sur le plan de la gouvernance.

Conséquences :

- toute modification fonctionnelle (ajout, suppression, changement de version, changement de criticité, passage en mode dégradé) part **du manifeste** et est ensuite répercutée dans `resources.yaml`
- en cas de divergence détectée à l'audit, c'est `resources.yaml` qui est considéré comme suspect, et c'est le manifeste qui sert de référence pour la résolution
- une dérive silencieuse (modification directe de `resources.yaml` sans passage par le manifeste) est une violation contractuelle

---

## 5. Interdictions

### INT-1
Référencer dans `resources.yaml` un chemin sous `/local/community/...` (équivalent à `/homeassistant/www/community/`).

### INT-2
Modifier un fichier sous `/homeassistant/www/<ressource>/` autrement que par copie depuis `/homeassistant/www/community/<ressource>/` (pas d'édition manuelle du JS).

### INT-3
Mettre à jour une ressource via HACS sans planifier une fenêtre de maintenance explicite pour la réplication runtime. Une avance de phase `community/` sur `www/` est tolérée, à condition d'être :

- **bornée** : un délai de réplication ou de décision est documenté
- **tracée** : le manifeste mentionne l'écart en commentaire (champ `notes`)

Une avance de phase non documentée est une violation.

### INT-4
Supprimer la ligne d'une ressource dans `resources.yaml` sans avoir audité au préalable les dashboards qui l'utilisent (risque de cartes cassées en production UI).

### INT-5
Ajouter une ressource directement en runtime sans la déclarer dans le manifeste le manifeste runtime du dossier /homeassistant/www.

### INT-6
Pousser un changement vers `resources.yaml` sans procéder au contrôle de cohérence cache (INV-11).

### INT-7
Écraser un fichier `.bak` représentant une version stable connue par une version fautive (cf. INV-13).

### INT-8
Modifier directement `resources.yaml` sans avoir préalablement mis à jour le manifeste (cf. INV-14).

---

## 6. Procédure de mise à jour d'une ressource

**Pré-conditions :**

- HACS signale une nouvelle version de la ressource
- Le frontend actuel est stable (aucune carte en erreur)
- Une fenêtre de maintenance est explicitement ouverte

**Étapes :**

1. **Approvisionnement HACS**
   Mettre à jour la ressource via l'interface HACS. La nouvelle version arrive dans `/homeassistant/www/community/<ressource>/`.

2. **Sauvegarde de la version actuelle figée**
   Dans `/homeassistant/www/<ressource>/`, renommer le ou les fichiers actifs en `.bak`.
   Exemple :
   ```
   apexcharts-card.js     → apexcharts-card.js.bak
   apexcharts-card.js.gz  → apexcharts-card.js.gz.bak
   ```
   Si un `.bak` existe déjà, vérifier qu'il représente bien une version stable connue avant de l'écraser. En cas de doute, le renommer en `.bak.<date>` plutôt que de le perdre.

3. **Copie de la nouvelle version**
   Copier l'intégralité du contenu de `/homeassistant/www/community/<ressource>/` vers `/homeassistant/www/<ressource>/`.

4. **Mise à jour du manifeste (source de vérité)**
   Mettre à jour dans le manifeste runtime du dossier /homeassistant/www :
   - `version`
   - `fichier` (si renommage)
   - `derniere_mise_a_jour` (date du jour)
   - `notes` (si type non-`module` ou autre particularité)

5. **Projection vers `resources.yaml`**
   Vérifier que le nom de fichier ciblé par l'URL n'a pas changé entre les deux versions. Si oui, ajuster l'entrée correspondante. Cette étape est une **conséquence** de l'étape 4, jamais une modification autonome (cf. INV-14, INT-8).

6. **Rechargement Lovelace côté serveur** *(optionnel)*
   Paramètres → Tableaux de bord → ⋮ → Ressources → recharger.
   Étape utile seulement en cas de changement structurel (URL, ajout/suppression d'entrée). Pour une simple mise à jour de fichier JS de même nom, l'étape 7 suffit.

7. **Contrôle de cohérence cache (impératif — INV-11)**
   Vérifier que le navigateur charge effectivement la nouvelle version. Tout moyen probant est admis :
   - inspection du fichier servi (taille, hash, en-tête de version dans le JS)
   - DevTools → Network → confirmation que le nouveau JS est servi
   - rechargement forcé (Ctrl+Shift+R) puis revérification

   Le critère contractuel est **le constat**, pas le geste.

8. **Validation frontend**
   Sur au moins un dashboard consommateur (et un dashboard principal pour ressource `criticite: critique`) :
   - affichage correct des cartes
   - absence d'erreur dans la console navigateur
   - absence de 404 sur les URL `/local/...`

9. **Validation contractuelle**
   Exécuter la procédure d'audit §9.

10. **Période d'observation (ressources critiques uniquement)**
    24 h recommandé en contexte normal. Ajustable selon les contraintes (cf. INV-12). En cas de réduction, le motif est noté dans le manifeste.

**Post-conditions :**

- Tous les invariants §4 sont satisfaits.
- La nouvelle version tourne en production, vérifiée côté navigateur.
- L'ancienne version est conservée en sauvegarde locale exploitable.
- Le manifeste reflète l'état réel du runtime.

---

## 7. Procédure de rollback

**Déclencheurs :**

- Une carte fonctionnelle avant la mise à jour est cassée après.
- Une régression visuelle ou comportementale est constatée.
- Une erreur JS apparaît dans la console navigateur, imputable à la nouvelle version.

**Étapes :**

1. **Conservation traçable de la version fautive**
   Dans `/homeassistant/www/<ressource>/`, renommer la version fautive avec le suffixe `.broken` :
   ```
   apexcharts-card.js      → apexcharts-card.js.broken
   apexcharts-card.js.gz   → apexcharts-card.js.gz.broken
   ```
   **Ne jamais écraser un `.bak`** (INV-13, INT-7).

2. **Restauration du fichier stable**
   ```
   apexcharts-card.js.bak     → apexcharts-card.js
   apexcharts-card.js.gz.bak  → apexcharts-card.js.gz
   ```

3. **Mise à jour du manifeste (source de vérité)**
   - `version` : remettre la valeur antérieure
   - `statut` : `rollback` (ou `actif` si on considère que la version stable redevient la version courante normale)
   - `derniere_mise_a_jour` : date du rollback
   - `notes` : raison du rollback, version fautive identifiée, lien vers issue amont si applicable

4. **Projection vers `resources.yaml`** (si nécessaire)
   Si le nom de fichier diffère entre version stable et version fautive, ajuster l'URL.

5. **Contrôle de cohérence cache (impératif — INV-11)**
   Particulièrement critique en rollback : sans invalidation effective, le navigateur continue de servir la version fautive depuis son cache.

6. **Validation frontend**
   Vérifier le retour à l'état stable, notamment sur les dashboards qui ont déclenché la détection de régression.

7. **Décision sur HACS**
   Décider du sort de l'approvisionnement HACS :
   - **Option A** : laisser la version HACS en avance, marquer la ressource `statut: divergence_assumee` dans le manifeste avec note explicite.
   - **Option B** : downgrade HACS vers la version stable (si HACS le permet pour cette ressource).

8. **Audit post-rollback**
   Exécuter la procédure d'audit §9.

**Post-conditions :**

- Le runtime est revenu à un état stable connu.
- Le manifeste reflète l'état réel, y compris la divergence éventuelle avec HACS.
- La version fautive est conservée localement avec un nommage non ambigu.
- Le navigateur sert effectivement la version stable.

---

## 8. Mode dégradé

**Déclencheurs :**

- Une ressource provoque une défaillance critique (erreur JS bloquante, freeze du frontend, comportement erratique généralisé)
- Le rollback échoue ou n'est pas immédiatement disponible
- Une décision opérationnelle est prise de retirer temporairement la ressource pour rétablir le frontend

**Principes :**

Le mode dégradé est un **état transitoire assumé** dans lequel une ressource est **temporairement retirée du runtime** sans être désinstallée. Les dashboards impactés doivent rester fonctionnels (graceful degradation) ; les cartes consommatrices apparaissent en erreur visible (placeholder Lovelace) plutôt que de provoquer une cascade d'échecs.

**Étapes :**

1. **Retrait de l'entrée dans `resources.yaml`**
   Commenter (ne pas supprimer) la ligne correspondant à la ressource :
   ```yaml
   # 📊 ApexCharts Card — DÉSACTIVÉE EN MODE DÉGRADÉ depuis YYYY-MM-DD
   # - url: /local/apexcharts-card/apexcharts-card.js
   #   type: module
   ```

2. **Mise à jour du manifeste**
   - `statut` : `desactivee_mode_degrade`
   - `notes` : motif du mode dégradé, date d'entrée en mode dégradé, fenêtre de résolution prévue

3. **Contrôle de cohérence cache et rechargement Lovelace**
   Pour s'assurer que le frontend prend bien acte du retrait.

4. **Validation frontend**
   Vérifier que les dashboards qui n'utilisent pas la ressource fonctionnent normalement et que les dashboards qui l'utilisent dégradent gracieusement (placeholder, pas d'effondrement).

5. **Planification de la sortie de mode dégradé**
   Le mode dégradé n'est pas un état stable. Une fenêtre de maintenance ultérieure doit être planifiée pour :
   - identifier la cause racine (régression amont, incompatibilité, etc.)
   - réintégrer la ressource (version corrigée, version antérieure stable, ou ressource alternative)
   - sortir formellement du mode dégradé via la procédure de mise à jour §6

**Post-conditions :**

- Le frontend est fonctionnel, à l'exception identifiée des cartes consommatrices de la ressource désactivée.
- Le manifeste documente précisément l'état dégradé et la trajectoire de sortie.
- La ressource reste présente sur disque (couches 1 et 2 inchangées) pour faciliter la réintégration.

---

## 9. Procédure d'audit

L'audit est une vérification **idempotente** et **non destructive** de la conformité au contrat. À exécuter :

- après chaque mise à jour, rollback ou entrée/sortie de mode dégradé
- ponctuellement à la demande (au moins une fois par trimestre)
- en cas de comportement frontend anormal

### 9.1 Vérifications

**A-1. Cohérence URL ↔ fichier**
Pour chaque entrée de `resources.yaml` :
- l'URL commence par `/local/` (INV-2)
- le fichier correspondant existe sous `/homeassistant/www/<dir>/<file>.js` (INV-3)
- un `type` est explicitement déclaré (INV-4)

**A-2. Absence de fuite HACS**
`grep -i 'community\|hacsfiles' /homeassistant/lovelace/resources.yaml` doit retourner vide (INV-1, INT-1).

**A-3. Cohérence manifeste ↔ runtime**
Pour chaque ressource, vérifier la cohérence des attributs :

- **nom de la ressource** : présent dans le manifeste ↔ présent dans `resources.yaml` (sauf statut `desactivee_mode_degrade`)
- **fichier cible** : `fichier` du manifeste ↔ nom de fichier dans l'URL `resources.yaml` ↔ fichier physique sur disque
- **version** : `version` du manifeste ↔ version embarquée dans le JS **si exposée et lisible** (commentaire d'en-tête, constante `VERSION`, etc.). Cette dernière vérification est **non bloquante** : nombre de cartes minifient ou n'exposent pas leur version. Une absence de signal est un *unknown*, pas un échec.

Toute divergence détectable est une violation. En cas de divergence, **le manifeste fait foi** (INV-14) et c'est `resources.yaml` ou le runtime qui sont à corriger.

**A-4. Présence des sauvegardes**
Pour chaque dossier `/homeassistant/www/<ressource>/` correspondant à une ressource ayant subi au moins une mise à jour, vérifier la présence d'une sauvegarde locale exploitable (INV-6). Pour les ressources jamais mises à jour, vérifier que le manifeste documente cette absence.

**A-5. Versionnement explicite**
Chaque ligne `version:` du manifeste matche le pattern `v\d+\.\d+\.\d+` (ou équivalent stable, sans `latest`, sans plage) (INV-10).

**A-6. Test de chargement frontend**
Sur un dashboard de test :
- absence d'erreur 404 sur les URL `/local/...`
- absence d'erreur de parsing JS
- absence d'erreur "custom element not defined" pour les cartes attendues

**A-7. Cohérence criticité ↔ usage**
Pour chaque ressource marquée `criticite: critique`, vérifier qu'elle est effectivement utilisée dans au moins un dashboard principal ou pivot. Inversement, identifier les ressources `criticite: secondaire` qui auraient migré vers un usage critique sans mise à jour du manifeste.

**A-8. État du mode dégradé**
Identifier toutes les ressources avec `statut: desactivee_mode_degrade` :
- vérifier que la ligne correspondante dans `resources.yaml` est bien commentée et non supprimée
- vérifier que le manifeste documente la fenêtre de résolution
- alerter si une ressource est en mode dégradé depuis plus de 30 jours sans plan de sortie actualisé

### 9.2 Format du rapport d'audit

```
Audit ressources Lovelace — <date>
[OK] A-1 Cohérence URL ↔ fichier (7/7 ressources)
[OK] A-2 Absence de fuite HACS
[OK] A-3 Cohérence manifeste ↔ runtime (3 versions inspectables / 4 unknown — non bloquant)
[OK] A-4 Présence des sauvegardes (6 .bak / 1 absence assumée : Layout Card)
[OK] A-5 Versionnement explicite
[OK] A-6 Test de chargement frontend
[OK] A-7 Cohérence criticité ↔ usage
[OK] A-8 État du mode dégradé (aucune ressource en mode dégradé)
Conclusion : conforme.
```

Toute mention `[KO]` doit être traitée avant la prochaine modification du frontend.

---

## 10. Tableau d'état canonique

| Ressource         | Dossier runtime              | Fichier actif              | URL `resources.yaml`                              | Version | Criticité  |
|-------------------|------------------------------|----------------------------|---------------------------------------------------|---------|------------|
| Mini Graph Card   | `mini-graph-card/`           | `mini-graph-card-bundle.js`| `/local/mini-graph-card/mini-graph-card-bundle.js`| v0.13.0 | à qualifier|
| Button Card       | `button-card/`               | `button-card.js`           | `/local/button-card/button-card.js`               | v7.0.1  | à qualifier|
| Bar Card          | `bar-card/`                  | `bar-card.js`              | `/local/bar-card/bar-card.js`                     | v3.2.0  | à qualifier|
| Card Mod          | `lovelace-card-mod/`         | `card-mod.js`              | `/local/lovelace-card-mod/card-mod.js`            | v4.2.1  | à qualifier|
| ApexCharts Card   | `apexcharts-card/`           | `apexcharts-card.js`       | `/local/apexcharts-card/apexcharts-card.js`       | v2.2.3  | à qualifier|
| Auto Entities     | `lovelace-auto-entities/`    | `auto-entities.js`         | `/local/lovelace-auto-entities/auto-entities.js`  | v1.16.1 | à qualifier|
| Layout Card       | `lovelace-layout-card/`      | `layout-card.js`           | `/local/lovelace-layout-card/layout-card.js`      | v2.4.7  | à qualifier|

Ce tableau est l'**état de référence** au moment de la rédaction du contrat. La colonne *Criticité* est à qualifier lors d'un passage dédié (cartographie des usages dans les dashboards). Le tableau doit être tenu à jour à chaque modification.

---

## 11. Évolutions futures

- **v1.3** : qualification de la criticité de chaque ressource (INV-12) après cartographie des usages dans les dashboards.
- **v1.4** : intégrer un script d'audit Python (sur le modèle de l'outil d'audit Arsenal) pour automatiser §9.1.
- **v1.5** : envisager un versioning Git du dossier `/homeassistant/www/` pour reconstituer l'historique des `.bak` au-delà de N-1.
- **v1.6** : formaliser une matrice de compatibilité entre versions de cartes et version de Home Assistant Core.

---

## 12. Historique

| Version | Date         | Modification                                                                                                  |
|---------|--------------|---------------------------------------------------------------------------------------------------------------|
| 1.0     | 2026-04-28   | Création initiale.                                                                                            |
| 1.1     | 2026-04-28   | Ajout sections Rôle / Risques / Non-objectifs. INV-4 assoupli. INV-6 reformulé en exigence de résultat.      |
|         |              | Ajout INV-11 (cache navigateur), INV-12 (criticité UI), INV-13 (traçabilité régressions). Manifeste structuré.|
|         |              | INT-3 reformulé en fenêtre de maintenance. Audit A-3 renforcé. Audit A-7 ajouté.                              |
|         |              | Procédures §6 et §7 explicitent le hard reload navigateur. INT-7 ajouté.                                      |
| 1.2     | 2026-04-28   | INV-11 reformulé en exigence de résultat observable (taille / hash / contenu) plutôt que de geste.            |
|         |              | INV-12 : période d'observation passée de "24 h impératif" à "24 h recommandé, adaptable au contexte".         |
|         |              | A-3 : version embarquée dans le JS rendue non bloquante (unknown autorisé).                                   |
|         |              | Procédure §6 : reload Lovelace serveur passé en optionnel ; validation visuelle et console fusionnées.        |
|         |              | Ajout INV-14 (source de vérité fonctionnelle unique) et INT-8 (interdiction de modifier `resources.yaml`     |
|         |              | sans passer par le manifeste).                                                                                |
|         |              | Ajout §8 Mode dégradé (graceful degradation) + statut `desactivee_mode_degrade` + audit A-8.                 |
|         |              | Renumérotation : audit §8 → §9, tableau §9 → §10, évolutions §10 → §11, historique §11 → §12.                |
