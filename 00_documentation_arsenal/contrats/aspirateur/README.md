# CONTRAT ARSENAL — ASPIRATEUR
## Index du domaine

**Domaine :** `aspirateur` — pilotage du robot aspirateur de la maison
**Version contrat :** v1.0
**Statut :** **Normatif — antérieur au runtime.** Fixe la doctrine, les invariants
opposables et les refus du domaine.
**Réalisation :** **aucune.** Ce lot ne crée ni runtime, ni helper, ni script, ni
automation, ni checker, ni dashboard, ni entrée de navigation. Il n'émet aucune
commande Home Assistant ni Roborock.

---

## Doctrine fondatrice (à retenir avant tout)

> L'objectif est de **remplacer l'usage courant de l'application Roborock par
> Home Assistant** — sans jamais transporter dans Arsenal les **silences** de
> l'appareil.

La voie technique retenue échoue **sans erreur** : une demande portant sur des
segments hors carte active est **tronquée en silence**, ou **n'émet rien du tout
en « réussissant »**
([audit](../../audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md) §8.1).

- **Arsenal décide, valide et refuse.** L'appareil n'est jamais l'arbitre de la
  cohérence d'une demande.
- **Un silence de l'appareil n'est jamais une réussite.** Toute issue non prouvée
  est qualifiée, jamais présumée.
- **Un refus est un livrable**, pas un échec : il porte un motif lisible.
- **Une mission porte une seule carte.** C'est une contrainte physique, pas une
  préférence d'ergonomie.

---

## Convention — noms conceptuels (NON figés)

Ce contrat est **antérieur au runtime**. Aucun `entity_id` Arsenal, aucun nom de
helper, de script ou d'automation, aucun ID d'automation n'est figé ici.

- Les **rôles Arsenal à créer** sont désignés par des noms **conceptuels** entre
  chevrons : `‹moteur_de_mission›`, `‹intention_courante›`, `‹verdict_de_mission›`.
  Un nom `‹…›` désigne un **rôle**, jamais une entité. Leur ratification relève
  d'un lot runtime ultérieur — inventaire au chapitre
  [`12`](12_identifiants_a_fournir.md).
- Les **entités natives Roborock** citées dans ce contrat sont, elles, **réelles
  et observées** : elles proviennent du relevé de l'audit, aucune n'est inventée.
  Les nommer n'est pas les ratifier comme surface commandable — la doctrine
  d'encapsulation du chapitre [`07`](07_moteur_de_mission.md) borne leur usage.

Cette convention reprend celle du domaine arrosage
([`../arrosage/README.md`](../arrosage/README.md)).

---

## Structure du dossier

| Fichier | Contenu |
|---|---|
| [`01_finalite_et_perimetre.md`](01_finalite_et_perimetre.md) | Finalité métier V1, expérience opérateur cible, ce que le domaine couvre et ce qu'il ne couvre pas ; place du Garage |
| [`02_referentiel_cartes_et_pieces.md`](02_referentiel_cartes_et_pieces.md) | Référentiel **métier** cartes ↔ segments ↔ pièces, **référentiel technique** des libellés exacts de l'appareil (§2.1), périmètres prédéfinis, règle de restitution des libellés |
| [`03_profils_metier.md`](03_profils_metier.md) | Les cinq profils arrêtés, mode de nettoyage dérivé et jamais écrit, prérequis matériel des profils avec eau |
| [`04_nombre_de_passages.md`](04_nombre_de_passages.md) | `×1` / `×2` / `×3`, convention de comptage, interdiction de transposer la convention zonée |
| [`05_intention_de_mission.md`](05_intention_de_mission.md) | L'intention de mission comme objet complet et atomique ; séparation intention / validation / exécution |
| [`06_integrite_mono_carte.md`](06_integrite_mono_carte.md) | `ASP-IMC-1` — intégrité mono-carte, ratification contractuelle de la contrainte de sécurité candidate de l'audit |
| [`07_moteur_de_mission.md`](07_moteur_de_mission.md) | Écrivain unique, **partition fermée des états de lancement**, séquence normative, **constantes temporelles 30 s / 60 s** (§3.1), qualification des trois issues, interdits d'exécution et **reprise sous garde** |
| [`08_etats_et_observation.md`](08_etats_et_observation.md) | Modèle d'états du domaine — **dix états canoniques, total sur la partition** ; mission ouverte ≠ nettoyage réel ; autorité de l'état `vacuum` sur le mouvement ; **disjonction déterministe** `MISSION_DEJA_OUVERTE` / `SESSION_INACHEVEE` |
| [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md) | Catalogue opposable des refus et des échecs, motifs lisibles, interdiction du fallback silencieux |
| [`10_raccourcis.md`](10_raccourcis.md) | Raccourcis = préréglages d'intention ; interdiction d'un second moteur ou d'un second chemin de commande |
| [`11_frontiere_ui.md`](11_frontiere_ui.md) | Frontière backend / UI : ce que l'UI rend et sollicite, ce qu'elle ne calcule ni ne commande jamais |
| [`12_identifiants_a_fournir.md`](12_identifiants_a_fournir.md) | Rôles abstraits dont l'identifiant doit être attribué par l'opérateur — aucune valeur proposée |
| [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md) | Hors périmètre du domaine, arbitrages contractuels explicites, questions ouvertes |
| [`14_entretien.md`](14_entretien.md) | **Entretien des consommables** — quatre postes, seuil d'échéance, remise à zéro confirmée, allowlist de la primitive irréversible, routage des erreurs |
| [`15_conduite_et_supervision.md`](15_conduite_et_supervision.md) | **Conduite et supervision de mission** — trois écrivains du verdict et leur disjonction, partition en quatre classes, séquence opposable d'un geste (engagement, émission unique, relecture bornée), sérialisation par le verdict, supervision d'une mission ouverte, réconciliation totale au redémarrage, routage du canal mobile |

---

## Chaîne logique

```
Finalité métier (01)
  └─ Référentiel cartes / pièces (02 — vérité de désignation)
       └─ Profils (03) + Nombre de passages (04 — vérité de réglage)
            └─ Intention de mission (05 — ce que l'opérateur demande)
                 └─ Intégrité mono-carte (06 — condition de sûreté)
                      └─ Moteur de mission (07 — écrivain unique, séquence)
                           └─ États & observation (08 — ce que le système sait)
                                └─ Refus & diagnostics (09 — ce que le système dit)
                                     └─ Raccourcis (10) · Frontière UI (11)
```

---

## Source factuelle du domaine

Ce contrat **ne relève rien lui-même** : il **arbitre et norme** les faits établis
par l'audit canonique du domaine —
[`audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md`](../../audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md)
(runtime observé, lecture du code source des versions en service, lot terrain
T1/T2 du 2026-08-26).

> **Rapport d'autorité.** L'audit est un **relevé** : il n'est ni normatif ni
> opposable, et il le dit lui-même. Le présent contrat est **normatif et
> opposable** ; il **ratifie** ce qu'il retient de l'audit et **assume** ce qu'il
> arbitre. En cas de divergence entre un fait d'audit et une clause de ce
> contrat, le fait d'audit prime sur la description du monde, le contrat prime
> sur la conduite du système.

---

## Renvois — doctrine transverse réutilisée

Ce domaine **réutilise** la doctrine Arsenal plutôt que de la dupliquer :

- Invariants universels, trois régimes d'un état externe, disponibilité explicite :
  [`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
- Séparation décision / action :
  [`separation_decision_action.md`](../../architecture/03_doctrines/separation_decision_action.md)
- Impossibilité physique (A) vs interdiction de politique (B) :
  [`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md)
- Autorité unique, révocabilité de la délégation :
  [`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md)
- Encapsulation d'une commande native derrière une action supervisée (modèle) :
  [`../arrosage/11_mode_manuel_supervise.md`](../arrosage/11_mode_manuel_supervise.md)
- Séparation besoin / intention / exécution (modèle) :
  [`../arrosage/05_intention.md`](../arrosage/05_intention.md)
- Exécution idempotente, post-condition et qualification d'échec (modèle) :
  [`../climatisation/08_execution.md`](../climatisation/08_execution.md)
- Modèle d'états et vocabulaire canonique (modèle) :
  [`../alarme/10_modele_etats_et_vocabulaire.md`](../alarme/10_modele_etats_et_vocabulaire.md)
- Frontière UI :
  [`../../ui/architecture_transverse.md`](../../ui/architecture_transverse.md)

---

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)
