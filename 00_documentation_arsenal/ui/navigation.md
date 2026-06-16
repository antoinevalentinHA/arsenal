# Arsenal — Navigation UI (référence structurelle)

## 1. Objet du document

Ce document est la **référence structurelle de la navigation UI Arsenal**. Il définit la grammaire de déplacement entre dashboards et les invariants qui la rendent stable.

Ce qu'il **n'est pas** :

- ce n'est **pas un guide utilisateur** (il ne décrit pas des parcours d'usage) ;
- ce n'est **pas un contrat métier** (il ne porte aucune règle fonctionnelle de domaine) ;
- ce n'est **pas une documentation runtime Lovelace détaillée** (l'implémentation fine — includes, templates button-card, surcharges — vit dans le code et dans les audits Lovelace ; voir §9).

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
- **Pas de retour au modèle Home Assistant UI multi-vues** (voir §8).

La conséquence directe est la grammaire canonique de la §4 : puisqu'un dashboard n'a qu'une vue, la navigation cible **le dashboard**, jamais une vue interne.

---

## 4. Grammaire canonique des chemins

La forme canonique d'un `navigation_path` interne Arsenal est **strictement** :

```
/<dashboard-key>
```

où `<dashboard-key>` est une clé déclarée dans `18_lovelace/dashboards.yaml`.

Sont **interdits** :

- `/<dashboard-key>/<segment>` — un segment de vue nommé ; reliquat de l'ancienne grammaire (§8) ;
- `/<dashboard-key>/0` — un segment de vue numérique ; ancienne forme de transition, désormais proscrite.

Règle complémentaire :

- **Ne jamais ajouter de `path:` à une vue** pour légitimer un segment existant. Ajouter un `path:` recréerait, de fait, une grammaire multi-vues que l'architecture a justement abandonnée.

Ces interdictions sont **vérifiées et bloquées en CI** par le contrat `R-LL-NAV-1` (§9). La seule exemption tolérée concerne un segment correspondant à un `path:` de vue **réellement déclaré** par le dashboard cible — situation résiduelle, non un motif pour en créer de nouvelles.

---

## 5. Points d'entrée et hubs

Trois dashboards structurent la circulation. Ce sont les seuls « hubs » ; il n'en existe pas d'autres.

- **Arsenal** (`arsenal-dashboard`) — **point d'entrée principal**, seul dashboard épinglé à la barre latérale. Vue synthétique des grands domaines, actions globales **volontaires et explicites**, et **point de retour universel** : tout dashboard doit permettre de revenir à Arsenal.
- **Navigation** (`navigation-dashboard`) — **trame globale de déplacement**. Expose l'ensemble des domaines fonctionnels, les accès système et diagnostics, et les transitions entre dashboards. Conceptuellement persistante, atteignable depuis tout dashboard, indépendante du contenu affiché.
- **Système** (`system-dashboard`) — **hub structurel des diagnostics système** (alimentation, onduleur, boiler, Zigbee, Bluetooth, batteries, etc.). Les feuilles de diagnostic système y remontent via leur **Retour contextuel**.

**Retours contextuels** : le bouton Retour n'est pas un raccourci fixe vers l'Accueil. Chaque page **surcharge** sa cible vers son **parent logique** — dashboard de domaine pour une page de réglages/diagnostics, ou **Système** pour une feuille système. C'est un véritable « remonter d'un niveau ».

---

## 6. Badges de navigation

Les badges en tête de dashboard sont les points d'accès **invariants**. Cinq rôles, tous **purement directionnels** :

- **Accueil** — retour à Arsenal ;
- **Navigation** — ouverture de la trame globale ;
- **Retour** — remontée vers le parent logique (contextuel) ;
- **Réglages** — accès aux réglages du domaine courant ;
- **Diagnostics** — accès aux diagnostics du domaine courant.

Principes :

- **Aucune action métier** : un badge navigue, point. Il ne pilote rien, ne modifie aucun état.
- **Surcharges d'instance** : Accueil et Navigation sont fixes ; **Retour, Réglages et Diagnostics sont contextuels** et **surchargent leur cible par instance** vers le bon parent / le bon domaine. Un audit ou un contrôle qui lit la valeur *par défaut* d'un template au lieu de la *surcharge réelle* conclut faux — la résolution des surcharges est obligatoire avant toute conclusion (§9).
- **Factorisation par includes** : de nombreux dashboards déclarent leurs badges via un `!include` partagé. Le contenu réel des badges vit alors dans le fichier inclus, pas dans le dashboard ; il doit être **résolu** avant tout constat.

---

## 7. Bandeaux contextuels

Certains domaines exposent un **bandeau** latéral de raccourcis (météo, voiture, imprimerie, planning ECS). Un bandeau **n'est pas un sous-système de navigation** : il **n'a pas de navigation propre** et **ne redéfinit pas** la trame globale.

- Il **réutilise** la structure de navigation existante et y ajoute un **raccourci de domaine** (basculer entre les facettes d'un même domaine : températures, humidité, CO₂… pour la météo ; facettes véhicule ; zones imprimerie ; etc.).
- Il est **stateless**, **purement visuel**, **strictement directionnel**, et **sans logique métier**.
- Il reste **borné à son domaine** : un bandeau météo ne navigue que dans la météo.

Les badges Accueil + Navigation restent présents **en tête de page**, avant le bandeau : un bandeau ne remplace jamais les points d'accès invariants.

---

## 8. Sortie du modèle Home Assistant UI multi-vues (historique)

> L'ancien modèle est mentionné comme **abandonné**, non effacé : il explique l'existence passée des segments de vue.

**Ancien modèle (abandonné).** Arsenal a d'abord suivi la grammaire native Home Assistant UI : quelques dashboards **multi-vues**, notamment un dashboard **Réglages** multi-vues et un dashboard **Diagnostics** multi-vues, où chaque domaine était une *vue interne* atteinte par un segment (`/<dashboard-key>/<segment>`).

**Reliquats supprimés.** Ces segments de vue étaient les **vestiges** de ce modèle. Ils ont été intégralement normalisés (segments nommés puis numériques `/0`), puis leur réapparition a été rendue bloquante.

**Grammaire actuelle.** Chaque réglage et chaque diagnostic de domaine est désormais **son propre dashboard mono-vue**, ciblé **directement** par `/<dashboard-key>`. Arsenal est **sorti** de la grammaire multi-vues HA : on ne cible plus une vue dans un dashboard, on cible un dashboard.

---

## 9. Contrôle contractuel — `R-LL-NAV-1`

La doctrine ci-dessus n'est pas seulement déclarative : elle est **gardée en CI** par le contrat `R-LL-NAV-1` (`scripts/arsenal_contracts/check_lovelace_navigation_contracts.py`, workflow `contracts_lovelace_navigation.yml`).

Principe méthodologique : le contrôle **résout les `!include` et les surcharges d'instance avant toute conclusion** — un contrôle purement textuel est proscrit.

Règles (résumé ; le détail vit dans le checker et les audits Lovelace) :

- **R1 — erreur bloquante** : tout `navigation_path` interne cible une **clé de dashboard existante**.
- **R2 — erreur bloquante** : **cohérence du Retour** (cible = parent réel de la page, ou hub structurel).
- **R3 — erreur bloquante** : **aucun cul-de-sac** après résolution.
- **R4 — erreur bloquante** : **forme canonique stricte `/<dashboard-key>`** ; `/<dashboard-key>/<segment>` et `/<dashboard-key>/0` sont rejetés.
- **R5 — warning non bloquant (volontaire)** : défauts latents des templates Réglages/Diagnostics (cibles par défaut surchargées partout — sans impact runtime). Conservé comme dette tracée, non masqué.

La CI agit comme **garde de non-régression** : toute réintroduction d'un segment de vue ou d'un `/0` échoue le contrôle.

Détail complet : checker `R-LL-NAV-1` et rapport [`audit_navigation_ui_lovelace.md`](../audits/01_rapports/lovelace/audit_navigation_ui_lovelace.md) (constat historique + clôture).

---

## 10. Ce que la navigation n'est PAS

- ❌ un **moteur métier** ;
- ❌ une **automatisation** ;
- ❌ une **couche de décision** ;
- ❌ une **zone d'empilement de vues** Home Assistant.

Elle ne calcule rien, n'arbitre rien, n'interprète rien, n'empile rien.

---

## 11. Règles non négociables

1. **Arsenal accessible partout** : tout dashboard permet de revenir à Arsenal.
2. **Navigation accessible partout** : la trame globale est atteignable depuis tout dashboard.
3. **Retour contextuel cohérent** : le Retour remonte vers le parent logique, jamais vers une page sans rapport.
4. **Chemins internes canoniques** : `navigation_path` interne = `/<dashboard-key>`, strictement.
5. **Aucun segment de vue** : `/<dashboard-key>/<segment>` interdit.
6. **Aucun `/0`** : `/<dashboard-key>/0` interdit.
7. **Aucune action métier** dans un élément de navigation (badge ou bandeau).
8. **Aucun `path:` de vue** ajouté pour justifier une ancienne forme.

---

## 12. Hiérarchie globale (lecture fonctionnelle)

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
