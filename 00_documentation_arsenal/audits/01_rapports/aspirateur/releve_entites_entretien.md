# Relevé des entités d'entretien — domaine Aspirateur

**Nature :** relevé factuel d'entités, **attestation de référence** du périmètre
Maintenance. Ce document ne décide rien et ne conçoit rien : il **atteste** que
huit entités natives existent, sous ces identifiants exacts, et rappelle les
quatre constantes amont qui leur donnent leur sens.

**Pourquoi ce document existe.** L'audit de faisabilité du domaine —
[`audit_faisabilite_roborock_q7_max.md`](audit_faisabilite_roborock_q7_max.md) —
atteste les entités de **mission** : état, erreurs, pièce courante, sélecteurs,
`vacuum`. Il **n'atteste aucune entité d'entretien** : le relevé Maintenance lui
est postérieur. Le chapitre contractuel
[`14_entretien.md`](../../../contrats/aspirateur/14_entretien.md) nomme ces
entités ; il lui faut donc une attestation, et c'est celle-ci.

---

## 1. Provenance — et ce qu'elle vaut

| Point | Valeur |
|---|---|
| Date du relevé d'instance | **2026-08-27** |
| Source **normative** | Cadrage `cadrage_l2_maintenance_ui`, **V4 ratifiée** (`D-44`, 2026-08-28), fichier `06_ENTITES_ENTRETIEN.md` §1 et §2 |
| Empreinte SHA-256 de cette source | `ebdce95ae884726e6608195f3c87c8e0c8c91ed20967e721c6ce423d15556c8c` |
| Source des **états relevés** | Même dossier, `05_DIAGNOSTICS_SANITISES.md` **§5** — « Entités de consommable — états relevés » |
| Source des **boutons** | Même fichier, **§6** — « Boutons de remise à zéro » |
| Source des **valeurs brutes** | Même fichier, **§3** — « Consommables — valeurs brutes du protocole » |
| Empreinte SHA-256 de `05_DIAGNOSTICS_SANITISES.md` | `87462fa9e3da4a8adc0df716344e538637a826e1ab087656c4af5b4e8697c9cd` |
| Recoupement | Chaque restant observé égale `plafond − travail cumulé` **à la seconde près** |

### 1.1 Trois régimes de preuve, à ne pas confondre — **précisé après audit**

| Ce qui est établi | Régime |
|---|---|
| **L'existence** des huit entités, sous ces identifiants exacts | **Relevé daté** du 2026-08-27, transcrit et sanitisé. C'est une **observation d'instance**, pas une preuve rejouable |
| **Les quatre plafonds** | **Corroborés** par les valeurs brutes du §3 : chaque restant égale `plafond − travail` à la seconde près, et celui de la brosse latérale exclut à lui seul trois des quatre constantes |
| **Un diagnostic terrain complet et rejouable** | **ABSENT.** Il n'existe pas, et ce document n'en tient pas lieu |

> **Ce document est une transcription sanitisée, pas une preuve terrain
> re-exécutable.** Rejouer le relevé exigerait un accès à l'instance et
> produirait d'autres valeurs — les compteurs décroissent. Ce qui est
> **reproductible**, c'est l'**arithmétique** du §4, à partir des valeurs
> citées ; ce qui ne l'est pas, c'est **l'observation elle-même**.

> **Ce document est une copie, et il le dit.** La source est le dossier de
> cadrage scellé ; ce relevé en extrait la **seule** table d'entités, pour la
> placer là où le checker du domaine cherche ses attestations —
> `audits/01_rapports/`. **En cas de divergence, la source scellée fait foi**, et
> son empreinte ci-dessus permet de la vérifier.
>
> **Ce que cette copie ne duplique pas.** Aucun seuil, aucune règle, aucune
> décision : le chapitre `14` est la seule autorité normative du périmètre
> Maintenance. Ce fichier ne porte que des **faits d'existence**.

---

## 2. Les quatre postes — entités natives attestées

| Poste | Capteur de mesure restante | Bouton de remise à zéro | Champ protocolaire |
|---|---|---|---|
| **Filtre** | `sensor.roborock_q7_max_temps_restant_filtre` | `button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air` | `filter_work_time` |
| **Brosse principale** | `sensor.roborock_q7_max_temps_restant_brosse_principale` | `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_principale` | `main_brush_work_time` |
| **Brosse latérale** | `sensor.roborock_q7_max_temps_restant_brosse_laterale` | `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_laterale` | `side_brush_work_time` |
| **Nettoyage des capteurs** | `sensor.roborock_q7_max_temps_restant_capteurs` | `button.roborock_q7_max_reinitialiser_le_consommable_du_capteur` | `sensor_dirty_time` |

**Quatre postes, quatre capteurs, quatre boutons. Ni plus, ni moins.**

**Attributs communs aux quatre capteurs**, relevés au registre d'entités :
`device_class: duration` · `entity_category: diagnostic` · unité native
**seconde** · unité restituée **heure** · **aucun `state_class`** · **aucun**
attribut de plafond ni d'échéance.

> **Conséquence directe.** Le plafond n'est **pas** exposé par l'entité : il vit
> **en amont**, en constante de bibliothèque (§3). Une échéance ne peut donc pas
> se lire sur l'entité seule ; elle se **calcule**.

---

## 3. Les quatre plafonds — constantes amont

| Poste | Constante amont | Secondes | **Heures** |
|---|---|---|---|
| Brosse principale | `MAIN_BRUSH_REPLACE_TIME` | 1 080 000 | **300 h** |
| Brosse latérale | `SIDE_BRUSH_REPLACE_TIME` | 720 000 | **200 h** |
| Filtre | `FILTER_REPLACE_TIME` | 540 000 | **150 h** |
| Nettoyage des capteurs | `SENSOR_DIRTY_REPLACE_TIME` | 108 000 | **30 h** |

`restant = plafond − temps de travail cumulé`, calculé **par la bibliothèque
amont**, avec une garde : si la donnée protocolaire du champ de travail est
absente, la propriété vaut une **valeur absente** et **le capteur devient
indisponible** — il ne vaut ni zéro, ni sa dernière valeur connue.

---

## 4. Recoupement du relevé — contrôle falsifiable

| Poste | Travail cumulé (s) | Plafond (s) | Restant calculé (s) | État d'entité (h) | Concordance |
|---|---|---|---|---|---|
| Brosse principale | 793 132 | 1 080 000 | 286 868 | 79,6855555555556 | **exacte** |
| Brosse latérale | 51 701 | 720 000 | 668 299 | 185,638611111111 | **exacte** |
| Filtre | 298 747 | 540 000 | 241 253 | 67,0147222222222 | **exacte** |
| Nettoyage des capteurs | 93 553 | 108 000 | 14 447 | 4,01305555555556 | **exacte** |

> **Pourquoi ce tableau falsifie.** Le restant de la brosse latérale vaut
> **668 299 s** : cette seule valeur **exclut** trois des quatre constantes du
> périmètre, et n'est compatible qu'avec 720 000. Une erreur d'attribution des
> plafonds serait immédiatement visible.

---

## 5. Ce qui n'est **pas** attesté ici

| Point | Statut |
|---|---|
| L'**effet** d'une pression de remise à zéro | **Prédit, non testé.** Les sources établissent l'envoi de la primitive et la relecture par la bibliothèque ; elles n'établissent **pas** que le micrologiciel remette le champ à zéro |
| Le **délai** de propagation vers l'entité | **Sans borne supérieure démontrable** ; le bouton natif ne force aucun rafraîchissement sur la voie V1 |
| Le **mode de connexion** de l'instance — local ou repli nuage | **Non relevé** |
| Un **seuil** d'entretien natif | **Aucun** : le constructeur n'en publie aucun ; le seul repère natif serait zéro |
| Les entités du **dock** — filtre à charpie, brosse de lavage | **Absentes** : boutons conditionnés à une capacité que cet appareil n'a pas |
| Le **bac à poussière** | **Hors périmètre** — fonction native autonome du couple robot/dock |

> **Aucune valeur d'instance postérieure au 2026-08-27 n'est promise ici.** Les
> quatre restants sont **datés** : ils décroissent pendant le nettoyage, et ce
> relevé n'est pas une mesure courante.

---

## Renvois

- Chapitre contractuel : [`14_entretien.md`](../../../contrats/aspirateur/14_entretien.md)
- Audit de faisabilité du domaine : [`audit_faisabilite_roborock_q7_max.md`](audit_faisabilite_roborock_q7_max.md)
- Cadrage source, ratifié : [`cadrage_l2_maintenance_ui`](../../02_conception/aspirateur/cadrage_l2_maintenance_ui/README.md)
- Index du domaine : [`../../../contrats/aspirateur/README.md`](../../../contrats/aspirateur/README.md)
