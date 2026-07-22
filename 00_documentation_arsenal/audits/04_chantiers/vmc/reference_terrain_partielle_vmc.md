# Référence terrain **partielle** VMC (C35 — Lot 5)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L5 — acquisition d'une référence *avant* changement** |
| **Statut** | **Référence terrain partielle établie.** **L5 n'est pas soldé** — le critère de clôture 5 de C35 n'est **pas** satisfait |
| **Nature** | Document de **synthèse métier et de qualification normative des faits**. Il ne calibre aucun paramètre, ne modifie aucun contrat, ne prescrit aucune correction runtime |
| **Frontière de propriété** | Arsenal **interprète** ; `arsenal-runtime` **acquiert, extrait et reproduit** ([`protocole_dispositif_preuve_vmc.md`](protocole_dispositif_preuve_vmc.md) §6) |
| **Preuve opérationnelle** | Dépôt `arsenal-runtime`, commit **`37a6bd69520be492d4377623d6eb64ff3ad82900`**, dossier `analyses/c35_l5_reference_20260722/` |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** — §2.2 bis, §4.4 bis, §9.1 bis, §14, §15. **Non modifié par ce lot** |

> **Ce document n'établit aucun comportement et ne calibre aucun paramètre.**
> Il consigne dans Arsenal ce que la campagne d'analyse a **démontré**, ce qu'elle
> a rendu **indicatif**, ce qu'elle laisse **non concluant**, et ce qui demeure
> **interdit de décision** à ce stade. La calibration relève de **L2b**,
> ordonnancé après L5 — **L2b n'est pas activé par ce lot**.

---

## 1. Objet et portée

L5 devait acquérir une référence terrain **avant** changement, afin que l'effet de
la révision soit mesurable en L8. Une campagne d'analyse a été conduite dans
`arsenal-runtime` sur un corpus historique de sauvegardes Home Assistant, puis
soumise à une **contre-analyse probatoire** qui a corrigé trois défauts
méthodologiques de la première passe.

Le résultat est une **référence terrain partielle** : une part des questions
posées à L5 reçoit une réponse robuste, une autre part n'en reçoit aucune.

**Ce document ne recopie ni script, ni sortie brute, ni empreinte, ni jeu de
données.** Ces artefacts appartiennent à `arsenal-runtime` et y sont versionnés,
scellés par un manifeste d'empreintes et reproductibles par une commande unique.

---

## 2. Corpus et méthode — acquis

| Élément | Valeur consignée |
|---|---|
| Bases Recorder exploitées | **38** |
| Période couverte | **29 décembre 2025 → 21 juillet 2026** |
| Couverture unique après déduplication | **≈ 202,6 jours** |
| Déduplication inter-bases | **démontrée** — plus d'une ligne brute sur deux était un doublon |
| Pondération temporelle | **nécessaire** — la fréquence de réémission des capteurs varie d'un facteur d'ordre 25 entre mois |
| Fuseau | **`Europe/Paris`** correctement appliqué, changements d'heure gérés |
| Provenance | **SHA-256 documentée** pour chaque base, dans `arsenal-runtime` |
| Reproductibilité | **chaîne reproductible** dans `arsenal-runtime`, vérifiée depuis un répertoire vide |

**Ce que la déduplication change.** Les sauvegardes se recouvrent largement : une
statistique calculée sans déduplication surpondère mécaniquement les mois les plus
richement sauvegardés. La clé de déduplication est justifiée sur le schéma réel du
Recorder, et non postulée.

**Ce que la pondération temporelle change.** Les capteurs émettent **sur
changement** : une médiane calculée par échantillons reflète autant le
comportement de réémission que l'état réel de la pièce. Toutes les conclusions
saisonnières consignées ici sont contrôlées par une distribution pondérée par le
temps réellement passé dans chaque état.

> **Correction d'un chiffre antérieur.** Le lot L4 (mergé en #512) a consigné
> « 199,6 jours de couverture » et « deux trous résiduels de 2,8 et 1,8 jours en
> février ». Ces valeurs ont été établies **avant déduplication**. Après
> déduplication, la couverture unique est de **≈ 202,6 jours** en 2 segments, avec
> **un seul** trou inter-bases de **1,57 jour**. Les deux séries de chiffres ne
> mesurent pas la même chose ; **celles du présent lot font foi** pour toute
> conclusion probatoire.

---

## 3. Faits démontrés

### 3.1 Dérive saisonnière de la ligne de base — **≈ 20 points**

La ligne de base d'humidité relative de la **salle de bain parents** dérive
d'**environ 20 points entre l'hiver et l'été**.

Ce fait est confirmé par **plusieurs contrôles indépendants** : sur les
échantillons uniques, sur la distribution pondérée par le temps, après exclusion
des épisodes d'humidité, et sous variation du paramètre méthodologique de
pondération. L'amplitude reste du même ordre dans tous les cas.

**Conséquence normative sur l'entrée :**

> Une **frontière absolue annuelle** ne conserve **pas** une signification uniforme
> au cours de l'année, et ne peut **pas, seule**, satisfaire toute la reconnaissance
> attendue. Elle peut néanmoins **rester candidate comme voie d'entrée forte** au
> sein d'une composition avec un critère dynamique.

Ce qui est écarté est donc le **niveau absolu annuel comme critère unique**, non
un seuil absolu élevé employé comme voie d'entrée forte dans une composition. **Le
choix de la composition appartient à L2b** et n'est pas préempté ici.

### 3.2 Limites instrumentales des capteurs

| Pièce | Constat consigné |
|---|---|
| **Salle de bain parents** | Finesse exploitable **limitée par la restitution** ; p99 des variations en période calme observé **autour de 1,8 point** dans le corpus analysé |
| **Séjour** | Variation calme **plus faible** que celle de la salle de bain parents |
| **Salle de bain enfants** | **Valeurs entières**, pas de quantification d'**un point** |

**Ces valeurs ne sont pas des largeurs de bande morte.** Elles décrivent ce que les
capteurs restituent, non ce que le contrat devra retenir. Le dimensionnement de la
bande morte relève de **L2b** et n'est pas acquis.

Conséquence structurelle à retenir : sur la salle de bain enfants, **toute bande
morte inférieure à un point serait inopérante par construction**, la restitution du
capteur ne descendant pas sous le point entier.

### 3.3 Trace déclarative de haute vitesse — recomptage

L'entité `input_boolean.vmc_haute_vitesse` est qualifiée, sans exception dans ce
document et dans tout document dérivé, comme :

> **Trace déclarative et historisée de l'état de commutation rapporté, non
> corroborée par la décision ni par les sorties relais historisées, et non
> assimilable à une preuve physique de débit.**

Après déduplication et retrait des périodes artificiellement prolongées par les
frontières de sauvegarde :

| Grandeur | Valeur |
|---|---|
| Transitions uniques | **779** |
| Périodes ON distinctes | **205** |
| Durée cumulée | **≈ 217,6 heures** |
| Épisodes d'humidité concernés | **22** épisodes présentant **au moins 60 minutes** de chevauchement pendant lesquelles la trace déclarative rapportait l'état haute vitesse |

Ces 22 épisodes ne sont **pas** des épisodes physiquement démontrés en haute
vitesse. Ils lèvent, **au niveau de la trace uniquement**, le constat antérieur
« aucune redescente observée en haute vitesse » — constat qui avait déjà été rendu
non bloquant par l'arbitrage distinguant **niveau** et **cinétique** (L3/L4).

---

## 4. Résultat indicatif — le séjour

**Énoncé retenu :**

> **Le corpus ne justifie pas actuellement de conférer au séjour un besoin humidité
> local autonome.**

Le séjour ne manifeste aucun épisode de forte amplitude, et la majorité de ses
montées suit temporellement celles des salles de bain.

**Ce qui n'est pas acté.** Le rattachement définitif du séjour à un objectif du
contrat **n'est pas prononcé par L5**. Cet énoncé supposerait un croisement avec la
hiérarchie d'objectifs du contrat que le corpus ne documente pas, et s'appuierait
sur la détection d'épisodes la moins robuste des trois pièces. **La décision
appartient à L2b.**

---

## 5. Résultat non concluant — comparaison basse / haute vitesse

> **La comparaison de l'efficacité relative entre basse et haute vitesse est
> `non concluante`.**

Motifs, tous constatés et non supposés :

1. **déséquilibre saisonnier** des groupes comparés ;
2. **faibles effectifs** dans certains groupes ;
3. **variables confondantes** connues et non neutralisables (saison, amplitude des
   épisodes, position des fenêtres non historisée, conditions extérieures) ;
4. **absence de retour physique** — aucune mesure de débit, de pression ni de
   courant moteur ;
5. **nature observationnelle** du corpus — l'activation de la haute vitesse n'est
   ni aléatoire ni indépendante des conditions, aucune identification causale n'est
   possible.

Le résultat brut agrégé, contradictoire en apparence, s'explique par un confondant
majeur ; il ne s'agit pas d'une mesure de l'effet de la haute vitesse.

**Aucune affirmation sur l'efficacité relative de la haute vitesse ne peut être
tirée de ce corpus.** Ce constat conforte l'arbitrage propriétaire ayant écarté la
cinétique du chemin critique.

---

## 6. Résultats qui demeurent non acquis

Restent **ouverts** à l'issue de ce lot, et ne peuvent être présumés par aucun
document dérivé :

- le **débit physique** en basse et en haute vitesse ;
- le **gain réel** basse → haute vitesse ;
- l'**effet causal** de la haute vitesse sur les cinétiques ;
- le **mécanisme de libération** ;
- la **frontière OFF** ;
- la **durée minimale d'exécution** ;
- le **périmètre définitif du séjour** ;
- la **formule et les paramètres** du critère dynamique ;
- la **largeur de bande morte** ;
- la **calibrabilité complète** avec les capteurs actuels.

---

## 7. Question contractuelle ouverte — la libération

La dérive saisonnière ne concerne pas seulement l'entrée : elle affecte aussi la
**signification d'une frontière de libération absolue**.

1. Une **frontière OFF annuelle fixe ne peut pas être reconduite** sans analyse
   complémentaire : la médiane hivernale observée place une telle frontière au
   cœur du régime ambiant de la pièce, ce qui change fortement sa signification,
   sa rapidité de libération et sa robustesse selon la saison.
2. Le corpus **ne valide pas** une **référence glissante** pour la libération.
3. Le **§2.2 bis** du contrat autorise actuellement la **fenêtre glissante bornée
   uniquement comme condition d'entrée**, et lui interdit de participer au maintien
   et à la libération.
4. Une **référence dynamique utilisée pour maintenir ou libérer** le besoin
   **nécessiterait un nouvel examen contractuel**.
5. Des **paramètres statiques saisonniers** ne sont **pas automatiquement**
   équivalents à une base glissante : ils doivent **eux aussi être qualifiés
   contractuellement** avant toute décision.

**Aucune de ces options n'est choisie dans ce lot.** Le contrat n'est pas modifié.
Si L2b retenait une base saisonnière ou une référence dynamique, le §2.2 bis et les
exigences d'explicabilité devraient être réexaminés **conjointement**, avant toute
implémentation.

---

## 8. Statut exact de L5

### 8.1 Partie L5 **acquise**

- **méthode et provenance** — déduplication justifiée, pondération temporelle,
  fuseau, empreintes et reproductibilité ;
- **dérive saisonnière** — ≈ 20 points, robuste à plusieurs contrôles ;
- **limites instrumentales** — finesse et quantification par pièce ;
- **recomptage et qualification de la trace déclarative** de haute vitesse ;
- **limites du corpus** — couverture réelle, trous, inégalités mensuelles.

### 8.2 Partie L5 **encore ouverte**

- **preuves physiques ou documentaires du débit** ;
- **corroboration décision → commande → relais** — toujours absente d'historique ;
- **mécanisme de libération** ;
- **éventuelle observation complémentaire** à définir ;
- **arbitrages nécessaires avant L2b**.

### 8.3 Ce que ce lot ne fait pas

Ce lot **ne solde pas L5**, **ne coche pas** le critère de clôture 5 de C35, **ne
déclare pas** la calibration possible, **ne déclare pas** la séquence probatoire
terminée et **n'active pas L2b**.

**Jalon actif : L5 demeure le jalon actif de C35**, désormais en partie servi. L4
est soldé depuis #512 et n'est pas rouvert ; L4 et L5 ne coexistent pas.

**Aucune correction runtime n'est autorisée** tant que la séquence probatoire et
L2b ne sont pas soldées.

---

## 9. Frontière de propriété et non-duplication

Conformément au [`protocole_dispositif_preuve_vmc.md`](protocole_dispositif_preuve_vmc.md) §6 :

| Propriétaire | Contenu |
|---|---|
| **Arsenal** (ce document) | synthèse métier, qualification normative des faits, conséquences pour le chantier, limites de décision, questions ouvertes |
| **`arsenal-runtime`** | bases et archives, scripts, déduplication, provenance, résultats canoniques, reproductibilité |

Ce document **ne contient** aucun script, aucune sortie brute, aucun fichier
tabulaire, aucun manifeste et aucune liste d'empreintes. La preuve opérationnelle
est intégralement portée par le commit **`37a6bd69520be492d4377623d6eb64ff3ad82900`**
du dépôt `arsenal-runtime`, dossier `analyses/c35_l5_reference_20260722/`, qui
contient la méthode, la provenance des 38 bases, les résultats canoniques scellés
par empreintes et la procédure de reproduction.

Les **archives sources ne sont pas versionnées** mais restent **indispensables à la
reproduction** : le corpus historique correspondant est irremplaçable, le Recorder
en fonctionnement ne conservant que 30 jours.

---

## 10. Ce que ce lot ne prétend pas établir

- que la référence terrain est complète — elle est **partielle** ;
- que la haute vitesse produit un effet physique mesurable — **non démontré** ;
- que les épisodes analysés correspondent à des douches ou des bains — la méthode
  retenue est statistique, **aucun épisode n'est étiqueté** ;
- que la cause physique de la dérive saisonnière est établie — elle ne l'est pas ;
- que les résultats se reproduiraient sur une autre année — le corpus n'en couvre
  qu'une, partiellement.
