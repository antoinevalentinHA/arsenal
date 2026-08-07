# 🧠 ARSENAL — Topologie NAS & Sauvegardes (maison / imprimerie / HA)

> Document **maître** (maison). Vue complète des 3 machines, des flux de
> sauvegarde/synchronisation, et de la cible de rationalisation.
> Relevé le **2026-08-07** par exploration directe des DSM (lecture seule).
>
> Principe de documentation : *ce qui touche à la maison est documenté à la
> maison ; ce qui touche à l'imprimerie est documenté à l'imprimerie.* Ce
> document-ci est la **vue complète** conservée à la maison.

---

## 1. Machines

| Rôle | Machine | Adresse | Notes |
|------|---------|---------|-------|
| 🏠 Maison | Synology **NAS_VALENTIN** (DS224+) | `192.168.1.118` | 2 Go RAM, DSM 7.3.2, volume ~3,5 To. **Serveur VPN** (tun0 `10.9.0.0/24`, `10.9.0.1`). QuickConnect actif. |
| 🏠 Maison | **Home Assistant** (Raspberry Pi) | `192.168.1.117:8123` | HAOS. Sauvegardes → dossier `Backups_HA` du NAS maison. |
| 🏭 Imprimerie | Synology **NAS_Baillet** | QuickConnect / `212.104.240.x` | Volume ~8,8 To (1,6 To utilisés). |
| 🏭 Imprimerie | **QNAP** | `212.104.240.242` (rsync) | Module rsync `Sauvegarde New`. |

---

## 2. État actuel des flux (2026-08-07)

```
        SYNOLOGY DRIVE SHARESYNC (bidirectionnel, CONTINU / temps réel, via QuickConnect SSL)
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  ① Maison = CLIENT de l'imprimerie  (imprimerie = serveur Drive)               │
  │      imprimerie ──▶ maison   (download-only)                                    │
  │      dossiers : Commercial · Direction · Direction_Compta · Transfert           │
  │                                                                                │
  │  ② Imprimerie (NAS_Baillet) = CLIENT de la maison  (maison = serveur Drive)    │
  │      maison ──▶ imprimerie                                                      │
  │      dossiers : Mes fichiers · Antoine · Backups_HA · homes                     │
  │                                                                                │
  │  monitoring : ⇄ BIDIRECTIONNEL  (canal d'état → MQTT → HA)  [INTOUCHABLE]       │
  └──────────────────────────────────────────────────────────────────────────────┘

  🏭 QNAP imprimerie ──rsync (module "Sauvegarde New", Lun/Mer/Ven 06:00)──▶ 🏠 /volume1/sauvegarde_qnap/
        (tâche Planificateur maison "Backup_QNAP", root, pull)
```

### Tableau récapitulatif

| # | Source → Destination | Mécanisme | Dossiers | Fréquence | Sens |
|---|----------------------|-----------|----------|-----------|------|
| ① | Imprimerie Syno → Maison | Synology Drive ShareSync | Commercial, Direction, Direction_Compta, Transfert | continu | download-only |
| ② | Maison → Imprimerie Syno | Synology Drive ShareSync | Mes fichiers, Antoine, Backups_HA, homes | continu | upload (imprimerie tire) |
| — | Maison ⇄ Imprimerie Syno | Synology Drive ShareSync | **monitoring** | continu | bidirectionnel |
| ③ | QNAP imprimerie → Maison | rsync (Backup_QNAP) | module `Sauvegarde New` → `/volume1/sauvegarde_qnap/` | Lun/Mer/Ven 06:00 | pull |

> ⚠️ **Piège de diagnostic** : côté maison, HyperBackup / Cloud Sync / Snapshot
> Replication sont **vides**. Le flux maison→imprimerie (②) ne passe PAS par eux :
> il passe par ShareSync, l'imprimerie étant **cliente** du serveur Drive maison.

### Le canal `monitoring` (à ne jamais casser)

Chaîne : le NAS imprimerie écrit son état dans le dossier `monitoring` → **ShareSync**
le réplique vers la maison → tâche planifiée **« Monitoring NAS imprimerie »**
(maison, root, **toutes les minutes**, `python3`) lit le fichier et **publie en MQTT**
→ capteurs HA (« NAS Imprimerie Connectivité », etc.). Ressources négligeables.

---

## 3. Constat

La **sauvegarde croisée maison ⇄ imprimerie existe déjà**, mais sous forme de
**synchronisation continue** (ShareSync temps réel), donc :

- pas de **point de restauration** (versionné) ;
- une **corruption/suppression/rançongiciel** se **propage immédiatement** des deux côtés.

Pour une *sauvegarde*, un **backup planifié versionné** est préférable.

---

## 4. Cible de rationalisation

| Flux | Aujourd'hui | Cible |
|------|-------------|-------|
| Imprimerie Syno → Maison (①) | ShareSync continu | **HyperBackup QUOTIDIEN (Lun–Ven), versionné** (Syno imprimerie → *Hyper Backup Vault* sur Syno maison) |
| Maison → Imprimerie Syno (②) | ShareSync continu | **HyperBackup HEBDOMADAIRE, versionné** (Syno maison → *Hyper Backup Vault* sur Syno imprimerie) |
| `monitoring` | ShareSync bidirectionnel | **inchangé** (MQTT) |
| QNAP → Maison (③) | rsync Lun/Mer/Ven | garder (ou aligner) |

Notes :
- Les deux NAS étant des **Synology**, *Hyper Backup Vault* (Syno↔Syno) est possible → sauvegarde versionnée, chiffrable, reprise sur coupure.
- Le backup **maison → imprimerie** ne doit contenir que les données **d'origine maison**
  (HA/Arsenal, Antoine, Mes fichiers, homes) — **pas** les copies imprimerie déjà collectées.
- Prévoir un **1er seed** volumineux (long via VPN/QuickConnect) et un **test de restauration**.

---

## 5. À documenter séparément (chantiers « traces » à venir)

- **VPN** : NAS maison = serveur VPN (`tun0`, `10.9.0.0/24`, `10.9.0.1`) ; QuickConnect (relais).
- **Reverse proxy** et **accès extérieur**.
- **Pipeline patrimonial HA** : voir `../schemas_ascii/pipeline_nas_ha.md`.

---

*Dernière mise à jour : 2026-08-07.*
