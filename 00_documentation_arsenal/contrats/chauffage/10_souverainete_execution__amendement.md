# ==========================================================
# 🧠 ARSENAL — AMENDEMENT NORMATIF
#     CHAUFFAGE — SOUVERAINETÉ D'EXÉCUTION (V3 Pro)
#     Amendement CH-4 : topologie d'appel de la couche d'Application
# ==========================================================
#
# 📌 STATUT :
#   AMENDEMENT au contrat fondateur `10_souverainete_execution.md`
#   NIVEAU : structurant — gouvernance de la frontière d'exécution
#
# 🎯 OBJET :
#   Fermer doctrinalement l'ensemble des appelants légitimes de la
#   couche d'Application (`script.chauffage_appliquer_consigne`) :
#     1. énumérer les appelants autorisés ;
#     2. distinguer l'autorité décisionnelle des ré-applicateurs bornés ;
#     3. poser la clause de fermeture (numerus clausus) ;
#     4. renvoyer la mécanique transactionnelle MQTT au contrat boiler,
#        sans la redéfinir.
#
#   Cet amendement est le fondement normatif de l'invariant CI R-CALL-1.
#   Il ne produit aucun changement runtime.
#
# 🔒 AUTORITÉ :
#   Opposable à toute implémentation appelant la couche d'Application
#   chauffage (scripts, automatisations, mécanismes de reprise).
#
# ----------------------------------------------------------
# 🧱 SUBORDINATION
#
#   Subordonné à :
#     • 00_gouvernance_chauffage.md
#     • 10_souverainete_execution.md (contrat de base)
#
#   Cohérent avec :
#     • boiler/retry_transactionnel.md (mécanique MQTT, non dupliquée)
#     • 30_decision_centrale.md (autorité décisionnelle unique)
# ----------------------------------------------------------

---

## 1. Objet

Le contrat de base (`10_souverainete_execution.md`, §3.3) institue
`script.chauffage_appliquer_consigne` comme **couche d'Application** et interdit
tout accès matériel hors chaîne officielle. Il ne **nommait pas** les entités
autorisées à **invoquer** cette couche. Cet amendement comble cet angle mort
(dette D7) en fermant l'ensemble des appelants légitimes.

---

## 2. Modèle doctrinal des appelants

La couche d'Application admet exactement **deux natures** d'appelant :

- **Autorité décisionnelle** — produit une **décision thermique nouvelle** et
  l'applique. Une seule entité détient ce mandat.
- **Ré-applicateur borné** — **rejoue une décision déjà prise et mémorisée**,
  jamais une nouvelle. Mandat strictement limité à la ré-application.

> Les ré-applicateurs sont conformes à la souveraineté de la décision **dès lors
> qu'ils rejouent exclusivement une intention déjà décidée et mémorisée**. Ils ne
> disposent d'**aucun mandat de décision thermique autonome**.

---

## 3. Énumération fermée des appelants légitimes

Les seuls invocateurs autorisés de `script.chauffage_appliquer_consigne` sont :

<!-- R-CALL-1:ALLOWLIST:BEGIN -->
- `10_scripts/chauffage/decision_centrale.yaml`
- `11_automations/chauffage/retry_transactionnel/declenchement.yaml`
- `11_automations/chauffage/modification_consigne.yaml`
<!-- R-CALL-1:ALLOWLIST:END -->

Classification :

| Appelant | Nature | Mandat |
|---|---|---|
| `10_scripts/chauffage/decision_centrale.yaml` | Autorité décisionnelle | Décide le régime et l'applique (`raison = {{ reason }}`). |
| `11_automations/chauffage/retry_transactionnel/declenchement.yaml` | Ré-applicateur borné | Rejoue l'intention sessionnelle `input_select.chauffage_mode_session` (`raison = retry_transactionnel`). |
| `11_automations/chauffage/modification_consigne.yaml` | Ré-applicateur borné | Rejoue le mode actif `input_select.chauffage_dernier_mode_decide` sur modification de consigne (`raison = reapplication_consigne_*`). |

> Le bloc délimité par les sentinelles `R-CALL-1:ALLOWLIST` est la **source
> d'autorité** de l'invariant CI : la constante `APPELANTS_AUTORISES` de
> `tools/arsenal_ci/execution/r_call_1.py` en est le **miroir mécanique**, et un
> méta-test garde leur égalité.

---

## 4. Prédicat de ré-application (mandat borné)

Un ré-applicateur :

- rejoue **exclusivement** une intention **déjà décidée et mémorisée**
  (`input_select.chauffage_mode_session` ou `input_select.chauffage_dernier_mode_decide`) ;
- **n'émet jamais** de raison décisionnelle nouvelle (sa `raison` appartient au
  vocabulaire de ré-application) ;
- **n'écrit jamais** la mémoire de décision `input_select.chauffage_dernier_mode_decide` ;
- ne contient **aucune logique de décision** (présence, seuil, hystérésis, blocage).

> Portée de vérification : ce prédicat est **contractuel**. Il n'est **pas**
> vérifié par R-CALL-1 dans CH-4 (qui se limite à la **topologie d'appel**). Sa
> garde mécanique éventuelle relève d'un chantier ultérieur.

---

## 5. Clause de fermeture (numerus clausus)

> Tout invocateur de `script.chauffage_appliquer_consigne` **non énuméré au §3**
> constitue une **rupture de souveraineté d'exécution**.

L'ajout d'un appelant **exige un amendement explicite** de ce document (mise à
jour du bloc `R-CALL-1:ALLOWLIST`), **jamais** un simple ajout runtime. Le
**déplacement** d'un appelant contractualisé (changement de chemin de fichier)
est traité comme un retrait : il doit casser la CI et déclencher un amendement.

---

## 6. Renvoi anti-duplication (mécanique transactionnelle)

La **mécanique transactionnelle** des commandes (corrélation `request_id`,
ACK `applied`/`rejected`/`timeout`, plafond de tentatives, annulation si la
couche décision a relancé) reste **intégralement régie** par
`boiler/retry_transactionnel.md` (v1.0). Le présent amendement **ne la redéfinit
pas** et ne la duplique pas.

---

## 7. Garde mécanique — R-CALL-1

L'invariant CI **R-CALL-1** (`tools/arsenal_ci/execution/`) garde le **§3** :

- l'ensemble des fichiers portant un site d'appel de la cible ⊆ allow-list →
  sinon **violation bloquante** nommant le fichier fautif ;
- un appelant contractualisé sans site d'appel → **warning** de divergence
  contrat↔runtime.

R-CALL-1 est un analyseur **structurel** dédié, **distinct** de l'étage-1
(graphe template) et de l'étage-2 (cascade de décision). Il ne recouvre ni
`R-COV-1`, ni `R-MIRROR-1`, ni `R-CAUSE-1`, ni `R-ISO-1`.

---

## 8. Portée et stabilité

Amendement **fondateur** dans la gouvernance d'exécution, stable, versionné,
opposable à toute implémentation. Modifié uniquement lors d'une évolution
explicite de l'ensemble des appelants légitimes.
