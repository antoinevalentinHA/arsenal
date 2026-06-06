# Arsenal

> Home Assistant, traité comme un logiciel. Gouverné comme tel.

La plupart des installations Home Assistant sont des configurations. Arsenal est un **système** : chaque domaine y répond à un contrat écrit, ce contrat est confronté à l'implémentation **par intégration continue**, et chaque domaine est suivi par un cycle d'audit jusqu'à sa **clôture**.

Ce n'est pas un dump de config à copier. C'est une démonstration : on *peut* faire tenir une maison connectée aux standards d'un logiciel sérieux — et le prouver, fichier par fichier.

---

## Le problème

Home Assistant est puissant, et c'est précisément ce qui le rend facile à laisser dériver :

- des automatisations qui en déclenchent d'autres ;
- de la logique métier éparpillée entre l'UI, les scripts, les automations et les helpers ;
- des dashboards qui *agissent* au lieu de *montrer* ;
- des entités dont plus personne ne sait si elles servent encore ;
- un `configuration.yaml` qui grossit organiquement depuis des années.

La dette s'accumule, invisible, jusqu'à la rupture. Arsenal répond à une seule question :

> Comment construire une installation HA qui reste maintenable, observable et cohérente sur plusieurs années ?

---

## Trois principes non négociables

**Le backend décide. L'UI observe. Jamais l'inverse.**
Aucune logique dans les dashboards. Les cartes affichent des états — elles ne les calculent pas.

**Contrat avant YAML.**
Chaque domaine a un contrat écrit *avant* d'avoir du code : entités impliquées, transitions valides, invariants à respecter. Le YAML implémente le contrat — si l'implémentation contredit le contrat, c'est l'implémentation qui est fausse.

**L'exposition est une décision, pas un accident.**
Ce qui sort vers l'extérieur (API, MQTT, notifications) est explicitement gouverné. La séparation interne/externe est une contrainte d'architecture, pas une convention de nommage.

---

## Ce qui rend Arsenal différent

Beaucoup de projets revendiquent une « architecture propre ». Peu la rendent **opposable**.

Chez Arsenal, les contrats ne sont pas des commentaires : ce sont des documents de référence confrontés au code. Une quinzaine de domaines sont contractualisés — chauffage, ECS, climatisation, alarme, aération, météo… — sur plusieurs centaines de fichiers de contrat, adossés à une bibliothèque de doctrines (nommage, séparation décision/action, gestion du temps, causalité métier).

Et surtout : **cette discipline est exécutée par la machine.** Une intégration continue confronte les implémentations à leurs contrats, domaine par domaine. La documentation elle-même est gouvernée — conventions de nommage vérifiées, index sans rapport orphelin, le tout sous CI. La gouvernance n'est pas un vœu ; c'est un test qui passe ou qui échoue.

La meilleure façon de le croire, c'est de regarder un domaine en entier.

---

## L'architecture, en une image

```
┌─────────────────────────────────────────────┐
│  Capteurs physiques · Intégrations · MQTT   │  PERCEPTION
└───────────────────────┬─────────────────────┘
                        │ états bruts
                        ▼
┌─────────────────────────────────────────────┐
│  Template sensors · Helpers · Admissibilité │  DÉCISION
└───────────────────────┬─────────────────────┘
                        │ états de décision
                        ▼
┌─────────────────────────────────────────────┐
│  Automatisations · Scripts souverains       │  EXÉCUTION
└───────────────────────┬─────────────────────┘
                        │ commandes
                        ▼
                    Hardware
```

La perception mesure, la décision conclut, l'exécution applique. L'UI n'apparaît pas dans ce flux : elle l'observe. Le détail des couches et des doctrines vit dans [`architecture/index.md`](00_documentation_arsenal/architecture/index.md).

---

## La gouvernance, prouvée sur un domaine

L'argument le plus solide n'est pas une promesse d'architecture : c'est une chaîne qu'on peut suivre sur des fichiers réels. Prenons le chauffage comme témoin.

Son **contrat** ([`contrats/chauffage/`](00_documentation_arsenal/contrats/chauffage/README.md)) dit ce que le domaine doit faire ; la décision est centralisée dans un script souverain qui ne produit que des états *lisibles* (`binary_sensor.chauffage_autorise_systeme`, `meteo_favorable_chauffage`, `poele_en_fonction`…). À chaque `push`, le workflow [`arsenal-ci-chauffage.yml`](.github/workflows/arsenal-ci-chauffage.yml) confronte l'implémentation au contrat : un self-test garde les analyseurs (on ne juge pas avec un juge défectueux), puis des étages *lint*, *décision* (`R-COV-1` / `R-MIRROR-1`) et *exécution* (`R-CALL-1`) rendent le verdict, contre un registre d'entités souverain — le domaine étant dans une transition documentée *warn-only → bloquant* (`ARSENAL_CI_ENFORCE`). Et l'audit est tracé jusqu'à sa [clôture](00_documentation_arsenal/audits/05_clotures/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md), où chaque constat est résorbé ou explicitement assumé.

Le héros de cette section n'est pas le chauffage : c'est la chaîne **contrat → CI → audit → clôture**. Le chauffage la rend simplement vérifiable — par vous, dans les fichiers liés.

---

## Comment Arsenal se gouverne

Le chauffage n'est pas une exception : c'est le motif.

Chaque domaine suit la même chaîne — **contrat → implémentation → vérification CI → audit → clôture** —, validée par une intégration continue par domaine. Le cycle d'audit n'est pas informel : rapports, contre-expertises, arbitrages, plans d'action, chantiers et clôtures sont des documents datés et traçables.

La documentation elle-même est soumise au même régime. Le corpus est tenu par ses propres gates, vérifiées en CI à chaque modification : tout rapport doit être indexé (aucun orphelin), et les pages d'orientation et de table des matières suivent une convention unique et opposable (`README.md` pour l'atterrissage, `index.md` pour l'énumération). Autrement dit, la référence de vérité ne peut pas dériver en silence de ce qu'elle décrit : la doc s'impose à elle-même le standard qu'elle impose au système.

C'est ce qui distingue Arsenal d'une configuration soignée : la rigueur n'y dépend pas de la discipline d'un humain un soir donné. Elle est **exécutée**.

---

## Entrer dans la documentation

La documentation est la référence de vérité du système. Points d'entrée :

- [`00_documentation_arsenal/README.md`](00_documentation_arsenal/README.md) — accueil et autorité du corpus.
- [`navigation/carte_domaines.md`](00_documentation_arsenal/navigation/carte_domaines.md) — la carte des domaines et ses hubs.
- [`contrats/index.md`](00_documentation_arsenal/contrats/index.md) — l'index des contrats fonctionnels.
- [`architecture/index.md`](00_documentation_arsenal/architecture/index.md) — couches, topologie, doctrines.
- [`audits/index.md`](00_documentation_arsenal/audits/index.md) — le cycle d'audit, des rapports aux clôtures.
- [`changelog/index.md`](00_documentation_arsenal/changelog/index.md) — l'historique versionné (canon).

---

## Ce qu'Arsenal n'est pas

**Pas une installation à copier.** Les entités, IPs, topics MQTT et noms de devices sont spécifiques. Ce qui est réutilisable, ce sont les patterns, les invariants et la doctrine.

**Pas une vitrine.** Arsenal n'est pas optimisé pour le screenshot. Il est optimisé pour rester maintenable et gouvernable des années après sa construction.

**Pas une documentation Home Assistant.** La doc officielle reste la référence pour les intégrations et Lovelace. Arsenal porte sur l'architecture du système : séparation décision/exécution, contractualisation, robustesse runtime et gouvernance.

---

## Licence

MIT — les patterns sont libres de réutilisation.

Arsenal est publié pour partager une façon d'architecturer Home Assistant, pas une maison. Le but n'est pas d'être reproduit. Le but est d'être étudié.
