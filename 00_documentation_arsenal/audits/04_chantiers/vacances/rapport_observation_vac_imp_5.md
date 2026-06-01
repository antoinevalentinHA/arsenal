# Rapport d'observation — VAC-IMP-5 (désinfection au retour de vacances)

> **Statut :** rapport d'observation runtime — **risque requalifié**
> **Constat :** `VAC-IMP-5` (🟠) — désinfection-retour : dépendance d'ordonnancement non garantie
> **Domaine :** `ecs` / `vacances`
> **Chemin d'archivage :** `00_documentation_arsenal/audits/04_chantiers/vacances/rapport_observation_vac_imp_5.md`
> **État du dépôt à la rédaction :** `origin/main` = `08b745d`
> **Référence :** chantier `04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md` (protocole §5, hypothèses C1/C2)
> **Nature :** observation et analyse. **Aucune correction définitive n'est proposée** ; les options de §7 sont des hypothèses.

---

## 1. Rappel du constat VAC-IMP-5

Au retour de vacances, deux automations réagissent à la transition `input_select.mode_maison : Vacances → Normal` :
- `desinfection_retour_vacances` (`10250000000021`) — **condition** : `binary_sensor.ecs_desinfection_retour_vacances_autorisee == on` ; **action** : `delay 5 min` puis cycle de désinfection ECS ;
- `start_timer_ecs_desinfection` (`10090000000010`) — exécute `timer.cancel` sur `timer.vacances_longues_ecs` (durée 6 j) à la sortie.

Le capteur d'autorisation est défini par :
`idle` **et** `remaining == '0:00:00'` sur `timer.vacances_longues_ecs`.

Le constat initial postulait une **dépendance d'ordonnancement** : selon que l'annulation du timer précède ou suit la lecture de l'autorisation, la désinfection pourrait être omise. Le chantier avait posé deux hypothèses sur l'effet de `timer.cancel` :
- **C1 :** `remaining` repositionné sur la durée configurée (≠ `0:00:00`) ;
- **C2 :** `remaining` laissé à `0:00:00` (ou à sa dernière valeur).

---

## 2. Observations runtime (intégrées telles que rapportées)

**État initial**
- `timer.vacances_longues_ecs = idle` ; `remaining = None` ; `duration = 144:00:00` ; `finishes_at = None`
- `binary_sensor.ecs_desinfection_retour_vacances_autorisee = off`
- `input_select.mode_maison = Normal` ; `binary_sensor.vacances_actives = off`
- automations actives : `ecs_desinfection_fin_vacances`, `modes_vacances_gestion_ecs_desinfection`, `ecs_veille_desinfection`

**Test S5-D — `timer.start` (durée normale) puis `timer.cancel`**
- après `timer.start` : `active` ; `remaining = 144:00:00` ; capteur `off`
- après `timer.cancel` : `idle` ; `remaining = None` ; `finishes_at = None` ; capteur `off`

**Test timer court — `timer.start` (`duration: "00:00:10"`), attente de fin naturelle**
- après expiration naturelle : `idle` ; `remaining = None` ; `duration = 144:00:00` ; `finishes_at = None` ; capteur `off`

**Conclusion empirique rapportée**
- `remaining` vaut `None` après `timer.cancel` **et** après expiration naturelle ;
- le capteur d'autorisation **ne passe pas à `on`** après expiration naturelle ;
- la condition `remaining == '0:00:00'` semble **incapable de détecter la fin naturelle** du timer dans le runtime observé.

---

## 3. Confrontation des hypothèses C1 / C2 aux faits

| Hypothèse du chantier | Prédiction | Fait observé | Verdict |
|---|---|---|---|
| **C1** — `cancel` remet `remaining` à la durée | `remaining = 144:00:00` à l'état idle | `remaining = None` | **Infirmée** |
| **C2** — `cancel` laisse `remaining` à `0:00:00` | `remaining = '0:00:00'`, capteur possiblement `on` | `remaining = None`, capteur `off` | **Infirmée** |

**Constat dominant — un troisième comportement (C3) :** à l'état `idle`, le timer ne porte **aucune** valeur exploitable de `remaining` (`None`), **que la sortie soit une annulation ou une expiration naturelle**. Ni C1 ni C2 ne décrivent le runtime réel.

**Implication décisive :** le test « timer court → fin naturelle » **ne fait pas intervenir d'annulation ni de course d'ordonnancement**, et pourtant le capteur reste `off`. La détection de complétion est donc défaillante **indépendamment de tout ordonnancement**.

---

## 4. Qualification du risque : **REQUALIFIÉ**

- L'**hypothèse d'ordonnancement** (mécanisme opérant supposé du constat initial) est **infirmée comme cause** : même sans concurrence ni annulation (cas fin naturelle isolée), l'autorisation reste `off`.
- Un **défaut plus fondamental est confirmé** : la condition d'autorisation `remaining == '0:00:00'` n'est **jamais satisfaite** à l'état idle dans le runtime observé (`remaining = None`). Le capteur `binary_sensor.ecs_desinfection_retour_vacances_autorisee` paraît rester `off` dans tous les états observés (idle initial, actif, post-cancel, post-expiration).
- Conséquence fonctionnelle confirmée et **systématique** (non plus intermittente) : la désinfection-retour **n'est jamais autorisée** par ce chemin, y compris après une absence légitimement longue.
- Le risque n'est donc ni simplement « confirmé » tel que formulé, ni « infirmé » : il est **requalifié** — d'un *aléa d'ordonnancement intermittent* vers un *défaut structurel de détection de complétion* produisant un **faux négatif systématique**.

> Précision : l'ordonnancement entre les deux automations reste théoriquement non garanti, mais il est désormais **secondaire** : il n'est pas la cause du dysfonctionnement observé.

---

## 5. Impact métier probable

- **Chemin dédié inopérant (confirmé) :** l'automation de désinfection spécifique au retour d'une absence longue ne se déclenche pas via ce capteur. La mesure d'hygiène « renforcée au retour » est, en l'état, silencieusement absente.
- **Atténuation probable (à vérifier) :** une désinfection ECS **quotidienne indépendante** existe — `ecs_veille_desinfection` déclenche le cycle au passage `OFF → ON` de `binary_sensor.ecs_creneau_desinfection_en_cours`, sans lien avec le timer de vacances. Si ce créneau régulier couvre l'hygiène ECS, l'impact réel du chemin dédié manquant serait **faible** (perte d'une désinfection « de confort » au retour, non d'une protection sanitaire de base). **Cette substitution doit être vérifiée** avant de conclure sur la criticité.
- **Risque latent de gouvernance :** un mécanisme présent, actif (`on`) et **jamais effectif** constitue une dette de fiabilité (fausse impression de couverture) même si l'impact sanitaire est atténué.

---

## 6. Cause probable

La cause probable est un **défaut de conception de la détection de complétion**, et non une course d'ordonnancement :

- Le capteur infère « timer terminé » à partir d'un **attribut interrogé** (`remaining`) supposé valoir `'0:00:00'` à la complétion. Or le runtime observé expose `remaining = None` dès que le timer est `idle`. La comparaison `None == '0:00:00'` est toujours fausse → capteur structurellement `off`.
- De surcroît, l'état `idle` est atteint **de façon identique** par une **expiration naturelle** (légitime) et par une **annulation** (non légitime). L'état de repos du timer **ne porte donc aucune information** permettant de distinguer « a couru jusqu'au bout » de « a été annulé ».
- Le signal fiable de complétion naturelle est l'**événement `timer.finished`** de `timer.vacances_longues_ecs`, qui — vérifié au dépôt — **n'est consommé par aucune automation**. La logique actuelle repose sur un sondage d'attribut au lieu d'un événement.

---

## 7. Options de correction — **hypothèses uniquement**

> À considérer après une étape de réconciliation contractuelle (doctrine Arsenal : contrat avant runtime). Aucune n'est retenue ni définitive à ce stade.

1. **Capture événementielle de la complétion.** S'appuyer sur l'événement `timer.finished` (`timer.vacances_longues_ecs`) pour poser un état souverain dédié, lu au retour — plutôt que de sonder `remaining`.
2. **Mémorisation de la légitimité.** Un état souverain (p. ex. `input_boolean` « désinfection due ») posé à la complétion naturelle et consommé/réinitialisé au retour, **découplant** la décision du timer mutable et distinguant complétion vs annulation.
3. **Révision de la condition du capteur.** Adapter la condition si une autre source d'état (`finishes_at`, état distinct) s'avère fiable ; mais l'observation montre que `remaining` est `None` à l'idle, donc toute condition fondée sur `remaining` resterait fragile et dépendante de version HA.
4. **Orchestrateur.** Un script unique ordonnant lecture → décision → annulation supprimerait la concurrence résiduelle, mais **ne résout pas à lui seul** le problème de signal de complétion (à combiner avec 1 ou 2).

Chaque piste devra respecter les invariants Arsenal (écrivain souverain unique, idempotence, REJECT-not-clamp, contrat avant YAML) et faire l'objet d'un contrat avant tout patch runtime.

---

## 8. Statut

- **Risque :** requalifié — faux négatif **systématique** de la désinfection-retour, de cause structurelle (détection de complétion), l'ordonnancement étant secondaire.
- **Cause probable :** identifiée (sondage de `remaining` inopérant à l'idle ; absence de distinction complétion/annulation ; `timer.finished` inexploité).
- **Verdict :** **PRÊT À PLANIFIER UNE CORRECTION** — le défaut est reproductible et sa cause probable est cernée ; l'étape suivante est une **conception + réconciliation contractuelle** (pas un patch direct). Le chantier n'est **pas** « prêt à patcher » au sens runtime : les options de §7 restent des hypothèses à arbitrer.
- **Observations complémentaires recommandées (non bloquantes, en parallèle de la conception) :**
  1. comportement après **redémarrage HA** avec `restore: true` (état/`remaining` restaurés) ;
  2. **vérification de la substitution** par `ecs_veille_desinfection` (le créneau quotidien couvre-t-il effectivement l'hygiène ECS ?) pour figer la criticité métier ;
  3. confirmation que le capteur reste `off` dans **tous** les états (aucun état observé ne le passe à `on`).

Tant que la correction n'est pas conçue, contractualisée puis validée, le constat `VAC-IMP-5` **reste ouvert** et le **domaine Vacances n'est pas clôturé**.

---

*Rapport d'observation `VAC-IMP-5`. Établi en lecture seule du dépôt, sans patch, sans YAML, sans modification runtime. Distingue observation empirique, cause probable et hypothèses restantes ; aucune correction n'est proposée comme définitive.*
