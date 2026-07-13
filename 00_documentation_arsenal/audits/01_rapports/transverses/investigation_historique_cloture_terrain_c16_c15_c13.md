# Investigation — faisabilité de clôture par historique (C16, C15, C13)

- **Type :** rapport d'investigation dynamique (historique Recorder), **lecture seule** — aucun runtime, contrat, checker, registre ni changelog modifié.
- **Statut :** investigation close ; **aucune clôture de chantier prononcée** (aucune preuve suffisante trouvée).
- **Question posée :** l'historique Recorder disponible permet-il de solder la validation terrain de C16, C15, C13 ?
- **Réponse :** **non pour les trois** — pour des raisons distinctes, et **sans qu'aucune non-conformité fonctionnelle ne soit démontrée**.
- **Données :** deux sauvegardes Home Assistant non chiffrées (2026-06-23 et 2026-07-13), bases Recorder — **conservées, avec les scripts et le détail technique, hors dépôt** (dépôt privé d'audit runtime). Le présent rapport n'en restitue que la méthode et les verdicts.

---

## 1. Trois constats de nature différente — à ne jamais confondre

Ce rapport sépare strictement trois notions :

1. **Absence de séquence exploitable** — la donnée ne contient pas la *situation* qui permettrait d'exercer le critère (p. ex. aucune pluie réelle après le correctif). Rien à évaluer.
2. **Absence de preuve suffisante** — une séquence partielle existe mais **ne couvre pas intégralement** le critère de clôture ; elle *contextualise* sans *prouver*.
3. **Non-conformité fonctionnelle** — la donnée montre le runtime se comporter **contrairement** au contrat.

> **Résultat cardinal.** Les trois chantiers relèvent de (1) ou (2). **Aucun** ne relève de (3). L'historique **n'a révélé aucun défaut de comportement** : il manque seulement la séquence de confirmation. « Non clôturable par historique » signifie ici *« preuve absente »*, **jamais** *« correctif invalidé »*.

## 2. Méthode et couverture

- Couverture combinée **continue** : **2026-05-24 → 2026-07-13** (~50 jours, deux sauvegardes).
- Le Recorder fonctionne en **liste blanche** (`recorder.yaml`, `include: entities:`). Conséquence structurelle : les **entités d'état décisives** de C15 et C13 (`input_boolean` de mode/cycle, `counter` de reprise, jalon de stabilisation au démarrage, état d'épisode pluie) **ne sont pas historisées**. Seules les traces **`call_service`** (table `events`) et les marqueurs de redémarrage permettent une lecture *indirecte* de leurs effets.
- Dates de déploiement des correctifs (établies par l'historique Git du dépôt) : **C13 = 2026-07-03**, **C15 = 2026-07-09**, **C16 = 2026-07-11**. Toute occurrence antérieure relève de l'**ancien** comportement : contexte, jamais preuve du correctif.

## 3. Verdicts par chantier

### C16 — état collant `pluie_en_cours` — **absence de séquence exploitable**
Le capteur d'évidence consolidée introduit par le correctif n'apparaît dans l'historique que depuis le **2026-07-11** et n'a **jamais** signalé de pluie ensuite : **aucun épisode de pluie réel après le correctif**. L'état d'épisode lui-même n'est de toute façon pas historisé. Ni le critère anti-collage ni le critère d'ouverture ne peuvent être exercés.
→ **Non clôturable par historique. Aucune non-conformité observée. Validation live requise (prochaine pluie réelle).**

### C15 — survie des notifications persistantes au reboot — **absence de preuve suffisante**
Le déclencheur de re-projection au démarrage **s'exécute bel et bien** (observé : exécution de la branche de retrait des projections — appels `persistent_notification.dismiss` — à chaque redémarrage post-correctif). Mais **aucun redémarrage n'a coïncidé avec un état actif après le 2026-07-09** : la branche décisive — reboot pendant un cycle/mode actif suivi du **ré-affichage** de la persistante — n'a **aucune occurrence** post-correctif. Les cas « reboot pendant état actif » présents dans l'historique sont **tous antérieurs** au correctif et illustrent l'**ancien** comportement (notification perdue) : contexte, jamais preuve.
→ **Non clôturable par historique. Aucune non-conformité observée (le mécanisme de boot est vu s'exécuter). Validation live requise (reboot volontaire pendant un cycle actif).**

### C13 — notification d'échec d'exécution persistant (D5) — **absence de séquence exploitable**
Sur toute la fenêtre post-correctif, l'événement déclencheur — échec d'exécution latché **et** budget de reprise épuisé — **ne s'est jamais produit**. La notification n'a donc jamais eu à être créée. Le chemin de reconstruction/nettoyage s'exécute normalement à chaque déclenchement (y compris au démarrage), mais la branche de création n'a pas été exercée, faute d'occurrence.
→ **Non clôturable par historique. Aucune non-conformité observée. Validation par occurrence réelle future ou test provoqué.**

## 4. Conclusion

Les trois chantiers **restent en validation terrain — statut inchangé et exact**. Aucune clôture. La cause est double :
- **structurelle** — pour C15 et C13, les entités d'état décisives sont hors liste blanche Recorder ; la preuve repose donc sur une reconstruction indirecte à partir des événements, moins complète qu'un historique d'états ;
- **de fenêtre** — pour C16, le correctif est trop récent et aucune pluie n'a suivi.

**Limite d'observabilité constatée.** L'absence des entités d'état décisives de C15 et C13 dans la liste blanche Recorder réduit la qualité et la portée de la preuve historique directe. Une clôture rétrospective reste possible si les événements `call_service`, les marqueurs de redémarrage et les effets observables permettent de reconstruire sans ambiguïté une séquence complète. À défaut, une validation live ou une instrumentation temporaire ciblée du Recorder sera nécessaire. Ce rapport constate cette limite ; il ne décide d'aucune modification de la liste blanche.
