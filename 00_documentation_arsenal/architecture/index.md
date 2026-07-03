# 🗺️ Index — Architecture Arsenal

> **Porte d'entrée navigation.** Ce document liste et classe l'ensemble des
> fichiers du dossier `architecture/`.
> Pour le positionnement, les principes et la règle d'or : voir [README.md](./README.md).

---

## Référence générale

- [README.md](./README.md) — Objet, périmètre, positionnement dans Arsenal,
  principes architecturaux globaux, règle d'or. **Entrée compréhension.**

---

## Racine — Journalisation et observabilité système

| Fichier | Contenu |
|---|---|
| [00_system_log.md](./00_system_log.md) | Contrat normatif — system log |
| [01_logger.md](./01_logger.md) | Principes du Logger Home Assistant |
| [02_logbook.md](./02_logbook.md) | Contrat normatif — logbook |

> ⚠️ Ces trois fichiers coexistent avec `logger.md` et `logbook.md` dans
> `00_structure_includes/` — contenus distincts (architecture vs fragment YAML,
> voir §Anomalies).

---

## Racine — Infrastructure et énergie

| Fichier | Contenu |
|---|---|
| [energie.md](./energie.md) | Architecture Énergie — séparation des couches |
| [infrastructure_puissance.md](./infrastructure_puissance.md) | Infrastructure & énergie — alimentation, sécurité |

---

## Racine — Capteurs et données

| Fichier | Contenu |
|---|---|
| [capteurs_meteo.md](./capteurs_meteo.md) | Architecture capteurs météo |
| [securisation_capteurs_externes.md](./securisation_capteurs_externes.md) | Sécurisation des capteurs externes |
| [capteurs_couleur.md](./capteurs_couleur.md) | Cartographie transverse des capteurs de couleur — descriptif, non normatif (familles A→G) |

---

## Racine — Transversal

| Fichier | Contenu |
|---|---|
| [integrite_parametres.md](./integrite_parametres.md) | Intégrité des paramètres (transversal) |

---

## Racine — Écosystème / dépôts gouvernés

| Fichier | Contenu |
|---|---|
| [ecosysteme_depots_satellites.md](./ecosysteme_depots_satellites.md) | **Référence canonique** de la couche « composants gouvernés » : les 6 dépôts satellites (`bluetti-bt-lib`, `hassio-bluetti-bt`, `ha_airstage`, `ha-linky`, `rainbird-esp32-elegoo`, `boiler-bridge`), leurs patrons d'intégration, criticités et frontières de responsabilité. Descriptif, non normatif (règles métier). |

---

## Racine — Sous-systèmes domaines

| Fichier | Domaine |
|---|---|
| [aeration_recommandation.md](./aeration_recommandation.md) | Architecture aération — recommandation |
| [bouclage.md](./bouclage.md) | Architecture bouclage ECS |
| [eclairage_jardin.md](./eclairage_jardin.md) | Architecture éclairage jardin (MATIN / SOIR) |
| [maintenance_chauffage.md](./maintenance_chauffage.md) | Exploitation et maintenance — chauffage |
| [meteo_affichage.md](./meteo_affichage.md) | Architecture affichage météo |
| [meteo_interpretation_contextuelle.md](./meteo_interpretation_contextuelle.md) | Interprétation météo contextuelle (amont de la clé couleur météo) |
| [notifications_mobiles.md](./notifications_mobiles.md) | Architecture notifications mobiles |
| [ouvertures.md](./ouvertures.md) | Architecture ouvertures |
| [voiture.md](./voiture.md) | Architecture voiture (Audi A3 e-tron) |

---

## Sous-dossiers

### Infrastructure HA

| Dossier | Fichiers | Contenu |
|---|:--:|---|
| [00_structure_includes/](./00_structure_includes/) | 23 | Structure normative des includes HA — [index dédié](./00_structure_includes/index.md) |
| [01_recorder/](./01_recorder/) | 2 | Contrat Recorder + fiche de décision |
| [02_etiquettes/](./02_etiquettes/) | 4 | Système de labels (automations, capteurs, helpers, scripts) |

### Doctrines transversales

| Dossier | Fichiers | Contenu |
|---|:--:|---|
| [03_doctrines/](./03_doctrines/) | 12 | **Bibliothèque doctrinale fondamentale** : nommage, causalité, gestion du temps, séparation décision/action, git, principes généraux, IDs d'automatisations et contrat préfixe ↔ domaine (voir note) |

> Note : `03_doctrines/` contient les documents les plus structurants du
> système Arsenal — `principes_generaux.md`, `gestion_du_temps.md`, etc. y
> sont hébergés. Le README les référence via leur chemin `03_doctrines/`.

### Domaines spécifiques

| Dossier | Fichiers | Contenu |
|---|:--:|---|
| [chauffage/](./chauffage/) | 3 | Architecture chauffage : boiler bridge, observabilité auto-ajustement |
| [presence/](./presence/) | 2 | Architecture présence : chaîne présence, WiFi |

---

## Anomalies signalées (non corrigées)

1. **Nommage ambigu logger / logbook** : `01_logger.md` et `02_logbook.md`
   (racine `architecture/`) coexistent avec `logger.md` et `logbook.md`
   (dans `00_structure_includes/`). Mêmes noms de base, contenus distincts :
   les fichiers racine sont des **docs d'architecture**, les fichiers dans
   `00_structure_includes/` sont des **fragments YAML de configuration**.
