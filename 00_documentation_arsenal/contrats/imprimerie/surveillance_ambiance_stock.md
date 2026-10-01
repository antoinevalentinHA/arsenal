# 🧠 ARSENAL — CONTRAT
## Imprimerie — Surveillance d'ambiance des stocks

**Version** : v1.0.1
**Domaine** : Imprimerie — mesure, surveillance et alerte de l'ambiance des zones de stockage
**Date** : 2026-09-30
**Statut** : normatif

---

## 1. Objet

Surveiller la température et l'humidité relative des deux zones de stockage
du site Imprimerie, et **alerter** lorsqu'une grandeur reste hors des
**conditions de stockage déclarées** pendant une durée critique continue.

| Zone | Nature | Température | Humidité relative |
|---|---|---|---|
| Stock carton | atelier climatisé | `sensor.temperature_stock_carton` | `sensor.humidite_relative_stock_carton` |
| Stock produits finis (PF) | mezzanine non climatisée | `sensor.temperature_stock_pf` | `sensor.humidite_relative_stock_pf` |

Les quatre sources sont des entités de l'intégration SwitchBot Cloud
(`group.switchbot_cloud_capteurs`). Aucune n'est définie ni modifiée par ce
domaine.

---

## 2. Rôle de Home Assistant — frontière opposable

> **SAS-1.** Home Assistant est ici un outil de **mesure**, de **surveillance**
> et d'**alerte**. Il est **hors du système qualité** de l'entreprise.

Il ne constitue **ni** un enregistrement qualité, **ni** une preuve, **ni** un
indicateur qualité, **ni** une démonstration de conformité. Aucun libellé,
commentaire, tableau de bord, carte, notification ou document de ce dépôt ne le
présente comme une « référence qualité », une « preuve », un outil de
« conformité » ou un « KPI » qualité. Vocabulaire admis : *surveillance
d'ambiance, mesure, conditions observées, alerte de dépassement, historique de
mesure*.

Toute validation éventuelle dans le système qualité est effectuée
**séparément, par l'opérateur humain**, hors de ce dépôt.

**Hors périmètre.** La chaleur ressentie par les personnes (mezzanine,
bureaux, postes de travail) relève d'un sujet santé-sécurité distinct, non
traité ici.

---

## 3. Paramètres — conditions de stockage déclarées

Paramètres **communs aux deux zones**, réglables par l'opérateur
([`06_input_selects/imprimerie/stock_surveillance_parametres.yaml`](../../../06_input_selects/imprimerie/stock_surveillance_parametres.yaml)) :

| Paramètre | Entité | Valeur de référence | Réglage possible |
|---|---|---|---|
| Température — seuil bas | `input_select.temperature_seuil_critique_bas_stock` | **10 °C** | 0 à 20 °C, pas de 1 |
| Température — seuil haut | `input_select.temperature_seuil_critique_haut_stock` | **35 °C** | 25 à 45 °C, pas de 1 |
| Humidité relative — seuil bas | `input_select.humidite_relative_seuil_critique_bas_stock` | **30 %** | 10 à 50 %, pas de 5 |
| Humidité relative — seuil haut | `input_select.humidite_relative_seuil_critique_haut_stock` | **80 %** | 60 à 95 %, pas de 5 |
| Durée critique hors plage | `input_select.duree_critique_hors_plage_stock` | **24 h** | 1 à 168 h |
| Durée critique d'indisponibilité | `input_select.duree_critique_indisponibilite_stock` | **2 h** | 1 à 24 h |

> **SAS-2 — Premier déploiement sûr.** Les paramètres sont des `input_select`
> **sans clé `initial`** (doctrine
> [`restauration_etat_helpers.md`](../../architecture/03_doctrines/restauration_etat_helpers.md), R01) :
> la valeur réglée est restaurée à chaque redémarrage. La **première option**
> de chaque liste est la valeur de référence : c'est la valeur native d'un
> `input_select` au tout premier démarrage (`options[0]` quand aucun état n'est
> restaurable). Aucune fenêtre ne place un seuil ou une durée à une valeur
> arbitraire. Patron « bootstrap ≠ fallback » de [`vmc.md`](../vmc.md) §16.4.
> L'ordre des options est donc **porteur** et ne doit pas être trié.
>
> Un `input_number` aurait démarré à son `min` (constat de
> [`11_automations/vmc/amorcage_parametres.yaml`](../../../11_automations/vmc/amorcage_parametres.yaml)) :
> écarté pour cette raison.

> **SAS-3 — Paramètre illisible ⇒ abstention.** Un seuil ou une durée non
> numérique n'a **aucune valeur de repli** : la voie se déclare
> `parametres_indisponibles` (seuils) ou l'entité de décision devient
> indisponible (durées). Aucune alarme, aucun retour n'est alors produit.
> Les plages de réglage des seuils bas et haut sont **disjointes** : un seuil
> bas ≥ seuil haut est impossible par construction.

> **SAS-4 — Seuils statistiques ≠ seuils critiques.** Les capteurs
> `sensor.*_seuil_bas_stock_*` / `sensor.*_seuil_haut_stock_*`
> (`12_template_sensors/statistiques/seuils_dynamiques/`) sont des repères
> statistiques de **coloration**. Ils ne sont **jamais** lus par la
> surveillance, ni transformés en seuils critiques.

Une valeur absente des listes s'ajoute par PR, avec revue des consommateurs.

---

## 4. Règles de décision

Une **voie** = une zone × une grandeur (4 voies réelles).

### 4.1 Situation courante

`sensor.<grandeur>_surveillance_<zone>` — décision pure, sans mémoire :

| État | Condition |
|---|---|
| `dans_plage` | valeur numérique valide, **bornes incluses** (10 ≤ T ≤ 35 ; 30 ≤ HR ≤ 80) |
| `hors_plage` | valeur numérique valide, strictement hors bornes |
| `mesure_invalide` | `unknown`, `unavailable`, valeur non numérique, capteur absent |
| `parametres_indisponibles` | seuil illisible (SAS-3) |

### 4.2 Dépassement et alarme

> **SAS-5 — Continuité stricte.** Un dépassement s'**ouvre** à la première
> valeur valide hors plage (début horodaté). Il se **ferme** à la première
> **vraie** valeur numérique revenue dans la plage : le compteur repart de
> zéro. Pas d'hystérésis ni de tolérance dans cette version. Un pic bref ne
> déclenche donc jamais l'alarme longue durée.

> **SAS-6 — Alarme.** L'alarme est déclenchée lorsque la situation est
> `hors_plage` **et** que *maintenant − début* ≥ durée critique
> (`binary_sensor.<grandeur>_depassement_prolonge_<zone>`). Une notification
> est émise **à l'entrée** en alarme (zone, grandeur, valeur mesurée, plage
> attendue, durée écoulée hors plage).

> **SAS-7 — Retour.** Une alarme n'est **soldée** que par une vraie valeur
> numérique revenue dans la plage ; une notification de retour est alors
> émise (zone, grandeur, valeur au retour, durée totale du dépassement). Un
> dépassement fermé **avant** l'alarme est clos sans notification.

> **SAS-8 — Indisponibilité pendant un dépassement.** Une mesure invalide :
> ne ferme pas le dépassement ; n'est **jamais** un retour dans la plage ; ne
> déclenche pas à elle seule l'alarme (la situation courante doit être
> `hors_plage`) ; conserve le début connu jusqu'à la prochaine valeur
> numérique valide. Si cette valeur est hors plage et que la durée critique
> est écoulée depuis le début connu, l'alarme est déclenchée à cet instant.
> L'indisponibilité elle-même fait l'objet d'une alerte technique distincte
> (§6).

### 4.3 Mémoire de dépassement

| Entité | Rôle |
|---|---|
| `input_select.<grandeur>_suivi_hors_plage_<zone>` | `aucun` / `depassement` / `alarme` — seule autorité « dépassement ouvert » |
| `input_datetime.<grandeur>_debut_hors_plage_<zone>` | début du dépassement (sens uniquement si suivi ≠ `aucun`) |

Écrivain unique : automation `10180000000007`
([`11_automations/imprimerie/stock/surveillance_conditions.yaml`](../../../11_automations/imprimerie/stock/surveillance_conditions.yaml)).

> **Pourquoi un sélecteur de suivi.** Un `input_datetime` neuf, sans `initial`,
> vaut « aujourd'hui 00:00 » dans le code Home Assistant (et non 1970) : il ne
> peut servir seul de sentinelle. Le sélecteur de suivi démarre à `aucun`
> (première option), ce qui rend l'horodatage inerte au premier déploiement.

---

## 5. Temps, redémarrage et modification de durée

Horloge de franchissement de seuil conforme à
[`gestion_du_temps.md`](../../architecture/03_doctrines/gestion_du_temps.md) §5 :
aucune minuterie figée ; la décision relit le début persistant et la durée à
chaque évaluation (`now()`, réévaluation chaque minute).

| Événement | Comportement |
|---|---|
| **Redémarrage complet** | Suivi et début restaurés (pas d'`initial`). Le temps écoulé est **recalculé** depuis le début connu : il est **conservé**. **Compromis :** la durée d'arrêt de Home Assistant est comptée comme hors plage ; la première valeur valide après redémarrage tranche (dans la plage ⇒ fermeture ; hors plage ⇒ poursuite). |
| **Rechargement des automatisations** | Aucune perte : l'état vit dans les helpers, pas dans l'automation. |
| **Rechargement des helpers** | Valeur conservée (Home Assistant met à jour la configuration en place). À confirmer terrain (§10). |
| **Durée critique modifiée en cours de dépassement** | La nouvelle durée s'applique **immédiatement** au temps déjà écoulé. Exemple : 10 h écoulées, 24 h → 12 h : alarme 2 h plus tard ; 24 h → 8 h : alarme à l'évaluation suivante (≤ 1 min). |
| **Durée augmentée alors qu'une alarme est active** | L'alarme **reste active** ; seul un vrai retour dans la plage la solde (SAS-7). |

Latence d'alarme : au plus une minute après l'échéance.

---

## 6. Indisponibilité des capteurs

> **SAS-9.** Une mesure non exploitable pendant la durée critique
> d'indisponibilité (2 h par défaut) est signalée comme **indisponibilité**,
> jamais comme situation saine, et jamais mélangée au dépassement des
> conditions de stockage.

`binary_sensor.<grandeur>_mesure_indisponible_<zone>` distingue strictement :

| Cas | Critère | Motif |
|---|---|---|
| `unknown` / `unavailable` / non numérique | durée **dans cet état** (`last_changed`) ≥ durée critique | `valeur_non_exploitable` |
| Absence réelle de nouvelle remontée | âge de `last_reported` ≥ durée critique | `aucune_remontee` |
| Valeur identique mais régulièrement remontée | `last_reported` récent | `nominale` — **jamais** une indisponibilité |
| Capteur absent de Home Assistant | — | `absente` |

`last_reported` est la référence de fraîcheur du dépôt
([`resilience_integrations.md`](../resilience_integrations.md) §2) ; l'axe est
applicable ici (écriture périodique du coordinateur cloud constatée,
`02_groups/integrations/switchbot.yaml`). `last_changed` n'est **jamais**
utilisé comme mesure de fraîcheur : seulement comme instant d'entrée dans un
état non exploitable, car le coordinateur réécrit `unavailable` à chaque cycle.

**Rapport au mécanisme existant.** La chaîne de résilience SwitchBot Cloud
relance l'intégration quand ses huit capteurs sont gelés ou tous
indisponibles : elle ne voit pas la perte d'**un** capteur. Le présent
mécanisme ne relance rien ; il signale par capteur. Pas de recouvrement.

Notifications (automation `10180000000008`) : entrée en indisponibilité ;
rétablissement **seulement** si une valeur numérique valide est revenue.
**Compromis :** au redémarrage de Home Assistant, le décompte des 2 h repart
de zéro, et une indisponibilité déjà notifiée n'est pas répétée.

---

## 7. Notifications

Canal mobile éphémère, destinataire parent 1, via `script.notification_envoyer`
(événements au sens de [`notifications.md`](../notifications.md) ; « alarme
déclenchée » y est un exemple normatif d'événement). Aucun persistant, aucun
indicateur ou état de synthèse ajouté au tableau de bord Stockage. Formatage
unique : [`10_scripts/imprimerie/stock_surveillance_notifier.yaml`](../../../10_scripts/imprimerie/stock_surveillance_notifier.yaml).

| Événement | Titre | Contenu minimal |
|---|---|---|
| Alarme | `📦 <Zone> – <Grandeur> hors plage` | zone, grandeur, valeur, plage attendue, durée écoulée |
| Retour | `📦 <Zone> – <Grandeur> dans la plage` | zone, grandeur, valeur au retour, durée totale |
| Indisponibilité | `📡 <Zone> – Mesure <grandeur> indisponible` | zone, motif, durée critique |
| Mesure rétablie | `📡 <Zone> – Mesure <grandeur> disponible` | zone, valeur |

---

## 8. ESSAI de la chaîne d'alarme

> **SAS-10.** L'essai éprouve la **chaîne réelle** — mêmes templates de
> décision, même automatisation écrivaine, même script de notification — sur
> une **voie distincte** `essai_stock`, sans simuler une mesure réelle.

- Déclenchement : `script.imprimerie_stock_essai_alarme`.
- Phase : `input_select.essai_alarme_stock` (`inactif` au premier démarrage).
- Valeur **simulée**, dérivée des seuils de production **lus, jamais
  écrits** : seuil haut + 1 °C (hors plage), absente (invalide), milieu de
  plage (retour).
- Durée d'essai **fixe de 2 min**, distincte de la durée de production, qui
  n'est ni lue ni abaissée.
- Trois vérifications : alarme après dépassement prolongé ; mesure invalide
  sans retour ; retour dans la plage. Puis bilan.
- **Marquage :** tout titre commence par `🧪 ESSAI –` (l'emoji de tête est
  exigé par le contrat notifications) et tout message commence par
  `ESSAI`. Aucune notification d'essai ne peut être confondue avec une
  alarme réelle.
- **Aucun capteur source** n'est lu ni écrit ; aucune entité d'essai n'a de
  `state_class` ni n'est historisée : les statistiques long terme ne sont pas
  affectées.
- **Aucun état résiduel :** en fin d'essai, phase `inactif` et suivi d'essai
  `aucun` ; en cas d'interruption, l'automation `10180000000007` applique la
  même remise à zéro à l'arrêt du script et au démarrage de Home Assistant.
  Seul subsiste l'horodatage du dernier début d'essai, inerte tant que le
  suivi vaut `aucun`.
- **Non couvert par l'essai :** l'alerte d'indisponibilité (§6), qui
  exigerait d'altérer un capteur réel.

---

## 9. Statistiques et conservation

La lecture annuelle repose sur les **statistiques horaires long terme** de
Home Assistant des quatre sources ; aucun indicateur supplémentaire n'est
créé.

- Les quatre sources sont historisées (`recorder.yaml`, Population A).
- Elles portent `state_class: measurement` (°C, %) **fixé par l'intégration**
  SwitchBot Cloud, invisible en YAML — à constater sur l'instance (§10).
- `purge_keep_days: 30` ne purge que les états bruts : la table des
  statistiques long terme n'est jamais purgée par le Recorder
  ([`01_recorder/contrat.md`](../../architecture/01_recorder/contrat.md) §Rétention).
- Aucune automatisation ni aucun script du dépôt n'appelle de service de
  purge ou de suppression de statistiques.
- `script.reset_stock_historique` n'écrit que des `input_text` (historique
  texte sur 4 semaines) et des `input_number` (min/max) : il **ne peut pas**
  toucher aux statistiques long terme. Il n'est pas modifié sur le fond.
- **Risques hors dépôt :** accepter une réparation Home Assistant proposant
  de supprimer des statistiques (changement d'unité ou de `state_class`) ;
  perte de la base (les statistiques long terme vivent dans la même base :
  leur pérennité dépend des sauvegardes).

Aucune entité créée par ce contrat n'est historisée ni ne produit de
statistiques.

---

## 10. Réserves et arbitrages

| Objet | Qualification | Propriétaire | Critère de levée |
|---|---|---|---|
| Durée critique de production (24 h) | Réglable ; valeur de référence non figée par l'exploitant | Opérateur | Décision de l'exploitant ; réglage de `duree_critique_hors_plage_stock` |
| Durée critique d'indisponibilité (2 h) | Arbitrée par l'opérateur le 2026-09-30 ; réglable | Opérateur | Retour d'expérience terrain |
| Comportement réel sur l'instance (alarme, retour, indisponibilité, redémarrage, rechargement des helpers) | Réserve **L5**, non bloquante | Opérateur | Essai terrain (§8) puis premier épisode réel observé |
| `state_class: measurement` effectif des quatre sources | Réserve **L5**, non bloquante | Opérateur | Constat sur l'instance (Outils de développement → Statistiques) |
| Temps d'arrêt de HA compté hors plage (§5) | Compromis assumé | Contrat | Révision contractuelle |
| Décompte d'indisponibilité remis à zéro au redémarrage (§6) | Compromis assumé | Contrat | Révision contractuelle |

---

## 11. Entités du domaine

- Paramètres : `input_select.{temperature,humidite_relative}_seuil_critique_{bas,haut}_stock`,
  `input_select.duree_critique_hors_plage_stock`,
  `input_select.duree_critique_indisponibilite_stock`.
- Décision : `sensor.<grandeur>_surveillance_<zone>`,
  `binary_sensor.<grandeur>_depassement_prolonge_<zone>`,
  `binary_sensor.<grandeur>_mesure_indisponible_<zone>`
  ([`12_template_sensors/imprimerie/stock/`](../../../12_template_sensors/imprimerie/stock/surveillance.yaml)).
- Mémoire : `input_select.<grandeur>_suivi_hors_plage_<zone>`,
  `input_datetime.<grandeur>_debut_hors_plage_<zone>`.
- Action : automations `10180000000007` et `10180000000008` ;
  `script.imprimerie_stock_surveillance_notifier` ;
  `script.imprimerie_stock_essai_alarme`.
- Essai : `input_select.essai_alarme_stock` et la voie `essai_stock`.

`<grandeur>` ∈ {`temperature`, `humidite_relative`} ;
`<zone>` ∈ {`stock_carton`, `stock_pf`} (+ `essai_stock` pour l'essai).

---

## 12. Invariants

- Aucun capteur source n'est écrit par ce domaine.
- Aucune valeur non numérique n'est un retour dans la plage.
- Une alarme n'est soldée que par une vraie mesure dans la plage.
- Aucun seuil statistique dynamique n'est lu.
- Aucune notification d'essai sans le marquage `ESSAI`.
- Home Assistant mesure, surveille et alerte ; il ne qualifie rien.

---

## Historique de version

- **v1.0** — création : seuils critiques réglables, alarme de dépassement
  prolongé, retour, indisponibilité par capteur, ESSAI.
- **v1.0.1** — correctif runtime, sans changement de règle. Le script de
  notification lisait des champs facultatifs (`valeur`, `duree_min`, `motif`,
  `detail`) que certains appelants ne transmettent pas. Or, pour Home
  Assistant, un champ non transmis est **indéfini**, et `| float(none)` /
  `| int(none)` ne protègent pas d'une variable indéfinie : le script échouait.
  Effets constatés : le bilan d'ESSAI n'était pas émis (premier essai
  terrain, alarme et retour d'ESSAI reçus conformes) ; par la même cause,
  l'alerte d'indisponibilité (§6) aurait échoué. Les champs facultatifs sont
  désormais normalisés en tête du script.

---

## Navigation

- [Contrats Imprimerie](README.md)
- [Hub de navigation du domaine](../../navigation/domaines/imprimerie.md)
