# Cadrage — Précipitations : autorité unique d'acquisition, qualifications plurielles (D-PLUIE / C17)

| Champ | Valeur |
|---|---|
| **Type** | Cadrage / arbitrage de chantier (conception préalable, **sans implémentation**) |
| **Domaine** | Météo — précipitations : couche d'acquisition + qualification (production des signaux pluie) |
| **Statut** | **Arbitré (2026-07-11) — direction incrémentale retenue.** **Lot 1 (contrat de production) LIVRÉ** : contrat normatif [`meteo/pluie_production.md`](../../../contrats/meteo/pluie_production.md) + checker CI `contracts_pluie_production.yml` ; la distinction chambres / séjour est désormais **gravée et opposable**. **Lot 2 séquencé, non engagé** (inchangé). Aucun runtime de fusion à ce stade. |
| **Version** | 0.1 (cadrage) |
| **Date** | 2026-07-11 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `29a1f20` |
| **Cadre** | Aucun YAML, aucun patch runtime, aucun helper, aucune automation, aucun ID d'automation, aucun changement d'entité, aucune modification UI. Ne fixe aucune règle opposable — **prépare** un futur contrat, n'en tient pas lieu. |
| **Registre** | Chantier **C17** — ② Parqués, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (ex-`D-PLUIE`, promu par arbitrage propriétaire 2026-07-11) |

> **Objet.** Acter la direction de traitement de la **couche de production des
> signaux de précipitation** d'Arsenal, à la lumière d'une **distinction métier
> clarifiée par le propriétaire** (chambres ≠ séjour). Reformuler la notion
> d'« autorité unique » — non comme une fusion des signaux, mais comme une
> **acquisition sécurisée partagée** dont **dérivent des qualifications
> volontairement plurielles**. Poser le séquencement (contrat d'abord,
> sécurisation ensuite) et les exclusions.

> **Garde-fou de lecture.** Ce document **ne décide rien d'opposable**, **ne crée
> aucun runtime**, **ne fixe aucun seuil**. La doctrine du domaine et les contrats
> priment ; en cas de divergence, **les contrats font foi**. Source d'analyse :
> [`audit_precipitations_domaine.md`](../../01_rapports/meteo/audit_precipitations_domaine.md)
> et [`audit_precipitations_chaine_decisionnelle.md`](../../01_rapports/meteo/audit_precipitations_chaine_decisionnelle.md).

---

## 1. État actuel (constat, sourcé)

| Élément | État réel | Source faisant foi |
|---|---|---|
| **Évidence consolidée any-rain** | **Livrée (C16, #337)** : `binary_sensor.pluie_evidence_active`, déclarative, multi-source (Netatmo `>0` ∪ SNZB borné 10 min ∪ injection), disponibilité = ≥ 1 source réelle. Consommée par les deux écrivains de `pluie_en_cours`. **Validation terrain en attente.** | `12_template_sensors/meteo/pluie/evidence_active.yaml` · `REGISTRE_CHANTIERS.md` (C16) |
| **Qualification « pluie forte »** | `binary_sensor.intention_pluie_forte` = Netatmo intensité ≥ `seuil_pluie_fermeture_volets` (2,5 mm). **Netatmo-seul, correct par construction** (cf. §2). | `12_template_sensors/volets/intention_pluie_forte.yaml` |
| **Qualification « pluie récente »** | `binary_sensor.pluie_recente` = Netatmo `last_hour` > 0. | `12_template_sensors/meteo/pluie/recente.yaml` |
| **Acquisition (sources de décision)** | Les qualifications lisent les **sources brutes externes** (`sensor.pluviometre_precipitation` cloud Netatmo, `binary_sensor.zigbee_pluie_water_leak` Zigbee). **Aucune façade locale sécurisée côté décision** — alors qu'elle existe côté cumuls (`sensor.pluie_total_local`). | `securisation_capteurs_externes.md` · audit domaine §6.2 |
| **Contrat de production** | **Inexistant.** `volets_pluie.md` §5.2 délègue la frontière à « un contrat météo distinct » qui n'existe pas ; la précipitation n'est pas un axe reconnu de `capteurs_meteo.md`. | `contrats/volets_pluie.md` §5.2 · audit domaine §7.1 |
| **Vérification CI** | Aucune sur la chaîne de production/qualification (palmarès pluie inclus). | `REGISTRE_COUVERTURE_VERIFICATION.md` |

> **Conséquence.** L'aigu (état collant) est **traité par C16**. Ce qui reste est
> une dette de **cohérence d'acquisition** (sources brutes) et de **gouvernance**
> (frontière non contractualisée), **sans incident actif**.

---

## 2. Distinction structurante — chambres ≠ séjour (le pivot de ce cadrage)

C'est la clarification métier qui **corrige** la lecture initiale de l'audit et
recadre toute la portée.

| | **Chambres** | **Séjour** |
|---|---|---|
| Objet de la protection | **Fenêtre ouverte** : empêcher l'entrée d'eau | **Ouvrant / façade** : protéger préventivement le volet, **baie même fermée** |
| Événement déclencheur | **Détection précoce** de pluie **+ fenêtre concernée ouverte** | **Pluie forte** (indépendante de l'ouverture) |
| Signal consommé | `pluie_en_cours` (any-rain, multi-source) | `intention_pluie_forte` (Netatmo ≥ 2,5 mm) |
| Rôle des premières gouttes | **Déterminant** (une fenêtre ouverte + bruine = eau à l'intérieur) | **Non pertinent** (protection préventive « pluie forte ») |

**Corollaire physique décisif.** Seule une **mesure quantitative** (le pluviomètre)
peut établir « ≥ 2,5 mm ». Le SNZB-05 est **binaire** (mouillé/sec) et **ne peut
pas** contribuer à une qualification « forte ». Donc `intention_pluie_forte`
**Netatmo-seul est la bonne source pour ce concept** — ce n'est pas une asymétrie
subie.

> **Requalification actée.** Le séjour **n'est pas « aveugle aux premières gouttes »
> au sens d'un défaut** : il poursuit un **objectif métier différent**. La lecture
> « limite » des audits sur ce point est **retirée** ; arbitrage propriétaire :
> **acceptable par design.**

---

## 3. Arbitrage

**Décision (propriétaire, 2026-07-11) : direction incrémentale, contrat de production d'abord.**

1. **« Autorité unique » recadrée.** Non pas *fusionner* les signaux (ce serait
   effacer des distinctions métier utiles), mais **unifier l'ACQUISITION** :
   une couche de sensing **sécurisée et partagée** d'où **dérivent** des
   qualifications **volontairement plurielles** (any-rain / forte / récente).
   La pluralité des qualifications est **saine et à documenter**, pas à résorber.
2. **Pas de refonte big-bang.** `pluie_en_cours` reste le *latch* d'épisode
   (piloté par l'évidence C16) ; on ne remplace pas les entités d'un coup.
3. **Séjour hors périmètre de modification** (acceptable par design, §2).
4. **Priorité au contrat** (Arsenal contract-first) : il *documente* la pluralité
   voulue — donc **protège la distinction chambres/séjour** contre une future
   « simplification » hâtive — et **ouvre la CI**.

---

## 4. Doctrine cible (principes du futur contrat de production — non opposables ici)

- **Une acquisition sécurisée, des qualifications dérivées.** Les sources externes
  (Netatmo cloud, SNZB Zigbee, prévision) sont **sécurisées localement** avant
  toute consommation décisionnelle (conforme `securisation_capteurs_externes.md`) ;
  les qualifications en dérivent.
- **Qualifications nommées et distinctes**, chacune avec **objectif métier, source
  légitime, seuil, régimes, consommateurs** explicites :
  - *pluie détectée / en cours* (any-rain) — multi-source, protection fenêtres ouvertes ;
  - *pluie forte* — Netatmo quantitatif, protection préventive séjour ;
  - *pluie récente* — contexte aération ;
  - *(réservés)* pluie prévue (déjà isolée), terminée, cumuls.
- **Trois régimes explicites** (`principes_generaux.md` §6) pour chaque source :
  nominal / absent / incohérent (l'acquis C16 en est l'exemple pour any-rain).
- **La précipitation comme axe** : reconnaître (ou documenter l'exclusion de) la
  précipitation dans le référentiel météo (`capteurs_meteo.md` ne la liste pas).
- **Séparation stricte** : le contrat régit la **production/qualification** ; la
  **réaction** (volets) reste régie par `volets_pluie.md` (frontière inchangée).

---

## 5. Prérequis (conditions de lançabilité)

| Prérequis | Pour quel lot | État |
|---|---|---|
| **Validation terrain de C16** (l'évidence confirmée en réel) | Lot 2 (bâtir la sécurisation *sur* l'évidence) et toute promotion de `pluie_evidence_active` en entité canonique | **En attente** (C16 « validation terrain en attente ») |
| Rédaction doc-first (aucun runtime) | Lot 1 (contrat) | **Aucun blocage** — lançable |

> Le **contrat (lot 1) peut être rédigé sans attendre** la validation terrain : il
> formalise l'existant et la cible. La **sécurisation runtime (lot 2)** gagne à
> attendre que l'évidence C16 soit confirmée en réel.

---

## 6. Exclusions (hors périmètre, opposables au futur chantier)

- **Fusion / collapse** des trois qualifications en un signal unique — **exclu**
  (elles sont plurielles par design).
- **Unification du séjour sur l'évidence** — **exclu** (acceptable par design, §2).
- **Refonte big-bang** de `pluie_en_cours` / des consommateurs — **exclu**
  (incrémental borné, réversible).
- **États gradués nouveaux** (pluie persistante, humidité résiduelle) — **réservés**
  (n'entrent que sur valeur fonctionnelle avérée, hors ce cadrage).
- **Modification de `volets_pluie.md`** ou de la chaîne volets — hors périmètre.

---

## 7. Séquencement proposé

| Lot | Objet | Nature | Dépendance |
|---|---|---|---|
| **Lot 1** | **Contrat de production** : définir les qualifications précipitations (objectif, source, seuil, régimes, consommateurs), **graver la distinction chambres/séjour**, combler la frontière orpheline `volets_pluie.md` §5.2, statuer sur l'axe précipitation. | Documentaire (contrat + éventuel checker/CI) | Aucune — lançable |
| **Lot 2** | **Sécurisation locale des sources de décision** : façade sécurisée Netatmo + SNZB côté décision (à l'image de `pluie_total_local`), consommée par les qualifications. | Runtime borné, réversible | Validation terrain C16 |
| **CI** | Checker + workflow du contrat de production (recoupe la **parité CI palmarès pluie** — cf. backlog ④ / C14). | Outillage | Après lot 1 |

Chaque lot est **re-décidé à son engagement** ; l'ouverture de ce cadrage ne vaut
pas décision d'implémenter un lot.

---

## 8. Renvois

- Audits sources : [`audit_precipitations_domaine.md`](../../01_rapports/meteo/audit_precipitations_domaine.md), [`audit_precipitations_chaine_decisionnelle.md`](../../01_rapports/meteo/audit_precipitations_chaine_decisionnelle.md).
- Acquis C16 : `12_template_sensors/meteo/pluie/evidence_active.yaml`, `REGISTRE_CHANTIERS.md` (C16).
- Doctrine : [`securisation_capteurs_externes.md`](../../../architecture/securisation_capteurs_externes.md), [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) (§6), [`capteurs_meteo.md`](../../../architecture/capteurs_meteo.md).
- Contrat de réaction (frontière inchangée) : [`volets_pluie.md`](../../../contrats/volets_pluie.md) (§2, §5.2).
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C17).
