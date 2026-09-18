# Clôture de chantier — C33 Dé-identification de la surface exposée (adultes)

> **Statut :** clôture de **chantier** — C33 **CLOS**
> **Domaine :** TRANSVERSE — Présence ↔ Sécurité/Alarme ↔ Notifications mobiles ↔ BSSID/Wi-Fi ↔ UI Lovelace ↔ Doctrine de nommage ↔ Publication/confidentialité
> **Destination d'archivage :** `00_documentation_arsenal/audits/05_clotures/transverses/cloture_c33_desidentification_surface_exposee.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/04_chantiers/transverses/chantier_desidentification_surface_exposee.md` (source faisant foi, §10-§11)
> - `00_documentation_arsenal/contrats/presence.md` (§ Symétrie des contributeurs parent_1 / parent_2)
> - `scripts/arsenal_contracts/check_presence_contracts.py` (test R4)
> - `00_documentation_arsenal/audits/04_chantiers/transverses/chantier_restructuration_chambres_enfants.md` (C32, chantier amont)
> **État du dépôt à la rédaction :** `origin/main` = `f5aff4d`. Lots 0-5 mergés 2026-07-20 (#461-#466) ; Lot 6 (solde du critère 4) et Lot 7 (clôture) portés par cette même PR.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime ; une décision propriétaire ne se déduit jamais par supposition.*

---

## 1. Objet

Acter la clôture du chantier **C33** : retrait des prénoms adultes (`antoine`, `valentin`,
`constance`) de la surface exposée du dépôt public (runtime, libellés UI, contrats actifs),
canon `parent_1`/`parent_2`, extension du verrou CI **S7** aux adultes, et solde du dernier
critère de clôture resté ouvert depuis le 2026-07-20.

---

## 2. Constat traité (rappel)

Le dépôt Arsenal est public depuis le 2026-05-23 (fork tiers `kloggy` du 2026-06-08, star
`aruesberg`). Sa surface exposée désignait nominativement les adultes du foyer
(`person.valentin` = Antoine, `person.constance`), notamment dans une chaîne **sensible**
(présence → décision d'alarme) et dans le canal de notifications mobiles. Décisions
propriétaire D1-D4 : dépôt maintenu public, résidu historique Git assumé et non traité,
canon `parent_1`/`parent_2`, identité Git de l'auteur maintenue (détail : chantier source §2).

---

## 3. Correctifs appliqués

| Lot | Objet | Réf. |
|-----|-------|------|
| **L1** | Canon des personnes `parent_1`/`parent_2` inscrit à `nommage_entites.md` | #461 |
| **L2** | Renommage runtime — 15 fichiers, `person.*`/`input_text.telephone_*`/`sensor.*_bssid_dynamic`/`binary_sensor.approche_securite_*` | #461 |
| **L2b** | Correctif urgent — 50 fichiers consommateurs manqués par L2 (notifications mobiles coupées) | #462 |
| **L2c** | Solde documentaire des dettes de L2b (critères de clôture 2 et 5 réécrits) | #463 |
| **L3a** | Réparation de 25 références mortes en documentation active | #464 |
| **L3c** | Solde des 7 annotations transitoires « ex-… » héritées de C32 | #465 |
| **L4** | Verrou S7 étendu aux adultes (`CRITICAL` runtime / `WARNING` doc active), frontière sujets/auteur (D4) | #466 |
| **L5** | Migration instance — `entity_id` renommés au registre HA, historique préservé | instance, 2026-07-20 |
| **L6** | Validation terrain (R1, R4) + solde du critère 4 par preuve de repli (symétrie de code) | terrain 2026-07-20 + cette PR |
| **L7** | Clôture | cette PR |

**Lot 6 (complément, 2026-09-18)** : le critère de clôture 4 exigeait une preuve terrain sur
les **deux** contributeurs (`parent_1`, `parent_2`) ; seul `parent_1` avait déclenché une
transition naturelle observable, `parent_2` restant non observable à court terme. Examen de
code (lecture seule) : `binary_sensor.presence_famille_securite`
(`12_template_sensors/presence/securite/presence.yaml`) traite les deux contributeurs par une
construction **strictement identique** (même `is_state(..., 'Maison securite')`, même boucle
sur les deux trackers GPS). **Arbitrage propriétaire** : le critère est requalifié — preuve
terrain sur un contributeur + preuve statique de symétrie de code **ancrée en CI** vaut
satisfaction. Contrat `presence.md` amendé (nouvelle section normative) ; test **R4** ajouté à
`check_presence_contracts.py` (4 assertions, `--selftest` étendu, mutation négative vérifiée).
Aucun runtime HA, aucune UI, aucun dashboard modifié par ce lot — uniquement le contrat
(Markdown) et le checker (Python CI).

---

## 4. Validation terrain réalisée

| Critère (§10 source) | Nature de la preuve | Résultat |
|---|---|---|
| 1 — `audit_publication_git.py` : 0 `CRITICAL`, 0 `WARNING` S7 | terrain (CI) | ✅ (Lot 3c, 2026-07-20) |
| 2 — recherche sans frontière de mot, liste positive d'exclusions | terrain (recherche exhaustive) | ✅ (Lot 2c/L2b, 2026-07-20) |
| 3 — 0 entité live portant un prénom hors périmètre D3/D4 | terrain (audit fonctionnel post-migration) | ✅ (2026-07-20, 17:05-17:25) |
| 4 — agrégat de sécurité éprouvé sur les deux contributeurs | terrain (`parent_1`, 19:03:12 le 2026-07-20) **+ preuve statique de symétrie de code ancrée CI** (`parent_2`) | ✅ **preuve de repli** (2026-09-18, voir §3) |
| 5 — notification reçue sur `parent_1` | terrain (réception confirmée par le propriétaire) | ✅ (Lot 6, 2026-07-20) |

Les critères 1, 2, 3 et 5 reposent sur une preuve terrain directe, acquise le 2026-07-20. Le
critère 4 est le seul à reposer, pour son second contributeur, sur une preuve de repli
(symétrie de code ancrée en CI) plutôt que sur une occurrence terrain observée — décision
explicite du propriétaire, motivée §3, non un contournement silencieux.

---

## 5. Résidus documentés (non bloquants)

- **R1 — Preuve directe préférable si elle survient.** Si `parent_2` déclenche un jour une
  transition naturelle isolée de la chaîne présence → sécurité, elle constituerait une preuve
  directe strictement supérieure à la preuve de repli retenue ici. **Aucune obligation de la
  provoquer** — la clôture ne dépend pas de cette occurrence.
- **R2 — Résidu historique Git assumé (D1).** Les prénoms figurent encore dans l'historique
  Git gelé (changelog, audits) et dans le fork tiers du 2026-06-08 — hors périmètre par
  décision propriétaire, non traité ici, non traitable sans réécriture d'historique jugée trop
  coûteuse (voir chantier source §2, D1).
- **R3 — Hors périmètre par D4.** `nas_valentin*` (39 entités, hostname Synology) et
  `linky_antoine*` (1, intégration) portent le nom de l'**auteur**, assumé par D4 — n'entrent
  pas dans le périmètre de dé-identification des sujets.

---

## 6. Qualification finale des critères de clôture

**Les 5 critères du §10 de la source sont satisfaits.** Le critère 4, seul resté ouvert depuis
le 2026-07-20, est satisfait par une preuve de repli explicitement arbitrée par le propriétaire
(symétrie de code démontrée + ancrage CI), et non par l'occurrence terrain initialement exigée
— requalification tracée au chantier source (§10, encart de correction) sur le même précédent
que la correction du critère 5 (2026-07-20).

---

## 7. Statut de C33 et impact domaine

**C33 CLOS.** Les trois couches du chantier (canon, renommage, verrou) sont livrées et
validées ; le dernier résidu (critère 4) est soldé par arbitrage propriétaire documenté.

**Articulation avec C32** : C33 soldait ce que C32 (restructuration des chambres enfants)
laissait ouvert côté confidentialité adultes — cette dette est désormais éteinte. Aucun impact
sur le statut propre de C32.

**Aucune régression attendue** : `check_presence_contracts.py` reste vert (8/8 tests, dont le
nouveau R4) ; `audit_publication_git.py` (S7) inchangé dans son comportement, aucune règle
existante affaiblie.

---

## 8. Verdict

**C33 clos (2026-09-18)** — dé-identification des adultes complète et vérifiée, verrou S7
étendu et durci, dernier critère de clôture satisfait par une preuve de repli explicitement
arbitrée par le propriétaire plutôt que par occurrence terrain forcée (`aucune panne
fabriquée`). Résidus documentés (§5) non bloquants, hors périmètre par décision propriétaire
antérieure (D1, D4).

---

*Clôture de chantier C33. Établie en lecture du dépôt (`origin/main` = `f5aff4d`) et de
l'arbitrage propriétaire rendu en session (2026-09-18) sur le critère 4. Acte à la fois
documentaire (contrat, chantier, registre) et CI (nouveau test R4, aucune régression) —
aucun runtime HA, aucune UI, aucun dashboard modifié.*
