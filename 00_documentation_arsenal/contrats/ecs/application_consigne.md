# Contrat — `10_scripts/ecs/appliquer_consigne_bridge.yaml`

**Arsenal** | Domaine : ECS | Couche : Exécution  
**Version** : V1.1 | **Statut** : Validé  
**Auteur** : Arsenal Architecture | **Date** : 2026-09-05

> ### AMENDÉ — surface de commande portée sur l'écrivain souverain
>
> **Le statut du présent contrat est CONSERVÉ.** Deux points sont amendés :
> le **topic de commande** et le **jeu de champs publié** — voir « Ressources
> internes » et « Garanties ».
>
> **Tout le reste est repris intact** : rôle strictement exécutif, entrée unique
> `target_temp`, helper de corrélation, attente d'une conclusion ACK parmi
> `applied` / `rejected` / `timeout`, contrat de sortie, non-garanties,
> hypothèses d'exécution, dette documentaire V1. **Aucun `entity_id` n'est
> touché.**
>
> Référence : [`../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)

---

## Rôle

Script strictement exécutif.

Il ne décide rien. Il ne notifie rien. Il ne gère aucun état métier ECS global.

Il fait uniquement ceci :

1. recevoir une valeur cible ECS
2. générer une transaction boiler bridge
3. publier la commande MQTT
4. attendre une conclusion ACK
5. nettoyer le helper de corrélation
6. laisser le résultat exploitable par l'appelant

---

## Entrée

| Champ         | Type    | Obligatoire | Description              |
|---------------|---------|-------------|--------------------------|
| `target_temp` | numeric | oui         | Consigne ECS cible (°C)  |

Aucun autre paramètre en V1. Les champs `ack_timeout` et `ttl_seconds`
sont réservés pour une version ultérieure si le besoin se confirme.

---

## Ressources internes (en dur)

| Rôle                  | Identifiant                                  |
|-----------------------|----------------------------------------------|
| Helper de corrélation | `input_text.boiler_req_dhw_set_setpoint`     |
| Topic MQTT commande   | `<prefix>/command`                           |
| `role` publié         | `dhw_setpoint`                               |
| Topic MQTT ACK        | `<prefix>/ack/dhw_setpoint`                  |
| Capteur ACK           | `sensor.boiler_ack_dhw_set_setpoint_result`  |

Ces ressources sont fixes en V1. Ce script n'est pas un framework générique.

> **Le topic de commande n'est plus propre à l'ECS.** ~~`boiler/command/dhw/set_setpoint`~~
> est **PÉRIMÉ** : la surface cible expose **un topic de commande unique pour
> toute l'installation**, et c'est `role` qui identifie la consigne ECS.
>
> **`<prefix>` est la racine configurée côté écrivain souverain**, `boilerack` au
> dernier relevé, **à revérifier avant toute mutation**.
>
> **Les deux `entity_id` ci-dessus sont CONSERVÉS**, et ils portent toujours la
> forme `dhw_set_setpoint` : ils nomment la famille transactionnelle Arsenal, non
> le topic.

---

## Paramètres temporels (en dur, V1)

| Paramètre     | Valeur | Description                              |
|---------------|--------|------------------------------------------|
| TTL commande  | 30 s   | Durée de validité du message MQTT        |
| Attente ACK   | 20 s   | Délai maximum avant décision de timeout  |

> **RÉSERVE CONSERVÉE — HORS LOT.** Le script applique aujourd'hui **15 s** de
> TTL et **15 s** d'attente ACK, non 30 s et 20 s. **Le contrat et le runtime
> divergent déjà**, et cette divergence est **antérieure** au portage de la
> surface : elle ne lui doit rien et n'en découle pas.
>
> **Elle est consignée ici, et délibérément NON corrigée.** La trancher — aligner
> le contrat sur le runtime, ou l'inverse — est une décision propre, qui suppose
> de confronter le TTL au budget de confirmation de l'écrivain souverain. **Ce
> lot ne la prend pas.**

---

## Garanties

- reçoit `target_temp` comme seul paramètre d'entrée
- génère un `request_id` UUID à chaque exécution
- écrit le `request_id` dans `input_text.boiler_req_dhw_set_setpoint` **avant** publication
- publie sur `<prefix>/command` un payload de **six champs exactement** :
  `request_id`, `ts`, `expires_at`, `source`, `role`, `value` — le jeu est
  **clos**, un champ manquant comme un champ surnuméraire produisant un rejet
  `invalid_payload`
- utilise un TTL fixe de **30 s** et une fenêtre d'attente ACK de **20 s**
- attend une conclusion ACK parmi : `applied` / `rejected` / `timeout`
- tente le nettoyage du helper de requête en fin d'exécution, dans le flux nominal du script
- laisse le résultat lisible via `sensor.boiler_ack_dhw_set_setpoint_result`

---

## Non-garanties

- aucune garantie de succès applicatif
- aucune relance automatique
- aucune notification
- aucune gestion d'état métier ECS (`ecs_cycle_en_cours`, `ecs_target_temp_session`, etc.)
- aucune libération de verrou ECS
- aucune annulation de timer externe
- **aucune garantie de corrélation stricte en cas d'appels concurrents** — en V1,
  l'attente ACK repose sur le canal ACK existant ; la corrélation n'est fiable
  que si la chaîne ACK existante expose effectivement le request_id de manière exploitable
  est le seul émetteur actif sur cette commande au moment de l'exécution
- **aucune vérification V1 d'occupation préalable du helper** — si le helper
  contient déjà un `request_id` non résolu, le script écrase sans contrôle
- en cas d'environnement dégradé, un état transitoire incohérent peut subsister
  dans le helper ; la convergence reste à la charge de l'appelant ou d'un gardien

---

## Hypothèses d'exécution

> Ce script suppose un contexte d'appel **séquentiel et maîtrisé**.
>
> Il n'est **pas conçu pour une exécution concurrente** sur la même commande ECS.
> En V1, aucun mécanisme de verrouillage interne n'est implémenté.
>
> L'appelant est responsable de garantir l'unicité d'exécution en amont.

Contrainte YAML : `mode: single`

---

## Contrat de sortie

Le script ne retourne pas de valeur au sens classique.

Après exécution, l'appelant lit :
```yaml
sensor.boiler_ack_dhw_set_setpoint_result
```

et décide de la suite : poursuite de cycle, relance, notification, arrêt.
Toute logique conditionnelle post-ACK reste chez l'appelant.

---

## Ce que ce script peut remplacer

| Contexte d'appel                  | Remplaçable |
|-----------------------------------|-------------|
| Montée ECS dans `cycle.yaml`      | ✓           |
| Descente ECS dans `cycle.yaml`    | ✓           |
| Sortie mode panne ECS             | ✓           |
| Watchdog fin de cycle             | ✓           |
| Gardien post-prélèvement          | ✓           |
| Gardien hors cycle                | ✓           |
| Retries spécifiques métier        | ✗           |
| Notifications                     | ✗           |
| Nettoyages métier contextuels     | ✗           |
| Décisions d'arrêt ou de poursuite | ✗           |

---

## Dette documentaire V1

| Point                             | Statut    | Cible       |
|-----------------------------------|-----------|-------------|
| Corrélation stricte par request_id | Non garanti V1 | V2 si concurrence avérée |
| Vérification occupation helper    | Non implémentée V1 | V2 si besoin confirmé |
| Réentrance / verrouillage interne | Non implémentée V1 | V2 si besoin confirmé |
| `ack_timeout` paramétrable        | Réservé V1 | V2 si multi-contexte |