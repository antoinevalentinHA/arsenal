# Découpage proposé en lots — **V3.1**

> **V3.1 — correction `R-2` : `A-15` manquait à la table d'état du §5, alors que le §2 le porte.**

> **Statut : PROPOSITION NON RATIFIÉE.**
> **Aucun lot n'est engageable tant que les arbitrages qui le bloquent ne sont
> pas rendus.** Ce découpage est soumis à l'opérateur au même titre que les
> **quinze** arbitrages de `02_ARBITRAGES_OUVERTS.md`.

> **Corrections V2 :** le lot « L2a » de CI seule **n'existe plus** — il n'était
> ni séparable du runtime ni exempt de robot ; la dépendance affirmée du lot
> Maintenance à cet amendement était **fausse** et masquait un trou de contrôle
> réel ; le lot contractuel Maintenance fait **dériver le registre de
> couverture** ; le candidat de premier lot de la V1 est **retiré**.

> **Corrections V3 :** la mise à jour du registre de couverture est portée au
> lot **L2**, conditionnellement à `A-9`, et la règle est **généralisée** à
> toute création de chapitre contractuel (§3.4) ; le lot L2 porte désormais
> l'arbitrage **`A-15`** et l'amendement de `ASP-CI-20` ; le piège de rédaction
> `ASP-CI-3` est ajouté (§3.5) ; **U2 hérite aussi de `A-3`**.

---

## 1. Natures, et pourquoi elles sont distinguées

Un lot qui mélange des natures n'est **pas auditable séparément** : il faut
alors ouvrir un contrat, un checker et du runtime dans le même geste, et rien
ne permet plus de dire ce qui a cassé quoi.

| Nature | Ce qu'elle recouvre |
|---|---|
| **Contrat** | Chapitre normatif, amendement d'invariant, registre documentaire confronté par la CI |
| **CI** | Amendement ou création de contrôle mécanique |
| **Runtime L1** | Les cinq fichiers existants du moteur et de ses helpers |
| **Runtime L2** | Script de conduite, automations d'écriture |
| **Templates** | Capteurs dérivés, sans effet sur l'appareil |
| **Notifications** | Automations de projection persistante, canal mobile |
| **UI** | Lovelace, helpers d'interface, scripts de composition |

---

## 2. Lots proposés

| Lot | Contenu proposé | **Natures mêlées** | Robot ? | Notification créée ? | Arbitrages bloquants |
|---|---|---|---|---|---|
| **M0** | Acte contractuel Maintenance : périmètre à quatre éléments, plafonds, sens de variation, primitive de remise à zéro, vocabulaire du verdict d'entretien, invariants d'absence de remise à zéro automatique et de répétition, qualification du vidage et ses deux bornes d'honnêteté, levée de l'exclusion des consommables. **Plus la mise à jour du registre de couverture** | **Contrat** | Non | Non | **A-6** |
| **L2** | **Indissociable** — acte contractuel de conduite et de supervision ; amendement de `ASP-CI-11`, `14`, `18`, `19` **et `20`** ; amendement conditionnel de `ASP-CI-10` selon A-15 ; **mise à jour du registre de couverture si A-9 retient la forme « nouveau chapitre »** ; **contrainte de rédaction `ASP-CI-3`, à rejouer pendant la rédaction** ; mise à jour des **deux fichiers L1** du vocabulaire et du motif lisible ; script de conduite ; automation de supervision ; automation de projection de mission | **Contrat + CI + Runtime L1 + Runtime L2 + Notifications** | **Oui** | Oui | **A-3, A-4, A-9, A-10, A-11, A-15** |
| **M1** | Entités dérivées d'entretien : liste des éléments dus et témoin binaire, **distinguant dû / non dû / non évaluable** | **Templates** | Non | Non | **A-1** |
| **U0** | Couche d'intention : sélecteurs, booléens de segment, scripts de composition et de raccourcis ; **mécanisme de remise à zéro au redémarrage — automation dédiée ou report sur un writer existant, selon A-12** ; **confrontation de CI du référentiel embarqué** | **UI + CI + Runtime L2** | Non | Non | **A-3, A-5, A-12, A-13** |
| **N1** | Automation de projection d'entretien et notification persistante agrégée | **Notifications** | Non | **Oui, dès le déploiement** | **A-1, A-3, A-8** |
| **M2** | Script de déclaration d'entretien et remise à zéro confirmée ; **garde de CI sur la primitive irréversible** | **Runtime L2 + CI** | **Oui — irréversible** | Non | **A-2, A-14** |
| **U1** | Ajout, dans le dashboard Système, de la carte récapitulative NAS **et** du raccourci vers le dashboard NAS. **N'enlève rien** | **UI** | Non | Non | *aucun bloquant* — voir A-7 |
| **U2** | Retrait du bouton NAS de Navigation **et** pose de la carte Aspirateur, dans le même geste | **UI** | Non | Non | **A-3, A-5, A-12, A-13** *(par dépendance à U0)* |

---

## 3. Dépendances

```
M0  ──►  M1  ──►  N1
M0  ──►  M2                       (M2 dépend du contrat, PAS d'un amendement de CI)
L2  (indissociable — contrat + CI + runtime L1 + runtime L2 + notifications)
U0  ──►  U2
U1  ──►  U2                       (U1 n'enlève rien ; U2 échange)
```

### 3.1 Ce que la V1 affirmait à tort

> « M2 dépend aussi de L2a : la CI refuse aujourd'hui tout appel d'appareil hors
> des cinq fichiers L1. »

**C'est faux.** `ASP-CI-11` ne refuse que les lignes `action:` / `service:`
valant littéralement un service `vacuum.<x>` ou `roborock.<x>`, plus les deux
helpers de mission. La remise à zéro passe par une **pression de bouton sur une
entité native**, qui n'est ni l'un ni l'autre. Et `ASP-CI-7`, seul contrôle qui
connaisse le domaine `button`, **ne balaie que Lovelace et les gabarits de
carte**.

> **Le lot Maintenance n'a donc besoin d'aucun amendement de CI — et la seule
> primitive irréversible du périmètre circule aujourd'hui sans aucune garde.**
>
> Le raisonnement que la V1 s'appliquait à elle-même — « ouvrir sans étendre
> créerait un trou de contrôle sur la seule primitive dangereuse du domaine » —
> vaut exactement ici, et n'était pas tenu. **Arbitrage A-14.**

### 3.2 Pourquoi L2 est indissociable

`ASP-CI-18` exige que **toute valeur du vocabulaire soit effectivement écrite**
par un writer, **et** confronte le décompte au texte de l'en-tête du fichier L1.

Porter la constante sans livrer conjointement les fichiers qui écrivent les
valeurs nouvelles fait **échouer la CI immédiatement**.

> **Il n'existe donc aucun lot de CI seul, et aucun ordonnancement où
> l'amendement précéderait le runtime.** La V1 proposait un lot « L2a »
> ordonnançable avant le runtime et le rangeait parmi les lots ne sollicitant
> pas le robot : **les deux affirmations étaient fausses.**

### 3.3 Le piège de rédaction du lot contractuel Maintenance

`ASP-CI-10` balaie les durées de **tous les chapitres** du domaine et n'admet
que **30 s** et **60 s**.

> **Les plafonds doivent donc être écrits en HEURES dans le chapitre
> Maintenance** — 300 h, 200 h, 150 h, 30 h. Les écrire en secondes y ferait
> lire des durées concurrentes et **casserait la CI**.

### 3.4 La dérive du registre de couverture — **règle généralisée en V3**

Un contrôle transverse compte les fichiers de contrat et confronte ce nombre
aux chiffres du registre de couverture ; toute dérive est une **erreur dure**.

> **Règle générale, opposable à tout lot du domaine :**
>
> **Toute création d'un chapitre contractuel — Maintenance comme L2 — impose,
> dans le même lot, la mise à jour de `REGISTRE_COUVERTURE_VERIFICATION.md` et
> le rejeu de `check_ci_coverage_registry.py`.**

**Deux arbitrages déclenchent cette conséquence, et pas un seul :**

| Arbitrage | Forme qui déclenche | Lot concerné |
|---|---|---|
| **A-6** | « nouveau chapitre » Maintenance | **M0** |
| **A-9** | « nouveau chapitre » de conduite et de supervision | **L2** |

> **Correction V3.** La V2 restreignait cette conséquence à « la forme 1 de
> l'arbitrage A-6 », et le contenu du lot L2 ne portait pas la mise à jour du
> registre. **Sous la forme 1 d'A-9, le lot L2 aurait échoué en CI pour
> exactement la raison que la V2 venait d'identifier ailleurs** — alors même
> qu'elle pose les deux arbitrages comme strictement symétriques.

### 3.5 Les deux pièges de rédaction, symétriques — **complété en V3**

| Lot | Piège | Règle |
|---|---|---|
| **M0** | Le balayage des durées n'admet que deux valeurs, exprimées en secondes | **Écrire les plafonds en heures** — 300 h, 200 h, 150 h, 30 h |
| **L2** | Le balayage des codes refuse tout jeton majuscule entre accents graves absent du catalogue | **Citer les valeurs sous leur forme complète préfixée**, jamais nue ; **rejouer `ASP-CI-3` pendant la rédaction** |

> **Correction V3.** La V2 avait levé le piège côté Maintenance et **pas** son
> jumeau côté L2. Voir `07_MACHINE_L2.md` §8.5.

---

## 4. Lots ne sollicitant pas le robot

Six des huit lots — **M0, M1, U0, N1, U1, U2** — n'exigent aucune mission,
aucun service d'appareil, aucune pression de bouton.

**L2 et M2 sollicitent le robot**, et M2 de façon **irréversible**.

Parmi les six, **cinq ne créent aucune notification**. Seul **N1** en crée une,
et il en créera une **immédiatement** : l'élément « nettoyage des capteurs » est
consommé à 86,6 %. Ce n'est pas une notification de test, mais une projection
d'état légitime — à connaître avant de décider.

---

## 5. Aucun candidat de premier lot

> **La V1 proposait le regroupement M0 + L2a + M1 + U0 comme premier lot « sans
> effet sur l'appareil ». Ce candidat est RETIRÉ.**
>
> Il mêlait contrat, CI, runtime L1 et templates dans un ensemble présenté comme
> auditable séparément, alors que sa composante L2a n'était ni séparable du
> runtime L2, ni exempte de robot. Le regroupement était donc **doublement
> faux**.

**État réel de chaque lot au regard de ses arbitrages :**

| Lot | Arbitrages bloquants ouverts | Engageable ? |
|---|---|---|
| M0 | A-6 | **Non** |
| M1 | A-1 | **Non** |
| M2 | A-2, A-14 | **Non** |
| L2 | A-3, A-4, A-9, A-10, A-11, **A-15** | **Non** |
| U0 | A-3, A-5, A-12, A-13 | **Non** |
| N1 | A-1, A-3, A-8 | **Non** |
| U2 | A-3, A-5, A-12, A-13 *(par U0)* | **Non** |
| **U1** | **aucun bloquant** | **Non — le cadrage lui-même n'est pas ratifié** |

**U1 est le seul lot dont aucun arbitrage bloquant n'est ouvert.** Il est de
nature **UI** unique, n'enlève rien, et laisse deux points d'entrée NAS
coexister. Ce constat est **factuel** : il ne vaut pas recommandation
d'engagement, la ratification du cadrage restant préalable à tout lot.

---

## 6. Ce que ce découpage ne préjuge pas

- Ni l'ordre définitif, ni le regroupement des lots.
- Ni le contenu exact d'un lot, tant que les arbitrages qui le bloquent ne sont
  pas rendus.
- Ni l'opportunité de la fonctionnalité : le cadrage décrit ce qui serait
  faisable et conforme, **pas ce qui doit être fait**.
