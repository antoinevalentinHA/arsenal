# CONTRAT ARSENAL — ASPIRATEUR
## 14 — Entretien des consommables

**Version contrat :** v1.0
**Statut :** Normatif — **antérieur au runtime Maintenance**
**Objet :** Fixer le périmètre d'entretien, son échéance, la séquence de remise
à zéro, et l'**autorité exclusive** sur la seule primitive irréversible du
domaine.

> **Ce chapitre ne crée aucun objet.** Aucun helper, aucun script, aucune
> automation, aucun capteur dérivé, aucune notification, aucune carte. Il fixe
> ce que les lots `M1`, `M2` et `N1` devront respecter, et **ce qu'ils n'auront
> pas le droit de faire**.

**Origine.** Cadrage `cadrage_l2_maintenance_ui`, **V4 ratifiée** — décision
`D-44`. Les arbitrages rendus qui fondent ce chapitre sont `A-1` (seuil),
`A-2` (comportement à l'expiration), `A-6` (forme de l'acte contractuel),
`A-8` (routage des erreurs) et `A-14` (garde sur la primitive irréversible).

---

## 1. Périmètre — quatre postes, et quatre seulement

**Attestation :** [`../../audits/01_rapports/aspirateur/releve_entites_entretien.md`](../../audits/01_rapports/aspirateur/releve_entites_entretien.md).

| Poste | Capteur de mesure restante | Bouton de remise à zéro |
|---|---|---|
| **Filtre** | `sensor.roborock_q7_max_temps_restant_filtre` | `button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air` |
| **Brosse principale** | `sensor.roborock_q7_max_temps_restant_brosse_principale` | `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_principale` |
| **Brosse latérale** | `sensor.roborock_q7_max_temps_restant_brosse_laterale` | `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_laterale` |
| **Nettoyage des capteurs** | `sensor.roborock_q7_max_temps_restant_capteurs` | `button.roborock_q7_max_reinitialiser_le_consommable_du_capteur` |

**Plafonds**, constantes amont, **exprimés en heures** : brosse principale
**300 h** · brosse latérale **200 h** · filtre **150 h** · nettoyage des
capteurs **30 h**.

> **`ASP-INV-73` — périmètre fermé.** Le domaine reconnaît **exactement ces
> quatre postes**. Un cinquième poste, un poste manquant, un capteur ou un
> bouton autre que les huit entités ci-dessus est une **non-conformité**, et non
> une extension.
>
> **Le bac à poussière n'en fait pas partie** : c'est une fonction native
> autonome du couple robot/dock. Le filtre à charpie et la brosse de lavage du
> dock n'existent pas sur cet appareil.

### 1.1 Sémantique réellement observée — et ses deux gardes

| Propriété | Valeur observée |
|---|---|
| Grandeur | **temps restant**, décroissant |
| Unité native | **seconde** ; restituée en heures |
| Décroissance | **pendant le nettoyage seulement** |
| Plafond exposé par l'entité | **aucun** — il vit en constante amont |
| Seuil d'échéance natif | **aucun** — le seul repère natif serait zéro |
| Historisation | **aucune** — pas de `state_class` |

> **`ASP-INV-74` — l'indisponibilité n'est pas une valeur.** Si la donnée
> protocolaire du champ de travail est absente, le capteur devient
> **indisponible**. Cet état ne vaut **ni zéro**, **ni la dernière valeur
> connue**, **ni un état nominal**. `unknown` et `unavailable` ne sont
> **jamais** assimilés à une mesure.
>
> C'est l'application directe de `ASP-INV-45` au périmètre Maintenance.

---

## 2. Échéance — un seuil, un seul

> **`ASP-INV-75` — seuil unique à 10 %.** Un poste est **dû** lorsque son
> compteur restant est **inférieur ou égal à 10 %** de son plafond. **Le même
> seuil s'applique aux quatre postes**, sans exception ni pondération.

**Trois situations, jamais deux.**

| Situation | Condition |
|---|---|
| **dû** | restant **≤ 10 %** du plafond, sur une mesure **lisible** |
| **non dû** | restant **> 10 %** du plafond, sur une mesure **lisible** |
| **non évaluable** | la mesure est **indisponible** ou inconnue |

> **`ASP-INV-76` — aucun poste n'est déclaré dû sur une donnée absente.** Un
> capteur indisponible produit **non évaluable**, jamais **dû**, et jamais
> **non dû**. Convertir un trou d'information en « non dû » masquerait une
> échéance ; le convertir en « dû » inventerait une usure.

**Ce que le domaine ne fait pas.**

- **Aucune anticipation prédictive.** Le domaine ne projette pas une date
  d'échéance, ne calcule aucune tendance et n'extrapole aucun rythme d'usage.
  Le seuil se constate, il ne se prévoit pas.
- **Aucune mesure de rendement.** Le chapitre [`08`](08_etats_et_observation.md)
  §6 exclut les statistiques d'usage ; ce chapitre ne les rétablit pas.
- **Aucune historisation** n'est exigée.

> **La projection persistante d'un entretien dû relève du lot `N1`**, et ce
> chapitre ne l'implémente pas. Il en fixe seulement l'objet : voir §5.

---

## 3. Remise à zéro — geste opérateur, pression unique, confirmation observable

> **`ASP-INV-77` — une remise à zéro est un geste opérateur explicite.** Elle
> n'est **jamais** déclenchée par une échéance, par une automation, par un
> redémarrage, ni par aucune inférence du système. **Aucune remise à zéro
> automatique n'existe dans ce domaine.**

**Séquence normative, dans cet ordre :**

| # | Étape | Obligation |
|---|---|---|
| 1 | Déclaration opérateur | Le geste est **explicite** et porte sur **un poste** |
| 2 | Émission | **Une seule pression** sur le **bouton exact** du poste |
| 3 | Relecture | Observation de la postcondition pendant **30 s au plus** |
| 4 | Issue | **Confirmée**, ou **terminale non confirmée** |

> **`ASP-INV-78` — pression unique, sans réémission.** Une déclaration
> opérateur produit **exactement une** pression. **Aucun retry**, **aucun
> `repeat`**, **aucune boucle**, **aucune seconde pression automatique**, quelle
> que soit l'issue. La relance est un **geste opérateur**, jamais une initiative
> du système.

**La postcondition, et elle seule.** La confirmation exige l'observation d'une
**postcondition réellement observable** : la **remontée du compteur restant à
son plafond**. Elle est **documentée comme telle** dans le relevé d'attestation,
et son effet y est qualifié **prédit, non testé**.

> **`ASP-INV-79` — une pression n'est pas une confirmation.** L'horodatage du
> bouton atteste que la **pression** a eu lieu ; il n'atteste **rien** de son
> **effet**. Une confirmation qui se contenterait de l'horodatage serait une
> confirmation **fausse**, et elle est interdite.

### 3.1 À l'expiration de la fenêtre — issue terminale, et honnêteté

> **`ASP-INV-80` — l'absence de confirmation n'est pas une preuve d'échec.**
> Si la postcondition n'est pas observée dans la fenêtre :
>
> 1. l'issue est **terminale**, sous la valeur « remise à zéro non confirmée » ;
> 2. le poste **reste dû** ;
> 3. **aucune nouvelle pression** n'est émise ;
> 4. le système **ne conclut à aucune panne matérielle**.
>
> **Une nouvelle tentative exige une vérification opérateur, puis un nouveau
> geste manuel.** Elle n'est jamais automatique.

**Pourquoi ce comportement, et pas un autre.** Le délai de propagation vers
l'entité **n'a aucune borne supérieure démontrable** : la fenêtre borne
l'**attente**, jamais l'**interprétation**. Une fenêtre expirée sur une remise à
zéro réussie donnerait un **faux négatif** sur un acte irréversible ; conclure à
la panne donnerait un **faux positif**. Le contrat refuse les deux : il **dit
que la confirmation manque**, et rend la main.

### 3.2 Fenêtre de relecture — **30 s**

La fenêtre vaut **30 s**. Elle appartient aux **deux constantes temporelles du
domaine**, et n'en ajoute aucune.

> L'invariant `ASP-INV-69` **n'est pas amendé dans son ensemble de valeurs.**
> Le domaine
> compte toujours **deux constantes, et deux seulement** — 30 s et 60 s. Seule
> la **portée** de l'invariant s'étend au périmètre Maintenance.

---

## 4. Autorité sur la primitive irréversible

**La remise à zéro est la seule primitive irréversible du périmètre
Maintenance.** Aucune primitive de restauration n'existe : ce qui est remis à
zéro ne se défait pas.

> **`ASP-INV-81` — allowlist nominative fermée.** Le service `button.press` sur
> les **quatre boutons** du §1 n'est appelable que par **un seul objet** : le
> **script de déclaration d'entretien** du lot `M2`. Cette autorisation est
> **nominative** — un fichier, nommément désigné — et **fermée** : tout autre
> appelant est une non-conformité.
>
> **Sont explicitement interdits :**
>
> | Interdit | Portée |
> |---|---|
> | Appel depuis un **fichier Lovelace** ou un gabarit de carte | sans exception |
> | Appel depuis une **automation** | sans exception |
> | **Boucle**, `repeat`, retry, seconde pression | sans exception |
> | Appel **générique** — ciblage par `device_id`, `area_id`, `label_id`, ou nom de service templatisé | sans exception |
> | Pression de **plusieurs boutons** pour une même déclaration opérateur | sans exception |
> | Toute **autre primitive Roborock** au titre de ce chapitre | ce chapitre n'en autorise aucune |

> **`ASP-INV-82` — ce chapitre n'ouvre rien d'autre.** Il n'autorise **aucune**
> écriture vers l'appareil au-delà de `button.press` sur les quatre boutons
> nommés. L'écrivain unique de mission reste le moteur (`ASP-INV-31`), et ce
> chapitre ne l'amende pas.

**Ce que cette allowlist ferme, et qui était ouvert.** Avant ce chapitre, la
pression de bouton sur une entité native **échappait à tout contrôle** : le
balayage de l'écrivain unique ne refuse que les services `vacuum.*` et
`roborock.*`, et le contrôle Lovelace ne parcourt que les arbres de cartes. La
seule primitive irréversible du périmètre circulait donc **sans garde**. Elle
est désormais **gardée mécaniquement** — voir §6.

---

## 5. Notifications — ce que Maintenance produit, et ce qu'il ne produit pas

> **`ASP-INV-83` — trois objets distincts, jamais confondus.**
>
> | Objet | Nature | Canal |
> |---|---|---|
> | **Entretien dû** | état durable | **persistant** — projection du lot `N1` |
> | **Erreur robot ou dock** | événement, **pendant une mission** | **mobile** — lot `N1` |
> | **Cycle en cours** | état de mission | persistant de mission, hors périmètre de ce chapitre |
>
> Une notification d'entretien ne restitue **jamais** une erreur d'appareil, et
> une alerte d'erreur ne restitue **jamais** une échéance d'entretien.

**Routage des erreurs — arbitrage `A-8`, contractualisé ici.**

| Contexte | Ce qui est émis |
|---|---|
| **Pendant une mission Arsenal** | Une erreur robot **ou** une erreur de dock relève de la **notification mobile** |
| **Hors mission** | **Aucune notification ajoutée** — ni mobile, ni persistante |

> **`ASP-INV-84` — hors mission, le domaine n'ajoute aucune notification.**
> Les seules restitutions hors mission sont celles **qui existent déjà** :
> l'**état natif** de l'appareil et le **refus de lancement** produit par le
> moteur. Le domaine n'en crée aucune autre.
>
> **Ne pas notifier n'est pas ne pas restituer.** L'interface reste libre de
> rendre un état visible ; cet invariant porte sur les **notifications**.

**Les notifications persistantes Maintenance ne concernent que l'entretien.**
Un **entretien dû**, ou sa projection contractuelle. Rien d'autre.

> **Aucune notification n'est créée par ce chapitre.** Il en fixe l'objet et les
> interdits ; le lot `N1` les implémentera.

---

## 6. Ce que la CI garde — et à partir de quand

**Deux régimes, à ne pas confondre.**

| Régime | Ce qui est vérifiable |
|---|---|
| **Immédiat** — sur ce chapitre | Le périmètre à quatre postes et ses huit entités · le seuil unique de 10 % · les trois situations · la séquence de remise à zéro et sa fenêtre · l'allowlist et ses interdits · le routage `A-8` |
| **Différé** — à l'arrivée du runtime | Que le script `M2` presse **une seule fois** · qu'il relise avant de conclure · que les entités dérivées de `M1` distinguent les trois situations · que la projection de `N1` ne se déclenche que sur un entretien dû |

> **Ce chapitre ne prétend pas garder un runtime absent.** Les contrôles
> immédiats portent sur le **texte contractuel** ; les contrôles différés
> deviendront actifs **quand les fichiers existeront**, et pas avant. Un
> contrôle qui prétendrait aujourd'hui vérifier un gabarit inexistant serait un
> contrôle qui ment.

**Contrôles portés par le checker du domaine :** `ASP-CI-29` périmètre et
entités · `ASP-CI-30` échéance et honnêteté · `ASP-CI-31` primitive
irréversible et allowlist · `ASP-CI-32` séquence de remise à zéro ·
`ASP-CI-33` notifications et routage.

### 6.1 Verrou transitoire — portée exacte

> ### ✅ Verrou levé au lot `M2` — et par ce qui le remplace
>
> **Le lot `M2` est livré.** L'allowlist nomme désormais un fichier, et un
> seul : `10_scripts/aspirateur/declarer_entretien.yaml`.
>
> **Le desserrage n'est pas une modification de constante.** Il est
> **conditionné** : l'état du visiteur récursif **dérive d'un essai réel** —
> le parseur est confronté aux **six formes adverses** énumérées plus bas, et
> n'est déclaré complet que s'il les rattrape toutes. Une régression du
> parseur rabaisse le drapeau, et le verrou **se referme de lui-même** sur une
> allowlist devenue non vide. Le contrôle `ASP-CI-31` le prouve dans son
> auto-test, dans les deux sens.
>
> **Une autorisation dormante est refusée** : une allowlist qui nommerait un
> fichier inexistant échoue, plutôt que de couvrir par avance le jour où ce
> fichier apparaîtrait.
>
> Le texte ci-dessous **reste normatif** : il énonce ce que le desserrage
> exigeait, et ce que `M2` a effectivement livré.

> **`ASP-INV-85` — aucun desserrage prématuré.** L'allowlist de pression est
> **vide** en `M0`, et elle doit le rester. **Toute allowlist non vide lève une
> erreur de CI explicite** tant que le **verrou transitoire** reste actif.

**Ce que le verrou fait, dit sans exagération.**

> L'allowlist est **indesserrable par sa seule modification** : toute allowlist
> non vide **échoue** tant que le verrou transitoire reste actif. Son ouverture
> exige une **modification explicite du checker**, portant **simultanément** sur
> le verrou et sur le visiteur YAML ; cette modification constitue un
> **changement de frontière CI soumis à revue**.

> **Ce que le verrou ne fait pas.** Il **ne prouve pas** que le visiteur
> récursif existe, ni qu'il sera correct le jour où il existera. Il rend
> seulement le desserrage **visible** et **délibéré** — jamais accidentel.

**Pourquoi ce verrou, et pas une simple bonne intention.** Le détecteur de
pression de `M0` reconnaît la forme la plus courante ; il **ne couvre pas**
toutes les formes valides de Home Assistant. Autoriser un fichier aujourd'hui
reviendrait à exposer la seule primitive irréversible du domaine derrière un
parseur incomplet.

**Ce que le lot `M2` devra livrer pour remplacer ce verrou :**

| # | Obligation |
|---|---|
| 1 | **Parsing YAML** réel, jamais une expression régulière sur le texte |
| 2 | **Visite récursive** des mappings et des listes |
| 3 | Un **fichier hôte unique**, nommément désigné |
| 4 | Les **quatre boutons exacts**, et eux seuls |
| 5 | **Interdiction du ciblage par `device_id`** |
| 6 | **Interdiction de l'entité templatisée** |
| 7 | **Une pression unique**, sans boucle ni retry |

**Formes que ce parseur devra reconnaître**, et que celui de `M0` ne couvre
pas : le **flow mapping**, `tap_action: call-service`, le **scalaire replié**,
les **alias YAML**, le ciblage par `device_id`, et l'`entity_id` **templatisé**.

> **Exigence de dérivation, pour `M2`.** L'état du visiteur devra **dériver de
> son implémentation réelle**, et non d'un booléen déclaratif comme celui que
> `M0` emploie faute de mieux.

**Livré au lot `M2`, obligation par obligation.**

| # | Obligation | Ce que `M2` livre |
|---|---|---|
| 1 | Parsing YAML réel | Le document est **chargé**, jamais lu à l'expression régulière |
| 2 | Visite récursive | Mappings et listes, en profondeur, clés comprises |
| 3 | Fichier hôte unique | `10_scripts/aspirateur/declarer_entretien.yaml`, nommément |
| 4 | Les quatre boutons exacts | Confrontés à la table fermée du §1 |
| 5 | Interdiction du ciblage par `device_id` | Étendue à `area_id`, `label_id` et `floor_id` |
| 6 | Interdiction de l'entité templatisée | Refusée sur le slot `entity_id` |
| 7 | Une pression unique, sans boucle ni retry | `mode: single`, quatre branches, aucune répétition |

**Les six formes sont des cas d'essai, pas des exemples.** Le drapeau du
visiteur vaut vrai **si et seulement si** les six sont rattrapées.

### 6.2 Ce que ces gardes ne prouvent pas

| Limite | Portée exacte |
|---|---|
| **Les listes fermées d'entités et de boutons sont des constantes du checker** | Une modification volontaire de ces constantes **dans le même commit** peut déplacer la frontière CI. Elle doit donc être traitée comme une **modification normative du contrôle**, soumise à **revue explicite** |

> **Cette limite ne remet pas en cause ce que les gardes protègent.** Une
> modification **documentaire seule** — du chapitre ou du relevé — ou une
> modification **coordonnée des deux** reste refusée : les listes fermées vivent
> dans le checker, et les deux documents y sont confrontés **séparément**.
>
> Ce qui échappe à la garde, c'est la modification du **juge lui-même**. Aucun
> contrôle ne s'auto-protège de sa propre réécriture ; la parade est la revue,
> pas le code.

> ### Périmètre exact de `ASP-CI-31` — **énoncé, pas résumé**
>
> **Corrigé après audit.** Une rédaction antérieure disait « tout le YAML de
> configuration du dépôt ». **C'était plus large que le balayage réel.** Le
> périmètre est celui-ci, et il est explicite dans le checker :
>
> | Inclus | Détail |
> |---|---|
> | Fichiers de configuration de **racine** | `configuration.yaml`, `logbook.yaml`, `logger.yaml`, `recorder.yaml`, `utility_meter.yaml` |
> | Répertoires **numérotés** `NN_` | récursif |
> | `blueprints/` · `esphome/` · `custom_components/` · `zigbee2mqtt/` | récursif |
> | Extensions | **`.yaml` et `.yml`** |
> | Arbres **Lovelace** | `18_lovelace/`, `19_button_card_templates/` |
>
> | Exclu | Pourquoi |
> |---|---|
> | `00_documentation_arsenal/` | **Le présent chapitre y nomme les quatre boutons** : balayer la documentation ferait s'auto-déclencher la garde sur le contrat qu'elle protège |
> | `.github/` | Orchestration CI, pas de la configuration Home Assistant |
> | `scripts/` · `tools/` | Outillage, registres de checkers et **contre-exemples délibérés** de tests |
> | `.git/` | Internes du gestionnaire de versions |
>
> **C'est ce périmètre qui ferme le trou décrit au §4** — et pas un périmètre
> plus large qu'on affirmerait sans le balayer.

---

## 7. Restitution de l'issue — l'objet que `M2` crée

> **Ce chapitre ne créait aucun objet** (préambule). Le lot `M2` en crée
> **un**, et un seul : le porteur de l'issue terminale du §3, étape 4.

| Rôle | Ce qu'il porte |
|---|---|
| `‹issue_remise_a_zero›` | Le verdict de la **dernière déclaration achevée** : le poste concerné, et son issue |

> **Aucun identifiant n'est proposé ici**, pas plus pour ce rôle que pour les
> autres : l'invariant `ASP-INV-58` s'applique sans réserve. Son
> identifiant est **attribué par l'opérateur** au lot `M2` et inventorié au
> chapitre [`12`](12_identifiants_a_fournir.md) §2.4.

**Vocabulaire fermé, deux issues terminales par poste.** Le rôle porte, pour
chaque poste du périmètre, l'une des **deux issues** du §3 — celle qui
constate la confirmation, et celle qui constate qu'elle manque — et il nomme
le **poste concerné**. L'ensemble est **fermé**, **énuméré au runtime** et
**mécaniquement confronté**, comme l'exige `ASP-INV-70` pour le verdict de
mission. Ce chapitre n'en énumère aucune valeur.

> **Ce verdict ne décide rien**, et l'unicité d'écrivain posée par
> `ASP-INV-86` n'en fait pas une autorité. Il n'est lu ni par la
> projection du lot `M1`, ni par celle du lot `N1`. Il ne participe à aucune
> décision qu'un poste est dû, n'acquitte aucune notification, n'autorise ni
> n'interdit aucune remise à zéro, et **ne remplace jamais la relecture du
> compteur**. Il décrit une **exécution passée** ; l'état d'entretien reste
> produit par `M1`, et par lui seul, depuis les compteurs natifs.

**Aucune réconciliation au démarrage.** Ce rôle ne prétend pas représenter
l'état courant : un verdict restauré après redémarrage décrit toujours la
dernière déclaration achevée, ce qu'il est. Aucune automation n'est créée, et
aucun identifiant d'automation n'est requis par ce lot.

**Un refus n'écrit rien.** Les trois gardes d'entrée — poste hors périmètre,
mesure non évaluable, compteur déjà à son plafond — s'arrêtent **avant toute
pression**, donc avant toute exécution : le verdict conserve la dernière
déclaration réellement achevée.

---

## Renvois

- Relevé d'attestation des entités : [`../../audits/01_rapports/aspirateur/releve_entites_entretien.md`](../../audits/01_rapports/aspirateur/releve_entites_entretien.md)
- États et observation, exclusion des consommables : [`08_etats_et_observation.md`](08_etats_et_observation.md) §6
- Refus et diagnostics : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Identifiants à fournir : [`12_identifiants_a_fournir.md`](12_identifiants_a_fournir.md)
- Hors périmètre et questions ouvertes : [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)
- Index du domaine : [`README.md`](README.md)
