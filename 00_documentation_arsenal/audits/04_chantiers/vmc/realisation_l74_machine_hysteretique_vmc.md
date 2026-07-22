# Réalisation L7.4 — machine hystérétique et libération modulée (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.3 |
| **Lot** | **L7.4 — machine hystérétique et libération modulée.** **Lot pivot du chantier** |
| **Statut** | **Préparé sur branche** |
| **Calibration** | Passe 5 de L2b — [`arbitrage_parametres_provisoires_vmc.md`](arbitrage_parametres_provisoires_vmc.md), `arsenal-runtime` `475f43a` |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2 → v2.3** — §2.2, §2.2 bis, §2.3, §4.4 bis, §6.2, §6.3, §6.4, §7.4 bis, §9.1, §9.1 bis, **§9.1 ter (nouveau)**, §10.2, §10.4, §12.3. **CO-CHANGEMENT CONTRACTUEL** — voir §9 bis |

> **L'écart contractuel n° 3 est résorbé.** Les besoins deviennent
> hystérétiques, la voie d'évolution devient décisionnelle, et la frontière de
> libération est modulée par la température extérieure.

---

## 1. La machine

```
OFF = borne( A − B × T_ext )        bornée dans [borne basse, borne haute]
P   = OFF + H

entrée      : niveau ≥ S   OU   ( évolution ≥ D sur W   ET   niveau ≥ P )
maintien    : ni entrée ni libération satisfaites
libération  : niveau ≤ OFF
```

Elle est répartie sur **quatre objets**, chacun avec un rôle unique :

| Objet | Rôle |
|---|---|
| `sensor.vmc_frontiere_liberation_sdb_*` | **calcule** `OFF` et `P`, **détient** `A`, `B`, `H`, **expose** tout |
| `input_boolean.vmc_etat_besoin_sdb_*` | **porte** l'état booléen minimal |
| `binary_sensor.vmc_besoin_humidite_sdb_*` | **expose** l'état et l'explicabilité |
| Automatisations `…07` et `…08` | **transitionnent** l'état, et rien d'autre |

**Aucun `entity_id` existant n'est renommé.** Le besoin conserve le sien : sa
nature change — il expose au lieu de comparer —, pas son nom.

---

## 2. Le porteur d'état — pourquoi un `input_boolean`

L6 avait établi qu'un besoin doit devenir un **état écrit**. L7.1 avait précisé
le constat : l'idiome `is_state(this.entity_id, …)`, pratiqué ailleurs dans le
dépôt, tient l'hystérésis **en session** mais **ne survit pas au redémarrage**.

Le **§9.1** exige que l'état soit **restauré** puis confronté aux mesures. Un
`input_boolean` est restauré nativement : c'est le seul porteur disponible sans
Python.

> **Un booléen ne peut structurellement rien porter d'autre.** Le §2.2 interdit
> mémoire d'épisode, instant de début, durée écoulée, valeur de pic, historique,
> compteur et timer ; le §9.1 précise que la restauration « ne restaure ni
> instant, ni durée, ni valeur, ni historique ». La forme retenue **rend
> l'infraction impossible**, elle ne se contente pas de l'interdire.

**Auteur unique** : ces états sont écrits exclusivement par les deux
automatisations de machine. Ils ne sont **pas** des paramètres et ne figurent
dans aucun réglage éditable.

---

## 3. Les constantes — les cinq engagements de L7.0, tenus

| # | Engagement | Réalisation |
|---|---|---|
| 1 | constantes versionnées | littéraux dans le dépôt, modifiables par commit seul |
| 2 | différenciées par pièce | parents `A = 78 / B = 0,8 / H = 4` · enfants `A = 66 / B = 1,0 / H = 4` |
| 3 | définies une seule fois | uniquement dans la frontière — **contrôlé en CI** |
| 4 | exposées par l'entité calculatrice | attributs `constante_a`, `constante_b`, `bande_morte_h` du capteur qui calcule |
| 5 | jamais dupliquées ni remplacées par un repli | la machine **lit** la frontière, ne la recalcule pas ; aucun `float(défaut)` |

**La machine ne recalcule aucune frontière.** Elle lit `OFF` sur l'état du
capteur et `P` sur son attribut `plancher_evolution`. C'est ce qui rend
l'engagement 3 vérifiable plutôt que déclaratif.

**Frontières entières pour la salle de douche enfants** : le capteur y restitue
la mesure au point entier, donc `OFF` et `P` y sont arrondis — une frontière
décimale y serait **inatteignable par construction**.

---

## 4. La garde d'indisponibilité — §7.4 bis condition 4

| Situation | Comportement |
|---|---|
| Frontière calculable | machine nominale |
| **Frontière non calculable, besoin actif** | **maintien** — aucune écriture |
| **Frontière non calculable, besoin inactif** | **voie de niveau opérante** (elle n'en dépend pas) ; **voie d'évolution non calculable**, faute de plancher |

**La garde est structurelle, pas déclarative.** La condition de libération exige
`off_frontiere is not none` : si la frontière n'est pas calculable, la condition
est **fausse**, aucune branche du `choose` ne s'active, et l'état demeure.
`unknown` et `unavailable` **ne valent jamais libération**.

> **Aucune bascule vers une frontière fixe.** Ce serait substituer
> silencieusement un mécanisme dont l'**inopérance estivale est démontrée** —
> 8 épisodes sur 42 — et qui **échoue le contrôle du §7.4**.

**Aucune garde de libération n'est retenue**, conformément à la passe 5 : le cas
visé — panne isolée du capteur extérieur — n'est pas observé dans le corpus, et
une temporisation calibrée sur rien serait celle que le §8.3 interdit. **Risque
R4 assumé**, pire cas observé 71 h.

---

## 4 bis. Réévaluation au démarrage — §9.1 cas 1 à 3

**L'état restauré est immédiatement confronté aux mesures courantes**, par un
déclencheur `homeassistant.start` sur chaque machine.

| Cas §9.1 | Situation | Comportement |
|---|---|---|
| **1** | mesure au-dessus de la frontière d'entrée | la branche **entrée** s'active — l'état restauré **ne fait pas autorité contre elle** |
| **2** | mesure sous la frontière de libération | la branche **libération** s'active — même remarque |
| **3** | mesure **dans la bande morte** | aucune branche — l'état restauré est **conservé** |

**Les trois cas sont servis par la même machine, sans branche particulière.**
C'est la conséquence directe de la forme retenue : les conditions d'entrée et de
libération sont évaluées sur la **mesure courante**, jamais sur l'état restauré.

> **Pourquoi ce déclencheur n'est pas optionnel.** Sans lui, un état restauré
> **incohérent avec la mesure** subsisterait jusqu'à la publication suivante du
> capteur — **plusieurs minutes en salle de douche enfants**. Or le §9.1 pose que
> les cas 1 et 2 « **priment inconditionnellement** », et le §12.3 range parmi
> les non-conformités « un état restauré l'emportant sur une mesure courante hors
> bande morte ».
>
> **C'est ce lot qui crée un état restaurable** : c'est donc à lui de le
> confronter, et non à un lot ultérieur.

**Contrôlé en CI**, avec preuve négative : retirer le déclencheur de démarrage
fait échouer le checker.

**Ce qui demeure à L7.5** : le **cas 4** du §9.1 — aucun état valide
restaurable —, son exposition (§10.2 exigence 10), et le §4.4 — maintien sur
mesure inexploitable.

---

## 5. La profondeur de fenêtre — un écart rattrapé

**Point qui aurait échappé sans relecture de la simulation de calibration.**

La simulation de la passe 5 exige une **demi-fenêtre au minimum** avant que la
voie d'évolution puisse conclure. Sans cette condition, l'implémentation aurait
été **plus permissive que la calibration qui la fonde**.

La condition est donc reprise **à l'identique** : `age_coverage_ratio ≥ 0,5`,
attribut dont L7.3 a **constaté l'existence** sur les 38 bases.

Elle sert deux clauses :

- **§9.1 bis** — le critère dynamique **ne peut pas créer** de besoin tant que la
  fenêtre est insuffisamment remplie ;
- **§4.4 bis** — une profondeur insuffisante n'est **ni** une mesure
  indisponible, **ni** un critère non satisfait ; elle est exposée comme telle
  (`evolution_profondeur_suffisante`).

**Elle ne révoque aucun besoin** : elle ne conditionne que l'entrée.

---

## 6. Explicabilité — ce qui est désormais exposé

**Sur le besoin** (24 attributs) : état, **condition d'entrée**, **condition de
maintien**, **condition de libération** (§10.2 exigences 2, 3, 4), mesure,
**frontières réellement consommées** (§10.4), pièce, abstention, et les neuf
attributs de l'observation glissante.

Un attribut mérite d'être signalé : **`maintenu_faute_de_frontiere`**.

> Le §10.2 impose qu'un besoin **maintenu parce que la frontière n'est pas
> calculable** soit **distinguable** d'un besoin dont la condition est calculée
> et non satisfaite. **Les confondre est une non-conformité** (§12.3). Cet
> attribut porte exactement cette distinction.

**Sur la frontière** : exigences **20 à 24** — grandeur modulante, sa valeur
courante, la valeur courante de la frontière, les bornes, le statut calculable
et **sa raison**. S'y ajoute `statut_grandeur_modulante`, qui remonte la cause
publiée par l'axe météo sans quitter l'entité.

**Tous les motifs sont des conditions d'état**, jamais des récits (§10.3).

---

## 7. Effet attendu

Celui que la passe 5 a simulé, **sur le corpus et non sur le terrain** :

| Pièce | AVANT (trace L5) | Après L7.2 | **Attendu après L7.4** |
|---|---:|---:|---:|
| Parents | 64/138 | 73/138 | **102/138** |
| dont été | 5/42 | 5/42 | **22/42** |
| Enfants | 2/27 | **0/27** | **19/27** |

**La salle de douche enfants redevient opérante** — et le devient pour la
première fois réellement : elle passe de 0 à 19 épisodes sur 27, **entièrement
par la voie d'évolution**, aucun de ses épisodes n'atteignant la frontière de
niveau.

**Coût** : 13 % du temps en besoin chez les parents, 7 % chez les enfants ;
2,1 et 0,4 battements par mois.

### 7.1 Une divergence entre simulation et implémentation, à consigner

La simulation de la passe 5 **ignorait purement** les instants où la
température extérieure est indisponible ; l'implémentation, elle, **maintient**
le besoin actif et laisse la voie de niveau opérante.

> **L'implémentation est donc plus conservatrice que la simulation** sur les
> 3,6 % du temps où la grandeur modulante est inexploitable. Les chiffres
> ci-dessus sont **une estimation, pas une prédiction** — L8 mesurera le réel.

---

## 8. Contrôles

**Le garde-fou daté de L7.3 est retiré**, comme annoncé : il interdisait que la
référence glissante entre dans l'état, tant que la libération se confondait avec
l'entrée. **Il a rempli son office.** Ce qui le remplace :

| Test | Objet |
|---|---|
| **6** *(révisé)* | l'exposition des exigences 11 à 19 existe ; l'évolution **n'intervient ni dans le maintien ni dans la libération** (§2.2 bis) |
| **7** *(nouveau)* | exigences 20 à 24 exposées ; la frontière **ne lit aucune mesure de pièce** (§6.4) ; **les constantes ne sont définies nulle part ailleurs** ; **la libération vérifie que la frontière est calculable** (§7.4 bis condition 4) |

**Deux preuves négatives établies** : une libération sans garde de calculabilité
fait échouer le checker ; une constante dupliquée hors de l'entité calculatrice
aussi.

**86 checkers exécutés, tous passent.** Les sept fichiers runtime sont **valides
au parseur YAML**. Les **gates documentaires** passent.

> **Deux échecs demeurent, ANTÉRIEURS** : `lovelace_no_inline_templating` et
> `vacances`. Ni causés, ni aggravés.

---

## 9. Ce que ce lot ne fait pas

- il **ne modifie pas `/config`** ;
- il **ne recalibre rien** — les valeurs sont celles de la passe 5,
  **provisoires** ;
- il **ne traite pas le cas 4 du §9.1** — aucun état valide restaurable — ni son
  exposition (§10.2 exigence 10) : **L7.5**. Les cas 1 à 3 sont, eux, traités
  ici (§4 bis) ;
- il **ne traite pas le §4.4** — maintien sur mesure inexploitable : **L7.5** ;
- il **n'expose aucun paramètre en UI** : **L7.7** ;
- il **ne modifie le contrat que sur le point strictement nécessaire** — §9.1
  bis, §9.1 ter et §12.3 (§9 bis) : aucune autre clause n'est touchée ;
- il **ne clôt pas C35**.

---

## 9 bis. Co-changement contractuel — `vmc.md` v2.2 → v2.3

**La tension relevée par L7.3 ne pouvait plus rester ouverte.** Elle était sans
effet tant que la voie d'évolution n'était pas décisionnelle ; **ce lot la rend
décisionnelle**, donc la fenêtre reconstituée au démarrage a désormais un effet
réel sur la décision.

**Le §9.1 bis disait** : « L'observation glissante n'est pas restaurée. Elle
repart vide. » Et le §12.3 rangeait parmi les non-conformités « une observation
glissante **persistée au redémarrage** ».

Or la plateforme employée **recharge sa fenêtre depuis l'historique enregistré**.
Sous une lecture littérale, l'implémentation serait **non conforme**.

### 9bis.1 La distinction retenue

> **L'interdiction porte sur la persistance de l'observation elle-même** —
> reporter au-delà du redémarrage une valeur de référence, une évolution
> calculée ou une conclusion. **Elle ne porte pas sur la provenance des mesures**
> qui remplissent la fenêtre.

C'est la même nature de distinction que celle retenue en v2.2 entre **mesure
comparée** et **point de comparaison** : ce qui est prohibé, c'est le **report
d'un état calculé**, non la lecture d'une mesure.

### 9bis.2 Ce que l'amendement porte

| Section | Apport |
|---|---|
| **§9.1 bis** | l'énoncé liminaire distingue **persistance de l'observation** et **provenance des mesures** |
| **§9.1 ter** *(nouveau)* | la reconstitution depuis l'historique enregistré est **admise sous quatre conditions cumulatives** : mesures réellement enregistrées de la même grandeur et de la même pièce, **aucune valeur fabriquée** ; **bornage par la fenêtre nominale**, faute de quoi ce serait un historique prohibé par le §2.2 ; **profondeur réellement disponible exposée** et critère non calculable tant qu'elle est insuffisante ; **aucun besoin restauré révoqué, aucun besoin créé** qu'une fenêtre remplie en fonctionnement n'aurait pas créé |
| **§12.3** | la non-conformité est **précisée** — c'est la persistance d'une **conclusion, d'une valeur de référence ou d'une évolution calculée** qui est prohibée — et une **nouvelle** est ajoutée : fenêtre reconstituée **au-delà de la fenêtre nominale**, ou remplie de **valeurs fabriquées** |

### 9bis.3 Ce que l'amendement ne fait pas

- il **n'autorise aucun historique** : la fenêtre nominale demeure la borne, et
  la dépasser reste prohibé par le §2.2 ;
- il **ne restitue ni instant, ni durée, ni pic, ni état antérieur** du besoin —
  le §2.2 n'est pas concerné ;
- il **n'affaiblit aucun invariant** du §9.1 bis : la condition 4 borne le risque
  de faux besoin, la fenêtre reconstituée étant **identique à celle qu'un
  fonctionnement continu aurait produite** ;
- il **ne calibre rien** ;
- il **ne rend obligatoire** aucune reconstitution : il l'**admet**.

> **La conformité de l'implémentation est ainsi établie par le contrat, et non
> par tolérance.** L'alternative aurait été de livrer un runtime dont une clause
> littérale du contrat interdit le fonctionnement — ce que la doctrine Arsenal
> proscrit : les contrats font autorité.

---

## 10. État des écarts contractuels

| # | Écart | État |
|---|---|---|
| 1 | verdict d'aération décisionnel | ✅ résorbé (L7.2) |
| 2 | frontières de libération non consommées | ✅ **résorbé** |
| 3 | aucun besoin hystérétique | ✅ **résorbé** |
| 4 | aucun état humidité par pièce | ✅ **résorbé** |
| 5 | restauration et indisponibilité | demeure — **L7.5** |
| 6 | intention divergente | ✅ résorbé (L7.1) |

> **Cinq écarts sur six sont résorbés.** Le dernier — restauration au
> redémarrage et maintien sur mesure inexploitable — est l'objet de **L7.5**,
> désormais le jalon actif.
