# Arsenal — Navigation UI (référence structurelle)

## 1. Objet du document

Ce document est la **référence structurelle de la navigation UI Arsenal**. Il définit la grammaire de déplacement entre dashboards et les invariants qui la rendent stable.

Ce qu'il **n'est pas** :

- ce n'est **pas un guide utilisateur** (il ne décrit pas des parcours d'usage) ;
- ce n'est **pas un contrat métier** (il ne porte aucune règle fonctionnelle de domaine) ;
- ce n'est **pas une documentation runtime Lovelace détaillée** (l'implémentation fine — includes, templates button-card, surcharges — vit dans le code et dans les audits Lovelace ; voir §10).

> En cas de divergence sur un point d'implémentation, le **code Lovelace et le contrat `R-LL-NAV-1` font foi**. Ce document formalise la doctrine ; il ne la duplique pas ligne à ligne.

---

## 2. Doctrine fondamentale

> **La navigation Arsenal est une couche d'orientation persistante et transversale, indépendante de toute logique métier.**

La navigation :

- **ne décide rien** : elle n'arbitre, ne calcule, n'interprète aucun état ;
- **ne porte aucune logique fonctionnelle** : aucun élément de navigation ne déclenche d'action métier ;
- **expose une grammaire de déplacement stable** : un ensemble réduit et constant de gestes (aller à l'Accueil, ouvrir la Navigation, remonter au parent, ouvrir les Réglages / Diagnostics du domaine).

Elle **oriente**, **organise**, **redirige** — rien de plus.

---

## 3. Architecture mono-vue

Arsenal est **mono-vue par dashboard**. C'est un invariant d'architecture, pas une simple convention.

- **Un domaine fonctionnel = un dashboard.**
- **Un dashboard = une vue.**
- **Aucune navigation intra-dashboard** : un dashboard ne dépend jamais d'un déplacement entre vues internes.
- **Pas de retour au modèle Home Assistant UI multi-vues** (voir §9).

La conséquence directe est la grammaire canonique de la §4 : puisqu'un dashboard n'a qu'une vue, la navigation cible **le dashboard**, jamais une vue interne.

---

## 4. Grammaire canonique des chemins

La forme canonique d'un `navigation_path` interne Arsenal est **strictement** :

```
/<dashboard-key>
```

où `<dashboard-key>` est une clé déclarée dans `18_lovelace/dashboards.yaml`.

Sont **interdits** :

- `/<dashboard-key>/<segment>` — un segment de vue nommé ; reliquat de l'ancienne grammaire (§9) ;
- `/<dashboard-key>/0` — un segment de vue numérique ; ancienne forme de transition, désormais proscrite.

Règle complémentaire :

- **Ne jamais ajouter de `path:` à une vue** pour légitimer un segment existant. Ajouter un `path:` recréerait, de fait, une grammaire multi-vues que l'architecture a justement abandonnée.

Ces interdictions sont **vérifiées et bloquées en CI** par le contrat `R-LL-NAV-1` (§10). La seule exemption tolérée concerne un segment correspondant à un `path:` de vue **réellement déclaré** par le dashboard cible — situation résiduelle, non un motif pour en créer de nouvelles.

---

## 5. Points d'entrée et hubs

Trois dashboards structurent la circulation. Ce sont les seuls « hubs » ; il n'en existe pas d'autres.

- **Arsenal** (`arsenal-dashboard`) — **point d'entrée principal**, seul dashboard épinglé à la barre latérale. Vue synthétique des grands domaines, actions globales **volontaires et explicites**, et **point de retour universel** : tout dashboard doit permettre de revenir à Arsenal.
- **Navigation** (`navigation-dashboard`) — **trame globale de déplacement**. Expose l'ensemble des domaines fonctionnels, les accès système et diagnostics, et les transitions entre dashboards. Conceptuellement persistante, atteignable depuis tout dashboard, indépendante du contenu affiché.
- **Système** (`system-dashboard`) — **hub structurel des diagnostics système** (alimentation, onduleur, boiler, Zigbee, Bluetooth, batteries, etc.). Les feuilles de diagnostic système y remontent via leur **Retour contextuel**.

**Retours contextuels** : le bouton Retour n'est pas un raccourci fixe vers l'Accueil. Chaque page **surcharge** sa cible vers son **parent logique** — dashboard de domaine pour une page de réglages/diagnostics, ou **Système** pour une feuille système. C'est un véritable « remonter d'un niveau ». Cette description vise les **sous-dashboards hiérarchiques** (Classe B) ; la taxonomie complète des relations entre dashboards et les conditions d'obligation du Retour sont formalisées au §6.

---

## 6. Taxonomie des dashboards et Retour contextuel (Classes A–E)

> Cette taxonomie a été **arbitrée humainement** à l'issue d'un audit de navigation clos (cf. [`audit_navigation_ui_lovelace.md`](../audits/01_rapports/lovelace/audit_navigation_ui_lovelace.md)). Elle **précise** — sans la contredire — la notion de Retour contextuel du §5 : elle répond à la question laissée ouverte « pour quels dashboards le Retour est-il réellement obligatoire ? ».

### 6.1 Les cinq classes

Tout dashboard Arsenal relève d'**exactement une** classe, déterminée par sa relation aux autres dashboards :

- **Classe A — Racine.** Dashboard exposé directement depuis `navigation-dashboard`. Dashboard de premier niveau : **aucun bouton Retour contextuel obligatoire**. Être exposé depuis Navigation est **suffisant** pour être Classe A ; mais l'**absence** d'exposition dans Navigation **ne suffit jamais**, à elle seule, à en conclure qu'un dashboard est un sous-dashboard hiérarchique (§6.3).
- **Classe B — Sous-dashboard hiérarchique à parent unique.** Dashboard dont la relation avec un autre dashboard est **explicitement déclarée hiérarchique** (intention architecturale, §6.3). **Retour obligatoire**, ciblant le **parent fonctionnel déclaré**, comme **action contextuelle dédiée** — jamais un simple lien latéral qui se trouve mener vers ce même parent. Exemples : `nas-dashboard` → `system-dashboard` (conforme, PR #828) ; `meteo-min-max-temperature-dashboard` → `meteo-temperature-dashboard` (actuellement **non conforme** — correction différée à un chantier runtime ultérieur, hors périmètre du présent document).
- **Classe C — Facette latérale de domaine.** Dashboard relié à des pairs par un bandeau ou un mécanisme de bascule de domaine (§8). La relation est **latérale**, pas hiérarchique : **pas de bouton Retour obligatoire au seul motif** qu'un autre dashboard permet d'y accéder. Une facette Classe C peut être **volontairement non exposée** dans Navigation (place limitée, importance fonctionnelle secondaire) sans devenir, de ce seul fait, un sous-dashboard hiérarchique. Exemple confirmé : `ecs-petite-maison-dashboard` (accès voulu via le bandeau ECS, non exposée dans Navigation, conforme **sans** Retour vers `ecs-dashboard`). Autres exemples de maillage latéral Classe C : Voiture, Aspirateur, Imprimerie.
- **Classe D — Ressource partagée multi-parent.** Dashboard de réglage / diagnostic / ressource utilisé depuis plusieurs dashboards **sans parent fonctionnel unique**. Ne pas inventer de Retour arbitraire : Accueil et Navigation suffisent tant qu'aucun parent unique n'est déclaré. Exemples : `reglages-meteo-dashboard`, `meteo-backups-dashboard`.
- **Classe E — Raccourci secondaire.** Accès secondaire depuis une carte, un `hold_action`, ou un geste transversal. Ce type de lien **ne crée pas** une relation parent/enfant et **ne modifie pas** la parenté principale du dashboard cible. Exemple : l'accès secondaire à `reglages-maison-dashboard` depuis Arsenal, alors que son parent fonctionnel reste `modes-dashboard`.

### 6.2 Définition normative du Retour

> **Un Retour est une action de navigation contextuelle dédiée qui ramène un sous-dashboard hiérarchique à parent fonctionnel unique vers ce parent, indépendamment des éventuels bandeaux de navigation latérale présents sur la page.**

Précisions opposables, indissociables de la définition :

- un dashboard **sans parent fonctionnel unique** (Classes A, C, D, E) **n'est pas soumis** à l'obligation de Retour ;
- un lien latéral qui mène **par coïncidence** vers le parent (bandeau, carte, `hold_action`) **ne constitue pas** un Retour ;
- l'**absence d'exposition dans Navigation ne prouve jamais**, à elle seule, une relation hiérarchique ;
- le **nombre de liens entrants** ne permet **jamais**, à lui seul, d'inférer une parenté ;
- la frontière entre Classe B et Classe C relève de l'**intention architecturale déclarée**, jamais d'une heuristique sur le graphe de navigation (§6.3).

### 6.3 Frontière B/C — interdiction d'inférence heuristique

La distinction entre un sous-dashboard hiérarchique (Classe B, Retour obligatoire) et une facette latérale (Classe C, Retour non requis) **ne se déduit d'aucun des signaux suivants**, pris isolément ou combinés — un audit de navigation l'a démontré sur le cas `ecs-petite-maison-dashboard` :

- l'**absence** de la page dans `navigation-dashboard` ;
- le **nombre de prédécesseurs** dans le graphe de navigation (pages qui pointent vers elle) ;
- une **asymétrie des badges** Réglages/Diagnostics ;
- la **réciprocité ou non** d'un bandeau de bascule de domaine.

Seule fait foi une **déclaration explicite de l'intention architecturale** : ce dashboard est-il pensé comme un niveau hiérarchique d'un autre, ou comme une facette parmi d'autres d'un même domaine ? La forme de cette déclaration est **hors périmètre du présent document** (§6.4).

### 6.4 Règle future — gouvernance CI

> **Classe B ⇒ Retour obligatoire vers le parent déclaré.**

Cette règle est **normative dès à présent** pour toute création ou revue de dashboard. Sa **vérification automatique en CI** est différée : le checker `R-LL-NAV-1` (§10) sait aujourd'hui contrôler la **cohérence** d'un Retour déjà présent (sa cible est-elle un parent réel ou un hub structurel ?), mais ne vérifie pas encore l'**obligation** de Retour pour un sous-dashboard Classe B — cette vérification suppose une déclaration explicite de l'intention architecturale (§6.3), dont la forme reste à concevoir dans un chantier ultérieur. Tant que ce mécanisme n'existe pas, la future CI **ne doit pas deviner** la topologie à partir des heuristiques structurelles proscrites au §6.3 : l'absence de vérification automatisée d'un cas Classe B n'autorise aucune inférence de conformité, ni de non-conformité, par un autre moyen que la revue humaine.

### 6.5 Cas de référence

| Dashboard | Classe | Retour attendu | État |
|---|---|---|---|
| `nas-dashboard` | B | → `system-dashboard` | ✅ conforme (PR #828) |
| `meteo-min-max-temperature-dashboard` | B | → `meteo-temperature-dashboard` | ❌ non conforme — correction runtime différée |
| `ecs-petite-maison-dashboard` | C | aucun (bandeau ECS) | ✅ conforme, volontairement non exposée en Navigation |
| Voiture / Aspirateur / Imprimerie | C | aucun (bandeau de domaine) | maillage latéral |
| `reglages-meteo-dashboard`, `meteo-backups-dashboard` | D | aucun (Accueil/Navigation suffisent) | conforme |
| `reglages-maison-dashboard` via `hold_action` Arsenal | E (accès secondaire) | parent principal inchangé = `modes-dashboard` | conforme |

---

## 7. Badges de navigation

Les badges en tête de dashboard sont les points d'accès **invariants**. Cinq rôles, tous **purement directionnels** :

- **Accueil** — retour à Arsenal ;
- **Navigation** — ouverture de la trame globale ;
- **Retour** — remontée vers le parent logique (contextuel) ;
- **Réglages** — accès aux réglages du domaine courant ;
- **Diagnostics** — accès aux diagnostics du domaine courant.

Principes :

- **Aucune action métier** : un badge navigue, point. Il ne pilote rien, ne modifie aucun état.
- **Surcharges d'instance** : Accueil et Navigation sont fixes ; **Retour, Réglages et Diagnostics sont contextuels** et **surchargent leur cible par instance** vers le bon parent / le bon domaine. Un audit ou un contrôle qui lit la valeur *par défaut* d'un template au lieu de la *surcharge réelle* conclut faux — la résolution des surcharges est obligatoire avant toute conclusion (§10).
- **Factorisation par includes** : de nombreux dashboards déclarent leurs badges via un `!include` partagé. Le contenu réel des badges vit alors dans le fichier inclus, pas dans le dashboard ; il doit être **résolu** avant tout constat.
- **Obligation de Retour** : seule la Classe B (§6) impose ce badge comme action contextuelle dédiée ; les autres classes ne sont tenues qu'à Accueil + Navigation.

---

## 8. Bandeaux contextuels

Certains domaines exposent un **bandeau** latéral de raccourcis (météo, voiture, imprimerie, planning ECS). Un bandeau **n'est pas un sous-système de navigation** : il **n'a pas de navigation propre** et **ne redéfinit pas** la trame globale.

- Il **réutilise** la structure de navigation existante et y ajoute un **raccourci de domaine** (basculer entre les facettes d'un même domaine : températures, humidité, CO₂… pour la météo ; facettes véhicule ; zones imprimerie ; etc.).
- Il est **stateless**, **purement visuel**, **strictement directionnel**, et **sans logique métier**.
- Il reste **borné à son domaine** : un bandeau météo ne navigue que dans la météo.

Les badges Accueil + Navigation restent présents **en tête de page**, avant le bandeau : un bandeau ne remplace jamais les points d'accès invariants.

Un bandeau matérialise typiquement une relation **Classe C** (§6) entre les facettes qu'il relie : il ne crée ni n'implique, à lui seul, aucune obligation de Retour.

---

## 9. Sortie du modèle Home Assistant UI multi-vues (historique)

> L'ancien modèle est mentionné comme **abandonné**, non effacé : il explique l'existence passée des segments de vue.

**Ancien modèle (abandonné).** Arsenal a d'abord suivi la grammaire native Home Assistant UI : quelques dashboards **multi-vues**, notamment un dashboard **Réglages** multi-vues et un dashboard **Diagnostics** multi-vues, où chaque domaine était une *vue interne* atteinte par un segment (`/<dashboard-key>/<segment>`).

**Reliquats supprimés.** Ces segments de vue étaient les **vestiges** de ce modèle. Ils ont été intégralement normalisés (segments nommés puis numériques `/0`), puis leur réapparition a été rendue bloquante.

**Grammaire actuelle.** Chaque réglage et chaque diagnostic de domaine est désormais **son propre dashboard mono-vue**, ciblé **directement** par `/<dashboard-key>`. Arsenal est **sorti** de la grammaire multi-vues HA : on ne cible plus une vue dans un dashboard, on cible un dashboard.

---

## 10. Contrôle contractuel — `R-LL-NAV-1`

La doctrine ci-dessus n'est pas seulement déclarative : elle est **gardée en CI** par le contrat `R-LL-NAV-1` (`scripts/arsenal_contracts/check_lovelace_navigation_contracts.py`, workflow `contracts_lovelace_navigation.yml`).

Principe méthodologique : le contrôle **résout les `!include` et les surcharges d'instance avant toute conclusion** — un contrôle purement textuel est proscrit.

Règles (résumé ; le détail vit dans le checker et les audits Lovelace) :

- **R1 — erreur bloquante** : tout `navigation_path` interne cible une **clé de dashboard existante**.
- **R2 — erreur bloquante** : **cohérence du Retour** (cible = parent réel de la page, ou hub structurel).
- **R3 — erreur bloquante** : **aucun cul-de-sac** après résolution.
- **R4 — erreur bloquante** : **forme canonique stricte `/<dashboard-key>`** ; `/<dashboard-key>/<segment>` et `/<dashboard-key>/0` sont rejetés.
- **R5 — warning non bloquant (volontaire)** : défauts latents des templates Réglages/Diagnostics (cibles par défaut surchargées partout — sans impact runtime). Conservé comme dette tracée, non masqué.

La CI agit comme **garde de non-régression** : toute réintroduction d'un segment de vue ou d'un `/0` échoue le contrôle.

**Périmètre actuel vs futur** : R2 vérifie la **cohérence** d'un Retour déjà présent (cible = parent réel ou hub structurel) ; il ne vérifie pas encore l'**obligation** de Retour pour un sous-dashboard Classe B (§6.4) — cette extension future suppose une déclaration explicite de l'intention architecturale, non encore conçue.

Détail complet : checker `R-LL-NAV-1` et rapport [`audit_navigation_ui_lovelace.md`](../audits/01_rapports/lovelace/audit_navigation_ui_lovelace.md) (constat historique + clôture).

---

## 11. Ce que la navigation n'est PAS

- ❌ un **moteur métier** ;
- ❌ une **automatisation** ;
- ❌ une **couche de décision** ;
- ❌ une **zone d'empilement de vues** Home Assistant.

Elle ne calcule rien, n'arbitre rien, n'interprète rien, n'empile rien.

---

## 12. Règles non négociables

1. **Arsenal accessible partout** : tout dashboard permet de revenir à Arsenal.
2. **Navigation accessible partout** : la trame globale est atteignable depuis tout dashboard.
3. **Retour contextuel cohérent et obligatoire pour la Classe B** : tout sous-dashboard hiérarchique à parent unique (Classe B, §6) expose un Retour vers son **parent fonctionnel déclaré**, jamais vers une page sans rapport ; les autres classes n'y sont pas soumises.
4. **Chemins internes canoniques** : `navigation_path` interne = `/<dashboard-key>`, strictement.
5. **Aucun segment de vue** : `/<dashboard-key>/<segment>` interdit.
6. **Aucun `/0`** : `/<dashboard-key>/0` interdit.
7. **Aucune action métier** dans un élément de navigation (badge ou bandeau).
8. **Aucun `path:` de vue** ajouté pour justifier une ancienne forme.
9. **Aucune inférence heuristique de parenté** : l'absence d'exposition dans Navigation, le nombre de liens entrants, ou une asymétrie de badges/bandeau ne permettent jamais, seuls, de conclure à une relation hiérarchique (Classe B) ou à son absence — seule l'intention architecturale déclarée fait foi (§6.3).

---

## 13. Hiérarchie globale (lecture fonctionnelle)

```
Arsenal  (point d'entrée — barre latérale)
│
├── Navigation  (trame globale)
│   ├── Domaines métier — un dashboard mono-vue par domaine
│   │   ├── Chauffage   → /chauffage-dashboard
│   │   ├── Climatisation → /clim-dashboard
│   │   ├── VMC         → /vmc-dashboard
│   │   └── …
│   │
│   ├── Réglages / Diagnostics — un dashboard mono-vue par (domaine × facette)
│   │   ├── /reglages-<domaine>-dashboard
│   │   └── /diagnostics-<domaine>-dashboard
│   │
│   └── Système — hub des diagnostics système
│       └── /system-dashboard  (Retour des feuilles système)
│
└── Bandeaux contextuels — raccourcis de domaine (météo, voiture, imprimerie, ECS)
    └── réutilisent la navigation ; ne la redéfinissent pas
```

---

## Statut du document

- **Portée** : UI Arsenal.
- **Nature** : **document normatif** de référence structurelle de la navigation.
- **Modifiable uniquement si** la doctrine de navigation évolue, ou si les **hubs** (Arsenal / Navigation / Système) changent. Une évolution de ce document doit rester cohérente avec le contrat `R-LL-NAV-1`.

---

## Phrase canonique

> **La navigation Arsenal est une structure de déplacement persistante et transversale, mono-vue par dashboard, qui cible toujours un dashboard (`/<dashboard-key>`) et jamais une vue interne — pour orienter l'utilisateur sans jamais intervenir sur la logique métier.**
