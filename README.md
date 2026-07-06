# Arsenal

[![License: MIT](https://img.shields.io/github/license/antoinevalentinHA/arsenal?color=blue)](./LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home_Assistant-system-41BDF5?logo=home-assistant&logoColor=white)](https://www.home-assistant.io/)

> Une maison réelle, pilotée par Home Assistant — et tenue aux standards d'un logiciel sérieux.

Arsenal est une configuration Home Assistant **réelle, utilisée en production dans une maison familiale**. Elle couvre le chauffage, l'eau chaude, la climatisation, l'aération, l'arrosage, l'énergie, la sécurité, la présence, les mesures intérieures et extérieures, les dashboards et l'observabilité d'infrastructure.

Ce n'est ni un framework, ni une configuration à copier telle quelle. C'est un système complet, observable fichier par fichier — et gouverné comme un logiciel.

---

## Ce qu'Arsenal fait concrètement

Quelques comportements réels du système, tels qu'ils tournent aujourd'hui :

- **Le chauffage est piloté par une décision centrale unique** : un script souverain évalue présence, météo, apport du poêle et fenêtres ouvertes, puis produit des états lisibles (`binary_sensor.chauffage_autorise_systeme`, `meteo_favorable_chauffage`, `poele_en_fonction`…) que des exécutants bornés appliquent.
- **L'aération bloque le chauffage via une machine d'état explicite** : chaque épisode d'aération suit un cycle de vie normé, avec timers monotones et anti-triggers fantômes — la reprise thermique restant du ressort exclusif de la décision chauffage.
- **L'eau chaude sanitaire est supervisée par un watchdog**, avec un sous-domaine bouclage (recirculation) audité et clôturé, et une désinfection au retour de vacances.
- **Les commandes physiques critiques sont transactionnelles** : la chaudière est pilotée via un pont Raspberry Pi ([`boiler_pi`](00_documentation_arsenal/outils_externes/boiler_pi/)) avec acquittement MQTT, retry et garde — on ne suppose jamais qu'une commande a été exécutée.
- **Une alimentation tampon locale (Bluetti AC180)** assure la continuité électrique de la chaîne thermique en cas de panne secteur, et les pannes internet / secteur sont des domaines à part entière, avec remédiation et signalisation.
- **L'arrosage coexiste avec un contrôleur Rain Bird** via un pont ESP32 : besoin sol → intention → exécution supervisée, en V1 automatique mono-station.
- **Les températures et humidités intérieures traversent un pipeline de mesure** — capteurs bruts → consolidation → stabilisation — avant toute décision : la mesure est un domaine en soi, séparé de la décision.

Chacun de ces comportements est adossé à un contrat écrit, visible dans le dépôt.

---

## Domaines couverts

La cartographie des domaines est tenue dans [`navigation/carte_domaines.md`](00_documentation_arsenal/navigation/carte_domaines.md), et chaque domaine **Tier 1** dispose d'un hub de navigation dans [`navigation/domaines/`](00_documentation_arsenal/navigation/domaines/). Les 22 hubs actuels, regroupés ici en familles de lecture :

> ⚠️ Ces familles sont un **confort de lecture pour ce README**, pas la taxonomie canonique interne — celle-ci vit dans la carte des domaines.

| Famille de lecture | Domaines (slugs canoniques) |
|---|---|
| Confort thermique & air | [`chauffage`](00_documentation_arsenal/navigation/domaines/chauffage.md) · [`climatisation`](00_documentation_arsenal/navigation/domaines/climatisation.md) · [`aeration_blocage_chauffage`](00_documentation_arsenal/navigation/domaines/aeration_blocage_chauffage.md) · [`deshumidificateur`](00_documentation_arsenal/navigation/domaines/deshumidificateur.md) |
| Eau chaude & chaîne chaudière | [`ecs`](00_documentation_arsenal/navigation/domaines/ecs.md) · [`boiler`](00_documentation_arsenal/navigation/domaines/boiler.md) · [`energie_chaudiere`](00_documentation_arsenal/navigation/domaines/energie_chaudiere.md) |
| Mesure intérieure | [`temperature_interieure`](00_documentation_arsenal/navigation/domaines/temperature_interieure.md) · [`humidite_relative_interieure`](00_documentation_arsenal/navigation/domaines/humidite_relative_interieure.md) |
| Énergie & résilience | [`energie`](00_documentation_arsenal/navigation/domaines/energie.md) · [`pannes`](00_documentation_arsenal/navigation/domaines/pannes.md) |
| Sécurité & présence | [`alarme`](00_documentation_arsenal/navigation/domaines/alarme.md) · [`presence`](00_documentation_arsenal/navigation/domaines/presence.md) · [`ouvertures`](00_documentation_arsenal/navigation/domaines/ouvertures.md) |
| Extérieur & jardin | [`meteo`](00_documentation_arsenal/navigation/domaines/meteo.md) · [`arrosage`](00_documentation_arsenal/navigation/domaines/arrosage.md) |
| Modes de vie & maison | [`eclairage`](00_documentation_arsenal/navigation/domaines/eclairage.md) · [`vacances`](00_documentation_arsenal/navigation/domaines/vacances.md) |
| Suivi spécialisé | [`sante`](00_documentation_arsenal/navigation/domaines/sante.md) · [`voiture`](00_documentation_arsenal/navigation/domaines/voiture.md) · [`imprimerie`](00_documentation_arsenal/navigation/domaines/imprimerie.md) |
| Interface | [`ui_lovelace`](00_documentation_arsenal/navigation/domaines/ui_lovelace.md) |

Trois précisions d'honnêteté :

- **La maturité n'est pas uniforme.** Certains domaines ont une chaîne d'audit complète et clôturée (chauffage, bouclage ECS), d'autres sont contractualisés mais non audités — c'est un état de cycle assumé, documenté dans la carte, pas un défaut caché.
- **La carte ne s'arrête pas au Tier 1.** Des domaines feuilles (Tier 2) existent en mono-contrat — `vmc`, `visite`, [`volets_pluie`](00_documentation_arsenal/contrats/volets_pluie.md)… — sans hub dédié.
- **Certains contrats sont transverses, pas métier** : la supervision NAS ([`arsenal_nas`](00_documentation_arsenal/contrats/arsenal_nas.md)) est une frontière externe outillée, volontairement hors hub.

---

## Dashboards & observabilité

Les dashboards vivent dans [`18_lovelace/dashboards/`](18_lovelace/dashboards/), organisés par domaine. Le motif récurrent est un triplet par domaine — visible par exemple sur le chauffage ([`principal.yaml`](18_lovelace/dashboards/chauffage/principal.yaml) · [`diagnostic.yaml`](18_lovelace/dashboards/chauffage/diagnostic.yaml) · [`reglages.yaml`](18_lovelace/dashboards/chauffage/reglages.yaml)) :

- **principal** — l'état du domaine, pour vivre avec ;
- **diagnostic** — la chaîne interne, pour comprendre ;
- **réglages** — les paramètres exposés, pour ajuster sans toucher au YAML.

Règle d'or : **le backend décide, l'UI observe**. Aucune logique métier dans les dashboards — les cartes affichent des états, elles ne les calculent pas.

Côté historisation, le [`recorder.yaml`](recorder.yaml) fonctionne en **allowlist** : chaque entité enregistrée est là par décision documentée (rôle, utilité, cardinalité, fréquence), pas par défaut.

---

## Ce que vous pouvez emporter

Arsenal n'est pas copiable tel quel, mais plusieurs patterns se picorent indépendamment du reste :

- **Séparation décision / action bornée** — une autorité décisionnelle unique par domaine produit des états lisibles ; des exécutants bornés les appliquent. Doctrine dans [`architecture/index.md`](00_documentation_arsenal/architecture/index.md), démonstration dans [`contrats/chauffage/`](00_documentation_arsenal/contrats/chauffage/README.md).
- **Commandes physiques fiabilisées par ACK transactionnel** — acquittement, retry, garde : [`contrats/boiler/`](00_documentation_arsenal/contrats/boiler/README.md) et [`contrats/switchbot_transactionnel.md`](00_documentation_arsenal/contrats/switchbot_transactionnel.md).
- **Machine d'état explicite** plutôt qu'un enchevêtrement d'automatisations : [`contrats/aeration_blocage_chauffage/`](00_documentation_arsenal/contrats/aeration_blocage_chauffage/).
- **Triplet de dashboards principal / diagnostic / réglages** par domaine : [`18_lovelace/dashboards/chauffage/`](18_lovelace/dashboards/chauffage/).
- **Recorder en allowlist documentée**, entité par entité : [`recorder.yaml`](recorder.yaml).
- **Résilience secteur / internet / cloud** comme domaines contractualisés : [`contrats/pannes/`](00_documentation_arsenal/contrats/pannes/) et [`contrats/resilience_integrations.md`](00_documentation_arsenal/contrats/resilience_integrations.md).
- **Pont NAS → MQTT → Home Assistant** comme outil transverse de frontière externe : [`outils_externes/nas_arsenal/`](00_documentation_arsenal/outils_externes/nas_arsenal/) et son contrat [`arsenal_nas.md`](00_documentation_arsenal/contrats/arsenal_nas.md).
- **Changelogs comme mémoire de décision** — pas un journal de commits, une lecture « signal net » de ce qui a vraiment changé : [`changelog/index.md`](00_documentation_arsenal/changelog/index.md).

Certains patterns ont même été extraits en dépôts publics autonomes, réutilisables sans rien connaître d'Arsenal :

- [`ha-self-parametrized-template-sensors`](https://github.com/antoinevalentinHA/ha-self-parametrized-template-sensors) — template sensors auto-paramétrés par `this.entity_id` : écrire la logique une fois, la réutiliser sur de nombreuses entités sans duplication.
- [`ha-state-archive`](https://github.com/antoinevalentinHA/ha-state-archive) — pipeline d'archivage, d'audit et de versionnement d'états Home Assistant, côté infrastructure.
- [`ha-archive-search`](https://github.com/antoinevalentinHA/ha-archive-search) — moteur de recherche sur les versions archivées, côté infrastructure.

Ce sont des extractions ponctuelles, pas un framework : Arsenal reste un système, pas une bibliothèque.

---

## L'architecture, en une minute

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

Trois principes non négociables structurent le tout :

**Le backend décide. L'UI observe. Jamais l'inverse.**
**Contrat avant YAML.** Chaque domaine a un contrat écrit *avant* d'avoir du code — si l'implémentation contredit le contrat, c'est l'implémentation qui est fausse.
**L'exposition est une décision, pas un accident.** Ce qui sort vers l'extérieur (API, MQTT, notifications) est explicitement gouverné.

---

## Pourquoi c'est gouverné

[![Arsenal Validation](https://github.com/antoinevalentinHA/arsenal/actions/workflows/validation.yml/badge.svg)](https://github.com/antoinevalentinHA/arsenal/actions/workflows/validation.yml)
[![Arsenal Doctrine](https://github.com/antoinevalentinHA/arsenal/actions/workflows/doctrine.yml/badge.svg)](https://github.com/antoinevalentinHA/arsenal/actions/workflows/doctrine.yml)
[![Arsenal Docs](https://github.com/antoinevalentinHA/arsenal/actions/workflows/docs.yml/badge.svg)](https://github.com/antoinevalentinHA/arsenal/actions/workflows/docs.yml)

Home Assistant est puissant, et c'est précisément ce qui le rend facile à laisser dériver : automatisations qui en déclenchent d'autres, logique éparpillée entre UI, scripts et helpers, entités dont plus personne ne sait si elles servent. La dette s'accumule, invisible, jusqu'à la rupture. Arsenal répond à une seule question : **comment construire une installation HA qui reste maintenable, observable et cohérente sur plusieurs années ?**

La réponse tient dans une chaîne, la même pour chaque domaine : **contrat → implémentation → vérification CI → audit → clôture.**

Les contrats ne sont pas des commentaires : ce sont des documents de référence confrontés au code. Une quinzaine de domaines sont contractualisés sur plusieurs centaines de fichiers de contrat, adossés à une bibliothèque de doctrines (nommage, séparation décision/action, gestion du temps, causalité métier). Et cette discipline est **exécutée par la machine** : une intégration continue confronte les implémentations à leurs contrats, domaine par domaine.

La CI est une borne, pas un oracle : **CI rouge = interdit. CI verte = admissible à jugement humain.**

### La preuve sur un domaine : le chauffage

L'argument le plus solide n'est pas une promesse d'architecture : c'est une chaîne qu'on peut suivre sur des fichiers réels.

Le **contrat** ([`contrats/chauffage/`](00_documentation_arsenal/contrats/chauffage/README.md)) dit ce que le domaine doit faire ; la décision est centralisée dans un script souverain qui ne produit que des états *lisibles*. À chaque `push`, le workflow [`arsenal-ci-chauffage.yml`](.github/workflows/arsenal-ci-chauffage.yml) confronte l'implémentation au contrat : un self-test garde les analyseurs (on ne juge pas avec un juge défectueux), puis des étages *lint*, *décision* (`R-COV-1` / `R-MIRROR-1`) et *exécution* (`R-CALL-1`) rendent le verdict, contre un registre d'entités souverain — le domaine étant dans une transition documentée *warn-only → bloquant* (`ARSENAL_CI_ENFORCE`). Et l'audit est tracé jusqu'à sa [clôture](00_documentation_arsenal/audits/05_clotures/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md), où chaque constat est résorbé ou explicitement assumé.

Le héros de cette section n'est pas le chauffage : c'est la chaîne **contrat → CI → audit → clôture**. Le chauffage la rend simplement vérifiable — par vous, dans les fichiers liés.

### La documentation aussi

Le cycle d'audit n'est pas informel : rapports, contre-expertises, arbitrages, plans d'action, chantiers et clôtures sont des documents datés et traçables. Et la documentation est soumise au même régime : le corpus est tenu par ses propres gates, vérifiées en CI à chaque modification — tout rapport doit être indexé (aucun orphelin), et les pages d'orientation suivent une convention unique et opposable. La référence de vérité ne peut pas dériver en silence de ce qu'elle décrit.

C'est ce qui distingue Arsenal d'une configuration soignée : la rigueur n'y dépend pas de la discipline d'un humain un soir donné. Elle est **exécutée**.

---

## Maintenu avec assistance IA

Arsenal n'est pas un projet « codé par IA ». C'est un projet **gouverné par un humain non-développeur**, qui utilise l'IA comme force d'exécution sous contraintes strictes.

Concrètement, le cadre de travail impose :

- **aucun ID inventé** : les entités manipulées existent dans le registre, ou la modification est refusée ;
- **pas de renommage d'entités à la légère** : un renommage est une décision d'architecture, pas une retouche cosmétique ;
- **pas de snippets partiels hors contexte** : on travaille sur des fichiers entiers, dans leur arborescence réelle ;
- **les contrats bornent les dérives** : une proposition qui contredit un contrat est fausse par définition, aussi élégante soit-elle ;
- **la CI ne remplace pas le jugement** : elle interdit le rouge, elle n'absout pas le vert ;
- **l'humain tranche** — toujours.

L'IA accélère l'exécution. Les contrats, la CI et le cycle d'audit existent précisément pour que cette accélération ne se paie pas en dérive silencieuse.

---

## Ce qu'Arsenal n'est pas

**Pas une installation à copier.** Les entités, IPs, topics MQTT, devices et choix métier sont spécifiques à une maison précise. Ce qui est réutilisable, ce sont les patterns, les invariants et la méthode.

**Pas une vitrine.** Arsenal n'est pas optimisé pour le screenshot. Il est optimisé pour rester maintenable et gouvernable des années après sa construction.

**Pas une documentation Home Assistant.** La doc officielle reste la référence pour les intégrations et Lovelace. Arsenal porte sur l'architecture du système : séparation décision/exécution, contractualisation, robustesse runtime et gouvernance.

**Pas un système uniformément abouti.** Des domaines sont clôturés, d'autres en cours de cycle, certains non audités — et c'est écrit noir sur blanc dans la carte des domaines et le registre des chantiers.

---

## Documentation & navigation

La documentation est la référence de vérité du système. Points d'entrée :

- [`00_documentation_arsenal/README.md`](00_documentation_arsenal/README.md) — accueil et autorité du corpus.
- [`navigation/carte_domaines.md`](00_documentation_arsenal/navigation/carte_domaines.md) — la carte des domaines et ses hubs.
- [`contrats/index.md`](00_documentation_arsenal/contrats/index.md) — l'index des contrats fonctionnels.
- [`architecture/index.md`](00_documentation_arsenal/architecture/index.md) — couches, topologie, doctrines.
- [`audits/index.md`](00_documentation_arsenal/audits/index.md) — le cycle d'audit, des rapports aux clôtures.
- [`audits/REGISTRE_CHANTIERS.md`](00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md) — le **cockpit de pilotage** : ce qui est réellement ouvert aujourd'hui.
- [`changelog/index.md`](00_documentation_arsenal/changelog/index.md) — l'historique versionné (canon).

---

## Discussion

Présentation et échanges d'architecture sur le forum Home Assistant : [Arsenal — a contract-driven architecture for Home Assistant](https://community.home-assistant.io/t/arsenal-a-contract-driven-architecture-for-home-assistant/1011597).

---

## Licence

MIT — les patterns sont libres de réutilisation.

Arsenal est publié pour partager une façon d'architecturer Home Assistant, pas une maison. Le but n'est pas d'être reproduit. Le but est d'être étudié.
