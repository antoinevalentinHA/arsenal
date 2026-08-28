# Machine L2 — conduite et supervision — **V4**

> ### V4 — six arbitrages rendus s'appliquent à ce fichier
>
> `A-3` identifiants · `A-4` vocabulaire · `A-9` forme contractuelle ·
> `A-10` garde de geste et partition · `A-11` sérialisation, volets 1 et 2 ·
> `A-15` fenêtres de relecture.
> Registre des décisions : [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md).
>
> **Le vocabulaire est désormais arrêté : trente-quatre valeurs.** Les passages
> qui le donnaient en **matrice à quatre issues** sont **conservés et datés** —
> ils décrivaient exactement l'état de l'artefact tant que `A-10` et `A-11`
> n'étaient pas rendus. **Aucune analyse n'est supprimée.**

> **V3.1 — corrections `R-3` et `R-5` : deux renvois périmés au décompte, et la nomenclature du §6.2 qui rangeait une valeur hors vocabulaire en classe H.**

**Statut.** Les décisions D-01 à D-11 et D-R1 à D-R5 sont **acquises**.
Le vocabulaire est **arrêté en V4** à **trente-quatre valeurs** (§3.3 bis).
Jusqu'à la V3.2, il ne l'était pas : son contenu et son décompte dépendaient
**conjointement** des arbitrages **A-10** et **A-11 volet 2** — quatre issues
possibles, voir §3.3.

> **Corrections V2 :** L2 est un **acte contractuel** avant d'être un
> amendement de CI (§8, A-9) ; la disjonction des valeurs n'est **pas** une
> propriété de sûreté (§1, A-11) ; la définition de « mission ouverte » est
> unifiée (§5.1) ; la **partition** des valeurs est explicitée (§4) ; un refus
> de geste ne referme **jamais** une mission ouverte (§4.3, A-10) ; les chaînes
> de retour sont **distinguées** des autres états d'activité (§4.2, §6) ; la
> table de réconciliation est rendue **totale** et ne peut adopter aucune
> mission externe (§6) ; **quatre** automations (§7) ; prérequis de CI corrigés
> (§8).

> **Corrections V3 :** la clôture de la **chaîne de retour** n'a pas d'écrivain
> déterminé — la valeur concernée est **suspendue** et A-11 reçoit un second
> volet (§3.1, §5.2, §5.3, §5.4) ; les **fenêtres de relecture** des gestes ne
> sont ni spécifiées, ni couvertes, ni gardées — arbitrage **A-15** ouvert
> (§5.2, §8.2) ; l'atteignabilité n'est **pas** attribuée à un invariant (§8.4) ;
> la quatrième condition de `ASP-INV-62` est reprise (§5.2) ; `ASP-INV-52` est
> cité (§3) ; le nombre d'identifiants est **conditionnel à A-12** (§7) ; le
> piège de rédaction `ASP-CI-3` est signalé (§8.5) ; l'énoncé de totalité inclut
> le verdict **hors vocabulaire** (§6.1).

---

## 1. Disjonction des valeurs — ce qu'elle garantit, et ce qu'elle ne garantit pas

**Règle acquise (D-09, D-11).** La disjonction porte sur les **ensembles de
valeurs exactes**. Un préfixe peut être **partagé** — et deux le sont
effectivement :

| Préfixe | Writers qui le partagent |
|---|---|
| `ECHEC/` | W1 (transition non observée) et W3 (mission interrompue, erreur en mission) |
| `CLOTURE/` | W2 (clôtures de geste) et W3 (clôtures observées et opaques) |

C'est ce partage qui rend intenable une contrainte de préfixe exclusif, et
nécessaire la contrainte d'ensembles exacts.

> **Correction V2 — ce que la disjonction ne fait pas.**
> La V1 présentait cette propriété comme celle « qui rend la contrainte
> tenable ». **Elle ne protège en rien contre les courses entre writers.**
>
> Elle garantit qu'aucune valeur n'a deux auteurs. Elle ne **sérialise aucune
> écriture**. Deux writers peuvent parfaitement écrire l'un après l'autre, dans
> un ordre non maîtrisé, sur le même helper — voir §5.4.
>
> **Aucune garde de sérialisation n'est proposée ici. Arbitrage A-11.**

---

## 2. W1 — moteur de lancement (existant, inchangé)

`10_scripts/aspirateur/lancer_mission.yaml` — **dix-huit valeurs, inchangées.**

**Cycle de vie — 4**

```
VALIDATION_EN_COURS
COMMANDE/ISSUE_NON_ETABLIE
EMISSION/COMMANDE_ACCEPTEE
LANCEE/DEMARRAGE_OBSERVE
```

**Refus avant émission — 13 codes du catalogue**

```
REFUS/SELECTION_VIDE            REFUS/SEGMENT_INCONNU
REFUS/SELECTION_MULTI_CARTE     REFUS/CARTE_NON_CONFIRMEE
REFUS/PROFIL_INCONNU            REFUS/PASSAGES_HORS_CONTRAT
REFUS/PREREQUIS_MATERIEL_ABSENT REFUS/ROBOT_INDISPONIBLE
REFUS/ETAT_NON_QUALIFIE         REFUS/ERREUR_EQUIPEMENT
REFUS/MISSION_DEJA_OUVERTE      REFUS/SESSION_INACHEVEE
REFUS/REGLAGE_NON_CONFIRME
```

**Échec après émission — 1 code du catalogue**

```
ECHEC/TRANSITION_NON_OBSERVEE
```

---

## 3. W2 et W3 — valeurs proposées

> ### ⚠ Section rendue caduque par la V4 — conservée pour l'historique
>
> **Les §3.1, §3.2 et §3.3 décrivent l'état de la proposition jusqu'à la V3.2**,
> lorsque le vocabulaire n'était pas arrêté. **Le vocabulaire arrêté est au
> §3.3 bis.** Rien n'est supprimé ici : c'est cette analyse qui a rendu
> l'arbitrage possible.

> **Aucune dénomination ci-dessous n'est arrêtée**, hors les quatre valeurs
> acquises. Le champ lexical est contraint par `ASP-INV-70` : une valeur de
> cycle de vie **ne peut pas se nommer comme un refus**. Arbitrage **A-4**.
>
> **Aucune de ces valeurs n'entre au catalogue** ([`09`](.)) : `ASP-INV-52`,
> qui gouverne l'extension du catalogue et impose catalogue + chapitre porteur +
> changelog, **n'est donc pas déclenché**. La seule voie qui le déclencherait —
> faire entrer une valeur au catalogue — est identifiée en A-4, **avec son coût
> exact**, y compris la casse de l'ancre « 18 codes » de `ASP-CI-19`.

### 3.1 W2 — conduite

Fichier pressenti : `10_scripts/aspirateur/conduire_mission.yaml`

| Valeur | Classe (§4) | Origine |
|---|---|---|
| `CONDUITE/PAUSE_CONFIRMEE` | **O** | proposé |
| `CONDUITE/PAUSE_NON_CONFIRMEE` | **O** | proposé |
| `CONDUITE/REPRISE_CONFIRMEE` | **O** | proposé |
| `CONDUITE/REPRISE_NON_CONFIRMEE` | **O** | proposé |
| `CONDUITE/RETOUR_ENGAGE` | **O-R** | proposé — **ajouté en V2**, voir §4.2 |
| `CLOTURE/APRES_ARRET_CONFIRME` | **T** | proposé |
| **`CLOTURE/APRES_ARRET_NON_CONFIRME`** | **T** | **acquis — D-10** |
| `CLOTURE/APRES_RETOUR_CONFIRME` | **T** | proposé — **écrivain non déterminé, valeur SUSPENDUE : A-11 volet 2** |
| **`CLOTURE/APRES_RETOUR_NON_CONFIRME`** | **T** | **acquis — D-10** |

**Neuf valeurs**, plus **deux** si l'arbitrage A-10 retient la voie O2 (§4.3),
**moins une** si l'arbitrage A-11 volet 2 retire la clôture de retour confirmée
faute d'écrivain (§5.3).

> **N-2 — la clôture de la chaîne de retour n'a pas d'écrivain déterminé.**
> Trois énoncés de la V2 ne se recouvraient pas : cette valeur était placée chez
> W2 ; un retour confirmé « passait en O-R puis clôturait à l'amarrage » ; et
> l'amarrage était attribué à W3 sous une clôture nominale.
>
> **Les deux lectures échouaient.** Ou bien la valeur n'est **jamais écrite** —
> et l'exigence mécanique d'atteignabilité en fait un échec de CI immédiat, tout
> en falsifiant le décompte. Ou bien **deux writers sont candidats au même
> événement physique**, sans règle de priorité : une seconde course, sur le
> geste que le domaine qualifie lui-même de **seul geste à traîne longue**.
>
> **La V3 ne tranche pas.** La valeur est **suspendue** et le cas est porté à
> **A-11 volet 2**.

### 3.2 W3 — supervision, automation `10280000000001`

| Valeur | Classe | Origine |
|---|---|---|
| **`ECHEC/MISSION_INTERROMPUE`** | **T** | **acquis — D-11, catalogue `09`** |
| **`ECHEC/ERREUR_EN_MISSION`** | **T** | **acquis — D-11, catalogue `09`** |
| `CLOTURE/FIN_NOMINALE` | **T** | proposé |
| `CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE` | **T** | proposé |

### 3.3 Décompte — **non arrêté**

> ### ⚠ Passage caduc — conservé pour l'historique, annoté en V4
>
> **Le décompte est arrêté depuis la V4 : il vaut 34** (§3.3 bis). Le titre et
> la matrice ci-dessous décrivent l'état de la proposition **jusqu'à la V3.2**,
> lorsque `A-10` et `A-11` volet 2 n'étaient pas rendus.
>
> **Le passage n'est ni supprimé ni réécrit** : c'est cette matrice qui rendait
> l'arbitrage possible, et son écart avec le résultat rendu est lui-même
> instructif — l'arbitrage a **ajouté une dimension** que la matrice ne portait
> pas. **L'autorité courante est le §3.3 bis.**

Le total dépend désormais de **deux** arbitrages, et non plus d'un seul.

| A-10 | A-11 volet 2 | W1 | W2 | W3 | **Total** | Catalogue présents / absents | Cycle de vie |
|---|---|---|---|---|---|---|---|
| **O1** | clôture de retour **conservée** | 18 | 9 | 4 | **31** | 16 / 2 | 15 |
| **O1** | clôture de retour **retirée** | 18 | 8 | 4 | **30** | 16 / 2 | 14 |
| **O2** | clôture de retour **conservée** | 18 | 11 | 4 | **33** | 16 / 2 | 17 |
| **O2** | clôture de retour **retirée** | 18 | 10 | 4 | **32** | 16 / 2 | 16 |

> **Le décompte n'est arrêté par aucune de ces lignes.** Il le sera lorsque
> **A-10** et **A-11 volet 2** auront été rendus, et pas avant.

*(Énoncé d'origine, exact jusqu'à la V3.2. Rendu caduc en V4 : voir l'encadré
en tête de section et le §3.3 bis.)*

### 3.3 bis Vocabulaire **arrêté** — rendu en V4

> **Trente-quatre valeurs**, et trente-quatre seulement.

| Writer | Nombre | Fichier porteur |
|---|---|---|
| **W1** — moteur de lancement, inchangé | **18** | `10_scripts/aspirateur/lancer_mission.yaml` |
| **W2** — conduite | **11** | script de conduite, lot `L2` |
| **W3** — supervision, `10280000000001` | **5** | automation de supervision, lot `L2` |
| | **34** | |

**W2 — les onze valeurs**

| Valeur | Classe | Origine |
|---|---|---|
| `CONDUITE/PAUSE_ENGAGEE` | **O** | **ajoutée en V4** — engagement exigé par `A-11` |
| `CONDUITE/PAUSE_CONFIRMEE` | **O** | proposée en V2, retenue |
| `CONDUITE/PAUSE_NON_CONFIRMEE` | **O** | proposée en V2, retenue |
| `CONDUITE/REPRISE_ENGAGEE` | **O** | **ajoutée en V4** — engagement exigé par `A-11` |
| `CONDUITE/REPRISE_CONFIRMEE` | **O** | proposée en V2, retenue |
| `CONDUITE/REPRISE_NON_CONFIRMEE` | **O** | proposée en V2, retenue |
| `CONDUITE/ARRET_ENGAGE` | **O** | **ajoutée en V4** — engagement exigé par `A-11` |
| `CLOTURE/APRES_ARRET_CONFIRME` | **T** | proposée en V2, retenue |
| `CLOTURE/APRES_ARRET_NON_CONFIRME` | **T** | **acquise — D-10** |
| `CONDUITE/RETOUR_ENGAGE` | **O-R** | proposée en V2, retenue |
| `CLOTURE/APRES_RETOUR_NON_CONFIRME` | **T** | **acquise — D-10** |

**W3 — les cinq valeurs**

| Valeur | Classe | Origine |
|---|---|---|
| `ECHEC/MISSION_INTERROMPUE` | **T** | acquise — `D-11`, catalogue `09` |
| `ECHEC/ERREUR_EN_MISSION` | **T** | acquise — `D-11`, catalogue `09` |
| `CLOTURE/FIN_NOMINALE` | **T** | proposée en V2, retenue |
| `CLOTURE/APRES_RETOUR_CONFIRME` | **T** | **déplacée en V4 de W2 vers W3** — `A-11` volet 2 |
| `CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE` | **T** | proposée en V2, retenue |

> **Pourquoi 34, alors que la matrice du §3.3 plafonnait à 33.** L'arbitrage
> rendu a **ajouté une dimension** que la matrice ne portait pas — les **trois
> valeurs d'engagement** exigées par `A-11` — et il a **déplacé** la clôture de
> retour confirmée vers W3 **au lieu de la retirer**. La matrice n'était pas
> fausse : elle était exhaustive sur les seules issues d'`A-10` × `A-11` volet 2.
>
> **9 + 3 − 1 = 11** pour W2 ; **4 + 1 = 5** pour W3 ; **18 + 11 + 5 = 34.**

**Vérifications faites sur ce vocabulaire :**

| Contrôle | Résultat |
|---|---|
| Disjonction W1 ∩ W2, W1 ∩ W3, W2 ∩ W3 (`D-09`) | **vide** dans les trois cas |
| Préfixes partagés admis (`D-09`) | `ECHEC/` par W1 et W3 ; `CLOTURE/` par W2 et W3 |
| `D-10` — deux clôtures non confirmées, distinctes et terminales | présentes, distinctes, toutes deux de classe **T** |
| `D-11` — codes du catalogue conservés tels quels | les quatre codes nommés sont présents à l'identique |
| `ASP-INV-70` — aucune valeur de cycle de vie ne se nomme comme un refus | **aucune** des seize valeurs nouvelles ne porte `REFUS` |
| `ASP-INV-52` — extension du catalogue | **non déclenché** : aucune valeur nouvelle n'y entre |
| Ancre « 18 codes » de `ASP-CI-19` | **intacte** |

**Répartition à écrire dans l'en-tête du fichier L1 — désormais calculable :**

| Grandeur | Valeur | Calcul |
|---|---|---|
| Codes du catalogue **présents** | **16** | 14 écrits par W1 + les deux codes d'échec écrits par W3 |
| Codes du catalogue **absents** | **2** | commande rejetée et canal indisponible — **inchangé** |
| Valeurs de **cycle de vie** | **18** | 34 − 16 |
| **Total** | **34** | |

**Les deux codes sans écrivain restent les mêmes**, et pour les mêmes raisons :
le code de canal indisponible appartient à l'**appelant** ; celui de commande
rejetée est **structurellement** hors de portée.

**Deux codes du catalogue restent délibérément sans écrivain**, inchangé :
le code de canal indisponible, qui appartient à l'**appelant** ; et le code de
commande rejetée, **structurellement** hors de portée.

> **Conséquence directe sur un fichier L1.** L'en-tête de
> `04_input_texts/aspirateur/mission.yaml` porte aujourd'hui la répartition
> « 14 présents · 4 absents · 4 valeurs de cycle de vie », et `ASP-CI-18`
> **confronte mécaniquement ce texte** au vocabulaire.
>
> La nouvelle répartition sera **16 présents · 2 absents**, et **14, 15, 16 ou
> 17 valeurs de cycle de vie** selon la matrice ci-dessus — pour un total de
> **30, 31, 32 ou 33**.
>
> **Elle ne peut être écrite qu'après `A-10` ET `A-11` volet 2.** Restreindre
> cette répartition à « 15 ou 17 » présumerait que le volet 2 se rend en faveur
> du **maintien** de la valeur disputée : ce serait un rétrécissement implicite
> de l'arbitrage que ce chapitre vient d'ouvrir.

---

## 4. Partition des valeurs — **ajoutée en V2**

> La V1 fondait toute sa table de réconciliation sur une distinction
> terminal / non terminal **qu'aucune section n'énonçait**. La voici.

### 4.1 Trois classes, exhaustives et disjointes

| Classe | Signification | Effet sur la mission Arsenal |
|---|---|---|
| **O** | **Mission Arsenal ouverte** | La mission est ouverte et reprenable ; la supervision s'applique ; la persistante de cycle est projetée |
| **T** | **Issue terminale de mission** | La mission est close ; la supervision cesse ; la persistante est supprimée |
| **H** | **Hors mission** | Aucune mission n'est ouverte **et** aucune n'est close par cette valeur : le verdict décrit une étape de lancement ou un refus |

**Répartition des dix-huit valeurs existantes :**

| Classe | Valeurs |
|---|---|
| **O** | `LANCEE/DEMARRAGE_OBSERVE` — **une seule** |
| **T** | *aucune* |
| **H** | les **13** refus, plus `VALIDATION_EN_COURS`, `COMMANDE/ISSUE_NON_ETABLIE`, `EMISSION/COMMANDE_ACCEPTEE`, `ECHEC/TRANSITION_NON_OBSERVEE` — **dix-sept** |

> **Partition ratifiée en V4.** `A-10` **ratifie** cette partition en trois
> classes et sa sous-classe **`O-R`** : `O`, `O-R`, `T`, `H`. Elle cesse d'être
> une proposition. Le §4.4 donne sa répartition sur les trente-quatre valeurs.

**Pourquoi trois classes et non deux.** Une acceptation de commande et un refus
de lancement ne sont **ni** des missions ouvertes **ni** des clôtures de
mission. Les ranger avec les clôtures — ce que faisait implicitement la V1 en
les traitant comme « non terminaux » — ouvrait la porte à l'adoption d'une
mission externe (§6).

### 4.2 Sous-classe **O-R** — chaîne de retour engagée

> **Ajoutée en V2**, sur demande de distinguer les chaînes de retour des autres
> états d'activité.

Le retour à la base est le **seul geste à traîne longue** : entre l'ordre et
l'amarrage, le robot roule. Les états machine de retour et d'amarrage
appartiennent à la classe d'activité comme le nettoyage : sans marquage propre,
une chaîne de retour est indiscernable d'une mission qui nettoie encore.

**O-R est une sous-classe de O** : la mission est ouverte, **et** un retour a
été ordonné par Arsenal et n'a pas encore abouti. Elle est **testée avant** la
classe O générique dans la table de réconciliation (§6) — c'est la règle de
priorité qui manquait à la V1.

**Aucune sous-classe symétrique pour l'arrêt.** La signature positive de
l'arrêt est **inconnue et n'est pas complétée** : il n'existe aucun état
observable de « arrêt engagé, non abouti ». C'est précisément ce qui rend la
clôture non confirmée d'arrêt **nécessaire et terminale** (D-10).

### 4.3 Un refus de geste ne referme **jamais** une mission ouverte

> **Contrainte opérateur, non négociable.**

Le verdict est la **seule** mémoire de mission ouverte (D-08). Écrire, par-dessus
une valeur de classe O, une valeur qui n'est pas de classe O, **efface cette
mémoire** pendant que le robot roule : la mission devient ni ouverte ni close,
la supervision cesse, et **aucune issue explicite n'est produite** — le silence
exact que `ASP-INV-49` proscrit.

**Deux voies conformes, non départagées ici — arbitrage A-10 :**

| Voie | Description | Ce qu'elle coûte |
|---|---|---|
| **O1** | Un geste sans sens physique, ou hors mission Arsenal, **n'écrit rien** au verdict | Le refus doit vivre ailleurs ; `ASP-INV-50` exige un motif lisible, reste à dire où |
| **O2** | Deux valeurs supplémentaires **de classe O**, nommées hors du champ lexical du refus | Deux valeurs de plus ; `ASP-INV-70` contraint la rédaction |

> La V1 proposait deux valeurs nommées comme des refus **et** définissait la
> porte d'entrée sans elles. Les deux lectures échouaient : soit le décompte
> était faux, soit la mémoire de mission était effacée. C'était le bloquant B-2.

> ### ✅ `A-10` rendu en V4 — **voie `O1`**
>
> Un geste **physiquement dépourvu de sens**, ou **demandé hors mission**,
> **n'écrit rien** au verdict. Le script **s'arrête**, avec un **message
> explicite au caller**. Le cas **hors vocabulaire** est traité **séparément**.
>
> **La voie `O2` est écartée** : le vocabulaire ne gagne **aucune** valeur de
> garde. C'est ce qui explique que W2 compte onze valeurs et non treize.
>
> **Où vit le refus — la question que `A-10` laissait explicitement ouverte.**
> Dans la **réponse du script à son appelant**, et nulle part ailleurs. Le motif
> lisible exigé par `ASP-INV-50` est porté par le message d'arrêt, visible au
> journal et à la trace Home Assistant — **le canal par lequel une exception du
> moteur remonte déjà, intacte, aujourd'hui**. Aucun helper, aucun canal nouveau.
>
> **La contrainte non négociable est préservée** : un refus de geste **n'écrit
> rien**, donc il ne peut pas écraser une valeur de classe `O` ni effacer la
> mémoire d'une mission encore ouverte.

### 4.4 Partition des trente-quatre valeurs — **ajouté en V4**

| Classe | Nombre | Détail |
|---|---|---|
| **O** | **8** | `LANCEE/DEMARRAGE_OBSERVE` (W1) + les **sept** valeurs de conduite de W2 hors retour |
| **O-R** | **1** | `CONDUITE/RETOUR_ENGAGE` |
| **T** | **8** | les **trois** clôtures de W2 + les **cinq** valeurs de W3 |
| **H** | **17** | les treize refus, `VALIDATION_EN_COURS`, `COMMANDE/ISSUE_NON_ETABLIE`, `EMISSION/COMMANDE_ACCEPTEE`, `ECHEC/TRANSITION_NON_OBSERVEE` |
| | **34** | 8 + 1 + 8 + 17 |

**Les quatre classes sont exhaustives et disjointes** sur les trente-quatre
valeurs. Le cas **hors vocabulaire** leur reste **extérieur** (§6.1).

---

## 5. Machine d'états

### 5.1 Porte d'entrée — définition unique

> **Une mission Arsenal est ouverte si et seulement si le verdict appartient à
> la classe O (§4.1), sous-classe O-R comprise.**

C'est la **seule** définition employée dans tout l'artefact. Elle est
énumérable : sous la voie O1, la classe O compte **six** valeurs — la valeur de
démarrage observé de W1, et les cinq valeurs de conduite de W2. Sous la voie O2,
elle en compte **huit**.

> **Corrigé en V4.** La voie `O1` est retenue, mais `A-11` ajoute **trois**
> valeurs d'engagement de classe `O`. **La classe `O`, sous-classe `O-R`
> comprise, compte donc neuf valeurs** : `LANCEE/DEMARRAGE_OBSERVE`, les sept
> valeurs de conduite de W2 hors retour, et `CONDUITE/RETOUR_ENGAGE` (§4.4).
> **Six** était juste sous la voie `O1` **seule** ; l'écart est exactement
> l'apport d'`A-11`.

**N'ouvrent rien**, et c'est explicite : l'acceptation de commande — une
acceptation n'est jamais un démarrage (`ASP-INV-38`) —, l'issue non établie, la
validation en cours, la transition non observée, et les treize refus. Toutes
sont de classe **H**.

### 5.2 Gestes — W2

Chaque geste : garde de sens physique (`ASP-INV-48`) → **émission unique** →
relecture dans une fenêtre → verdict. Aucune réémission (`ASP-INV-39`).

> **La durée de ces fenêtres n'est ni spécifiée, ni couverte, ni gardée —
> ouverture V3.** Le domaine n'arrête aujourd'hui que **deux** constantes
> temporelles, dont la portée déclarée est **nommément liée aux étapes L1**, et
> aucun contrôle ne balaie les fichiers L2 à la recherche d'une temporisation
> concurrente. Un script de conduite pourrait donc porter **n'importe quelle**
> temporisation sans qu'aucun contrôle ne la voie, en violation d'un invariant
> resté intact.
>
> C'est exactement la structure du trou identifié pour la Maintenance en
> **A-14** — que la V2 n'avait pas cherchée sur son propre lot phare.
> **Arbitrage A-15. Aucune durée n'est proposée ici.**

> ### ✅ `A-15` rendu en V4 — **30 s**, mutualisées sur les quatre gestes
>
> Pause, reprise, arrêt et **engagement du retour** : **30 secondes**. La fenêtre
> du retour **confirme seulement l'entrée dans la chaîne de retour** ;
> l'**amarrage** reste observé **événementiellement** par W3, sans fenêtre.
>
> **Aucune constante temporelle nouvelle n'est créée.** Le domaine reste à
> `{30 s, 60 s}` : `ASP-INV-69` reçoit une **extension de portée** aux fenêtres
> L2, et `ASP-CI-20` une **extension de périmètre** aux fichiers L2.
> **Aucune autre temporisation** n'est admise dans un fichier L2.
>
> **La reprise n'a lieu que par geste opérateur explicite** — ce qui confirme la
> quatrième condition de `ASP-INV-62` plutôt que de l'assouplir.
>
> **Conséquence vérifiée : `ASP-CI-10` n'a pas à être amendé** — voir §8.2.

**Séquence de geste, telle que rendue en V4 :** garde de sens physique
(`ASP-INV-48`) → **écriture de l'engagement** (`A-11`) → **émission unique** →
relecture dans la fenêtre de **30 s** → verdict. Aucune réémission
(`ASP-INV-39`).

| Geste | Garde | Engagement écrit d'abord | Confirmé | Non confirmé |
|---|---|---|---|---|
| **Pause** | activité en cours | `CONDUITE/PAUSE_ENGAGEE` — **O** | `CONDUITE/PAUSE_CONFIRMEE` — **O** | `CONDUITE/PAUSE_NON_CONFIRMEE` — **O** : la mission peut rouler encore ; on le dit, on ne conclut pas |
| **Reprise** | garde fermée `ASP-INV-62`, **quatre conditions** : état de pause · session réellement ouverte · aucune erreur ni indisponibilité · **geste opérateur explicite, jamais une initiative du système** ; plus « mission Arsenal ouverte » au titre de D-07 | `CONDUITE/REPRISE_ENGAGEE` — **O** | `CONDUITE/REPRISE_CONFIRMEE` — **O** | `CONDUITE/REPRISE_NON_CONFIRMEE` — **O** |
| **Retour base** | le robot n'y est pas déjà et n'y va pas déjà | `CONDUITE/RETOUR_ENGAGE` — **O-R** | **W2 s'arrête là.** L'amarrage est observé par **W3**, qui écrit `CLOTURE/APRES_RETOUR_CONFIRME` — **T** | clôture **T** — `CLOTURE/APRES_RETOUR_NON_CONFIRME`, sur défaut d'entrée dans la chaîne |
| **Arrêt** | mission ouverte ; jamais plus contraint que le lancement (`ASP-INV-43`) | `CONDUITE/ARRET_ENGAGE` — **O** | clôture **T** — `CLOTURE/APRES_ARRET_CONFIRME` | clôture **T** — `CLOTURE/APRES_ARRET_NON_CONFIRME` |

> **Ce que la fenêtre du retour confirme, et ce qu'elle ne confirme pas.** Elle
> confirme **l'entrée dans la chaîne de retour**, pas son aboutissement. Le
> retour est le **seul geste à traîne longue** : lui appliquer une fenêtre de
> clôture reviendrait à borner un trajet physique par une durée, ce qui est
> exactement ce que `A-15` refuse. C'est pourquoi l'amarrage est **événementiel**
> et revient à W3.

> **`CONDUITE/ARRET_ENGAGE` n'est pas une sous-classe symétrique de `O-R`.**
> La **signature positive de l'arrêt reste inconnue** : cette valeur dit
> qu'Arsenal a **engagé** un arrêt, elle **n'observe rien**. Elle ne rend pas
> l'arrêt observable, et c'est ce qui maintient
> `CLOTURE/APRES_ARRET_NON_CONFIRME` **nécessaire et terminale** (`D-10`).

> **La signature positive de l'arrêt reste inconnue et n'est pas complétée.**
> Aucune déduction ne vient en tenir lieu.

> **La reprise est la seule voie de la primitive de démarrage** dans tout le
> domaine, et elle ne relance jamais une intention : elle poursuit la mission
> ouverte avec le périmètre et les réglages qui étaient les siens.

### 5.3 Supervision — W3

| Observation, **sur mission ouverte uniquement** | Verdict |
|---|---|
| Interruption hors geste opérateur | `ECHEC/MISSION_INTERROMPUE` — **ne présume pas la cause** |
| Erreur robot ou dock | `ECHEC/ERREUR_EN_MISSION` |
| Retour puis amarrage observés, **sans retour ordonné par Arsenal** | `CLOTURE/FIN_NOMINALE` |
| Amarrage observé **après un retour ordonné par Arsenal** | ~~cas disputé~~ → **rendu en V4** : `CLOTURE/APRES_RETOUR_CONFIRME`, écrit par **W3** |

> **`A-11` volet 2, rendu.** W3 est le **seul** writer autorisé à conclure après
> un retour ordonné par Arsenal. W2 s'arrête à `CONDUITE/RETOUR_ENGAGE` et **ne
> prétend pas conclure** : il n'y a donc plus deux candidats au même événement
> physique. La valeur disputée est **conservée** et **change de writer** — elle
> passe de W2 à W3, et cesse d'être suspendue.

> **W3 n'écrit aucune interruption pendant un engagement.** Tant que le verdict
> vaut `CONDUITE/PAUSE_ENGAGEE`, `CONDUITE/REPRISE_ENGAGEE`,
> `CONDUITE/ARRET_ENGAGE` ou `CONDUITE/RETOUR_ENGAGE`, W3 **s'abstient** de
> produire `ECHEC/MISSION_INTERROMPUE`. C'est l'exclusion rendue par `A-11`, et
> elle ne coûte **aucun helper** : W3 lit le verdict qu'il surveille déjà.

### 5.4 Course entre W2 et W3 — problème posé, **non résolu**

> **Ajouté en V2.**

**Séquence réelle.** L'opérateur demande l'arrêt → W2 émet → le robot
s'immobilise → **pendant la fenêtre de relecture de W2**, le verdict vaut
encore une valeur de classe O, et W3 observe une « interruption hors geste
opérateur » → W3 écrit une issue terminale → W2 l'écrase avec sa propre
clôture.

**Selon l'ordonnancement : on perd un échec réel, ou on affirme un échec faux.**
Même exposition sur la pause, l'état de pause appartenant à la classe
d'activité.

**Seconde course — la chaîne de retour, ajoutée en V3.** Sur un retour ordonné
par Arsenal, **l'amarrage est un événement physique unique** que **deux** writers
peuvent prétendre conclure : W2, qui a émis le geste et attend sa confirmation ;
W3, qui observe le retour puis l'amarrage et y voit une fin nominale.

> **C'est le geste le plus exposé — et c'était le seul dont la course n'était pas
> posée.** La V2 ne décrivait ici que l'arrêt et la pause.

**La disjonction des valeurs n'y change rien** (§1). Une garde d'exclusion est
nécessaire — jalon d'exclusion, inhibition de la supervision pendant une fenêtre
de geste, ou autre mécanisme.

> **Aucune garde n'est choisie ici. Arbitrage A-11, volets 1 et 2.**

### 5.5 La garde rendue — **`A-11`, volets 1 et 2, en V4**

> **Exclusion des writers par le verdict lui-même, sans helper supplémentaire.**

| # | Règle rendue |
|---|---|
| 1 | **W2 écrit l'engagement avant chaque commande** |
| 2 | **W3 ne produit aucune interruption pendant un engagement** |
| 3 | **W2 conclut** la pause, la reprise et l'arrêt |
| 4 | Sur un retour : **W2 s'arrête à `CONDUITE/RETOUR_ENGAGE`** ; **W3 seul** observe l'amarrage et écrit `CLOTURE/APRES_RETOUR_CONFIRME` |

**Reprise de la séquence du §5.4, sous la garde rendue.** L'opérateur demande
l'arrêt → **W2 écrit `CONDUITE/ARRET_ENGAGE`** → W2 émet → le robot s'immobilise
→ pendant la fenêtre de relecture, W3 **voit l'engagement dans le verdict et
s'abstient** → W2 conclut, confirmé ou non.
**Il n'y a plus ni échec perdu, ni échec faux.**

**Ce que la règle 1 apporte, et qui n'existait pas.** Les trois valeurs
d'engagement rendent la fenêtre de relecture **visible dans le verdict**. C'est
ce qui permet à l'exclusion de fonctionner **sans helper** : le jalon
d'exclusion envisagé par la V2 n'est pas nécessaire, parce que le verdict le
porte déjà.

**Les quatre questions du volet 2 reçoivent quatre réponses :**

| # | Question | Réponse rendue |
|---|---|---|
| 1 | Quel writer conclut après un retour ordonné par Arsenal ? | **W3** |
| 2 | Quelle valeur exacte à l'amarrage ? | `CLOTURE/APRES_RETOUR_CONFIRME` |
| 3 | Comment l'autre writer est-il neutralisé ? | **W2 s'arrête** à l'engagement du retour |
| 4 | La valeur est-elle conservée ? | **Oui** — elle **change de writer**, de W2 vers W3 |

---

## 6. Réconciliation au redémarrage — **table totale**

Déclencheur : passage à l'état stable du système.
**Indexée sur la classe du verdict (§4), jamais sur « terminal / non terminal ».**
**Les lignes sont évaluées dans l'ordre ; la première qui s'applique tranche.**

| # | Classe du verdict | État machine | Action | Règles servies |
|---|---|---|---|---|
| **1** | **T**, **H**, ou verdict inconnu | **quelconque** | **Rien.** Aucune supervision, aucune notification, aucun verdict écrit | D-R4, D-R5 |
| **2** | **O-R** | retour ou amarrage en cours | **Poursuivre** la supervision de la chaîne. **La clôture à l'amarrage revient à W3, qui écrit `CLOTURE/APRES_RETOUR_CONFIRME`** *(rendu en V4 — la V3.2 y lisait le cas disputé d'`A-11` volet 2)* | D-R2 |
| **3** | **O-R** | **tout autre état** | Clôture **opaque** | D-R1, D-R3 |
| **4** | **O** hors O-R | classe d'**activité** | Re-projeter la persistante, reprendre la supervision. **Aucune transition inventée** | D-R1 |
| **5** | **O** hors O-R | classe de **repos**, **quel que soit le témoin de session** | Clôture **opaque** | D-R1, D-R3 |
| **6** | **O** hors O-R | classe d'**erreur ou d'indisponibilité**, ou classe **non qualifiée** | Clôture **opaque** | D-R3 |

### 6.1 Preuve de totalité

Les classes de verdict `{T, H, hors vocabulaire}`, `{O-R}` et `{O hors O-R}`
sont **exhaustives et disjointes** sur l'ensemble des valeurs **augmenté du cas
hors vocabulaire**.

> **Précision V4.** L'ensemble couvert vaut désormais **34 valeurs** augmentées
> du cas hors vocabulaire. La preuve de totalité est **inchangée dans sa
> structure** : elle porte sur les **classes**, jamais sur un décompte.

> **Précision V3.** La V2 énonçait l'exhaustivité « sur les 31 ou 33 valeurs »,
> alors que le verdict **inconnu** — helper non initialisé au premier démarrage,
> ou valeur hors vocabulaire — n'en fait précisément **pas** partie. L'ensemble
> couvert est donc `vocabulaire ∪ {hors vocabulaire}`, et la ligne 1 absorbe ce
> dernier cas comme les deux autres. **L'écart renforçait la totalité au lieu de
> l'affaiblir** ; il est néanmoins corrigé, l'énoncé devant être exact.

- `{T, H, hors vocabulaire}` est intégralement couvert par la ligne 1, quel que
  soit l'état machine.
- `{O-R}` est couvert par les lignes 2 et 3, dont la seconde absorbe
  **tout autre état**.
- `{O hors O-R}` est couvert par les lignes 4, 5 et 6, qui recouvrent les
  **quatre classes** de la partition d'états du contrat : activité, repos,
  erreur ou indisponibilité, non qualifiée.

**Aucun couple (classe de verdict, état machine) n'est sans ligne.**

> **La ligne 5 est celle qui manquait à la V1.** Le cas « verdict ouvert, robot
> au repos, session encore ouverte » n'était couvert par aucune ligne : un
> silence, proscrit par `ASP-INV-49` et par D-R3.

### 6.2 Aucune adoption d'une mission externe — **par construction**

Les deux seules lignes qui **reprennent une supervision** — 2 et 4 — exigent un
verdict de **classe O**. Or la classe O ne s'atteint que par la valeur de
démarrage observé écrite par W1, ou par une valeur de conduite écrite par W2 sur
une mission **déjà** ouverte.

> **Conséquence.** Si le robot nettoie au redémarrage alors que le verdict vaut
> l'un des cas suivants, la **ligne 1** s'applique : **rien**. Aucune
> supervision, aucune notification, aucun verdict.
>
> | Cas | Nomenclature |
> |---|---|
> | Issue non établie · validation en cours · acceptation de commande · l'un des treize refus · transition non observée | **classe H** — valeurs **du** vocabulaire, hors mission |
> | Helper non initialisé au premier démarrage, ou valeur **hors vocabulaire** | **ni H, ni O, ni T** — la valeur **n'appartient pas au vocabulaire** |
>
> **Les deux sont absorbés par la même ligne 1, sans être confondus dans la
> nomenclature.** La classe H est une classe **du** vocabulaire ; le verdict
> hors vocabulaire lui est **extérieur**, conformément au §6.1.
>
> La V1 indexait sa table sur « non terminal », ce qui plaçait l'issue non
> établie et la validation en cours du côté des missions à re-superviser :
> **elle pouvait adopter une mission qu'Arsenal n'avait jamais observé
> démarrer**, contre D-06 et D-R4. C'était le point M-4c.

### 6.3 Pourquoi une clôture opaque distincte

Écrire une clôture nominale inventerait une observation que personne n'a faite.
Écrire une mission interrompue présumerait une cause. La seule chose vraie est
que **la chaîne est devenue inobservable** — et c'est cela qui doit s'écrire.

---

## 7. Rôles d'automation — **quatre rôles, quatre automations** *(rendu en V4)*

> ### ✅ `A-3` et `A-12` rendus en V4 — quatre identifiants attribués
>
> | Identifiant | Rôle |
> |---|---|
> | `10280000000001` | Supervision de mission — W3 |
> | `10280000000002` | Projection persistante de **mission** |
> | `10280000000003` | Projection persistante de **maintenance** |
> | `10280000000004` | **Remise à zéro de la composition d'intention** |
>
> **La conditionnalité du §7.1 est levée** : `A-12` retient l'**automation
> dédiée**, donc le quatrième identifiant est nécessaire **et** attribué. Le
> domaine compte **quatre rôles et quatre automations** — le « trois ou quatre »
> du titre historique ci-dessous est **résolu à quatre**.
>
> **Aucun identifiant n'est déduit par l'artefact** : les quatre sont **donnés
> par l'opérateur**. Le registre `06_input_selects/system/prefix_id.yaml` porte
> l'entrée `1028 - aspirateur`, ce qui les rend **bien formés** au regard des
> deux doctrines d'identifiants.

### 7.0 Titre historique — **quatre rôles, trois ou quatre automations**

> **Correction V2.** La V1 n'en annonçait que trois rôles. Il en faut **quatre**.
> **Correction V3.** Le nombre d'**automations** — et donc d'identifiants — est
> **conditionnel à l'arbitrage A-12**. La V2 affirmait « trois identifiants »
> comme acquis : c'était une **sur-assertion**, la seconde branche d'A-12 n'en
> exigeant que deux.

| # | Rôle | Nature | Identifiant |
|---|---|---|---|
| 1 | Supervision de mission — détection, clôtures, réconciliation, envoi mobile | **écrivain** | `10280000000001` — acquis (D-04) |
| 2 | Projection persistante de mission | **lecteur pur** | **`10280000000002`** *(attribué en V4)* |
| 3 | Projection persistante d'entretien | **lecteur pur** | **`10280000000003`** *(attribué en V4)* |
| 4 | **Remise à zéro de la composition d'intention** | écrivain de helpers d'interface, **lecteur** du verdict | **`10280000000004`** *(attribué en V4)* |

> **Le rôle 4 s'élargit en V4.** `A-12` lui donne **deux** déclencheurs, et non
> plus le seul redémarrage : `input_boolean.systeme_stable` passant à `on`, **et**
> le verdict prenant la valeur `COMMANDE/ISSUE_NON_ETABLIE`. Il **lit** donc le
> verdict — sans jamais l'écrire — ce qui exige une **exception nominative
> minimale à `ASP-CI-11`**. Détail :
> [`09_UI.md`](09_UI.md) §3.3 bis et
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §4.2.
>
> **Le rôle 4 reste un lecteur pur du verdict et un écrivain des seuls helpers
> d'interface.** L'écrivain unique vers l'appareil demeure le moteur
> (`ASP-INV-31`), et l'écrivain du verdict demeure le trio W1/W2/W3.

### 7.1 Décompte conditionnel des identifiants

| Branche d'A-12 retenue | Automations | Identifiants nouveaux |
|---|---|---|
| **Automation dédiée** de remise à zéro | **4** | **3** |
| **Report** du rôle 4 sur un writer existant | **3** | **2** |

> **Deux identifiants nouveaux sont certains** — les deux projections.
> **Le troisième n'est nécessaire que sous la première branche.**
> `10280000000001` reste le **seul acquis**, et **aucun autre identifiant n'est
> proposé, suggéré ni préattribué.**

**Pourquoi la quatrième est nécessaire.** La remise à zéro de la composition
est **obligatoire, pas optionnelle** : la voie native `initial` est **fermée par
la CI** — l'interdiction est dure et sans exception sur les booléens d'entrée —,
si bien que les quatorze booléens de segment seront **restaurés** au
redémarrage. Un script ne se déclenche pas seul, et les trois voies évidentes
sont fermées :

| Voie | Pourquoi elle est fermée |
|---|---|
| L'automation de stabilisation existante | Son en-tête, contrat local opposable, lui interdit toute décision métier et tout pilotage |
| Les automations n° 2 et n° 3 | Déclarées **lecteurs purs** ; leur faire écrire dix-sept helpers les disqualifierait |
| La clé `initial` | Interdiction dure de la CI sur les booléens d'entrée |

> Le dépôt porte déjà le patron d'une telle automation de réconciliation au
> démarrage dans deux autres domaines. Le choix entre **quatrième automation**
> et **report explicite sur un writer existant** appartient à l'opérateur :
> **arbitrage A-12**.

**Pourquoi les automations 1 et 2 ne peuvent pas fusionner.** La projection doit
réagir à **tout** changement du verdict, y compris ceux écrits par W1 et W2. La
supervision réagit aux transitions du robot. Une automation unique en mode
redémarrage-sur-déclenchement **annulerait sa propre supervision en vol** à
chaque écriture de verdict par un autre writer.

**Pourquoi les automations 2 et 3 ne peuvent pas fusionner.** Sources, cycles de
vie et identifiants de notification distincts ; toute évolution de l'une
recréerait l'autre.

> **Deux identifiants certains, un troisième conditionnel — voir §7.1.**
> Aucun n'est préattribué, ni suggéré, ni déduit d'une suite arithmétique.
> Arbitrages **A-3** et **A-12**.
>
> **Rendu en V4 :** les trois identifiants nouveaux sont **attribués par
> l'opérateur** — `…02`, `…03`, `…04`. La conditionnalité est **levée**, pas
> contournée : `A-12` a retenu l'automation dédiée.

---

## 8. L2 est un **acte contractuel**, avant d'être un amendement de CI

> **Correction V2 — la V1 se trompait de nature.** Elle titrait « Prérequis de
> CI — bloquant » et ne parlait que de checkers.

### 8.1 Ce que le contrat dit, et que le lot rompt

`ASP-INV-31` énumère **nommément** les gestes que la décision D-01 confierait à
un second script : « Toute écriture vers le robot — sélection de carte,
intensité d'eau, aspiration, commande de mission, **interruption, retour à la
base** — passe exclusivement par lui. » `ASP-INV-42` le redit pour les gestes
de conduite.

> **Créer un second script de conduite rompt ces deux invariants, pas seulement
> le contrôle qui les garde.** Amender le checker seul rendrait la CI verte sur
> une violation d'invariant restée intacte.

> **Arbitrage A-9 ouvert** : nouveau chapitre de conduite et de supervision, ou
> extension du chapitre `07` ? **Situation symétrique de A-6**, correctement
> ouvert pour la Maintenance.

> ### ✅ `A-9` rendu en V4 — **nouveau chapitre `15_conduite_et_supervision.md`**
>
> Avec **amendements minimaux à `ASP-INV-31` et `ASP-INV-42`**, le **checker**
> correspondant, et la **mise à jour du registre de couverture**.
>
> La forme 1 étant retenue **pour `A-6` comme pour `A-9`**, la conséquence
> documentaire du §8.6 se réalise : **deux** chapitres contractuels nouveaux
> feront dériver le compte du registre, et chacun doit le mettre à jour **dans
> son propre lot**.
>
> **« Minimal » se lit strictement.** Les deux invariants énumèrent nommément
> l'interruption et le retour à la base parmi les écritures réservées au moteur
> unique : l'amendement ouvre **ces gestes-là**, au **seul** script de conduite,
> et ne relâche ni l'écrivain unique vers l'appareil, ni la garde fermée
> `ASP-INV-62` sur la primitive de démarrage.

### 8.2 Amendements de CI, une fois l'acte contractuel rendu

| Contrôle | Action | Nature |
|---|---|---|
| `ASP-CI-11` | Liste d'autorisation de **trois** écrivains, table `{fichier → ensemble littéral}`, vérification de la disjonction deux à deux ; appels d'appareil autorisés dans le **seul** fichier de conduite | **amendement** |
| `ASP-CI-14` | **Étendre le périmètre** aux fichiers L2 et n'y tolérer qu'**une seule** occurrence de la primitive de démarrage, adossée à la garde `ASP-INV-62` | **amendement** |
| `ASP-CI-18` | Élargir le vocabulaire fermé et sa constante de cycle de vie ; **le décompte confronté au fichier L1 doit être réécrit** | **amendement** |
| **`ASP-CI-19`** | **Étendre l'obligation de motif lisible aux valeurs nouvelles.** Le contrôle n'ancre aujourd'hui que les 18 codes du catalogue et les 4 valeurs de cycle de vie : sans amendement, les valeurs L2 n'auraient **aucune** obligation de motif, contre `ASP-INV-50` | **amendement — manquait à la V1** |
| **`ASP-CI-20`** | **Étendre le périmètre aux fichiers L2.** Le contrôle refuse toute temporisation concurrente mais **ne balaie que les cinq fichiers L1** : une fenêtre de relecture L2 y échapperait entièrement. Sa forme dépend de **A-15** | **amendement — manquait à la V2** |
| `ASP-CI-10` | ~~**Selon A-15.**~~ **Aucun amendement — rendu en V4.** Voir l'encadré ci-dessous | **retiré du lot** |
| `ASP-CI-3` | **À rejouer** lors de la rédaction contractuelle L2 — voir §8.5 | **réexécution** |
| `ASP-CI-21` | **À réexécuter, pas à amender.** La marge de capacité est recalculée par le contrôle lui-même ; la valeur la plus longue proposée reste très en deçà de la capacité déclarée | **réexécution** |

> ### `ASP-CI-10` n'a **pas** à être amendé — vérifié en V4
>
> La V3.2 inscrivait au lot `L2` un « amendement conditionnel de `ASP-CI-10`
> selon `A-15` ». **La condition ne se réalise pas**, pour deux raisons dont
> chacune suffit :
>
> 1. Le contrôle n'admet que `{30, 60}` secondes sur **tous** les chapitres du
>    domaine. `A-15` ayant **mutualisé à 30 s**, un chapitre `15` portant ces
>    fenêtres ne produit **aucune durée concurrente**.
> 2. L'exigence de « **exactement deux lignes** » porte sur le **seul** tableau
>    des fenêtres du chapitre `07`, que le contrôle lit **dans ce chapitre-là**.
>    Un chapitre `15` doté de son propre tableau ne le fait pas dériver.
>
> **C'est la mutualisation qui l'évite.** Une quatrième valeur, ou une ligne
> supplémentaire dans le tableau du `07`, l'aurait rendu obligatoire.
>
> **L'amendement est retiré du contenu du lot `L2`** — voir
> [`10_LOTS.md`](10_LOTS.md) §2.

> ### Ce que `A-15` ajoute au lot, et qui remplace l'amendement retiré
>
> | Contrôle ou invariant | Action rendue |
> |---|---|
> | `ASP-INV-69` | **Extension de portée** aux fenêtres L2 — **aucune constante nouvelle** |
> | `ASP-CI-20` | **Extension du périmètre** aux fichiers L2, avec interdiction de toute temporisation non contractualisée |

### 8.3 Deux fichiers L1 sont réellement touchés

| Fichier L1 | Ce qui doit y changer |
|---|---|
| `04_input_texts/aspirateur/mission.yaml` | Le **décompte** de son en-tête, confronté mécaniquement par `ASP-CI-18` ; et sa déclaration « écrivain unique … aucune automation, aucune UI, aucun autre script n'écrit ici », devenue fausse |
| `12_template_sensors/aspirateur/motif_lisible.yaml` | La **traduction** des valeurs nouvelles, exigée par `ASP-CI-19` amendé |

### 8.4 Indissociabilité — **conséquence à retenir**

`ASP-CI-18` exige que **toute valeur du vocabulaire soit effectivement écrite**.

> **Correction V3 — attribution normative.** Cette exigence est **mécanique** :
> elle vit dans le **checker**, pas dans le contrat. La V2 l'attribuait à
> `ASP-INV-65`, dont l'énoncé réel est tout autre — « le catalogue est total sur
> l'état machine ». Le point est **matériel** : toute la thèse de A-9 repose sur
> la distinction entre obligation contractuelle et exigence de CI, et attribuer
> à un invariant ce qui relève d'un checker l'affaiblissait. Voir
> `03_REFERENCES_CONTRATS.md` §1, « trois exigences à ne jamais confondre ».
>
> **Précision de portée.** Le contrôle vérifie aujourd'hui l'atteignabilité par
> le **moteur seul**. L'amendement devra l'étendre aux **trois writers** — ce
> qui **renforce** la conclusion d'indissociabilité plutôt qu'il ne l'affaiblit.

Porter la constante de 18 à un total qui dépend de A-10 et A-11 sans livrer
conjointement les fichiers qui écrivent les valeurs nouvelles fait **échouer la
CI immédiatement**.

> **Précisé en V4.** Le total ne dépend plus d'un arbitrage : il vaut **34**, et
> la répartition à écrire dans l'en-tête du fichier L1 est **16 présents · 2
> absents · 18 valeurs de cycle de vie** (§3.3 bis). **L'indissociabilité n'en
> est pas affaiblie** — elle est même renforcée : les seize valeurs nouvelles
> étant désormais nommées, chacune doit avoir un écrivain **dans le même lot**,
> sous peine d'échec d'atteignabilité.

> **Il n'existe donc aucun lot de CI seul, et aucun ordonnancement où
> l'amendement précéderait le runtime.** L'acte contractuel, l'amendement de
> CI, les deux fichiers L1 et le runtime L2 forment **un seul lot
> indissociable** — qui sollicite le robot.
>
> *La V1 présentait un lot « L2a » de CI seule, ordonnançable avant le runtime,
> et le rangeait parmi les lots ne sollicitant pas le robot. C'était faux.*

---

### 8.5 Piège de rédaction du chapitre L2 — `ASP-CI-3` *(ajouté en V3)*

`ASP-CI-3` refuse **tout jeton entre accents graves** de la forme
`[A-Z][A-Z_]{4,}` qui ne figure pas au catalogue des codes.

Le contrat actuel ne cite **aucune** valeur de cycle de vie sous forme nue : la
contrainte est donc déjà respectée, mais **elle n'est écrite nulle part**.

> **Conséquence pour la rédaction du chapitre L2.**
> Un code de cycle de vie **nu** entre accents graves serait pris pour un code
> de catalogue inconnu et **ferait échouer le contrôle**. Sous sa **forme
> complète préfixée**, il contient un caractère qui interrompt l'expression et
> **y échappe**.
>
> **Trois obligations de rédaction, à porter au lot L2 :**
>
> 1. citer les valeurs sous leur **forme complète préfixée**, ou sous une forme
>    explicitement admise par le contrôle ;
> 2. **ne jamais** écrire un identifiant de cycle de vie nu entre accents
>    graves dans un chapitre de contrat ;
> 3. **rejouer `ASP-CI-3`** pendant la rédaction contractuelle, et non après.

C'est le **piège jumeau** de celui relevé pour la Maintenance — les durées à
écrire en heures. La V2 avait levé l'un et pas l'autre.

---

### 8.6 Conséquence documentaire de la forme 1 d'A-9 *(ajouté en V3)*

Si **A-9** retient la création d'un **nouveau chapitre** de conduite et de
supervision, le lot L2 hérite mécaniquement de la même conséquence que le lot
Maintenance sous la forme 1 d'A-6 :

> Le contrôle transverse de couverture **compte les fichiers de contrat** et
> confronte ce nombre au registre de couverture. **Un chapitre nouveau fait
> dériver ce compte et casse la CI** si le registre n'est pas mis à jour **dans
> le même lot**.

**La V2 avait établi cette conséquence pour A-6 et ne l'avait pas transposée à
A-9**, alors qu'elle pose elle-même les deux cas comme strictement symétriques.
Voir `10_LOTS.md` §3.4, où la règle est désormais **généralisée**.
