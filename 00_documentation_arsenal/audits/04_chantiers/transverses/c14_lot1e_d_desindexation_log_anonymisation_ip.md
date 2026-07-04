# C14 — Lot 1E-d : traitement des 2 vrais signaux résiduels (log versionné + IP arrosage)

- **Type :** lot d'**implémentation** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md), suite de la préparation du scanner [Lot 1E-c](c14_lot1e_c_preparation_scanner_publication.md)
- **Statut :** exécuté — en attente de revue
- **Base :** `main` @ `3832a19` (post-#272)
- **Périmètre modifié :** `.gitignore` (règle `*.log`), désindexation Git de `zigbee2mqtt/migration-4-to-5.log`, contrat métier `contrats/arrosage/08_inventaire_pont_runtime.md` (anonymisation IP), + ce rapport + index + registre
- **Non fait ici :** scanner **non branché en CI** (Lot 1E-b) ; historique git **non assaini** ; aucun runtime YAML / ID / entité touché

---

## 1. Objet

Solder les **2 `CRITICAL` résiduels** de la baseline honnête laissée par le Lot 1E-c (cf. son §6), qui étaient les deux seuls vrais signaux bloquant un branchement CI honnête du scanner :

1. `zigbee2mqtt/migration-4-to-5.log` — un `.log` **versionné** (violation de frontière git + contrôle S5a) ;
2. `contrats/arrosage/08_inventaire_pont_runtime.md:42` — une **IP privée réelle** (réservation DHCP) dans un contrat métier destiné à publication.

Décision propriétaire (2026-07-04) : **anonymisation** de l'IP (pas de requalification `audit:scope=doc`) ; **désindexation** du log avec conservation du fichier local.

## 2. Actions exécutées

| # | Signal | Contrôle | Action | Effet |
|---|--------|----------|--------|-------|
| 1 | `.log` versionné | S5 | `.gitignore` : ajout de la règle générale `*.log` (les règles existantes `home-assistant.log*`, `zigbee2mqtt/log/`, `*.log.*` ne couvraient pas ce fichier) | tout `.log` futur ignoré par défaut |
| 2 | `.log` versionné | S5 | `git rm --cached zigbee2mqtt/migration-4-to-5.log` (fichier local **conservé**) | artefact de migration z2m one-shot retiré du suivi Git |
| 3 | IP privée arrosage | S2 | Contrat `08_inventaire_pont_runtime.md` ligne 42 : IP réelle **remplacée** par une formulation abstraite (« Réservation DHCP locale stable, hors référentiel Git ») ; ancienne réservation C3 caduque conservée **sans IP** | information contractuelle utile préservée (le pont Rain Bird dispose d'une adresse stable), aucune IP/hostname/secret inventé |

Le contenu contractuel utile est intact : le pont Rain Bird doit disposer d'une **adresse réseau locale stable** ; seule la valeur numérique privée (récupérable via HA / l'historique git) disparaît du référentiel publiable.

## 3. Vérification

- **Scanner `audit_publication_git.py`** sur corpus réel : `CRITICAL 2 → 0`. Les deux findings S2 (arrosage) et S5 (log z2m) ont disparu ; aucun nouveau finding introduit.
- **`--fail-on critical`** → **exit 0** (le scanner deviendrait vert en mode bloquant).
- **`--selftest`** → **selftest OK** (aucune détection affaiblie : la garde S1 littéral-en-code et les positifs restent inchangés).
- Aucune IP, hostname ni secret n'est reproduit dans ce rapport (référence par fichier + contrôle uniquement, comme au Lot 1E-c).

**`CRITICAL=0` est désormais atteint honnêtement** — aucun signal masqué : l'un est corrigé à la racine (désindexation), l'autre est réellement anonymisé dans le référentiel.

## 4. Non-actions

- **Scanner non branché en CI** → Lot **1E-b** (d'abord informatif `continue-on-error`, puis bloquant `--fail-on critical` — désormais possible puisque `CRITICAL=0`).
- **Historique git non assaini** (l'IP et le `.log` restent dans les commits passés) → lot terrain dédié, hors périmètre.
- Aucun runtime YAML, aucun ID, aucun alias, aucune entité, aucun chemin touché hors nécessité stricte.
- Fichier local `zigbee2mqtt/migration-4-to-5.log` **non supprimé** du disque.

## 5. Suite

Le dernier verrou avant branchement est levé. **Prochain lot : 1E-b** — brancher le scanner en CI (informatif, puis bloquant une fois la non-régression verrouillée).
