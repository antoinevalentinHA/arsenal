# Chantier VOITURE — Migration `audiconnect` vers l'authentification device-code (RFC 8628)

| Champ | Valeur |
|---|---|
| **Chantier** | Migration de l'intégration HACS **`audiconnect`** vers l'authentification **Device Authorization Grant (RFC 8628)** suite à la coupure CARIAD / Play Integrity. |
| **Domaine** | Voiture — Audi A3 e-tron — couche d'ingestion cloud (`custom_components/audiconnect`). |
| **Statut** | **Ouvert — correctif vendorisé en production, en attente du merge upstream.** Le device-code tourne en local (voiture fonctionnelle). Deux PR ouvertes sur le dépôt officiel : **#777** (correctif de fond) et **#778** (traductions FR). Aucune release upstream ne contient encore le device-code. |
| **Priorité** | **P1 pendant la panne (résolue localement) → P3 en suivi** : la voiture fonctionne ; le reste est de la gouvernance de mise à jour. |
| **Dépôt officiel** | `audiconnect/audi_connect_ha` (cf. `manifest.json` : `documentation`, `issue_tracker`). |
| **Issue amont** | [`audiconnect/audi_connect_ha#772`](https://github.com/audiconnect/audi_connect_ha/issues/772) — changement backend CARIAD (attestation Play Integrity) début juillet 2026. |
| **PR de fond** | [`#777`](https://github.com/audiconnect/audi_connect_ha/pull/777) — `feat!: device-code login` (auteur `jonny190`, branche `jonny190:feat/device-code-auth`, base `master`). **Ouverte.** |
| **PR traductions FR** | [`#778`](https://github.com/audiconnect/audi_connect_ha/pull/778) — `fix(i18n)` device-code FR (auteur `antoinevalentinHA`, dépend de #777, à merger **après**). **Ouverte.** |
| **Contribution en revue** | Scope `mbb` manquant identifié en revue de #777 (débloque trip / climater / charger) — **déjà intégré dans la branche #777**. |
| **État vendorisé** | Commits arsenal `881b0cd` (sync device-code) puis `e45ab4e` (ajout scope `mbb` + `fr.json`). `manifest.json` **inchangé à `2.2.0`**. |

> **Nature de ce document.** Runbook de **gouvernance de mise à jour**. Il décrit la stratégie pour maintenir la copie vendorisée alignée sur l'amont **sans régression**, et la procédure de bascule propre vers HACS **après** merge. Il **ne modifie aucun runtime** et **ne fige aucune correction de code** ; le code correctif vit déjà dans `custom_components/audiconnect/`.

---

## 1. Contexte — ce qui s'est passé

**Cause de la panne.** Début juillet 2026, CARIAD (backend d'authentification Audi/VW) a activé une attestation *Play Integrity* sur l'échange de token IDK. L'ancien flux **authorization-code** (scraping de la page login + mot de passe) est devenu inexploitable : le endpoint token renvoie une erreur au lieu d'un token, ce qui remonte en aval en `KeyError('access_token')`. Cela affecte à l'identique les versions stock **v2.1.4 et v2.2.0** ; il n'existe **aucun correctif côté client** pour l'ancien flux.

**Le correctif.** Bascule vers le **Device Authorization Grant OAuth (RFC 8628)** : l'utilisateur approuve un `user_code` dans un navigateur (`verification_uri_complete`), sans mot de passe. Ce flux **ne requiert pas** l'attestation Play Integrity. C'est un changement **structurel** (`config_flow.py`, `audi_services.py`, `audi_account.py`, `__init__.py`, `coordinator.py`, `strings.json`, traductions) — d'où l'ampleur du commit `881b0cd`. C'est un changement **cassant** (`feat!` amont) : une entrée de configuration existante login/mot de passe doit être **re-authentifiée** en device-code (déjà fait en local lors du déploiement).

**Historique de la tentative avortée (pour mémoire).** Un premier essai (`#357` arsenal) retirait l'en-tête `X-QMAuth` de l'échange IDK ; une capture live a prouvé l'inefficacité (`400 invalid assertion headers` persistant), d'où le revert `#358` restaurant la v2.2.0 stock avant l'adoption du device-code. Le device-code est la **seule** voie viable.

---

## 2. État actuel — pourquoi il n'y a rien d'urgent à faire

- La copie vendorisée dans `custom_components/audiconnect/` **fonctionne** : la voiture est ingérée normalement (auth, trip, climater, charger).
- Cette copie est **committée** dans arsenal (le dépôt reflète le runtime, conformément au principe « le dépôt est la vérité »).
- **Convergence vérifiée** : la copie locale ≈ **branche #777 + traductions #778**. Le fix de scope `DEVICE_CODE_SCOPE = "openid mbb profile badge cars dealers vin"` est **identique** à la branche #777 (commentaire compris). La future release officielle sera donc un **sur-ensemble** de ce qui tourne en local → risque de casse **faible** à la bascule, **sous réserve de la règle d'or (§3)**.

**Invariant à préserver.** Tant que #777 n'est pas mergé **et** publié dans une release, la copie vendorisée est la **source de vérité** du correctif. Ne pas la « nettoyer » ni la réaligner sur la v2.2.0 stock.

---

## 3. ⚠️ Règle d'or — le piège du hotfix intermédiaire

L'intégration est installée **via HACS** mais avec des fichiers **patchés à la main** ; HACS croit toujours être en **v2.2.0**. HACS proposera **n'importe quelle** release **> 2.2.0**.

> **RÈGLE D'OR : n'accepter une mise à jour HACS d'`audiconnect` QUE si les notes de la release cible mentionnent explicitement la PR #777 (device-code).**

Contre-exemple à éviter : si un mainteneur publie un **hotfix intermédiaire** (ex. `v2.2.1`) qui **ne contient pas** #777, cliquer « Update » dans HACS **écrase** le device-code par l'ancien code login/mot de passe → **la voiture recasse**.

**Mesure de protection immédiate.** D'ici le merge de #777 : **ignorer toute proposition de mise à jour HACS** sur `audiconnect`. Ne **pas** modifier le champ `version` de `manifest.json` (le laisser à `2.2.0`) — le remonter empêcherait HACS de détecter la future bonne release.

---

## 4. Phase A — Intérim (maintenant → merge de #777)

**Objectif : rester aligné sur l'amont sans diverger, sans rien casser.**

1. **Ne rien faire par défaut.** Le correctif vendorisé suffit ; la voiture fonctionne.
2. **Geler le `manifest.json`** à `version: 2.2.0` (cf. §3).
3. **Surveiller #777.** Si la branche `jonny190:feat/device-code-auth` évolue pendant la revue (retours mainteneurs, correctifs), **re-synchroniser** ces changements dans la copie vendorisée pour éviter la dérive :
   - récupérer le(s) fichier(s) modifié(s) depuis la branche #777 ;
   - rejouer le diff dans `custom_components/audiconnect/` ;
   - **re-vérifier** les deux invariants du §6 (scope `mbb`, chaînes FR device-code) ;
   - committer sur la branche de travail avec un message `fix(audiconnect): re-sync device-code from upstream #777`.
4. **Surveiller #778.** Si un mainteneur demande des retouches sur la traduction FR, les appliquer dans la PR **et** répercuter dans `translations/fr.json` vendorisé.

**Alternative écartée.** Installer #777 en « beta » via un dépôt personnalisé HACS pointant sur le fork `jonny190` : impraticable tant que la branche n'a pas de tag de pré-release ; la copie vendorisée reste plus sûre.

---

## 5. Phase B — Bascule propre via HACS (après merge + release)

**Déclencheur : une release officielle `> 2.2.0` dont les notes listent #777** (idéalement aussi #778).

1. **Vérifier la release.** Confirmer que le tag contient bien #777 (device-code). Noter si #778 (FR) y est **ou non**.
2. **Filet de sécurité git.** Poser un tag avant bascule : `git tag pre-hacs-audi-<AAAA-MM-JJ>` (l'état est déjà versionné, mais le tag facilite le rollback).
3. **Mettre à jour via HACS** → redémarrer Home Assistant. HACS remplace le dossier `custom_components/audiconnect/` par le contenu de la release.
4. **Vérifications post-update (§6).**
5. **Réconcilier le dépôt.** `git diff` du dossier re-téléchargé vs la copie pré-bascule ; committer l'état post-update dans arsenal (`chore(audiconnect): adopt official release vX.Y.Z (device-code)`), le dépôt reflète de nouveau le runtime.
6. **Si `fr.json` a régressé** (release sans #778) → ré-appliquer les chaînes FR device-code depuis `pre-hacs-audi-<date>`, ou attendre le merge de #778. Objectif préférable : **faire merger #778 d'abord**.
7. **Clôturer ce chantier** une fois la release officielle adoptée et le runtime vérifié.

---

## 6. Critères d'acceptation / checklist de non-régression

À vérifier après **toute** re-synchronisation (Phase A) **et** après la bascule HACS (Phase B) :

- [ ] **Auth device-code opérationnelle** : le refresh de token réussit, pas de `KeyError('access_token')`, pas de re-configuration requise.
- [ ] **Scope `mbb` présent** : `DEVICE_CODE_SCOPE` contient bien `mbb` (`grep DEVICE_CODE_SCOPE custom_components/audiconnect/audi_services.py`). Sans lui, trip / climater / charger cassent silencieusement.
- [ ] **Capteurs métier peuplés** : autonomie, distance, état de charge, climatisation → valeurs non `unknown`.
- [ ] **UI FR** : l'étape « device » du config-flow affiche le texte et le lien de vérification en **français** (pas de corps vide — HA ne retombe pas sur l'anglais pour une intégration custom).
- [ ] **`manifest.json`** : `version` cohérent avec l'objectif (Phase A : figé `2.2.0` ; Phase B : version de la release officielle).
- [ ] **Dépôt = runtime** : l'état déployé est committé sur la branche de travail.

---

## 7. Renvois

- Contrat normatif du domaine : [`contrats/voiture.md`](../../../contrats/voiture.md).
- Audit du domaine (état runtime) : [`audits/01_rapports/voiture/audit_domaine_audi.md`](../../01_rapports/voiture/audit_domaine_audi.md).
- Manifeste de l'intégration : `custom_components/audiconnect/manifest.json`.
- Amont : issue #772, PR #777, PR #778 (`audiconnect/audi_connect_ha`).
