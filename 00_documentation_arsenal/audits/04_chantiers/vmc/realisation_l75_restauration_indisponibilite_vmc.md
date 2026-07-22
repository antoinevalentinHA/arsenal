# Réalisation L7.5 — restauration et indisponibilité (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.3 |
| **Lot** | **L7.5 — restauration et indisponibilité.** Résorbe le **dernier écart contractuel** |
| **Statut** | **Préparé sur branche** |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.3** — §4.4, §4.4 bis, §8.3, §9.1 cas 4, §10.2 exigences 8 et 10, §12.3. **Non modifié par ce lot** |
| **Preuve opérationnelle** | `arsenal-runtime`, commit **`704a056`**, dossier `analyses/c35_l75_cas4_20260722/` |

> **L'écart n° 5 est résorbé sur la prescription, PAS sur l'exposabilité.**
> Le §9.1 cas 4 est correctement **appliqué** ; le §10.2 exigence 10, qui impose
> de le rendre **exposable**, **ne l'est pas** — et ce lot démontre pourquoi
> plutôt que de le prétendre.

---

## 1. §9.1 cas 4 — prescription satisfaite, exposabilité impossible

### 1.1 Une détection avait été construite. Elle ne fonctionne pas.

Une première version détectait le cas 4 en testant si le porteur d'état vaut
`unknown` ou `unavailable` au démarrage, et allumait alors un indicateur.

**Cette détection supposait qu'un `input_boolean` sans état restaurable prenne
l'un de ces états. La supposition a été vérifiée — elle est fausse.**

Balayage des **38 bases**, en lecture seule (`704a056`) :

| Grandeur | Valeur |
|---|---|
| `input_boolean` observés | **18** |
| Lignes d'état | **21 964** |
| `off` / `on` | 13 564 / 8 400 |
| **`unknown`** | **0** |
| **`unavailable`** | **0** |

**Aucune occurrence, sur 21 964 lignes** — et parmi ces 18 helpers, certains ont
été **créés en cours de période**, donc sont nécessairement apparus **sans état
restaurable**.

**Réponses aux trois questions posées :**

| Question | Réponse |
|---|---|
| Absence réelle de restauration → `unknown`/`unavailable` ou déjà `off` ? | **déjà `off`** |
| Restauration valide → état déjà disponible avant l'exécution ? | **oui**, `on` ou `off` |
| Faux positif transitoire avant restauration ? | **la question ne se pose pas** : il n'y a **aucun positif**, ni vrai ni faux |

### 1.2 Ce qui a été retiré, et pourquoi

**Le mécanisme et son indicateur sont supprimés.**

> Un indicateur qui **ne se déclenche jamais** afficherait en permanence
> l'absence de reconstruction. **Ce serait une affirmation non fondée, pas une
> exposition** — et le remède serait pire que le mal : il donnerait l'impression
> que la situation est surveillée alors qu'elle ne l'est pas.

### 1.3 Ce qui demeure — et c'est l'essentiel

**Le comportement prescrit par le §9.1 cas 4 est acquis sans aucun mécanisme** :
un porteur à `off` **est déjà** un besoin initialisé inactif.

**C'est la prescription qui est satisfaite ; c'est l'exposabilité du §10.2
exigence 10 qui ne l'est pas.** Le point est **déclaré ouvert**, non contourné.

### 1.4 Voie non retenue

Un `input_select` dont la **première option** serait `inconnu` prendrait cette
valeur en l'absence d'état restaurable, rendant le cas 4 **détectable**.

**Elle n'est pas retenue**, pour deux motifs :

1. le §9.1 parle d'un **« état booléen minimal »** ; un porteur à trois valeurs
   n'en est plus un, et ouvre la porte à y loger davantage ;
2. **la même vérification n'a pas été faite sur `input_select`** — l'adopter sur
   la seule foi d'un raisonnement **reproduirait exactement l'erreur que ce lot
   corrige**.

**La CI garde l'absence** : réintroduire un indicateur de reconstruction sans
preuve de détectabilité fait échouer le checker.

---

## 2. §4.4 — maintien sur mesure inexploitable

**Le comportement était déjà correct ; il était subi, il devient construit.**

Depuis L7.4, une mesure inexploitable rend l'entrée **et** la libération
impossibles : le besoin actif demeure. C'était la bonne conséquence, mais elle
résultait de l'absence de branche plutôt que d'une intention lisible.

**Ce lot la rend explicite** : une variable `mesure_exploitable` est nommée dans
la machine, avec le motif contractuel en regard — le §12.3 range parmi les
non-conformités « la libération d'un besoin actif sur mesure inexploitable ».

> **La différence n'est pas cosmétique.** Un comportement correct par accident
> se perd à la première réécriture ; un comportement nommé et **gardé en CI**
> ne se perd pas.

---

## 3. §10.2 exigence 8 — maintenu n'est pas observé

Deux attributs sont ajoutés à chaque besoin, portant à trois les distinctions exposées :

| Attribut | Objet |
|---|---|
| `maintenu_faute_de_mesure` | §10.2 exigence 8, §4.4 cas 2 |
| `mesure_exploitable` | état de la mesure, distinct de l'état métier |
| `maintenu_faute_de_frontiere` | *(déjà présent depuis L7.4)* |

**Trois attributs, non quatre** : l'exposition de la reconstruction a été
retirée faute de détectabilité (§1).

> Le §10.2 exigence 8 le dit sans ambiguïté : un besoin **maintenu faute de
> mesure exploitable** et un besoin **observé** sont tous deux `actif`, « mais
> l'un repose sur une observation et l'autre sur l'absence de preuve de
> libération. **Les confondre dans l'exposition est une non-conformité** »
> (§12.3).

La `condition_maintien` nomme désormais le cas explicitement, avec sa référence.

---

## 4. Risque R4 — assumé, mais rendu visible

Le contrat impose de maintenir un besoin actif sur mesure inexploitable (§4.4)
et sur frontière non calculable (§7.4 bis condition 4). Le chantier a inscrit la
contrepartie en **risque R4** : sur panne durable, **la VMC peut demeurer en
haute vitesse sans dispositif de sortie**.

**Cette contrepartie reste assumée. Ce lot ne la lève pas — il la rend
visible.**

Une automatisation de diagnostic (`10190000000009`) publie une notification
persistante lorsque la situation dure **plus de deux heures**.

> **Ce n'est pas un dispositif de sortie.** Elle **ne libère rien**, **ne pilote
> rien**, **n'écrit aucun état de besoin**. Le §8.3 interdit qu'une durée tienne
> lieu de condition métier : c'est précisément pourquoi ce délai **n'agit pas
> sur la décision**. Il ne fait que **retarder un affichage**, afin qu'une
> indisponibilité passagère ne produise pas de bruit.

**Le délai de deux heures n'est pas calibré, et n'a pas à l'être** : il ne
gouverne aucune décision. Il sépare le transitoire du durable pour l'œil humain,
rien de plus. Le dire évite qu'il soit un jour lu comme un paramètre métier.

> **Pourquoi cela compte.** Une immobilisation silencieuse est **indiscernable
> d'un fonctionnement normal**. Un risque assumé qu'on ne peut pas constater
> n'est pas assumé : il est subi.

---

## 5. Garde CI — le §8.3 protégé par construction

Un **test 8** est ajouté à `check_vmc_contracts.py` :

| Contrôle | Objet |
|---|---|
| exposition | les trois situations d'indisponibilité sont exposées par chaque besoin |
| **cas 4** | **aucun indicateur de reconstruction n'est écrit** — la CI garde l'absence, faute de détectabilité prouvée |
| §4.4 | la machine rend l'exploitabilité de la mesure **explicite** |
| **§8.3** | **aucune durée (`for:`, `delay:`) dans la machine de besoin** |

> **Le dernier contrôle mérite d'être souligné.** Il interdit qu'un futur lot
> « règle » le risque R4 en ajoutant une temporisation de libération — la
> solution qui vient naturellement à l'esprit, et que le §8.3 proscrit. La garde
> rend la tentation **détectable**.

**Deux preuves négatives établies** : ajouter un `delay` dans la machine fait
échouer le checker ; réintroduire un indicateur de reconstruction aussi.

---

## 6. Contrôles exécutés

**86 checkers `arsenal_contracts` exécutés**, tous passent — dont les huit tests
du contrat VMC. Les cinq fichiers runtime sont **valides au parseur YAML**. Les
**gates documentaires** passent.

> **Deux échecs demeurent, ANTÉRIEURS** : `lovelace_no_inline_templating` et
> `vacances`. Ni causés, ni aggravés.

---

## 7. Ce que ce lot ne fait pas

- il **ne modifie pas `/config`** ;
- il **ne modifie pas le contrat** ;
- il **ne lève pas le risque R4** — il le rend constatable ;
- il **ne rend pas exposable le §9.1 cas 4** — il **démontre** que ce n'est pas
  possible avec ce porteur, et le déclare ;
- il **n'introduit aucun dispositif de sortie temporel**, et **interdit en CI**
  d'en introduire un dans la machine ;
- il **ne recalibre rien** ;
- il **n'expose aucun paramètre en UI** : **L7.7** ;
- il **ne clôt pas C35** — restent **L7.6** (composition et commande), **L7.7**
  (UI, intégrité et CI), puis **L8 à L10**.

---

## 8. État des écarts contractuels

| # | Écart | État |
|---|---|---|
| 1 | verdict d'aération décisionnel | ✅ résorbé (L7.2) |
| 2 | frontières de libération non consommées | ✅ résorbé (L7.4) |
| 3 | aucun besoin hystérétique | ✅ résorbé (L7.4) |
| 4 | aucun état humidité par pièce | ✅ résorbé (L7.4) |
| 5 | restauration et indisponibilité | ⚠️ **partiellement résorbé** — §9.1 cas 1 à 4 **appliqués**, §4.4 **construit et exposé** ; **§10.2 exigence 10 NON SERVIE**, le cas 4 n'étant pas détectable avec ce porteur |
| 6 | intention divergente (§11.2) | ✅ résorbé (L7.1) |

> **Cinq écarts sont pleinement résorbés ; le sixième l'est sur sa
> prescription, pas sur son exposabilité.** Le **critère de clôture 6 n'est
> donc pas entièrement satisfait** : il reste l'exposabilité du §9.1 cas 4,
> dont l'impossibilité est **démontrée et déclarée**, non contournée.
>
> **Deux issues, à arbitrer** : accepter cette limite et la consigner au
> contrat comme une exposabilité non servie, ou instruire le porteur
> `input_select` — avec la vérification que ce lot n'a pas faite.

**Prochain jalon : L7.6 — composition et commande.**
