#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : domaine Aspirateur.

Contrat (source normative) : 00_documentation_arsenal/contrats/aspirateur/
Audit factuel du domaine    : 00_documentation_arsenal/audits/01_rapports/
                              aspirateur/audit_faisabilite_roborock_q7_max.md

PÉRIMÈTRE — ce que ce checker vérifie, et ce qu'il ne vérifie pas.

Deux couches, depuis le lot runtime L1.

1. L'**intégrité du système normatif lui-même** (ASP-CI-1 … ASP-CI-10) : un
   contrat dont le référentiel, le catalogue de refus ou la partition d'états
   se troue cesse d'être opposable, et le trou est silencieux.

2. La **conduite runtime** (ASP-CI-11 … ASP-CI-27), étendue au lot L2. Les obligations que le
   contrat énonçait sans pouvoir les confronter — écrivain unique, forme
   enveloppée de la charge utile, convention de passages, interdiction
   d'écrire le mode dérivé, ordre de la séquence, unicité de la commande,
   fermeture du vocabulaire de verdict, totalité du motif lisible, constantes
   temporelles — le sont désormais.

CE QUE LES LOTS COUVRENT, ET CE QU'ILS NE COUVRENT PAS. L1 portait le seul
lancement. Le lot L2 ajoute la CONDUITE d'une mission ouverte et sa
SUPERVISION : le verdict compte désormais TROIS écrivains — moteur, script de
conduite, automation de supervision — à ensembles de valeurs exactes et DEUX À
DEUX DISJOINTS, dont l'union fait les 34 valeurs du vocabulaire. Deux des
quatre codes du catalogue qui restaient sans écrivain en trouvent un :
`MISSION_INTERROMPUE` et `ERREUR_EN_MISSION`, écrits par la supervision.

DEUX RESTENT DÉLIBÉRÉMENT SANS ÉCRIVAIN, et ce n'est pas un manque.
`CANAL_INDISPONIBLE` est le diagnostic de l'APPELANT : si la demande n'atteint
pas Home Assistant, aucun objet Arsenal ne s'exécute pour l'écrire.
`COMMANDE_REJETEE` est **structurellement** hors de portée : Home Assistant
n'expose aucune construction YAML d'attrapage d'erreur, et distinguer un rejet
d'une interruption d'exécution exigerait un observateur survivant à l'appel.
ASP-CI-18 **interdit** au moteur d'écrire ces codes — un verdict anticipé
affirmerait un rejet avant qu'un rejet soit observable — pendant qu'ASP-CI-19
**exige** leur traduction dans le motif lisible : le catalogue reste total,
sans qu'aucun verdict ne dépasse la connaissance acquise.

CE QUE LE LOT L2 NE COUVRE TOUJOURS PAS : l'interface. Aucune couche
d'intention, aucune surface Lovelace — lots `U0` et `U2`, et `ASP-CI-28` leur
reste RÉSERVÉ. La SIGNATURE POSITIVE DE L'ARRÊT reste inconnue et n'est pas
complétée : la confirmation d'arrêt est établie NÉGATIVEMENT, par la cessation
d'activité, et jamais par un état d'arrêt nommé qu'aucune partition ne classe.

TROIS ANCRES INDÉPENDANTES DU CONTRAT. Un contrôle qui ne lit que le contrat ne
prouve que sa cohérence interne : falsifier la table ET ses consommateurs le
laisse passer. Trois ancres extérieures ferment cette porte :

  1. l'AUDIT du domaine        — segments, noms, cartes, entités et primitives ;
  2. les CONSTANTES de module  — partition d'états et énumérations natives,
                                 figées ici et non relues du contrat ;
  3. l'arbre LOVELACE réel     — surface de commande.

Dix contrôles, tous adossés à une clause déjà normée par le contrat :

  ASP-CI-1  Invariants  — `ASP-INV-n` numérotés 1..N sans trou ni doublon,
                          format de déclaration uniforme ; `ASP-IMC-1` défini
                          une fois et une seule.
  ASP-CI-2  Référentiel — chaque couple (segment, nom Roborock) de la table
                          canonique est ATTESTÉ PAR L'AUDIT, index de carte
                          compris ; les segments observés non commandables
                          restent hors table ; le Garage n'est pas promu ; les
                          périmètres et raccourcis restent mono-carte et dans
                          la table (ASP-INV-6/28/55, ASP-IMC-1).
  ASP-CI-3  Codes       — tout code cité figure au catalogue ; tout motif de
                          REFUS y figurant est produit par au moins une clause
                          RÉELLE — catalogues, index, sections de renvois et
                          blocs de code exclus des zones productrices
                          (ASP-INV-50/52).
  ASP-CI-4  États       — la classification est FIGÉE ICI : un état déplacé,
                          ajouté ou retiré échoue, et le lien classe N → refus
                          par défaut → `ETAT_NON_QUALIFIE` est vérifié
                          explicitement (ASP-INV-60).
  ASP-CI-5  Profils     — six profils exactement, `gentle` exclu, valeurs
                          natives bornées aux énumérations attestées
                          (ASP-INV-10/11).
  ASP-CI-6  Identifiants— tout jeton `<domaine>.<objet>` d'un domaine Home
                          Assistant doit être EXACTEMENT attesté par l'audit —
                          comparaison par jeton entier, un préfixe tronqué ne
                          passe pas — ou reconnu comme primitive de service
                          documentée ; les domaines de helpers Arsenal sont
                          interdits en bloc (ASP-INV-58).
  ASP-CI-7  Lovelace    — ni entité native d'ACTION du robot, ni NOM DE SERVICE
                          STATIQUE `vacuum.*` / `roborock.*` sous les clés
                          `service:` / `action:` / `perform_action:`, quel que
                          soit le mode de ciblage — `entity_id`, `device_id`,
                          `area_id`, `label_id` (ASP-INV-31, chapitre 11).
  ASP-CI-8  Réf. tech.  — le référentiel TECHNIQUE (02 §2.1) est confronté à
                          l'audit — option EXACTE du sélecteur (espace finale
                          comprise), index de carte, index natif de segment, nom
                          Roborock —, mis en correspondance COMPLÈTE avec le
                          référentiel métier, et SÉPARÉ de lui mécaniquement :
                          aucune ligne n'est lue par les deux parseurs. `2_17`,
                          `2_18` et le Garage ne peuvent pas être promus
                          (ASP-INV-66/67, QO-1). Garde aussi, SECTION PAR
                          SECTION, les clauses qui rendent l'exception
                          cartographique close : cardinalité seule interdite,
                          table des trois usages autorisés, conditions 3 et 4
                          d'ASP-IMC-1, comparaison littérale, non-exposition des
                          libellés techniques. Une phrase semblable dans un
                          renvoi ou un index ne satisfait aucune garde.
  ASP-CI-9  États canon.— dix états canoniques exactement, sans synonyme ; image
                          TOTALE de la partition 07 §5.0 vers ces codes
                          (`charger_disconnected` → `repos_hors_base`, classe N →
                          `etat_non_qualifie`), lien vers le refus
                          `ETAT_NON_QUALIFIE`, et compteurs des chapitres 08, 11
                          et 12 réalignés (ASP-INV-44/68). Chaque compteur et
                          l'admissibilité de `repos_hors_base` sont ancrés sur
                          LEUR clause exacte — jamais sur une occurrence isolée
                          de « dix » ou « admissible » ailleurs dans le même
                          chapitre. Vérifie en outre que PARTITION_ATTENDUE et
                          IMAGE_ATTENDUE décrivent le même monde, classe par
                          classe : un état déplacé à image inchangée échoue.
  ASP-CI-10 Fenêtres    — deux constantes temporelles et deux seulement, 30 s
                          pour les confirmations (étapes 6, 8, 10) et 60 s pour
                          la seule transition de démarrage, associée sur SA
                          LIGNE de catalogue à `TRANSITION_NON_OBSERVEE` ;
                          aucune durée concurrente sur LES QUATORZE chapitres —
                          l'observation terrain du 08 §3 est exemptée par sa
                          clause littérale, jamais par une allowlist de nombres ;
                          aucun helper temporel, aucun fallback, révision
                          CONJOINTE contrat + checker + runtime
                          (ASP-INV-69, ARB-3).

Dix-sept contrôles de CONDUITE, adossés au runtime L1 et — depuis le lot L2 —
au runtime de conduite et de supervision :

  ASP-CI-11 Écrivains  — le moteur : un seul script, `mode: single`, quatre
                          champs ; le script de conduite : un seul script,
                          `mode: single`, UN champ fermé. TABLE
                          `{fichier -> ensemble littéral}` des TROIS écrivains
                          du verdict, avec DISJONCTION deux à deux, couverture
                          TOTALE du vocabulaire, et refus de toute valeur non
                          littérale. La TRACE d'intention garde UN écrivain, le
                          moteur. Le verdict n'est mentionnable que par le
                          runtime L1, ses trois écrivains et la SEULE
                          projection de mission, qui ne l'écrit jamais. Un
                          appel d'appareil n'est admis que dans DEUX fichiers.
                          Slots critiques LITTÉRAUX dans les huit fichiers
                          nommés (ASP-INV-31/32/61/86).
  ASP-CI-12 Charge utile — le gabarit `params` est RENDU, pas cherché à la
                          regex : le résultat doit être une LISTE contenant UN
                          mapping, la forme nue échouant en silence
                          (ASP-INV-33).
  ASP-CI-13 Passages    — rendu pour ×1, ×2, ×3 : `repeat` ABSENT pour ×1, et
                          jamais `0` ni `1`, qui transposeraient la convention
                          DÉCALÉE de la voie zonée (ASP-INV-18/19).
  ASP-CI-14 Voies       — ni `app_zoned_clean`, ni `repeats`, ni `vacuum.start`,
                          ni `clean_area` : commentaires neutralisés d'abord,
                          faute de quoi l'en-tête qui INTERDIT ces voies les
                          déclencherait lui-même (07 §6). Périmètre ÉTENDU aux
                          trois fichiers L2, avec UNE exception nominative : la
                          primitive de démarrage est admise dans le SEUL
                          fichier de conduite, UNE SEULE FOIS, et seulement si
                          les quatre ancres de sa garde fermée y figurent
                          (ASP-INV-62).
  ASP-CI-15 Mode dérivé — `select.entree_…_mode_de_nettoyage` n'est jamais la
                          CIBLE d'une écriture : l'écrire écrase le profil
                          d'aspiration (ASP-INV-12).
  ASP-CI-16 Ordre       — carte, puis EAU, puis ASPIRATION, puis commande, et
                          une relecture des gardes INTERCALÉE entre le dernier
                          réglage et l'émission, portant sur les QUATRE témoins
                          (ASP-INV-34/36).
  ASP-CI-17 Commande    — exactement une émission de démarrage (ASP-INV-35).
  ASP-CI-18 Verdict     — DÉCOMPTE du vocabulaire RECALCULÉ et confronté au
                          texte du helper : 34 valeurs de verdict pour 18 codes
                          du catalogue, et les deux ensembles SE RECOUPENT — 16
                          présents, 2 absents, 18 valeurs de cycle de vie. Le
                          moteur écrit EXACTEMENT ses 18 valeurs ;
                          `ISSUE_NON_ETABLIE` posé AVANT l'appel avec la trace,
                          `COMMANDE_ACCEPTEE` seulement au retour réussi ;
                          aucun `continue_on_error` sur l'émission ; aucun des
                          deux codes hors de portée. SÉQUENCE L2, geste par
                          geste : l'ENGAGEMENT précède la commande, il y a
                          EXACTEMENT une émission et c'est celle du geste, la
                          relecture est unique et bornée, et le verdict ne
                          s'écrit qu'avec les valeurs de CE geste. SUPERVISION :
                          aucune écriture hors d'une mission ouverte, exclusion
                          de l'interruption pendant un engagement, clôture
                          opaque réservée à la réconciliation de redémarrage
                          (ASP-INV-37/38/49/86/87/88/89/92/94).
  ASP-CI-19 Motif       — les 18 codes du catalogue et les 18 valeurs de cycle
                          de vie traduits, chacun sous 255 caractères, sans
                          index nu, sans libellé d'appareil, sans nom d'entité
                          (ASP-INV-6/7/50/53).
  ASP-CI-20 Constantes  — trois fenêtres de 30 s et une de 60 s dans le moteur,
                          QUATRE fenêtres de 30 s dans le script de conduite —
                          mutualisées, donc sans durée concurrente et sans
                          amendement d'ASP-CI-10 —, AUCUNE dans la supervision
                          ni dans la projection, aucune autre temporisation,
                          aucun helper temporel (ASP-INV-69, A-15).
  ASP-CI-21 Concordance — les six identifiants ATTRIBUÉS par l'opérateur, le
                          référentiel embarqué confronté aux tables §2 / §2.1
                          — espace finale de `Étage ` comprise —, les cinq
                          profils, la partition, l'attestation des entités
                          natives par l'audit, et la CAPACITÉ réelle des
                          helpers face à la sérialisation MAXIMALE d'une
                          intention V1 (ASP-INV-58/63/66/67).
  ASP-CI-22 Rendus      — les DEUX défauts de plateforme que ce lot revendique
                          avoir évités sont VERROUILLÉS, en rendant les
                          gabarits : le `data:` de la sélection de carte doit
                          se rendre en mapping et restituer l'option EXACTE,
                          espace finale comprise (sinon `.strip()` la mange) ;
                          aucune variable ne doit se rendre en valeur que
                          `_parse_result` retype (sinon `referentiel[0]` ne
                          résout plus) ; et la garde de type de `segments`
                          refuse un MAPPING, dont Jinja itérerait les clés.
  ASP-CI-23 État rendu  — le gabarit d'état canonique est RENDU sur les 43
                          valeurs réellement exposées par l'appareil, plus
                          `unavailable`, et confronté à l'image contractuelle
                          classe par classe ; `mission_ouverte` doit distinguer
                          l'indisponibilité de `non` (ASP-INV-45/68).
  ASP-CI-24 Garde rendue— la garde de lancement est RENDUE sur le produit
                          cartésien des quatre témoins et confrontée à la règle
                          du moteur : une garde qui ne calcule plus rien ne
                          passe plus (07 §5.1).
  ASP-CI-25 Refus tardifs— chaque COMPARAISON exigée à l'étape 11 existe, et
                          produit LE code de refus qui lui correspond, avec
                          `stop:`. C'est la comparaison qui est contrôlée, pas
                          la seule présence du nom du témoin : retirer
                          `g2_err_dock != 'ok'` en laissant `g2_err_dock` dans
                          une autre branche passait au vert, alors qu'un dock
                          en erreur ne refusait plus rien. Le jeu de refus
                          tardifs égale par ailleurs celui de la garde
                          initiale (ASP-INV-36, ASP-INV-50).
  ASP-CI-26 Silences   — propriete generale dont les trois chemins muets du
                          lot L1 etaient un cas : toute etape pouvant lever une
                          exception non absorbee doit etre PRECEDEE d'un verdict
                          qui reste VRAI si l'execution s'arrete la.
                          `VALIDATION_EN_COURS` ne survit pas ;
                          `COMMANDE/ISSUE_NON_ETABLIE`, si. Le verdict courant
                          se lit sur le CHEMIN NOMINAL — une ecriture logee dans
                          une branche de refus est suivie d'un `stop:` et n'est
                          jamais en vigueur ensuite (ASP-INV-49, ASP-INV-50).
  ASP-CI-27 Preparatoires— `continue_on_error: true` sur les TROIS ecritures
                          preparatoires et nulle part ailleurs ; instant de
                          reference PROPRE a chacune, rendu par
                          `now().timestamp()` et capture AVANT l'appel ;
                          confirmation bornee a 30 s avec
                          `continue_on_timeout: true` ; relecture finale qui
                          reevalue valeur ET fraicheur sans jamais s'appuyer sur
                          `wait.completed` ; `last_reported` et non
                          `last_updated`, comparaison STRICTE ; refus attendu
                          pose avec `stop:` ; et l'ordre de la sequence V-A —
                          selection carte < ecriture eau < confirmation carte <
                          confirmation eau < aspiration < commande
                          (ASP-IMC-1, ASP-INV-17, ASP-INV-69).

Trois contrôles de PROPAGATION, livrés par le lot 3 du chantier C45, qui
exécute les arbitrages `Q1` et `Q2` :

  ASP-CI-43 Représentations— toute représentation runtime d'une CLASSE du
                          verdict, ou d'un SOUS-ENSEMBLE contractuellement
                          nommé de classe, est confrontée À ÉGALITÉ EXACTE à
                          l'ensemble canonique fermé correspondant. Le
                          recensement suit l'ÉNUMÉRATION, jamais le nom de la
                          clé — chercher `verdict_ouvert` avait manqué les
                          engagements de la supervision ET les clés de la
                          table de phrases de la projection, qui énumèrent
                          l'une et l'autre une classe sous un autre nom. Le
                          cardinal du recensement est figé : une huitième
                          représentation doit être QUALIFIÉE avant d'être
                          admise, une liste qui diverge pouvant être la bonne
                          (ASP-INV-98).
  ASP-CI-44 Ancien code  — régime TRANSITOIRE du code historique du dixième
                          état. Allowlist FERMÉE et NOMINATIVE qui GÈLE la
                          population existant au HEAD du lot 2 : producteur,
                          quatre sites de restitution, ce module et le
                          chapitre 08. Refus de toute occurrence technique
                          supplémentaire ou déplacée, et refus du code de
                          REMPLACEMENT tant que le mouvement atomique du lot 5
                          n'a pas eu lieu. Le cardinal des deux fichiers gelés
                          est lu DEUX FOIS : en FORME, par analyse structurée
                          des clés d'attribut du producteur et des slots de
                          restitution de l'arbre Lovelace ; en NOMBRE, par
                          recomptage du fichier une fois NEUTRALISÉS les
                          commentaires YAML — pleine ligne comme fin de ligne.
                          La première dit ce que les emplois SONT, la seconde
                          rattrape ceux qui ne sont ni clé ni slot : une
                          lecture Jinja de l'attribut, une carte qui le
                          restitue. Dans les CONTRATS, les destinations de
                          liens Markdown sont neutralisées d'abord — un
                          chapitre doit pouvoir renvoyer à l'arbitrage `Q1`,
                          dont le NOM DE FICHIER porte le code de
                          remplacement. Les mentions documentaires hors
                          contrats et hors ce module ne sont PAS des emplois
                          techniques et ne sont pas balayées. Ce contrôle a
                          une MORT PROGRAMMÉE : le lot 5 supprime l'allowlist
                          et lui substitue, dans le même mouvement, la règle
                          permanente de ZÉRO occurrence (08 §1.3).
  ASP-CI-45 Offre gestes — l'offre d'un geste de conduite Arsenal se règle sur
                          le verdict, et sur lui seul : la garde de classe `O`
                          PRÉCÈDE le dispatch et n'écrit rien ; l'ARRÊT ne
                          porte AUCUNE restriction de sens physique, ni au
                          backend ni à l'interface — c'est la conséquence
                          directe d'ASP-INV-43, l'arrêt n'est jamais plus
                          contraint que le lancement ; le RETOUR À LA BASE
                          porte ses TROIS exclusions de sens physique, ni plus
                          ni moins, des deux côtés (ASP-INV-97, ASP-INV-48).

CE QUE LE LOT 3 NE COUVRE PAS, ET POURQUOI. Ni la source exclusive de la
projection métier, ni ses trois régimes d'indisponibilité, ni l'AUTORITÉ des
quatre sites Lovelace. Les deux premières portent sur un objet livré au lot 4
— la projection n'existe pas encore —, la troisième sur une bascule du lot 6.
Un contrôle vert parce que sa cible est absente est DORMANT, et il ment : il
affiche une garantie que rien ne soutient. C'est pour la même raison que
l'exception nominative de lecture d'ASP-CI-11 REFUSE désormais un fichier
qu'elle nomme sans qu'il existe, et refuse qu'il réside dans un arbre
Lovelace — l'ouvrir là relâcherait l'interdit du chapitre 11.


Les blocs de code clôturés sont neutralisés avant TOUS les contrôles, et aussi
sur l'audit : un exemple documentaire n'est normatif nulle part, et un faux
tableau placé dans un bloc n'atteste rien.

CE QU'ASP-CI-7 NE PEUT PAS GARANTIR — dit ici plutôt que passé sous silence.
Ces trois angles morts sont réels ; aucun n'est neutralisé par une exemption,
et aucun n'est réductible par une analyse statique du seul dépôt :

  1. **Un appel générique ciblé par `device_id`.** `select.select_option` visant
     un `device_id` peut basculer la carte active sans nommer le robot. Rattacher
     un `device_id` — un UUID opaque — à un appareil exige le registre de
     périphériques, qui ne vit pas dans le dépôt. Interdire globalement
     `select.select_option` serait faux : le motif a des emplois légitimes dans
     d'autres domaines.
  2. **Un nom de service entièrement construit par template.** Sans littéral
     analysable, il n'y a rien à confronter.
  3. **Un second aspirateur relevant d'une autre autorité.** La portée de
     `vacuum.*` est aujourd'hui GLOBALE sur les arbres Lovelace. C'est accepté
     parce qu'Arsenal ne possède qu'un seul aspirateur : la portée coïncide donc
     en pratique avec l'autorité du domaine. **Elle devra être réexaminée avant
     l'ajout d'un second équipement relevant d'une autre autorité**, faute de
     quoi ce checker refuserait une commande qu'il n'a pas à gouverner.

ASP-CI-7 est donc une garde d'anti-régression **sur les commandes statiquement
nommées** : elle balaie une surface réelle, n'y trouve aujourd'hui aucune
violation, et se déclenche sur toute entité d'action ou tout nom de service
littéral. Elle ne prétend pas détecter « toute commande brute ».

Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
Codes de sortie : 0 conforme, 1 violation(s), 2 erreur d'usage/infra.

Usage :
  python check_aspirateur_contracts.py
  python check_aspirateur_contracts.py --selftest
"""

from __future__ import annotations

import argparse
import ast
import inspect
import math
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DOMAIN = ROOT / "00_documentation_arsenal" / "contrats" / "aspirateur"
AUDIT = (ROOT / "00_documentation_arsenal" / "audits" / "01_rapports" /
         "aspirateur" / "audit_faisabilite_roborock_q7_max.md")
# Seconde source d'attestation, NOMMEE et FERMEE : le releve des entites
# d'entretien. L'audit de faisabilite est anterieur au perimetre Maintenance et
# n'atteste AUCUNE de ses huit entites ; sans cette source, ASP-CI-6 refuserait
# le chapitre 14 alors que ces entites sont bel et bien relevees.
# Ce fichier n'apporte QUE des faits d'existence : aucune regle, aucun seuil.
RELEVE_ENTRETIEN = (ROOT / "00_documentation_arsenal" / "audits" / "01_rapports" /
                    "aspirateur" / "releve_entites_entretien.md")
LOVELACE_DIRS = ("18_lovelace", "19_button_card_templates")
FICHIER_CATALOGUE = "09_refus_et_diagnostics.md"
FICHIER_ENTRETIEN = "14_entretien.md"
FICHIER_ETATS = "08_etats_et_observation.md"

# ═════════════════════════════════════════════════════════════
# COUCHE D'INTENTION — ASP-CI-28 (lot U0, arbitrage A-13)
#
# La reserve est LEVEE : le lot U0 livre les vingt objets, et avec eux la
# SECONDE MATERIALISATION du referentiel du chapitre 02. Le cadrage ne
# pretend pas l'eviter — il la reconnait et exige qu'une confrontation la
# garde, exactement comme ASP-CI-21 garde celle du moteur.
#
# Ce que le controle confronte, et rien d'autre : les quatorze booleens,
# leurs paires canoniques, leur appartenance aux cartes, leurs libelles
# Arsenal, le chapitre 02 et le referentiel embarque du moteur L1 — plus le
# MAPPING qui les relie, qui vit dans les scripts de composition et de
# raccourci. Une copie derivee designe la mauvaise piece : c'est cela, et
# seulement cela, que le controle rend impossible.
# ═════════════════════════════════════════════════════════════

FICHIER_U0_SEGMENTS = "05_input_booleans/aspirateur/segments.yaml"
FICHIER_U0_CARTE = "06_input_selects/aspirateur/intention_carte.yaml"
FICHIER_U0_PROFIL = "06_input_selects/aspirateur/intention_profil.yaml"
FICHIER_U0_PASSAGES = "06_input_selects/aspirateur/intention_passages.yaml"
FICHIER_U0_COMPOSITION = "10_scripts/aspirateur/composer_intention.yaml"
FICHIER_U0_RACCOURCI = "10_scripts/aspirateur/appliquer_raccourci.yaml"
FICHIER_U0_REINIT = "10_scripts/aspirateur/reinitialiser_composition.yaml"
FICHIERS_U0 = (FICHIER_U0_SEGMENTS, FICHIER_U0_CARTE, FICHIER_U0_PROFIL,
               FICHIER_U0_PASSAGES, FICHIER_U0_COMPOSITION,
               FICHIER_U0_RACCOURCI, FICHIER_U0_REINIT)

# Le suffixe d'un booleen de segment est la PAIRE CANONIQUE elle-meme
# (ASP-INV-6) : aucun index nu, aucun libelle Roborock.
PREFIXE_SEGMENT_U0 = "aspirateur_segment_"
CLE_U0_SEGMENTS = re.compile(r"^" + PREFIXE_SEGMENT_U0 + r"(\d+_\d+)$")

# Nom de carte tel qu'il apparait dans le NOM AFFICHE des booleens
# (09_UI.md §3.5.3). Distinct de l'option du selecteur, et c'est voulu.
CARTE_AFFICHEE_U0 = {"0": "RDC", "1": "Étage", "2": "Annexe"}
# Options du selecteur de carte -> index du moteur (09_UI.md §3.5.2).
# `Étage` s'affiche SANS espace finale : l'espace de `Étage ` appartient au
# referentiel TECHNIQUE, dont ASP-INV-66 borne l'usage au moteur.
CARTE_OPTION_U0 = {"Rez-de-chaussée": "0", "Étage": "1", "Annexe": "2"}
PASSAGES_OPTION_U0 = {"1 passage": "1", "2 passages": "2", "3 passages": "3"}
# Options du selecteur de profil -> cle du moteur (03 §1, 09_UI.md §3.5.2).
# SIX depuis l'exposition du niveau d'aspiration le plus faible : `quiet`
# etait deja ecrit par les deux profils de serpillere, mais restait
# inatteignable en aspiration seule.
PROFIL_OPTION_U0 = {
    "Aspiration minimale": "aspiration_minimale",
    "Aspiration normale": "aspiration_normale",
    "Aspiration turbo": "aspiration_turbo",
    "Aspiration maximale": "aspiration_maximale",
    "Serpillière moyenne": "serpilliere_moyenne",
    "Serpillière intensive": "serpilliere_intensive",
}

# Les TROIS raccourcis — cles du champ ferme `raccourci` -> perimetre
# contractuel (02 §3, 10 §3), profil par defaut et passages par defaut
# (10 §3.1). La cle est une valeur de conception ; le PERIMETRE et les DEUX
# REGLAGES sont contractuels, et ce sont eux que le controle confronte.
#
# DEUX PERIMETRES, TROIS RACCOURCIS : le perimetre RDC est expose deux fois,
# une fois en aspiration et une fois en serpillere. Le chapitre 02 §3
# continue de recenser CINQ perimetres — un perimetre n'est pas un
# raccourci, et la couverture du referentiel repose sur 02 §3, jamais sur
# la table des raccourcis.
RACCOURCI_U0 = {
    "rdc_aspiration": ("RDC complet", "Aspiration normale", "3 passages"),
    "rdc_serpilliere": ("RDC complet", "Serpillière moyenne", "3 passages"),
    "etage_aspiration": ("Étage complet", "Aspiration normale", "3 passages"),
}


def load_runtime_u0() -> dict[str, str]:
    """Les sept fichiers de la couche d'intention, lus par CHEMIN NOMME."""
    out: dict[str, str] = {}
    for rel in FICHIERS_U0:
        chemin = ROOT / rel
        if chemin.is_file():
            out[rel] = chemin.read_text(encoding="utf-8", errors="ignore")
    return out


def _doc_u0(u0: dict[str, str], rel: str):
    try:
        return yaml.safe_load(u0.get(rel) or "")
    except yaml.YAMLError:
        return None


def _variables_u0(doc, cle: str):
    """La valeur de `cle` dans le premier bloc `variables:` d'un script."""
    if not isinstance(doc, dict):
        return None
    for corps in doc.values():
        if not isinstance(corps, dict):
            continue
        for st in corps.get("sequence") or []:
            if isinstance(st, dict) and isinstance(st.get("variables"), dict) \
                    and cle in st["variables"]:
                return st["variables"][cle]
    return None


def check_referentiel_intention(t02: str, t10: str, corps,
                                u0: dict[str, str]) -> list[str]:
    """ASP-CI-28 — la seconde materialisation du referentiel, confrontee.

    Six faces, toutes confrontees et jamais supposees : les quatorze
    booleens, leurs paires, leurs cartes, leurs libelles, le chapitre 02, et
    le referentiel embarque du moteur L1. Plus le mapping qui les relie.
    """
    errs: list[str] = []

    manquants = [rel for rel in FICHIERS_U0 if rel not in u0]
    if manquants:
        return [f"ASP-CI-28 : la couche d'intention est incomplete — "
                f"{sorted(manquants)} absent(s) du depot."]

    # ── Les trois autorites confrontees ────────────────────────────────────
    canon = parse_segments(t02)              # chapitre 02 §2
    if not canon:
        return ["ASP-CI-28 : table canonique des segments introuvable (02 §2)."]
    ref = next((v["referentiel"] for v in _bloc_variables(corps)
                if "referentiel" in v), None)
    if not isinstance(ref, dict):
        return ["ASP-CI-28 : referentiel embarque du moteur introuvable — la "
                "confrontation n'a pas de second terme."]
    moteur: dict[str, str] = {}
    for carte, bloc in ref.items():
        for paire in (bloc.get("segments") or {}):
            moteur[str(paire)] = str(carte)

    # ── (a) les quatorze booleens : cles, paires, cartes, libelles ─────────
    doc_seg = _doc_u0(u0, FICHIER_U0_SEGMENTS)
    if not isinstance(doc_seg, dict) or not doc_seg:
        return [f"ASP-CI-28 : `{FICHIER_U0_SEGMENTS}` est illisible ou vide."]
    paires_u0: dict[str, str] = {}
    for cle, corps_helper in sorted(doc_seg.items()):
        m = CLE_U0_SEGMENTS.match(str(cle))
        if not m:
            errs.append(f"ASP-CI-28 : la cle `{cle}` ne porte pas la forme "
                        f"`{PREFIXE_SEGMENT_U0}‹paire canonique›` — un index "
                        "nu ou un libelle Roborock ne designe rien "
                        "(ASP-INV-6, ASP-INV-67).")
            continue
        paire = m.group(1)
        paires_u0[paire] = str((corps_helper or {}).get("name") or "")

    attendues = set(canon)
    if set(paires_u0) != attendues:
        errs.append(f"ASP-CI-28 : les booleens de segment couvrent "
                    f"{sorted(paires_u0)} — le chapitre 02 §2 en compte "
                    f"{sorted(attendues)}. Une copie qui derive designe la "
                    "mauvaise piece.")
    if set(paires_u0) != set(moteur):
        errs.append(f"ASP-CI-28 : les booleens de segment couvrent "
                    f"{sorted(paires_u0)} — le referentiel embarque du moteur "
                    f"en compte {sorted(moteur)}.")

    for paire, nom in sorted(paires_u0.items()):
        if paire not in canon or paire not in moteur:
            continue
        libelle = canon[paire][0]
        carte = CARTE_AFFICHEE_U0.get(moteur[paire])
        if carte is None:
            errs.append(f"ASP-CI-28 : le segment `{paire}` releve de la carte "
                        f"`{moteur[paire]}`, sans nom de carte affichable.")
            continue
        if paire.split("_", 1)[0] != moteur[paire]:
            errs.append(f"ASP-CI-28 : la paire `{paire}` annonce la carte "
                        f"`{paire.split('_', 1)[0]}` et le moteur la range "
                        f"dans `{moteur[paire]}`.")
        attendu = f"Aspirateur — {carte} — {libelle}"
        if nom != attendu:
            errs.append(f"ASP-CI-28 : `{PREFIXE_SEGMENT_U0}{paire}` affiche "
                        f"{nom!r} — attendu {attendu!r} : carte ET libelle "
                        "canonique Arsenal (02 §4, ASP-INV-7).")

    # ── (b) aucun `initial:` sur les dix-sept helpers ──────────────────────
    for rel in (FICHIER_U0_SEGMENTS, FICHIER_U0_CARTE, FICHIER_U0_PROFIL,
                FICHIER_U0_PASSAGES):
        if re.search(r"^[ \t]+initial[ \t]*:", sans_commentaires_yaml(u0[rel]),
                     re.M):
            errs.append(f"ASP-CI-28 : `{rel}` porte `initial:` — la remise a "
                        "zero au demarrage est portee par l'automation "
                        f"`{AID_U0_COMPOSITION}`, jamais par une cle native "
                        "(A-12).")

    # ── (c) les trois selecteurs : options exactes ─────────────────────────
    def options(rel: str, cle: str) -> list[str]:
        doc = _doc_u0(u0, rel)
        bloc = (doc or {}).get(cle) or {}
        return [str(o) for o in (bloc.get("options") or [])]

    opts_carte = options(FICHIER_U0_CARTE, "aspirateur_intention_carte")
    if opts_carte != list(CARTE_OPTION_U0):
        errs.append(f"ASP-CI-28 : le selecteur de carte expose {opts_carte} — "
                    f"attendu {list(CARTE_OPTION_U0)}.")
    if any(o != o.strip() for o in opts_carte):
        errs.append("ASP-CI-28 : une option du selecteur de carte porte une "
                    "espace de bord — l'espace finale de `Étage ` appartient "
                    "au referentiel TECHNIQUE, borne au moteur (ASP-INV-66).")
    opts_pass = options(FICHIER_U0_PASSAGES, "aspirateur_intention_passages")
    if opts_pass != list(PASSAGES_OPTION_U0):
        errs.append(f"ASP-CI-28 : le selecteur de passages expose {opts_pass} "
                    f"— attendu {list(PASSAGES_OPTION_U0)}.")

    # Les cinq libelles de profil sont ceux du chapitre 03, pris via la table
    # de traduction : l'interface n'introduit aucun vocabulaire parallele.
    opts_profil = options(FICHIER_U0_PROFIL, "aspirateur_intention_profil")
    doc_comp = _doc_u0(u0, FICHIER_U0_COMPOSITION)
    table_profils = _variables_u0(doc_comp, "profils")
    profils_moteur = next((v["profils"] for v in _bloc_variables(corps)
                           if "profils" in v), None)
    if not isinstance(table_profils, dict) or not isinstance(profils_moteur, dict):
        errs.append("ASP-CI-28 : table de traduction des profils introuvable "
                    "— la concordance interface -> moteur n'est pas etablie.")
    else:
        if list(table_profils) != opts_profil:
            errs.append(f"ASP-CI-28 : la traduction des profils porte "
                        f"{list(table_profils)} — le selecteur expose "
                        f"{opts_profil}. Une option non traduisible partirait "
                        "en valeur vide.")
        if set(table_profils.values()) != set(profils_moteur):
            errs.append(f"ASP-CI-28 : la traduction des profils vise "
                        f"{sorted(set(table_profils.values()))} — le moteur "
                        f"connait {sorted(profils_moteur)}.")

    # ── (d) la table carte et le mapping paire -> booleen ──────────────────
    table_cartes = _variables_u0(doc_comp, "cartes")
    if table_cartes != CARTE_OPTION_U0:
        errs.append(f"ASP-CI-28 : la traduction des cartes porte "
                    f"{table_cartes!r} — attendu {CARTE_OPTION_U0!r}.")
    table_passages = _variables_u0(doc_comp, "table_passages")
    if table_passages != PASSAGES_OPTION_U0:
        errs.append(f"ASP-CI-28 : la traduction des passages porte "
                    f"{table_passages!r} — attendu {PASSAGES_OPTION_U0!r}.")

    ordre_canon = sorted(canon, key=lambda s: (int(s.split("_")[0]),
                                               int(s.split("_")[1])))
    composition = _variables_u0(doc_comp, "composition")
    if not isinstance(composition, list):
        errs.append(f"ASP-CI-28 : `{FICHIER_U0_COMPOSITION}` ne porte aucune "
                    "table `composition` — le mapping paire -> booleen est "
                    "introuvable.")
    else:
        vues = [str((s or {}).get("paire")) for s in composition]
        if vues != ordre_canon:
            errs.append(f"ASP-CI-28 : la table `composition` porte {vues} — "
                        f"attendu l'ordre canonique {ordre_canon} (02 §2).")
        for s in composition:
            paire = str((s or {}).get("paire"))
            attendu = f"input_boolean.{PREFIXE_SEGMENT_U0}{paire}"
            if str((s or {}).get("helper")) != attendu:
                errs.append(f"ASP-CI-28 : la paire `{paire}` est associee a "
                            f"`{(s or {}).get('helper')}` — attendu "
                            f"`{attendu}`.")

    # ── (e) les cinq raccourcis, confrontes aux perimetres contractuels ────
    doc_rac = _doc_u0(u0, FICHIER_U0_RACCOURCI)
    raccourcis = _variables_u0(doc_rac, "raccourcis")
    perimetres: dict[str, tuple[str, list[str]]] = {}
    for source, label in ((t02, "02 §3"), (t10, "10 §3")):
        for nom, carte, comp in PERIMETRE.findall(source):
            perimetres.setdefault(nom.strip(), (carte, SEGMENT_REF.findall(comp)))
    if not isinstance(raccourcis, dict):
        errs.append(f"ASP-CI-28 : `{FICHIER_U0_RACCOURCI}` ne porte aucune "
                    "table `raccourcis` — le champ ferme n'a pas d'enumeration.")
    else:
        if set(raccourcis) != set(RACCOURCI_U0):
            errs.append(f"ASP-CI-28 : le champ ferme expose {sorted(raccourcis)} "
                        f"— attendu exactement {sorted(RACCOURCI_U0)}. Creer, "
                        "modifier ou supprimer un raccourci est un acte "
                        "contractuel (ASP-INV-57).")
        for cle, (nom, profil_attendu, passages_attendus) in sorted(
                RACCOURCI_U0.items()):
            bloc = raccourcis.get(cle)
            if not isinstance(bloc, dict):
                continue
            if nom not in perimetres:
                errs.append(f"ASP-CI-28 : le perimetre « {nom} » du raccourci "
                            f"`{cle}` est introuvable dans les tables "
                            "contractuelles (02 §3, 10 §3).")
                continue
            carte_attendue, segs_attendus = perimetres[nom]
            segs = [str(s) for s in (bloc.get("segments") or [])]
            if sorted(segs) != sorted(segs_attendus):
                errs.append(f"ASP-CI-28 : le raccourci `{cle}` prerempli "
                            f"{sorted(segs)} — le perimetre « {nom} » en "
                            f"compte {sorted(segs_attendus)}.")
            cartes_vues = {s.split("_", 1)[0] for s in segs}
            if len(cartes_vues) > 1:
                errs.append(f"ASP-CI-28 : le raccourci `{cle}` agrege les "
                            f"cartes {sorted(cartes_vues)} — un raccourci est "
                            "mono-carte (ASP-INV-55).")
            option = str(bloc.get("carte") or "")
            if CARTE_OPTION_U0.get(option) != carte_attendue:
                errs.append(f"ASP-CI-28 : le raccourci `{cle}` designe la "
                            f"carte {option!r}, qui ne vaut pas l'index "
                            f"`{carte_attendue}` du perimetre « {nom} ».")
            # ── Les DEUX reglages par defaut, confrontes au 10 §3.1 ────
            # Le second alinea d'ASP-INV-56 les AUTORISE, a trois conditions :
            # visibles, modifiables avant lancement, jamais appliques
            # implicitement. Les trois tiennent PAR CONSTRUCTION — ce sont des
            # options de SELECTEUR D'INTENTION, donc rendues par la composition
            # et modifiables d'un geste, et ce script ne lance rien (garde
            # ci-dessous). Ce qui reste a prouver, c'est leur VALEUR : un
            # raccourci qui proposerait un autre profil que celui du 10 §3.1
            # serait un raccourci que le contrat ne decrit pas.
            for champ, attendu, table in (
                    ("profil", profil_attendu, PROFIL_OPTION_U0),
                    ("passages", passages_attendus, PASSAGES_OPTION_U0)):
                valeur = bloc.get(champ)
                if valeur is None:
                    errs.append(f"ASP-CI-28 : le raccourci `{cle}` ne propose "
                                f"aucun `{champ}` — le 10 §3.1 lui en attribue "
                                f"un : {attendu!r}.")
                elif str(valeur) != attendu:
                    errs.append(f"ASP-CI-28 : le raccourci `{cle}` propose "
                                f"`{champ}: {valeur!r}` — le 10 §3.1 attribue "
                                f"{attendu!r}.")
                elif str(valeur) not in table:
                    errs.append(f"ASP-CI-28 : le raccourci `{cle}` propose "
                                f"`{champ}: {valeur!r}`, hors des options du "
                                f"selecteur {sorted(table)}. Un raccourci "
                                "n'ecrit que des options existantes.")
            # ── Et RIEN d'autre : la composition, jamais le lancement ──────
            for champ in sorted(set(bloc) - {"carte", "segments", "profil",
                                             "passages"}):
                errs.append(f"ASP-CI-28 : le raccourci `{cle}` porte le champ "
                            f"`{champ}` — un raccourci compose une intention, "
                            "et ne porte que carte, segments, profil et "
                            "passages.")

    tous = _variables_u0(doc_rac, "tous_les_segments")
    if [str(s) for s in (tous or [])] != ordre_canon:
        errs.append(f"ASP-CI-28 : `{FICHIER_U0_RACCOURCI}` porte "
                    f"{[str(s) for s in (tous or [])]} comme liste complete — "
                    f"attendu {ordre_canon}. Une liste incomplete laisserait "
                    "une case d'une autre carte allumee.")

    # ── (f) la remise a zero eteint les QUATORZE, nommes un a un ───────────
    eteints = set(re.findall(r"input_boolean\.(" + PREFIXE_SEGMENT_U0
                             + r"\d+_\d+)",
                             sans_commentaires_yaml(u0[FICHIER_U0_REINIT])))
    attendus_eteints = {PREFIXE_SEGMENT_U0 + p for p in canon}
    if eteints != attendus_eteints:
        errs.append(f"ASP-CI-28 : la remise a zero nomme {sorted(eteints)} — "
                    f"attendu les quatorze {sorted(attendus_eteints)}.")
    return errs


# ═════════════════════════════════════════════════════════════
# MAINTENANCE — ASP-CI-29 … ASP-CI-33 (lot M0, chapitre 14)
# ═════════════════════════════════════════════════════════════

# Les quatre postes, FIGES ICI. Ils sont CONFRONTES au releve d'attestation,
# jamais tires de lui : un releve falsifie ne peut pas deplacer la verite.
POSTES_ENTRETIEN = {
    "filtre": ("sensor.roborock_q7_max_temps_restant_filtre",
               "button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air",
               150),
    "brosse principale": (
        "sensor.roborock_q7_max_temps_restant_brosse_principale",
        "button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_principale",
        300),
    "brosse laterale": (
        "sensor.roborock_q7_max_temps_restant_brosse_laterale",
        "button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_laterale",
        200),
    "capteurs": ("sensor.roborock_q7_max_temps_restant_capteurs",
                 "button.roborock_q7_max_reinitialiser_le_consommable_du_capteur",
                 30),
}
BOUTONS_ENTRETIEN = frozenset(v[1] for v in POSTES_ENTRETIEN.values())
CAPTEURS_ENTRETIEN = frozenset(v[0] for v in POSTES_ENTRETIEN.values())

# ── F3 : familles FERMEES. Tout jeton de ces deux familles, cite dans le
# chapitre 14 ou dans le releve d'attestation, doit appartenir exactement aux
# listes ci-dessus. Une falsification COORDONNEE des deux documents ne deplace
# donc plus la verite : elle se heurte a la constante figee ici.
FAMILLE_CAPTEUR = re.compile(r"sensor\.roborock_q7_max_[a-z0-9_]+")
FAMILLE_BOUTON = re.compile(r"button\.roborock_q7_max_[a-z0-9_]+")
# Jetons de ces familles legitimement cites HORS perimetre Maintenance : ils
# appartiennent au lot L1 et sont attestes par l'audit de faisabilite.
HORS_MAINTENANCE = frozenset({
    "sensor.roborock_q7_max_etat",
    "sensor.roborock_q7_max_erreur_de_l_aspirateur",
    "sensor.roborock_q7_max_dock_erreur_de_dock",
    "sensor.roborock_q7_max_piece_actuelle",
    "button.roborock_q7_max_nettoyage_complet",
})

# ── LOT M2 : LE VERROU EST LEVE, ET PAR CE QUI LE REMPLACE.
# L'allowlist n'est plus vide : elle nomme le fichier UNIQUE du lot M2, celui
# que le contrat 14 §4 designe comme seul appelant autorise (ASP-INV-81).
# Le desserrage n'est PAS une modification de constante : il est conditionne
# au visiteur YAML recursif ci-dessous, dont l'etat DERIVE d'un essai reel.
ALLOWLIST_PRESSION: frozenset[str] = frozenset({
    "10_scripts/aspirateur/declarer_entretien.yaml"})

# Toute mention d'un bouton d'entretien, ou l'un des quatre boutons nommes.
# Declare ICI, et non plus bas : le visiteur recursif le consomme des le
# calcul de `VISITEUR_YAML_RECURSIF`, en tete de module.
BOUTON_ENTRETIEN_RE = re.compile(
    r"button\.roborock_q7_max_reinitialiser_le_consommable_[a-z_]+")

# Les six formes que le detecteur de M0 ne couvrait pas, et que le visiteur
# doit rattraper. Ce ne sont pas des exemples : ce sont les CAS D'ESSAI dont
# le succes conditionne le desserrage de l'allowlist.
FORMES_ADVERSES_PRESSION = (
    # 1 — flow mapping
    ('a:\n  - {action: button.press, target: {entity_id: '
     'button.roborock_q7_max_reinitialiser_le_consommable_du_capteur}}\n'),
    # 2 — `tap_action: call-service` (forme Lovelace)
    ('a:\n  tap_action:\n    action: call-service\n'
     '    service: button.press\n    service_data:\n      entity_id: '
     'button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n'),
    # 3 — scalaire replie
    ('a:\n  - action: button.press\n    target:\n      entity_id: >-\n'
     '        button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n'),
    # 4 — alias YAML
    ('cible: &c '
     'button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n'
     'a:\n  - action: button.press\n    target:\n      entity_id: *c\n'),
    # 5 — ciblage par device_id, la pression restant nommee ailleurs
    ('a:\n  - action: button.press\n    target:\n      device_id: abc123\n'
     '    # button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n'
     'b: button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n'),
    # 6 — entity_id templatise, la cible reelle etant illisible
    ('a:\n  - action: button.press\n    target:\n      entity_id: '
     '"{{ cible }}"\n'
     'b: button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n'),
)


def _noeuds_yaml(noeud):
    """Visite RECURSIVE de tout mapping et de toute liste, en profondeur.

    Rend chaque noeud rencontre — le document lui-meme compris. Les alias
    YAML sont resolus par `yaml.safe_load` en amont : l'ancre et son alias
    designent le meme objet Python, et il est donc visite.
    """
    yield noeud
    if isinstance(noeud, dict):
        for v in noeud.values():
            yield from _noeuds_yaml(v)
    elif isinstance(noeud, list):
        for v in noeud:
            yield from _noeuds_yaml(v)


def _chaines_yaml(noeud):
    """Toute chaine du document, cles comprises."""
    for n in _noeuds_yaml(noeud):
        if isinstance(n, str):
            yield n
        elif isinstance(n, dict):
            for k in n:
                if isinstance(k, str):
                    yield k


def pressions_entretien(txt: str) -> set[str]:
    """Les boutons d'entretien nommes par un document YAML, quelle qu'en soit
    la forme.

    Le balayage est STRUCTUREL : le document est charge, puis visite
    recursivement. Il rattrape donc le flow mapping, le scalaire replie et
    l'alias — trois formes qu'une expression reguliere sur le texte manque.

    Il retombe sur un balayage TEXTUEL du document prive de ses commentaires
    lorsque le YAML est illisible : un fichier qu'on ne sait pas charger ne
    doit pas devenir un angle mort.
    """
    trouves: set[str] = set()
    try:
        doc = yaml.safe_load(txt)
    except yaml.YAMLError:
        doc = None
    if doc is not None:
        for s in _chaines_yaml(doc):
            trouves |= set(BOUTON_ENTRETIEN_RE.findall(s))
    if not trouves:
        trouves |= set(BOUTON_ENTRETIEN_RE.findall(sans_commentaires_yaml(txt)))
    return trouves


def _visiteur_est_complet() -> bool:
    """L'etat du visiteur DERIVE de son implementation reelle.

    Le contrat 14 §6.1 l'exige explicitement : « l'etat du visiteur devra
    deriver de son implementation reelle, et non d'un booleen declaratif
    comme celui que M0 employe faute de mieux ».

    Le visiteur n'est donc declare complet que s'il rattrape LES SIX formes
    adverses. Une regression du parseur rabaisse le drapeau, et l'allowlist
    non vide leve alors le verrou d'elle-meme.
    """
    return all(pressions_entretien(f) for f in FORMES_ADVERSES_PRESSION)


VISITEUR_YAML_RECURSIF = _visiteur_est_complet()

# ── F2 : perimetre YAML FONCTIONNEL, explicite et justifie.
# INCLUS — configuration Home Assistant reellement chargee :
RACINE_HA = ("configuration.yaml", "logbook.yaml", "logger.yaml",
             "recorder.yaml", "utility_meter.yaml")
DOSSIERS_FONCTIONNELS = ("blueprints", "esphome", "custom_components",
                         "zigbee2mqtt")
# EXCLUS, et pourquoi :
#   .git/                    internes du gestionnaire de versions ;
#   00_documentation_arsenal documentation — le chapitre 14 y NOMME les quatre
#                            boutons : la balayer ferait s'auto-declencher la
#                            garde sur le contrat qu'elle protege ;
#   .github/                 orchestration CI, pas de la configuration HA ;
#   scripts/                 outillage et registres de checkers ;
#   tools/**/tests/fixtures/ contre-exemples deliberes.
EXCLUS_YAML = ("00_documentation_arsenal/", ".github/", "scripts/", "tools/",
               "node_modules/", ".venv/")
# Nombre de profils de la table canonique (03 §1). SIX depuis l'exposition
# du niveau d'aspiration le plus faible : `quiet` sans eau. Fige ici pour
# qu'un profil ajoute ou retire en silence echoue, contrat comme moteur.
NB_PROFILS = 6
SEUIL_ENTRETIEN_PCT = 10
CLASSES_ECHEANCE = ("dû", "non dû", "non évaluable")

# ═════════════════════════════════════════════════════════════
# MAINTENANCE — lot M1, PROJECTION d'entretien (ASP-CI-34 … ASP-CI-36)
#
# M1 est un lot de TEMPLATES : deux entites derivees, aucune action, aucune
# notification, aucune commande. Les deux identifiants ne sont PAS inventes
# ici : ils sont FIXES par le cadrage ratifie (D-44), 08_NOTIFICATIONS.md
# §4.2. ASP-INV-58 — « aucun identifiant invente » — est donc respecte, et
# les figer ici fait echouer un renommage silencieux.
#
# Aucun invariant neuf. M1 ne cree aucune obligation : il rend IMMEDIATEMENT
# OPPOSABLES celles que le chapitre 14 avait deja posees et rangees au regime
# DIFFERE (§6) — ASP-INV-73 perimetre ferme, ASP-INV-74 l'indisponibilite
# n'est pas une valeur, ASP-INV-75 seuil unique, ASP-INV-76 aucune echeance
# conclue sur une donnee absente.
# ═════════════════════════════════════════════════════════════

RUNTIME_M1 = "12_template_sensors/aspirateur/entretien.yaml"
ID_M1_LISTE = "aspirateur_entretien_du"
ID_M1_TEMOIN = "aspirateur_entretien_requis"
ENTITE_M1_LISTE = "sensor." + ID_M1_LISTE
ENTITE_M1_TEMOIN = "binary_sensor." + ID_M1_TEMOIN

# Libelles Arsenal des quatre postes, tels que le chapitre 14 §1 les nomme.
LIBELLES_M1 = {
    "filtre": "Filtre",
    "brosse principale": "Brosse principale",
    "brosse laterale": "Brosse latérale",
    "capteurs": "Nettoyage des capteurs",
}
# Perimetre attendu du bloc `variables:` — libelle -> (source, plafond en
# heures). Il DERIVE de POSTES_ENTRETIEN : contrat, releve et runtime sont
# ainsi confrontes a une seule et meme constante figee.
PERIMETRE_M1 = {LIBELLES_M1[k]: (v[0], v[2])
                for k, v in POSTES_ENTRETIEN.items()}

ORDRE_M1 = tuple(LIBELLES_M1[k] for k in POSTES_ENTRETIEN)
ETAT_M1_AUCUN = "aucun"
ETAT_M1_NON_EVAL = "non_evaluable"
CLASSES_M1 = ("du", "non_du", "non_evaluable")
# Les deux icones du temoin. Elles derivent de `postes_dus` du capteur de
# liste — jamais de l'etat precedent du temoin lui-meme, qui n'existe pas
# au premier rendu.
ICONE_M1_DUE = "mdi:broom"
ICONE_M1_SOLDEE = "mdi:check-circle-outline"
# Cinq attributs, et cinq seulement — un par besoin identifie des lots avals :
#   seuil_pourcentage      restitution du seuil, depuis la variable du calcul
#   postes_dus             consomme par le temoin binaire et par N1
#   postes_non_dus         etabli POSITIVEMENT, jamais par difference
#   postes_non_evaluables  la troisieme situation, nommee ; disponibilite N1/UI
#   postes                 detail restant/plafond par poste, pour UI et M2
ATTRIBUTS_M1 = ("seuil_pourcentage", "postes_dus", "postes_non_dus",
                "postes_non_evaluables", "postes")
CLES_POSTE_M1 = ("poste", "classe", "restant_h", "plafond_h",
                 "restant_pourcentage")

# Valeurs qu'un capteur natif peut porter SANS etre une mesure. Aucune ne vaut
# zero, aucune ne vaut « non du » (ASP-INV-74, ASP-INV-76).
ILLISIBLES_M1 = ("unavailable", "unknown", "none", "", "abc", "  ")

# ═════════════════════════════════════════════════════════════
# NOTIFICATIONS — lot N1, PROJECTION PERSISTANTE (ASP-CI-37 … ASP-CI-39)
#
# N1 est un lot de NOTIFICATIONS : des automations de projection, lecteurs
# purs, sans aucune ecriture vers l'appareil ni vers le verdict. Les
# identifiants ne sont PAS inventes ici : ils sont ATTRIBUES par l'operateur
# (A-3, rendu en V4 — 07_MACHINE_L2.md §7, 11_ARBITRAGES_RENDUS.md §6.6), et
# les figer dans ce module fait echouer un renommage silencieux (ASP-INV-58).
#
# CE QUE N1 IMPLEMENTE, ET CE QU'IL DIFFERE — etabli avant codage.
#
#   Canal 2, entretien requis    -> IMPLEMENTE. Son autorite existe et elle
#                                   est deployee : les deux entites derivees
#                                   du lot M1.
#   Canal 1, cycle en cours      -> DIFFERE au lot L2. 08_NOTIFICATIONS.md §3
#                                   fixe son autorite : le verdict persistant,
#                                   apparition en classe O, extinction « a
#                                   toute valeur de classe T, sans exception ».
#                                   Or 07_MACHINE_L2.md §4.1 etablit que, sur
#                                   les dix-huit valeurs du vocabulaire L1, la
#                                   CLASSE T EST VIDE. L'autorite de creation
#                                   existe ; celle de SUPPRESSION n'existe pas.
#                                   Une projection livree maintenant creerait
#                                   une notification qu'aucun etat ne pourrait
#                                   plus eteindre, et transformerait le verdict
#                                   L1 FIGE — `LANCEE/DEMARRAGE_OBSERVE`, seule
#                                   valeur de classe O — en preuve permanente
#                                   de cycle courant. Substituer le temoin de
#                                   session natif adopterait une mission
#                                   externe, ce que 07 §6.2 interdit (D-06,
#                                   D-R4) et qu'ASP-INV-47 refuse deja.
#                                   10_LOTS.md §2 range d'ailleurs « automation
#                                   de projection de mission » dans le lot L2.
#   Canal 3, erreur robot/dock   -> DIFFERE a L2/W3. `A-8` conditionne l'envoi
#                                   mobile a « PENDANT une mission Arsenal »,
#                                   et 07 §5.1 n'en connait qu'une definition :
#                                   verdict en classe O. Le verdict L1 etant
#                                   fige, « pendant une mission » serait
#                                   indiscernable de « apres n'importe quelle
#                                   mission passee » : chaque erreur ulterieure
#                                   partirait en push HORS MISSION, contre
#                                   ASP-INV-84 et contre la seconde branche
#                                   d'`A-8` elle-meme. 07 §7.0 attribue de plus
#                                   l'envoi mobile au ROLE 1 — la supervision
#                                   W3, `10280000000001`, lot L2.
#
# Aucun invariant neuf, aucun contrat modifie. N1 rend opposables des
# obligations deja posees : ASP-INV-76 (aucune echeance conclue sur une donnee
# absente), ASP-INV-77 (aucune remise a zero automatique), ASP-INV-83
# (cloisonnement des trois objets), ASP-INV-84 (rien hors mission).
# ═════════════════════════════════════════════════════════════

DOSSIER_N1 = "11_automations/aspirateur"
RUNTIME_N1 = DOSSIER_N1 + "/notification_entretien.yaml"

# Identifiants d'automation. ATTRIBUES par l'operateur, jamais deduits.
AID_N1_MISSION = "10280000000002"       # projection persistante de mission
AID_N1_MAINTENANCE = "10280000000003"   # projection persistante de maintenance
# AMENDEMENT L2 — le dossier d'automations du domaine porte desormais TROIS
# automations : la supervision W3, la projection de mission et la projection
# d'entretien. La table nomme chacune AVEC son fichier : un identifiant
# deplace d'un fichier a l'autre echoue, la ou un simple ensemble d'IDs
# l'aurait laisse passer.
# AMENDEMENT U0 — `...04` est ATTRIBUE : `A-5` est clos, et l'automation de
# remise a zero de la composition existe (A-12). Le dossier porte donc QUATRE
# automations de natures differentes. `AID_HORS_N1` devient VIDE et reste en
# place : c'est le point d'accroche d'un futur identifiant differe, et le
# supprimer ferait disparaitre le mecanisme avec la donnee.
AID_U0_COMPOSITION = "10280000000004"   # remise a zero de la composition
AID_N1_AUTORISES = frozenset({"10280000000001", AID_N1_MISSION,
                              AID_N1_MAINTENANCE, AID_U0_COMPOSITION})
RUNTIME_U0_AUTO = DOSSIER_N1 + "/remise_a_zero_composition.yaml"
FICHIER_DE_L_AID = {
    "10280000000001": "11_automations/aspirateur/supervision_mission.yaml",
    AID_N1_MISSION: "11_automations/aspirateur/notification_mission.yaml",
    AID_N1_MAINTENANCE: RUNTIME_N1,
    AID_U0_COMPOSITION: RUNTIME_U0_AUTO,
}
AID_HORS_N1: dict[str, str] = {}
# Tout identifiant du domaine, quelle que soit sa valeur. Balaye le TEXTE du
# dossier, commentaires compris : le parseur YAML ne voit que les automations
# qu'il sait lire, et un identifiant cite ailleurs — une forme non couverte,
# un renvoi de commentaire — echapperait a la table `vus`.
AID_DOMAINE = re.compile(r"\b(1028\d{10})\b")

# ── VERROU N1/MISSION : la projection de cycle reste NON CONSTRUITE ────────
# Elle le reste tant que son autorite d'EXTINCTION n'existe pas, c'est-a-dire
# tant qu'aucune valeur de classe T n'est ecrite par un writer. Le verrou ne
# prouve pas que L2 sera correct le jour ou il existera : il rend la
# construction de cette projection VISIBLE et DELIBEREE — jamais accidentelle.
# Le lever exige de modifier CE module, sous revue, en meme temps que le
# runtime. C'est le meme mecanisme que le verrou transitoire de `M0`.
#
# ── VERROU LEVE PAR LE LOT L2, ET PAR LUI SEUL ────────────────────────────
# La condition posee est REALISEE, et elle l'est par le lot qui fournit
# l'autorite manquante : `CLASSE_T` compte desormais HUIT valeurs — trois
# clotures ecrites par le script de conduite, cinq par la supervision. La
# projection de cycle peut donc s'eteindre, et elle a un writer.
# Le verrou n'est pas retire du module : il est mis a `False`, de sorte que
# l'histoire du refus reste lisible et qu'un retour en arriere reste possible
# sans reecrire le controle.
VERROU_N1_MISSION = False

# Identifiants de notification. FERMES : 08_NOTIFICATIONS.md §1 en fixe deux,
# un par canal persistant, et le lot n'en instancie qu'un.
NOTIF_N1_ENTRETIEN = "aspirateur_entretien"
NOTIF_N1_MISSION = "aspirateur_mission"
NOTIF_N1_FERMES = frozenset({NOTIF_N1_ENTRETIEN, NOTIF_N1_MISSION})
# Ce que N1 instancie REELLEMENT. La difference avec l'ensemble ferme est le
# volet differe, et elle est verifiee — pas seulement commentee.
NOTIF_N1_INSTANCIES = frozenset({NOTIF_N1_ENTRETIEN, NOTIF_N1_MISSION})

TITRE_N1_ENTRETIEN = "\U0001F9F0 Aspirateur \u2013 Entretien requis"
TITRE_N1_MISSION = "\U0001F916 Aspirateur \u2013 Mission en cours"
# Readiness : le patron du depot, et le seul admis pour la re-projection.
READINESS_N1 = "input_boolean.systeme_stable"
# Autorite metier de la projection d'entretien — les deux entites de M1, et
# elles seules. Toute autre entite lue serait une seconde autorite.
AUTORITE_N1 = (ENTITE_M1_LISTE, ENTITE_M1_TEMOIN)
# Le SEUL attribut que le message a le droit de lire. Lire `postes`,
# `postes_non_dus` ou `seuil_pourcentage` ouvrirait la duree chiffree que
# 08_NOTIFICATIONS.md §4.2 proscrit, et la date que 14 §2 refuse.
ATTRIBUT_N1_MESSAGE = "postes_dus"
# Le MEME attribut borne le declencheur de liste, et c'est la meme raison.
# Un declencheur d'etat sans `to:`, `from:` ni `attribute:` passe en
# `match_all` : il part sur tout changement d'attribut, `postes` compris —
# donc a chaque decroissance d'un compteur natif. Ce que le declencheur
# surveille et ce que le message rend sont ainsi la meme donnee, et ils le
# restent : deplacer l'un deplace l'autre.
ATTRIBUT_N1_DECLENCHEUR = ATTRIBUT_N1_MESSAGE
# Etat de synthese, UNIQUE et SCALAIRE, qui autorise la disqualification.
# Une liste de valeurs acceptees y glisserait `unknown` ou `unavailable` sans
# casser le nominal : c'est la mutation que la garde structurelle refuse.
ETAT_N1_SUPPRESSION = ETAT_M1_AUCUN
# Modes admis. `single` abandonnerait EN SILENCE le second declenchement d'un
# franchissement de seuil — les deux entites d'autorite mutent dans le meme
# cycle ; `queued` rejouerait un rendu deja perime. Les trois precedents de
# projection persistante du depot portent `restart`.
MODES_N1 = frozenset({"restart"})
# AMENDEMENT L2 — le dossier porte trois automations de natures DIFFERENTES.
# Les interdits d'ASP-CI-39 ne peuvent donc plus etre une liste unique : un
# lecteur pur et un ecrivain du verdict n'ont pas les memes droits, et leur
# appliquer les memes regles rendrait le controle soit inutile, soit faux.
# La table ci-dessous nomme, fichier par fichier, ce que chacun a le droit de
# lire et d'appeler. Un fichier absent de la table est REFUSE : le dossier est
# ferme, et un quatrieme objet n'y apparait pas en silence.
SCRIPT_MOBILE = "script.notification_envoyer_avance"
# Le SEUL objet que l'automation de remise a zero appelle (lot U0).
SCRIPT_U0_REINIT = "script.aspirateur_reinitialiser_composition"
CIBLE_MOBILE = "input_text.telephone_parent_1_notify"
# La projection d'entretien lit ses deux entites d'autorite ; celle de mission
# lit le verdict et sa derivation lisible ; la supervision lit le verdict, les
# trois temoins de l'appareil et la cible mobile.
AUTORITE_PAR_FICHIER = {
    RUNTIME_N1: frozenset(AUTORITE_N1) | {READINESS_N1},
    "11_automations/aspirateur/notification_mission.yaml":
        frozenset({"input_text.aspirateur_mission_verdict",
                   "sensor.aspirateur_motif_lisible", READINESS_N1}),
    "11_automations/aspirateur/supervision_mission.yaml":
        # `vacuum.roborock_q7_max` y est LU, et seulement lu : c'est le
        # SEUL temoin du domaine qui dise « pose sur sa base » (07 §5.0),
        # donc le seul qui puisse prouver un amarrage POSITIVEMENT. Sa
        # lecture n'ouvre aucune seconde autorite : la supervision ne
        # commande jamais l'appareil, et l'interdit de commande ci-dessous
        # reste porte par SERVICES_PAR_FICHIER, qui ne contient aucun
        # service `vacuum.*`.
        frozenset({"input_text.aspirateur_mission_verdict",
                   "sensor.roborock_q7_max_etat",
                   "sensor.roborock_q7_max_erreur_de_l_aspirateur",
                   "sensor.roborock_q7_max_dock_erreur_de_dock",
                   "vacuum.roborock_q7_max",
                   READINESS_N1, CIBLE_MOBILE}),
    # AMENDEMENT U0 — quatrieme nature : la remise a zero de la composition.
    # Elle LIT le verdict — exception nominative d'ASP-CI-11 ci-dessous — et
    # le readiness, rien d'autre. Elle n'ecrit aucun helper elle-meme : le
    # script de remise a zero est le seul ecrivain (A-12).
    RUNTIME_U0_AUTO: frozenset({"input_text.aspirateur_mission_verdict",
                                READINESS_N1}),
}
SERVICES_PAR_FICHIER = {
    RUNTIME_N1: frozenset({"persistent_notification.create",
                           "persistent_notification.dismiss"}),
    "11_automations/aspirateur/notification_mission.yaml":
        frozenset({"persistent_notification.create",
                   "persistent_notification.dismiss"}),
    "11_automations/aspirateur/supervision_mission.yaml":
        frozenset({"input_text.set_value", SCRIPT_MOBILE}),
    RUNTIME_U0_AUTO: frozenset({SCRIPT_U0_REINIT}),
}
# Les deux LECTEURS PURS : ils ne doivent ecrire aucun verdict, ni commander.
PROJECTIONS_PURES = frozenset({
    RUNTIME_N1, "11_automations/aspirateur/notification_mission.yaml"})
# Types de condition que l'evaluateur de scenarios sait rendre FIDELEMENT. Un
# type absent d'ici fait ECHOUER le controle, jamais passer : un evaluateur
# silencieusement incomplet rendrait un faux vert.
CONDITIONS_N1_RENDABLES = frozenset({"state", "template"})
# Services d'envoi mobile, sous toutes leurs formes dans le depot. N1 n'en
# appelle AUCUN : le canal 3 est differe.
MOBILE_N1 = ("notify.", "notify:", "script.notification_envoyer",
             "notification_envoyer_famille", "notification_envoyer_avance",
             "telephone_parent_1_notify", "telephone_parent_2_notify")
# Lexique d'ERREUR robot/dock. Aucune notification persistante ne le porte :
# hors mission, le domaine n'ajoute rien (ASP-INV-84), et une erreur n'est pas
# un entretien (ASP-INV-83).
ERREUR_N1 = ("erreur_de_dock", "erreur_de_l_aspirateur", "dock_erreur",
             "ERREUR_EN_MISSION", "MISSION_INTERROMPUE")
# Jetons du vocabulaire de verdict L1 dont la CITATION dans ce lot trahirait
# une deduction de « cycle en cours ». La garde qui les consomme :
#   · INTERDIT de prendre le verdict L1 FIGE pour autorite d'un cycle
#     courant — sur les dix-huit valeurs deployees, la classe T est VIDE
#     (07_MACHINE_L2.md §4.1), donc rien n'eteindrait une telle projection ;
#   · CONTRIBUE au verrou qui empeche l'implementation prematuree de
#     l'automation `10280000000002`, aux cotes de `VERROU_N1_MISSION` ;
#   · NE CONSTITUE PAS une supervision L2 et ne prouve l'existence d'AUCUN
#     terminal de classe T. Elle constate une absence, elle ne la comble pas.
# La liste melange deliberement des jetons de classe O et de classe H : elle
# ne classe rien, elle refuse une citation. L'inclusion d'un jeton de classe H
# ne fait que rendre la garde plus stricte.
VERDICT_FIGE_N1 = ("LANCEE/DEMARRAGE_OBSERVE", "DEMARRAGE_OBSERVE",
                   "EMISSION/COMMANDE_ACCEPTEE", "COMMANDE_ACCEPTEE")
# Temoins natifs de session et d'activite : les lire ici adopterait une
# mission externe (07 §6.2, ASP-INV-47).
SESSION_NATIVE_N1 = ("binary_sensor.roborock_q7_max_nettoyage",
                     "sensor.roborock_q7_max_etat",
                     "vacuum.roborock_q7_max")
# Helpers d'INTENTION — couche U0. Le lot n'existe pas, et N1 ne le prejuge pas.
INTENTION_N1 = ("input_select.aspirateur", "input_boolean.aspirateur",
                "input_number.aspirateur", "input_text.aspirateur")
# Lexique de PREDICTION. Le seuil se constate, il ne se prevoit pas (14 §2).
PREDICTION_N1 = ("prochaine echeance", "prochaine échéance", "date prevue",
                 "date prévue", "prevu le", "prévu le", "dans environ",
                 "d'ici le", "tendance", "estimation", "estimé le",
                 "estime le", "sera du le", "sera dû le")

# Repli numerique, sous ses formes courantes : `| float(0)`, `| int(0)`,
# `| default(0)`. C'est EXACTEMENT ce que le lot s'interdit — une valeur de
# repli transformerait un trou d'information en mesure nominale.
REPLI_NUMERIQUE = re.compile(
    r"\|\s*(?:float|int)\s*\(\s*[^)\s]|\|\s*default\s*\(\s*[-+]?[\d'\"]")
# Primitives TEMPORELLES : elles ouvrent la date, la tendance et le rythme.
# Le domaine CONSTATE un seuil, il ne le prevoit pas (14 §2).
TEMPOREL_M1 = ("now(", "utcnow(", "today_at(", "as_timestamp(", "timedelta(",
               "as_datetime(", "strptime(", "relative_time(", "time_since(",
               "time_until(", "last_changed", "last_updated", "last_reported",
               "states.sensor", "states.binary_sensor")
# Tout appel de service, quel qu'il soit : un capteur template n'en emet
# aucun, et on le PROUVE plutot que de l'affirmer.
SERVICE_M1 = re.compile(
    r"^[^\S\n]*(?:-[^\S\n]*)?(?:service|action|perform_action)[^\S\n]*:", re.M)
# Notification, sous ses deux formes de plateforme.
NOTIFICATION_M1 = ("persistent_notification", "notify.", "notify:")

# Un appel de `button.press` sous une cle de service, quelle que soit la facon
# de viser la cible. C'est le SERVICE qui est garde, pas le ciblage.
PRESS_SERVICE = re.compile(
    r"^[^\S\n]*(?:-[^\S\n]*)?(?:service|action|perform_action)"
    r"[^\S\n]*:[^\S\n]*[\"']?(button\.press)", re.M)
# `BOUTON_ENTRETIEN_RE` est declare PLUS HAUT, avec le visiteur recursif du
# lot M2 qui le consomme des le calcul de `VISITEUR_YAML_RECURSIF`. Une seule
# definition : deux expressions pour la meme famille deriveraient.
# Repetitions interdites autour d'une pression.
REPETITION = re.compile(r"^[^\S\n]*(?:-[^\S\n]*)?(repeat|until|while|count)"
                        r"[^\S\n]*:", re.M)
FICHIER_INDEX = "README.md"

# ── Ancre 2 : constantes de module, jamais relues du contrat ────────────────

# Énumérations natives attestées par l'audit §3.1. Ne pas élargir sans preuve.
FAN_SPEEDS_AUTORISEES = {"quiet", "balanced", "turbo", "max"}
WATER_LEVELS_ATTESTES = {"off", "low", "medium", "high", "custom_water_flow"}
FAN_SPEED_EXCLUE = "gentle"

# Classification contractuelle ATTENDUE des états (contrat 07 §5.0). Figée ici :
# c'est ce qui rend un DÉPLACEMENT d'état entre classes détectable, là où une
# simple vérification de disjonction le laisserait passer. `returning_home` et
# `docking` relèvent du mouvement — fait établi par le contrat alarme
# (ALM-ROBO-1) : côté entité `vacuum`, tous deux sont mappés sur `returning`.
PARTITION_ATTENDUE = {
    "R": frozenset({"charger_disconnected", "charging"}),
    "A": frozenset({"cleaning", "segment_cleaning", "zoned_cleaning",
                    "paused", "returning_home", "docking"}),
    "E": frozenset({"error", "device_offline", "unknown", "unavailable"}),
}
CLASSE_NON_QUALIFIEE = "N"
CODE_ETAT_NON_QUALIFIE = "ETAT_NON_QUALIFIE"
CODE_TRANSITION = "TRANSITION_NON_OBSERVEE"

# Segments observés dans une carte mais SANS rôle métier V1 (contrat 02 §2,
# QO-1). Attestés par l'audit, ils doivent rester hors de la table canonique.
SEGMENTS_NON_COMMANDABLES = {"2_17", "2_18"}
# Carte observée sans aucun segment nommé — jamais commandable (audit §4).
CARTE_SANS_SEGMENT = "Garage"

# Vocabulaire canonique des états (08 §1). Dix codes, aucun synonyme.
ETATS_CANONIQUES = (
    "mission_ouverte", "nettoyage_reel", "pause", "erreur", "retour_base",
    "amarrage", "charge", "repos_hors_base", "indisponibilite",
    "etat_non_qualifie")
# `mission_ouverte` dérive du TÉMOIN DE SESSION, pas de l'état machine : il se
# superpose aux neuf autres et n'a donc aucune image dans la partition.
ETAT_ORTHOGONAL = "mission_ouverte"
# Image attendue partition (07 §5.0) -> code canonique (08 §1).
IMAGE_ATTENDUE = {
    "charger_disconnected": "repos_hors_base", "charging": "charge",
    "cleaning": "nettoyage_reel", "segment_cleaning": "nettoyage_reel",
    "zoned_cleaning": "nettoyage_reel", "paused": "pause",
    "returning_home": "retour_base", "docking": "amarrage",
    "error": "erreur", "device_offline": "indisponibilite",
    "unknown": "indisponibilite", "unavailable": "indisponibilite"}
CODE_CANONIQUE_CLASSE_N = "etat_non_qualifie"
# i-2 — codes canoniques admis pour chaque classe explicite de la partition.
# Lier les deux ancres par la CLASSE, et pas seulement par l'ensemble des états,
# est ce qui rend détectable un DÉPLACEMENT d'état entre classes à image
# inchangée : `charging` passé de R à A garderait l'image `charge`, qui
# n'appartient pas aux codes de la classe A.
CODES_PAR_CLASSE = {
    "R": {"charge", "repos_hors_base"},
    "A": {"nettoyage_reel", "pause", "retour_base", "amarrage"},
    "E": {"erreur", "indisponibilite"}}

# Fenêtres temporelles contractuelles (07 §3.1). Deux valeurs, et deux seulement.
FENETRE_CONFIRMATION_S = 30
FENETRE_TRANSITION_S = 60
ETAPES_CONFIRMATION = ("7", "8", "10")
# Cartes portant un référentiel commandable. Le Garage n'y figure pas et ne
# doit pas y être promu (contrat 01 §5, ASP-INV-2).
CARTES_COMMANDABLES = {"0", "1", "2"}
CARTE_NON_PROMUE = "Garage"

# ── Ciblage LEXICAL des identifiants du domaine (I1) ───────────────────────
# La protection ne repose sur AUCUNE liste de domaines Home Assistant : une
# telle liste se prétendrait exhaustive et laisserait passer `plant.aspirateur_x`
# ou `sun.aspirateur_x` le jour où le domaine manque. Un jeton est examiné dès
# qu'il désigne LEXICALEMENT ce domaine — objet mentionnant l'aspirateur ou le
# robot — ou qu'il relève des deux domaines propres à l'appareil.
MARQUEURS_DOMAINE = ("roborock", "aspirateur")
ROBOT_DOMAINS = frozenset({"vacuum", "roborock"})
# Domaines de helpers/objets Arsenal. Cette liste n'influe QUE sur le libellé du
# diagnostic : un domaine absent d'ici reste refusé par la règle d'attestation.
# La détection ne dépend donc d'aucune énumération.
ARSENAL_HELPER_DOMAINS = frozenset({
    "automation", "counter", "group", "input_boolean", "input_button",
    "input_datetime", "input_number", "input_select", "input_text", "scene",
    "schedule", "script", "timer", "todo",
})
# Primitives de SERVICE documentées. Ce ne sont pas des `entity_id` : elles
# restent néanmoins soumises à l'attestation par l'audit.
SERVICE_PRIMITIVES = frozenset({
    "vacuum.send_command", "vacuum.start", "vacuum.pause", "vacuum.stop",
    "vacuum.return_to_base", "vacuum.set_fan_speed", "vacuum.clean_area",
    "vacuum.locate", "vacuum.clean_spot", "select.select_option",
})
# Domaines dont un appel de service commanderait le robot en contournant
# l'écrivain unique (ASP-CI-7).
SERVICE_DOMAINS_INTERDITS = ("vacuum", "roborock")
# Domaines d'entités natives capables d'ACTION sur le robot.
ACTION_DOMAINS = ("vacuum", "select", "button")


# ─────────────────────────────────────────────────────────────
# Neutralisation des blocs de code clôturés
# ─────────────────────────────────────────────────────────────

def strip_fences(texte: str) -> str:
    """Neutralise les blocs de code clôturés, lignes de clôture comprises.

    Reproduit strictement la sémantique de `strip_fenced_code`
    (scripts/docs_navigation/audit_doc_links.py), déjà employée par DOC-CI-1 et
    DOC-CI-2 pour ce motif exact : une ligne dont le contenu strippé commence
    par ``` bascule l'état et est elle-même marquée « dans la clôture ».
    Reproduite plutôt qu'importée : un checker de contrat ne dépend d'aucun
    autre outil du dépôt. Le nombre de lignes est conservé.
    """
    sortie: list[str] = []
    dans_cloture = False
    for ligne in texte.splitlines():
        if ligne.strip().startswith("```"):
            sortie.append("")
            dans_cloture = not dans_cloture
            continue
        sortie.append("" if dans_cloture else ligne)
    return "\n".join(sortie)


def sans_clotures(textes: dict[str, str]) -> dict[str, str]:
    return {nom: strip_fences(txt) for nom, txt in textes.items()}


# ─────────────────────────────────────────────────────────────
# ASP-CI-1 — intégrité des invariants
# ─────────────────────────────────────────────────────────────

DECL_INV = re.compile(r'^> \*\*`ASP-INV-(\d+)`', re.M)
DECL_INV_LAXE = re.compile(r'^> \*\*(?:Invariant\s+)?`?ASP-INV-(\d+)`?', re.M)
DECL_IMC = re.compile(r'^> ### `ASP-IMC-1`', re.M)


def check_invariants(textes: dict[str, str]) -> list[str]:
    """Attend des textes DÉJÀ débarrassés de leurs blocs de code."""
    errs: list[str] = []
    stricts: list[int] = []
    laxes: list[int] = []
    for _, txt in sorted(textes.items()):
        stricts += [int(m.group(1)) for m in DECL_INV.finditer(txt)]
        laxes += [int(m.group(1)) for m in DECL_INV_LAXE.finditer(txt)]
    if not stricts:
        errs.append("ASP-CI-1 : aucun invariant `ASP-INV-n` déclaré dans le domaine.")
        return errs
    divergents = sorted(set(laxes) - set(stricts))
    if divergents:
        errs.append(
            "ASP-CI-1 : format de déclaration non uniforme pour "
            f"ASP-INV-{', '.join(str(n) for n in divergents)} — attendu "
            "`> **`ASP-INV-n`**`.")
    doublons = sorted({n for n in stricts if stricts.count(n) > 1})
    if doublons:
        errs.append("ASP-CI-1 : invariant(s) déclaré(s) plusieurs fois : "
                    + ", ".join(f"ASP-INV-{n}" for n in doublons) + ".")
    trous = [n for n in range(1, max(stricts) + 1) if n not in set(stricts)]
    if trous:
        errs.append("ASP-CI-1 : numérotation trouée — manque "
                    + ", ".join(f"ASP-INV-{n}" for n in trous) + ".")
    imc = sum(len(DECL_IMC.findall(t)) for t in textes.values())
    if imc != 1:
        errs.append(f"ASP-CI-1 : `ASP-IMC-1` doit être défini exactement une fois "
                    f"(trouvé {imc}).")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-2 — référentiel, ancré sur l'audit
# ─────────────────────────────────────────────────────────────

SEGMENT_CANON = re.compile(
    r'^\| `(\d+_\d+)` \| \*\*([^*\n]+)\*\*'
    r'(?:[^\S\n]*\|[^\S\n]*(?:`([^`\n]*)`|([^|`\n]*?))[^\S\n]*\|)?',
    re.M)
PERIMETRE = re.compile(
    r'^\| \*\*([^*|\n]+)\*\* \| `(\d)` \| ([^|\n]+) \|$', re.M)
SEGMENT_REF = re.compile(r'`(\d+_\d+)`')
# Table §5.1 de l'audit : | `0_16` | `Salon` | RDC |
AUDIT_SEGMENT = re.compile(
    r'^\| `(\d+_\d+)` \| `([^`\n]+)` \| ([^|\n]+?)[^\S\n]*\|', re.M)
# Table §4 de l'audit : | **0** | `RDC` | 4 |
AUDIT_CARTE = re.compile(r'^\| \*\*(\d)\*\* \| `([^`\n]+)`', re.M)


def parse_segments(t02: str) -> dict[str, tuple[str, str]]:
    """Renvoie {segment: (libellé canonique Arsenal, nom Roborock si divergent)}."""
    out: dict[str, tuple[str, str]] = {}
    for seg, libelle, roboro_bt, roboro_nu in SEGMENT_CANON.findall(t02):
        divergent = (roboro_bt or roboro_nu or "").strip().strip("`").strip()
        if divergent in {"—", "-", ""}:
            divergent = ""
        out[seg] = (libelle.strip(), divergent)
    return out


def parse_audit_segments(audit: str) -> dict[str, tuple[str, str]]:
    """Renvoie {segment: (nom Roborock, nom de carte)} depuis l'audit §5.1."""
    return {seg: (nom.strip(), carte.strip())
            for seg, nom, carte in AUDIT_SEGMENT.findall(audit)}


def check_referentiel(t02: str, t10: str, audit: str) -> list[str]:
    errs: list[str] = []
    canon = parse_segments(t02)
    if not canon:
        errs.append("ASP-CI-2 : table canonique des segments introuvable "
                    "(02 §2) — le référentiel du domaine est vide.")
        return errs

    # ---- Ancre 1 : attestation par l'audit --------------------------------
    atteste = parse_audit_segments(audit)
    cartes_audit = dict(AUDIT_CARTE.findall(audit))
    if not atteste:
        errs.append("ASP-CI-2 : table des segments introuvable dans l'audit du "
                    "domaine — le référentiel ne peut pas être attesté.")
    else:
        for seg in sorted(canon):
            libelle, divergent = canon[seg]
            attendu = divergent or libelle
            if seg not in atteste:
                errs.append(f"ASP-CI-2 : segment `{seg}` de la table canonique "
                            "ABSENT de l'audit du domaine — un segment non relevé "
                            "ne peut pas être commandable.")
                continue
            nom_audit, carte_audit = atteste[seg]
            if attendu != nom_audit:
                errs.append(f"ASP-CI-2 : segment `{seg}` — le contrat attend le "
                            f"nom Roborock « {attendu} », l'audit atteste "
                            f"« {nom_audit} ». Incohérence du contrat.")
            index = seg.split("_", 1)[0]
            if index not in CARTES_COMMANDABLES:
                errs.append(f"ASP-CI-2 : segment `{seg}` — index de carte "
                            f"`{index}` hors des cartes commandables "
                            f"{sorted(CARTES_COMMANDABLES)}.")
            elif index in cartes_audit and carte_audit not in cartes_audit[index]:
                errs.append(f"ASP-CI-2 : segment `{seg}` — l'index `{index}` "
                            f"désigne « {cartes_audit[index].strip()} » dans "
                            f"l'audit, mais le segment y appartient à "
                            f"« {carte_audit} ».")
            if carte_audit == CARTE_NON_PROMUE:
                errs.append(f"ASP-CI-2 : segment `{seg}` appartient au "
                            f"{CARTE_NON_PROMUE}, que le contrat ne promeut pas "
                            "(ASP-INV-2).")
        # Segments observés mais non commandables : attestés, et hors table.
        for seg in sorted(SEGMENTS_NON_COMMANDABLES):
            if seg not in atteste:
                errs.append(f"ASP-CI-2 : segment observé `{seg}` absent de "
                            "l'audit — la liste des non-commandables ne "
                            "correspond plus au relevé.")
            if seg in canon:
                errs.append(f"ASP-CI-2 : segment `{seg}` est observé mais NON "
                            "COMMANDABLE : il ne doit pas figurer à la table "
                            "canonique (QO-1).")

    # ---- Cohérence interne : périmètres et raccourcis ---------------------
    sources = (("02 §3 (périmètres prédéfinis)", t02), ("10 §3 (raccourcis)", t10))
    vus: set[str] = set()
    for label, txt in sources:
        lignes = PERIMETRE.findall(txt)
        if not lignes:
            errs.append(f"ASP-CI-2 : aucun périmètre lisible dans {label}.")
            continue
        for nom, carte, composition in lignes:
            segs = SEGMENT_REF.findall(composition)
            nom = nom.strip()
            if not segs:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) ne "
                            "désigne aucun segment.")
                continue
            vus.update(segs)
            inconnus = [s for s in segs if s not in canon]
            if inconnus:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) désigne "
                            f"un segment hors référentiel : {', '.join(inconnus)}.")
            cartes = {s.split("_", 1)[0] for s in segs}
            if len(cartes) > 1:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) agrège "
                            f"plusieurs cartes ({', '.join(sorted(cartes))}) — "
                            "violation de ASP-IMC-1.")
            elif cartes and carte not in cartes:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) déclare la "
                            f"carte `{carte}` mais désigne des segments de la "
                            f"carte `{cartes.pop()}`.")
    orphelins = sorted(set(canon) - vus)
    if orphelins:
        errs.append("ASP-CI-2 : segment(s) du référentiel jamais employés par un "
                    f"périmètre : {', '.join(orphelins)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-3 — clôture du catalogue des codes
# ─────────────────────────────────────────────────────────────

CODE_LIGNE = re.compile(r'^\| `([A-Z][A-Z_]{4,})`', re.M)
CODE_CITE = re.compile(r'`([A-Z][A-Z_]{4,})`')
LIGNE_CATALOGUE = re.compile(r'^\| `[A-Z][A-Z_]{4,}`.*$', re.M)
SECTION_RENVOIS = re.compile(r'^#{2,3} Renvois\s*$.*?(?=^#{1,3} |\Z)', re.M | re.S)


def split_catalogue(t09: str) -> tuple[set[str], set[str]]:
    try:
        apres = t09.split("## 2. Catalogue des refus", 1)[1]
        sec2, reste = apres.split("## 3. Catalogue des échecs", 1)
    except (IndexError, ValueError):
        return set(), set()
    sec3 = reste.split("\n## ", 1)[0]
    return set(CODE_LIGNE.findall(sec2)), set(CODE_LIGNE.findall(sec3))


def zone_productrice(nom: str, txt: str) -> str:
    """Texte où une citation vaut PRODUCTION d'un refus.

    Sont exclus : le catalogue lui-même (un motif ne se justifie pas seul), les
    sections de renvois (un pointeur n'est pas une règle) et l'index du domaine
    (il oriente, il ne norme pas). Les blocs de code sont déjà neutralisés en
    amont.
    """
    if nom == FICHIER_INDEX:
        return ""
    txt = SECTION_RENVOIS.sub("", txt)
    if nom == FICHIER_CATALOGUE:
        txt = LIGNE_CATALOGUE.sub("", txt)
    return txt


def check_codes(textes: dict[str, str]) -> list[str]:
    """Attend des textes DÉJÀ débarrassés de leurs blocs de code."""
    errs: list[str] = []
    refus, echecs = split_catalogue(textes.get(FICHIER_CATALOGUE, ""))
    if not refus or not echecs:
        errs.append("ASP-CI-3 : catalogue des refus ou des échecs illisible "
                    "(09 §2 / §3).")
        return errs
    connus = refus | echecs
    cites: set[str] = set()
    produits: set[str] = set()
    for nom, txt in textes.items():
        cites |= set(CODE_CITE.findall(txt))
        produits |= set(CODE_CITE.findall(zone_productrice(nom, txt)))
    orphelins = sorted(cites - connus)
    if orphelins:
        errs.append("ASP-CI-3 : code(s) cité(s) hors catalogue — un motif "
                    f"inexistant rend le refus inapplicable : {', '.join(orphelins)}.")
    # Règle bornée aux REFUS. Un refus est produit par une clause : s'il n'est
    # cité par aucune zone productrice, aucune règle ne le déclenche et il est
    # mort. Un ÉCHEC décrit une issue constatée après émission et se suffit de
    # sa définition — l'exiger ailleurs forcerait une redite sans valeur.
    morts = sorted(refus - produits)
    if morts:
        errs.append("ASP-CI-3 : motif(s) de refus au catalogue mais qu'aucune "
                    "clause ne produit — un renvoi, un index ou le catalogue "
                    f"lui-même ne comptent pas : {', '.join(morts)}.")
    chevauche = sorted(refus & echecs)
    if chevauche:
        errs.append("ASP-CI-3 : code(s) déclarés à la fois comme refus et comme "
                    f"échec : {', '.join(chevauche)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-4 — partition des états, ancrée sur les constantes
# ─────────────────────────────────────────────────────────────

# R1 — `[^|\n]` et non `[^|]` : une classe négative sans `\n` franchirait la
# ligne et laisserait une table malformée capturer de la prose ultérieure.
CLASSE = re.compile(
    r'^\| \*\*([RAEN]) — [^|\n]*\|([^|\n]*)\|([^|\n]*)\|', re.M)
ENUM_08 = re.compile(r'énumération \*\*non exhaustive\*\* : (.+?)…')
ETAT = re.compile(r'`([a-z][a-z_]+)`')


def bloc_partition(t07: str) -> str:
    try:
        return t07.split("### 5.0", 1)[1].split("### 5.1", 1)[0]
    except IndexError:
        return ""


def parse_partition(t07: str) -> dict[str, tuple[set[str], str]]:
    """Renvoie {classe: (états énumérés, cellule d'effet)}."""
    bloc = bloc_partition(t07)
    return {cls: (set(ETAT.findall(valeurs)), effet)
            for cls, valeurs, effet in CLASSE.findall(bloc)}


def check_partition(t07: str, t08: str) -> list[str]:
    errs: list[str] = []
    part = parse_partition(t07)
    attendues = set(PARTITION_ATTENDUE) | {CLASSE_NON_QUALIFIEE}
    if set(part) != attendues:
        errs.append("ASP-CI-4 : partition des états incomplète (07 §5.0) — "
                    f"classes trouvées : {sorted(part) or 'aucune'} ; "
                    f"attendu {sorted(attendues)}.")
        return errs

    # ---- Ancre 2 : classification figée dans ce module --------------------
    for cls, attendu in PARTITION_ATTENDUE.items():
        reel = part[cls][0]
        manquants = sorted(attendu - reel)
        surnumeraires = sorted(reel - attendu)
        if manquants:
            errs.append(f"ASP-CI-4 : classe {cls} — état(s) attendu(s) mais "
                        f"absent(s) : {', '.join(manquants)}.")
        if surnumeraires:
            deplaces = {v: c for c, a in PARTITION_ATTENDUE.items()
                        for v in surnumeraires if v in a and c != cls}
            for v in surnumeraires:
                if v in deplaces:
                    errs.append(f"ASP-CI-4 : état `{v}` DÉPLACÉ — attendu en "
                                f"classe {deplaces[v]}, trouvé en classe {cls}. "
                                "La classification attestée n'est pas "
                                "renégociable par édition du contrat.")
                else:
                    errs.append(f"ASP-CI-4 : classe {cls} — état `{v}` ajouté, "
                                "hors classification attestée.")
    # La classe N n'énumère rien : « toute autre valeur » n'est pas énumérable.
    if part[CLASSE_NON_QUALIFIEE][0]:
        errs.append("ASP-CI-4 : la classe N ne doit énumérer aucune valeur — "
                    "elle absorbe par définition tout ce qui n'est pas nommé.")

    # ---- Lien classe N → refus par défaut → ETAT_NON_QUALIFIE -------------
    effet_n = part[CLASSE_NON_QUALIFIEE][1]
    if CODE_ETAT_NON_QUALIFIE not in effet_n:
        errs.append(f"ASP-CI-4 : la classe N ne produit pas "
                    f"`{CODE_ETAT_NON_QUALIFIE}` — sans ce lien, un état inconnu "
                    "n'a plus de motif de refus nommé.")
    bloc = bloc_partition(t07)
    regle_defaut = [m for m in DECL_INV.finditer(bloc)]
    if not regle_defaut:
        errs.append("ASP-CI-4 : aucune règle de refus par défaut déclarée en "
                    "07 §5.0 — la classe N n'est pas opposable.")
    elif CODE_ETAT_NON_QUALIFIE not in bloc.split(regle_defaut[0].group(0), 1)[1]:
        errs.append(f"ASP-CI-4 : la règle de refus par défaut de 07 §5.0 ne nomme "
                    f"pas `{CODE_ETAT_NON_QUALIFIE}`.")

    # ---- Couverture des états cités ailleurs dans le domaine --------------
    tous = {v for cls in PARTITION_ATTENDUE for v in part[cls][0]}
    m = ENUM_08.search(t08)
    if not m:
        errs.append("ASP-CI-4 : énumération des états introuvable en 08 §2.")
        return errs
    non_classes = sorted(set(ETAT.findall(m.group(1))) - tous)
    if non_classes:
        errs.append("ASP-CI-4 : état(s) cité(s) par le domaine mais non classés "
                    f"par la partition : {', '.join(non_classes)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-5 — table des profils
# ─────────────────────────────────────────────────────────────

PROFIL = re.compile(
    r'^\| \*\*([^*|\n]+)\*\* \| `([a-z_]+)` \| `([a-z_]+)` \|', re.M)


def parse_profils(t03: str) -> list[tuple[str, str, str]]:
    try:
        bloc = t03.split("## 1. Table canonique", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        return []
    return PROFIL.findall(bloc)


def check_profils(t03: str) -> list[str]:
    errs: list[str] = []
    profils = parse_profils(t03)
    if len(profils) != NB_PROFILS:
        errs.append(f"ASP-CI-5 : la table des profils doit en compter "
                    f"{NB_PROFILS} (trouvé {len(profils)}).")
    if not profils:
        return errs
    noms = [p[0].strip() for p in profils]
    if len(set(noms)) != len(noms):
        errs.append("ASP-CI-5 : deux profils portent le même libellé.")
    for nom, fan, eau in profils:
        nom = nom.strip()
        if fan == FAN_SPEED_EXCLUE:
            errs.append(f"ASP-CI-5 : profil « {nom} » emploie `{FAN_SPEED_EXCLUE}`, "
                        "explicitement exclu par ASP-INV-11.")
        elif fan not in FAN_SPEEDS_AUTORISEES:
            errs.append(f"ASP-CI-5 : profil « {nom} » — aspiration `{fan}` hors "
                        f"énumération attestée {sorted(FAN_SPEEDS_AUTORISEES)}.")
        if eau not in WATER_LEVELS_ATTESTES:
            errs.append(f"ASP-CI-5 : profil « {nom} » — intensité d'eau `{eau}` "
                        f"hors énumération attestée {sorted(WATER_LEVELS_ATTESTES)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-6 — identifiants, attestation par jeton exact
# ─────────────────────────────────────────────────────────────

JETON = re.compile(r'\b([a-z][a-z0-9_]*)\.([a-z0-9_]+)\b')


def tous_les_jetons(texte: str) -> set[str]:
    """Tous les jetons `<domaine>.<objet>` du texte, sans filtrage."""
    return {f"{d}.{o}" for d, o in JETON.findall(texte)}


def concerne_le_domaine(jeton: str) -> bool:
    """Le jeton désigne-t-il ce domaine ?

    Deux voies, aucune ne reposant sur une liste de domaines Home Assistant :
    l'objet mentionne l'aspirateur ou le robot, ou le domaine est l'un des deux
    propres à l'appareil (`vacuum.`, `roborock.`). C'est ce qui écarte un nom de
    fichier (`07_moteur_de_mission.md`) ou un littéral (`image.png`) sans avoir à
    énumérer quoi que ce soit.
    """
    domaine, objet = jeton.split(".", 1)
    return domaine in ROBOT_DOMAINS or any(m in objet for m in MARQUEURS_DOMAINE)


def jetons_du_domaine(texte: str) -> set[str]:
    return {j for j in tous_les_jetons(texte) if concerne_le_domaine(j)}


def check_identifiants(textes: dict[str, str], audit: str) -> list[str]:
    """Attend des textes DÉJÀ débarrassés de leurs blocs de code."""
    errs: list[str] = []
    if not audit:
        errs.append("ASP-CI-6 : audit factuel du domaine introuvable — aucun "
                    "identifiant ne peut être attesté.")
        return errs
    # L'attestation se fait contre TOUS les jetons de l'audit : la comparaison
    # est une appartenance exacte, jamais une sous-chaîne.
    attestes = tous_les_jetons(audit)
    cites: set[str] = set()
    for txt in textes.values():
        cites |= jetons_du_domaine(txt)
    for jeton in sorted(cites):
        # Comparaison par JETON ENTIER : un préfixe tronqué d'une entité réelle
        # ne passe pas, là où une recherche par sous-chaîne l'aurait laissé filer.
        if jeton in attestes:
            continue
        domaine = jeton.split(".", 1)[0]
        if domaine in ARSENAL_HELPER_DOMAINS:
            errs.append(f"ASP-CI-6 : `{jeton}` — un contrat antérieur au runtime "
                        "ne nomme aucun objet Arsenal ; ASP-INV-58 interdit d'en "
                        "proposer la valeur.")
        elif jeton in SERVICE_PRIMITIVES:
            errs.append(f"ASP-CI-6 : `{jeton}` est une primitive de service "
                        "documentée, mais elle n'est pas attestée par l'audit du "
                        "domaine.")
        else:
            errs.append(f"ASP-CI-6 : `{jeton}` n'est ni attesté par l'audit du "
                        "domaine, ni une primitive de service documentée.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-7 — aucune commande brute en Lovelace
# ─────────────────────────────────────────────────────────────

ROBOROCK_ACTION = re.compile(
    r'\b(?:' + "|".join(ACTION_DOMAINS) + r')\.[a-z0-9_]*roborock[a-z0-9_]*')
# Nom de service STATIQUE sous une clé Lovelace. La cible (`entity_id`,
# `device_id`, `area_id`, `label_id`) n'est pas regardée : c'est le SERVICE qui
# est interdit, pas la façon de le viser. Limites assumées et documentées en
# tête de module : un appel générique ciblé par `device_id`, un nom de service
# templatisé, et la portée globale de `vacuum.*` face à un futur second
# aspirateur.
APPEL_SERVICE = re.compile(
    r'^[^\S\n]*(?:-[^\S\n]*)?(?:service|action|perform_action)[^\S\n]*:[^\S\n]*["\']?'
    r'((?:' + "|".join(SERVICE_DOMAINS_INTERDITS) + r')\.[a-z0-9_]+)',
    re.M)


def check_lovelace(fichiers: dict[str, str]) -> list[str]:
    errs: list[str] = []
    for chemin, contenu in sorted(fichiers.items()):
        # Une mention en commentaire n'est pas un appel : on retire les lignes
        # dont le premier caractère non blanc est un dièse.
        utile = "\n".join(l for l in contenu.splitlines()
                          if not l.lstrip().startswith("#"))
        for trouve in sorted(set(ROBOROCK_ACTION.findall(utile))):
            errs.append(f"ASP-CI-7 : entité native d'action `{trouve}` exposée "
                        f"dans {chemin} — ASP-INV-31 impose le passage par "
                        "l'écrivain unique du domaine.")
        for service in sorted(set(APPEL_SERVICE.findall(utile))):
            errs.append(f"ASP-CI-7 : nom de service `{service}` sous une clé "
                        f"d'action dans {chemin} — une commande statiquement "
                        "nommée contourne l'écrivain unique, quel que soit le "
                        "mode de ciblage (ASP-INV-31).")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-8 — référentiel TECHNIQUE (02 §2.1), ancré sur l'audit
# ─────────────────────────────────────────────────────────────
#
# Le domaine porte DEUX référentiels qui ne doivent jamais se confondre :
#
#   - le référentiel MÉTIER (02 §2)    — libellés canoniques Arsenal, ce que le
#                                        système restitue et ce qu'il désigne ;
#   - le référentiel TECHNIQUE (02 §2.1) — valeurs exactes de l'appareil,
#                                        employées UNIQUEMENT pour écrire et
#                                        confirmer le contexte cartographique.
#
# La séparation est MÉCANIQUE, pas typographique : les deux tables ont des
# parseurs distincts, et ce contrôle vérifie explicitement qu'aucune ligne n'est
# capturée par les deux — une table technique que le parseur métier lirait comme
# un référentiel de désignation serait exactement la confusion que 02 §5 proscrit.
#
# ANCRE : l'audit. Une falsification COHÉRENTE du contrat — table métier, table
# technique, périmètres et raccourcis modifiés ensemble — reste détectée, car
# aucune des deux tables ne s'atteste elle-même.

TECH_CARTE = re.compile(
    r'^\| (?:`(\d)`|—) \| `([^`\n]*)` \| (commandable|non commandable) \|$', re.M)
TECH_SEGMENT = re.compile(
    r'^\| `(\d+_\d+)` \| `(\d+)` \| `([^`\n]*)` \| (commandable|non commandable) \|$',
    re.M)


def section_normative(texte: str, debut: str,
                      fin: str = "\n## ") -> str:
    """Bloc NORMATIF borné : de `debut` jusqu'à la borne suivante.

    Les gardes de clause s'appliquent à ce bloc et à lui seul : une phrase
    semblable placée dans un renvoi, un index ou une autre section ne satisfait
    aucune garde. Les blocs clôturés sont déjà neutralisés en amont (R3).
    """
    try:
        return texte.split(debut, 1)[1].split(fin, 1)[0]
    except IndexError:
        return ""


def bloc_technique(t02: str) -> str:
    """Bloc 02 §2.1 seul — jamais le référentiel métier qui le précède."""
    try:
        return t02.split("### 2.1", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        return ""


# M-2 — clauses qui rendent l'exception cartographique CLOSE. Chacune est
# localisée dans SA section normative : (bloc, ancre de début, motifs exigés).
CLAUSES_BORNAGE = (
    ("02 §2.1", "### 2.1", "\n## ",
     ("- **Ni une confirmation par cardinalité.**", "inclusion nominale"),
     "l'exception admettrait une confirmation par simple décompte des pièces"),
    ("02 §2.1", "### 2.1", "\n## ",
     ("- **Ni une autorité métier.**",),
     "le référentiel technique deviendrait une vérité de désignation"),
    ("02 §2.1", "### 2.1", "\n## ",
     ("- **Ni une donnée d'interface.**",),
     "les libellés d'appareil pourraient être exposés à l'opérateur"),
    ("02 §5", "## 5. Règle de restitution", "\n## ",
     ("| Écrire la sélection de carte |",
      "| Confirmer la sélection par relecture |",
      "| Confirmer les pièces exposées de la carte |"),
     "l'exception ne serait plus énumérée, donc plus close"),
    ("02 §5", "## 5. Règle de restitution", "\n## ",
     ("la comparaison est **littérale**", "approchée"),
     "un rapprochement approximatif deviendrait admissible"),
    ("06 §3", "## 3. Conditions de satisfaction", "\n### ",
     ("| 3 |", "comparaison **littérale**"),
     "la relecture du sélecteur ne serait plus littérale"),
    ("06 §3", "## 3. Conditions de satisfaction", "\n### ",
     ("| 4 |", "contiennent l'intégralité", "§2.1"),
     "la condition 4 ne serait plus fondée sur le référentiel technique"),
    ("06 §3.1", "### 3.1", "\n## ",
     ("Comment l'inclusion se constate", "§2.1", "**littérale**"),
     "le mécanisme d'inclusion nominale ne serait plus dit"),
)


def check_bornage_exception(t02: str, t06: str) -> list[str]:
    """M-2 — l'exception cartographique reste close, clause par clause."""
    errs: list[str] = []
    sources = {"02": t02, "06": t06}
    for section, debut, fin, motifs, consequence in CLAUSES_BORNAGE:
        corps = section_normative(sources[section.split()[0]], debut, fin)
        if not corps:
            errs.append(f"ASP-CI-8 : section {section} introuvable — la clause "
                        "de bornage ne peut plus être vérifiée.")
            continue
        for motif in motifs:
            if motif not in corps:
                errs.append(f"ASP-CI-8 : {section} — clause de bornage absente "
                            f"ou affaiblie ({motif!r} introuvable DANS cette "
                            f"section) : {consequence}.")
    return errs


def check_referentiel_technique(t02: str, t06: str, audit: str) -> list[str]:
    errs: list[str] = []
    bloc = bloc_technique(t02)
    if not bloc:
        return ["ASP-CI-8 : référentiel technique introuvable (02 §2.1) — la "
                "sélection et la confirmation de carte n'ont plus de source."]

    cartes = TECH_CARTE.findall(bloc)
    segments = TECH_SEGMENT.findall(bloc)
    if not cartes:
        errs.append("ASP-CI-8 : table technique des cartes introuvable (02 §2.1).")
    if not segments:
        errs.append("ASP-CI-8 : table technique des segments introuvable (02 §2.1).")
    if errs:
        return errs

    # ---- Séparation mécanique des deux référentiels ----------------------
    if SEGMENT_CANON.search(bloc):
        errs.append("ASP-CI-8 : le référentiel technique est capturé par le "
                    "parseur du référentiel MÉTIER — les deux tables se "
                    "confondent, la séparation de 02 §5 n'est plus mécanique.")
    if TECH_SEGMENT.search(t02.split("### 2.1", 1)[0]):
        errs.append("ASP-CI-8 : le référentiel métier contient une ligne au "
                    "format TECHNIQUE — un libellé d'appareil s'est glissé dans "
                    "la vérité de désignation (ASP-INV-66).")

    # ---- Ancre : cartes attestées par l'audit ----------------------------
    cartes_audit = dict(AUDIT_CARTE.findall(audit))
    if not cartes_audit:
        return errs + ["ASP-CI-8 : table des cartes introuvable dans l'audit — "
                       "le référentiel technique ne peut pas être attesté."]

    commandables = set()
    for idx, option, statut in cartes:
        if statut == "non commandable":
            if option != CARTE_SANS_SEGMENT:
                errs.append(f"ASP-CI-8 : carte `{option}` déclarée non "
                            f"commandable — seule `{CARTE_SANS_SEGMENT}` l'est.")
            elif idx:
                errs.append(f"ASP-CI-8 : `{CARTE_SANS_SEGMENT}` porte un index "
                            f"de carte (`{idx}`) — l'audit ne lui en atteste "
                            "aucun, et lui en donner un le rendrait adressable.")
            continue
        if not idx:
            errs.append(f"ASP-CI-8 : carte commandable `{option}` sans index.")
            continue
        commandables.add(idx)
        if idx not in cartes_audit:
            errs.append(f"ASP-CI-8 : carte `{idx}` ABSENTE de l'audit — le "
                        "référentiel technique invente une carte.")
        elif cartes_audit[idx] != option:
            errs.append(f"ASP-CI-8 : carte `{idx}` — option du sélecteur "
                        f"`{option}` alors que l'audit atteste "
                        f"`{cartes_audit[idx]}`. La comparaison est LITTÉRALE : "
                        "une espace finale attestée fait partie de la valeur "
                        "(ASP-INV-67).")
    if commandables != CARTES_COMMANDABLES:
        errs.append("ASP-CI-8 : cartes commandables "
                    f"{sorted(commandables) or 'aucune'} ; attendu "
                    f"{sorted(CARTES_COMMANDABLES)}.")
    if not any(o == CARTE_SANS_SEGMENT and s == "non commandable"
               for _, o, s in cartes):
        errs.append(f"ASP-CI-8 : `{CARTE_SANS_SEGMENT}` n'est pas déclaré non "
                    "commandable — son statut doit rester explicite.")

    # ---- Ancre : segments attestés par l'audit ---------------------------
    atteste = parse_audit_segments(audit)
    if not atteste:
        return errs + ["ASP-CI-8 : table des segments introuvable dans l'audit."]

    vus = set()
    for seg, index_natif, nom, statut in segments:
        vus.add(seg)
        carte, _, suffixe = seg.partition("_")
        if index_natif != suffixe:
            errs.append(f"ASP-CI-8 : segment `{seg}` — index natif "
                        f"`{index_natif}` incohérent avec la paire (`{suffixe}` "
                        "attendu). C'est cet index qui entre dans la charge "
                        "utile : une dérive y nettoie une autre pièce.")
        if seg not in atteste:
            errs.append(f"ASP-CI-8 : segment `{seg}` ABSENT de l'audit — le "
                        "référentiel technique invente un segment.")
            continue
        nom_atteste, carte_attestee = atteste[seg]
        if nom != nom_atteste:
            errs.append(f"ASP-CI-8 : segment `{seg}` — nom Roborock `{nom}` "
                        f"alors que l'audit atteste `{nom_atteste}`.")
        if carte in cartes_audit and \
                cartes_audit[carte].strip() != carte_attestee.strip():
            errs.append(f"ASP-CI-8 : segment `{seg}` — l'audit le rattache à la "
                        f"carte `{carte_attestee}`, incompatible avec l'index "
                        f"de carte `{carte}` (`{cartes_audit[carte].strip()}`).")
        attendu = "non commandable" if seg in SEGMENTS_NON_COMMANDABLES \
            else "commandable"
        if statut != attendu:
            errs.append(f"ASP-CI-8 : segment `{seg}` déclaré `{statut}` — "
                        f"attendu `{attendu}`. Les segments observés hors "
                        "référentiel V1 confirment la carte, ils ne deviennent "
                        "jamais désignables (QO-1).")
    manquants = sorted(set(atteste) - vus)
    if manquants:
        errs.append("ASP-CI-8 : segment(s) attesté(s) par l'audit et absent(s) "
                    f"du référentiel technique : {', '.join(manquants)} — la "
                    "vue de l'appareil doit y être exhaustive, statut compris.")

    # ---- Correspondance complète métier ↔ technique ----------------------
    canon = parse_segments(t02)
    tech_commandables = {s for s, _, _, st in segments if st == "commandable"}
    if tech_commandables != set(canon):
        errs.append("ASP-CI-8 : les deux référentiels divergent — commandables "
                    f"techniques {sorted(tech_commandables)} contre métier "
                    f"{sorted(canon)}.")
    noms_tech = {s: n for s, _, n, _ in segments}
    for seg in sorted(set(canon) & set(noms_tech)):
        libelle, divergent = canon[seg]
        if (divergent or libelle) != noms_tech[seg]:
            errs.append(f"ASP-CI-8 : segment `{seg}` — le référentiel métier "
                        f"annonce le nom Roborock `{divergent or libelle}`, le "
                        f"référentiel technique `{noms_tech[seg]}`.")
    promus = sorted(SEGMENTS_NON_COMMANDABLES & set(canon))
    if promus:
        errs.append(f"ASP-CI-8 : segment(s) non commandable(s) promu(s) au "
                    f"référentiel métier : {', '.join(promus)}.")

    # ---- M-2 : l'exception cartographique reste close --------------------
    errs.extend(check_bornage_exception(t02, t06))
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-9 — modèle canonique d'états (08 §1), total sur la partition
# ─────────────────────────────────────────────────────────────

ETAT_CANON = re.compile(r'^\| \*\*([^*|\n]+)\*\* \| `([a-z_]+)` \|', re.M)
IMAGE_CANON = re.compile(
    r'^> \| \*\*([RAEN])\*\* \| ([^|\n]+) \| `([a-z_]+)` \|', re.M)


def coherence_ancres(partition: dict | None = None,
                     image: dict | None = None,
                     codes_par_classe: dict | None = None) -> list[str]:
    """i-2 — PARTITION_ATTENDUE et IMAGE_ATTENDUE décrivent le MÊME monde.

    Deux ancres de module qui divergeraient laisseraient passer un contrat
    faux : un état ajouté à la partition sans image canonique, ou une image
    portant un état que la partition ne classe pas. La classe N est traitée à
    part — elle n'énumère rien, sa règle est un défaut.
    """
    partition = PARTITION_ATTENDUE if partition is None else partition
    image = IMAGE_ATTENDUE if image is None else image
    codes_par_classe = (CODES_PAR_CLASSE if codes_par_classe is None
                        else codes_par_classe)
    errs: list[str] = []
    explicites = {v for etats in partition.values() for v in etats}
    for etat in sorted(explicites - set(image)):
        errs.append(f"ASP-CI-9 : ancre incohérente — l'état `{etat}` est classé "
                    "par la partition mais n'a AUCUNE image canonique.")
    for etat in sorted(set(image) - explicites):
        errs.append(f"ASP-CI-9 : ancre incohérente — l'état `{etat}` reçoit une "
                    "image canonique mais n'appartient à AUCUNE classe "
                    "explicite de la partition.")
    for cls, etats in sorted(partition.items()):
        admis = codes_par_classe.get(cls, set())
        for etat in sorted(etats):
            code = image.get(etat)
            if code is not None and code not in admis:
                errs.append(f"ASP-CI-9 : ancre incohérente — `{etat}` est en "
                            f"classe {cls} mais porte l'image `{code}`, qui "
                            f"n'appartient pas aux codes de cette classe "
                            f"({sorted(admis)}). Un DÉPLACEMENT d'état à image "
                            "inchangée est ainsi rendu détectable.")
    return errs


def bloc_etats(t08: str) -> str:
    try:
        return t08.split("## 1. États canoniques", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        return ""


# M-1 — chaque compteur est ancré sur SA clause normative, jamais sur une
# recherche globale de « dix » : une occurrence leurre ailleurs dans le même
# chapitre ne doit satisfaire aucune de ces gardes.
COMPTEURS_ANCRES = (
    ("08", "08 §1, phrase d'ouverture",
     re.compile(r'^Le domaine distingue \*\*dix\*\* situations', re.M)),
    ("08", "08, déclaration `ASP-INV-44`",
     re.compile(r'\*\*`ASP-INV-44`\*\* — Ces dix états sont')),
    ("11", "11 §3, point 3",
     re.compile(r'Restituer les états canoniques distinctement\*\* — les '
                r'\*\*dix\*\* du')),
    ("12", "12 §2.3, rôle `‹etat_canonique›`",
     re.compile(r"^\| `‹etat_canonique›` \|[^\n]*parmi les \*\*dix\*\*", re.M)),
)
# Admissibilité de `repos_hors_base` : la clause vit DANS sa ligne de tableau.
LIGNE_REPOS = re.compile(
    r'^\| \*\*[^*|\n]+\*\* \| `repos_hors_base` \|([^\n]*)$', re.M)
MOTIF_ADMISSIBLE = "**repos admissible au lancement**"


def check_etats_canoniques(t08: str, t11: str, t12: str) -> list[str]:
    errs: list[str] = coherence_ancres()
    bloc = bloc_etats(t08)
    if not bloc:
        return errs + ["ASP-CI-9 : modèle d'états canoniques introuvable "
                       "(08 §1)."]

    codes = [c for _, c in ETAT_CANON.findall(bloc)]
    if len(codes) != len(set(codes)):
        doublons = sorted({c for c in codes if codes.count(c) > 1})
        errs.append(f"ASP-CI-9 : code(s) canonique(s) en doublon : "
                    f"{', '.join(doublons)} — aucun synonyme n'est admis.")
    attendus, reels = set(ETATS_CANONIQUES), set(codes)
    for c in sorted(attendus - reels):
        errs.append(f"ASP-CI-9 : état canonique `{c}` ABSENT du chapitre 08 §1.")
    for c in sorted(reels - attendus):
        errs.append(f"ASP-CI-9 : état canonique `{c}` AJOUTÉ — le vocabulaire "
                    f"est clos à {len(ETATS_CANONIQUES)} codes (ASP-INV-44).")
    if errs:
        return errs

    # ---- Image partition -> code canonique -------------------------------
    image: dict[str, str] = {}
    for _, valeurs, code in IMAGE_CANON.findall(bloc):
        for etat in ETAT.findall(valeurs):
            image[etat] = code
    for etat, attendu in sorted(IMAGE_ATTENDUE.items()):
        if etat not in image:
            errs.append(f"ASP-CI-9 : l'état machine `{etat}` n'a AUCUNE image "
                        "canonique — le modèle n'est plus total (ASP-INV-68).")
        elif image[etat] != attendu:
            errs.append(f"ASP-CI-9 : `{etat}` projeté sur `{image[etat]}` ; "
                        f"attendu `{attendu}`.")
    for etat in sorted(set(image) - set(IMAGE_ATTENDUE)):
        errs.append(f"ASP-CI-9 : l'état machine `{etat}` est projeté alors "
                    "qu'il n'appartient pas à la partition attestée.")
    if ETAT_ORTHOGONAL in image.values():
        errs.append(f"ASP-CI-9 : `{ETAT_ORTHOGONAL}` reçoit une image depuis "
                    "l'état machine — il dérive du TÉMOIN DE SESSION et se "
                    "superpose aux autres, il ne les exclut pas (08 §3).")

    # ---- Classe N -> etat_non_qualifie -> refus ETAT_NON_QUALIFIE --------
    ligne_n = [c for cls, _, c in IMAGE_CANON.findall(bloc) if cls == "N"]
    if not ligne_n:
        errs.append("ASP-CI-9 : la classe N n'a aucune image canonique.")
    elif ligne_n[0] != CODE_CANONIQUE_CLASSE_N:
        errs.append(f"ASP-CI-9 : la classe N est projetée sur `{ligne_n[0]}` ; "
                    f"attendu `{CODE_CANONIQUE_CLASSE_N}`.")
    if CODE_ETAT_NON_QUALIFIE not in bloc:
        errs.append(f"ASP-CI-9 : le chapitre 08 §1 ne relie pas "
                    f"`{CODE_CANONIQUE_CLASSE_N}` au refus "
                    f"`{CODE_ETAT_NON_QUALIFIE}` — l'état est nommé sans être "
                    "opposable au lancement.")
    for confusion in ("ROBOT_INDISPONIBLE", "ERREUR_EQUIPEMENT"):
        if confusion not in bloc:
            errs.append(f"ASP-CI-9 : le chapitre 08 §1 ne distingue pas "
                        f"`{CODE_CANONIQUE_CLASSE_N}` de `{confusion}` — la "
                        "confusion produirait un diagnostic faux (ASP-INV-60).")
    # ---- M-1 : admissibilité ancrée sur la LIGNE de `repos_hors_base` ----
    lignes_repos = LIGNE_REPOS.findall(bloc)
    if not lignes_repos:
        errs.append("ASP-CI-9 : ligne canonique de `repos_hors_base` "
                    "introuvable (08 §1).")
    elif not any(MOTIF_ADMISSIBLE in l for l in lignes_repos):
        errs.append("ASP-CI-9 : `repos_hors_base` n'est plus déclaré "
                    f"{MOTIF_ADMISSIBLE} DANS SA LIGNE canonique — la classe R "
                    "perd son image, et le lancement après transport n'est plus "
                    "acquis (ARB-1). Une occurrence d'« admissible » ailleurs "
                    "dans le chapitre ne vaut pas cette clause.")

    # ---- M-1 : compteurs ancrés sur leur clause normative ----------------
    sources = {"08": t08, "11": t11, "12": t12}
    for nom, ou, motif in COMPTEURS_ANCRES:
        if not motif.search(sources[nom]):
            errs.append(f"ASP-CI-9 : compteur d'états FAUX ou absent — {ou} "
                        "n'annonce plus DIX états canoniques. Une autre "
                        "occurrence de « dix » dans le même chapitre ne "
                        "satisfait pas cette garde.")
    for nom, texte in sources.items():
        if "huit états" in texte or "les huit du" in texte:
            errs.append(f"ASP-CI-9 : le chapitre {nom} compte encore HUIT états "
                        "— renvoi non réaligné.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-10 — fenêtres temporelles contractuelles (07 §3.1)
# ─────────────────────────────────────────────────────────────

FENETRE = re.compile(
    r'^> \| \*\*([^*|\n]+)\*\* \| \*\*(\d+) s\*\* \| ([^|\n]+) \|', re.M)
# R1 — `[^\S\n]` et non `\s` : une classe d'espaces incluant `\n` ferait
# d'un nombre en fin de ligne suivi d'un `s` en tête de la suivante une fausse
# durée, et lierait deux clauses distinctes.
DUREE = re.compile(r'(\d+)[^\S\n]*(?:s\b|secondes?\b)')
# Les numéros d'étape se lisent DANS une mention « étape(s) … », jamais par
# sous-chaîne : `ASP-INV-38` contient un « 8 » qui n'est pas une étape.
ETAPES_CITEES = re.compile(
    r'étapes?[^\S\n]+(\d+(?:(?:,|[^\S\n]+et)[^\S\n]*\d+)*)')


def etapes_citees(cellule: str) -> set[str]:
    return {n for groupe in ETAPES_CITEES.findall(cellule)
            for n in re.findall(r'\d+', groupe)}


# M-3 — SEULE exemption au balayage des durées : l'observation terrain du
# désalignement du témoin de session (08 §3). Ce n'est PAS une allowlist de
# nombres : c'est la clause elle-même, littérale, qui est retirée du balayage.
# Altérée, elle cesse d'être reconnue et ses durées redeviennent concurrentes ;
# supprimée, son absence est signalée.
CLAUSE_TERRAIN_08 = ("témoin **sous-inclusif** (53 s puis 25 s de déplacement "
                     "à `off`, deux fois)")
FICHIER_TERRAIN_08 = "08_etats_et_observation.md"

# Seconde exemption, de même nature : l'OBSERVATION de la durée d'un appel de
# service (07 §3.1). Elle n'est pas une durée du domaine — Arsenal ne la borne
# pas — mais `10,0075 s` se lit « 75 s » au balayage. Comme la première, c'est
# la CLAUSE LITTÉRALE qui est retirée, jamais un nombre : altérée, elle cesse
# d'être reconnue et sa durée redevient concurrente ; supprimée, son absence
# est signalée. Toutes deux sont vérifiées présentes EXACTEMENT UNE FOIS.
CLAUSE_APPEL_07 = ("`HomeAssistantError` après **10,0075 s**. "
                   "C'est une **observation**")
FICHIER_APPEL_07 = "07_moteur_de_mission.md"
EXEMPTIONS_DUREE = ((FICHIER_TERRAIN_08, CLAUSE_TERRAIN_08),
                    (FICHIER_APPEL_07, CLAUSE_APPEL_07))

# m-1 — l'association 60 s ↔ transition ↔ TRANSITION_NON_OBSERVEE est ancrée
# sur la LIGNE du catalogue, pas sur une co-présence de chaînes dans le fichier.
LIGNE_ECHEC = re.compile(r'^\| `([A-Z][A-Z_]{4,})` \|([^\n]*)$', re.M)
NOTE_FENETRE_09 = ("**La fenêtre d'observation de `TRANSITION_NON_OBSERVEE` "
                   "est de 60 s**")


def bloc_fenetres(t07: str) -> str:
    return section_normative(t07, "### 3.1")


def check_fenetres(textes: dict[str, str]) -> list[str]:
    t07 = textes.get("07_moteur_de_mission.md", "")
    t09 = textes.get("09_refus_et_diagnostics.md", "")
    t12 = textes.get("12_identifiants_a_fournir.md", "")
    t13 = textes.get("13_hors_perimetre_arbitrages_et_questions_ouvertes.md", "")
    errs: list[str] = []
    bloc = bloc_fenetres(t07)
    if not bloc:
        return ["ASP-CI-10 : constantes temporelles introuvables (07 §3.1) — "
                "la séquence n'a plus de borne opposable."]

    lignes = FENETRE.findall(bloc)
    valeurs = [int(v) for _, v, _ in lignes]
    if sorted(valeurs) != sorted((FENETRE_CONFIRMATION_S, FENETRE_TRANSITION_S)):
        return errs + [f"ASP-CI-10 : fenêtres déclarées {sorted(valeurs)} s ; "
                       f"attendu exactement "
                       f"[{FENETRE_CONFIRMATION_S}, {FENETRE_TRANSITION_S}] s."]

    portees = {int(v): portee for _, v, portee in lignes}
    conf = etapes_citees(portees[FENETRE_CONFIRMATION_S])
    for etape in ETAPES_CONFIRMATION:
        if etape not in conf:
            errs.append(f"ASP-CI-10 : la fenêtre de {FENETRE_CONFIRMATION_S} s "
                        f"ne couvre pas l'étape {etape} — une confirmation "
                        "resterait non bornée.")
    trans_cellule = portees[FENETRE_TRANSITION_S]
    if "transition" not in trans_cellule.lower():
        errs.append(f"ASP-CI-10 : la fenêtre de {FENETRE_TRANSITION_S} s n'est "
                    "pas affectée à la transition de démarrage.")
    empietement = sorted(etapes_citees(trans_cellule) & set(ETAPES_CONFIRMATION))
    if empietement:
        errs.append(f"ASP-CI-10 : la fenêtre de {FENETRE_TRANSITION_S} s couvre "
                    f"l'étape {', '.join(empietement)} — les deux portées sont "
                    "INVERSÉES ou confondues.")
    if conf & etapes_citees(trans_cellule):
        errs.append("ASP-CI-10 : une même étape relève des deux fenêtres.")

    # ---- Affectation dans la séquence -----------------------------------
    lignes_seq = {e: [l for l in t07.splitlines()
                      if l.startswith(f"| **{e}** |")]
                  for e in ETAPES_CONFIRMATION}
    for etape, trouvees in lignes_seq.items():
        if not trouvees:
            errs.append(f"ASP-CI-10 : l'étape {etape} est ABSENTE de la "
                        "séquence de lancement — une confirmation supprimée "
                        "n'est pas une confirmation bornée.")
        elif not any(f"{FENETRE_CONFIRMATION_S} s" in l for l in trouvees):
            errs.append(f"ASP-CI-10 : l'étape {etape} de la séquence ne "
                        f"porte pas la fenêtre de "
                        f"{FENETRE_CONFIRMATION_S} s.")

    # ---- M-3 : aucune durée concurrente, sur les 14 chapitres ------------
    autorisees = {FENETRE_CONFIRMATION_S, FENETRE_TRANSITION_S}
    for fichier, clause in EXEMPTIONS_DUREE:
        source = textes.get(fichier, "")
        if not source:
            continue
        vues = source.count(clause)
        if vues != 1:
            errs.append(f"ASP-CI-10 : la clause d'observation de "
                        f"{fichier} est {'absente' if not vues else 'dupliquée'} "
                        "— l'exemption au balayage des durées n'est plus ancrée "
                        "sur un texte connu, et ses durées ne peuvent plus être "
                        "distinguées d'une durée normative.")
    for nom in sorted(textes):
        corps = textes[nom]
        for fichier, clause in EXEMPTIONS_DUREE:
            if nom == fichier:
                corps = corps.replace(clause, "")
        concurrentes = sorted({int(v) for v in DUREE.findall(corps)} - autorisees)
        if concurrentes:
            errs.append(f"ASP-CI-10 : durée(s) concurrente(s) dans {nom} : "
                        f"{concurrentes} s — le domaine n'admet que "
                        f"{sorted(autorisees)} s.")

    # ---- Ni helper temporel, ni fallback, révision conjointe -------------
    minuscule = bloc.lower()
    if "ni helper" not in minuscule:
        errs.append("ASP-CI-10 : 07 §3.1 n'exclut pas explicitement un helper "
                    "temporel — une durée réglable à chaud serait un second "
                    "arbitre de la sûreté.")
    if "aucun fallback" not in minuscule:
        errs.append("ASP-CI-10 : 07 §3.1 n'exclut pas le fallback — une "
                    "échéance atteinte doit refuser ou qualifier un échec.")
    if "Helper temporel" not in t12 or "Aucun" not in t12:
        errs.append("ASP-CI-10 : le chapitre 12 n'acte pas l'absence de helper "
                    "temporel à fournir (ASP-INV-69).")
    try:
        arb3 = t13.split("### `ARB-3`", 1)[1].split("\n### ", 1)[0].lower()
    except IndexError:
        arb3 = ""
    if not arb3:
        errs.append("ASP-CI-10 : arbitrage ARB-3 introuvable (13).")
    elif not all(m in arb3 for m in ("contrat", "checker", "runtime")):
        errs.append("ASP-CI-10 : ARB-3 ne conserve pas la révision CONJOINTE "
                    "contrat + checker + runtime.")
    # ---- m-1 : 60 s ↔ transition ↔ TRANSITION_NON_OBSERVEE ---------------
    catalogue = section_normative(t09, "## 3. Catalogue des échecs")
    if not catalogue:
        errs.append("ASP-CI-10 : catalogue des échecs introuvable (09 §3).")
    else:
        fenetre = f"{FENETRE_TRANSITION_S} s"
        lignes = dict(LIGNE_ECHEC.findall(catalogue))
        if CODE_TRANSITION not in lignes:
            errs.append(f"ASP-CI-10 : `{CODE_TRANSITION}` absent du catalogue "
                        "des échecs (09 §3).")
        else:
            ligne = lignes[CODE_TRANSITION]
            if fenetre not in ligne:
                errs.append(f"ASP-CI-10 : la LIGNE de `{CODE_TRANSITION}` ne "
                            f"porte pas la fenêtre de {fenetre} — la seule "
                            "co-présence des deux chaînes dans le chapitre ne "
                            "vaut pas association.")
            if "transition" not in ligne.lower():
                errs.append(f"ASP-CI-10 : la LIGNE de `{CODE_TRANSITION}` ne "
                            "nomme pas la transition de démarrage.")
        egarees = sorted(code for code, ligne in lignes.items()
                         if code != CODE_TRANSITION and fenetre in ligne)
        if egarees:
            errs.append(f"ASP-CI-10 : la fenêtre de {fenetre} est affectée à "
                        f"{', '.join('`' + c + '`' for c in egarees)} — elle ne "
                        f"qualifie QUE `{CODE_TRANSITION}`.")
        if NOTE_FENETRE_09 not in catalogue:
            errs.append(f"ASP-CI-10 : 09 §3 ne relie plus explicitement la "
                        f"fenêtre de {fenetre} à `{CODE_TRANSITION}`.")
    return errs


# ─────────────────────────────────────────────────────────────
# RUNTIME L1 — ASP-CI-22 … ASP-CI-25 : contrôles PAR RENDU
#
# Les contrôles 11 à 21 lisent la STRUCTURE des artefacts. Un contre-audit a
# montré que cela ne suffit pas : les deux défauts que ce lot revendique avoir
# évités — la troncature de `Template.async_render` et le retypage de
# `_parse_result` — pouvaient être RÉINTRODUITS sans qu'aucun contrôle ne
# bronche, et le contenu des deux gabarits template pouvait être remplacé par
# n'importe quoi. Les quatre contrôles ci-dessous RENDENT les gabarits, comme
# ASP-CI-12 le fait déjà pour la charge utile, et confrontent le RÉSULTAT.
# ─────────────────────────────────────────────────────────────

# Motif du chemin rapide numérique de `_parse_result`, recopié à l'identique
# depuis helpers/template/__init__.py (2026.8.3). C'est lui qui retype `"0"`
# en entier, et qui a failli rendre `referentiel[carte_cle]` insoluble.
IS_NUMERIC_HA = re.compile(r"^[+-]?(?!0\d)\d*(?:\.\d*)?$")

# Variables du moteur dont le retypage numérique est VOULU et sans danger.
# Toute autre variable retypée est une régression.
#
# Les trois instants de référence en font partie DÉLIBÉRÉMENT : c'est leur
# retypage en `float` par `_parse_result` qui rend la comparaison de fraîcheur
# NUMÉRIQUE, donc exempte de toute conversion textuelle. Rendu sous forme de
# datetime, `now()` serait ramené à une chaîne et la comparaison lèverait.
# Littéraux : les constantes runtime sont déclarées plus bas dans ce module.
# Leur concordance avec INSTANTS_PREPARATOIRES est confrontée par le selftest,
# et non supposée.
VARIABLES_NUMERIQUES_ADMISES = frozenset(
    {"passages_int", "t_carte", "t_eau", "t_aspiration"})

# Énumération NATIVE de `sensor.roborock_q7_max_etat`, relevée en lecture seule
# le 2026-08-27 (attribut `options`). Ancre extérieure au contrat : c'est elle
# qui rend testable la TOTALITÉ de l'image canonique, classe N comprise.
ETATS_NATIFS_RELEVES = (
    "unknown", "starting", "charger_disconnected", "idle",
    "remote_control_active", "cleaning", "returning_home", "manual_mode",
    "charging", "charging_problem", "paused", "spot_cleaning", "error",
    "shutting_down", "updating", "docking", "going_to_target",
    "zoned_cleaning", "segment_cleaning", "emptying_the_bin",
    "washing_the_mop", "washing_the_mop_2", "going_to_wash_the_mop", "in_call",
    "mapping", "egg_attack", "patrol", "attaching_the_mop",
    "detaching_the_mop", "charging_complete", "device_offline", "locked",
    "air_drying_stopping", "robot_status_mopping", "clean_mop_cleaning",
    "clean_mop_mopping", "segment_mopping", "segment_clean_mop_cleaning",
    "segment_clean_mop_mopping", "zoned_mopping", "zoned_clean_mop_cleaning",
    "zoned_clean_mop_mopping", "back_to_dock_washing_duster")


def _env_jinja(etats: dict[str, object] | None = None, horloge: float = 0.0):
    """Bac à sable Jinja muni des primitives Home Assistant, sur un état simulé.

    `states` y est, comme dans Home Assistant, UN SEUL objet à la fois
    APPELABLE — `states('x.y')` — et NAVIGABLE — `states.x.y.last_reported`.
    Sans cette seconde forme, `now()` et `as_timestamp(...)` levaient dans le
    bac à sable et l'exception était avalée par l'appelant : les gabarits de
    fraîcheur passaient sans être rendus. Un contrôle qui ne rend rien ne
    prouve rien.

    `lr` porte le `last_reported` simulé. Il est DISTINCT de l'état : c'est
    tout l'objet du contrôle, une republication identique ne mutant que lui.
    """
    from jinja2.sandbox import ImmutableSandboxedEnvironment

    etats = etats or {}
    _opaques = ("unsafe_callable", "alters_data")

    def _brut(eid):
        return etats.get(eid)

    def _st(eid=None):
        v = etats.get(eid, "unknown") if eid is not None else None
        return v["state"] if isinstance(v, dict) else v

    def _attr(eid, cle):
        v = etats.get(eid)
        return v.get("attrs", {}).get(cle) if isinstance(v, dict) else None

    class _Etat:
        def __init__(self, eid):
            self._eid = eid

        def __getattr__(self, nom):
            if nom.startswith("_") or nom in _opaques:
                raise AttributeError(nom)
            v = _brut(self._eid)
            if nom == "state":
                return _st(self._eid)
            if nom in ("last_reported", "last_updated", "last_changed"):
                # Entité absente : aucune date. `as_timestamp(..., 0)` rendra
                # 0, donc `0 > t` est faux — refus fermé, jamais un repli.
                if not isinstance(v, dict):
                    return None
                return v.get(nom, v.get("lr") if nom == "last_reported" else None)
            raise AttributeError(nom)

    class _Dom:
        def __init__(self, domaine):
            self._domaine = domaine

        def __getattr__(self, objet):
            if objet.startswith("_") or objet in _opaques:
                raise AttributeError(objet)
            return _Etat(f"{self._domaine}.{objet}")

    class _AllStates:
        def __call__(self, eid=None):
            return _st(eid)

        def __getattr__(self, domaine):
            if domaine.startswith("_") or domaine in _opaques:
                raise AttributeError(domaine)
            return _Dom(domaine)

    def _as_timestamp(valeur, defaut=None):
        if isinstance(valeur, (int, float)):
            return float(valeur)
        return defaut

    class _Now:
        """`now()` ne rend pas un datetime ici : seul `.timestamp()` est lu."""

        def timestamp(self):
            return horloge

    env = ImmutableSandboxedEnvironment()
    env.globals["states"] = _AllStates()
    env.globals["state_attr"] = _attr
    env.globals["is_state"] = lambda eid, val: _st(eid) == val
    env.globals["as_timestamp"] = _as_timestamp
    env.globals["now"] = lambda: _Now()
    return env


def rendu_ha(gabarit: str, etats=None, horloge: float = 0.0, **variables):
    """Reproduit `Template.async_render(parse_result=True)` : rendu, PUIS
    `.strip()`, PUIS `_parse_result`. Les trois étapes, dans cet ordre — c'est
    la deuxième qui mange l'espace finale de `Étage `, et la troisième qui
    retype `"0"`."""
    import ast

    brut = _env_jinja(etats, horloge).from_string(gabarit).render(**variables)
    rendu = brut.strip()
    if IS_NUMERIC_HA.match(rendu):
        try:
            return float(rendu) if "." in rendu else int(rendu)
        except ValueError:
            pass
    try:
        valeur = ast.literal_eval(rendu)
    except (ValueError, TypeError, SyntaxError, MemoryError):
        return rendu
    return rendu if isinstance(valeur, (str, complex)) else valeur


def _bloc_variables(corps):
    """Toutes les étapes `variables:` du moteur, dans l'ordre."""
    return [s["variables"] for s in _aplatir(corps.get("sequence"))
            if isinstance(s, dict) and "variables" in s]


def check_rendus_moteur(corps, etapes, t02) -> list[str]:
    """ASP-CI-22 — troncature, retypage et garde de type, prouvés par RENDU."""
    errs = []
    tech = bloc_technique(t02)
    cartes = {idx: opt for idx, opt, statut in TECH_CARTE.findall(tech)
              if idx and statut == "commandable"}
    ref = next((v["referentiel"] for v in _bloc_variables(corps)
                if "referentiel" in v), None)
    if ref is None:
        errs.append("ASP-CI-22 : référentiel embarqué introuvable.")
        return errs

    # (a) l'écriture de carte doit être rendue EN BLOC.
    ecritures = [s for s in etapes
                 if _service(s) == SVC_EAU and NATIF_CARTE in _cibles(s)]
    if len(ecritures) != 1:
        errs.append(f"ASP-CI-22 : une seule écriture du sélecteur de carte est "
                    f"attendue — trouvé {len(ecritures)}.")
        return errs
    data = ecritures[0].get("data")
    if not isinstance(data, str):
        errs.append(
            "ASP-CI-22 : le `data:` de la sélection de carte doit être UN "
            "GABARIT rendu en bloc, pas un mapping de scalaires. "
            "`Template.async_render` tronque chaque rendu : sous la forme "
            "`option: \"{{ ctx_carte.option }}\"`, l'espace finale de "
            "l'option `Étage ` disparaît et la carte devient inlançable.")
        return errs

    # (a2) rendu réel, carte par carte, espace finale comprise.
    for idx, opt in sorted(cartes.items()):
        if idx not in ref:
            continue
        obtenu = rendu_ha(data, ctx_carte=ref[idx])
        if not isinstance(obtenu, dict):
            errs.append(f"ASP-CI-22 : carte `{idx}` — le `data:` doit se rendre "
                        f"en dictionnaire ; obtenu {obtenu!r}.")
        elif obtenu.get("option") != opt:
            errs.append(
                f"ASP-CI-22 : carte `{idx}` — l'option transmise au sélecteur "
                f"vaut {obtenu.get('option')!r}, le contrat exige {opt!r}. "
                f"La comparaison porte sur la valeur EXACTE, espace finale "
                f"comprise (ASP-INV-66, ASP-INV-67).")

    # (b) aucune variable retypée par le chemin rapide numérique.
    stub = {"carte": "0", "passages": "1", "profil": "aspiration_normale",
            "segments": ["0_18"], "segments_demandes": ["0_18"]}
    # Le contexte CUMULE les blocs `variables` successifs, comme le fait Home
    # Assistant : `ctx_carte` s'appuie sur `referentiel`, `indices` sur
    # `ctx_carte`. Le réinitialiser à chaque bloc faisait LEVER tous les
    # gabarits dépendants — silencieusement, tant que l'exception était avalée.
    contexte = dict(stub)
    for bloc in _bloc_variables(corps):
        for cle, val in bloc.items():
            if not isinstance(val, str) or "{" not in val:
                contexte[cle] = val
                continue
            try:
                brut = _env_jinja(horloge=T0_SIM).from_string(val).render(
                    **contexte).strip()
            except Exception as exc:               # noqa: BLE001
                # Une exception de rendu est un ÉCART, jamais un cas ignoré.
                # L'avaler était un FAUX VERT : les gabarits qui levaient
                # n'étaient tout simplement pas contrôlés.
                errs.append(
                    f"ASP-CI-22 : la variable `{cle}` LÈVE au rendu "
                    f"({type(exc).__name__}: {exc}). Un gabarit qui lève "
                    f"arrête la séquence sans verdict — et un contrôle qui "
                    f"l'ignore ne prouve rien.")
                contexte[cle] = ""
                continue
            contexte[cle] = rendu_ha(val, horloge=T0_SIM, **contexte)
            if IS_NUMERIC_HA.match(brut) and cle not in VARIABLES_NUMERIQUES_ADMISES:
                errs.append(
                    f"ASP-CI-22 : la variable `{cle}` se rend en {brut!r}, que "
                    f"`_parse_result` retype en "
                    f"{type(rendu_ha(val, horloge=T0_SIM, **contexte)).__name__}. "
                    f"Une clé de carte retypée rend `referentiel[…]` insoluble. "
                    f"Porter le contexte EN BLOC, ou déclarer la variable dans "
                    f"VARIABLES_NUMERIQUES_ADMISES.")

    # (c) la garde de type de `segments` doit refuser un mapping.
    #     `choose` est normalisé : il accepte un choix unique en MAPPING NU,
    #     et l'itérer directement parcourrait alors ses CLÉS.
    _formes: list[str] = []
    gardes = []
    for i_s, s in enumerate(etapes):
        if not (isinstance(s, dict) and "choose" in s):
            continue
        for o in _ensure_list(s["choose"], f"etape[{i_s}]/choose", _formes):
            if not isinstance(o, dict):
                continue
            for c in _ensure_list(o.get("conditions"),
                                  f"etape[{i_s}]/choose/conditions", _formes):
                if isinstance(c, dict) and "segments is" in str(
                        c.get("value_template")):
                    gardes.append(c["value_template"])
    errs += [f"ASP-CI-22 : {a}" for a in _formes]
    if not gardes:
        errs.append("ASP-CI-22 : aucune garde de type sur `segments`.")
    else:
        for forme, description in (
                ({"0_18": 1, "0_21": 2}, "un mapping"),
                ("0_18", "une chaîne"),
                ([], "une liste vide")):
            if not any(rendu_ha(g, carte="0", segments=forme,
                                profil="aspiration_normale", passages="1")
                       is True for g in gardes):
                errs.append(
                    f"ASP-CI-22 : {description} passée en `segments` n'est pas "
                    f"refusée. En Jinja un dictionnaire satisfait `is sequence` "
                    f"et `map('string')` en itérerait les CLÉS : la demande "
                    f"serait comprise pour une autre (ASP-INV-23).")
    return errs


def check_etat_canonique_rendu(texte_etat) -> list[str]:
    """ASP-CI-23 — image TOTALE, prouvée en rendant le gabarit sur les 44
    valeurs réellement exposées par l'appareil."""
    errs = []
    try:
        bloc = yaml.safe_load(texte_etat)[0]["sensor"][0]
    except (TypeError, KeyError, IndexError, yaml.YAMLError) as exc:
        return [f"ASP-CI-23 : `{ID_ETAT_CANON}` illisible : {exc}"]
    attrs = bloc.get("attributes") or {}
    for cle in ("state",):
        if cle not in bloc:
            return [f"ASP-CI-23 : `{ID_ETAT_CANON}` sans clé `{cle}`."]

    for etat in ETATS_NATIFS_RELEVES + ("unavailable",):
        ctx = {NATIF_ETAT: etat, NATIF_SESSION: "off"}
        attendu = IMAGE_ATTENDUE.get(etat, CODE_CANONIQUE_CLASSE_N)
        obtenu = rendu_ha(bloc["state"], etats=ctx)
        if obtenu != attendu:
            errs.append(f"ASP-CI-23 : état natif `{etat}` — image obtenue "
                        f"{obtenu!r}, image contractuelle {attendu!r} "
                        f"(08 §1, ASP-INV-68).")
        if "classe_partition" in attrs:
            classe = next((c for c, v in PARTITION_ATTENDUE.items()
                           if etat in v), CLASSE_NON_QUALIFIEE)
            vue = rendu_ha(attrs["classe_partition"], etats=ctx)
            if str(vue) != classe:
                errs.append(f"ASP-CI-23 : état natif `{etat}` — classe obtenue "
                            f"{vue!r}, partition contractuelle {classe!r} "
                            f"(07 §5.0).")
    # l'état orthogonal reste orthogonal, et l'indisponibilité n'est pas `non`
    if ETAT_ORTHOGONAL not in "".join(str(v) for v in attrs.values()) \
            and ETAT_ORTHOGONAL not in attrs:
        errs.append(f"ASP-CI-23 : `{ETAT_ORTHOGONAL}` doit être exposé "
                    f"SÉPARÉMENT, jamais fondu dans la valeur d'état "
                    f"(ASP-INV-68).")
    if ETAT_ORTHOGONAL in attrs:
        rendus = {s: rendu_ha(attrs[ETAT_ORTHOGONAL],
                              etats={NATIF_SESSION: s, NATIF_ETAT: "charging"})
                  for s in ("on", "off", "unknown", "unavailable")}
        if rendus["on"] == rendus["off"]:
            errs.append("ASP-CI-23 : `mission_ouverte` ne distingue pas une "
                        "session ouverte d'une session close.")
        for indispo in ("unknown", "unavailable"):
            if rendus[indispo] in (rendus["off"], rendus["on"]):
                errs.append(f"ASP-CI-23 : `mission_ouverte` rend "
                            f"{rendus[indispo]!r} sur `{indispo}` — une "
                            f"indisponibilité ne vaut ni `oui` ni `non` "
                            f"(ASP-INV-45).")
    for etat in ETATS_NATIFS_RELEVES:
        if rendu_ha(bloc["state"], etats={NATIF_ETAT: etat,
                                          NATIF_SESSION: "off"}) \
                not in ETATS_CANONIQUES:
            errs.append(f"ASP-CI-23 : état natif `{etat}` produit un code hors "
                        f"du vocabulaire canonique (ASP-INV-44).")
    return errs


def check_garde_rendue(texte_garde) -> list[str]:
    """ASP-CI-24 — la garde template applique la MÊME règle que le moteur,
    prouvé sur le produit cartésien des témoins."""
    errs = []
    try:
        bloc = yaml.safe_load(texte_garde)[0]["binary_sensor"][0]
    except (TypeError, KeyError, IndexError, yaml.YAMLError) as exc:
        return [f"ASP-CI-24 : `{ID_GARDE}` illisible : {exc}"]
    if "state" not in bloc:
        return [f"ASP-CI-24 : `{ID_GARDE}` sans clé `state`."]

    etats = ("charging", "charger_disconnected", "idle", "cleaning", "paused",
             "error", "device_offline", "unknown", "charging_complete")
    err_vac = (NOMINAL_ERR_VAC, "wheels_suspended", "unknown", "unavailable")
    err_dock = (NOMINAL_ERR_DOCK, "dust_full", "unknown", "unavailable")
    sessions = ("off", "on", "unknown", "unavailable")
    joues = 0
    for e in etats:
        for ev in err_vac:
            for ed in err_dock:
                for se in sessions:
                    joues += 1
                    ctx = {NATIF_ETAT: e, NATIF_ERR_VAC: ev,
                           NATIF_ERR_DOCK: ed, NATIF_SESSION: se}
                    attendu = ("on" if (e in PARTITION_ATTENDUE["R"]
                                        and ev == NOMINAL_ERR_VAC
                                        and ed == NOMINAL_ERR_DOCK
                                        and se == "off") else "off")
                    obtenu = rendu_ha(bloc["state"], etats=ctx)
                    if str(obtenu) != attendu:
                        errs.append(
                            f"ASP-CI-24 : garde divergente — état `{e}`, "
                            f"erreur robot `{ev}`, erreur dock `{ed}`, session "
                            f"`{se}` : garde `{obtenu}`, règle du moteur "
                            f"`{attendu}` (07 §5.1).")
                        if len(errs) > 6:
                            errs.append("ASP-CI-24 : … divergences suivantes "
                                        "tronquées.")
                            return errs
    if joues < 100:
        errs.append(f"ASP-CI-24 : seulement {joues} combinaisons jouées.")
    return errs


def check_branches_tardives(etapes) -> list[str]:
    """ASP-CI-25 — chaque témoin relu tardivement PRODUIT son refus, par la
    COMPARAISON EXACTE qui le motive.

    La version précédente se contentait de voir le NOM du témoin quelque part
    dans les conditions. C'était insuffisant, et un contre-audit l'a montré :
    retirer `g2_err_dock != 'ok'` de la condition d'erreur, en laissant
    `g2_err_dock` dans la branche d'indisponibilité, passait au vert — alors
    qu'un dock en erreur ne refusait plus rien. Le contrôle exige désormais,
    pour chaque couple (témoin, comparaison), une branche qui porte CETTE
    comparaison, écrit CE code de refus, et s'arrête.
    """
    errs = []
    i_var = [i for i, s in enumerate(etapes)
             if isinstance(s, dict) and "variables" in s
             and any(k.startswith("g2_") for k in s["variables"])]
    if not i_var:
        errs.append("ASP-CI-25 : aucune relecture tardive des gardes "
                    "(ASP-INV-36).")
        return errs
    suite = [s for s in etapes[i_var[0] + 1:]
             if isinstance(s, dict) and "choose" in s]
    if not suite:
        errs.append("ASP-CI-25 : la relecture tardive n'est suivie d'aucun "
                    "arbitrage — relire sans refuser ne garde rien.")
        return errs
    # `choose` normalisé AVANT toute indexation ou itération : un mapping nu
    # est une forme valide, une liste vide ne doit pas lever `IndexError`, et
    # un type invalide doit produire un diagnostic, pas un traceback.
    _formes: list[str] = []
    bloc = _ensure_list(suite[0]["choose"], "arbitrage tardif/choose", _formes)
    errs += [f"ASP-CI-25 : {a}" for a in _formes]
    if not bloc:
        errs.append("ASP-CI-25 : l'arbitrage qui suit la relecture tardive ne "
                    "porte AUCUNE branche — relire sans refuser ne garde rien.")
        return errs

    # Chaque branche : sa condition normalisée, ses verdicts, son `stop:`.
    branches = []
    codes_tardifs = set()
    for opt in bloc:
        if not isinstance(opt, dict):
            errs.append(f"ASP-CI-25 : branche d'arbitrage tardif de type "
                        f"{type(opt).__name__} ({opt!r}) — forme non admise.")
            continue
        conditions = " ".join(
            str(c.get("value_template", "")) if isinstance(c, dict) else str(c)
            for c in _ensure_list(opt.get("conditions"),
                                  "arbitrage tardif/choose/conditions",
                                  _formes)).split()
        conditions = " ".join(conditions)
        sequence = opt.get("sequence") or []
        verdicts = {v for _i, v in _ecritures_verdict(sequence)}
        arrete = any(isinstance(s, dict) and "stop" in s for s in sequence)
        branches.append((conditions, verdicts, arrete))
        if not verdicts:
            errs.append(f"ASP-CI-25 : une branche tardive n'écrit aucun "
                        f"verdict — un refus est un livrable (ASP-INV-50) : "
                        f"{conditions[:70]}")
        if not arrete:
            errs.append(f"ASP-CI-25 : une branche tardive n'arrête pas la "
                        f"séquence (ASP-INV-51) : {conditions[:70]}")
        codes_tardifs |= {v for v in verdicts if v.startswith("REFUS/")}

    # Le coeur du contrôle : la COMPARAISON, pas le nom.
    for temoin, comparaison, code in COMPARAISONS_TARDIVES:
        motif = f"{temoin} {comparaison}"
        portantes = [b for b in branches if motif in b[0]]
        if not portantes:
            errs.append(
                f"ASP-CI-25 : la revérification tardive ne compare jamais "
                f"`{motif}`. Voir le nom `{temoin}` ailleurs ne prouve rien : "
                f"c'est CETTE comparaison qui produit `{code}` (07 §5, "
                f"ASP-INV-36).")
            continue
        if not any(code in b[1] for b in portantes):
            vus = sorted({v for b in portantes for v in b[1]}) or ["aucun"]
            errs.append(
                f"ASP-CI-25 : `{motif}` ne produit pas `{code}` mais {vus} — "
                f"le refus doit nommer le manque réel (ASP-INV-50, "
                f"ASP-INV-60).")
        if not any(b[2] for b in portantes if code in b[1]):
            errs.append(f"ASP-CI-25 : la branche `{motif}` -> `{code}` "
                        f"n'arrête pas la séquence (ASP-INV-51).")

    # Chaque témoin relu doit être effectivement comparé quelque part.
    for temoin in TEMOINS_TARDIFS:
        if not any(temoin in b[0] for b in branches):
            errs.append(f"ASP-CI-25 : témoin relu sans aucune branche de "
                        f"refus : `{temoin}` (ASP-INV-36).")

    # Le jeu de refus tardifs doit égaler celui de la garde initiale.
    i_var_1 = [i for i, s in enumerate(etapes)
               if isinstance(s, dict) and "variables" in s
               and any(k.startswith("g1_") for k in s["variables"])]
    if i_var_1:
        premier = next((s for s in etapes[i_var_1[0] + 1:]
                        if isinstance(s, dict) and "choose" in s), None)
        if premier:
            codes_init = set()
            _formes_init: list[str] = []
            for opt in _ensure_list(premier["choose"],
                                    "garde initiale/choose", _formes_init):
                if not isinstance(opt, dict):
                    continue
                codes_init |= {v for _i, v in _ecritures_verdict(
                    _ensure_list(opt.get("sequence"),
                                 "garde initiale/choose/sequence",
                                 _formes_init))
                    if v.startswith("REFUS/")}
            errs += [f"ASP-CI-25 : {a}" for a in _formes_init]
            if codes_init != codes_tardifs:
                errs.append(
                    f"ASP-CI-25 : la revérification tardive ne produit pas les "
                    f"mêmes refus que la garde initiale — manquants "
                    f"{sorted(codes_init - codes_tardifs)}, en trop "
                    f"{sorted(codes_tardifs - codes_init)} (ASP-INV-36).")
    return errs


def _texte_conditions(step) -> str:
    """Concatène les gabarits de condition d'un `choose`, branches comprises."""
    morceaux = []
    _rebut: list[str] = []
    for opt in _ensure_list(step.get("choose"), "", _rebut):
        if not isinstance(opt, dict):
            continue
        for cond in _ensure_list(opt.get("conditions"), "", _rebut):
            if isinstance(cond, str):
                morceaux.append(cond)
            elif isinstance(cond, dict) and isinstance(cond.get("value_template"), str):
                morceaux.append(cond["value_template"])
    return "\n".join(morceaux)


def _refus_du_choose(step) -> set[str]:
    """Codes de refus posés par un `choose`, et qui portent bien un `stop:`."""
    out = set()
    _rebut: list[str] = []
    for opt in _ensure_list(step.get("choose"), "", _rebut):
        if not isinstance(opt, dict):
            continue
        seq = _ensure_list(opt.get("sequence"), "", _rebut)
        if not any(isinstance(s, dict) and "stop" in s for s in seq):
            continue
        out |= {v for _i, v in _ecritures_verdict(seq)}
    return out


# Jeux d'états joués sur chaque postcondition. Chacun porte son verdict
# attendu : c'est la table qui fait foi, pas le gabarit. Les cas reprennent
# ceux du banc d'essai du patron — valeur juste mais périmée, publication
# fraîche mais valeur fausse, une seule des deux lectures fraîche, entité
# disparue. `lr` est le `last_reported` simulé ; l'instant de référence vaut
# 100,0 dans tous les cas.
T0_SIM = 100.0


def contextes_postcondition(corps):
    """DEUX contextes réellement distincts, dérivés du référentiel EMBARQUÉ.

    Valider les postconditions sur le seul couple `RDC` / `off` / `vacuum`
    laisserait passer une substitution par littéral : un gabarit où
    `ctx_carte.option` serait remplacé par `"RDC"`, ou `eau_cible` par
    `"off"`, rendrait exactement la même chose. En les rendant dans DEUX
    contextes — une carte et un profil différents —, la substitution se
    trahit d'elle-même : elle réussit ici et échoue là.

    Les valeurs ne sont pas recopiées : elles sont LUES dans le référentiel et
    la table de profils du moteur. Un référentiel modifié change donc les
    contextes, et le contrôle suit.
    """
    blocs = _bloc_variables(corps)
    ref = next((v["referentiel"] for v in blocs if "referentiel" in v), None)
    profils = next((v["profils"] for v in blocs if "profils" in v), None)
    if not isinstance(ref, dict) or not isinstance(profils, dict):
        return []
    # Une carte SÈCHE et une carte AVEC EAU, choisies pour différer sur les
    # quatre substituables à la fois : option, noms, eau, mode, aspiration.
    choix = (("0", "aspiration_normale"), ("1", "serpilliere_intensive"))
    out = []
    for carte, profil in choix:
        if carte not in ref or profil not in profils:
            continue
        pr = profils[profil]
        out.append({
            "nom": f"carte {carte} · {profil}",
            "ctx_carte": {"option": ref[carte]["option"],
                          "noms": list(ref[carte]["noms"])},
            "eau_cible": pr["eau"], "mode_attendu": pr["mode"],
            "aspiration_cible": pr["aspiration"],
            "t_carte": T0_SIM, "t_eau": T0_SIM, "t_aspiration": T0_SIM,
        })
    return out


def cas_postcondition(ctx):
    """Les cas de rendu, ENGENDRÉS pour un contexte donné.

    Rien n'y est littéral : l'option de carte, les noms de pièces, l'intensité
    d'eau, le mode dérivé et l'aspiration viennent tous du contexte, donc du
    référentiel du moteur.
    """
    option, noms = ctx["ctx_carte"]["option"], ctx["ctx_carte"]["noms"]
    eau, mode, asp = ctx["eau_cible"], ctx["mode_attendu"], ctx["aspiration_cible"]
    autre_option = option + "-AUTRE"
    autre_eau = "high" if eau != "high" else "off"
    autre_mode = "vac_and_mop" if mode != "vac_and_mop" else "vacuum"
    autre_asp = "turbo" if asp != "turbo" else "max"

    carte_ok = {"state": option, "lr": 120.0}
    piece_ok = {"state": noms[0], "attrs": {"options": list(noms)}, "lr": 120.0}
    eau_ok = {"state": eau, "lr": 120.0}
    mode_ok = {"state": mode, "lr": 120.0}
    vac_ok = {"state": "docked", "lr": 120.0, "attrs": {"fan_speed": asp}}

    return {
        "t_carte": (
            ("valeur juste, les deux lectures fraîches", True,
             {NATIF_CARTE: carte_ok, NATIF_PIECE: piece_ok}),
            ("valeur juste mais carte PÉRIMÉE", False,
             {NATIF_CARTE: dict(carte_ok, lr=80.0), NATIF_PIECE: piece_ok}),
            ("valeur juste mais pièces PÉRIMÉES", False,
             {NATIF_CARTE: carte_ok, NATIF_PIECE: dict(piece_ok, lr=80.0)}),
            ("publication fraîche mais CARTE FAUSSE", False,
             {NATIF_CARTE: dict(carte_ok, state=autre_option),
              NATIF_PIECE: piece_ok}),
            ("publication fraîche mais un segment MANQUE", False,
             {NATIF_CARTE: carte_ok,
              NATIF_PIECE: {"state": noms[0], "lr": 120.0,
                            "attrs": {"options": list(noms[:-1])}}}),
            ("entité carte DISPARUE", False, {NATIF_PIECE: piece_ok}),
            ("entité PIÈCES DISPARUE", False, {NATIF_CARTE: carte_ok}),
            ("pièces exposées VIDES", False,
             {NATIF_CARTE: carte_ok,
              NATIF_PIECE: {"state": noms[0], "lr": 120.0,
                            "attrs": {"options": []}}}),
            ("attribut `options` ABSENT", False,
             {NATIF_CARTE: carte_ok,
              NATIF_PIECE: {"state": noms[0], "lr": 120.0, "attrs": {}}}),
            ("aucune publication du tout", False, {}),
        ),
        "t_eau": (
            ("valeur juste, intensité et mode frais", True,
             {NATIF_EAU: eau_ok, NATIF_MODE: mode_ok}),
            ("intensité fraîche mais INCORRECTE", False,
             {NATIF_EAU: dict(eau_ok, state=autre_eau), NATIF_MODE: mode_ok}),
            ("valeurs justes mais mode PÉRIMÉ", False,
             {NATIF_EAU: eau_ok, NATIF_MODE: dict(mode_ok, lr=80.0)}),
            ("valeurs justes mais intensité PÉRIMÉE", False,
             {NATIF_EAU: dict(eau_ok, lr=80.0), NATIF_MODE: mode_ok}),
            # Relevé par l'audit : les deux entités sont FRAÎCHES, l'intensité
            # est CORRECTE, et le mode dérivé est pourtant incohérent. Écrire
            # le mode est interdit (ASP-INV-12) : il ne peut être que
            # CONFIRMÉ, et une incohérence signe un réglage non appliqué.
            ("intensité juste et fraîche mais MODE DÉRIVÉ INCOHÉRENT", False,
             {NATIF_EAU: eau_ok, NATIF_MODE: dict(mode_ok, state=autre_mode)}),
            ("mode juste et frais mais ENTITÉ INTENSITÉ DISPARUE", False,
             {NATIF_MODE: mode_ok}),
            ("intensité juste et fraîche mais ENTITÉ MODE DISPARUE", False,
             {NATIF_EAU: eau_ok}),
            ("aucune publication du tout", False, {}),
        ),
        "t_aspiration": (
            ("attribut juste et entité fraîche", True, {NATIF_VACUUM: vac_ok}),
            ("attribut juste mais entité PÉRIMÉE", False,
             {NATIF_VACUUM: dict(vac_ok, lr=80.0)}),
            ("entité fraîche mais attribut INCORRECT", False,
             {NATIF_VACUUM: dict(vac_ok, attrs={"fan_speed": autre_asp})}),
            ("entité fraîche mais attribut `fan_speed` ABSENT", False,
             {NATIF_VACUUM: dict(vac_ok, attrs={})}),
            ("entité DISPARUE", False, {}),
        ),
    }


def _postcondition_rendue(instant, gabarit, valeur_instant=None,
                          ctx=None) -> list[str]:
    """Rend la postcondition sur des états simulés et confronte le verdict.

    `valeur_instant` est la valeur RÉELLEMENT rendue par le gabarit d'instant
    du moteur, et non un flottant figé par le checker. Sans cela, le contrôle
    testerait une comparaison que le moteur ne fait pas : un instant antidaté
    ou retypé passerait, puisque la postcondition serait jouée avec la valeur
    du checker et non avec la sienne.
    """
    errs = []
    if ctx is None:                       # contexte de repli, sans référentiel
        ctx = {"nom": "contexte nu",
               "ctx_carte": {"option": "RDC", "noms": ["Salon", "Entrée",
                                                       "WC RDC",
                                                       "Cage d'escaliers"]},
               "eau_cible": "off", "mode_attendu": "vacuum",
               "aspiration_cible": "balanced",
               "t_carte": T0_SIM, "t_eau": T0_SIM, "t_aspiration": T0_SIM}
    cas = cas_postcondition(ctx)
    contexte = {k: v for k, v in ctx.items() if k != "nom"}
    if valeur_instant is not None:
        contexte = dict(contexte, **{instant: valeur_instant})
    for libelle, attendu, etats in cas[instant]:
        try:
            rendu = _env_jinja(etats, horloge=T0_SIM).from_string(
                gabarit).render(**contexte).strip()
        except Exception as exc:                    # noqa: BLE001
            errs.append(f"ASP-CI-27 : la postcondition de `{instant}` lève sur "
                        f"« {libelle} » ({exc}) — une garde qui lève ne refuse "
                        f"pas, elle casse la séquence.")
            continue
        obtenu = rendu == "True"
        if obtenu is not attendu:
            errs.append(
                f"ASP-CI-27 : postcondition de `{instant}` [{ctx['nom']}] — « {libelle} » "
                f"rend {rendu!r}, attendu {attendu}. "
                + ("Une confirmation doit tenir sur ce cas."
                   if attendu else
                   "Ce cas doit REFUSER : une valeur périmée, fausse ou "
                   "illisible ne confirme rien (ASP-INV-72)."))
    return errs


def check_ecritures_preparatoires(top, corps=None) -> list[str]:
    """ASP-CI-27 — allowlist fermée, instants propres, fraîcheur, refus, ordre.

    Le patron opposable, pour chacune des TROIS écritures et pour elles seules :

        variables: t_X = now().timestamp()      (instant PROPRE, avant l'appel)
        action:    <écriture>  continue_on_error: true
        …
        wait_template: <valeur exacte> ET <fraîcheur > t_X>   timeout 30 s
        choose:        NOT(<la même postcondition>) -> <refus> + stop:

    L'appariement écriture ↔ confirmation se fait par le NOM DE L'INSTANT, et
    non par l'adjacence : la séquence V-A apparie délibérément les deux
    premières écritures avant de les confirmer, pour que le rafraîchissement
    provoqué par l'eau publie aussi le contexte cartographique.

    Le CHEMIN NOMINAL inclut la garde d'abstention de la sélection de carte
    (07 §3.2 bis) : l'écriture qu'elle porte garde le rang du `choose` qui la
    garde, et la sémantique de cette garde est fermée par
    `check_garde_abstention`. Les instants, les confirmations et les relectures
    restent, eux, exigés au PREMIER NIVEAU — une preuve logée dans une branche
    ne serait pas opposable.
    """
    errs = []
    corps = corps if corps is not None else {"sequence": top}
    idx_svc, idx_var, idx_wait, etape_svc = {}, {}, {}, {}

    for i, step in enumerate(top):
        if not isinstance(step, dict):
            continue
        if isinstance(step.get("variables"), dict):
            for nom, gabarit in step["variables"].items():
                if nom in INSTANTS_PREPARATOIRES:
                    idx_var.setdefault(nom, (i, gabarit))
        if isinstance(step.get("wait_template"), str):
            for nom in INSTANTS_PREPARATOIRES:
                if re.search(rf'\b{nom}\b', step["wait_template"]):
                    idx_wait.setdefault(nom, i)

    for i, step in _nominal(top):
        svc = _service(step)
        if svc:
            for cible in _cibles(step):
                idx_svc.setdefault((svc, cible), i)
                etape_svc.setdefault((svc, cible), step)

    # (a) allowlist FERMÉE — nulle part ailleurs, à AUCUNE profondeur.
    #     La visite est exhaustive : `repeat`, `if`, `parallel` et toute
    #     séquence imbriquée sont inspectés, et le CHEMIN est cité.
    autorisees = {(s, c) for s, c, _t, _r in ECRITURES_PREPARATOIRES}
    au_premier_niveau = {id(s) for _r, s in _nominal(top)}
    for chemin, step in _actions(top):
        if not (isinstance(step, dict) and step.get("continue_on_error")):
            continue
        svc = _service(step)
        couple = (svc, (_cibles(step) or [None])[0])
        if couple not in autorisees:
            errs.append(
                f"ASP-CI-27 : {chemin} — `continue_on_error` sur `{svc}` vers "
                f"`{couple[1]}` — hors des trois écritures préparatoires "
                f"autorisées. Interdit sur l'émission, sur les écritures de "
                f"helper et partout ailleurs (07 §3, ASP-INV-49).")
        elif id(step) not in au_premier_niveau:
            # Une écriture préparatoire AUTORISÉE, mais logée dans une
            # branche : elle n'est plus sur le chemin nominal, et l'ordre
            # V-A cesserait d'être opposable.
            errs.append(
                f"ASP-CI-27 : {chemin} — l'écriture préparatoire `{couple[1]}` "
                f"est imbriquée dans une structure conditionnelle ou répétée. "
                f"Les trois écritures appartiennent au CHEMIN NOMINAL, au "
                f"premier niveau de la séquence — seule la sélection de carte "
                f"peut être logée dans une GARDE D'ABSTENTION conforme, et "
                f"celle-ci n'en est pas une (07 §3, 07 §3.2 bis).")

    for svc, cible, instant, refus in ECRITURES_PREPARATOIRES:
        i_svc = idx_svc.get((svc, cible))
        if i_svc is None:
            errs.append(f"ASP-CI-27 : écriture préparatoire `{svc}` vers "
                        f"`{cible}` introuvable (07 §3).")
            continue
        # (b) l'écriture DOIT absorber l'exception, sinon le moteur se tait.
        #     Le drapeau est lu sur l'ÉTAPE elle-même, gardée ou non : la
        #     garde d'abstention retire l'appel, elle ne le protège pas.
        if not etape_svc[(svc, cible)].get("continue_on_error"):
            errs.append(
                f"ASP-CI-27 : sequence/{i_svc} — `{cible}` doit porter "
                f"`continue_on_error: true` : une exception de transport n'est "
                f"ni une réussite ni un refus, et seule la confirmation "
                f"tranche (07 §3, ASP-INV-50).")

        # (c) instant PROPRE, capturé avant l'appel, rendu numérique.
        pose = idx_var.get(instant)
        if pose is None:
            errs.append(f"ASP-CI-27 : instant de référence `{instant}` jamais "
                        f"capturé — la fraîcheur n'a plus d'origine.")
            continue
        i_var, gabarit = pose
        # (c1) FORME — canonique, strictement bornée.
        if not (isinstance(gabarit, str)
                and GABARIT_INSTANT_CANONIQUE.match(gabarit.strip())):
            errs.append(
                f"ASP-CI-27 : `{instant}` doit être EXACTEMENT "
                f"`{GABARIT_INSTANT}` — trouvé {gabarit!r}. Aucune "
                f"arithmétique (`- 3600` antidate la preuve, `+ 1` la "
                f"postdate), aucun filtre (`| string` la retype et fait LEVER "
                f"la comparaison, `| int` la tronque, `| default(0)` introduit "
                f"un repli), aucune référence à un autre instant.")
        # (c2) TYPAGE — le gabarit est RENDU, et son résultat doit être un
        #      nombre fini. Une exception de rendu est un ÉCART, jamais un cas
        #      ignoré : c'est précisément ce silence qui rouvrait un chemin
        #      muet.
        valeur = None
        try:
            valeur = rendu_ha(gabarit, horloge=T0_SIM) if isinstance(gabarit, str) \
                else None
        except Exception as exc:                     # noqa: BLE001
            errs.append(f"ASP-CI-27 : le gabarit de `{instant}` LÈVE au rendu "
                        f"({type(exc).__name__}: {exc}) — une capture qui lève "
                        f"arrête la séquence sans verdict.")
        else:
            if isinstance(valeur, bool) or not isinstance(valeur, (int, float)):
                errs.append(
                    f"ASP-CI-27 : `{instant}` se rend en "
                    f"{type(valeur).__name__} ({valeur!r}) — un instant doit "
                    f"être un NOMBRE. Une chaîne ferait lever la comparaison "
                    f"`>` dans la postcondition, et un booléen la rendrait "
                    f"absurde.")
                valeur = None
            elif valeur != valeur or valeur in (float("inf"), float("-inf")):
                errs.append(f"ASP-CI-27 : `{instant}` se rend en {valeur!r} — "
                            f"valeur non finie, aucune comparaison n'a de sens.")
                valeur = None
        if not i_var < i_svc:
            errs.append(f"ASP-CI-27 : `{instant}` est capturé APRÈS son "
                        f"écriture (sequence/{i_var} ≥ sequence/{i_svc}) — une "
                        f"publication antérieure à l'appel passerait pour "
                        f"fraîche.")

        # (d) la confirmation : un wait 30 s, puis un choose qui refuse.
        i_wait = idx_wait.get(instant)
        if i_wait is None:
            errs.append(f"ASP-CI-27 : aucune confirmation ne borne `{instant}` "
                        f"— la fraîcheur n'est jamais vérifiée.")
            continue
        if not i_svc < i_wait:
            errs.append(f"ASP-CI-27 : la confirmation de `{instant}` précède "
                        f"son écriture (sequence/{i_wait} ≤ sequence/{i_svc}).")
        wait = top[i_wait]
        if wait.get("timeout") != FENETRE_CONFIRMATION_YAML:
            errs.append(f"ASP-CI-27 : la confirmation de `{instant}` porte "
                        f"`timeout: {wait.get('timeout')!r}` — attendu "
                        f"{FENETRE_CONFIRMATION_YAML} (ASP-INV-69).")
        if wait.get("continue_on_timeout") is not True:
            errs.append(f"ASP-CI-27 : la confirmation de `{instant}` doit "
                        f"porter `continue_on_timeout: true` : une "
                        f"republication IDENTIQUE n'émet que "
                        f"`EVENT_STATE_REPORTED`, qui ne réveille PAS un "
                        f"`wait_template` — la décision revient à la relecture.")

        suivant = top[i_wait + 1] if i_wait + 1 < len(top) else None
        if not (isinstance(suivant, dict) and "choose" in suivant):
            errs.append(f"ASP-CI-27 : la confirmation de `{instant}` n'est pas "
                        f"suivie d'un `choose` de relecture — le refus ne peut "
                        f"plus être posé.")
            continue
        cond = _texte_conditions(suivant)
        if "wait.completed" in cond or "wait[" in cond:
            errs.append(f"ASP-CI-27 : la relecture de `{instant}` s'appuie sur "
                        f"`wait.completed` — or le wait n'est PAS réveillé par "
                        f"une republication identique. La décision doit "
                        f"réévaluer la postcondition COMPLÈTE.")
        if not re.search(rf'\b{instant}\b', cond):
            errs.append(f"ASP-CI-27 : la relecture qui suit la confirmation de "
                        f"`{instant}` ne réévalue pas la fraîcheur.")
        if refus not in _refus_du_choose(suivant):
            errs.append(f"ASP-CI-27 : la relecture de `{instant}` ne pose pas "
                        f"`{refus}` avec un `stop:` — trouvé "
                        f"{sorted(_refus_du_choose(suivant))}.")

        # (e) valeur ET fraîcheur, sur TOUTES les entités probantes, dans les
        #     DEUX gabarits. `last_updated` ne prouve rien : une republication
        #     identique ne le fait pas bouger (core.py, async_set_internal).
        for ou, gab in (("confirmation", wait.get("wait_template", "")),
                        ("relecture", cond)):
            for entite in ENTITES_PROBANTES[instant]:
                attendu = (f"as_timestamp(states.{entite}.last_reported, 0) "
                           f"> {instant}")
                if _normalise(attendu) not in _normalise(gab):
                    errs.append(
                        f"ASP-CI-27 : la {ou} de `{instant}` n'exige pas la "
                        f"publication fraîche de `{entite}` sous la forme "
                        f"`{attendu}` — une valeur correcte mais PÉRIMÉE "
                        f"passerait (ASP-IMC-1, ASP-INV-17).")
            if re.search(rf'last_updated[^\n]*{instant}', _normalise(gab)):
                errs.append(
                    f"ASP-CI-27 : la {ou} de `{instant}` compare "
                    f"`last_updated` : une republication à valeur identique "
                    f"mute `last_reported` SEUL. Preuve inopérante.")
            if re.search(rf'>=\s*{instant}', _normalise(gab)):
                errs.append(
                    f"ASP-CI-27 : la {ou} de `{instant}` compare `>=` — une "
                    f"publication exactement contemporaine de l'instant "
                    f"capturé ne prouve aucune postériorité.")

        # (h) la postcondition est RENDUE, comme ASP-CI-12 rend la charge
        #     utile : une expression qui ne calcule plus rien ne passe plus.
        contextes = contextes_postcondition(corps) or [None]
        if len(contextes) < 2:
            errs.append(
                "ASP-CI-27 : moins de DEUX contextes de rendu — une "
                "postcondition validée sur un seul couple carte/profil ne "
                "distingue pas une expression d'un littéral substitué.")
        for ctx in contextes:
            errs += _postcondition_rendue(instant, wait.get("wait_template", ""),
                                          valeur, ctx)

    # (f) les trois instants sont DISTINCTS et posés dans trois blocs séparés.
    poses = {n: p[0] for n, p in idx_var.items()}
    if len(set(poses.values())) != len(INSTANTS_PREPARATOIRES):
        errs.append(
            f"ASP-CI-27 : les trois instants doivent être capturés dans TROIS "
            f"blocs distincts, chacun collé à son écriture — trouvé "
            f"{poses}. Un instant global rendrait recevable, pour une "
            f"écriture, une publication antérieure à elle.")

    # (g) ordre structurel de la séquence V-A.
    jalons = [
        ("sélection carte", idx_svc.get((SVC_EAU, NATIF_CARTE))),
        ("écriture eau", idx_svc.get((SVC_EAU, NATIF_EAU))),
        ("confirmation carte", idx_wait.get("t_carte")),
        ("confirmation eau", idx_wait.get("t_eau")),
        ("écriture aspiration", idx_svc.get((SVC_ASPIRATION, NATIF_VACUUM))),
        ("commande", idx_svc.get((SVC_COMMANDE, NATIF_VACUUM))),
    ]
    if all(i is not None for _n, i in jalons):
        rangs = [i for _n, i in jalons]
        if rangs != sorted(rangs):
            errs.append(
                "ASP-CI-27 : ordre non conforme. Attendu : sélection carte < "
                "écriture eau < confirmation carte < confirmation eau < "
                "aspiration < commande — trouvé "
                + " < ".join(f"{n}({i})" for n, i in jalons) + ". L'eau doit "
                "précéder la confirmation de carte : elle seule provoque le "
                "`coordinator.async_refresh()` qui publie le contexte "
                "cartographique (07 §3).")
        i_conf_carte = idx_wait.get("t_carte")
        i_cmd = idx_svc.get((SVC_COMMANDE, NATIF_VACUUM))
        if i_cmd is not None and i_conf_carte is not None and i_cmd < i_conf_carte:
            errs.append("ASP-CI-27 : une commande de mission précède la "
                        "confirmation cartographique — violation directe "
                        "d'ASP-IMC-1.")

    # (j) la garde d'abstention, lorsqu'elle existe : forme, silence, rendu.
    errs += check_garde_abstention(top, corps)
    return errs


def _normalise(texte: str) -> str:
    """Retire tout blanc : la mise en forme d'un gabarit n'est pas normative."""
    return re.sub(r"\s+", "", texte or "")


def sans_commentaires_yaml(texte: str) -> str:
    """Neutralise les lignes de commentaire YAML, en conservant le compte.

    Un en-tête Arsenal ÉNUMÈRE ce que le fichier s'interdit : sans cette
    neutralisation, la clause « n'émet JAMAIS vacuum.start » déclencherait
    elle-même le contrôle qui interdit `vacuum.start`.
    """
    return "\n".join("" if l.lstrip().startswith("#") else l
                     for l in texte.splitlines())


# ═════════════════════════════════════════════════════════════
# C-6 — SLOTS CRITIQUES LITTÉRAUX
#
# LE DÉFAUT. Les gardes de ce module cherchent `vacuum.start`,
# `button.press`, `notify.` ou un identifiant d'entité EN SOUS-CHAÎNE du YAML
# livré. Home Assistant, lui, résout la valeur d'un slot par Jinja avant de
# l'employer : `service: "{{ 'vacu' ~ 'um.start' }}"` commande réellement
# l'appareil sans qu'aucune sous-chaîne interdite n'apparaisse. Les gardes
# concluaient « absent » là où la vérité est « je ne sais pas ».
#
# LA RÈGLE, et elle tient en une phrase. Dans les fichiers du domaine que ce
# module protège NOMMÉMENT, les quatre slots critiques — `service`, `action`,
# `perform_action`, `entity_id` — doivent être LITTÉRAUX. Tout `{{` ou `{%`
# dans leur valeur est refusé, avec le fichier, la ligne et la clé.
#
# POURQUOI PAS DE RÉSOLUTION. Décider ce que vaut un gabarit demanderait de
# reproduire Jinja et la portée réelle des variables de Home Assistant. Une
# reproduction partielle se contourne par le premier filtre non prévu et
# introduit ses propres faux positifs : elle rend un verdict là où elle
# devrait s'abstenir. Refuser le gabarit à cet endroit précis ne demande
# aucun verdict — et c'est exactement ce que le domaine peut exiger de ses
# propres fichiers, où aucun slot critique n'est aujourd'hui templatisé.
#
# PORTÉE, dite plutôt que passée sous silence. La règle ne s'applique QU'AUX
# périmètres nominatifs (`RUNTIME_FICHIERS`, `DOSSIER_N1`). Elle ne balaie
# pas le dépôt, ne cherche aucun marqueur de contenu, et ne remplace aucune
# garde existante : elle leur garantit un texte sur lequel elles disent vrai.
# Un fichier tiers qui construirait une commande reste hors garantie — c'est
# une limite assumée, renvoyée à la revue humaine (L2/M2), pas un oubli.
# ═════════════════════════════════════════════════════════════

CLES_SERVICE = ("service", "action", "perform_action")
CLES_CIBLE = ("entity_id",)
CLES_SENSIBLES = CLES_SERVICE + CLES_CIBLE

INDICATEUR_BLOC = re.compile(r"^[|>][+-]?\d*$")
LIGNE_SLOT = re.compile(
    r"^(?P<tete>[ \t]*(?:-[ \t]+)?)"
    r"(?P<cle>service|action|perform_action|entity_id)"
    r"[ \t]*:[ \t]*(?P<val>.*?)[ \t]*$")


def slots_sensibles(txt, cles=CLES_SENSIBLES):
    """(ligne, clé, valeur nue) de chaque slot critique du texte.

    Les scalaires de bloc (`>-`, `|`) sont recollés — sans quoi un gabarit
    écrit sous la clé, et non sur sa ligne, échapperait au relevé. Les lignes
    de commentaire sont ignorées.

    C'est une lecture de SCALAIRES, et rien de plus : ni flow mapping, ni
    alias, ni ancre, ni ciblage par `device_id`. Ceux-là relèvent du visiteur
    YAML du lot M2, et le verrou `VISITEUR_YAML_RECURSIF` reste fermé.
    """
    if not isinstance(txt, str):
        return []
    lignes = txt.splitlines()
    out = []
    for i, ligne in enumerate(lignes):
        if ligne.lstrip().startswith("#"):
            continue
        m = LIGNE_SLOT.match(ligne)
        if not m or m.group("cle") not in cles:
            continue
        val = m.group("val")
        if INDICATEUR_BLOC.match(val):
            marge, corps, j = len(m.group("tete")), [], i + 1
            while j < len(lignes):
                s = lignes[j]
                if s.strip() and (len(s) - len(s.lstrip())) <= marge:
                    break
                corps.append(s.strip())
                j += 1
            val = " ".join(x for x in corps if x)
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        out.append((i + 1, m.group("cle"), val))
    return out


def slots_templatises(txt, cles=CLES_SENSIBLES):
    """Les slots critiques dont la valeur porte du Jinja."""
    return [(no, cle, val) for no, cle, val in slots_sensibles(txt, cles)
            if "{{" in val or "{%" in val]


def refus_slots_templatises(code: str, rel: str, txt: str,
                            cles=CLES_SENSIBLES) -> list[str]:
    """Le refus, formulé une seule fois pour tous les sites d'appel."""
    return [
        f"{code} : {rel}:{no} — `{cle}` porte un gabarit Jinja : "
        f"{val.strip()[:80]!r}. Dans les fichiers du domaine, les slots "
        f"critiques sont LITTÉRAUX : un identifiant assemblé en Jinja "
        f"désigne à l'exécution ce qu'aucune garde textuelle ne peut lire. "
        f"Écrire la valeur en clair."
        for no, cle, val in slots_templatises(txt, cles)]


# ═════════════════════════════════════════════════════════════
# RUNTIME L1 — ASP-CI-11 … ASP-CI-21
#
# Le domaine cesse d'être antérieur au runtime : les obligations de CONDUITE
# deviennent confrontables. Ces quinze contrôles ne relisent PAS le contrat pour
# se donner raison — chacun est ancré soit sur une constante de module figée
# ici, soit sur la table du contrat, soit sur le comportement RÉEL du gabarit
# (les charges utiles sont RENDUES, pas cherchées à la regex).
# ═════════════════════════════════════════════════════════════

RUNTIME_MOTEUR = "10_scripts/aspirateur/lancer_mission.yaml"
RUNTIME_HELPERS = "04_input_texts/aspirateur/mission.yaml"
RUNTIME_ETAT = "12_template_sensors/aspirateur/etat_canonique.yaml"
RUNTIME_MOTIF = "12_template_sensors/aspirateur/motif_lisible.yaml"
RUNTIME_GARDE = "12_template_sensors/aspirateur/conditions_lancement_hors_carte.yaml"
RUNTIME_FICHIERS = (RUNTIME_MOTEUR, RUNTIME_HELPERS, RUNTIME_ETAT,
                    RUNTIME_MOTIF, RUNTIME_GARDE)

# Identifiants ATTRIBUÉS PAR L'OPÉRATEUR au lot L1 (ASP-INV-58 : le contrat
# n'en propose aucun). Figés ici : un renommage silencieux échoue.
ID_MOTEUR = "aspirateur_lancer_mission"
ID_VERDICT = "input_text.aspirateur_mission_verdict"
ID_TRACE = "input_text.aspirateur_derniere_intention_lancee"
ID_ETAT_CANON = "aspirateur_etat_canonique"
ID_MOTIF = "aspirateur_motif_lisible"
ID_GARDE = "aspirateur_conditions_lancement_hors_carte"

# ═════════════════════════════════════════════════════════════
# VOCABULAIRE DU VERDICT — 34 valeurs, TROIS ecrivains (lot L2)
#
# Jusqu'au lot L1, le verdict avait UN ecrivain et 18 valeurs. Le lot L2 en
# ajoute deux, et seize valeurs. Les trois ensembles sont figes ici, SEPAREMENT
# et non par difference : c'est ce qui rend detectable un deplacement de valeur
# d'un writer a l'autre, la ou un vocabulaire global en un seul bloc laisserait
# passer exactement cela.
#
# La DISJONCTION porte sur les VALEURS, jamais sur les prefixes (D-09). Deux
# prefixes sont partages, et c'est conforme : `ECHEC/` entre W1 et W3,
# `CLOTURE/` entre W2 et W3. Une contrainte de prefixe exclusif serait donc
# fausse, et le checker n'en pose aucune.
#
# Source : contrat 15_conduite_et_supervision.md §1 et §3 ; cadrage V4 ratifie
# (D-44), 07_MACHINE_L2.md §3.3 bis, arbitrage A-4.
# ═════════════════════════════════════════════════════════════

# W1 — moteur de lancement. INCHANGE.
VERDICT_W1 = frozenset({
    "VALIDATION_EN_COURS",
    "REFUS/SELECTION_VIDE", "REFUS/SEGMENT_INCONNU", "REFUS/SELECTION_MULTI_CARTE",
    "REFUS/CARTE_NON_CONFIRMEE", "REFUS/PROFIL_INCONNU",
    "REFUS/PASSAGES_HORS_CONTRAT", "REFUS/PREREQUIS_MATERIEL_ABSENT",
    "REFUS/ROBOT_INDISPONIBLE", "REFUS/ETAT_NON_QUALIFIE",
    "REFUS/ERREUR_EQUIPEMENT", "REFUS/MISSION_DEJA_OUVERTE",
    "REFUS/SESSION_INACHEVEE", "REFUS/REGLAGE_NON_CONFIRME",
    "COMMANDE/ISSUE_NON_ETABLIE", "EMISSION/COMMANDE_ACCEPTEE",
    "ECHEC/TRANSITION_NON_OBSERVEE", "LANCEE/DEMARRAGE_OBSERVE"})

# W2 — script de conduite. Trois valeurs d'ENGAGEMENT, trois issues de pause,
# trois de reprise, deux cloturent l'arret, une cloture le retour non entre.
VERDICT_W2 = frozenset({
    "CONDUITE/PAUSE_ENGAGEE", "CONDUITE/PAUSE_CONFIRMEE",
    "CONDUITE/PAUSE_NON_CONFIRMEE",
    "CONDUITE/REPRISE_ENGAGEE", "CONDUITE/REPRISE_CONFIRMEE",
    "CONDUITE/REPRISE_NON_CONFIRMEE",
    "CONDUITE/ARRET_ENGAGE", "CLOTURE/APRES_ARRET_CONFIRME",
    "CLOTURE/APRES_ARRET_NON_CONFIRME",
    "CONDUITE/RETOUR_ENGAGE", "CLOTURE/APRES_RETOUR_NON_CONFIRME"})

# W3 — automation de supervision. Cinq valeurs, TOUTES terminales.
VERDICT_W3 = frozenset({
    "ECHEC/MISSION_INTERROMPUE", "ECHEC/ERREUR_EN_MISSION",
    "CLOTURE/FIN_NOMINALE", "CLOTURE/APRES_RETOUR_CONFIRME",
    "CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE"})

# Vocabulaire FERME du verdict — l'UNION des trois, et rien d'autre.
VOCABULAIRE_VERDICT = VERDICT_W1 | VERDICT_W2 | VERDICT_W3

# Classe O, sous-classe O-R comprise — la porte d'entree du 15 §2. NEUF
# valeurs : la seule de W1 qui ouvre, plus les huit de conduite hors clotures.
CLASSE_O = frozenset({
    "LANCEE/DEMARRAGE_OBSERVE",
    "CONDUITE/PAUSE_ENGAGEE", "CONDUITE/PAUSE_CONFIRMEE",
    "CONDUITE/PAUSE_NON_CONFIRMEE",
    "CONDUITE/REPRISE_ENGAGEE", "CONDUITE/REPRISE_CONFIRMEE",
    "CONDUITE/REPRISE_NON_CONFIRMEE",
    "CONDUITE/ARRET_ENGAGE", "CONDUITE/RETOUR_ENGAGE"})
CLASSE_O_R = "CONDUITE/RETOUR_ENGAGE"
# Classe T — HUIT issues terminales : trois clotures de W2, les cinq de W3.
CLASSE_T = frozenset({
    "CLOTURE/APRES_ARRET_CONFIRME", "CLOTURE/APRES_ARRET_NON_CONFIRME",
    "CLOTURE/APRES_RETOUR_NON_CONFIRME"}) | VERDICT_W3
# Les quatre valeurs d'ENGAGEMENT — la fenetre de relecture, rendue visible
# dans le verdict. C'est ce que W3 lit pour s'abstenir (A-11, regle 2).
ENGAGEMENTS_W2 = ("CONDUITE/PAUSE_ENGAGEE", "CONDUITE/REPRISE_ENGAGEE",
                  "CONDUITE/ARRET_ENGAGE", "CONDUITE/RETOUR_ENGAGE")

# Codes du catalogue que L1 NE PEUT PAS écrire, et pourquoi. Le moteur ne doit
# en porter AUCUN littéralement : un verdict anticipé affirmerait un rejet
# avant qu'un rejet soit observable. Leur TRADUCTION reste obligatoire dans le
# motif lisible — le catalogue demeure total.
CODES_HORS_PORTEE_L1 = {
    "COMMANDE_REJETEE": "un rejet n'est distinguable d'une interruption que "
                        "par un observateur survivant à l'appel",
    "CANAL_INDISPONIBLE": "appartient à l'appelant, qui seul observe une "
                          "erreur de transport",
    "MISSION_INTERROMPUE": "supervision continue, hors L1",
    "ERREUR_EN_MISSION": "supervision continue, hors L1"}

# Valeurs de cycle de vie que le motif lisible doit traduire en plus des
# 18 codes du catalogue. DIX-HUIT depuis le lot L2 : les quatre du lot L1, les
# onze de la conduite, et les trois valeurs de supervision qui n'appartiennent
# a aucun catalogue. Les deux autres valeurs de W3 — mission interrompue et
# erreur en mission — SONT des codes du catalogue et ne comptent pas ici.
CYCLE_DE_VIE = ("VALIDATION_EN_COURS", "ISSUE_NON_ETABLIE",
                "COMMANDE_ACCEPTEE", "DEMARRAGE_OBSERVE",
                "PAUSE_ENGAGEE", "PAUSE_CONFIRMEE", "PAUSE_NON_CONFIRMEE",
                "REPRISE_ENGAGEE", "REPRISE_CONFIRMEE",
                "REPRISE_NON_CONFIRMEE",
                "ARRET_ENGAGE", "APRES_ARRET_CONFIRME",
                "APRES_ARRET_NON_CONFIRME",
                "RETOUR_ENGAGE", "APRES_RETOUR_NON_CONFIRME",
                "FIN_NOMINALE", "APRES_RETOUR_CONFIRME",
                "ISSUE_OPAQUE_APRES_REDEMARRAGE")

# Entités natives dont le moteur a besoin, par rôle. Figées ici : elles sont
# CONFRONTÉES à l'audit (ASP-CI-21), jamais tirées de lui.
NATIF_CARTE = "select.roborock_q7_max_carte_selectionnee"
NATIF_EAU = "select.roborock_q7_max_intensite_de_frottement"
NATIF_MODE = "select.entree_roborock_q7_max_mode_de_nettoyage"
NATIF_VACUUM = "vacuum.roborock_q7_max"
NATIF_PIECE = "sensor.roborock_q7_max_piece_actuelle"
NATIF_ETAT = "sensor.roborock_q7_max_etat"
NATIF_ERR_VAC = "sensor.roborock_q7_max_erreur_de_l_aspirateur"
NATIF_ERR_DOCK = "sensor.roborock_q7_max_dock_erreur_de_dock"
NATIF_SESSION = "binary_sensor.roborock_q7_max_nettoyage"
NATIF_MOP = "binary_sensor.roborock_q7_max_serpilliere_fixee"

# Les quatre témoins du §5.1, et leurs valeurs nominales (ARB-5). Le moteur ET
# la garde template doivent appliquer la MÊME règle sur les MÊMES entités.
TEMOINS_GARDE = (NATIF_ETAT, NATIF_ERR_VAC, NATIF_ERR_DOCK, NATIF_SESSION)
NOMINAL_ERR_VAC = "none"
NOMINAL_ERR_DOCK = "ok"

# Séquence normative : eau -> aspiration -> commande (ASP-INV-34, ASP-INV-35).
SVC_EAU = "select.select_option"
SVC_ASPIRATION = "vacuum.set_fan_speed"
SVC_COMMANDE = "vacuum.send_command"
COMMANDE_SEGMENTEE = "app_segment_clean"

# Voies formellement interdites (07 §6).
VOIES_INTERDITES = ("app_zoned_clean", "set_vacuum_zoned_cleaning", "repeats",
                    "vacuum.start", "vacuum.clean_area", "clean_area",
                    "app_start", "resume_segment_clean")

# Comparaisons EXIGEES a l'etape 11, temoin par temoin. C'est la comparaison
# qui est controlee, jamais la seule presence du nom : retirer
# `g2_err_dock != 'ok'` en laissant `g2_err_dock` ailleurs passait au vert dans
# la version precedente, alors qu'un dock en erreur ne refusait plus rien.
TEMOINS_TARDIFS = ("g2_etat", "g2_err_vac", "g2_err_dock", "g2_session")
COMPARAISONS_TARDIVES = (
    ("g2_etat", "in classe_a", "REFUS/MISSION_DEJA_OUVERTE"),
    ("g2_etat", "== 'error'", "REFUS/ERREUR_EQUIPEMENT"),
    ("g2_etat", "in classe_e_indispo", "REFUS/ROBOT_INDISPONIBLE"),
    ("g2_etat", "not in classe_r", "REFUS/ETAT_NON_QUALIFIE"),
    ("g2_err_vac", "in indispo", "REFUS/ROBOT_INDISPONIBLE"),
    ("g2_err_vac", "!= 'none'", "REFUS/ERREUR_EQUIPEMENT"),
    ("g2_err_dock", "in indispo", "REFUS/ROBOT_INDISPONIBLE"),
    ("g2_err_dock", "!= 'ok'", "REFUS/ERREUR_EQUIPEMENT"),
    ("g2_session", "in indispo", "REFUS/ROBOT_INDISPONIBLE"),
    ("g2_session", "== 'on'", "REFUS/SESSION_INACHEVEE"),
)

FENETRE_CONFIRMATION_YAML = "00:00:30"
FENETRE_TRANSITION_YAML = "00:01:00"
NB_CONFIRMATIONS = 3          # carte (6), eau (8), aspiration (10)

# ═════════════════════════════════════════════════════════════
# RUNTIME L2 — conduite et supervision (lot L2)
#
# Trois fichiers, NOMMES ici. Le perimetre ne vient pas d'une recherche de
# mots dans le depot : il vient de cette liste, exactement comme
# `RUNTIME_FICHIERS` pour le lot L1. Un quatrieme fichier qui commanderait
# l'appareil ou ecrirait le verdict est refuse par le balayage du depot.
#
# AUCUN CONTROLE NEUF n'est cree pour ce lot. Les cinq controles de conduite
# deja en place — ASP-CI-11, 14, 18, 19, 20 — voient leur PERIMETRE etendu,
# et les deux controles de projection — ASP-CI-37, 39 — leur table de
# writers elargie. `ASP-CI-10` n'est PAS amende : les quatre fenetres L2
# sont mutualisees a une valeur deja admise, et ne produisent donc aucune
# duree concurrente. `ASP-CI-28` reste RESERVE au lot U0.
# ═════════════════════════════════════════════════════════════

RUNTIME_L2_CONDUITE = "10_scripts/aspirateur/conduire_mission.yaml"
RUNTIME_L2_SUPERVISION = "11_automations/aspirateur/supervision_mission.yaml"
RUNTIME_L2_PROJECTION = "11_automations/aspirateur/notification_mission.yaml"
RUNTIME_L2_FICHIERS = (RUNTIME_L2_CONDUITE, RUNTIME_L2_SUPERVISION,
                       RUNTIME_L2_PROJECTION)

# Identifiants ATTRIBUES PAR L'OPERATEUR (A-3, rendu en V4). Figes ici : un
# renommage silencieux echoue (ASP-INV-58).
ID_CONDUITE = "aspirateur_conduire_mission"
ID_MOTIF_ENTITE = "sensor.aspirateur_motif_lisible"
AID_SUPERVISION = "10280000000001"      # W3 — ecrivain du verdict
AID_PROJECTION_MISSION = "10280000000002"   # projection de cycle, lecteur pur
NOTIF_MISSION = "aspirateur_mission"
TITRE_NOTIF_MISSION = "\U0001F916 Aspirateur \u2013 Mission en cours"

# Table des ECRIVAINS du verdict : {fichier -> ensemble litteral}. C'est la
# forme exigee par l'amendement d'ASP-CI-11. La disjonction deux a deux et la
# couverture totale sont VERIFIEES, jamais supposees.
WRITERS_VERDICT = {
    RUNTIME_MOTEUR: VERDICT_W1,
    RUNTIME_L2_CONDUITE: VERDICT_W2,
    RUNTIME_L2_SUPERVISION: VERDICT_W3,
}
# LECTEUR nominatif du verdict : la projection persistante de mission, et elle
# seule. Elle a le droit de MENTIONNER le helper ; elle n'a AUCUN droit
# d'ecriture — l'ecrivain reste le trio (ASP-INV-31, ASP-INV-86).
# AMENDEMENT U0 — l'exception nominative de LECTURE du verdict s'ouvre a un
# SECOND objet, et a un seul : l'automation de remise a zero de la
# composition. Elle en a structurellement besoin — la frontiere « apres tous
# les refus, avant l'emission » n'est lisible que dans le verdict (A-12) —, et
# l'exception reste NOMINATIVE : elle nomme un fichier, jamais un motif.
LECTEURS_VERDICT = frozenset({RUNTIME_L2_PROJECTION, RUNTIME_U0_AUTO})
# Fichiers ou un appel d'appareil est admis. DEUX, et deux seulement.
COMMANDENT_APPAREIL = frozenset({RUNTIME_MOTEUR, RUNTIME_L2_CONDUITE})

# Les quatre gestes, leur service LITTERAL et leur valeur d'engagement.
# Figes ici : c'est ce qui rend detectable un geste dont la commande aurait
# ete remplacee par une autre — un `vacuum.stop` sous la branche « pause »
# passerait toutes les gardes textuelles sans cette table.
GESTES_L2 = ("pause", "reprise", "arret", "retour_base")
SERVICE_DU_GESTE = {
    "pause": "vacuum.pause",
    "reprise": "vacuum.start",
    "arret": "vacuum.stop",
    "retour_base": "vacuum.return_to_base",
}
ENGAGEMENT_DU_GESTE = {
    "pause": "CONDUITE/PAUSE_ENGAGEE",
    "reprise": "CONDUITE/REPRISE_ENGAGEE",
    "arret": "CONDUITE/ARRET_ENGAGE",
    "retour_base": "CONDUITE/RETOUR_ENGAGE",
}
# LE SEUL etat d'arret ATTESTE du domaine (15 §3.1). W2 y fonde sa
# postcondition d'arret, W3 sa conclusion d'interruption : dans les deux
# cas la regle est POSITIVE et FERMEE. La regle NEGATIVE qu'elle remplace
# — « ni activite, ni erreur, ni indisponibilite » — concluait sur TOUT
# etat de classe N, `emptying_the_bin` compris : une phase de dock
# nominale y produisait un verdict terminal FAUX.
ETAT_ARRET_ATTESTE = "idle"
# Les DEUX temoins d'amarrage, en DISJONCTION (15 §5). `docking` n'en fait
# pas partie : le contrat le classe en etat de MOUVEMENT (07 §5.0). Une
# disjonction, et non une sequence : exiger un passage par un etat
# intermediaire rendrait l'arrivee inobservable des qu'un echantillon
# manque.
TEMOINS_AMARRAGE = ("vacuum.roborock_q7_max", "charging")
# L'etat que le contrat classe en MOUVEMENT et que rien n'autorise a tenir
# pour une arrivee (07 §5.0). Fige ici pour que sa reintroduction echoue.
ETAT_MOUVEMENT_DOCK = "docking"
# Verdicts d'ARRIVEE — les deux seuls que la preuve d'amarrage autorise.
VERDICTS_ARRIVEE = frozenset({"CLOTURE/APRES_RETOUR_CONFIRME",
                              "CLOTURE/FIN_NOMINALE"})
# Fenetre de relecture L2 — la MEME constante que la confirmation L1 (A-15,
# mutualisation totale). Quatre occurrences, une par geste, et aucune autre.
NB_FENETRES_L2 = 4
# La primitive de demarrage est admise dans le SEUL fichier de conduite, et
# une seule fois (07 §7.1, ASP-INV-62). Les quatre ancres textuelles de sa
# garde fermee : etat de pause, session ouverte, temoin robot nominal, temoin
# dock nominal.
PRIMITIVE_DEMARRAGE = "vacuum.start"
GARDE_REPRISE_ANCRES = ("'paused'", NATIF_SESSION,
                        f"'{NOMINAL_ERR_VAC}'", f"'{NOMINAL_ERR_DOCK}'")

# Capacité d'un état de capteur Home Assistant.
MAX_ETAT_CAPTEUR = 255


def _ensure_list(valeur, chemin, anomalies):
    """Normalise un conteneur d'actions, comme le fait `cv.ensure_list`.

    Le schéma de scripts Home Assistant applique `ensure_list` **partout** où
    une séquence est attendue : un **mapping nu** y est donc une forme
    parfaitement valide, et `choose:` accepte un choix unique en mapping.

    Sans cette normalisation, le parcours itérait les **clés** d'un
    dictionnaire — quarante-deux mutations passaient au vert ou faisaient
    planter le checker sur une forme que Home Assistant accepte.

    | Entrée | Sortie |
    |---|---|
    | `None` | `[]` |
    | `list` | elle-même |
    | `dict` | `[dict]` |
    | autre | `[]` **et une anomalie datée du chemin** — jamais une exception |
    """
    if valeur is None:
        return []
    if isinstance(valeur, list):
        return valeur
    if isinstance(valeur, dict):
        return [valeur]
    anomalies.append(
        f"{chemin} — conteneur d'actions de type {type(valeur).__name__} "
        f"({valeur!r}) : ni liste, ni mapping, ni absent. Forme non admise "
        f"par le schéma de scripts.")
    return []


def _actions(seq, chemin="sequence", out=None, anomalies=None):
    """Visite RÉCURSIVE EXHAUSTIVE des actions, avec leur CHEMIN YAML.

    Rend des couples `(chemin, étape)` en ordre de document, en descendant
    dans **toutes** les structures composites du schéma de scripts Home
    Assistant 2026.8.3 :

        choose[].sequence · choose.default · repeat.sequence
        if.then · if.else · parallel[] (et parallel[].sequence)
        sequence imbriquée

    Une version antérieure ne descendait que dans `choose` : une seconde
    `vacuum.send_command` logée dans un `repeat:` — ou un second écrivain du
    verdict dans un `if.then` — restait INVISIBLE à tous les contrôles de
    détection. Ce n'est pas une omission théorique : seize mutations sont
    passées au vert avant cette correction.

    Le chemin est rendu avec l'étape pour que chaque écart cite l'endroit
    EXACT de l'action fautive, et non un simple index de premier niveau.
    """
    if out is None:
        out = []
    if anomalies is None:
        anomalies = []
    for i, step in enumerate(_ensure_list(seq, chemin, anomalies)):
        p = f"{chemin}/{i}"
        out.append((p, step))
        if not isinstance(step, dict):
            continue
        if "choose" in step:
            # `choose` accepte un CHOIX UNIQUE en mapping, pas seulement une
            # liste d'options.
            for j, opt in enumerate(_ensure_list(step["choose"],
                                                 f"{p}/choose", anomalies)):
                if isinstance(opt, dict):
                    _actions(opt.get("sequence"), f"{p}/choose/{j}/sequence",
                             out, anomalies)
            _actions(step.get("default"), f"{p}/default", out, anomalies)
        if "repeat" in step:
            rep = step["repeat"]
            _actions(rep.get("sequence") if isinstance(rep, dict) else None,
                     f"{p}/repeat/sequence", out, anomalies)
        if "if" in step:
            _actions(step.get("then"), f"{p}/then", out, anomalies)
            _actions(step.get("else"), f"{p}/else", out, anomalies)
        if "parallel" in step:
            for j, branche in enumerate(_ensure_list(step["parallel"],
                                                     f"{p}/parallel",
                                                     anomalies)):
                if isinstance(branche, dict) and "sequence" in branche:
                    _actions(branche["sequence"],
                             f"{p}/parallel/{j}/sequence", out, anomalies)
                else:
                    _actions(branche, f"{p}/parallel/{j}", out, anomalies)
        # `sequence` nue — mais pas celle d'un `repeat`, déjà visitée, ni
        # celle d'une branche `parallel`, visitée ci-dessus.
        if "sequence" in step and "repeat" not in step and "parallel" not in step:
            _actions(step["sequence"], f"{p}/sequence", out, anomalies)
    return out


def _anomalies_de_forme(seq):
    """Les conteneurs d'actions dont la forme n'est pas admise par le schéma."""
    anomalies: list[str] = []
    _actions(seq, "sequence", [], anomalies)
    return anomalies


def _aplatir(seq):
    """Les mêmes étapes que `_actions`, sans les chemins.

    Conservé pour les contrôles qui n'ont pas besoin de citer un chemin ;
    il est EXHAUSTIF comme `_actions`, dont il dérive.
    """
    return [step for _chemin, step in _actions(seq)]


def _service(step):
    return step.get("action") or step.get("service") if isinstance(step, dict) else None


def _cibles(step):
    tgt = (step.get("target") or {}) if isinstance(step, dict) else {}
    eid = tgt.get("entity_id")
    if eid is None:
        return []
    return [eid] if isinstance(eid, str) else list(eid)


def _ecritures_verdict(etapes):
    """Valeurs écrites dans le helper de verdict, en ordre de document."""
    out = []
    for i, step in enumerate(etapes):
        if _service(step) != "input_text.set_value":
            continue
        if ID_VERDICT not in _cibles(step):
            continue
        data = step.get("data")
        if isinstance(data, dict) and isinstance(data.get("value"), str):
            out.append((i, data["value"].strip()))
    return out


def _index_service(etapes, svc):
    return [i for i, s in enumerate(etapes) if _service(s) == svc]


def charge_utile(params_tpl: str, indices: list[int], passages: int):
    """REND réellement le gabarit de charge utile — aucune lecture à la regex.

    C'est ce qui rend ASP-CI-12 et ASP-CI-13 opposables : une forme nue, une
    enveloppe perdue ou un `repeat` mal conditionné se voient dans le RÉSULTAT,
    là où une recherche textuelle se laisserait berner par un commentaire.
    """
    import ast

    from jinja2 import StrictUndefined
    from jinja2.sandbox import ImmutableSandboxedEnvironment

    env = ImmutableSandboxedEnvironment(undefined=StrictUndefined)
    rendu = env.from_string(params_tpl).render(
        indices=indices, passages_int=passages).strip()
    try:
        return ast.literal_eval(rendu)
    except (ValueError, SyntaxError):
        return rendu


# ─────────────────────────────────────────────────────────────
# ASP-CI-26 / ASP-CI-27 — chemins d'exception et écritures préparatoires
#
# ASP-CI-26 énonce une propriété générale, dont les trois chemins silencieux
# du moteur L1 sont un cas particulier :
#
#   Toute étape susceptible de lever une exception non absorbée doit être
#   PRÉCÉDÉE d'un verdict qui reste VRAI si l'exécution s'arrête là.
#
# `VALIDATION_EN_COURS` ne survit pas : il affirme qu'une validation est en
# cours. `COMMANDE/ISSUE_NON_ETABLIE`, si : il constate une absence de
# connaissance. C'est ce seul critère qui distingue le traitement des
# écritures préparatoires de celui de l'émission, sans cas particulier.
#
# Portée : les appels qui commandent L'APPAREIL. Une écriture de helper est
# exclue — absorber son échec produirait un verdict faux en silence, ce qui
# serait pire que le subir ; sa capacité est gardée par ASP-CI-21.
# ─────────────────────────────────────────────────────────────

# Verdicts qui restent vrais si l'exécution s'arrête juste après.
VERDICTS_SURVIVANTS = frozenset(
    {v for v in VOCABULAIRE_VERDICT if v.startswith("REFUS/")}
    | {"COMMANDE/ISSUE_NON_ETABLIE", "EMISSION/COMMANDE_ACCEPTEE",
       "ECHEC/TRANSITION_NON_OBSERVEE", "LANCEE/DEMARRAGE_OBSERVE"})

# Domaines dont un appel atteint l'appareil, donc expose à un aléa externe.
DOMAINES_APPAREIL = ("select", "vacuum", "roborock")

# Les TROIS écritures préparatoires, seules autorisées à porter
# `continue_on_error: true`. Chaque ligne fige le quadruplet opposable :
# service, cible, instant de reference propre, refus attendu a l'expiration.
ECRITURES_PREPARATOIRES = (
    (SVC_EAU, NATIF_CARTE, "t_carte", "REFUS/CARTE_NON_CONFIRMEE"),
    (SVC_EAU, NATIF_EAU, "t_eau", "REFUS/REGLAGE_NON_CONFIRME"),
    (SVC_ASPIRATION, NATIF_VACUUM, "t_aspiration", "REFUS/REGLAGE_NON_CONFIRME"),
)
INSTANTS_PREPARATOIRES = tuple(t for _s, _c, t, _r in ECRITURES_PREPARATOIRES)

# FORME CANONIQUE STRICTEMENT BORNÉE du gabarit d'instant.
#
# Une simple sous-chaîne `now().timestamp()` est INSUFFISANTE, et six
# mutations l'ont prouvé : `- 3600` antidate la preuve, `+ 1` la postdate,
# `| string` la retype en chaîne — la comparaison lève alors un TypeError et
# ROUVRE un chemin silencieux —, `| int` la tronque à la seconde, `| default(0)`
# introduit un repli, `> 0` la rend booléenne.
#
# Le gabarit doit donc être EXACTEMENT l'heure courante, sans arithmétique,
# sans filtre, sans conversion, sans repli. Seuls les blancs varient.
GABARIT_INSTANT = "{{ now().timestamp() }}"
GABARIT_INSTANT_CANONIQUE = re.compile(
    r"^\{\{\s*now\(\)\s*\.\s*timestamp\(\)\s*\}\}$")

# Entités dont la publication doit être FRAÎCHE pour chaque confirmation.
# Carte : les DEUX lectures d'ASP-INV-29. Eau : intensité ET mode dérivé.
ENTITES_PROBANTES = {
    "t_carte": (NATIF_CARTE, NATIF_PIECE),
    "t_eau": (NATIF_EAU, NATIF_MODE),
    "t_aspiration": (NATIF_VACUUM,),
}

# ─────────────────────────────────────────────────────────────
# GARDE D'ABSTENTION — 07 §3.2 bis
#
# UNE seule des trois écritures préparatoires peut être gardée : la sélection
# de carte. Elle seule possède un postétat OBSERVABLE AVANT l'appel — la carte
# active attestée par les deux lectures d'ASP-INV-29. L'eau et l'aspiration
# n'en ont aucun : leur valeur cible ne se distingue pas d'une valeur ancienne
# sans la publication que l'écriture provoque. Les garder serait un repli.
#
# La garde ne dispense de RIEN : la confirmation de l'étape 7 reste au premier
# niveau, inconditionnelle, et réévalue valeur ET fraîcheur sur les DEUX
# entités — c'est `check_ecritures_preparatoires` qui l'exige, en n'admettant
# de confirmation qu'au PREMIER NIVEAU. Une abstention ne vaut donc jamais
# preuve.
# ─────────────────────────────────────────────────────────────
ECRITURE_GARDABLE = (SVC_EAU, NATIF_CARTE)


def _action_gardee(step):
    """L'écriture préparatoire logée dans une GARDE D'ABSTENTION conforme.

    Forme opposable de la garde : un `choose` portant UNE seule option, sans
    `default:`, dont la séquence ne contient QUE l'écriture du sélecteur de
    carte. Toute autre imbrication n'est pas une garde — elle reste refusée
    par l'allowlist d'ASP-CI-27.

    Rend l'étape d'écriture, ou `None`.
    """
    if not isinstance(step, dict) or "choose" not in step:
        return None
    if step.get("default") is not None:
        return None
    anomalies: list[str] = []
    options = _ensure_list(step.get("choose"), "", anomalies)
    if anomalies or len(options) != 1 or not isinstance(options[0], dict):
        return None
    seq = _ensure_list(options[0].get("sequence"), "", anomalies)
    if anomalies or len(seq) != 1 or not isinstance(seq[0], dict):
        return None
    action = seq[0]
    if (_service(action), (_cibles(action) or [None])[0]) != ECRITURE_GARDABLE:
        return None
    return action


def _nominal(top):
    """Le chemin nominal : couples `(rang de premier niveau, étape exécutée)`.

    Une étape de premier niveau porte son propre rang. L'écriture logée dans
    la garde d'abstention porte le rang du `choose` qui la garde : elle
    APPARTIENT au chemin nominal — la garde ne détourne pas la séquence vers
    une autre issue, elle retire au plus un appel dont le postétat est déjà
    atteint. L'ordre de la séquence V-A reste donc décidable, ce qu'une
    branche ordinaire ne permettrait pas.
    """
    out = []
    for i, step in enumerate(top):
        out.append((i, step))
        gardee = _action_gardee(step)
        if gardee is not None:
            out.append((i, gardee))
    return out


def cas_garde_abstention(ctx):
    """Les cas joués sur la garde, ENGENDRÉS depuis le référentiel du moteur.

    Le booléen attendu est celui de la CONDITION de la garde : `True` =
    l'appel est émis, `False` = le moteur s'abstient. La table fait foi, pas
    le gabarit.

    Aucune fraîcheur n'est jouée ici, et c'est délibéré : la garde décide d'un
    APPEL, jamais d'une confirmation. Une lecture périmée ne peut donc produire
    qu'une abstention — que l'étape 7 refusera si la publication n'est pas
    postérieure à `t_carte`.
    """
    option, noms = ctx["ctx_carte"]["option"], ctx["ctx_carte"]["noms"]
    carte_ok = {"state": option, "lr": 120.0}
    piece_ok = {"state": noms[0], "attrs": {"options": list(noms)}, "lr": 120.0}
    return (
        ("carte demandée DÉJÀ active, pièces concordantes", False,
         {NATIF_CARTE: carte_ok, NATIF_PIECE: piece_ok}),
        ("carte active DIFFÉRENTE", True,
         {NATIF_CARTE: dict(carte_ok, state=option + "-AUTRE"),
          NATIF_PIECE: piece_ok}),
        ("carte active `unknown`", True,
         {NATIF_CARTE: dict(carte_ok, state="unknown"), NATIF_PIECE: piece_ok}),
        ("carte active `unavailable`", True,
         {NATIF_CARTE: dict(carte_ok, state="unavailable"),
          NATIF_PIECE: piece_ok}),
        ("entité carte ABSENTE", True, {NATIF_PIECE: piece_ok}),
        ("entité PIÈCES ABSENTE", True, {NATIF_CARTE: carte_ok}),
        ("attribut `options` ABSENT", True,
         {NATIF_CARTE: carte_ok,
          NATIF_PIECE: {"state": noms[0], "lr": 120.0, "attrs": {}}}),
        ("pièces exposées VIDES", True,
         {NATIF_CARTE: carte_ok,
          NATIF_PIECE: {"state": noms[0], "lr": 120.0,
                        "attrs": {"options": []}}}),
        ("un segment du référentiel MANQUE", True,
         {NATIF_CARTE: carte_ok,
          NATIF_PIECE: {"state": noms[0], "lr": 120.0,
                        "attrs": {"options": list(noms[:-1])}}}),
        ("aucune publication du tout", True, {}),
    )


def check_garde_abstention(top, corps=None) -> list[str]:
    """ASP-CI-27 — la garde d'abstention de la sélection de carte (07 §3.2 bis).

    L'écriture NUE, au premier niveau, reste conforme : ce contrôle ne
    s'applique qu'à la forme gardée, et il en ferme la sémantique.

    Que la confirmation de l'étape 7, elle, reste au premier niveau et hors
    garde est déjà exigé par `check_ecritures_preparatoires` : `t_carte` n'y
    est borné que par un `wait_template` de PREMIER NIVEAU, faute de quoi
    « aucune confirmation ne borne `t_carte` ». Ce contrôle-ci n'y revient pas.

      (i)   la garde est UNIQUE, ne porte qu'UNE branche, aucun `default:`, et
            son unique étape est l'écriture gardée — rien d'autre ne s'y loge ;
      (ii)  la garde n'écrit AUCUN verdict et ne porte AUCUN `stop:` — une
            abstention n'est ni un refus ni une preuve ;
      (iii) la garde n'invoque NI `t_carte` NI `last_reported` : elle décide
            d'un appel, pas d'une confirmation, et emprunter la fraîcheur
            ferait passer une garde pour une postcondition ;
      (iv)  RENDUE sur les deux contextes du référentiel, elle s'abstient
            EXACTEMENT lorsque la carte active est lisible et concordante, et
            émet l'appel dans tous les autres cas — `unknown`, `unavailable`,
            entité absente, pièces illisibles ou incomplètes comprises.
    """
    errs: list[str] = []
    # Tout `choose` de premier niveau qui PORTE l'écriture de carte prétend
    # être la garde : sa conformité est examinée ici, jamais présumée.
    porteurs = [(i, s) for i, s in enumerate(top)
                if isinstance(s, dict) and "choose" in s
                and any((_service(a), (_cibles(a) or [None])[0])
                        == ECRITURE_GARDABLE for _ch, a in _actions([s]))]
    if not porteurs:
        return errs
    if len(porteurs) != 1:
        errs.append(
            f"ASP-CI-27 : {len(porteurs)} structures conditionnelles portent "
            f"la sélection de carte — la garde d'abstention est UNIQUE "
            f"(07 §3.2 bis).")
        return errs
    rang, garde = porteurs[0]

    # (ii) une abstention n'écrit rien et n'arrête rien.
    ecrits, _anos = _verdicts_du_document(garde)
    if ecrits:
        errs.append(
            f"ASP-CI-27 : la garde d'abstention (sequence/{rang}) écrit "
            f"{sorted(ecrits)}. S'abstenir d'un appel redondant n'est NI un "
            f"refus NI une issue : la garde ne pose aucun verdict, et seule la "
            f"confirmation de l'étape 7 tranche (07 §3.2, ASP-INV-71).")
    if any("stop" in s for s in _aplatir([garde]) if isinstance(s, dict)):
        errs.append(
            f"ASP-CI-27 : la garde d'abstention (sequence/{rang}) porte un "
            f"`stop:` — elle arrêterait la séquence sans verdict, exactement "
            f"le chemin muet qu'ASP-CI-26 proscrit (ASP-INV-49).")

    # (i) forme fermée : une branche, aucun `default:`, une seule étape.
    if _action_gardee(garde) is None:
        anomalies: list[str] = []
        options = _ensure_list(garde.get("choose"), "", anomalies)
        errs.append(
            f"ASP-CI-27 : la garde d'abstention (sequence/{rang}) n'a pas la "
            f"forme fermée exigée — UNE branche "
            f"(trouvé {len(options)}), aucun `default:` "
            f"(trouvé {garde.get('default') is not None}), et pour unique "
            f"étape l'écriture du sélecteur de carte. Toute autre forme "
            f"détourne le chemin nominal au lieu de retirer un appel "
            f"redondant (07 §3.2 bis).")
        return errs

    cond = _texte_conditions(garde)
    if not cond.strip():
        errs.append(
            f"ASP-CI-27 : la garde d'abstention (sequence/{rang}) ne porte "
            f"aucune condition — l'appel serait retiré inconditionnellement.")
        return errs

    # (iii) la garde n'emprunte pas la preuve de la confirmation.
    for emprunt, pourquoi in (
            ("t_carte", "l'instant de référence ne borne QUE la confirmation ; "
                        "aucune publication ne lui est postérieure au moment "
                        "où la garde s'évalue"),
            ("last_reported", "la fraîcheur est la preuve de l'étape 7 ; "
                              "l'emprunter ici ferait passer une décision "
                              "d'appel pour une postcondition")):
        if re.search(rf'\b{emprunt}\b', cond):
            errs.append(
                f"ASP-CI-27 : la garde d'abstention invoque `{emprunt}` — "
                f"{pourquoi} (ASP-INV-72).")

    # (iv) RENDUE, sur les deux contextes, cas par cas.
    contextes = contextes_postcondition(corps or {"sequence": top}) or []
    if len(contextes) < 2:
        errs.append(
            "ASP-CI-27 : moins de DEUX contextes de rendu pour la garde "
            "d'abstention — une garde validée sur un seul couple carte/profil "
            "ne distingue pas une expression d'un littéral substitué.")
    for ctx in contextes:
        for libelle, appel_attendu, etats in cas_garde_abstention(ctx):
            try:
                obtenu = rendu_ha(cond, etats=etats, horloge=T0_SIM,
                                  **{k: v for k, v in ctx.items()
                                     if k != "nom"})
            except Exception as exc:                     # noqa: BLE001
                errs.append(
                    f"ASP-CI-27 : la garde d'abstention LÈVE au rendu "
                    f"[{ctx['nom']}] — « {libelle} » ({type(exc).__name__}: "
                    f"{exc}). Une condition qui lève arrête la séquence sans "
                    f"verdict.")
                continue
            if not isinstance(obtenu, bool):
                errs.append(
                    f"ASP-CI-27 : la garde d'abstention se rend en "
                    f"{type(obtenu).__name__} ({obtenu!r}) [{ctx['nom']}] — "
                    f"« {libelle} ». Une condition doit être BOOLÉENNE.")
                continue
            if obtenu is not appel_attendu:
                errs.append(
                    f"ASP-CI-27 : la garde d'abstention [{ctx['nom']}] — "
                    f"« {libelle} » : attendu "
                    + ("l'APPEL" if appel_attendu else "l'ABSTENTION")
                    + ", obtenu "
                    + ("l'APPEL" if obtenu else "l'ABSTENTION")
                    + ". "
                    + ("Le moteur ne s'abstient QUE sur une carte active "
                       "LISIBLE et CONCORDANTE : `unknown`, `unavailable`, "
                       "une entité absente ou des pièces incomplètes ne "
                       "valent JAMAIS carte correcte (ASP-INV-45, "
                       "ASP-INV-51)." if appel_attendu else
                       "La carte demandée EST déjà la carte active attestée : "
                       "l'appel est un no-op qui journalise une ERREUR pour "
                       "une opération nominale (07 §3.2 bis)."))
    return errs


def _domaine(svc: str | None) -> str:
    return svc.split(".", 1)[0] if svc else ""


def _verdict_courant(top, i):
    """Verdict en vigueur sur le CHEMIN NOMINAL à l'entrée de l'étape i.

    Seules les écritures de PREMIER NIVEAU comptent. Une écriture logée dans
    une branche de `choose` est un refus, immédiatement suivi d'un `stop:` :
    elle n'est jamais en vigueur lorsqu'une étape ultérieure s'exécute. Les
    compter reviendrait à croire le moteur protégé par des refus qu'il n'a pas
    pris — c'est précisément le faux vert que ce contrôle doit éviter.
    """
    courant = None
    for j, step in enumerate(top):
        if j >= i:
            break
        if not isinstance(step, dict):
            continue
        if _service(step) != "input_text.set_value":
            continue
        if ID_VERDICT not in _cibles(step):
            continue
        data = step.get("data")
        if isinstance(data, dict) and isinstance(data.get("value"), str):
            courant = data["value"].strip()
    return courant


def check_chemins_silencieux(top) -> list[str]:
    """ASP-CI-26 — aucun appel vers l'appareil sous un verdict qui ne survit pas.

    Deux façons de se conformer, et deux seulement :
      a) porter `continue_on_error: true` — l'exception est journalisée puis
         absorbée, et la CONFIRMATION qui suit tranche (écritures
         préparatoires) ;
      b) être précédé d'un verdict survivant — l'arrêt laisse une trace
         honnête (émission).
    """
    errs = [f"ASP-CI-26 : {a}" for a in _anomalies_de_forme(top)]
    # Le chemin nominal, garde d'abstention comprise : une écriture gardée
    # reste un appel vers l'appareil, et doit se conformer comme les autres.
    for i, step in _nominal(top):
        if not isinstance(step, dict):
            continue
        svc = _service(step)
        if _domaine(svc) not in DOMAINES_APPAREIL:
            continue
        if step.get("continue_on_error"):
            continue
        courant = _verdict_courant(top, i)
        if courant in VERDICTS_SURVIVANTS:
            continue
        cible = (_cibles(step) or ["<sans cible>"])[0]
        errs.append(
            f"ASP-CI-26 : sequence/{i} — `{svc}` vers `{cible}` peut lever une "
            f"exception non absorbée alors que le verdict courant vaut "
            f"{courant!r}, qui ne survit pas à un arrêt. Aucun refus ne serait "
            f"posé : le moteur se tairait (ASP-INV-49, ASP-INV-50). Attendu : "
            f"`continue_on_error: true` suivi d'une confirmation qui refuse, "
            f"ou un verdict survivant posé avant l'appel.")
    return errs


# ─────────────────────────────────────────────────────────────
# Lecture STRUCTURELLE des ecrivains du verdict — lots L1 et L2
#
# La table `{fichier -> ensemble litteral}` d'ASP-CI-11 exige de savoir ce
# qu'un fichier ECRIT REELLEMENT, pas ce qu'il MENTIONNE : les trois writers
# citent tous des valeurs qu'ils n'ecrivent pas — le script de conduite et la
# supervision portent la liste des neuf valeurs de classe O pour tester la
# porte d'entree, dont une appartient au moteur. Un balayage textuel du
# vocabulaire accuserait donc les deux fichiers a tort.
#
# La lecture est donc STRUCTURELLE, et elle n'est complete QUE parce que trois
# gardes tiennent ensemble : le service et la cible sont litteraux (C-6), et la
# valeur ecrite est verifiee litterale ci-dessous. Une seule de ces trois
# gardes en moins, et un verdict pourrait etre assemble hors de portee.
# ─────────────────────────────────────────────────────────────

def _mappings(noeud):
    """Tous les mappings d'un document YAML, recursivement."""
    if isinstance(noeud, list):
        for x in noeud:
            yield from _mappings(x)
    elif isinstance(noeud, dict):
        yield noeud
        for v in noeud.values():
            yield from _mappings(v)


def _svc_de(step):
    """Nom de service d'une etape, sous ses trois cles possibles."""
    if not isinstance(step, dict):
        return None
    return (step.get("action") or step.get("service")
            or step.get("perform_action"))


def _ecrit_le_verdict(step) -> bool:
    return (_svc_de(step) == "input_text.set_value"
            and ID_VERDICT in _cibles(step))


def _verdicts_du_document(doc) -> tuple[set[str], list[str]]:
    """(valeurs litteralement ecrites, anomalies) pour un document YAML."""
    valeurs: set[str] = set()
    anomalies: list[str] = []
    for st in _mappings(doc):
        if not _ecrit_le_verdict(st):
            continue
        val = (st.get("data") or {}).get("value")
        if not isinstance(val, str) or "{{" in val or "{%" in val:
            anomalies.append(repr(val)[:60])
            continue
        valeurs.add(val.strip())
    return valeurs, anomalies


def check_table_writers(textes_l2) -> list[str]:
    """ASP-CI-11 — la table `{fichier -> ensemble litteral}` des trois writers.

    Trois proprietes, verifiees et non affirmees :
      · chaque fichier ecrit EXACTEMENT son ensemble — ni plus, ni moins ;
      · les trois ensembles sont DEUX A DEUX DISJOINTS (D-09) ;
      · leur UNION est le vocabulaire entier — aucune valeur orpheline.
    """
    errs: list[str] = []
    for rel, attendu in sorted(WRITERS_VERDICT.items(),
                               key=lambda kv: kv[0]):
        txt = textes_l2.get(rel)
        if txt is None:
            errs.append(f"ASP-CI-11 : le writer `{rel}` est ABSENT du depot — "
                        f"les {len(attendu)} valeurs qu'il porte n'auraient "
                        "aucun ecrivain (ASP-INV-86).")
            continue
        try:
            doc = yaml.safe_load(txt)
        except yaml.YAMLError as exc:
            errs.append(f"ASP-CI-11 : `{rel}` est illisible en YAML ({exc}).")
            continue
        vus, anomalies = _verdicts_du_document(doc)
        for mauvais in anomalies:
            errs.append(f"ASP-CI-11 : `{rel}` ecrit le verdict avec une valeur "
                        f"NON LITTERALE {mauvais} — une valeur assemblee en "
                        "Jinja n'est confrontable a aucun vocabulaire ferme "
                        "(ASP-INV-70).")
        if vus - attendu:
            errs.append(f"ASP-CI-11 : `{rel}` ecrit {sorted(vus - attendu)}, "
                        "hors de son ensemble. Un writer n'ecrit que SES "
                        "valeurs — sinon deux writers auraient la meme "
                        "(ASP-INV-86).")
        if attendu - vus:
            errs.append(f"ASP-CI-11 : `{rel}` n'ecrit jamais "
                        f"{sorted(attendu - vus)} — chaque valeur de "
                        "l'ensemble doit etre atteignable dans le fichier qui "
                        "la porte (ASP-CI-18).")
    noms = sorted(WRITERS_VERDICT)
    for i, a in enumerate(noms):
        for b in noms[i + 1:]:
            commun = WRITERS_VERDICT[a] & WRITERS_VERDICT[b]
            if commun:
                errs.append(f"ASP-CI-11 : `{a}` et `{b}` partagent "
                            f"{sorted(commun)} — la disjonction porte sur les "
                            "VALEURS (D-09) : aucune valeur n'a deux auteurs.")
    union = set()
    for ens in WRITERS_VERDICT.values():
        union |= ens
    if union != set(VOCABULAIRE_VERDICT):
        manque = sorted(set(VOCABULAIRE_VERDICT) - union)
        trop = sorted(union - set(VOCABULAIRE_VERDICT))
        errs.append(f"ASP-CI-11 : l'union des trois writers ne recouvre pas le "
                    f"vocabulaire — manquantes {manque}, en trop {trop}.")
    return errs


def check_conduite_forme(textes_l2) -> list[str]:
    """ASP-CI-11 — forme du script de conduite : un script, un mode, un champ."""
    errs: list[str] = []
    txt = textes_l2.get(RUNTIME_L2_CONDUITE)
    if txt is None:
        return [f"ASP-CI-11 : `{RUNTIME_L2_CONDUITE}` est absent — le lot L2 "
                "n'a pas d'ecrivain de conduite."]
    try:
        doc = yaml.safe_load(txt)
    except yaml.YAMLError as exc:
        return [f"ASP-CI-11 : `{RUNTIME_L2_CONDUITE}` illisible ({exc})."]
    if not isinstance(doc, dict) or list(doc) != [ID_CONDUITE]:
        return [f"ASP-CI-11 : le fichier de conduite doit declarer EXACTEMENT "
                f"le script `{ID_CONDUITE}` — trouve "
                f"{sorted(doc) if isinstance(doc, dict) else type(doc)} "
                "(ASP-INV-31, amendement L2)."]
    corps = doc[ID_CONDUITE]
    if corps.get("mode") != "single":
        errs.append(f"ASP-CI-11 : `{ID_CONDUITE}` doit porter `mode: single` — "
                    f"trouve {corps.get('mode')!r}. Deux gestes concurrents "
                    "emettraient deux commandes sur une meme mission.")
    recus = set(corps.get("fields") or {})
    if recus != {"geste"}:
        errs.append(f"ASP-CI-11 : le script de conduite expose {sorted(recus)} "
                    "— un seul champ, `geste`, et ferme aux quatre gestes "
                    "(D-02). Tout autre champ ouvrirait un parametre que le "
                    "contrat ne connait pas.")
    return errs


def refus_allowlist_lecteurs(lecteurs) -> list[str]:
    """ASP-CI-11 — l'exception nominative n'est ni DORMANTE, ni une breche.

    AMENDEMENT C45 LOT 3. Deux refus, et ils sont de nature differente.

    EXISTENCE. Un fichier nomme dans l'allowlist et absent du depot passait
    en silence : `yaml.safe_load("")` rend `None`, aucune ecriture n'est
    trouvee, et la preuve « lit le verdict, ne l'ecrit jamais » portait alors
    sur un document VIDE — donc sur rien. La question est posee au SYSTEME DE
    FICHIERS, jamais a un dictionnaire de balayage : un fichier peut manquer a
    un balayage pour une raison de filtre sans manquer au depot, et c'est bien
    l'existence REELLE que l'autorisation dormante met en cause. C'est
    exactement l'autorisation
    DORMANTE qu'ASP-CI-31 refuse deja pour l'allowlist de pression. La regle
    d'ordre 2 du chantier C45 en fait la raison meme pour laquelle le
    controle precede son objet : il le PRECEDE, il ne le DEVANCE pas. Le nom
    de la projection metier s'inscrit donc au lot 4, dans le commit meme qui
    cree le fichier — jamais avant.

    FRONTIERE. Le balayage d'anti-concurrence couvre TOUT le YAML de
    configuration, arbres Lovelace COMPRIS. Nommer un lecteur autorise sous
    `18_lovelace/` ou `19_button_card_templates/` relacherait donc
    mecaniquement l'interdit du chapitre 11 — l'UI consomme la PROJECTION
    metier, elle ne lit jamais le helper de verdict (ASP-INV-96). Le chantier
    en fait une condition d'ARRET : l'exception serait refusee en l'etat.
    """
    errs: list[str] = []
    for rel in sorted(lecteurs):
        if not (ROOT / rel).is_file():
            errs.append(
                f"ASP-CI-11 : `{rel}` est nomme lecteur pur du verdict mais "
                f"n'existe pas au depot — une autorisation DORMANTE. "
                f"L'exception nominative s'ouvre au fichier, JAMAIS avant "
                f"lui : le controle PRECEDE l'objet qu'il garde, il ne le "
                f"devance pas (ASP-INV-86, C45 §9 regle 2).")
        if rel.startswith(LOVELACE_DIRS):
            errs.append(
                f"ASP-CI-11 : `{rel}` est nomme lecteur pur du verdict et "
                f"reside dans un arbre Lovelace — l'UI consomme la PROJECTION "
                f"metier, elle ne lit jamais le helper de verdict. "
                f"L'ouverture nominative ne relache pas cet interdit "
                f"(ASP-INV-96, chapitre 11, C45 condition d'arret A6).")
    return errs


def check_ecrivain_unique(moteur_yaml, textes_runtime, yaml_depot) -> list[str]:
    """ASP-CI-11 — un seul moteur, un seul écrivain, une seule règle de garde."""
    errs = []
    if list(moteur_yaml) != [ID_MOTEUR]:
        errs.append(
            f"ASP-CI-11 : le fichier moteur doit déclarer EXACTEMENT le script "
            f"`{ID_MOTEUR}` — trouvé {sorted(moteur_yaml)} (ASP-INV-31).")
        return errs
    corps = moteur_yaml[ID_MOTEUR]
    if corps.get("mode") != "single":
        errs.append(f"ASP-CI-11 : `{ID_MOTEUR}` doit porter `mode: single` — "
                    f"trouvé {corps.get('mode')!r} (ASP-INV-32).")
    attendus = {"carte", "segments", "profil", "passages"}
    recus = set(corps.get("fields") or {})
    if recus != attendus:
        errs.append(f"ASP-CI-11 : l'intention est atomique — quatre champs "
                    f"exactement, {sorted(attendus)} ; trouvé {sorted(recus)} "
                    f"(ASP-INV-23).")

    # Aucun autre fichier du dépôt n'écrit les helpers ni ne commande le robot.
    #
    # AMENDEMENT L2 — deux listes d'autorisation NOMINATIVES, et pas une.
    #   · le VERDICT est mentionnable par les cinq fichiers L1, par les trois
    #     writers, et par la SEULE projection de mission, lectrice pure ;
    #   · la TRACE d'intention garde UN seul ecrivain, le moteur : ni la
    #     conduite ni la supervision ne la citent, et la conduite ne relance
    #     aucune intention (ASP-INV-15) ;
    #   · un appel d'appareil n'est admis que dans DEUX fichiers — le moteur
    #     et la conduite (ASP-INV-31, amendement L2 du 07 §1).
    verdict_admis = (set(RUNTIME_FICHIERS) | set(WRITERS_VERDICT)
                     | set(LECTEURS_VERDICT))
    for rel, txt in sorted(yaml_depot.items()):
        if ID_VERDICT in txt and rel not in verdict_admis:
            errs.append(f"ASP-CI-11 : {rel} référence `{ID_VERDICT}` — le "
                        f"verdict n'est mentionnable que par ses trois "
                        f"écrivains, par le runtime L1 et par la projection "
                        f"de mission (ASP-INV-86).")
        if ID_TRACE in txt and rel not in RUNTIME_FICHIERS:
            errs.append(f"ASP-CI-11 : {rel} référence `{ID_TRACE}` — la trace "
                        f"d'intention n'a qu'UN écrivain, le moteur : ni la "
                        f"conduite ni la supervision ne la connaissent "
                        f"(ASP-INV-15, ASP-INV-31).")
        # `- action: vacuum.stop` comme `  action: vacuum.stop` : le tiret de
        # liste fait partie de la ligne, l'oublier laisserait passer la forme
        # la plus courante. Le guillemet est optionnel — un scalaire cite est
        # le meme appel — et `perform_action` est l'alias moderne de
        # `service`, que la forme anterieure ignorait.
        if rel in COMMANDENT_APPAREIL:
            continue
        for m in re.finditer(r'^[ \t]*-?[ \t]*(?:action|service|perform_action)'
                             r'[ \t]*:[ \t]*["\']?'
                             r'(vacuum\.[a-z_]+|roborock\.[a-z_]+)["\']?[ \t]*$',
                             sans_commentaires_yaml(txt), re.M):
            errs.append(f"ASP-CI-11 : {rel} appelle `{m.group(1)}` — seuls le "
                        f"moteur et le script de conduite commandent "
                        f"l'appareil (ASP-INV-31).")

    errs += refus_allowlist_lecteurs(LECTEURS_VERDICT)

    # La projection de mission LIT le verdict ; elle ne l'ecrit JAMAIS.
    for rel in sorted(LECTEURS_VERDICT):
        try:
            # Le lecteur U0 n'appartient pas aux fichiers runtime L1/L2 : sans
            # ce repli sur le depot, la preuve « lit mais n'ecrit jamais »
            # porterait sur un document VIDE, donc sur rien.
            doc = yaml.safe_load(
                textes_runtime.get(rel) or yaml_depot.get(rel) or "")
        except yaml.YAMLError:
            continue
        ecrites, _ = _verdicts_du_document(doc)
        if ecrites:
            errs.append(f"ASP-CI-11 : {rel} ÉCRIT le verdict "
                        f"{sorted(ecrites)} — cette automation est un lecteur "
                        f"pur ; l'écrivain reste le trio W1/W2/W3 "
                        f"(ASP-INV-86).")

    # C-6 : dans les fichiers runtime que ce module nomme — les cinq du lot L1
    # et les trois du lot L2 —, les slots critiques sont litteraux. Les
    # balayages ci-dessus sont textuels ; sans cette regle,
    # `service: "{{ 'vacu' ~ 'um.start' }}"` les traversait sans qu'aucune
    # sous-chaine interdite n'apparaisse. Le perimetre vient des deux listes de
    # fichiers, pas d'une recherche de mots dans le contenu.
    for rel in RUNTIME_FICHIERS + RUNTIME_L2_FICHIERS:
        errs += refus_slots_templatises(
            "ASP-CI-11", rel,
            sans_commentaires_yaml(textes_runtime.get(rel, "")))

    errs += check_conduite_forme(textes_runtime)
    errs += check_table_writers(textes_runtime)

    # Moteur et garde template appliquent la MÊME règle sur les MÊMES témoins.
    garde = textes_runtime.get(RUNTIME_GARDE, "")
    mot = textes_runtime.get(RUNTIME_MOTEUR, "")
    for temoin in TEMOINS_GARDE:
        if temoin not in garde:
            errs.append(f"ASP-CI-11 : la garde `{ID_GARDE}` ignore le témoin "
                        f"`{temoin}` que le moteur consulte — deux règles "
                        f"divergentes pour une seule condition (07 §5.1).")
        if temoin not in mot:
            errs.append(f"ASP-CI-11 : le moteur ne relit pas `{temoin}` "
                        f"(07 §5.1).")
    for nominal, quoi in ((NOMINAL_ERR_VAC, "robot"), (NOMINAL_ERR_DOCK, "dock")):
        if f"'{nominal}'" not in garde:
            errs.append(f"ASP-CI-11 : la garde n'exige pas la valeur nominale "
                        f"`{nominal}` du témoin d'erreur {quoi} (ASP-INV-61).")
    return errs


def check_charge_utile(etapes) -> list[str]:
    """ASP-CI-12 / ASP-CI-13 — forme enveloppée, et convention ×1 / ×2 / ×3."""
    errs = []
    idx = _index_service(etapes, SVC_COMMANDE)
    if len(idx) != 1:
        errs.append(f"ASP-CI-12 : le moteur doit émettre EXACTEMENT un "
                    f"`{SVC_COMMANDE}` — trouvé {len(idx)} (ASP-INV-35).")
        return errs
    step = etapes[idx[0]]
    data = step.get("data") or {}
    if data.get("command") != COMMANDE_SEGMENTEE:
        errs.append(f"ASP-CI-12 : la commande protocolaire doit être "
                    f"`{COMMANDE_SEGMENTEE}` — trouvé "
                    f"{data.get('command')!r} (07 §2).")
        return errs
    tpl = data.get("params")
    if not isinstance(tpl, str):
        errs.append("ASP-CI-12 : `params` doit être un gabarit rendant la "
                    "charge utile enveloppée (ASP-INV-33).")
        return errs
    for passages, attendu_repeat in ((1, None), (2, 2), (3, 3)):
        rendu = charge_utile(tpl, [16, 21], passages)
        if not isinstance(rendu, list) or len(rendu) != 1 \
                or not isinstance(rendu[0], dict):
            errs.append(f"ASP-CI-12 : ×{passages} — la charge utile doit être "
                        f"une LISTE contenant UN mapping (forme enveloppée) ; "
                        f"rendu : {rendu!r}. La forme nue échoue en silence "
                        f"(ASP-INV-33).")
            continue
        utile = rendu[0]
        if utile.get("segments") != [16, 21]:
            errs.append(f"ASP-CI-12 : ×{passages} — la charge utile doit "
                        f"porter les index natifs demandés ; rendu : "
                        f"{utile!r}.")
        if attendu_repeat is None:
            if "repeat" in utile:
                errs.append(f"ASP-CI-13 : ×1 exige l'ABSENCE du champ "
                            f"`repeat` — rendu : {utile!r} (ASP-INV-18).")
        elif utile.get("repeat") != attendu_repeat:
            errs.append(f"ASP-CI-13 : ×{passages} exige `repeat: "
                        f"{attendu_repeat}` — rendu : {utile!r} (ASP-INV-18).")
        if utile.get("repeat") in (0, 1):
            errs.append(f"ASP-CI-13 : `repeat: {utile['repeat']}` transpose la "
                        f"convention DÉCALÉE de la voie zonée sur la commande "
                        f"segmentée — non conforme (ASP-INV-19).")
    return errs


def check_voies_interdites(textes_runtime) -> list[str]:
    """ASP-CI-14 / ASP-CI-15 — voie zonée, mode dérivé, démarreurs interdits.

    AMENDEMENT L2 — le périmètre s'étend aux trois fichiers du lot L2, et une
    UNIQUE exception nominative y apparaît : la primitive de démarrage est
    admise dans le SEUL fichier de conduite, UNE SEULE FOIS, et seulement si
    les quatre ancres de sa garde fermée y figurent (07 §7.1, ASP-INV-62).

    Sans cette extension, un fichier L2 échapperait entièrement au contrôle :
    la primitive circulerait sans garde, et `vacuum.start` sur session close
    déclencherait un nettoyage GLOBAL — toute la carte au lieu du périmètre
    demandé.
    """
    errs = []
    for rel in RUNTIME_FICHIERS + RUNTIME_L2_FICHIERS:
        txt = sans_commentaires_yaml(textes_runtime.get(rel, ""))
        for interdit in VOIES_INTERDITES:
            if interdit == PRIMITIVE_DEMARRAGE and rel == RUNTIME_L2_CONDUITE:
                continue
            if re.search(rf'\b{re.escape(interdit)}\b', txt):
                errs.append(f"ASP-CI-14 : {rel} emploie `{interdit}` — voie "
                            f"zonée ou démarreur interdit (07 §6, "
                            f"ASP-INV-19).")
    # L'exception, verifiee et non concedee.
    conduite = sans_commentaires_yaml(textes_runtime.get(RUNTIME_L2_CONDUITE, ""))
    appels = re.findall(
        r'^[ \t]*-?[ \t]*(?:action|service|perform_action)[ \t]*:[ \t]*'
        r'["\']?' + re.escape(PRIMITIVE_DEMARRAGE) + r'["\']?[ \t]*$',
        conduite, re.M)
    if len(appels) != 1:
        errs.append(f"ASP-CI-14 : `{RUNTIME_L2_CONDUITE}` porte {len(appels)} "
                    f"appel(s) de `{PRIMITIVE_DEMARRAGE}` — il en faut "
                    "EXACTEMENT un. C'est la seule voie de la primitive de "
                    "démarrage dans tout le domaine, et le geste de reprise "
                    "n'émet qu'une commande (ASP-INV-62, ASP-INV-89).")
    for ancre in GARDE_REPRISE_ANCRES:
        if ancre not in conduite:
            errs.append(f"ASP-CI-14 : la garde de reprise ne lit pas `{ancre}` "
                        "— la garde fermée d'ASP-INV-62 a QUATRE conditions, "
                        "et sur session close la primitive déclencherait un "
                        "nettoyage global (07 §6, §7.1).")
    return errs


def check_mode_jamais_ecrit(etapes) -> list[str]:
    """ASP-CI-15 — le mode de nettoyage se lit et se confirme, jamais ne s'écrit."""
    errs = []
    for step in etapes:
        svc = _service(step)
        if not svc:
            continue
        if NATIF_MODE in _cibles(step):
            errs.append(f"ASP-CI-15 : `{NATIF_MODE}` est la CIBLE de `{svc}` — "
                        f"écrire le mode écrase silencieusement le profil "
                        f"d'aspiration (ASP-INV-12).")
        data = step.get("data")
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, str) and NATIF_MODE in v and svc != "input_text.set_value":
                    errs.append(f"ASP-CI-15 : `{NATIF_MODE}` apparaît dans les "
                                f"données de `{svc}` (ASP-INV-12).")
    return errs


def _garde_memoire_mission(top) -> list[str]:
    """ASP-CI-16 — le moteur se TAIT sur une mission deja ouverte (15 §2).

    Le moteur ouvre son canal en ecrivant `VALIDATION_EN_COURS`
    INCONDITIONNELLEMENT. Cette valeur est de classe H. Ecrite par-dessus un
    verdict de classe O ou O-R, elle DETRUIT la seule memoire de mission
    ouverte du domaine — le verdict lui-meme (ASP-INV-87, D-08). Trois
    consequences en cascade, toutes observables : la supervision perd sa
    porte d'entree et n'ecrira plus aucune issue ; la projection de cycle
    perd sa voie d'extinction et laisse sa notification affichee sans fin ;
    les gestes de conduite sont ensuite refuses, la mission etant devenue
    invisible alors que le robot roule.

    La propriete exigee, et elle est ORDINALE : au PREMIER NIVEAU de la
    sequence, un arret sec garde par la classe du verdict precede TOUTE
    ecriture du verdict. L'ordre se prouve la, et seulement la — une garde
    logee dans une branche serait mutuellement exclusive des autres, et son
    rang n'aurait aucun sens d'execution.
    """
    errs: list[str] = []
    ouvert = CLASSE_O | {CLASSE_O_R}

    # (a) la table LUE par la garde, embarquee dans les referentiels.
    variables = {}
    for st in top:
        if isinstance(st, dict) and isinstance(st.get("variables"), dict):
            variables.update(st["variables"])
    embarquee = variables.get("verdict_ouvert")
    if set(embarquee or []) != ouvert:
        errs.append(
            f"ASP-CI-16 : le moteur doit embarquer les {len(ouvert)} valeurs "
            f"de classe O et O-R sous `verdict_ouvert` — trouve "
            f"{sorted(embarquee or [])}. C'est la table que sa garde LIT ; "
            "incomplete, elle laisse passer les appels qu'elle doit taire "
            "(15 §2).")

    # (b) la garde, au premier niveau, et ce qu'elle fait.
    rang_garde = None
    anomalies: list[str] = []
    for i, st in enumerate(top):
        if not (isinstance(st, dict) and "choose" in st):
            continue
        for opt in _ensure_list(st.get("choose"), f"sequence/{i}/choose",
                                anomalies):
            if not isinstance(opt, dict):
                continue
            cond = _conditions_option(opt)
            if ID_VERDICT not in cond or "verdict_ouvert" not in cond:
                continue
            corps = opt.get("sequence") or []
            ecrit, _ = _verdicts_du_document(corps)
            if ecrit:
                errs.append(
                    f"ASP-CI-16 : la garde de memoire de mission ECRIT "
                    f"{sorted(ecrit)}. Elle doit s'ARRETER SEC : toute valeur "
                    "ecrite ici est de classe H et detruit exactement ce que "
                    "la garde protege — y compris "
                    "`REFUS/MISSION_DEJA_OUVERTE`, dont la place reste la "
                    "mission observee sur les TEMOINS NATIFS (15 §2, D-08).")
            elif not any("stop" in x for x in corps if isinstance(x, dict)):
                errs.append("ASP-CI-16 : la garde de memoire de mission ne "
                            "s'arrete pas — sans `stop`, la sequence poursuit "
                            "vers l'ouverture du canal et ecrit malgre tout.")
            if rang_garde is None:
                rang_garde = i
    if rang_garde is None:
        errs.append(
            f"ASP-CI-16 : le moteur n'a AUCUNE garde de memoire de mission au "
            f"premier niveau. Appele pendant une mission ouverte, il ecrit "
            f"`VALIDATION_EN_COURS` — classe H — par-dessus un verdict de "
            f"classe O : la supervision perd sa porte d'entree, la "
            f"notification persistante perd sa voie d'extinction, et les "
            f"gestes de conduite sont ensuite refuses (ASP-INV-87, D-08).")
        return errs

    # (c) ORDRE : la garde precede toute ecriture du verdict.
    premieres = [i for i, st in enumerate(top)
                 if isinstance(st, dict) and _verdicts_du_document([st])[0]]
    if premieres and min(premieres) < rang_garde:
        errs.append(
            f"ASP-CI-16 : le moteur ecrit le verdict au pas {min(premieres)}, "
            f"AVANT sa garde de memoire de mission (pas {rang_garde}). Une "
            "garde posee apres l'ecriture ne garde plus rien : la memoire est "
            "deja detruite quand elle s'evalue (15 §2, D-08).")
    return errs


def check_ordre_sequence(corps_sequence) -> list[str]:
    """ASP-CI-16 / ASP-CI-17 — carte -> eau -> aspiration -> revérif -> commande.

    **Deux besoins, deux mécanismes — et la docstring dit lequel fait quoi.**

    *Unicité* : comptée sur la visite RÉCURSIVE EXHAUSTIVE (`_actions`), donc
    une écriture cachée dans un `repeat`, un `if` ou une branche `parallel`
    est vue et refusée.

    *Ordre* : établi **exclusivement sur la séquence de PREMIER NIVEAU**, où
    les pas s'exécutent réellement l'un après l'autre. Aucune branche n'est
    concaténée à une autre : deux branches d'un même `choose` sont
    **mutuellement exclusives**, et leur ordre textuel n'a aucune signification
    d'exécution. Une version antérieure comparait des index d'aplatissement —
    elle fabriquait un ordre là où il n'en existe pas.

    Corollaire opposable : les quatre actions ordonnées doivent se trouver au
    premier niveau. Une seule d'entre elles logée dans une branche rend
    l'ordre indécidable, et le contrôle le dit au lieu de l'inventer.
    """
    errs = []
    top = corps_sequence or []
    errs += _garde_memoire_mission(top)

    def _partout(pred):
        return [ch for ch, s in _actions(top) if pred(s)]

    def _au_premier_niveau(pred):
        # Le chemin nominal, garde d'abstention comprise (07 §3.2 bis) :
        # l'écriture qu'elle porte garde le rang du `choose` qui la garde,
        # et reste donc ordonnable face aux trois autres actions.
        return [i for i, s in _nominal(top) if pred(s)]

    roles = (
        ("carte", lambda s: _service(s) == SVC_EAU and NATIF_CARTE in _cibles(s)),
        ("eau", lambda s: _service(s) == SVC_EAU and NATIF_EAU in _cibles(s)),
        ("aspiration", lambda s: _service(s) == SVC_ASPIRATION),
        ("commande", lambda s: _service(s) == SVC_COMMANDE),
    )

    # (1) UNICITÉ — sur la visite exhaustive.
    comptes = {nom: _partout(pred) for nom, pred in roles}
    if any(len(v) != 1 for v in comptes.values()):
        errs.append(
            "ASP-CI-16 : la séquence exige exactement une écriture de "
            + ", ".join(f"{nom} ({len(ch)})" for nom, ch in comptes.items())
            + " — 07 §3. Occurrences : "
            + " · ".join(f"{nom}={ch}" for nom, ch in comptes.items() if ch))
        return errs

    # (2) ORDRE — sur le PREMIER NIVEAU seul.
    rangs = {nom: _au_premier_niveau(pred) for nom, pred in roles}
    hors = [nom for nom, r in rangs.items() if len(r) != 1]
    if hors:
        errs.append(
            f"ASP-CI-16 : {', '.join(hors)} — action(s) absente(s) du chemin "
            f"nominal. L'ordre ne se prouve QUE sur la séquence de premier "
            f"niveau : une action logée dans une branche est mutuellement "
            f"exclusive des autres, et son rang n'a aucun sens d'exécution "
            f"(07 §3).")
        return errs
    ordre = [rangs[nom][0] for nom, _p in roles]
    if ordre != sorted(ordre):
        errs.append(
            "ASP-CI-16 : ordre non conforme — carte, puis EAU, puis "
            "ASPIRATION, puis commande. L'inverser écraserait le profil "
            "d'aspiration (ASP-INV-34). Rangs observés : "
            + ", ".join(f"{nom}={rangs[nom][0]}" for nom, _p in roles) + ".")
    i_asp, i_cmd = rangs["aspiration"][0], rangs["commande"][0]

    # (3) Revérification tardive, elle aussi sur le chemin nominal.
    relectures = [i for i, s in enumerate(top)
                  if isinstance(s, dict) and isinstance(s.get("variables"), dict)
                  and any(k.startswith("g2_") for k in s["variables"])]
    if not relectures:
        errs.append("ASP-CI-16 : aucune relecture des gardes entre le dernier "
                    "réglage et l'émission (ASP-INV-36).")
    elif not (i_asp < relectures[0] < i_cmd):
        errs.append("ASP-CI-16 : la relecture des gardes doit se situer APRÈS "
                    "les réglages et AVANT l'émission (ASP-INV-36).")
    else:
        lues = set(top[relectures[0]]["variables"].values())
        for temoin in TEMOINS_GARDE:
            if not any(temoin in v for v in lues if isinstance(v, str)):
                errs.append(f"ASP-CI-16 : la revérification tardive omet "
                            f"`{temoin}` — elle porte sur la TOTALITÉ des "
                            f"conditions du §5 (ASP-INV-36).")
    return errs


def check_decompte_vocabulaire(textes_runtime, t09) -> list[str]:
    """ASP-CI-18 — le DÉCOMPTE annoncé dans le helper est-il vrai ?

    Les deux ensembles — valeurs de verdict et codes du catalogue — comptent
    18 éléments, et **se recoupent**. Une version antérieure du helper
    affirmait qu'ils étaient disjoints, avec une répartition 13 / 5 / 5 qui ne
    tombait juste que par compensation d'erreurs : `TRANSITION_NON_OBSERVEE`
    appartient bien au catalogue ET figure au verdict sous `ECHEC/`. Le
    décompte est donc RECALCULÉ ici et confronté au texte.
    """
    errs = []
    refus, echecs = split_catalogue(t09)
    catalogue = refus | echecs
    if not catalogue:
        return ["ASP-CI-18 : catalogue du contrat illisible — décompte du "
                "vocabulaire non vérifiable."]
    codes_verdict = {v.split("/")[-1] for v in VOCABULAIRE_VERDICT}
    presents = codes_verdict & catalogue
    absents = catalogue - codes_verdict
    cycle = codes_verdict - catalogue
    attendus = {
        r"(\d+) codes du catalogue figurent": len(presents),
        r"(\d+) codes du catalogue en sont ABSENTS": len(absents),
        r"(\d+) valeurs de CYCLE DE VIE": len(cycle),
    }
    texte = textes_runtime.get(RUNTIME_HELPERS, "")
    for motif, valeur in attendus.items():
        trouve = re.search(motif, texte)
        if not trouve:
            errs.append(f"ASP-CI-18 : le helper de verdict n'énonce pas son "
                        f"décompte — motif attendu « {motif} » (ASP-INV-70).")
        elif int(trouve.group(1)) != valeur:
            errs.append(
                f"ASP-CI-18 : décompte FAUX dans le helper — « {motif} » "
                f"annonce {trouve.group(1)}, le calcul donne {valeur}. "
                f"Codes du catalogue au verdict : {sorted(presents)} ; "
                f"absents : {sorted(absents)} ; cycle de vie : "
                f"{sorted(cycle)}.")
    if len(presents) + len(cycle) != len(VOCABULAIRE_VERDICT):
        errs.append(f"ASP-CI-18 : la décomposition ne totalise pas le "
                    f"vocabulaire — {len(presents)} + {len(cycle)} ≠ "
                    f"{len(VOCABULAIRE_VERDICT)}.")
    if sorted(cycle) != sorted(CYCLE_DE_VIE):
        errs.append(f"ASP-CI-18 : valeurs de cycle de vie calculées "
                    f"{sorted(cycle)} ≠ constante de module "
                    f"{sorted(CYCLE_DE_VIE)} (ASP-INV-70).")
    return errs


# Les cinq valeurs STRUCTURANTES du verdict, et la place que chacune doit
# occuper. `nature` : `nominal` = premier niveau ; `branche_positive` = dans
# une option de `choose` ; `branche_negative` = dans son `default`.
# `vs_emission` : position exigée par rapport à l'unique `vacuum.send_command`.
VERDICTS_STRUCTURANTS = (
    ("VALIDATION_EN_COURS", "nominal", "avant"),
    ("COMMANDE/ISSUE_NON_ETABLIE", "nominal", "avant"),
    ("EMISSION/COMMANDE_ACCEPTEE", "nominal", "apres"),
    ("LANCEE/DEMARRAGE_OBSERVE", "branche_positive", "apres"),
    ("ECHEC/TRANSITION_NON_OBSERVEE", "branche_negative", "apres"),
)


def _ancre(chemin: str) -> int:
    """Index de PREMIER NIVEAU dont dépend un chemin.

    `sequence/12/choose/0/sequence/3` est ancré en 12 : la branche s'exécute
    au douzième pas du chemin nominal. C'est cette ancre, et elle seule, qui
    permet de comparer une écriture logée dans une branche à une action du
    chemin nominal — sans jamais comparer deux branches EXCLUSIVES entre
    elles, ce qui n'aurait aucun sens.
    """
    return int(chemin.split("/")[1])


def _occurrences_verdict(top):
    """Toutes les écritures du verdict, avec chemin, nature et ancre.

    À la différence d'un dictionnaire `{valeur: index}` — qui écrase les
    occurrences antérieures et ne retient que la dernière —, cette analyse
    conserve CHAQUE occurrence. Une valeur posée deux fois, dont une
    correctement placée, ne peut donc plus se cacher derrière la bonne.
    """
    out = []
    for chemin, step in _actions(top):
        if _service(step) != "input_text.set_value":
            continue
        if ID_VERDICT not in _cibles(step):
            continue
        data = step.get("data")
        if not (isinstance(data, dict) and isinstance(data.get("value"), str)):
            continue
        segments = chemin.split("/")
        if len(segments) == 2:
            nature = "nominal"
        elif "/default/" in chemin:
            nature = "branche_negative"
        elif "/choose/" in chemin:
            nature = "branche_positive"
        else:
            nature = "imbrique"
        out.append({"valeur": data["value"].strip(), "chemin": chemin,
                    "nature": nature, "ancre": _ancre(chemin)})
    return out


def _verdicts_structurants(top) -> list[str]:
    """ASP-CI-18 — multiplicité ET position des cinq verdicts structurants.

    Chaque valeur doit apparaître **exactement une fois**, à la **nature**
    d'emplacement prescrite, et du **bon côté** de l'unique émission. La
    comparaison se fait sur l'ANCRE de premier niveau : jamais entre deux
    branches exclusives.
    """
    errs = []
    occurrences = _occurrences_verdict(top)
    emissions = [ch for ch, st in _actions(top) if _service(st) == SVC_COMMANDE]
    if len(emissions) != 1:
        return errs                     # ASP-CI-12 le dit déjà, et mieux.
    ancre_cmd = _ancre(emissions[0])

    for valeur, nature_attendue, cote in VERDICTS_STRUCTURANTS:
        vues = [o for o in occurrences if o["valeur"] == valeur]
        if len(vues) != 1:
            errs.append(
                f"ASP-CI-18 : `{valeur}` doit être écrit EXACTEMENT une fois — "
                f"trouvé {len(vues)} occurrence(s)"
                + (f" : {', '.join(o['chemin'] for o in vues)}" if vues else "")
                + ". Une valeur structurante dupliquée rend son ordonnancement "
                  "indécidable, et une valeur absente laisse une issue muette "
                  "(ASP-INV-49).")
            continue
        o = vues[0]
        if o["nature"] != nature_attendue:
            errs.append(
                f"ASP-CI-18 : {o['chemin']} — `{valeur}` est posé en "
                f"« {o['nature']} », attendu « {nature_attendue} ». "
                + {"nominal": "Cette valeur appartient au chemin nominal.",
                   "branche_positive": "Cette valeur ne se pose que dans la "
                                       "branche d'observation POSITIVE.",
                   "branche_negative": "Cette valeur ne se pose que dans la "
                                       "branche NÉGATIVE (`default`) de la "
                                       "même observation."}[nature_attendue])
        avant = o["ancre"] < ancre_cmd
        if cote == "avant" and not avant:
            errs.append(
                f"ASP-CI-18 : {o['chemin']} — `{valeur}` doit être posé AVANT "
                f"l'émission (ancre {o['ancre']} ≥ {ancre_cmd}). Après, "
                f"l'issue d'un appel qui ne revient pas ne serait plus tracée "
                f"(ASP-INV-49).")
        if cote == "apres" and avant:
            errs.append(
                f"ASP-CI-18 : {o['chemin']} — `{valeur}` est posé AVANT "
                f"l'émission (ancre {o['ancre']} < {ancre_cmd}) : il "
                f"affirmerait une acceptation, ou un démarrage, que rien n'a "
                f"encore établi (ASP-INV-37, ASP-INV-38).")

    # Les deux issues de l'observation partagent le MÊME parent : ce sont les
    # deux branches d'un seul `choose`. Les séparer les rendrait comparables à
    # tort, et permuter leurs valeurs deviendrait indétectable.
    positifs = [o for o in occurrences
                if o["valeur"] == "LANCEE/DEMARRAGE_OBSERVE"]
    negatifs = [o for o in occurrences
                if o["valeur"] == "ECHEC/TRANSITION_NON_OBSERVEE"]
    if len(positifs) == 1 and len(negatifs) == 1:
        if positifs[0]["ancre"] != negatifs[0]["ancre"]:
            errs.append(
                f"ASP-CI-18 : les deux issues de l'observation de démarrage "
                f"doivent être les DEUX BRANCHES D'UN MÊME `choose` — trouvées "
                f"aux ancres {positifs[0]['ancre']} et {negatifs[0]['ancre']} "
                f"({positifs[0]['chemin']} · {negatifs[0]['chemin']}).")
    return errs


def check_vocabulaire_verdict(corps_sequence, textes_runtime) -> list[str]:
    """ASP-CI-18 — vocabulaire fermé, ordonnancement, et EMPLACEMENT des
    écritures du verdict.

    Reçoit la séquence de PREMIER NIVEAU : l'ordonnancement se raisonne sur le
    chemin nominal, tandis que la détection descend, elle, dans toutes les
    structures imbriquées via `_actions`.
    """
    errs = []
    etapes = _aplatir(corps_sequence)
    ecrits = _ecritures_verdict(etapes)
    valeurs = {v for _, v in ecrits}
    if not valeurs:
        errs.append(f"ASP-CI-18 : le moteur n'écrit jamais `{ID_VERDICT}` — "
                    f"un refus est un livrable (ASP-INV-50).")
        return errs
    # AMENDEMENT L2 — l'atteignabilite se confronte desormais aux TROIS
    # writers, pas au moteur seul. Ici, le moteur doit ecrire EXACTEMENT son
    # ensemble : les seize valeurs des lots L2 ne lui appartiennent pas, et
    # les lui exiger ferait echouer un fichier conforme. La couverture totale
    # du vocabulaire par l'union des trois est verifiee par
    # `check_table_writers` (ASP-CI-11), qui porte la table nominative.
    hors = valeurs - VERDICT_W1
    if hors:
        errs.append(f"ASP-CI-18 : le moteur écrit {sorted(hors)}, hors de son "
                    f"ensemble de dix-huit valeurs — le vocabulaire est fermé "
                    f"ET réparti (ASP-INV-52, ASP-INV-86).")
    absentes = VERDICT_W1 - valeurs
    if absentes:
        errs.append(f"ASP-CI-18 : le moteur n'écrit jamais {sorted(absentes)} "
                    f"— l'ensemble d'un writer doit être intégralement "
                    f"atteignable (ASP-INV-65).")
    moteur = sans_commentaires_yaml(textes_runtime.get(RUNTIME_MOTEUR, ""))
    for code, pourquoi in sorted(CODES_HORS_PORTEE_L1.items()):
        if re.search(rf'\b{code}\b', moteur):
            errs.append(f"ASP-CI-18 : le moteur porte `{code}` alors que L1 ne "
                        f"peut pas l'observer ({pourquoi}) — aucun verdict ne "
                        f"doit affirmer un rejet avant qu'un rejet soit "
                        f"observable (09 §5).")
    errs += _verdicts_structurants(corps_sequence)
    # La trace d'intention accompagne le verdict non concluant, pas l'inverse.
    # Comparaison par ANCRE de premier niveau, comme pour les verdicts.
    traces = [ch for ch, s in _actions(corps_sequence)
              if _service(s) == "input_text.set_value" and ID_TRACE in _cibles(s)]
    emissions = [ch for ch, s in _actions(corps_sequence)
                 if _service(s) == SVC_COMMANDE]
    if len(traces) != 1:
        errs.append(f"ASP-CI-18 : `{ID_TRACE}` doit être écrit exactement une "
                    f"fois par exécution — trouvé {len(traces)}"
                    + (f" : {', '.join(traces)}" if traces else "") + " (08 §5).")
    elif len(emissions) == 1 and not _ancre(traces[0]) < _ancre(emissions[0]):
        errs.append(f"ASP-CI-18 : {traces[0]} — la trace d'intention est posée "
                    f"AVANT l'appel, avec le verdict non concluant ; sinon "
                    f"trace et verdict décriraient deux missions différentes "
                    f"(08 §5).")
    # `continue_on_error` n'est PAS interdit en bloc : il est réservé aux trois
    # écritures préparatoires, et ASP-CI-27 en ferme l'allowlist. Ici, seule
    # l'ÉMISSION est protégée — l'absorber ferait passer une issue non établie
    # pour une acceptation, contre 07 §4 et ASP-INV-38.
    #
    # Correction d'une affirmation FAUSSE portée par la version précédente de
    # ce contrôle : `continue_on_error` ne rend pas l'exception illisible.
    # `_handle_exception` (helpers/script.py, 2026.8.3) appelle
    # `_log_exception` AVANT de tester `continue_on_error`. Le motif de
    # l'interdiction n'est pas la lisibilité — c'est l'absence de
    # postcondition suffisante.
    for chemin, step in _actions(corps_sequence):
        if not (isinstance(step, dict) and step.get("continue_on_error")):
            continue
        if _service(step) == SVC_COMMANDE:
            errs.append(
                f"ASP-CI-18 : {chemin} — `continue_on_error` sur "
                f"`{SVC_COMMANDE}` : l'émission n'a AUCUNE postcondition "
                f"suffisante (acceptation ≠ démarrage, ASP-INV-38). Absorber "
                f"son exception présenterait une issue non établie comme une "
                f"acceptation (07 §4).")

    # Le verdict est le LIVRABLE : il ne s'écrit que sur le chemin nominal ou
    # dans une branche de refus de premier niveau. Une écriture logée dans un
    # `repeat`, un `if` ou un `parallel` produirait un verdict hors séquence,
    # invisible à l'analyse d'ordonnancement — et donc un verdict que rien ne
    # garantit vrai (ASP-INV-49, ASP-INV-50).
    # Les conteneurs sont normalisés par `_ensure_list` : `choose` accepte un
    # choix unique en mapping, et chaque `sequence` un mapping nu.
    _rebut: list[str] = []
    legitimes = set()
    for i, step in enumerate(_ensure_list(corps_sequence, "sequence", _rebut)):
        legitimes.add(f"sequence/{i}")
        if isinstance(step, dict) and "choose" in step:
            for j, opt in enumerate(_ensure_list(step["choose"], "", _rebut)):
                if not isinstance(opt, dict):
                    continue
                for k, _p in enumerate(_ensure_list(opt.get("sequence"), "",
                                                    _rebut)):
                    legitimes.add(f"sequence/{i}/choose/{j}/sequence/{k}")
            for k, _p in enumerate(_ensure_list(step.get("default"), "",
                                                _rebut)):
                legitimes.add(f"sequence/{i}/default/{k}")
    for chemin, step in _actions(corps_sequence):
        if _service(step) != "input_text.set_value":
            continue
        if ID_VERDICT not in _cibles(step):
            continue
        if chemin not in legitimes:
            errs.append(
                f"ASP-CI-18 : {chemin} — écriture de `{ID_VERDICT}` hors du "
                f"chemin nominal et hors branche de refus. Le verdict ne "
                f"s'écrit qu'au premier niveau de la séquence ou dans une "
                f"branche `choose` de premier niveau (ASP-INV-49).")
    return errs


# Valeurs qu'un geste a le droit d'ecrire — son engagement et ses issues.
# Figees ici : un `CLOTURE/APRES_ARRET_CONFIRME` ecrit sous la branche
# « pause » resterait dans l'ensemble de W2 et passerait toutes les gardes
# globales. C'est cette table qui l'attrape.
VALEURS_DU_GESTE = {
    "pause": frozenset({"CONDUITE/PAUSE_ENGAGEE", "CONDUITE/PAUSE_CONFIRMEE",
                        "CONDUITE/PAUSE_NON_CONFIRMEE"}),
    "reprise": frozenset({"CONDUITE/REPRISE_ENGAGEE",
                          "CONDUITE/REPRISE_CONFIRMEE",
                          "CONDUITE/REPRISE_NON_CONFIRMEE"}),
    "arret": frozenset({"CONDUITE/ARRET_ENGAGE",
                        "CLOTURE/APRES_ARRET_CONFIRME",
                        "CLOTURE/APRES_ARRET_NON_CONFIRME"}),
    "retour_base": frozenset({"CONDUITE/RETOUR_ENGAGE",
                              "CLOTURE/APRES_RETOUR_NON_CONFIRME"}),
}
# Tout appel d'appareil, quel qu'il soit — pour compter les emissions d'une
# branche sans supposer laquelle elle porte.
SERVICES_APPAREIL = frozenset(SERVICE_DU_GESTE.values()) | {SVC_COMMANDE}


def _conditions_option(opt) -> str:
    """Concatene les conditions d'UNE option de `choose`, sous leurs formes.

    `_texte_conditions` prend le `choose` entier et fond toutes les branches :
    utilisable pour chercher une comparaison quelque part, inutilisable pour
    dire QUELLE branche porte QUELLE garde. C'est cette distinction que les
    controles L2 exigent.
    """
    morceaux: list[str] = []
    _rebut: list[str] = []
    for cond in _ensure_list((opt or {}).get("conditions"), "", _rebut):
        if isinstance(cond, str):
            morceaux.append(cond)
        elif isinstance(cond, dict):
            for cle in ("value_template", "state", "id", "condition",
                        "entity_id"):
                val = cond.get(cle)
                if isinstance(val, str):
                    morceaux.append(val)
                elif isinstance(val, list):
                    morceaux += [x for x in val if isinstance(x, str)]
    return "\n".join(morceaux)


def _lineaire(seq):
    """Etapes d'une sequence, a plat et EN ORDRE DE DOCUMENT.

    Descend dans `choose` et `default`, et NULLE PART ailleurs. Un `repeat`,
    un `if` ou un `parallel` n'est pas traverse : une ecriture qui s'y
    logerait resterait invisible a l'analyse d'ordonnancement, et c'est
    precisement ce que le controle refuse (ASP-INV-49).
    """
    out = []
    if isinstance(seq, dict):
        seq = [seq]
    for st in seq or []:
        if not isinstance(st, dict):
            continue
        if "choose" in st:
            for opt in st.get("choose") or []:
                if isinstance(opt, dict):
                    out += _lineaire(opt.get("sequence"))
            out += _lineaire(st.get("default"))
        else:
            out.append(st)
    return out


def check_sequence_conduite(textes_runtime) -> list[str]:
    """ASP-CI-18 — la sequence opposable d'un geste, geste par geste.

    Quatre proprietes, dans cet ordre, et pour chacun des quatre gestes :
      1. l'ENGAGEMENT est ecrit AVANT la commande (ASP-INV-88) ;
      2. il y a EXACTEMENT UNE emission, et c'est celle du geste
         (ASP-INV-89) ;
      3. la relecture est UNIQUE et bornee a la constante du domaine ;
      4. le verdict ne s'ecrit qu'avec les valeurs de CE geste ;
      5. l'emission ABSORBE son exception (`continue_on_error`) — sans quoi
         une levee laisse le verdict fige sur l'engagement, sans expiration
         et sans issue : un engagement PERMANENT (ASP-INV-49) ;
      6. chaque conclusion RELIT le verdict et n'ecrit que s'il porte ENCORE
         l'engagement de CE geste — sans quoi l'EXPIRATION de W2 ecrase une
         conclusion qu'un autre ecrivain a fondee sur une OBSERVATION
         (15 §4, regle 5).

    C'est le controle qui empeche les quatre regressions concretes du lot :
    commander le robot a tort, dupliquer une commande, ecrire un verdict
    impossible, et briser l'unicite d'un writer.
    """
    errs: list[str] = []
    txt = textes_runtime.get(RUNTIME_L2_CONDUITE)
    if not txt:
        return [f"ASP-CI-18 : `{RUNTIME_L2_CONDUITE}` est absent."]
    try:
        doc = yaml.safe_load(txt)
    except yaml.YAMLError as exc:
        return [f"ASP-CI-18 : `{RUNTIME_L2_CONDUITE}` illisible ({exc})."]
    corps = (doc or {}).get(ID_CONDUITE) or {}
    seq = corps.get("sequence") or []

    # Aucune repetition, nulle part : la relance est un geste operateur.
    if REPETITION.search(sans_commentaires_yaml(txt)):
        errs.append(f"ASP-CI-18 : `{RUNTIME_L2_CONDUITE}` porte une "
                    "répétition — aucune réémission, aucun retry, aucune "
                    "seconde attente (ASP-INV-39, ASP-INV-89).")

    branches: dict[str, list] = {}
    for st in seq:
        if not isinstance(st, dict) or "choose" not in st:
            continue
        for opt in st.get("choose") or []:
            if not isinstance(opt, dict):
                continue
            cond = _conditions_option(opt)
            for geste in GESTES_L2:
                if f"geste == '{geste}'" in cond:
                    branches.setdefault(geste, []).append(opt.get("sequence"))

    for geste in GESTES_L2:
        trouvees = branches.get(geste) or []
        if len(trouvees) != 1:
            errs.append(f"ASP-CI-18 : le geste `{geste}` est porté par "
                        f"{len(trouvees)} branche(s) — il en faut exactement "
                        "une. Deux branches pour un geste, c'est deux chemins "
                        "de commande (ASP-INV-31).")
            continue
        etapes = _lineaire(trouvees[0])

        emissions = [(i, _svc_de(st)) for i, st in enumerate(etapes)
                     if _svc_de(st) in SERVICES_APPAREIL]
        if len(emissions) != 1:
            errs.append(f"ASP-CI-18 : le geste `{geste}` émet "
                        f"{len(emissions)} commande(s) — un geste émet "
                        "EXACTEMENT une commande (ASP-INV-89).")
            continue
        i_svc, svc = emissions[0]
        if svc != SERVICE_DU_GESTE[geste]:
            errs.append(f"ASP-CI-18 : le geste `{geste}` émet `{svc}` — "
                        f"attendu `{SERVICE_DU_GESTE[geste]}`. Un geste qui "
                        "commande autre chose que ce qu'il annonce commande "
                        "le robot à tort.")
        cibles = _cibles(etapes[i_svc])
        if cibles != [NATIF_VACUUM]:
            errs.append(f"ASP-CI-18 : le geste `{geste}` vise {cibles} — "
                        f"attendu `{NATIF_VACUUM}`, littéralement.")
        if etapes[i_svc].get("continue_on_error") is not True:
            errs.append(
                f"ASP-CI-18 : l'émission du geste `{geste}` n'absorbe pas son "
                "exception — sans `continue_on_error`, une levée du service "
                "AVORTE la séquence APRÈS l'écriture de l'engagement : le "
                "verdict reste sur une valeur de classe O, sans expiration et "
                "sans issue. La supervision s'abstient tant qu'elle voit un "
                "engagement, la notification persistante reste affichée, et "
                "les gestes suivants sont refusés. Absorber n'est PAS "
                "réémettre (ASP-INV-49, ASP-INV-89).")

        ecrits = [(i, v) for i, v in _ecritures_verdict(etapes)]
        valeurs = {v for _, v in ecrits}
        interdites = valeurs - VALEURS_DU_GESTE[geste]
        if interdites:
            errs.append(f"ASP-CI-18 : le geste `{geste}` écrit "
                        f"{sorted(interdites)} — hors des valeurs de ce "
                        f"geste {sorted(VALEURS_DU_GESTE[geste])} "
                        "(contrat 15 §3.1).")

        engagement = ENGAGEMENT_DU_GESTE[geste]
        poses = [i for i, v in ecrits if v == engagement]
        if len(poses) != 1:
            errs.append(f"ASP-CI-18 : le geste `{geste}` pose `{engagement}` "
                        f"{len(poses)} fois — exactement une (ASP-INV-88).")
        elif poses[0] > i_svc:
            errs.append(f"ASP-CI-18 : le geste `{geste}` pose `{engagement}` "
                        "APRÈS sa commande. L'engagement rend la fenêtre de "
                        "relecture visible dans le verdict : posé après, il "
                        "n'exclut plus la supervision et la course de "
                        "l'arbitrage A-11 revient (15 §4).")
        avant = [v for i, v in ecrits if i < min(poses or [i_svc])]
        if avant:
            errs.append(f"ASP-CI-18 : le geste `{geste}` écrit {avant} avant "
                        "son engagement — un refus de geste n'écrit RIEN, et "
                        "rien ne précède l'engagement (ASP-INV-91).")

        attentes = [i for i, st in enumerate(etapes) if "wait_template" in st]
        if len(attentes) != 1:
            errs.append(f"ASP-CI-18 : le geste `{geste}` porte "
                        f"{len(attentes)} relecture(s) — une seule, bornée "
                        "(ASP-INV-90).")
        elif attentes[0] < i_svc:
            errs.append(f"ASP-CI-18 : le geste `{geste}` relit AVANT "
                        "d'émettre — la relecture qualifie l'issue d'une "
                        "commande, elle ne la précède pas.")
        else:
            conclusions = [v for i, v in ecrits if i > attentes[0]]
            if not conclusions:
                errs.append(f"ASP-CI-18 : le geste `{geste}` ne conclut RIEN "
                            "après sa relecture — toute mission produit une "
                            "issue explicite (ASP-INV-49).")
            errs += _garde_de_course(geste, trouvees[0], set(conclusions))
    return errs


def _garde_de_course(geste, sequence, conclusions) -> list[str]:
    """ASP-CI-18 — la relecture du verdict avant chaque conclusion (15 §4).

    Ce qu'elle empeche, concretement : W2 engage un retour ; W3 observe
    l'amarrage et ecrit `CLOTURE/APRES_RETOUR_CONFIRME` ; la fenetre de W2
    expire ENSUITE et ecrase cette observation par un defaut d'entree dans la
    chaine. Le meme scenario existe sur les trois autres gestes avec une
    erreur qualifiee par W3, qui ne s'abstient PAS pendant un engagement.

    La propriete exigee : CHAQUE option qui conclut porte, dans sa condition,
    la relecture du helper ET l'egalite a l'engagement de CE geste. Et il ne
    subsiste AUCUN `default:` sur le `choose` de conclusion — un `default`
    s'executerait precisement quand la garde ne passe pas, c'est-a-dire quand
    le verdict a deja bouge.
    """
    errs: list[str] = []
    if not conclusions:
        return errs
    engagement = ENGAGEMENT_DU_GESTE[geste]
    for st in _mappings(sequence):
        if "choose" not in st:
            continue
        options = [o for o in _ensure_list(st.get("choose"), "choose", [])
                   if isinstance(o, dict)]
        porte = [o for o in options
                 if _verdicts_du_document(o.get("sequence"))[0] & conclusions]
        if not porte:
            continue
        for opt in porte:
            cond = _conditions_option(opt)
            if ID_VERDICT not in cond or f"== '{engagement}'" not in cond:
                ecrit = sorted(_verdicts_du_document(opt.get("sequence"))[0]
                               & conclusions)
                errs.append(
                    f"ASP-CI-18 : le geste `{geste}` conclut {ecrit} sans "
                    f"relire le verdict — la condition doit exiger que "
                    f"`{ID_VERDICT}` vaille ENCORE `{engagement}`. Sans "
                    "cette relecture, l'EXPIRATION de W2 écrase une "
                    "conclusion qu'un autre écrivain a fondée sur une "
                    "OBSERVATION : sur un retour, une arrivée constatée "
                    "redevient un défaut d'entrée dans la chaîne (15 §4, "
                    "règle 5).")
        if st.get("default"):
            errs.append(
                f"ASP-CI-18 : le `choose` de conclusion du geste `{geste}` "
                "porte un `default:` — il s'exécuterait EXACTEMENT quand la "
                "garde de course ne passe pas, c'est-à-dire quand le verdict "
                "a déjà bougé. L'absence de `default` EST la troisième issue "
                "du geste, et elle n'écrit rien (15 §4, règle 5).")
    return errs


def check_supervision(textes_runtime) -> list[str]:
    """ASP-CI-18 — la supervision : porte d'entree, exclusion, reconciliation.

    Cinq proprietes, chacune fondee sur une regle ecrite :
      1. AUCUNE ecriture de verdict hors d'une mission ouverte — c'est ce qui
         rend impossible l'adoption d'une mission externe (ASP-INV-87) ;
      2. la conclusion d'INTERRUPTION est exclue pendant un engagement — la
         garde rendue par A-11, regle 2 (ASP-INV-92) ;
      3. la cloture opaque n'est ecrite QUE sur la reconciliation de
         redemarrage (15 §6) ;
      4. l'interruption se conclut POSITIVEMENT, sur le seul etat d'arret
         atteste, et JAMAIS par negation d'une classe (15 §5) ;
      5. l'AMARRAGE se prouve POSITIVEMENT, sur les deux temoins en
         disjonction, et `docking` — etat de MOUVEMENT — n'en est pas un.

    Les deux dernieres sont ce qui empeche la regression qui rendait ce
    fichier dangereux : une regle negative concluait sur tout etat de classe
    N, donc sur des etats parfaitement sains, et `docking` faisait passer un
    trajet en cours pour une arrivee.
    """
    errs: list[str] = []
    txt = textes_runtime.get(RUNTIME_L2_SUPERVISION)
    if not txt:
        return [f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` est absent — les "
                f"{len(VERDICT_W3)} valeurs de supervision n'auraient aucun "
                "écrivain."]
    try:
        doc = yaml.safe_load(txt)
    except yaml.YAMLError as exc:
        return [f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` illisible ({exc})."]
    autos = [a for a in (doc if isinstance(doc, list) else [doc])
             if isinstance(a, dict)]
    if len(autos) != 1 or autos[0].get("id") != AID_SUPERVISION:
        return [f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` doit déclarer "
                f"EXACTEMENT l'automation `{AID_SUPERVISION}` — trouvé "
                f"{[a.get('id') for a in autos]} (ASP-INV-58)."]
    auto = autos[0]

    if REPETITION.search(sans_commentaires_yaml(txt)):
        errs.append(f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` porte une "
                    "répétition — une supervision observe, elle ne boucle "
                    "pas.")

    for st in _mappings(auto):
        if "wait_template" in st or "delay" in st:
            errs.append(f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` porte une "
                        "attente — l'amarrage est ÉVÉNEMENTIEL, jamais borné "
                        "par une durée (A-15).")

    # ── (4) et (5) : les DEUX règles positives fermées, dans les
    #    référentiels embarqués. Elles sont contrôlées SUR LES VARIABLES,
    #    donc une fois, et non branche par branche : c'est là qu'elles
    #    sont écrites, et c'est de là que les conditions les tirent.
    variables = {}
    for st in (auto.get("action") or auto.get("actions") or []):
        if isinstance(st, dict) and isinstance(st.get("variables"), dict):
            variables.update(st["variables"])

    if variables.get("arret_atteste") != ETAT_ARRET_ATTESTE:
        errs.append(
            f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` doit embarquer "
            f"`arret_atteste: {ETAT_ARRET_ATTESTE}` — trouvé "
            f"{variables.get('arret_atteste')!r}. La cessation d'activité ne "
            "s'établit que sur le SEUL état d'arrêt attesté du domaine "
            "(15 §5).")

    amarre = variables.get("amarre")
    if not isinstance(amarre, str):
        errs.append(f"ASP-CI-18 : `{RUNTIME_L2_SUPERVISION}` n'embarque "
                    "aucune preuve `amarre` — l'arrivée au dock serait "
                    "déduite d'une liste d'états, et `docking` y rentrerait "
                    "de nouveau (15 §5).")
    else:
        for temoin in TEMOINS_AMARRAGE:
            if temoin not in amarre:
                errs.append(
                    f"ASP-CI-18 : la preuve d'amarrage n'invoque pas "
                    f"`{temoin}` — les DEUX témoins sont exigés, EN "
                    "DISJONCTION : l'un des deux peut être manqué, et exiger "
                    "une transition intermédiaire rendrait l'arrivée "
                    "inobservable (15 §5).")
        if " or " not in amarre:
            errs.append("ASP-CI-18 : la preuve d'amarrage ne met pas ses deux "
                        "témoins en DISJONCTION — les conjoindre exigerait un "
                        "échantillon que rien ne garantit (15 §5).")
        if ETAT_MOUVEMENT_DOCK in amarre:
            errs.append(
                f"ASP-CI-18 : la preuve d'amarrage invoque "
                f"`{ETAT_MOUVEMENT_DOCK}` — le contrat le classe en état de "
                "MOUVEMENT, au même titre que `returning_home` (07 §5.0), et "
                "il n'a jamais été observé sur cet appareil. Le tenir pour "
                "une arrivée conclut un trajet EN COURS.")

    for st in (auto.get("action") or auto.get("actions") or []):
        if not isinstance(st, dict) or "choose" not in st:
            continue
        for opt in st.get("choose") or []:
            if not isinstance(opt, dict):
                continue
            cond = _conditions_option(opt)
            ecrites, _ = _verdicts_du_document(opt.get("sequence"))
            if not ecrites:
                continue
            if "verdict_ouvert" not in cond and CLASSE_O_R not in cond:
                errs.append(
                    f"ASP-CI-18 : une branche de supervision écrit "
                    f"{sorted(ecrites)} sans exiger un verdict de classe O — "
                    "la porte d'entrée est le verdict, et elle seule. Sans "
                    "elle, une activité du robot qu'Arsenal n'a jamais "
                    "ouverte serait ADOPTÉE (ASP-INV-87, D-06, D-R4).")
            if "ECHEC/MISSION_INTERROMPUE" in ecrites and "engagements" not in cond:
                errs.append(
                    "ASP-CI-18 : la branche d'interruption ne s'exclut pas "
                    "pendant un engagement — pendant la fenêtre de relecture "
                    "d'un geste, elle produirait un échec FAUX, aussitôt "
                    "écrasé par la clôture du geste (ASP-INV-92, A-11).")
            if "ECHEC/MISSION_INTERROMPUE" in ecrites:
                if "arret_atteste" not in cond:
                    errs.append(
                        "ASP-CI-18 : la branche d'interruption ne s'appuie "
                        "pas sur `arret_atteste` — la cessation doit être "
                        "établie POSITIVEMENT, sur le seul état d'arrêt "
                        "attesté (15 §5).")
                if "not in classe" in cond or "!=" in cond:
                    errs.append(
                        "ASP-CI-18 : la branche d'interruption conclut par "
                        "NÉGATION d'une classe. Cette règle conclut sur TOUT "
                        "état de classe N — un vidage de dock, un séchage, un "
                        "déplacement non nommé — et produit alors un verdict "
                        "terminal FAUX, une projection éteinte, une "
                        "supervision désarmée et une notification mobile "
                        "mensongère (15 §5).")
            if ecrites & VERDICTS_ARRIVEE and "amarre" not in cond:
                errs.append(
                    f"ASP-CI-18 : une branche écrit {sorted(ecrites & VERDICTS_ARRIVEE)} "
                    "sans s'appuyer sur la preuve `amarre` — l'arrivée au "
                    "dock se PROUVE sur ses deux témoins, elle ne se déduit "
                    "pas d'une liste d'états (15 §5).")
            if "CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE" in ecrites \
                    and "readiness" not in cond:
                errs.append(
                    "ASP-CI-18 : la clôture opaque est écrite hors de la "
                    "réconciliation de redémarrage — elle constate qu'une "
                    "chaîne est devenue inobservable, ce que seul un "
                    "redémarrage établit (15 §6, ASP-INV-94).")
    return errs


def check_motif_total(t09: str, t02: str, motif_txt: str) -> list[str]:
    """ASP-CI-19 — les 18 codes traduits, sans mécanique interne."""
    errs = []
    refus, echecs = split_catalogue(t09)
    catalogue = refus | echecs
    if len(catalogue) != 18:
        errs.append(f"ASP-CI-19 : le catalogue du contrat compte "
                    f"{len(catalogue)} codes au lieu de 18 — le contrôle de "
                    f"totalité perd son ancre (09 §2, §3).")
    manquants = sorted(c for c in catalogue
                       if not re.search(rf"'{c}'\s*:", motif_txt))
    if manquants:
        errs.append(f"ASP-CI-19 : `{ID_MOTIF}` ne traduit pas {manquants} — le "
                    f"catalogue doit rester TOTAL, y compris pour les codes "
                    f"qu'aucun lot n'écrit encore (ASP-INV-50).")
    for valeur in CYCLE_DE_VIE:
        if not re.search(rf"'{valeur}'\s*:", motif_txt):
            errs.append(f"ASP-CI-19 : `{ID_MOTIF}` ne traduit pas la valeur de "
                        f"cycle de vie `{valeur}` (ASP-INV-49).")
    # Aucun index nu, aucun libellé d'appareil, aucun nom d'entité.
    motifs = re.findall(r'^\s*"([^"\n]{20,})",?\s*$', motif_txt, re.M)
    noms_roborock = {n for _, _, n, _ in TECH_SEGMENT.findall(bloc_technique(t02))}
    noms_roborock |= {c for _, c, _ in TECH_CARTE.findall(bloc_technique(t02))}
    for m in motifs:
        if len(m) > MAX_ETAT_CAPTEUR:
            errs.append(f"ASP-CI-19 : motif de {len(m)} caractères — l'état "
                        f"d'un capteur est borné à {MAX_ETAT_CAPTEUR} : "
                        f"« {m[:60]}… ».")
        if re.search(r'\b\d+_\d+\b', m):
            errs.append(f"ASP-CI-19 : un motif expose un index de segment nu — "
                        f"« {m[:60]}… » (ASP-INV-6, ASP-INV-53).")
        if re.search(r'\b(?:sensor|binary_sensor|select|vacuum|input_text)\.',
                     m) or COMMANDE_SEGMENTEE in m:
            errs.append(f"ASP-CI-19 : un motif expose de la mécanique interne "
                        f"— « {m[:60]}… » (09 §4).")
        for nom in noms_roborock:
            if nom.strip() and re.search(rf'\b{re.escape(nom.strip())}\b', m):
                errs.append(f"ASP-CI-19 : un motif restitue le libellé "
                            f"d'appareil « {nom.strip()} » — jamais de libellé "
                            f"brut (ASP-INV-7, ASP-INV-53).")
    return errs


def check_constantes_temporelles(textes_runtime) -> list[str]:
    """ASP-CI-20 — 30 s x3, 60 s x1, et aucune autre temporisation."""
    errs = []
    moteur = sans_commentaires_yaml(textes_runtime.get(RUNTIME_MOTEUR, ""))
    timeouts = re.findall(r'^[ \t]*-?[ \t]*timeout[ \t]*:[ \t]*"?([0-9:]+)"?[ \t]*$',
                          moteur, re.M)
    n30 = timeouts.count(FENETRE_CONFIRMATION_YAML)
    n60 = timeouts.count(FENETRE_TRANSITION_YAML)
    if n30 != NB_CONFIRMATIONS:
        errs.append(f"ASP-CI-20 : {NB_CONFIRMATIONS} fenêtres de confirmation "
                    f"de {FENETRE_CONFIRMATION_S} s sont exigées — carte, eau, "
                    f"aspiration ; trouvé {n30} (ASP-INV-69).")
    if n60 != 1:
        errs.append(f"ASP-CI-20 : une seule fenêtre d'observation de "
                    f"{FENETRE_TRANSITION_S} s est exigée — la transition de "
                    f"démarrage ; trouvé {n60} (ASP-INV-69).")
    autres = sorted(set(timeouts) - {FENETRE_CONFIRMATION_YAML,
                                     FENETRE_TRANSITION_YAML})
    if autres:
        errs.append(f"ASP-CI-20 : durée(s) concurrente(s) dans le moteur : "
                    f"{autres} — deux constantes, et deux seulement "
                    f"(ASP-INV-69).")
    for rel in RUNTIME_FICHIERS + RUNTIME_L2_FICHIERS:
        txt = sans_commentaires_yaml(textes_runtime.get(rel, ""))
        for cle in ("delay", "wait_for_trigger"):
            # Le tiret de liste fait partie de la ligne : `- delay:` est la
            # forme la plus courante, et l'ignorer viderait la garde.
            if re.search(rf'^[ \t]*-?[ \t]*{cle}[ \t]*:', txt, re.M):
                errs.append(f"ASP-CI-20 : {rel} porte `{cle}:` — aucune "
                            f"temporisation hors des deux constantes "
                            f"(ASP-INV-69).")
        if "input_number." in txt:
            errs.append(f"ASP-CI-20 : {rel} référence un `input_number` — le "
                        f"domaine n'expose AUCUN réglage temporel "
                        f"(12 §3, ASP-INV-69).")

    # ── AMENDEMENT L2 : extension du perimetre aux fichiers du lot L2 ──────
    #
    # Sans elle, une fenetre de relecture L2 echapperait ENTIEREMENT au
    # controle — c'est le trou que l'arbitrage A-15 identifie, et il est
    # ferme ici, pas ailleurs. Les quatre fenetres sont MUTUALISEES a la
    # constante de confirmation : le domaine reste a deux durees, et
    # `ASP-CI-10` n'a donc pas a etre amende.
    conduite = sans_commentaires_yaml(
        textes_runtime.get(RUNTIME_L2_CONDUITE, ""))
    t_l2 = re.findall(
        r'^[ \t]*-?[ \t]*timeout[ \t]*:[ \t]*"?([0-9:]+)"?[ \t]*$',
        conduite, re.M)
    n30 = t_l2.count(FENETRE_CONFIRMATION_YAML)
    if n30 != NB_FENETRES_L2:
        errs.append(f"ASP-CI-20 : {NB_FENETRES_L2} fenêtres de relecture de "
                    f"{FENETRE_CONFIRMATION_S} s sont exigées dans le script "
                    f"de conduite — pause, reprise, arrêt, engagement du "
                    f"retour ; trouvé {n30} (ASP-INV-69, A-15).")
    autres_l2 = sorted(set(t_l2) - {FENETRE_CONFIRMATION_YAML})
    if autres_l2:
        errs.append(f"ASP-CI-20 : durée(s) concurrente(s) dans le script de "
                    f"conduite : {autres_l2} — les quatre fenêtres sont "
                    f"MUTUALISÉES à une seule valeur, et c'est ce qui évite "
                    f"d'amender ASP-CI-10 (A-15).")
    for rel in (RUNTIME_L2_SUPERVISION, RUNTIME_L2_PROJECTION):
        txt = sans_commentaires_yaml(textes_runtime.get(rel, ""))
        veilles = re.findall(r'^[ \t]*-?[ \t]*timeout[ \t]*:', txt, re.M)
        if veilles:
            errs.append(f"ASP-CI-20 : {rel} porte {len(veilles)} `timeout:` — "
                        "une supervision et une projection sont "
                        "ÉVÉNEMENTIELLES : aucune ne borne un fait physique "
                        "par une durée (A-15).")
    return errs


def check_concordance_runtime(corps, textes_runtime, helpers_yaml, t02, t03,
                              audit) -> list[str]:
    """ASP-CI-21 — identifiants, référentiel embarqué, profils, capacité."""
    errs = []
    # a) identifiants attribués, aux fichiers attribués
    attendus = ((RUNTIME_HELPERS, ID_VERDICT.split(".", 1)[1]),
                (RUNTIME_HELPERS, ID_TRACE.split(".", 1)[1]),
                (RUNTIME_ETAT, ID_ETAT_CANON),
                (RUNTIME_MOTIF, ID_MOTIF),
                (RUNTIME_GARDE, ID_GARDE))
    for rel, ident in attendus:
        if ident not in textes_runtime.get(rel, ""):
            errs.append(f"ASP-CI-21 : identifiant `{ident}` absent de {rel} — "
                        f"attribution opérateur non respectée (ASP-INV-58).")
    if set(helpers_yaml) != {ID_VERDICT.split(".", 1)[1],
                             ID_TRACE.split(".", 1)[1]}:
        errs.append(f"ASP-CI-21 : le domaine expose EXACTEMENT deux helpers "
                    f"textuels — trouvé {sorted(helpers_yaml)} (12 §2.3).")

    # b) référentiel embarqué == table du contrat (métier ET technique)
    variables = next((s["variables"] for s in (corps.get("sequence") or [])
                      if isinstance(s, dict) and "variables" in s
                      and "referentiel" in s["variables"]), None)
    if variables is None:
        errs.append("ASP-CI-21 : le moteur ne porte aucun référentiel de "
                    "segments — la validation n'a plus de vérité de "
                    "désignation (ASP-INV-6).")
        return errs
    ref = variables["referentiel"]
    tech = bloc_technique(t02)
    cartes_contrat = {idx: opt for idx, opt, statut in TECH_CARTE.findall(tech)
                      if idx and statut == "commandable"}
    segments_contrat = {seg: (int(nat), nom)
                        for seg, nat, nom, statut in TECH_SEGMENT.findall(tech)
                        if statut == "commandable"}
    if set(ref) != set(cartes_contrat):
        errs.append(f"ASP-CI-21 : cartes embarquées {sorted(ref)} ≠ cartes "
                    f"commandables du contrat {sorted(cartes_contrat)} "
                    f"(02 §2.1).")
    for idx, opt in sorted(cartes_contrat.items()):
        if idx in ref and ref[idx].get("option") != opt:
            errs.append(f"ASP-CI-21 : option de la carte `{idx}` — le moteur "
                        f"porte {ref[idx].get('option')!r}, le contrat "
                        f"{opt!r}. La comparaison est LITTÉRALE, espace finale "
                        f"comprise (ASP-INV-66, ASP-INV-67).")
    embarques = {seg: (info["index"], carte)
                 for carte, bloc in ref.items()
                 for seg, info in (bloc.get("segments") or {}).items()}
    if set(embarques) != set(segments_contrat):
        manque = sorted(set(segments_contrat) - set(embarques))
        trop = sorted(set(embarques) - set(segments_contrat))
        errs.append(f"ASP-CI-21 : segments embarqués non conformes au "
                    f"référentiel V1 — manquants {manque}, en trop {trop} "
                    f"(02 §2, QO-1).")
    for seg, (nat, _nom) in sorted(segments_contrat.items()):
        if seg in embarques and embarques[seg][0] != nat:
            errs.append(f"ASP-CI-21 : index natif de `{seg}` — moteur "
                        f"{embarques[seg][0]}, contrat {nat} (02 §2.1).")
    for seg in SEGMENTS_NON_COMMANDABLES:
        if seg in embarques:
            errs.append(f"ASP-CI-21 : `{seg}` est hors référentiel V1 et ne "
                        f"peut pas devenir commandable (QO-1).")
    # noms Roborock exacts, pour la seule confirmation de carte
    for carte, bloc in sorted(ref.items()):
        attendus_noms = sorted(nom for seg, (_i, nom) in segments_contrat.items()
                               if seg.split("_")[0] == carte)
        if sorted(bloc.get("noms") or []) != attendus_noms:
            errs.append(f"ASP-CI-21 : noms Roborock de la carte `{carte}` — "
                        f"moteur {sorted(bloc.get('noms') or [])}, contrat "
                        f"{attendus_noms} (06 §3.1, ASP-INV-63).")

    # c) profils : les six du contrat, valeurs natives bornées
    profils = variables.get("profils") or {}
    contrat_profils = parse_profils(t03)
    if len(profils) != NB_PROFILS or len(contrat_profils) != NB_PROFILS:
        errs.append(f"ASP-CI-21 : {NB_PROFILS} profils exactement — moteur "
                    f"{len(profils)}, contrat {len(contrat_profils)} "
                    f"(ASP-INV-10).")
    couples_contrat = {(a, e) for _l, a, e in contrat_profils}
    couples_moteur = {(p["aspiration"], p["eau"]) for p in profils.values()}
    if couples_moteur != couples_contrat:
        errs.append(f"ASP-CI-21 : couples (aspiration, eau) du moteur "
                    f"{sorted(couples_moteur)} ≠ contrat "
                    f"{sorted(couples_contrat)} (03 §1).")
    for cle, p in sorted(profils.items()):
        if p.get("aspiration") == FAN_SPEED_EXCLUE:
            errs.append(f"ASP-CI-21 : le profil `{cle}` emploie "
                        f"`{FAN_SPEED_EXCLUE}`, exclu du domaine "
                        f"(ASP-INV-11).")
        attendu = "vacuum" if p.get("eau") == "off" else "vac_and_mop"
        if p.get("mode") != attendu:
            errs.append(f"ASP-CI-21 : mode dérivé du profil `{cle}` — "
                        f"eau `{p.get('eau')}` implique `{attendu}`, trouvé "
                        f"`{p.get('mode')}` (03 §3).")

    # d) partition embarquée == partition du module
    for classe, cle in (("R", "classe_r"), ("A", "classe_a")):
        if set(variables.get(cle) or []) != set(PARTITION_ATTENDUE[classe]):
            errs.append(f"ASP-CI-21 : classe {classe} embarquée "
                        f"{sorted(variables.get(cle) or [])} ≠ partition "
                        f"contractuelle {sorted(PARTITION_ATTENDUE[classe])} "
                        f"(07 §5.0).")
    if set(variables.get("classe_e_indispo") or []) != \
            set(PARTITION_ATTENDUE["E"]) - {"error"}:
        errs.append("ASP-CI-21 : les valeurs d'indisponibilité embarquées ne "
                    "recouvrent pas la classe E hors `error` (07 §5.0).")
    if set(variables.get("indispo") or []) != {"unknown", "unavailable"}:
        errs.append("ASP-CI-21 : le régime d'indisponibilité doit être "
                    "exactement {`unknown`, `unavailable`} — y ajouter `none` "
                    "confondrait la valeur NOMINALE du témoin d'erreur avec "
                    "une absence (ASP-INV-45, ASP-INV-61).")

    # e) entités natives attestées par l'audit
    attestes = tous_les_jetons(audit)
    for natif in (NATIF_CARTE, NATIF_EAU, NATIF_MODE, NATIF_VACUUM, NATIF_PIECE,
                  NATIF_ETAT, NATIF_ERR_VAC, NATIF_ERR_DOCK, NATIF_SESSION,
                  NATIF_MOP):
        if natif not in attestes:
            errs.append(f"ASP-CI-21 : `{natif}` n'est attesté par aucun relevé "
                        f"de l'audit du domaine (ASP-INV-58).")

    # f) capacité : la sérialisation MAXIMALE d'une intention V1 tient
    pire = 0
    for carte, bloc in ref.items():
        paires = ",".join(sorted(bloc.get("segments") or {}))
        for cle in profils:
            for n in ("1", "2", "3"):
                pire = max(pire, len(
                    f"carte={carte}|segments={paires}|profil={cle}|passages={n}"))
    capacite = (helpers_yaml.get(ID_TRACE.split(".", 1)[1]) or {}).get("max")
    if not isinstance(capacite, int):
        errs.append(f"ASP-CI-21 : `{ID_TRACE}` doit déclarer une capacité "
                    f"`max` explicite (04_input_texts §Structure).")
    elif pire > capacite:
        errs.append(f"ASP-CI-21 : la sérialisation maximale d'une intention V1 "
                    f"occupe {pire} caractères pour une capacité de "
                    f"{capacite} — la trace serait tronquée ou refusée "
                    f"(08 §5).")
    verdict_max = (helpers_yaml.get(ID_VERDICT.split(".", 1)[1]) or {}).get("max")
    pire_verdict = max(len(v) for v in VOCABULAIRE_VERDICT)
    if isinstance(verdict_max, int) and pire_verdict > verdict_max:
        errs.append(f"ASP-CI-21 : le verdict le plus long occupe "
                    f"{pire_verdict} caractères pour une capacité de "
                    f"{verdict_max}.")
    return errs


# ─────────────────────────────────────────────────────────────
# Exécution réelle
# ─────────────────────────────────────────────────────────────

def load_domain() -> dict[str, str]:
    if not DOMAIN.is_dir():
        return {}
    return {p.name: p.read_text(encoding="utf-8", errors="ignore")
            for p in sorted(DOMAIN.glob("*.md"))}


def load_lovelace() -> dict[str, str]:
    out: dict[str, str] = {}
    for d in LOVELACE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.yaml")):
            if p.is_file():
                out[p.relative_to(ROOT).as_posix()] = p.read_text(
                    encoding="utf-8", errors="ignore")
    return out


def load_runtime() -> dict[str, str]:
    """Les cinq fichiers du lot L1 et les trois du lot L2, tels quels.

    Commentaires compris : plusieurs gardes du domaine balaient le fichier
    ENTIER, et un identifiant cite en commentaire est deja une proximite trop
    grande avec ce qu'il designe.
    """
    out: dict[str, str] = {}
    for rel in RUNTIME_FICHIERS + RUNTIME_L2_FICHIERS:
        p = ROOT / rel
        if p.is_file():
            out[rel] = p.read_text(encoding="utf-8", errors="ignore")
    return out


def load_yaml_fonctionnel() -> dict[str, str]:
    """Tout le YAML FONCTIONNEL du depot — `.yaml` ET `.yml`.

    F2 : le balayage d'ASP-CI-11 n'itere que les repertoires `^\\d{2}_` et ne
    connait que `.yaml`. Il laissait donc hors perimetre les fichiers de
    configuration de racine, `blueprints/`, `esphome/`, et toute extension
    `.yml`. ASP-CI-31 garde la seule primitive irreversible du domaine : son
    perimetre est defini ici, explicitement, et les exclusions sont justifiees
    en tete de module.
    """
    out: dict[str, str] = {}

    def prendre(p: Path) -> None:
        if not p.is_file():
            return
        rel = p.relative_to(ROOT).as_posix()
        if any(rel.startswith(x) for x in EXCLUS_YAML):
            return
        out[rel] = p.read_text(encoding="utf-8", errors="ignore")

    for nom in RACINE_HA:
        prendre(ROOT / nom)
    for base in sorted(ROOT.iterdir()):
        if not base.is_dir():
            continue
        if not (re.match(r"^\d{2}_", base.name)
                or base.name in DOSSIERS_FONCTIONNELS):
            continue
        for motif in ("*.yaml", "*.yml"):
            for p in sorted(base.rglob(motif)):
                prendre(p)
    return out


def load_runtime_m1() -> str:
    """Le fichier UNIQUE du lot M1 — la projection d'entretien."""
    p = ROOT / RUNTIME_M1
    return (p.read_text(encoding="utf-8", errors="ignore")
            if p.is_file() else "")


def load_yaml_depot() -> dict[str, str]:
    """Tout le YAML de configuration Home Assistant du dépôt.

    Sert l'ANTI-CONCURRENCE d'ASP-CI-11 : prouver qu'aucun autre fichier
    n'écrit les helpers du domaine ni ne commande l'appareil suppose de les
    avoir tous lus, pas seulement ceux du lot.
    """
    out: dict[str, str] = {}
    for base in sorted(ROOT.iterdir()):
        if not base.is_dir() or not re.match(r"^\d{2}_", base.name):
            continue
        for p in sorted(base.rglob("*.yaml")):
            if p.is_file():
                out[p.relative_to(ROOT).as_posix()] = p.read_text(
                    encoding="utf-8", errors="ignore")
    return out


def dashboards_declares() -> dict:
    """Les cles de `18_lovelace/dashboards.yaml`, chargees.

    ASP-CI-42 en a besoin pour prouver qu'un `navigation_path` cible une cle
    REELLE : un bandeau qui mene a une cle absente produit un ecran
    inatteignable, et aucune garde du domaine ne le verrait.
    """
    p = ROOT / "18_lovelace" / "dashboards.yaml"
    if not p.is_file():
        return {}
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}


def run() -> int:
    bruts = load_domain()
    if not bruts:
        sys.stderr.write(f"erreur : domaine introuvable : {DOMAIN}\n")
        return 2
    # Blocs de code neutralisés : un exemple documentaire n'est pas une
    # déclaration normative (ASP-CI-1, ASP-CI-3, ASP-CI-6).
    # R3 — la neutralisation vaut pour LES DIX contrôles, pas seulement pour
    # ASP-CI-1/3/6 : un exemple documentaire n'est normatif nulle part. L'audit
    # est neutralisé pour la même raison — un faux tableau de segments placé dans
    # un bloc n'y attesterait rien.
    textes = sans_clotures(bruts)
    brut_audit = AUDIT.read_text(encoding="utf-8", errors="ignore") if AUDIT.is_file() else ""
    audit = strip_fences(brut_audit)
    brut_releve = (RELEVE_ENTRETIEN.read_text(encoding="utf-8", errors="ignore")
                   if RELEVE_ENTRETIEN.is_file() else "")
    releve = strip_fences(brut_releve)
    # ASP-CI-6 atteste contre les DEUX sources factuelles, nommees et fermees :
    # l'audit de faisabilite (mission) et le releve d'entretien (Maintenance).
    # L'audit est anterieur au perimetre Maintenance : sans le releve, le
    # chapitre 14 nommerait huit entites que nulle attestation ne couvre.
    attestation = audit + "\n" + releve
    lovelace = load_lovelace()
    # F2 : perimetre YAML FONCTIONNEL explicite, propre a ASP-CI-31.
    fonctionnel = load_yaml_fonctionnel()
    # M1 : la projection d'entretien. Le fichier est aussi balaye par
    # ASP-CI-11 (anti-concurrence) et par ASP-CI-31 (primitive) : les
    # trois controles M1 s'ajoutent a ces gardes, ils ne s'y substituent
    # pas.
    m1 = load_runtime_m1()
    # N1 : les automations de projection. Le DOSSIER est lu, pas un fichier
    # nomme : c'est ce qui rend detectable un troisieme writer glisse a cote.
    n1 = load_runtime_n1()
    u0 = load_runtime_u0()
    depot = load_yaml_depot()

    controles = (
        ("ASP-CI-1  invariants", check_invariants(textes)),
        ("ASP-CI-2  référentiel des segments",
         check_referentiel(textes.get("02_referentiel_cartes_et_pieces.md", ""),
                           textes.get("10_raccourcis.md", ""), audit)),
        ("ASP-CI-3  catalogue des codes", check_codes(textes)),
        ("ASP-CI-4  partition des états",
         check_partition(textes.get("07_moteur_de_mission.md", ""),
                         textes.get("08_etats_et_observation.md", ""))),
        ("ASP-CI-5  table des profils",
         check_profils(textes.get("03_profils_metier.md", ""))),
        ("ASP-CI-6  identifiants", check_identifiants(textes, attestation)),
        ("ASP-CI-7  Lovelace", check_lovelace(lovelace)),
        ("ASP-CI-8  référentiel technique",
         check_referentiel_technique(
             textes.get("02_referentiel_cartes_et_pieces.md", ""),
             textes.get("06_integrite_mono_carte.md", ""), audit)),
        ("ASP-CI-9  états canoniques",
         check_etats_canoniques(textes.get("08_etats_et_observation.md", ""),
                                textes.get("11_frontiere_ui.md", ""),
                                textes.get("12_identifiants_a_fournir.md", ""))),
        ("ASP-CI-10 fenêtres temporelles", check_fenetres(textes)),
    )

    # ── Runtime L1 — obligations de CONDUITE, désormais confrontables ──
    runtime = load_runtime()
    manquants = [r for r in RUNTIME_FICHIERS if r not in runtime]
    if manquants:
        sys.stderr.write(
            "erreur : runtime L1 introuvable : " + ", ".join(manquants) + "\n")
        return 2
    try:
        moteur_yaml = yaml.safe_load(runtime[RUNTIME_MOTEUR]) or {}
        helpers_yaml = yaml.safe_load(runtime[RUNTIME_HELPERS]) or {}
    except yaml.YAMLError as exc:
        sys.stderr.write(f"erreur : runtime L1 illisible : {exc}\n")
        return 2
    corps = (moteur_yaml.get(ID_MOTEUR) or {}) if isinstance(moteur_yaml, dict) else {}
    etapes = _aplatir(corps.get("sequence"))
    depot = load_yaml_depot()

    controles += (
        ("ASP-CI-11 écrivains du verdict (table, disjonction, appareil)",
         check_ecrivain_unique(moteur_yaml, runtime, depot)),
        ("ASP-CI-12 charge utile enveloppée · ASP-CI-13 passages",
         check_charge_utile(etapes)),
        ("ASP-CI-14 voies interdites · primitive de démarrage L2",
         check_voies_interdites(runtime)),
        ("ASP-CI-15 mode dérivé jamais écrit", check_mode_jamais_ecrit(etapes)),
        ("ASP-CI-16 ordre · ASP-CI-17 commande unique",
         check_ordre_sequence(corps.get("sequence") or [])),
        ("ASP-CI-18 vocabulaire de verdict · séquences L2",
         check_vocabulaire_verdict(corps.get("sequence") or [], runtime)
         + check_decompte_vocabulaire(runtime,
                                      textes.get(FICHIER_CATALOGUE, ""))
         + check_sequence_conduite(runtime)
         + check_supervision(runtime)),
        ("ASP-CI-19 motif lisible total",
         check_motif_total(textes.get(FICHIER_CATALOGUE, ""),
                           textes.get("02_referentiel_cartes_et_pieces.md", ""),
                           runtime[RUNTIME_MOTIF])),
        ("ASP-CI-20 constantes temporelles du moteur et des fichiers L2",
         check_constantes_temporelles(runtime)),
        ("ASP-CI-21 concordance runtime ↔ contrat",
         check_concordance_runtime(corps, runtime, helpers_yaml,
                                   textes.get("02_referentiel_cartes_et_pieces.md", ""),
                                   textes.get("03_profils_metier.md", ""), audit)),
        ("ASP-CI-22 rendus du moteur (troncature, retypage, type)",
         check_rendus_moteur(corps, etapes,
                             textes.get("02_referentiel_cartes_et_pieces.md", ""))),
        ("ASP-CI-23 état canonique rendu sur les 44 valeurs",
         check_etat_canonique_rendu(runtime[RUNTIME_ETAT])),
        ("ASP-CI-24 garde de lancement rendue", check_garde_rendue(
            runtime[RUNTIME_GARDE])),
        ("ASP-CI-25 branches de refus tardives",
         check_branches_tardives(etapes)),
        ("ASP-CI-26 chemins d'exception couverts",
         check_chemins_silencieux(corps.get("sequence") or [])),
        ("ASP-CI-27 écritures préparatoires (allowlist, fraîcheur, ordre)",
         check_ecritures_preparatoires(corps.get("sequence") or [], corps)),
        ("ASP-CI-28 référentiel de la couche d'intention (A-13)",
         check_referentiel_intention(
             textes.get("02_referentiel_cartes_et_pieces.md", ""),
             textes.get("10_raccourcis.md", ""), corps, u0)),
        ("ASP-CI-29 périmètre et entités d'entretien",
         check_perimetre_entretien(textes.get(FICHIER_ENTRETIEN, ""), releve)),
        ("ASP-CI-30 échéance d'entretien et honnêteté",
         check_echeance_entretien(textes.get(FICHIER_ENTRETIEN, ""))),
        ("ASP-CI-31 primitive irréversible (allowlist fermée)",
         check_primitive_irreversible(textes.get(FICHIER_ENTRETIEN, ""),
                                      fonctionnel, lovelace)),
        ("ASP-CI-32 séquence de remise à zéro",
         check_remise_a_zero(textes.get(FICHIER_ENTRETIEN, ""))),
        ("ASP-CI-33 notifications d'entretien et routage",
         check_notifications_entretien(textes.get(FICHIER_ENTRETIEN, ""),
                                       textes.get(FICHIER_ETATS, ""))),
        ("ASP-CI-34 projection d'entretien (périmètre, seuil, autorité)",
         check_projection_entretien(m1)),
        ("ASP-CI-35 projection rendue sur les trois situations",
         check_projection_rendue(m1)),
        ("ASP-CI-36 interdits de la projection", check_interdits_projection(m1)),
        ("ASP-CI-37 writers, identifiants et cycle de vie N1",
         check_writers_n1(n1, depot)),
        ("ASP-CI-38 projection persistante rendue sur les huit scénarios",
         check_projection_n1_rendue(n1, m1)),
        ("ASP-CI-39 interdits du lot N1", check_interdits_n1(n1)),
        # ── Lot M2 — la declaration d'entretien ────────────────────────
        ("ASP-CI-40 déclaration d'entretien (forme, champ fermé, branches)",
         check_declaration_entretien(depot)),
        ("ASP-CI-41 séquence de déclaration rendue (capture, transition, issues)",
         check_sequence_entretien(depot)),
        ("ASP-CI-42 écran d'entretien (appel exclusif du script backend)",
         check_ui_entretien(lovelace, dashboards_declares())),
        # ── Lot 3 de C45 — propagation des arbitrages Q1 et Q2 ─────────
        ("ASP-CI-43 égalité exacte des représentations de classe",
         check_representations_de_classe(runtime, depot)),
        ("ASP-CI-44 régime transitoire du code historique",
         check_ancien_code_transitoire(runtime, depot, textes)),
        ("ASP-CI-45 autorité et offre des gestes de conduite",
         check_offre_gestes(runtime, lovelace)),
    )

    erreurs: list[str] = []
    for label, errs in controles:
        print(f"  {'✗' if errs else '✔'} {label}")
        erreurs.extend(errs)

    attestes_audit = tous_les_jetons(attestation)
    print(f"\n  périmètre : {len(textes)} fichiers de contrat · "
          f"{len(lovelace)} fichiers Lovelace balayés · "
          f"{len(RUNTIME_FICHIERS)} fichiers runtime L1 · "
          f"{len(RUNTIME_L2_FICHIERS)} fichiers runtime L2 "
          f"(conduite, supervision, projection de mission) · "
          f"{len(depot)} fichiers YAML balayés par ASP-CI-11 · "
          f"{len(fonctionnel)} fichiers YAML fonctionnels balayés par ASP-CI-31 · "
          f"{len(attestes_audit)} identifiants attestés (audit + relevé) · "
          f"{1 if m1 else 0} fichier runtime M1 (projection d'entretien) · "
          f"{len(n1)} automation(s) du domaine balayées par ASP-CI-37/39 · "
          f"{len(u0)} fichier(s) de la couche d'intention balayés par ASP-CI-28")
    if erreurs:
        print("\nAspirateur — écarts contractuels détectés :")
        for e in erreurs:
            print(f"- {e}")
        return 1
    print("\nOK - domaine Aspirateur : intégrité normative, conduite "
          "runtime, acte contractuel Maintenance, projection "
          "d'entretien, projections persistantes, conduite et supervision "
          "de mission, couche d'intention vérifiées — "
          f"{len(controles)} lignes affichées pour 45 contrôles logiques, "
          "0 écart.")
    print("     décompte : ASP-CI-12/13 et ASP-CI-16/17 partagent chacun une "
          "ligne ; ASP-CI-28 est LIVRÉ par le lot U0 ; ASP-CI-43/44/45 sont "
          "LIVRÉS par le lot 3 de C45.")
    return 0



# ═════════════════════════════════════════════════════════════
# MAINTENANCE — ASP-CI-29 … ASP-CI-33
# ═════════════════════════════════════════════════════════════


def texte_plat(s: str) -> str:
    """Aplatit un texte Markdown pour une recherche de PHRASE normative.

    Un contrat se relit et se re-enveloppe : une garde qui casserait au premier
    retour a la ligne serait fragile. Les marqueurs de citation et les suites
    d'espaces sont donc reduits a une espace simple.

    ⚠️ F1 : l'aplatissement sert aux PHRASES COMPLETES, jamais aux mots-cles.
    Chercher un mot isole dans le texte aplati laisse passer toute mutation
    dont le mot survit ailleurs dans le chapitre — c'est exactement le faux
    vert que l'audit a demontre. Les structures — tableaux, colonnes, ordre —
    se verifient sur les LIGNES, par les aides ci-dessous.
    """
    return re.sub(r"\s+", " ", re.sub(r"\n>\s*", " ", s))


def cellules(ligne: str) -> list[str]:
    """Cellules d'une ligne de tableau Markdown, marqueur de citation retire."""
    nu = re.sub(r"^\s*>\s?", "", ligne).strip()
    if not nu.startswith("|"):
        return []
    return [c.strip() for c in nu.strip("|").split("|")]


def lignes_tableau(txt: str, *entetes: str) -> list[list[str]]:
    """Lignes de DONNEES du premier tableau dont l'en-tete porte `entetes`.

    Ancre STRUCTURELLE : on localise l'en-tete par ses libelles de colonnes,
    on saute le separateur, puis on rend les lignes tant qu'elles sont des
    lignes de tableau. Supprimer une ligne la fait disparaitre ICI — ce qu'un
    `in` sur le texte aplati ne voyait pas.
    """
    lignes = txt.splitlines()
    for k, ligne in enumerate(lignes):
        cols = cellules(ligne)
        if not cols or not all(any(e in c for c in cols) for e in entetes):
            continue
        if k + 1 >= len(lignes) or not set(
                cellules(lignes[k + 1]) and "".join(cellules(lignes[k + 1]))) <= set("-: "):
            continue
        out = []
        for suite in lignes[k + 2:]:
            cols2 = cellules(suite)
            if not cols2:
                break
            out.append(cols2)
        return out
    return []


def sans_accent_bas(s: str) -> str:
    return s.lower().replace("*", "").replace("`", "").strip()


# ═════════════════════════════════════════════════════════════
# MAINTENANCE — ASP-CI-29 … ASP-CI-33
# ═════════════════════════════════════════════════════════════


def _entites_hors_liste(txt: str, source: str, prefixe: str) -> list[str]:
    """F3 — filet ferme sur les deux familles d'entites du domaine."""
    errs = []
    for motif, permis, quoi in ((FAMILLE_CAPTEUR, CAPTEURS_ENTRETIEN, "capteur"),
                                (FAMILLE_BOUTON, BOUTONS_ENTRETIEN, "bouton")):
        for jeton in sorted(set(motif.findall(txt))):
            if jeton in permis or jeton in HORS_MAINTENANCE:
                continue
            errs.append(f"{prefixe} : {source} cite le {quoi} `{jeton}`, hors "
                        "de la liste fermée des quatre postes — une "
                        "falsification coordonnée du contrat et du relevé ne "
                        "déplace pas la vérité (ASP-INV-73).")
    return errs


def check_perimetre_entretien(t14: str, releve: str) -> list[str]:
    """ASP-CI-29 — quatre postes, huit entites, plafonds en heures.

    F3 : le filet est FERME dans les deux sens. Une entite manquante est
    refusee ; une entite SUPPLEMENTAIRE de l'une des deux familles l'est aussi,
    dans le chapitre comme dans le releve.
    """
    errs: list[str] = []
    if not t14:
        return ["ASP-CI-29 : chapitre 14 introuvable — le périmètre "
                "Maintenance n'a aucune vérité de désignation."]
    if not releve:
        return ["ASP-CI-29 : relevé d'attestation des entités d'entretien "
                "introuvable — aucune entité ne peut être attestée."]
    plat = texte_plat(t14)
    for poste, (capteur, bouton, plafond) in sorted(POSTES_ENTRETIEN.items()):
        for jeton, quoi in ((capteur, "capteur"), (bouton, "bouton")):
            if jeton not in t14:
                errs.append(f"ASP-CI-29 : le {quoi} du poste « {poste} » est "
                            f"ABSENT du chapitre 14 — `{jeton}`.")
            if jeton not in releve:
                errs.append(f"ASP-CI-29 : `{jeton}` n'est pas attesté par le "
                            "relevé — un contrat ne nomme pas une entité que "
                            "nul relevé n'a vue.")
        if f"{plafond} h" not in plat:
            errs.append(f"ASP-CI-29 : le plafond du poste « {poste} » doit "
                        f"s'écrire en HEURES — `{plafond} h` absent du "
                        "chapitre 14 (en secondes, ASP-CI-10 y lirait une "
                        "durée concurrente).")
    # F3 — filet ferme, confronte SEPAREMENT au contrat puis au releve.
    errs += _entites_hors_liste(t14, "le chapitre 14", "ASP-CI-29")
    errs += _entites_hors_liste(releve, "le relevé d'attestation", "ASP-CI-29")
    # Le tableau du perimetre porte EXACTEMENT quatre lignes.
    table = lignes_tableau(t14, "Poste", "Capteur", "Bouton")
    if len(table) != len(POSTES_ENTRETIEN):
        errs.append(f"ASP-CI-29 : le tableau du périmètre porte {len(table)} "
                    f"ligne(s) — il en faut exactement {len(POSTES_ENTRETIEN)} "
                    "(ASP-INV-73).")
    if "quatre postes" not in plat.lower():
        errs.append("ASP-CI-29 : le chapitre 14 n'énonce pas la clôture du "
                    "périmètre à quatre postes.")
    return errs


def check_echeance_entretien(t14: str) -> list[str]:
    """ASP-CI-30 — seuil unique, et TABLEAU des trois situations.

    F1 : la garde est ancree sur les LIGNES du tableau et sur leurs COLONNES.
    Remplacer « non evaluable » par « non du » dans la ligne de la mesure
    indisponible echoue ici, meme si les deux libelles subsistent ailleurs.
    """
    errs: list[str] = []
    if not t14:
        return ["ASP-CI-30 : chapitre 14 introuvable."]
    plat = texte_plat(t14)
    seuils = {int(m) for m in re.findall(
        r"(?:inférieur ou égal à|≤)\s*\*{0,2}(\d{1,3})\s*%", plat)}
    if not seuils:
        errs.append("ASP-CI-30 : aucun seuil d'échéance lisible dans le "
                    "chapitre 14 — l'échéance n'est pas opposable.")
    elif seuils != {SEUIL_ENTRETIEN_PCT}:
        errs.append(f"ASP-CI-30 : seuil(s) d'échéance {sorted(seuils)} % — le "
                    f"domaine n'admet que {SEUIL_ENTRETIEN_PCT} %, identique "
                    "pour les quatre postes (ASP-INV-75).")
    if "même seuil s'applique aux quatre postes" not in plat.lower():
        errs.append("ASP-CI-30 : la phrase normative « le même seuil "
                    "s'applique aux quatre postes » est absente.")

    # ── Ancre STRUCTURELLE : le tableau des situations ────────────────────
    table = lignes_tableau(t14, "Situation", "Condition")
    if len(table) != 3:
        errs.append(f"ASP-CI-30 : le tableau des situations porte "
                    f"{len(table)} ligne(s) — trois situations sont exigées, "
                    "jamais deux (ASP-INV-76).")
    else:
        libelles = [sans_accent_bas(l[0]) for l in table]
        attendus = ["dû", "non dû", "non évaluable"]
        if libelles != attendus:
            errs.append(f"ASP-CI-30 : situations {libelles} — attendu "
                        f"exactement {attendus}, dans cet ordre (ASP-INV-76).")
        # La ligne de la mesure INDISPONIBLE doit porter « non évaluable ».
        for lib, cond in ((sans_accent_bas(l[0]), sans_accent_bas(l[1]))
                          for l in table):
            if "indisponible" in cond or "inconnue" in cond:
                if lib != "non évaluable":
                    errs.append(
                        f"ASP-CI-30 : la mesure indisponible est classée "
                        f"« {lib} » — elle doit produire « non évaluable », "
                        "jamais « dû » ni « non dû » (ASP-INV-76).")
        if not any("indisponible" in sans_accent_bas(l[1]) or
                   "inconnue" in sans_accent_bas(l[1]) for l in table):
            errs.append("ASP-CI-30 : aucune ligne du tableau ne traite la "
                        "mesure indisponible (ASP-INV-76).")

    if "aucune anticipation prédictive" not in plat.lower():
        errs.append("ASP-CI-30 : la clause « aucune anticipation prédictive » "
                    "est absente.")
    if not ("`unknown`" in t14 and "`unavailable`" in t14):
        errs.append("ASP-CI-30 : le chapitre 14 ne nomme pas les deux régimes "
                    "d'indisponibilité — ils ne peuvent pas être exclus sans "
                    "être nommés (ASP-INV-74).")
    if "ni la dernière valeur connue" not in plat:
        errs.append("ASP-CI-30 : le chapitre 14 n'exclut pas la dernière "
                    "valeur connue comme substitut d'une mesure absente.")
    return errs


def check_primitive_irreversible(t14: str, fonctionnel: dict[str, str],
                                 lovelace: dict[str, str]) -> list[str]:
    """ASP-CI-31 — allowlist FERMEE, verrou transitoire, balayage etendu.

    F1 : les interdits sont cherches dans les LIGNES du tableau d'interdits,
    pas dans le texte aplati — supprimer une ligne echoue ici.
    F2 : le balayage porte sur le perimetre YAML fonctionnel explicite.
    F4/F8 : une allowlist non vide leve une erreur AVANT toute analyse.
    """
    errs: list[str] = []

    # ── F4/F8 : verrou transitoire, evalue en PREMIER ─────────────────────
    if ALLOWLIST_PRESSION and not VISITEUR_YAML_RECURSIF:
        errs.append(
            "ASP-CI-31 : VERROU M0 — l'allowlist de pression est non vide "
            f"({sorted(ALLOWLIST_PRESSION)}) alors que le visiteur YAML "
            "récursif complet n'est pas implémenté. Le desserrer maintenant "
            "exposerait la seule primitive irréversible du domaine derrière "
            "un parseur qui ne couvre ni le flow mapping, ni "
            "`tap_action: call-service`, ni le scalaire replié, ni les alias "
            "YAML, ni le ciblage par `device_id`, ni l'entité templatisée. "
            "Le lot M2 doit livrer ce parseur AVANT toute autorisation.")
        return errs

    if not t14:
        return ["ASP-CI-31 : chapitre 14 introuvable."]
    plat = texte_plat(t14)
    if "n'est appelable que par **un seul objet**" not in plat:
        errs.append("ASP-CI-31 : la phrase normative d'exclusivité — « n'est "
                    "appelable que par **un seul objet** » — est absente ou "
                    "affaiblie (ASP-INV-81).")
    for clause in ("allowlist", "nominative", "fermée"):
        if clause not in plat.lower():
            errs.append(f"ASP-CI-31 : le chapitre 14 n'énonce pas d'allowlist "
                        f"« {clause} » sur la primitive irréversible.")

    # ── Ancre STRUCTURELLE : le tableau des interdits ─────────────────────
    interdits = lignes_tableau(t14, "Interdit", "Portée")
    corpus = " ".join(sans_accent_bas(l[0]) for l in interdits)
    for motif, quoi in (("lovelace", "l'appel depuis un fichier Lovelace"),
                        ("automation", "l'appel depuis une automation"),
                        ("repeat", "la répétition (`repeat`, retry, boucle)"),
                        ("device_id", "l'appel générique par `device_id`"),
                        ("plusieurs", "la pression de plusieurs boutons")):
        if motif not in corpus:
            errs.append(f"ASP-CI-31 : le tableau des interdits ne porte aucune "
                        f"ligne interdisant {quoi} (ASP-INV-81).")
    if len(interdits) < 5:
        errs.append(f"ASP-CI-31 : le tableau des interdits porte "
                    f"{len(interdits)} ligne(s) — au moins cinq sont exigées.")

    # ── F2 : balayage du perimetre fonctionnel explicite ──────────────────
    # Le balayage est desormais STRUCTUREL (lot M2) : `pressions_entretien`
    # charge le document et le visite recursivement, la ou M0 lisait le texte
    # a la regex. Les six formes adverses sont rattrapees, et l'etat du
    # visiteur derive de cet essai (voir `_visiteur_est_complet`).
    for source, ensemble in (("configuration fonctionnelle", fonctionnel),
                             ("Lovelace", lovelace)):
        for rel, txt in sorted(ensemble.items()):
            boutons = pressions_entretien(txt)
            if not boutons:
                continue
            if rel not in ALLOWLIST_PRESSION:
                errs.append(f"ASP-CI-31 : {rel} ({source}) mentionne "
                            f"{', '.join('`' + b + '`' for b in sorted(boutons))} "
                            "— hors allowlist nominative (ASP-INV-81).")

    # ── L'allowlist ne nomme QUE des fichiers qui existent ────────────────
    # Une allowlist qui autorise un fichier absent est une autorisation
    # dormante : elle passerait tous les controles, et couvrirait le jour ou
    # ce fichier apparaitrait.
    for rel in sorted(ALLOWLIST_PRESSION):
        if not (ROOT / rel).is_file():
            errs.append(f"ASP-CI-31 : l'allowlist nominative autorise `{rel}`, "
                        "qui n'existe pas. Une autorisation sans fichier est "
                        "une autorisation dormante (ASP-INV-81).")
    return errs


def check_remise_a_zero(t14: str) -> list[str]:
    """ASP-CI-32 — sequence ORDONNEE, fenetre, terminal.

    F1 : les quatre etapes sont verifiees dans le TABLEAU et DANS L'ORDRE.
    Supprimer la ligne de relecture echoue ici, meme si le mot « relecture »
    subsiste dans une phrase voisine.
    """
    errs: list[str] = []
    if not t14:
        return ["ASP-CI-32 : chapitre 14 introuvable."]
    plat = texte_plat(t14)

    # ── Ancre STRUCTURELLE : la sequence, dans son ordre normatif ─────────
    seq = lignes_tableau(t14, "Étape", "Obligation")
    etapes = [sans_accent_bas(l[1]) for l in seq] if seq else []
    attendues = ["déclaration opérateur", "émission", "relecture", "issue"]
    if etapes != attendues:
        errs.append(f"ASP-CI-32 : séquence {etapes} — les quatre étapes "
                    f"{attendues} sont exigées, dans cet ordre (ASP-INV-77). "
                    "L'ordre est normatif : on n'observe pas avant d'émettre.")
    else:
        relecture = sans_accent_bas(seq[2][2])
        if "postcondition" not in relecture:
            errs.append("ASP-CI-32 : l'étape de relecture ne nomme pas la "
                        "postcondition observée (ASP-INV-79).")
        if not re.search(r"\d+\s*s\b", relecture):
            errs.append("ASP-CI-32 : l'étape de relecture ne porte aucune "
                        "fenêtre — une confirmation non bornée n'est pas une "
                        "confirmation.")
        emission = sans_accent_bas(seq[1][2])
        if "une seule pression" not in emission:
            errs.append("ASP-CI-32 : l'étape d'émission n'exige pas une seule "
                        "pression (ASP-INV-78).")

    phrases = (
        ("aucun retry", "l'interdiction de retry"),
        ("remise à zéro non confirmée", "l'issue terminale nommée"),
        ("le poste **reste dû**", "le maintien du poste comme dû"),
        ("ne conclut à aucune panne matérielle", "le refus de conclure à la panne"),
        ("nouveau geste manuel", "la reprise par geste manuel"),
        ("n'atteste **rien** de son **effet**", "la distinction pression / effet"),
    )
    for motif, quoi in phrases:
        if motif.lower() not in plat.lower():
            errs.append(f"ASP-CI-32 : le chapitre 14 n'énonce pas {quoi} "
                        f"— « {motif} » absent.")
    fen = {int(m) for m in re.findall(r"(\d{1,3})\s*s\b", plat)}
    fen |= {int(m) for m in re.findall(r"(\d{1,3})\s*secondes", plat)}
    hors = sorted(fen - {FENETRE_CONFIRMATION_S, FENETRE_TRANSITION_S})
    if hors:
        errs.append(f"ASP-CI-32 : durée(s) {hors} s hors des constantes "
                    f"admises {sorted((FENETRE_CONFIRMATION_S, FENETRE_TRANSITION_S))} "
                    "— le domaine n'en compte que deux (ASP-INV-69).")
    return errs


def check_notifications_entretien(t14: str, t08: str) -> list[str]:
    """ASP-CI-33 — routage A-8, cloisonnement, amendement MINIMAL du 08.

    F1 : les trois exclusions du 08 §6 sont verifiees comme PUCES de liste,
    ancrees en debut de ligne — supprimer une puce echoue ici.
    """
    errs: list[str] = []
    if not t14:
        return ["ASP-CI-33 : chapitre 14 introuvable."]
    plat = texte_plat(t14)
    if "pendant une mission arsenal" not in plat.lower():
        errs.append("ASP-CI-33 : le chapitre 14 ne contractualise pas le "
                    "routage PENDANT une mission (A-8).")
    if "aucune notification ajoutée" not in plat.lower():
        errs.append("ASP-CI-33 : le chapitre 14 n'énonce pas qu'AUCUNE "
                    "notification n'est ajoutée hors mission (ASP-INV-84).")
    for reste in ("état natif", "refus de lancement"):
        if reste not in plat:
            errs.append(f"ASP-CI-33 : le chapitre 14 ne nomme pas « {reste} » "
                        "parmi les seules restitutions hors mission.")
    # Ancre STRUCTURELLE : le tableau des trois objets, une ligne chacun.
    objets = lignes_tableau(t14, "Objet", "Nature", "Canal")
    noms = [sans_accent_bas(l[0]) for l in objets]
    for attendu in ("entretien dû", "erreur robot ou dock", "cycle en cours"):
        if attendu not in noms:
            errs.append(f"ASP-CI-33 : l'objet « {attendu} » n'a pas sa ligne "
                        "propre dans le tableau de cloisonnement (ASP-INV-83).")
    if len(objets) != 3:
        errs.append(f"ASP-CI-33 : le tableau de cloisonnement porte "
                    f"{len(objets)} ligne(s) — trois objets distincts sont "
                    "exigés (ASP-INV-83).")

    # ── Amendement MINIMAL du 08 §6 : les trois puces, en tete de ligne ───
    if t08:
        # Une puce Markdown court sur sa ligne ET ses lignes de continuation
        # indentees : la lire ligne a ligne couperait « statistiques d'usage »
        # en deux et produirait un faux positif.
        puces, courante = [], None
        for ligne in t08.splitlines():
            if ligne.startswith("- "):
                if courante is not None:
                    puces.append(courante)
                courante = ligne
            elif courante is not None and ligne.startswith("  ") and ligne.strip():
                courante += " " + ligne.strip()
            elif courante is not None and not ligne.strip():
                puces.append(courante)
                courante = None
        if courante is not None:
            puces.append(courante)
        corpus = " ".join(sans_accent_bas(p) for p in puces)
        for motif, quoi in (
                ("aucune historisation", "l'exclusion d'historisation"),
                ("aucune mesure de rendement", "l'exclusion des mesures de rendement"),
                ("aucune position cartographique", "l'exclusion de la position")):
            if motif not in corpus:
                errs.append(f"ASP-CI-33 : l'amendement du chapitre 08 §6 a "
                            f"emporté {quoi} — seule la durée de vie des "
                            "consommables devait être levée.")
        if "statistiques d'usage" not in corpus:
            errs.append("ASP-CI-33 : l'amendement du 08 §6 a emporté "
                        "l'exclusion des statistiques d'usage.")
        if "14_entretien.md" not in t08:
            errs.append("ASP-CI-33 : le chapitre 08 §6 ne renvoie pas au "
                        "chapitre 14 — l'exclusion levée n'est pas tracée.")
    return errs


# ─────────────────────────────────────────────────────────────
# Selftest — le juge se vérifie avant de juger
# ─────────────────────────────────────────────────────────────


# ═════════════════════════════════════════════════════════════
# MAINTENANCE — lot M1 : ASP-CI-34 … ASP-CI-36
#
# Les trois controles ne relisent pas le contrat pour se donner raison : ils
# confrontent le RUNTIME a POSTES_ENTRETIEN et a SEUIL_ENTRETIEN_PCT, deja
# figes pour M0, et ils RENDENT les gabarits plutot que de les chercher a la
# regex. Un faux vert de M1 supposerait donc de deplacer la constante commune
# aux deux lots — c'est-a-dire de modifier le juge, sous revue (14 §6.2).
# ═════════════════════════════════════════════════════════════

_SENTINELLE_M1 = object()


def _est_nombre(valeur) -> bool:
    """`is_number` de Home Assistant, a l'identique.

    C'est la SEULE garde du runtime M1 : ce qu'elle refuse devient
    `non_evaluable`. La reproduire fidelement ici est donc la condition pour
    que le rendu simule prouve quoi que ce soit.
    """
    if isinstance(valeur, bool):
        return False
    if isinstance(valeur, (int, float)):
        return not (math.isnan(valeur) or math.isinf(valeur))
    try:
        f = float(valeur)
    except (ValueError, TypeError):
        return False
    return not (math.isnan(f) or math.isinf(f))


def _float_ha(valeur, defaut=_SENTINELLE_M1):
    """`float` de Home Assistant : SANS defaut, il LEVE — il ne replie pas.

    Jinja rend `0.0` sur une valeur non convertible ; Home Assistant leve une
    erreur. Employer le filtre de Jinja ici transformerait silencieusement
    `unavailable` en `0.0` — exactement la conversion que le lot interdit — et
    le rendu simule vaudrait alors le contraire de ce qu'il pretend prouver.
    """
    try:
        return float(valeur)
    except (ValueError, TypeError):
        if defaut is _SENTINELLE_M1:
            raise ValueError(f"float sans défaut sur {valeur!r}")
        return defaut


def _env_m1(etats: dict[str, object] | None = None):
    """Bac a sable du moteur, muni des deux filtres propres a M1.

    Les filtres sont ajoutes APRES coup, sur l'environnement commun : aucun
    controle L1 ne les voit, donc aucun ne change de comportement.
    """
    env = _env_jinja(etats)
    env.filters["is_number"] = _est_nombre
    env.filters["float"] = _float_ha
    return env


def rendu_m1(gabarit: str, etats: dict[str, object], **variables):
    """Rend un gabarit M1 comme Home Assistant le ferait, retypage compris."""
    import ast
    txt = _env_m1(etats).from_string(gabarit).render(**variables).strip()
    try:
        return ast.literal_eval(txt)
    except (ValueError, SyntaxError):
        return txt


def entites_m1(txt: str):
    """(capteur de liste, temoin binaire, nombre total d'entites du fichier)."""
    try:
        doc = yaml.safe_load(txt) or []
    except yaml.YAMLError:
        return None, None, -1
    liste = temoin = None
    total = 0
    if not isinstance(doc, list):
        return None, None, -1
    for bloc in doc:
        if not isinstance(bloc, dict):
            continue
        for domaine, entites in bloc.items():
            for e in entites or []:
                if not isinstance(e, dict):
                    continue
                total += 1
                if domaine == "sensor" and e.get("unique_id") == ID_M1_LISTE:
                    liste = e
                if (domaine == "binary_sensor"
                        and e.get("unique_id") == ID_M1_TEMOIN):
                    temoin = e
    return liste, temoin, total


def _gabarits_m1(entite: dict) -> str:
    """Concatene TOUS les gabarits d'une entite — etat, disponibilite, icone
    et attributs. Un interdit glisse dans un attribut compte autant que dans
    l'etat."""
    if not isinstance(entite, dict):
        return ""
    morceaux = [str(entite.get(cle) or "")
                for cle in ("state", "availability", "icon")]
    attrs = entite.get("attributes")
    if isinstance(attrs, dict):
        morceaux += [str(v) for v in attrs.values()]
    return "\n".join(morceaux)


def check_projection_entretien(m1: str) -> list[str]:
    """ASP-CI-34 — perimetre ferme, plafonds, seuil unique, AUTORITE UNIQUE.

    Le point dur est la DERNIERE section : chacune des quatre sources natives
    doit apparaitre UNE SEULE FOIS dans le fichier. Une seconde declaration —
    dans un attribut, ou dans le temoin binaire — serait une seconde autorite
    de calcul, et deux autorites divergent tot ou tard.
    """
    errs: list[str] = []
    if not m1:
        return [f"ASP-CI-34 : runtime M1 introuvable — `{RUNTIME_M1}`. La "
                "projection d'entretien n'existe pas."]
    liste, temoin, total = entites_m1(m1)
    if total < 0:
        return [f"ASP-CI-34 : `{RUNTIME_M1}` est illisible en YAML."]
    if liste is None:
        errs.append(f"ASP-CI-34 : le capteur de liste `{ID_M1_LISTE}` est "
                    "absent — le cadrage ratifié le nomme (08_NOTIFICATIONS "
                    "§4.2).")
    if temoin is None:
        errs.append(f"ASP-CI-34 : le témoin binaire `{ID_M1_TEMOIN}` est "
                    "absent — le cadrage ratifié le nomme (08_NOTIFICATIONS "
                    "§4.2).")
    if liste is None or temoin is None:
        return errs
    if total != 2:
        errs.append(f"ASP-CI-34 : le fichier M1 déclare {total} entité(s) — il "
                    "en porte exactement deux, celles que le cadrage nomme.")
    for entite, attendu, quoi in ((liste, ENTITE_M1_LISTE, "capteur de liste"),
                                  (temoin, ENTITE_M1_TEMOIN, "témoin binaire")):
        if entite.get("default_entity_id") != attendu:
            errs.append(f"ASP-CI-34 : le {quoi} n'épingle pas son identifiant "
                        f"`{attendu}` — `default_entity_id` vaut "
                        f"{entite.get('default_entity_id')!r}. Les lots N1, M2 "
                        "et UI consomment cet identifiant nommément.")

    # ── Le bloc `variables:` : UNE seule declaration du perimetre ─────────
    variables = liste.get("variables")
    if not isinstance(variables, dict):
        errs.append("ASP-CI-34 : le capteur de liste ne porte aucun bloc "
                    "`variables:` — le périmètre et le seuil y sont déclarés "
                    "une fois, et une seule.")
        return errs
    seuil = variables.get("seuil_pct")
    if seuil != SEUIL_ENTRETIEN_PCT:
        errs.append(f"ASP-CI-34 : le seuil déclaré vaut {seuil!r} — le domaine "
                    f"en connaît UN SEUL, {SEUIL_ENTRETIEN_PCT} %, pour les "
                    "quatre postes (ASP-INV-75).")
    perimetre = variables.get("perimetre")
    if not isinstance(perimetre, list):
        errs.append("ASP-CI-34 : `variables.perimetre` est absent ou n'est pas "
                    "une liste — le périmètre fermé n'est pas déclaré.")
        return errs
    if len(perimetre) != len(PERIMETRE_M1):
        errs.append(f"ASP-CI-34 : le périmètre déclare {len(perimetre)} "
                    f"poste(s) — il en compte exactement {len(PERIMETRE_M1)}, "
                    "ni plus, ni moins (ASP-INV-73).")
    vus = {}
    for i, p in enumerate(perimetre):
        if not isinstance(p, dict):
            errs.append(f"ASP-CI-34 : l'entrée {i} du périmètre n'est pas un "
                        "mapping `nom` / `source` / `plafond_h`.")
            continue
        nom = p.get("nom")
        if nom not in PERIMETRE_M1:
            errs.append(f"ASP-CI-34 : le poste {nom!r} n'appartient pas au "
                        "périmètre contractuel — les quatre libellés Arsenal "
                        f"sont {sorted(PERIMETRE_M1)} (ASP-INV-73).")
            continue
        if nom in vus:
            errs.append(f"ASP-CI-34 : le poste « {nom} » est déclaré deux "
                        "fois.")
        vus[nom] = True
        source, plafond = PERIMETRE_M1[nom]
        if p.get("source") != source:
            errs.append(f"ASP-CI-34 : le poste « {nom} » lit "
                        f"{p.get('source')!r} — sa source attestée est "
                        f"`{source}` (ASP-INV-73).")
        if p.get("plafond_h") != plafond:
            errs.append(f"ASP-CI-34 : le plafond du poste « {nom} » vaut "
                        f"{p.get('plafond_h')!r} h — le contrat en fixe "
                        f"{plafond} h (14 §1).")
    for nom in sorted(set(PERIMETRE_M1) - set(vus)):
        errs.append(f"ASP-CI-34 : le poste « {nom} » est ABSENT du périmètre "
                    "déclaré — un poste manquant est une non-conformité, pas "
                    "une simplification (ASP-INV-73).")

    # ── Filet ferme sur la famille des capteurs natifs ────────────────────
    nu = sans_commentaires_yaml(m1)
    for jeton in sorted(set(FAMILLE_CAPTEUR.findall(nu))):
        if jeton not in CAPTEURS_ENTRETIEN:
            errs.append(f"ASP-CI-34 : le runtime M1 lit `{jeton}`, hors de la "
                        "liste fermée des quatre capteurs d'entretien "
                        "(ASP-INV-73).")

    # ── AUTORITE UNIQUE : une source, une seule declaration ───────────────
    for nom, (source, _plafond) in sorted(PERIMETRE_M1.items()):
        n = nu.count(source)
        if n > 1:
            errs.append(f"ASP-CI-34 : `{source}` est déclarée {n} fois dans le "
                        "runtime M1 — le périmètre a UNE autorité, le bloc "
                        "`variables:`. Deux déclarations divergent tôt ou "
                        "tard.")
    # Le graphe de dependance est un ARBRE, et il n'a que deux etages :
    # quatre natifs -> le capteur de liste -> le temoin. L'autorite ne relit
    # donc ni le temoin, ni elle-meme ; le temoin ne relit pas les natifs, ni
    # lui-meme. Aucun cycle n'est possible, et c'est verifie des deux cotes.
    gabarits_liste = _gabarits_m1(liste)
    for jeton, quoi in ((ENTITE_M1_LISTE, "se relit elle-même"),
                        (ENTITE_M1_TEMOIN, "relit le témoin qui en dérive")):
        if jeton in gabarits_liste:
            errs.append(f"ASP-CI-34 : l'autorité de calcul {quoi} — "
                        f"`{jeton}` apparaît dans ses gabarits. La projection "
                        "dérive des quatre capteurs natifs, et d'eux seuls : "
                        "toute autre lecture ouvre un cycle.")
    gabarits_temoin = _gabarits_m1(temoin)
    if ENTITE_M1_TEMOIN in gabarits_temoin:
        errs.append(f"ASP-CI-34 : le témoin binaire se relit lui-même — "
                    f"`{ENTITE_M1_TEMOIN}` apparaît dans ses propres "
                    "gabarits. Une entité qui dépend de son état précédent "
                    "est fausse à son PREMIER rendu, puis se rattrape : le "
                    "témoin dérive de l'autorité de calcul, jamais de "
                    "lui-même.")
    for jeton in sorted(set(FAMILLE_CAPTEUR.findall(gabarits_temoin))):
        errs.append(f"ASP-CI-34 : le témoin binaire lit directement `{jeton}` "
                    "— il ne CONSOMME plus la projection, il la recalcule. "
                    "C'est une seconde autorité de calcul.")
    if ENTITE_M1_LISTE not in gabarits_temoin:
        errs.append(f"ASP-CI-34 : le témoin binaire ne consomme pas "
                    f"`{ENTITE_M1_LISTE}` — sa valeur ne dérive donc pas de "
                    "l'autorité de calcul du lot.")
    if not str(temoin.get("availability") or "").strip():
        errs.append("ASP-CI-34 : le témoin binaire n'a pas de `availability:` "
                    "— sans elle, la situation « non évaluable » se replierait "
                    "sur `off`, c'est-à-dire sur « non dû » (ASP-INV-76).")

    # ── Les cinq attributs, exactement ────────────────────────────────────
    attrs = liste.get("attributes")
    if not isinstance(attrs, dict):
        errs.append("ASP-CI-34 : le capteur de liste n'expose aucun attribut "
                    "— les lots N1, M2 et UI n'ont rien à consommer.")
    elif tuple(attrs) != ATTRIBUTS_M1:
        errs.append(f"ASP-CI-34 : les attributs exposés sont {list(attrs)} — "
                    f"le lot en expose exactement {list(ATTRIBUTS_M1)}, dans "
                    "cet ordre : ni moins, sans quoi un consommateur manque ; "
                    "ni plus, le lot n'exposant que le nécessaire.")
    return errs


def _liste_de_libelles(valeur, quoi: str, scenario: str) -> list[str]:
    """Refuse tout ce qui n'est pas une liste de LIBELLES Arsenal.

    Un `entity_id` restitue a la place d'un libelle, un doublon, un libelle
    substitue : chacun se voit ici, et aucun ne se voyait quand seul le
    CARDINAL etait confronte.
    """
    errs: list[str] = []
    if not isinstance(valeur, list):
        return [f"ASP-CI-35 : « {scenario} » — `{quoi}` rend {valeur!r}, qui "
                "n'est pas une liste."]
    for item in valeur:
        if not isinstance(item, str):
            errs.append(f"ASP-CI-35 : « {scenario} » — `{quoi}` porte "
                        f"{item!r}, qui n'est pas un libellé.")
        elif item not in ORDRE_M1:
            quoi_dit = ("un identifiant d'entité" if "." in item
                        else "un libellé hors du vocabulaire Arsenal")
            errs.append(f"ASP-CI-35 : « {scenario} » — `{quoi}` porte "
                        f"{item!r} : {quoi_dit}. Les quatre libellés sont "
                        f"{list(ORDRE_M1)}, et l'UI les restitue tels quels.")
    if len(valeur) != len(set(valeur)):
        errs.append(f"ASP-CI-35 : « {scenario} » — `{quoi}` porte des "
                    f"doublons : {valeur!r}.")
    rang = {nom: i for i, nom in enumerate(ORDRE_M1)}
    connus = [x for x in valeur if isinstance(x, str) and x in rang]
    if connus != sorted(connus, key=rang.__getitem__):
        errs.append(f"ASP-CI-35 : « {scenario} » — `{quoi}` rend {valeur!r} "
                    "hors de l'ordre canonique du périmètre "
                    f"{list(ORDRE_M1)} : l'UI et `N1` restituent une liste "
                    "stable, pas un ordre qui bouge d'un rendu à l'autre.")
    return errs


def _partition_m1(dus, non_dus, illisibles, scenario: str) -> list[str]:
    """Les trois listes PARTITIONNENT les quatre postes — toujours.

    C'est l'assertion generale : union exacte, intersections vides, total de
    quatre, chaque libelle une fois et une seule. Un poste vu deux fois ou
    disparu ne peut plus se cacher derriere trois cardinaux qui tombent juste.
    """
    errs: list[str] = []
    listes = {"postes_dus": dus, "postes_non_dus": non_dus,
              "postes_non_evaluables": illisibles}
    if any(not isinstance(v, list) for v in listes.values()):
        return errs                       # deja signale par _liste_de_libelles
    total = [x for v in listes.values() for x in v]
    if len(total) != len(ORDRE_M1):
        errs.append(f"ASP-CI-35 : « {scenario} » — les trois listes cumulent "
                    f"{len(total)} entrée(s) pour {len(ORDRE_M1)} postes. "
                    "Chaque poste relève d'exactement une des trois "
                    "situations (14 §2).")
    for nom in ORDRE_M1:
        n = total.count(nom)
        if n != 1:
            ou = [c for c, v in listes.items() if nom in v]
            errs.append(f"ASP-CI-35 : « {scenario} » — « {nom} » apparaît "
                        f"{n} fois dans les trois listes"
                        + (f" ({', '.join(ou)})" if ou else " — nulle part")
                        + ". Un poste est dû, non dû ou non évaluable : "
                          "jamais deux à la fois, jamais aucune.")
    for a, b in (("postes_dus", "postes_non_dus"),
                 ("postes_dus", "postes_non_evaluables"),
                 ("postes_non_dus", "postes_non_evaluables")):
        commun = sorted(set(listes[a]) & set(listes[b]))
        if commun:
            errs.append(f"ASP-CI-35 : « {scenario} » — `{a}` et `{b}` se "
                        f"recoupent sur {commun}. Les trois situations sont "
                        "exclusives (ASP-INV-76).")
    if set(total) != set(ORDRE_M1):
        errs.append(f"ASP-CI-35 : « {scenario} » — l'union des trois listes "
                    f"vaut {sorted(set(total))}, attendu {list(ORDRE_M1)}.")
    return errs


# Tolerances de la confrontation numerique.
#
# Le runtime arrondit `restant_h` a 3 decimales et `restant_pourcentage` a 2.
# L'ecart legitime est donc borne par une DEMI-unite du dernier rang :
# 5e-4 h et 5e-3 point. Les tolerances retenues valent le double, ce qui
# absorbe le flottant sans rien laisser passer d'autre :
#
#   `restant_h` x2 ..................... ecart de l'ordre de 67 h
#   `restant_h` en secondes ............ ecart de l'ordre de 241 000
#   mauvais diviseur (plafond x2) ...... ecart de 22 points
#   plafond permute ................... ecart de plusieurs dizaines de points
#   pourcentage arrondi a l'entier ..... ecart jusqu'a 0,5 point
#   pourcentage remplace par 50 ........ ecart de plusieurs points
#
# La plus fine de ces mutations — l'arrondi a l'entier — laisse jusqu'a
# 0,5 point d'ecart, soit CINQUANTE fois la tolerance. La marge est donc
# large des deux cotes : aucun faux positif de flottant, aucun faux vert.
TOL_RESTANT_H = 1e-3
TOL_POURCENTAGE = 1e-2


def check_projection_rendue(m1: str) -> list[str]:
    """ASP-CI-35 — les TROIS situations, RENDUES sur des etats simules.

    Ce controle ne cherche aucun mot-cle : il execute les gabarits. Un repli
    numerique, une indisponibilite rabattue sur « non du », un seuil deplace
    ou un poste disparu changent le RESULTAT, et c'est le resultat qui est
    confronte.

    Revue ciblee — deux angles morts fermes. Les listes sont confrontees
    VALEUR PAR VALEUR, plus seulement par leur cardinal, et la charge
    NUMERIQUE de `postes` est verifiee au lieu d'etre supposee.
    """
    errs: list[str] = []
    if not m1:
        return [f"ASP-CI-35 : runtime M1 introuvable — `{RUNTIME_M1}`."]
    liste, temoin, _total = entites_m1(m1)
    if liste is None or temoin is None:
        return ["ASP-CI-35 : les deux entités de la projection sont "
                "introuvables — rien à rendre."]
    variables = liste.get("variables")
    if not isinstance(variables, dict):
        return ["ASP-CI-35 : bloc `variables:` absent — rien à rendre."]
    attrs = liste.get("attributes") or {}

    # Le releve du 2026-08-27, RECONDUIT a l'observation passive du
    # 2026-08-28 : les quatre compteurs n'ont pas bouge, le robot n'ayant pas
    # nettoye entre les deux. Aucun poste n'est du, le plus avance etant a
    # 13,377 % de restant.
    #
    # Les restants sont donnes en SECONDES — l'unite native, celle du releve
    # d'attestation §4 — et les heures en DERIVENT. C'est la forme falsifiable
    # de la fixture : `restant = plafond - travail cumule` s'y verifie a la
    # seconde pres, et 668 299 n'est compatible qu'avec le plafond de 720 000.
    F, P, L, C = ORDRE_M1
    SOURCE = {nom: src for nom, (src, _p) in PERIMETRE_M1.items()}
    RESTANT_S = {F: 241253, P: 286868, L: 668299, C: 14447}
    REEL = {SOURCE[nom]: repr(s / 3600) for nom, s in RESTANT_S.items()}

    def etats(**remplacements):
        """Le releve reel, avec les postes nommes remplaces ou retires."""
        e = dict(REEL)
        for cle, val in remplacements.items():
            cible = SOURCE[{"filtre": F, "principale": P, "laterale": L,
                            "capteurs": C}[cle]]
            if val is None:
                e.pop(cible, None)
            else:
                e[cible] = val
        return e

    # (états natifs, état attendu, dus, non dus, non évaluables,
    #  témoin disponible ?, témoin allumé ?, postes au-dessus du plafond,
    #  libellé)
    scenarios = [
        (etats(), ETAT_M1_AUCUN, [], [F, P, L, C], [], True, False, [],
         "relevé réel"),
        (etats(capteurs="3.0"), C, [C], [F, P, L], [], True, True, [],
         "seuil atteint pile"),
        (etats(capteurs="3.001"), ETAT_M1_AUCUN, [], [F, P, L, C], [], True,
         False, [], "juste au-dessus du seuil"),
        (etats(capteurs="0"), C, [C], [F, P, L], [], True, True, [],
         "compteur à zéro"),
        (etats(capteurs="-1"), C, [C], [F, P, L], [], True, True, [],
         "compteur négatif"),
        (etats(filtre="15.0", capteurs="unavailable"), F, [F], [P, L], [C],
         True, True, [], "un dû et un illisible"),
        ({}, ETAT_M1_NON_EVAL, [], [], [F, P, L, C], False, None, [],
         "les quatre absents"),
        ({SOURCE[n]: "0" for n in ORDRE_M1}, ", ".join(ORDRE_M1),
         [F, P, L, C], [], [], True, True, [], "les quatre dus"),
        # ── Revue ciblee : valeur SUPERIEURE au plafond ───────────────────
        #
        # Valeur ACCEPTEE du compteur natif : le restant remonte a son
        # plafond apres une remise a zero, et rien ne garantit qu'il n'y
        # depasse jamais — le plafond vit en constante amont, pas dans
        # l'entite. Le poste est alors LISIBLE et NON DU, et le pourcentage
        # est restitue TEL QUEL, au-dessus de 100. Le normaliser
        # silencieusement a 100 masquerait un etat reel de l'appareil.
        # Ce n'est ni une anomalie a signaler, ni une prediction.
        (etats(capteurs="35"), ETAT_M1_AUCUN, [], [F, P, L, C], [], True,
         False, [C], "restant au-dessus du plafond"),
        # ── Revue ciblee : PLUSIEURS illisibles, et un poste du ───────────
        #
        # L'information incomplete ne masque pas l'entretien effectivement
        # du : le temoin reste DISPONIBLE et ALLUME, parce que la question
        # « au moins un entretien reclame-t-il une intervention ? » est
        # tranchee des qu'un poste est du.
        (etats(filtre="15.0", principale="unavailable", laterale="unknown"),
         F, [F], [C], [P, L], True, True, [], "deux illisibles et un dû"),
    ]
    for illisible in ILLISIBLES_M1:
        scenarios.append(
            (etats(capteurs=illisible), ETAT_M1_NON_EVAL, [], [F, P, L], [C],
             False, None, [], f"capteurs = {illisible!r}"))
    scenarios.append(
        (etats(capteurs=None), ETAT_M1_NON_EVAL, [], [F, P, L], [C], False,
         None, [], "capteurs absent du registre"))

    for (natifs, attendu, dus, non_dus, illisibles, dispo, allume, sup_100,
         quoi) in scenarios:
        try:
            etat = rendu_m1(str(liste.get("state") or ""), natifs, **variables)
            rendus = {cle: rendu_m1(str(gab), natifs, **variables)
                      for cle, gab in attrs.items()}
        except Exception as exc:                       # noqa: BLE001
            errs.append(f"ASP-CI-35 : le rendu échoue sur « {quoi} » — "
                        f"{type(exc).__name__} : {exc}. Un gabarit qui lève "
                        "rend l'entité indisponible sans le dire.")
            continue
        if etat != attendu:
            errs.append(f"ASP-CI-35 : « {quoi} » rend l'état {etat!r} — "
                        f"attendu {attendu!r} (14 §2, ASP-INV-75 / "
                        "ASP-INV-76).")

        # ── Les trois listes, VALEUR par VALEUR ───────────────────────────
        for cle, cible in (("postes_dus", dus), ("postes_non_dus", non_dus),
                           ("postes_non_evaluables", illisibles)):
            obtenu = rendus.get(cle)
            errs += _liste_de_libelles(obtenu, cle, quoi)
            if obtenu != cible:
                errs.append(f"ASP-CI-35 : « {quoi} » rend `{cle}` "
                            f"{obtenu!r} — attendu {cible!r}"
                            + (" ; un poste illisible n'est JAMAIS « non dû » "
                               "(ASP-INV-76)."
                               if cle == "postes_non_dus" else "."))
        errs += _partition_m1(rendus.get("postes_dus"),
                              rendus.get("postes_non_dus"),
                              rendus.get("postes_non_evaluables"), quoi)

        if rendus.get("seuil_pourcentage") != SEUIL_ENTRETIEN_PCT:
            errs.append(f"ASP-CI-35 : « {quoi} » restitue le seuil "
                        f"{rendus.get('seuil_pourcentage')!r} — attendu "
                        f"{SEUIL_ENTRETIEN_PCT}.")

        # ── Le detail : classe, plafond, ET CHARGE NUMERIQUE ──────────────
        detail = rendus.get("postes")
        if not isinstance(detail, list) or len(detail) != len(PERIMETRE_M1):
            errs.append(f"ASP-CI-35 : « {quoi} » rend un détail de "
                        f"{detail!r} — les quatre postes y figurent toujours, "
                        "y compris illisibles.")
            continue
        for ligne in detail:
            if not isinstance(ligne, dict) or tuple(ligne) != CLES_POSTE_M1:
                errs.append(f"ASP-CI-35 : « {quoi} » — le détail d'un poste "
                            f"porte {list(ligne) if isinstance(ligne, dict) else ligne!r}"
                            f", attendu {list(CLES_POSTE_M1)}.")
                break
            nom = ligne["poste"]
            if nom not in PERIMETRE_M1:
                errs.append(f"ASP-CI-35 : « {quoi} » — le détail nomme "
                            f"{nom!r}, hors du périmètre.")
                continue
            source, plafond = PERIMETRE_M1[nom]
            if ligne["plafond_h"] != plafond:
                errs.append(f"ASP-CI-35 : « {quoi} » — le plafond restitué "
                            f"pour « {nom} » vaut {ligne['plafond_h']!r} h, "
                            f"attendu {plafond} h.")
            brut = natifs.get(source)
            lisible = _est_nombre(brut)
            classe = ("non_evaluable" if not lisible
                      else "du" if float(brut) <= plafond * SEUIL_ENTRETIEN_PCT
                      / 100 else "non_du")
            if ligne["classe"] != classe:
                errs.append(f"ASP-CI-35 : « {quoi} » — « {nom} » est classé "
                            f"{ligne['classe']!r}, attendu {classe!r} "
                            "(ASP-INV-75, ASP-INV-76).")
            if not lisible:
                for cle in ("restant_h", "restant_pourcentage"):
                    if ligne[cle] is not None:
                        errs.append(f"ASP-CI-35 : « {quoi} » — « {nom} » est "
                                    f"non évaluable et porte pourtant "
                                    f"`{cle}` = {ligne[cle]!r}. Une valeur de "
                                    "repli est apparue (ASP-INV-74).")
                continue
            v = float(brut)
            for cle, exact, tol, quoi_dit in (
                    ("restant_h", v, TOL_RESTANT_H,
                     "la valeur native, rendue en HEURES"),
                    ("restant_pourcentage", v / plafond * 100,
                     TOL_POURCENTAGE, "`restant_h / plafond_h × 100`")):
                obtenu = ligne[cle]
                if not isinstance(obtenu, (int, float)) or \
                        isinstance(obtenu, bool):
                    errs.append(f"ASP-CI-35 : « {quoi} » — « {nom} » rend "
                                f"`{cle}` = {obtenu!r}, qui n'est pas un "
                                "nombre.")
                elif not math.isclose(obtenu, exact, rel_tol=0.0,
                                      abs_tol=tol):
                    errs.append(f"ASP-CI-35 : « {quoi} » — « {nom} » rend "
                                f"`{cle}` = {obtenu!r}, attendu {exact!r} à "
                                f"{tol} près — c'est {quoi_dit}. L'écart "
                                f"vaut {abs(obtenu - exact):.6g}, bien "
                                "au-delà de l'arrondi de restitution.")
            if nom in sup_100 and not (
                    isinstance(ligne["restant_pourcentage"], (int, float))
                    and ligne["restant_pourcentage"] > 100):
                errs.append(f"ASP-CI-35 : « {quoi} » — « {nom} » a un restant "
                            "SUPÉRIEUR à son plafond et rend pourtant "
                            f"{ligne['restant_pourcentage']!r} %. La valeur "
                            "est restituée telle quelle : la normaliser à 100 "
                            "masquerait un état réel de l'appareil.")

        # ── Le temoin binaire, rendu SUR la projection ────────────────────
        simule = dict(natifs)
        simule[ENTITE_M1_LISTE] = {"state": etat, "attrs": rendus}
        try:
            d = rendu_m1(str(temoin.get("availability") or ""), simule)
            v_etat = rendu_m1(str(temoin.get("state") or ""), simule)
            ico = rendu_m1(str(temoin.get("icon") or ""), simule)
        except Exception as exc:                       # noqa: BLE001
            errs.append(f"ASP-CI-35 : le témoin échoue sur « {quoi} » — "
                        f"{type(exc).__name__} : {exc}.")
            continue
        if bool(d) is not dispo:
            errs.append(f"ASP-CI-35 : « {quoi} » — le témoin est "
                        f"{'disponible' if d else 'indisponible'}, attendu "
                        f"{'disponible' if dispo else 'INDISPONIBLE'}. Rendre "
                        "un booléen quand la question n'est pas tranchable "
                        "convertit un trou d'information en « non dû » "
                        "(ASP-INV-76).")
        if dispo and bool(v_etat) is not allume:
            errs.append(f"ASP-CI-35 : « {quoi} » — le témoin vaut {v_etat!r}, "
                        f"attendu {allume!r}.")
        # L'icone derive de l'AUTORITE, jamais de l'etat precedent du temoin.
        # Elle est donc juste DES LE PREMIER rendu, sans etat anterieur : le
        # bac a sable n'en fournit aucun, et c'est exactement le point.
        if dispo:
            attendue = ICONE_M1_DUE if allume else ICONE_M1_SOLDEE
            if ico != attendue:
                errs.append(f"ASP-CI-35 : « {quoi} » — l'icône du témoin rend "
                            f"{ico!r}, attendu {attendue!r}. Elle doit dériver "
                            f"de `postes_dus` du capteur de liste, et être "
                            "juste dès le PREMIER rendu — aucun état "
                            "antérieur n'existe alors.")
    return errs


def check_interdits_projection(m1: str) -> list[str]:
    """ASP-CI-36 — ce que M1 ne fait pas, et qu'aucun commentaire n'excuse.

    Le balayage porte sur le fichier PRIVE DE SES COMMENTAIRES : un en-tete
    qui ENUMERE ce que le lot s'interdit ne doit pas declencher la garde qui
    l'interdit. Un interdit reintroduit en commentaire n'execute rien.
    """
    errs: list[str] = []
    if not m1:
        return [f"ASP-CI-36 : runtime M1 introuvable — `{RUNTIME_M1}`."]
    nu = sans_commentaires_yaml(m1)

    for m in SERVICE_M1.finditer(nu):
        errs.append(f"ASP-CI-36 : le runtime M1 porte une clé de service "
                    f"(ligne « {m.group(0).strip()} ») — une projection "
                    "n'agit pas. Aucun appel de service, donc aucune pression "
                    "de bouton et aucune commande robot (ASP-INV-77, "
                    "ASP-INV-82).")
    if PRESS_SERVICE.search(nu):
        errs.append("ASP-CI-36 : le runtime M1 appelle `button.press` — la "
                    "primitive irréversible n'appartient qu'au script du lot "
                    "M2 (ASP-INV-81).")
    for bouton in sorted(set(BOUTON_ENTRETIEN_RE.findall(nu))):
        errs.append(f"ASP-CI-36 : le runtime M1 mentionne `{bouton}` — M1 "
                    "projette, il ne remet rien à zéro (ASP-INV-81).")
    for m in re.finditer(r"\b(?:vacuum|roborock)\.[a-z0-9_]+", nu):
        errs.append(f"ASP-CI-36 : le runtime M1 mentionne `{m.group(0)}` — "
                    "l'écrivain unique du domaine est le moteur de mission, "
                    "et M1 ne commande pas l'appareil (ASP-INV-31).")
    for jeton in NOTIFICATION_M1:
        if jeton in nu:
            errs.append(f"ASP-CI-36 : le runtime M1 porte `{jeton}` — M1 ne "
                        "notifie pas. Le lot N1 CONSOMMERA cette projection "
                        "(14 §5).")
    for helper in (ID_VERDICT, ID_TRACE):
        if helper in nu:
            errs.append(f"ASP-CI-36 : le runtime M1 référence `{helper}` — la "
                        "projection d'entretien ne lit ni n'écrit le verdict "
                        "de mission ; les deux périmètres sont cloisonnés "
                        "(ASP-INV-31, 14 §5).")
    for m in REPLI_NUMERIQUE.finditer(nu):
        errs.append(f"ASP-CI-36 : le runtime M1 emploie un repli numérique "
                    f"(« {m.group(0).strip()} ») — il convertirait une donnée "
                    "absente en mesure nominale, contre ASP-INV-74. La garde "
                    "du lot est `is_number`, et `float` y est appelé SANS "
                    "défaut.")
    for jeton in TEMPOREL_M1:
        if jeton in nu:
            errs.append(f"ASP-CI-36 : le runtime M1 emploie `{jeton}` — le "
                        "domaine CONSTATE un seuil, il ne projette aucune "
                        "date, aucune tendance et aucun rythme d'usage "
                        "(14 §2).")
    # La garde d'illisibilite doit etre presente autant de fois qu'il y a de
    # gabarits qui lisent une source : la retirer d'un seul suffirait a
    # rabattre un trou sur une mesure.
    liste, _temoin, _t = entites_m1(m1)
    if isinstance(liste, dict):
        for cle, gabarit in [("state", liste.get("state"))] + \
                list((liste.get("attributes") or {}).items()):
            g = str(gabarit or "")
            if "p.source" in g and "is_number" not in g:
                errs.append(f"ASP-CI-36 : le gabarit « {cle} » lit une source "
                            "sans la garde `is_number` — une valeur non "
                            "numérique y serait traitée comme une mesure "
                            "(ASP-INV-74).")
    return errs


class Compteur:
    """Décompte DÉRIVÉ des cas joués : aucun total n'est écrit à la main."""

    def __init__(self) -> None:
        self.conformes = 0
        self.violations = 0

    def conforme(self, errs: list[str], libelle: str) -> None:
        assert not errs, f"{libelle} : attendu conforme, obtenu {errs}"
        self.conformes += 1

    def viole(self, errs: list[str], motif: str, libelle: str) -> None:
        assert any(motif in e for e in errs), \
            f"{libelle} : attendu « {motif} », obtenu {errs}"
        self.violations += 1

    def total(self) -> int:
        return self.conformes + self.violations


def selftest() -> None:
    c = Compteur()

    # ---- strip_fences (F6) : un bloc clôturé ne déclare rien --------------
    fixture_bloc = (
        "> **`ASP-INV-1`** — vrai\n> ### `ASP-IMC-1` — vrai\n"
        "```yaml\n> **`ASP-INV-99`** — faux invariant\n"
        "`REFUS_FICTIF`\nscript.faux_identifiant\n```\n")
    neutralise = {"a.md": strip_fences(fixture_bloc)}
    c.conforme(check_invariants(neutralise), "F6/CI-1 bloc clôturé")
    cat_bloc = {
        FICHIER_CATALOGUE: ("## 2. Catalogue des refus\n| `REFUS_UN` | m |\n"
                            "## 3. Catalogue des échecs\n| `ECHEC_UN` | m |\n\n## 4. s\n"),
        "07.md": strip_fences("`REFUS_UN`\n```\n`REFUS_FICTIF`\n```\n")}
    c.conforme(check_codes(cat_bloc), "F6/CI-3 bloc clôturé")
    c.conforme(check_identifiants(
        {"a.md": strip_fences("```\nscript.faux_identifiant\n```\n")},
        "vacuum.roborock_q7_max"), "F6/CI-6 bloc clôturé")

    # ---- ASP-CI-1 --------------------------------------------------------
    bon = {"a.md": "> **`ASP-INV-1`** — x\n> **`ASP-INV-2`** — y\n",
           "b.md": "> **`ASP-INV-3`** — z\n> ### `ASP-IMC-1` — t\n"}
    c.conforme(check_invariants(bon), "CI-1 conforme")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n> **`ASP-INV-3`** — z\n"
                                      "> ### `ASP-IMC-1` — t\n"}),
            "trouée", "CI-1 trou")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n> **`ASP-INV-1`** — y\n"
                                      "> ### `ASP-IMC-1` — t\n"}),
            "plusieurs fois", "CI-1 doublon")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n"
                                      "> **Invariant `ASP-INV-2`** — y\n"
                                      "> ### `ASP-IMC-1` — t\n"}),
            "non uniforme", "CI-1 format")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n"}),
            "ASP-IMC-1", "CI-1 IMC absent")

    # ---- ASP-CI-2 : ancre audit (F1) -------------------------------------
    AUD = ("| `0_16` | `Salon` | RDC |\n| `0_18` | `Entrée` | RDC |\n"
           "| `1_16` | `Palier` | Étage |\n"
           "| `2_17` | `Ext` | Annexe |\n| `2_18` | `Chambre1` | Annexe |\n"
           "| **0** | `RDC` | 2 |\n| **1** | `Étage ` | 1 |\n")

    def t02(seg="0_16", nom="Séjour", roboro="`Salon`", comp="`0_16` · `0_18`",
            carte="0", extra=""):
        return (f"| `{seg}` | **{nom}** | {roboro} |\n"
                "| `0_18` | **Entrée** | — |\n"
                "| `1_16` | **Palier** |\n" + extra +
                f"| **RDC complet** | `{carte}` | {comp} |\n")
    t10_ok = "| **Étage** | `1` | `1_16` |\n"
    c.conforme(check_referentiel(t02(), t10_ok, AUD), "CI-2 conforme")
    # Falsification COHÉRENTE de toute la chaîne : table + périmètre + raccourci.
    c.viole(check_referentiel(t02(seg="0_77", comp="`0_77` · `0_18`"),
                              t10_ok, AUD),
            "ABSENT de l'audit", "F1/CI-2 falsification cohérente")
    c.viole(check_referentiel(t02(nom="Salon Bis", roboro="—"), t10_ok, AUD),
            "l'audit atteste", "F1/CI-2 nom falsifié")
    c.viole(check_referentiel(t02(extra="| `2_17` | **Extérieur** |\n",
                                  comp="`0_16` · `0_18` · `2_17`"), t10_ok, AUD),
            "NON COMMANDABLE", "F1/CI-2 segment observé promu")
    c.viole(check_referentiel(t02(), t10_ok, ""),
            "ne peut pas être attesté", "F1/CI-2 audit absent")
    c.viole(check_referentiel(t02(comp="`0_16` · `0_99`"), t10_ok, AUD),
            "hors référentiel", "CI-2 segment inconnu")
    c.viole(check_referentiel(t02(comp="`0_16` · `1_16`"),
                              "| **X** | `0` | `0_18` |\n", AUD),
            "plusieurs cartes", "CI-2 multi-carte")
    c.viole(check_referentiel(t02(carte="1"), t10_ok, AUD),
            "déclare la carte", "CI-2 carte incohérente")
    c.viole(check_referentiel(t02(), "| **X** | `0` | `0_18` |\n", AUD),
            "jamais employés", "CI-2 segment orphelin")

    # ---- ASP-CI-3 --------------------------------------------------------
    def cat(extra_refus="", cite="", renvoi=""):
        t09 = ("## 2. Catalogue des refus\n| `REFUS_UN` | motif |\n"
               f"{extra_refus}"
               "## 3. Catalogue des échecs\n| `ECHEC_UN` | motif |\n\n## 4. suite\n")
        return {FICHIER_CATALOGUE: t09,
                "07.md": "`REFUS_UN`" + cite + renvoi}
    c.conforme(check_codes(cat()), "CI-3 conforme")
    c.viole(check_codes(cat(cite=" et `REFUS_FANTOME`")),
            "hors catalogue", "CI-3 code orphelin")
    c.viole(check_codes(cat(extra_refus="| `REFUS_MORT` | motif |\n")),
            "qu'aucune clause ne produit", "CI-3 refus mort")
    # F8 : un refus cité UNIQUEMENT dans une section « Renvois » est mort.
    c.viole(check_codes(cat(extra_refus="| `REFUS_RENVOI` | motif |\n",
                            renvoi="\n\n## Renvois\n\n- voir `REFUS_RENVOI`\n")),
            "qu'aucune clause ne produit", "F8/CI-3 refus vivant par renvoi seul")
    # F9 : un code de cinq caractères est traité comme les autres.
    c.viole(check_codes(cat(extra_refus="| `ABCDE` | motif |\n")),
            "ABCDE", "F9/CI-3 code de cinq caractères")
    c.conforme(check_codes({FICHIER_CATALOGUE: ("## 2. Catalogue des refus\n"
                                                "| `ABCDE` | motif |\n"
                                                "## 3. Catalogue des échecs\n"
                                                "| `ECHEC_UN` | m |\n\n## 4. s\n"),
                            "07.md": "`ABCDE`"}),
               "F9/CI-3 code de cinq caractères produit")

    # ---- ASP-CI-4 : classification figée (F2) et lien N (F13) -------------
    def part(r="`charger_disconnected` · `charging`",
             a="`cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · "
               "`returning_home` · `docking`",
             e="`error` · `device_offline` · `unknown` · `unavailable`",
             n_effet="**Refus** `ETAT_NON_QUALIFIE`",
             regle="> **`ASP-INV-60`** — refus par défaut `ETAT_NON_QUALIFIE`.\n"):
        return ("### 5.0 titre\n"
                f"| **R — Repos** | {r} | **Admissible** |\n"
                f"| **A — Activité** | {a} | `MISSION_DEJA_OUVERTE` |\n"
                f"| **E — Erreur** | {e} | Refus |\n"
                f"| **N — Non qualifiée** | toute autre valeur | {n_effet} |\n"
                + regle + "### 5.1 suite\n")
    t08 = ("énumération **non exhaustive** : `charger_disconnected`, `charging`, "
           "`cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, "
           "`returning_home`, `docking`, `error`, `device_offline`…\n")
    c.conforme(check_partition(part(), t08), "CI-4 conforme")
    # F2 : le déplacement A -> R, la régression exacte que le checker vise.
    c.viole(check_partition(part(
        r="`charger_disconnected` · `charging` · `returning_home`",
        a="`cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · `docking`"),
        t08), "DÉPLACÉ", "F2/CI-4 returning_home A -> R")
    c.viole(check_partition(part(
        a="`cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · "
          "`returning_home`"), t08),
        "absent", "F2/CI-4 docking retiré")
    c.viole(check_partition(part(r="`charger_disconnected` · `charging` · `idle`"), t08),
            "hors classification attestée", "F2/CI-4 état ajouté")
    # F13 : le lien classe N -> ETAT_NON_QUALIFIE, code conservé ailleurs.
    c.viole(check_partition(part(n_effet="**Refus**"), t08),
            "ne produit pas", "F13/CI-4 lien N rompu")
    c.viole(check_partition(part(regle="> **`ASP-INV-60`** — refus par défaut.\n"),
                            t08),
            "ne nomme pas", "F13/CI-4 règle par défaut muette")
    c.viole(check_partition(part(regle=""), t08),
            "aucune règle de refus par défaut", "F13/CI-4 règle absente")
    # R1 : ligne N tronquée à deux colonnes, suivie d'une prose SANS barre qui
    # mentionne le code. Un motif franchissant la ligne capturerait cette prose
    # comme cellule d'effet et conclurait à tort que le lien tient.
    c.viole(check_partition(
        "### 5.0 titre\n"
        "| **R — Repos** | `charger_disconnected` · `charging` | ok |\n"
        "| **A — Activité** | `cleaning` · `segment_cleaning` · `zoned_cleaning` · "
        "`paused` · `returning_home` · `docking` | ok |\n"
        "| **E — Erreur** | `error` · `device_offline` · `unknown` · `unavailable` | ok |\n"
        "| **N — Non qualifiée** | toute autre valeur |\n"
        "prose libre sans barre mentionnant ETAT_NON_QUALIFIE\n"
        "> **`ASP-INV-60`** — refus par défaut `ETAT_NON_QUALIFIE`.\n"
        "### 5.1 suite\n", t08),
        "incomplète", "R1/CI-4 ligne N tronquée + prose ultérieure")
    c.viole(check_partition("pas de section 5.0", t08),
            "incomplète", "CI-4 partition absente")

    # ---- ASP-CI-5 --------------------------------------------------------
    lignes = [("Minimale", "quiet", "off"), ("Normale", "balanced", "off"),
              ("Turbo", "turbo", "off"), ("Max", "max", "off"),
              ("Moyenne", "quiet", "medium"), ("Intensive", "quiet", "high")]

    def t03(rows):
        corps = "".join(f"| **{n}** | `{f}` | `{e}` |\n" for n, f, e in rows)
        return "## 1. Table canonique\n" + corps + "\n## 2. suite\n"
    c.conforme(check_profils(t03(lignes)), "CI-5 conforme")
    c.viole(check_profils(t03(lignes[:5])), "compter 6", "CI-5 cardinalité")
    c.viole(check_profils(t03(lignes[:5] + [("Douce", "gentle", "off")])),
            "gentle", "CI-5 gentle réintroduit")
    c.viole(check_profils(t03(lignes[:5] + [("Bizarre", "ultra", "off")])),
            "hors énumération", "CI-5 valeur inventée")

    # ---- R3 : blocs clôturés sur ASP-CI-2, ASP-CI-4 et ASP-CI-5 ----------
    # Un exemple en bloc clôturé ne modifie ni le référentiel, ni une classe
    # d'état, ni la table des profils. La prose normative hors bloc, elle, reste
    # contrôlée — c'est ce que prouve le second cas de chaque paire.
    AUD_R3 = ("| `0_16` | `Salon` | RDC |\n| `0_18` | `Entrée` | RDC |\n"
              "| `2_17` | `Ext` | Annexe |\n| `2_18` | `Chambre1` | Annexe |\n"
              "| **0** | `RDC` | 2 |\n")
    t02_r3 = ("| `0_16` | **Séjour** | `Salon` |\n| `0_18` | **Entrée** | — |\n"
              "```markdown\n| `9_99` | **Pièce fictive** | — |\n```\n"
              "| **RDC complet** | `0` | `0_16` · `0_18` |\n")
    t10_r3 = "| **Séjour seul** | `0` | `0_16` |\n"
    c.conforme(check_referentiel(strip_fences(t02_r3), t10_r3, AUD_R3),
               "R3/CI-2 faux segment en bloc clôturé")
    hors_bloc = t02_r3.replace("```markdown\n", "").replace("\n```\n", "\n")
    c.viole(check_referentiel(strip_fences(hors_bloc), t10_r3, AUD_R3),
            "ABSENT de l'audit", "R3/CI-2 le même segment hors bloc reste contrôlé")

    t07_r3 = part().replace("### 5.1 suite\n",
                            "```\n| **R — Repos** | `idle` | ok |\n```\n### 5.1 suite\n")
    c.conforme(check_partition(strip_fences(t07_r3), t08),
               "R3/CI-4 fausse classe en bloc clôturé")

    t03_r3 = ("## 1. Table canonique\n"
              + "".join(f"| **{n}** | `{f}` | `{e}` |\n" for n, f, e in lignes)
              + "```\n| **Faux profil** | `gentle` | `off` |\n```\n\n## 2. suite\n")
    c.conforme(check_profils(strip_fences(t03_r3)), "R3/CI-5 faux profil en bloc clôturé")
    c.viole(check_profils(strip_fences(t03_r3.replace("```\n", ""))),
            "gentle", "R3/CI-5 le même profil hors bloc reste contrôlé")

    # ---- ASP-CI-6 : jeton exact (F7, F12) --------------------------------
    # CONTRE-EXEMPLES DÉLIBÉRÉS, confinés au selftest. `script.aspirateur_lancer`,
    # `switch.aspirateur_relance` et `sensor.roborock_q7_max_eta` n'existent pas
    # et ne doivent jamais être créés : ils prouvent que le contrôle les REFUSE.
    audit_fixture = ("`vacuum.roborock_q7_max`, `sensor.roborock_q7_max_etat`, "
                     "`vacuum.send_command`")
    c.conforme(check_identifiants(
        {"a.md": "on cite `vacuum.roborock_q7_max` et `vacuum.send_command`"},
        audit_fixture), "CI-6 conforme")
    c.conforme(check_identifiants(
        {"a.md": "voir `07_moteur_de_mission.md` et le rôle `‹moteur_de_mission›`"},
        audit_fixture), "CI-6 nom de fichier et rôle abstrait")
    c.viole(check_identifiants({"a.md": "script.aspirateur_lancer"}, audit_fixture),
            "ASP-INV-58", "CI-6 helper Arsenal")
    # F7 : un domaine jusque-là absent de la liste.
    c.viole(check_identifiants({"a.md": "switch.aspirateur_relance"}, audit_fixture),
            "ni attesté", "F7/CI-6 domaine absent (switch)")
    c.viole(check_identifiants({"a.md": "input_button.aspirateur_relance"},
                               audit_fixture),
            "ASP-INV-58", "F7/CI-6 domaine absent (input_button)")
    # I1 : domaines volontairement absents de toute liste — la détection est
    # LEXICALE, elle ne dépend d'aucune énumération de domaines Home Assistant.
    for ident in ("plant.aspirateur_x", "sun.aspirateur_x", "lawn_mower.aspirateur_x",
                  "un_domaine_inexistant.aspirateur_x", "sensor.roborock_q7_max_inexistant"):
        c.viole(check_identifiants({"a.md": ident}, audit_fixture),
                "ni attesté", f"I1/CI-6 ciblage lexical — {ident}")
    # …et les emplois légitimes passent, y compris les primitives de service.
    c.conforme(check_identifiants(
        {"a.md": "`vacuum.start`, `vacuum.send_command`, `select.select_option`, "
                 "`sensor.roborock_q7_max_etat`, `image.png`, `un.texte`"},
        audit_fixture + " `select.select_option` `vacuum.start`"),
        "I1/CI-6 primitives, entité attestée, littéraux hors domaine")
    # F12 : préfixe tronqué d'une entité réelle.
    c.viole(check_identifiants({"a.md": "`sensor.roborock_q7_max_eta`"},
                               audit_fixture),
            "ni attesté", "F12/CI-6 identifiant tronqué")
    c.viole(check_identifiants({"a.md": "x"}, ""),
            "introuvable", "CI-6 audit absent")

    # ---- ASP-CI-7 : entités et services (F3) -----------------------------
    c.conforme(check_lovelace({"18_lovelace/x.yaml":
                               "entity: sensor.roborock_q7_max_batterie\n"
                               "entity: binary_sensor.roborock_q7_max_en_charge\n"
                               "entity: image.roborock_q7_max_rdc\n"}),
               "CI-7 lecture seule préservée")
    c.conforme(check_lovelace({"18_lovelace/x.yaml":
                               "# on ne doit pas appeler service: vacuum.start ici\n"}),
               "CI-7 mention en commentaire")
    c.viole(check_lovelace({"18_lovelace/x.yaml": "entity: vacuum.roborock_q7_max"}),
            "ASP-INV-31", "CI-7 entité d'action")
    c.viole(check_lovelace({"19_button_card_templates/y.yaml":
                            "entity: select.roborock_q7_max_carte_selectionnee"}),
            "ASP-CI-7", "CI-7 sélecteur brut")
    # F3 : cinq services bruts, ciblés sans aucun `entity_id` contenant roborock.
    for cible, service, libelle in (
        ("device_id: abc", "vacuum.send_command", "send_command par device_id"),
        ("area_id: rdc", "roborock.set_vacuum_zoned_cleaning", "service roborock.*"),
        ("label_id: sol", "vacuum.set_fan_speed", "set_fan_speed par label_id"),
        ("device_id: abc", "vacuum.start", "start par device_id"),
        ("area_id: etage", "vacuum.return_to_base", "return_to_base par area_id"),
    ):
        c.viole(check_lovelace({"18_lovelace/d.yaml":
                                "tap_action:\n  action: call-service\n"
                                f"  service: {service}\n  target: {{{cible}}}\n"
                                "  data: {command: app_segment_clean, "
                                "params: [{segments: [21], repeat: 2}]}\n"}),
                "nom de service", f"F3/CI-7 {libelle}")
    c.viole(check_lovelace({"18_lovelace/e.yaml":
                            "  perform_action: vacuum.stop\n  target: {device_id: z}\n"}),
            "nom de service", "F3/CI-7 perform_action")

    # ---- ASP-CI-8 : référentiel technique --------------------------------
    AUD8 = ("| `0_16` | `Salon` | RDC |\n| `0_18` | `Entrée` | RDC |\n"
            "| `1_16` | `Palier` | Étage |\n"
            "| `2_17` | `Ext` | Annexe |\n| `2_18` | `Chambre1` | Annexe |\n"
            "| **0** | `RDC` | 2 |\n| **1** | `Étage ` | 1 |\n"
            "| **2** | `Annexe` | 3 |\n")

    # Clauses de bornage (M-2), retirables une à une, avec leurre optionnel.
    CL21 = {
        "cardinalite": "> - **Ni une confirmation par cardinalité.** Compter les "
                       "pièces ne confirme rien : inclusion nominale exigée.\n",
        "autorite": "> - **Ni une autorité métier.** La vérité de désignation "
                    "reste le §2.\n",
        "ui": "> - **Ni une donnée d'interface.** L'UI expose les libellés "
              "canoniques Arsenal.\n"}
    CL5 = {
        "usages": "| Écrire la sélection de carte | Option exacte | §2.1 |\n"
                  "| Confirmer la sélection par relecture | Option exacte | §2.1 |\n"
                  "| Confirmer les pièces exposées de la carte | Noms | §2.1 |\n",
        "litterale": "elle est stricte : la comparaison est **littérale**, "
                     "jamais approchée.\n"}
    CL6 = {
        "cond3": "| 3 | La sélection est confirmée par relecture, par "
                 "comparaison **littérale** à cette option | `X` |\n",
        "cond4": "| 4 | Les pièces exposées **contiennent l'intégralité** des "
                 "segments V1 (§2, §2.1) — voir §3.1 | `X` |\n",
        "inclusion": "> **Comment l'inclusion se constate.** Confrontation aux "
                     "noms de §2.1 — comparaison **littérale**.\n"}

    def t02t(opt1="`Étage `", nom="`Salon`", idx="16", statut17="non commandable",
             garage="| — | `Garage` | non commandable |", metier_extra="",
             tech_extra="", metier_roboro="`Salon`", retirer=(), leurre=False):
        metier = ("## 2. Table canonique des segments\n"
                  f"| `0_16` | **Séjour** | {metier_roboro} |\n"
                  "| `0_18` | **Entrée** | — |\n"
                  "| `1_16` | **Palier** | — |\n") + metier_extra
        b21 = "".join(v for k, v in CL21.items() if k not in retirer)
        b5 = "".join(v for k, v in CL5.items() if k not in retirer)
        # Leurre : la clause retirée reparaît dans une SECTION NON NORMATIVE.
        renvois = "## Renvois\n" + ("".join(CL21.get(k, "") + CL5.get(k, "")
                                            for k in retirer) if leurre else "")
        return (metier +
                "### 2.1 Table technique\n"
                "| `0` | `RDC` | commandable |\n"
                f"| `1` | {opt1} | commandable |\n"
                "| `2` | `Annexe` | commandable |\n"
                f"{garage}\n"
                f"| `0_16` | `{idx}` | {nom} | commandable |\n"
                "| `0_18` | `18` | `Entrée` | commandable |\n"
                "| `1_16` | `16` | `Palier` | commandable |\n"
                f"| `2_17` | `17` | `Ext` | {statut17} |\n"
                "| `2_18` | `18` | `Chambre1` | non commandable |\n"
                f"{tech_extra}{b21}"
                "\n## 3. Périmètres\n"
                "\n## 5. Règle de restitution des libellés\n" + b5 +
                "\n" + renvois)

    def t06t(retirer=(), leurre=False):
        c3 = "".join(v for k, v in CL6.items()
                     if k in ("cond3", "cond4") and k not in retirer)
        inc = CL6["inclusion"] if "inclusion" not in retirer else ""
        renvois = "## Renvois\n" + ("".join(CL6.get(k, "") for k in retirer)
                                    if leurre else "")
        return ("## 3. Conditions de satisfaction — dans cet ordre\n" + c3 +
                "\n### 3.1 La condition 4 est une inclusion\n" + inc +
                "\n## 4. Suite\n\n" + renvois)

    c.conforme(check_referentiel_technique(t02t(), t06t(), AUD8), "CI-8 conforme")
    c.viole(check_referentiel_technique(t02t(opt1="`Étage`"), t06t(), AUD8),
            "LITTÉRALE", "CI-8 espace finale supprimée")
    c.viole(check_referentiel_technique(t02t(nom="`Sallon`"), t06t(), AUD8),
            "l'audit atteste", "CI-8 nom Roborock falsifié")
    c.viole(check_referentiel_technique(t02t(idx="17"), t06t(), AUD8),
            "index natif", "CI-8 index natif dérivé")
    c.viole(check_referentiel_technique(t02t(statut17="commandable"), t06t(), AUD8),
            "attendu `non commandable`", "CI-8 promotion de 2_17")
    c.viole(check_referentiel_technique(
        t02t(metier_extra="| `2_17` | **Extérieur** | — |\n"), t06t(), AUD8),
        "promu(s) au référentiel métier", "CI-8 2_17 promu côté métier")
    c.viole(check_referentiel_technique(
        t02t(garage="| `3` | `Garage` | non commandable |"), t06t(), AUD8),
        "porte un index", "CI-8 Garage rendu adressable")
    c.viole(check_referentiel_technique(t02t(garage=""), t06t(), AUD8),
            "non commandable", "CI-8 Garage absent")
    # Falsification COHÉRENTE : les deux tables internes mentent ENSEMBLE.
    c.viole(check_referentiel_technique(
        t02t(nom="`Sallon`", metier_roboro="`Sallon`"), t06t(), AUD8),
        "l'audit atteste", "CI-8 falsification cohérente des deux tables")
    c.viole(check_referentiel_technique(
        t02t(tech_extra="| `0_99` | `99` | `Cuisine` | commandable |\n"),
        t06t(), AUD8),
        "ABSENT de l'audit", "CI-8 segment inventé")
    c.viole(check_referentiel_technique(t02t(), t06t(), ""),
            "introuvable dans l'audit", "CI-8 audit absent")
    c.viole(check_referentiel_technique("## 2. Table\n| `0_16` | **Séjour** |\n",
                                        t06t(), AUD8),
            "introuvable", "CI-8 §2.1 absent")
    # Séparation MÉCANIQUE : une table technique au format métier est refusée.
    c.viole(check_referentiel_technique(
        t02t().replace("| `0_16` | `16` | `Salon` | commandable |",
                       "| `0_16` | **Salon** | `16` |"), t06t(), AUD8),
        "parseur du référentiel MÉTIER", "CI-8 séparation typographique seule")

    # ---- M-2 : bornage de l'exception cartographique, clause par clause ---
    for cle, libelle in (("cardinalite", "confirmation par cardinalité"),
                         ("autorite", "autorité métier"),
                         ("ui", "donnée d'interface"),
                         ("usages", "table des trois usages"),
                         ("litterale", "comparaison littérale (02 §5)")):
        c.viole(check_referentiel_technique(t02t(retirer=(cle,)), t06t(), AUD8),
                "clause de bornage absente", f"M-2 {libelle} supprimée")
        # LEURRE : la clause reparaît dans « ## Renvois » — non normatif.
        c.viole(check_referentiel_technique(
            t02t(retirer=(cle,), leurre=True), t06t(), AUD8),
            "DANS cette section", f"M-2 {libelle} déplacée en renvoi")
    for cle, libelle in (("cond3", "condition 3 littérale"),
                         ("cond4", "condition 4 fondée sur §2.1"),
                         ("inclusion", "mécanisme d'inclusion nominale")):
        c.viole(check_referentiel_technique(t02t(), t06t(retirer=(cle,)), AUD8),
                "clause de bornage absente", f"M-2 {libelle} supprimée")
        c.viole(check_referentiel_technique(
            t02t(), t06t(retirer=(cle,), leurre=True), AUD8),
            "DANS cette section", f"M-2 {libelle} déplacée en renvoi")

    # ---- i-2 : cohérence PARTITION_ATTENDUE ↔ IMAGE_ATTENDUE -------------
    c.conforme(coherence_ancres(), "i-2 ancres cohérentes")
    c.viole(coherence_ancres(
        partition={**PARTITION_ATTENDUE, "R": PARTITION_ATTENDUE["R"] | {"idle"}}),
        "n'a AUCUNE image", "i-2 état ajouté à la partition sans image")
    c.viole(coherence_ancres(image={**IMAGE_ATTENDUE, "idle": "charge"}),
            "AUCUNE classe", "i-2 image sans appartenance à la partition")
    c.viole(coherence_ancres(partition={
        "R": PARTITION_ATTENDUE["R"] - {"charging"},
        "A": PARTITION_ATTENDUE["A"] | {"charging"},
        "E": PARTITION_ATTENDUE["E"]}),
        "DÉPLACEMENT", "i-2 état déplacé entre classes à image inchangée")

    # ---- ASP-CI-9 : dix états canoniques ---------------------------------
    def t08e(codes=None, image=None, extra="", refus="ETAT_NON_QUALIFIE",
             distinctions="ROBOT_INDISPONIBLE / ERREUR_EQUIPEMENT",
             admis="**repos admissible au lancement**", ouverture=True,
             inv44=True, leurre=""):
        codes = codes or list(ETATS_CANONIQUES)
        image = image or dict(IMAGE_ATTENDUE)
        lignes = "".join(
            f"| **{code}** | `{code}` | "
            + (f"sens {admis}" if code == "repos_hors_base" else "sens")
            + " |\n" for code in codes)
        par_code: dict[str, list[str]] = {}
        for etat, code in image.items():
            par_code.setdefault(code, []).append(etat)
        img = "".join(
            f"> | **A** | {' · '.join(f'`{e}`' for e in etats)} | `{code}` |\n"
            for code, etats in par_code.items())
        img += f"> | **N** | toute autre valeur | `{CODE_CANONIQUE_CLASSE_N}` |\n"
        tete = ("Le domaine distingue **dix** situations, qui ne se confondent "
                "jamais :\n" if ouverture else "Le domaine distingue plusieurs "
                "situations :\n")
        decl = ("> **`ASP-INV-44`** — Ces dix états sont **exposés "
                "distinctement**.\n" if inv44 else
                "> **`ASP-INV-44`** — Ces états sont **exposés distinctement**.\n")
        return ("## 1. États canoniques du domaine\n" + tete + lignes + extra
                + img + decl + leurre
                + f"refus {refus} ; ni {distinctions}\n" + "\n## 2. Autorité\n")

    t11e = ("3. **Restituer les états canoniques distinctement** — les **dix** "
            "du chapitre 08.\n")
    t12e = ("| `‹etat_canonique›` | L'état du domaine parmi les **dix** du "
            "chapitre 08 |\n")
    c.conforme(check_etats_canoniques(t08e(), t11e, t12e), "CI-9 conforme")
    c.viole(check_etats_canoniques(
        t08e(codes=[x for x in ETATS_CANONIQUES if x != "repos_hors_base"]),
        t11e, t12e), "ABSENT", "CI-9 état canonique retiré")
    c.viole(check_etats_canoniques(t08e(extra="| **Onzième** | `onzieme` | s |\n"),
                                   t11e, t12e),
            "AJOUTÉ", "CI-9 onzième état")
    c.viole(check_etats_canoniques(
        t08e(extra="| **Repos** | `repos_hors_base` | doublon |\n"), t11e, t12e),
        "doublon", "CI-9 synonyme")
    c.viole(check_etats_canoniques(
        t08e(image={**IMAGE_ATTENDUE, "charger_disconnected": "charge"}),
        t11e, t12e), "attendu `repos_hors_base`", "CI-9 image charger_disconnected")
    c.viole(check_etats_canoniques(
        t08e().replace(f"| **N** | toute autre valeur | `{CODE_CANONIQUE_CLASSE_N}` |",
                       "| **N** | toute autre valeur | `indisponibilite` |"),
        t11e, t12e), "classe N", "CI-9 classe N détournée")
    c.viole(check_etats_canoniques(t08e(refus="néant"), t11e, t12e),
            "ne relie pas", "CI-9 lien refus rompu")
    c.viole(check_etats_canoniques(t08e(distinctions="rien"), t11e, t12e),
            "ne distingue pas", "CI-9 confusion indisponibilité")
    c.viole(check_etats_canoniques("", t11e, t12e),
            "introuvable", "CI-9 chapitre absent")

    # ---- M-1 : compteurs et admissibilité ancrés, LEURRES compris ---------
    LEURRE_DIX = "Par ailleurs, dix segments sont observés, dont un admissible.\n"
    c.viole(check_etats_canoniques(t08e(ouverture=False), t11e, t12e),
            "phrase d'ouverture", "M-1 compteur 08 (ouverture) faux")
    c.viole(check_etats_canoniques(
        t08e(ouverture=False, leurre=LEURRE_DIX), t11e, t12e),
        "phrase d'ouverture", "M-1 compteur 08 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(inv44=False), t11e, t12e),
            "ASP-INV-44", "M-1 compteur 08 (ASP-INV-44) faux")
    c.viole(check_etats_canoniques(
        t08e(inv44=False, leurre=LEURRE_DIX), t11e, t12e),
        "ASP-INV-44", "M-1 ASP-INV-44 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(), "les états, au nombre de dix.\n", t12e),
            "11 §3", "M-1 compteur 11 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(), t11e, "un rôle parmi dix autres |\n"),
            "12 §2.3", "M-1 compteur 12 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(admis="sens ordinaire"), t11e, t12e),
            "DANS SA LIGNE", "M-1 admissibilité perdue")
    c.viole(check_etats_canoniques(
        t08e(admis="sens ordinaire", leurre=LEURRE_DIX), t11e, t12e),
        "DANS SA LIGNE", "M-1 admissibilité perdue malgré un leurre « admissible »")
    c.viole(check_etats_canoniques(t08e(), "les huit du chapitre", t12e),
            "HUIT", "CI-9 renvoi 11 non réaligné")
    c.viole(check_etats_canoniques(t08e(), t11e, "les dix — jadis huit états"),
            "HUIT", "CI-9 renvoi 12 non réaligné")

    # ---- ASP-CI-10 : fenêtres temporelles --------------------------------
    def t07f(conf=30, trans=60, portee_conf="étapes 7, 8 et 10",
             portee_trans="transition de démarrage — étape 13",
             helper="ni helper", fallback="aucun fallback", seq=True,
             exemption=True):
        etapes = "".join(
            f"| **{e}** | Confirmer, sous **{conf} s** | refus |\n"
            for e in ETAPES_CONFIRMATION) if seq else ""
        # La fixture porte la clause d'exemption comme le contrat réel : sans
        # elle, ASP-CI-10 signale l'ancre manquante — et c'est précisément ce
        # qu'une mutation ci-dessous vérifie.
        note = f"> {CLAUSE_APPEL_07}, pas une borne.\n" if exemption else ""
        return (etapes + "### 3.1 Constantes\n"
                f"> | **Fenêtre de confirmation** | **{conf} s** | {portee_conf} |\n"
                f"> | **Fenêtre de transition** | **{trans} s** | {portee_trans} |\n"
                f"> {helper} ; {fallback}\n" + note + "\n## 4. Suite\n")

    def t09f(fenetre_sur=CODE_TRANSITION, note=True):
        lignes = {
            "CANAL_INDISPONIBLE": "La demande n'est pas parvenue",
            "COMMANDE_REJETEE": "La commande a été refusée",
            CODE_TRANSITION: "aucune transition de démarrage observée",
            "MISSION_INTERROMPUE": "arrêt avant terme"}
        corps = "".join(
            f"| `{code}` | {texte}"
            + (" dans la fenêtre de **60 s**" if code == fenetre_sur else "")
            + " | — |\n" for code, texte in lignes.items())
        # Les deux chaînes restent présentes AILLEURS dans le chapitre :
        # seule leur ASSOCIATION sur la ligne fait foi (m-1).
        queue = ("> Rappel : la transition de démarrage et la fenêtre de 60 s "
                 "sont traitées au chapitre 07.\n")
        if note:
            queue += f"> {NOTE_FENETRE_09}, et 30 s pour les réglages.\n"
        return "## 3. Catalogue des échecs\n" + corps + queue + "\n## 4. Qualité\n"

    t12f = "| **Helper temporel** | **Aucun.** |"
    t13f = ("### `ARB-3` — fenêtres\nrévision conjointe contrat + checker + "
            "runtime\n### `ARB-4`\n")
    T08F = ("## 3. Témoin\n| Robot roulant | `off` | Le robot se déplace — "
            + CLAUSE_TERRAIN_08 + " |\n")

    def corpus(t07=None, t09=None, t12=t12f, t13=t13f, t08=T08F, **autres):
        base = {"07_moteur_de_mission.md": t07 if t07 is not None else t07f(),
                "09_refus_et_diagnostics.md": t09 if t09 is not None else t09f(),
                "12_identifiants_a_fournir.md": t12,
                "13_hors_perimetre_arbitrages_et_questions_ouvertes.md": t13,
                FICHIER_TERRAIN_08: t08}
        base.update(autres)
        return base

    c.conforme(check_fenetres(corpus()), "CI-10 conforme")
    # Inversion PURE : l'ensemble des valeurs reste {30, 60}, seule
    # l'affectation ment. C'est le contrôle de PORTÉE qui la lève.
    c.viole(check_fenetres(corpus(t07=t07f(conf=60, trans=30))),
            "INVERSÉES ou confondues", "CI-10 inversion 30/60")
    c.viole(check_fenetres(corpus(
        t07=t07f(portee_trans="transition — étapes 8 et 13"))),
        "INVERSÉES ou confondues", "CI-10 portées confondues")
    c.viole(check_fenetres(corpus(t07=t07f(trans=45))),
            "attendu exactement", "CI-10 disparition d'une fenêtre")
    c.viole(check_fenetres(corpus(t07=t07f(helper="réglable par input_number"))),
            "helper", "CI-10 helper temporel réintroduit")
    c.viole(check_fenetres(corpus(t07=t07f(fallback="repli admis"))),
            "fallback", "CI-10 fallback ajouté")
    c.viole(check_fenetres(corpus(t12="aucune ligne")),
            "chapitre 12", "CI-10 helper non acté au 12")
    c.viole(check_fenetres(corpus(
        t13="### `ARB-3` — fenêtres\nrévisable à chaud\n### `ARB-4`\n")),
        "CONJOINTE", "CI-10 révision conjointe perdue")
    c.viole(check_fenetres(corpus(t07=t07f(portee_conf="étapes 6 et 8"))),
            "étape 10", "CI-10 étape de confirmation non bornée")
    c.viole(check_fenetres(corpus(t07=t07f(seq=False))),
            "ABSENTE de la séquence", "CI-10 étape de confirmation supprimée")
    c.viole(check_fenetres(corpus(t07=t07f().replace(
        "| **8** | Confirmer, sous **30 s** | refus |",
        "| **8** | Confirmer | refus |"))),
        "ne porte pas la fenêtre", "CI-10 étape non bornée")
    c.viole(check_fenetres(corpus(t07="")),
            "introuvables", "CI-10 §3.1 absent")

    # ---- m-1 : association 60 s ↔ transition ↔ TRANSITION_NON_OBSERVEE ----
    c.viole(check_fenetres(corpus(t09=t09f(fenetre_sur="COMMANDE_REJETEE"))),
            "ne porte pas la fenêtre",
            "m-1 fenêtre déplacée sur COMMANDE_REJETEE")
    c.viole(check_fenetres(corpus(t09=t09f(fenetre_sur="COMMANDE_REJETEE"))),
            "elle ne qualifie QUE", "m-1 fenêtre affectée à un autre code")
    c.viole(check_fenetres(corpus(t09=t09f(note=False))),
            "ne relie plus explicitement", "m-1 note d'association supprimée")
    c.viole(check_fenetres(corpus(t09="## 4. Qualité\n")),
            "catalogue des échecs introuvable", "m-1 catalogue absent")

    # ---- M-3 : balayage des 14 chapitres, exemption bornée ---------------
    for chapitre in ("01_finalite_et_perimetre.md",
                     "02_referentiel_cartes_et_pieces.md",
                     "06_integrite_mono_carte.md",
                     "11_frontiere_ui.md",
                     "12_identifiants_a_fournir.md"):
        c.viole(check_fenetres(corpus(**{chapitre: "temporisation de 90 s.\n"})),
                "durée(s) concurrente(s)", f"M-3 durée concurrente dans {chapitre[:2]}")
    c.viole(check_fenetres(corpus(t08=T08F + "attente de 15 s avant relecture.\n")),
            "durée(s) concurrente(s)", "M-3 durée concurrente dans 08")
    c.viole(check_fenetres(corpus(t12=t12f + "\nrepli à 120 secondes.\n")),
            "durée(s) concurrente(s)", "M-3 durée concurrente dans 12 (en toutes lettres)")
    # La clause terrain 53 s / 25 s n'est PAS une allowlist de nombres :
    # altérée, elle cesse d'être reconnue et ses durées redeviennent visibles.
    c.viole(check_fenetres(corpus(t08=T08F.replace("53 s puis 25 s", "53 s ou 25 s"))),
            "durée(s) concurrente(s)", "M-3 clause terrain altérée")
    c.viole(check_fenetres(corpus(t08=T08F.replace("53 s puis 25 s", "53 s ou 25 s"))),
            "n'est plus ancrée", "M-3 exemption désancrée")
    c.viole(check_fenetres(corpus(t08="## 3. Témoin\naucune observation.\n")),
            "est absente", "M-3 clause terrain supprimée")

    # ---- Franchissement de ligne et de section — aucun motif ne déborde ---
    # LIGNE_REPOS est ancrée par `$` en mode M : le motif placé à la ligne
    # SUIVANTE, ou ailleurs dans le chapitre, ne satisfait pas la garde.
    c.viole(check_etats_canoniques(
        t08e(admis="sens ordinaire", leurre=MOTIF_ADMISSIBLE + "\n"), t11e, t12e),
        "DANS SA LIGNE", "franchissement — admissibilité hors de sa ligne")
    # Le motif du chapitre 12 ne se satisfait pas d'une répartition sur 2 lignes.
    c.viole(check_etats_canoniques(
        t08e(), t11e,
        "| `‹etat_canonique›` | L'état du domaine\nparmi les **dix** du 08 |\n"),
        "12 §2.3", "franchissement — motif 12 réparti sur deux lignes")
    # Une clause du §5 déplacée DANS le §2.1 ne satisfait pas la garde du §5.
    c.viole(check_referentiel_technique(
        t02t(retirer=("litterale",)).replace(
            "\n## 3. Périmètres\n", CL5["litterale"] + "\n## 3. Périmètres\n"),
        t06t(), AUD8),
        "02 §5", "franchissement — clause du §5 déplacée dans le §2.1")
    # Une clause du 06 §3.1 remontée dans le §3 ne satisfait pas la garde du §3.1.
    c.viole(check_referentiel_technique(
        t02t(), t06t(retirer=("inclusion",)).replace(
            "\n### 3.1", CL6["inclusion"] + "\n### 3.1"), AUD8),
        "06 §3.1", "franchissement — clause du §3.1 remontée dans le §3")

    # ---- m-1 : l'association ne franchit pas la ligne --------------------
    c.viole(check_fenetres(corpus(t09=t09f(fenetre_sur=None))),
            "ne porte pas la fenêtre",
            "m-1 fenêtre à la ligne suivante, hors de la ligne de catalogue")

    # ---- M-3 : blocs clôturés neutralisés, et neutralisation non vacuous --
    FENCE = "```yaml\nwait_template: 90 s\n```\n"
    c.conforme(check_fenetres(corpus(
        **{"01_finalite_et_perimetre.md": strip_fences(FENCE)})),
        "M-3 durée dans un bloc clôturé — neutralisée")
    c.viole(check_fenetres(corpus(
        **{"01_finalite_et_perimetre.md": "wait_template: 90 s\n"})),
        "durée(s) concurrente(s)",
        "M-3 même durée HORS bloc — détectée (neutralisation non vacante)")
    # Une durée ajoutée SUR LA LIGNE de la clause terrain reste visible :
    # l'exemption retire la clause exacte, pas la ligne ni son voisinage.
    c.viole(check_fenetres(corpus(
        t08=T08F.replace(CLAUSE_TERRAIN_08, CLAUSE_TERRAIN_08 + ", puis 15 s"))),
        "durée(s) concurrente(s)",
        "M-3 durée ajoutée à côté des observations 53 s / 25 s")

    # R1 — les motifs de durée et d'étape ne franchissent pas la ligne.
    assert not DUREE.search("90\ns"), "DUREE franchit la ligne"
    assert DUREE.findall("90 s") == ["90"], "DUREE ne lit plus une durée"
    assert not ETAPES_CITEES.search("étape\n6"), "ETAPES_CITEES franchit la ligne"
    assert etapes_citees("étapes 7, 8 et 10") == {"7", "8", "10"}
    assert etapes_citees("étape 13 (§4, `ASP-INV-38`)") == {"13"}, \
        "un chiffre hors mention d'étape ne doit pas être lu comme une étape"
    c.conforme([], "R1 motifs bornés à la ligne (5 assertions)")

    # ---- i-2 : retrait d'un état de l'image canonique --------------------
    c.viole(coherence_ancres(
        image={k: v for k, v in IMAGE_ATTENDUE.items() if k != "docking"}),
        "AUCUNE image", "i-2 état retiré de l'image canonique")

    # ═════════════════════════════════════════════════════════════
    # RUNTIME L1 — ASP-CI-11 … ASP-CI-21
    # Les mutations portent sur l'ARTEFACT RÉEL, pas sur une maquette : un
    # contrôle qui ne se déclenche que sur une fixture inventée ne prouve rien
    # du fichier qui part en production.
    # ═════════════════════════════════════════════════════════════
    import copy

    rt0 = load_runtime()
    attendus_rt = set(RUNTIME_FICHIERS) | set(RUNTIME_L2_FICHIERS)
    assert set(rt0) == attendus_rt, \
        f"runtime introuvable : {sorted(attendus_rt - set(rt0))}"
    mot0 = yaml.safe_load(rt0[RUNTIME_MOTEUR])
    hlp0 = yaml.safe_load(rt0[RUNTIME_HELPERS])
    corps0 = mot0[ID_MOTEUR]
    etapes0 = _aplatir(corps0["sequence"])
    depot0 = load_yaml_depot()
    doc0 = sans_clotures(load_domain())
    t02r = doc0["02_referentiel_cartes_et_pieces.md"]
    t03r = doc0["03_profils_metier.md"]
    t09r = doc0[FICHIER_CATALOGUE]
    audit0 = strip_fences(AUDIT.read_text(encoding="utf-8", errors="ignore"))

    def mot_txt(vieux, neuf, n=1):
        """Mutation TEXTUELLE du moteur réel."""
        r = dict(rt0)
        assert vieux in r[RUNTIME_MOTEUR], f"ancre absente : {vieux!r}"
        r[RUNTIME_MOTEUR] = r[RUNTIME_MOTEUR].replace(vieux, neuf, n)
        return r

    def mot_yml(mutation):
        """Mutation STRUCTURELLE du moteur réel — renvoie (corps, étapes)."""
        m = copy.deepcopy(mot0)
        mutation(m[ID_MOTEUR])
        return m, _aplatir(m[ID_MOTEUR]["sequence"])

    def vars0(m):
        return next(s["variables"] for s in m["sequence"]
                    if isinstance(s, dict) and "variables" in s
                    and "referentiel" in s["variables"])

    # ---- ASP-CI-11 : écrivain unique -------------------------------------
    c.conforme(check_ecrivain_unique(mot0, rt0, depot0), "CI-11 conforme")
    m, _ = mot_yml(lambda s: s.__setitem__("mode", "restart"))
    c.viole(check_ecrivain_unique(m, rt0, depot0),
            "mode: single", "CI-11 mode concurrent autorisé")
    m, _ = mot_yml(lambda s: s["fields"].pop("passages"))
    c.viole(check_ecrivain_unique(m, rt0, depot0),
            "quatre champs", "CI-11 intention non atomique")
    c.viole(check_ecrivain_unique(
        mot0, rt0, dict(depot0, **{"11_automations/x.yaml":
                                   f"  value: {ID_VERDICT}\n"})),
        "n'est mentionnable que par ses trois écrivains",
        "CI-11 quatrième mention du verdict")
    c.viole(check_ecrivain_unique(
        mot0, rt0, dict(depot0, **{"11_automations/x.yaml":
                                   f"  value: {ID_TRACE}\n"})),
        "n'a qu'UN écrivain, le moteur", "CI-11 second lecteur de la trace")
    c.viole(check_ecrivain_unique(
        mot0, rt0, dict(depot0, **{"11_automations/x.yaml":
                                   "    - action: vacuum.stop\n"})),
        "seuls le moteur et le script de conduite",
        "CI-11 commande concurrente du robot")
    c.viole(check_ecrivain_unique(
        mot0, {**rt0, RUNTIME_GARDE: rt0[RUNTIME_GARDE].replace(
            NATIF_SESSION, "binary_sensor.autre_chose")}, depot0),
        "ignore le témoin", "CI-11 garde et moteur divergents")
    c.viole(check_ecrivain_unique(
        mot0, {**rt0, RUNTIME_GARDE: rt0[RUNTIME_GARDE].replace(
            "'ok'", "'OK'")}, depot0),
        "valeur nominale `ok`", "CI-11 valeur nominale du dock altérée")

    # ---- ASP-CI-12 / ASP-CI-13 : charge utile et passages -----------------
    c.conforme(check_charge_utile(etapes0), "CI-12/13 conforme")

    def _params(step_mut):
        m = copy.deepcopy(mot0)
        for s in _aplatir(m[ID_MOTEUR]["sequence"]):
            if _service(s) == SVC_COMMANDE:
                step_mut(s)
        return _aplatir(m[ID_MOTEUR]["sequence"])

    c.viole(check_charge_utile(_params(
        lambda s: s["data"].__setitem__(
            "params", "{{ dict(segments=indices) }}"))),
        "forme enveloppée", "CI-12 charge utile NUE")
    c.viole(check_charge_utile(_params(
        lambda s: s["data"].__setitem__(
            "params", "{{ [dict(segments=indices, repeat=passages_int)] }}"))),
        "×1 exige l'ABSENCE", "CI-13 repeat: 1 émis pour ×1")
    c.viole(check_charge_utile(_params(
        lambda s: s["data"].__setitem__(
            "params",
            "{{ [dict(segments=indices, repeat=passages_int - 1)]"
            " if passages_int > 1 else [dict(segments=indices)] }}"))),
        "×2 exige `repeat: 2`", "CI-13 convention zonée transposée")
    c.viole(check_charge_utile(_params(
        lambda s: s["data"].__setitem__("command", "app_zoned_clean"))),
        "app_segment_clean", "CI-12 commande protocolaire détournée")
    doublon = copy.deepcopy(mot0)
    doublon[ID_MOTEUR]["sequence"].append(
        {"action": SVC_COMMANDE, "target": {"entity_id": NATIF_VACUUM},
         "data": {"command": COMMANDE_SEGMENTEE, "params": "{{ [] }}"}})
    c.viole(check_charge_utile(_aplatir(doublon[ID_MOTEUR]["sequence"])),
            "EXACTEMENT un", "CI-17 seconde commande de démarrage")

    # ---- ASP-CI-14 : voies interdites ------------------------------------
    c.conforme(check_voies_interdites(rt0), "CI-14 conforme")
    for interdit in ("app_zoned_clean", "vacuum.start", "vacuum.clean_area"):
        c.viole(check_voies_interdites(
            mot_txt("      command: app_segment_clean",
                    f"      command: {interdit}")),
            "voie zonée ou démarreur interdit", f"CI-14 {interdit}")

    # ---- ASP-CI-15 : le mode dérivé ne s'écrit jamais --------------------
    c.conforme(check_mode_jamais_ecrit(etapes0), "CI-15 conforme")
    m2 = copy.deepcopy(mot0)
    for s in _aplatir(m2[ID_MOTEUR]["sequence"]):
        if _service(s) == SVC_EAU and NATIF_EAU in _cibles(s):
            s["target"]["entity_id"] = NATIF_MODE
    c.viole(check_mode_jamais_ecrit(_aplatir(m2[ID_MOTEUR]["sequence"])),
            "est la CIBLE", "CI-15 écriture du mode dérivé")

    # ---- ASP-CI-16 / ASP-CI-17 : ordre et revérification -----------------
    c.conforme(check_ordre_sequence(mot0[ID_MOTEUR]["sequence"]),
               "CI-16/17 conforme")
    inv = copy.deepcopy(mot0)
    seqi = inv[ID_MOTEUR]["sequence"]
    i_eau = next(i for i, s in enumerate(seqi)
                 if _service(s) == SVC_EAU and NATIF_EAU in _cibles(s))
    i_asp = next(i for i, s in enumerate(seqi) if _service(s) == SVC_ASPIRATION)
    seqi[i_eau], seqi[i_asp] = seqi[i_asp], seqi[i_eau]
    c.viole(check_ordre_sequence(seqi),
            "ordre non conforme", "CI-16 aspiration écrite avant l'eau")
    sans_g2 = copy.deepcopy(mot0)
    sans_g2[ID_MOTEUR]["sequence"] = [
        s for s in sans_g2[ID_MOTEUR]["sequence"]
        if not (isinstance(s, dict) and "variables" in s
                and any(k.startswith("g2_") for k in s["variables"]))]
    c.viole(check_ordre_sequence(sans_g2[ID_MOTEUR]["sequence"]),
            "aucune relecture des gardes", "CI-16 revérification supprimée")
    partiel = copy.deepcopy(mot0)
    for s in partiel[ID_MOTEUR]["sequence"]:
        if isinstance(s, dict) and "variables" in s and "g2_session" in s["variables"]:
            s["variables"].pop("g2_session")
    c.viole(check_ordre_sequence(partiel[ID_MOTEUR]["sequence"]),
            "revérification tardive omet", "CI-16 revérification partielle")

    # ---- ASP-CI-18 : vocabulaire de verdict ------------------------------
    c.conforme(check_vocabulaire_verdict(mot0[ID_MOTEUR]["sequence"], rt0),
               "CI-18 conforme")
    c.viole(check_vocabulaire_verdict(
        _aplatir(yaml.safe_load(mot_txt(
            'value: "REFUS/SESSION_INACHEVEE"',
            'value: "REFUS/SESSION_BIZARRE"')[RUNTIME_MOTEUR])[ID_MOTEUR]["sequence"]),
        rt0),
        "hors de son ensemble de dix-huit valeurs",
        "CI-18 valeur hors vocabulaire")
    r_sup = mot_txt('value: "LANCEE/DEMARRAGE_OBSERVE"',
                    'value: "EMISSION/COMMANDE_ACCEPTEE"')
    c.viole(check_vocabulaire_verdict(
        _aplatir(yaml.safe_load(r_sup[RUNTIME_MOTEUR])[ID_MOTEUR]["sequence"]),
        r_sup),
        "n'écrit jamais", "CI-18 valeur de W1 inatteignable")
    r_rej = mot_txt('value: "COMMANDE/ISSUE_NON_ETABLIE"',
                    'value: "ECHEC/COMMANDE_REJETEE"')
    c.viole(check_vocabulaire_verdict(
        _aplatir(yaml.safe_load(r_rej[RUNTIME_MOTEUR])[ID_MOTEUR]["sequence"]),
        r_rej),
        "affirmer un rejet avant", "CI-18 verdict de rejet anticipé")
    tard = copy.deepcopy(mot0)
    sq = tard[ID_MOTEUR]["sequence"]
    i_nc = next(i for i, s in enumerate(sq)
                if _service(s) == "input_text.set_value"
                and (s.get("data") or {}).get("value")
                == "COMMANDE/ISSUE_NON_ETABLIE")
    i_cmd = next(i for i, s in enumerate(sq) if _service(s) == SVC_COMMANDE)
    sq.insert(i_cmd + 1, sq.pop(i_nc))
    c.viole(check_vocabulaire_verdict(sq, rt0),
            "AVANT l'émission", "CI-18 verdict non concluant posé trop tard")
    coe = copy.deepcopy(mot0)
    for s in coe[ID_MOTEUR]["sequence"]:
        if _service(s) == SVC_COMMANDE:
            s["continue_on_error"] = True
    # Mutation conservée à l'identique — seul le MOTIF change : l'interdiction
    # ne repose plus sur une lisibilité prétendument perdue (fausse :
    # `_log_exception` est appelé AVANT le test de `continue_on_error`), mais
    # sur l'absence de postcondition suffisante à l'émission.
    c.viole(check_vocabulaire_verdict(coe[ID_MOTEUR]["sequence"], rt0),
            "AUCUNE postcondition suffisante",
            "CI-18 continue_on_error sur l'émission")

    # ---- ASP-CI-19 : motif lisible total ---------------------------------
    c.conforme(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF]),
               "CI-19 conforme")
    c.viole(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF].replace(
        "'COMMANDE_REJETEE':", "'COMMANDE_REJETEE_X':")),
        "ne traduit pas", "CI-19 code du catalogue non traduit")
    c.viole(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF].replace(
        "'ISSUE_NON_ETABLIE':", "'AUTRE_CHOSE':")),
        "cycle de vie", "CI-19 valeur de cycle de vie non traduite")
    c.viole(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF].replace(
        '"Mission démarrée : le robot nettoie le périmètre demandé.",',
        '"Mission démarrée : le robot nettoie le segment 0_16 demandé.",')),
        "index de segment nu", "CI-19 index nu restitué")
    c.viole(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF].replace(
        '"Mission démarrée : le robot nettoie le périmètre demandé.",',
        '"Mission démarrée : le robot nettoie Salon comme demandé.",')),
        "libellé d'appareil", "CI-19 libellé Roborock restitué")
    c.viole(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF].replace(
        '"Mission démarrée : le robot nettoie le périmètre demandé.",',
        '"Mission démarrée, voir sensor.roborock_q7_max_etat pour le détail.",')),
        "mécanique interne", "CI-19 nom d'entité restitué")
    c.viole(check_motif_total(t09r, t02r, rt0[RUNTIME_MOTIF].replace(
        '"Mission démarrée : le robot nettoie le périmètre demandé.",',
        '"' + ("Mission démarrée. " * 20) + '",')),
        "borné à 255", "CI-19 motif au-delà de la capacité d'un capteur")

    # ---- ASP-CI-20 : constantes temporelles ------------------------------
    c.conforme(check_constantes_temporelles(rt0), "CI-20 conforme")
    c.viole(check_constantes_temporelles(
        mot_txt('timeout: "00:00:30"', 'timeout: "00:00:45"')),
        "durée(s) concurrente(s)", "CI-20 troisième durée introduite")
    c.viole(check_constantes_temporelles(
        mot_txt('timeout: "00:00:30"', 'timeout: "00:01:00"')),
        "fenêtres de confirmation", "CI-20 confirmation manquante")
    c.viole(check_constantes_temporelles(
        mot_txt('timeout: "00:01:00"', 'timeout: "00:00:30"')),
        "une seule fenêtre d'observation", "CI-20 observation supprimée")
    c.viole(check_constantes_temporelles(
        mot_txt('    - action: vacuum.send_command',
                '    - delay: "00:00:05"\n    - action: vacuum.send_command')),
        "porte `delay:`", "CI-20 temporisation hors contrat")
    c.viole(check_constantes_temporelles(
        mot_txt("passages_int: \"{{ passages | int }}\"",
                "passages_int: \"{{ states('input_number.aspirateur_x') | int }}\"")),
        "AUCUN réglage temporel", "CI-20 helper temporel réintroduit")

    # ---- ASP-CI-21 : concordance runtime ↔ contrat -----------------------
    c.conforme(check_concordance_runtime(corps0, rt0, hlp0, t02r, t03r, audit0),
               "CI-21 conforme")
    m, _ = mot_yml(lambda s: vars0(s)["referentiel"]["1"].__setitem__(
        "option", "Étage"))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "espace finale comprise", "CI-21 espace finale de `Étage ` perdue")
    m, _ = mot_yml(lambda s: vars0(s)["referentiel"]["0"]["segments"]["0_16"]
                   .__setitem__("index", 17))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "index natif", "CI-21 index natif dévié")
    m, _ = mot_yml(lambda s: vars0(s)["referentiel"]["2"]["segments"]
                   .__setitem__("2_17", {"index": 17, "libelle": "Ext"}))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "hors référentiel V1", "CI-21 segment non commandable promu")
    m, _ = mot_yml(lambda s: vars0(s)["referentiel"]["0"].__setitem__(
        "noms", ["Salon", "Entree", "WC RDC", "Cage d'escaliers"]))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "noms Roborock de la carte", "CI-21 nom Roborock approximé")
    m, _ = mot_yml(lambda s: vars0(s)["profils"]["aspiration_normale"]
                   .__setitem__("mode", "vac_and_mop"))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "mode dérivé du profil", "CI-21 mode dérivé incohérent")
    m, _ = mot_yml(lambda s: vars0(s)["profils"]["aspiration_turbo"]
                   .__setitem__("aspiration", FAN_SPEED_EXCLUE))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "exclu du domaine", "CI-21 `gentle` réintroduit")
    m, _ = mot_yml(lambda s: vars0(s).__setitem__(
        "indispo", ["unknown", "unavailable", "none"]))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "valeur NOMINALE", "CI-21 `none` confondu avec une indisponibilité")
    m, _ = mot_yml(lambda s: vars0(s).__setitem__(
        "classe_r", ["charger_disconnected", "charging", "idle"]))
    c.viole(check_concordance_runtime(m[ID_MOTEUR], rt0, hlp0, t02r, t03r, audit0),
            "classe R embarquée", "CI-21 classe de repos élargie")
    hlp_petit = copy.deepcopy(hlp0)
    hlp_petit[ID_TRACE.split(".", 1)[1]]["max"] = 50
    c.viole(check_concordance_runtime(corps0, rt0, hlp_petit, t02r, t03r, audit0),
            "sérialisation maximale", "CI-21 capacité de trace insuffisante")
    c.viole(check_concordance_runtime(
        corps0, {**rt0, RUNTIME_GARDE: rt0[RUNTIME_GARDE].replace(ID_GARDE, "autre")},
        hlp0, t02r, t03r, audit0),
        "attribution opérateur non respectée", "CI-21 identifiant renommé")

    # ═════════════════════════════════════════════════════════════
    # RUNTIME L1 — ASP-CI-22 … ASP-CI-25 : mutations PAR RENDU
    # Chacune réintroduit un défaut RÉEL que les contrôles structurels
    # laissaient passer. Les deux premières sont exactement les deux défauts
    # que ce lot revendique avoir évités : sans elles, la revendication
    # n'était adossée à aucune garde.
    # ═════════════════════════════════════════════════════════════
    t02r_2 = doc0["02_referentiel_cartes_et_pieces.md"]
    c.conforme(check_rendus_moteur(corps0, etapes0, t02r_2), "CI-22 conforme")
    c.conforme(check_etat_canonique_rendu(rt0[RUNTIME_ETAT]), "CI-23 conforme")
    c.conforme(check_garde_rendue(rt0[RUNTIME_GARDE]), "CI-24 conforme")
    c.conforme(check_branches_tardives(etapes0), "CI-25 conforme")

    # ---- ASP-CI-22 : le défaut de TRONCATURE, réintroduit -----------------
    scalaire = mot_txt(
        '              data: "{{ {\'option\': ctx_carte.option} }}"',
        '              data:\n                option: "{{ ctx_carte.option }}"')
    m_sc = yaml.safe_load(scalaire[RUNTIME_MOTEUR])[ID_MOTEUR]
    c.viole(check_rendus_moteur(m_sc, _aplatir(m_sc["sequence"]), t02r_2),
            "GABARIT rendu en bloc",
            "CI-22 `.strip()` — data de carte repassé en scalaires")

    # ---- ASP-CI-22 : la même chose, mais l'espace finale perdue en table --
    m_esp = copy.deepcopy(mot0)
    vars0(m_esp[ID_MOTEUR])["referentiel"]["1"]["option"] = "Étage"
    c.viole(check_rendus_moteur(m_esp[ID_MOTEUR],
                                _aplatir(m_esp[ID_MOTEUR]["sequence"]), t02r_2),
            "espace finale comprise",
            "CI-22 option de carte amputée de son espace finale")

    # ---- ASP-CI-22 : le défaut de RETYPAGE, réintroduit -------------------
    retype = mot_txt(
        '        ctx_carte: "{{ referentiel[carte | string] }}"',
        '        carte_cle: "{{ carte | string }}"\n'
        '        ctx_carte: "{{ referentiel[carte | string] }}"')
    m_rt = yaml.safe_load(retype[RUNTIME_MOTEUR])[ID_MOTEUR]
    c.viole(check_rendus_moteur(m_rt, _aplatir(m_rt["sequence"]), t02r_2),
            "retype", "CI-22 `_parse_result` — clé de carte rendue en scalaire")

    # ---- ASP-CI-22 : la garde de type de `segments` affaiblie -------------
    sans_map = mot_txt("or segments is string or segments is mapping",
                       "or segments is string")
    m_sm = yaml.safe_load(sans_map[RUNTIME_MOTEUR])[ID_MOTEUR]
    c.viole(check_rendus_moteur(m_sm, _aplatir(m_sm["sequence"]), t02r_2),
            "un mapping", "CI-22 mapping accepté pour une liste de segments")

    # ---- ASP-CI-23 : image canonique falsifiée ---------------------------
    c.viole(check_etat_canonique_rendu(rt0[RUNTIME_ETAT].replace(
        "else 'etat_non_qualifie' }}", "else 'repos_hors_base' }}")),
        "image contractuelle",
        "CI-23 fourre-tout de classe N promu en repos admissible")
    c.viole(check_etat_canonique_rendu(rt0[RUNTIME_ETAT].replace(
        "'repos_hors_base' if e == 'charger_disconnected'",
        "'charge' if e == 'charger_disconnected'")),
        "image obtenue", "CI-23 état de classe R déplacé dans l'image")
    c.viole(check_etat_canonique_rendu(rt0[RUNTIME_ETAT].replace(
        "{{ 'oui' if s == 'on' else 'non' if s == 'off' else 'indisponible' }}",
        "{{ 'oui' if s == 'on' else 'non' }}")),
        "ni `oui` ni `non`",
        "CI-23 indisponibilité de session rabattue sur `non`")

    # ---- ASP-CI-24 : garde neutralisée ------------------------------------
    lg = rt0[RUNTIME_GARDE].split("\n")
    i_g = next(k for k, l in enumerate(lg) if l.strip().startswith("state: >"))
    j_g = next(k for k in range(i_g + 1, len(lg))
               if lg[k].strip().startswith("attributes:"))
    c.viole(check_garde_rendue("\n".join(
        lg[:i_g] + ["      state: \"{{ 'on' }}\""] + lg[j_g:])),
        "garde divergente", "CI-24 garde remplacée par un `on` constant")
    c.viole(check_garde_rendue(rt0[RUNTIME_GARDE].replace(
        "and s == 'off')", "and s != 'jamais')")),
        "garde divergente", "CI-24 session ouverte n'interdit plus le feu vert")
    c.viole(check_garde_rendue(rt0[RUNTIME_GARDE].replace(
        "and ev == 'none' and ed == 'ok'", "and ev != 'jamais'")),
        "garde divergente", "CI-24 témoins d'erreur retirés de la garde")

    # ---- ASP-CI-25 : branches de refus tardives --------------------------
    sans_g2 = copy.deepcopy(mot0)
    for st in sans_g2[ID_MOTEUR]["sequence"]:
        if isinstance(st, dict) and "choose" in st and any(
                "g2_session" in str(o.get("conditions")) for o in st["choose"]):
            st["choose"] = [o for o in st["choose"]
                            if "g2_session" not in str(o.get("conditions"))]
    c.viole(check_branches_tardives(_aplatir(sans_g2[ID_MOTEUR]["sequence"])),
            "ne compare jamais",
            "CI-25 refus tardif SESSION_INACHEVEE supprimé")
    muet = copy.deepcopy(mot0)
    for st in muet[ID_MOTEUR]["sequence"]:
        if isinstance(st, dict) and "choose" in st and any(
                "g2_session" in str(o.get("conditions")) for o in st["choose"]):
            for o in st["choose"]:
                if "g2_session" in str(o.get("conditions")):
                    o["sequence"] = [s for s in o["sequence"]
                                     if not (isinstance(s, dict)
                                             and "stop" in s)]
    c.viole(check_branches_tardives(_aplatir(muet[ID_MOTEUR]["sequence"])),
            "n'arrête pas la séquence",
            "CI-25 branche tardive sans `stop:`")

    # ═════════════════════════════════════════════════════════════
    # N1 — le DÉCOMPTE annoncé par le helper doit être vrai
    # ═════════════════════════════════════════════════════════════
    t09_n = doc0[FICHIER_CATALOGUE]
    c.conforme(check_decompte_vocabulaire(rt0, t09_n), "CI-18 décompte conforme")
    faux = rt0[RUNTIME_HELPERS].replace(
        "16 codes du catalogue figurent", "14 codes du catalogue figurent")
    c.viole(check_decompte_vocabulaire({**rt0, RUNTIME_HELPERS: faux}, t09_n),
            "décompte FAUX",
            "CI-18 codes présents sous-comptés (14 au lieu de 16)")
    faux = rt0[RUNTIME_HELPERS].replace(
        "2 codes du catalogue en sont ABSENTS",
        "4 codes du catalogue en sont ABSENTS")
    c.viole(check_decompte_vocabulaire({**rt0, RUNTIME_HELPERS: faux}, t09_n),
            "décompte FAUX", "CI-18 codes absents sur-comptés (4 au lieu de 2)")
    faux = rt0[RUNTIME_HELPERS].replace(
        "18 valeurs de CYCLE DE VIE", "4 valeurs de CYCLE DE VIE")
    c.viole(check_decompte_vocabulaire({**rt0, RUNTIME_HELPERS: faux}, t09_n),
            "décompte FAUX",
            "CI-18 décompte du helper resté à la répartition du lot L1")
    c.viole(check_decompte_vocabulaire(
        {**rt0, RUNTIME_HELPERS: "aucun decompte ici"}, t09_n),
        "n'énonce pas son décompte", "CI-18 décompte absent du helper")

    # ═════════════════════════════════════════════════════════════
    # N3 / N4 — ASP-CI-25 contrôle la COMPARAISON, pas le nom
    # Chaque mutation retire ou fausse UNE comparaison en laissant le nom du
    # témoin ailleurs dans le bloc : la version précédente les laissait toutes
    # passer.
    # ═════════════════════════════════════════════════════════════
    def _tardif(vieux, neuf):
        m = yaml.safe_load(mot_txt(vieux, neuf)[RUNTIME_MOTEUR])[ID_MOTEUR]
        return _aplatir(m["sequence"])

    # N3, cas nommé par le contre-audit : `g2_err_dock != 'ok'` retiré, le nom
    # restant présent dans la branche d'indisponibilité.
    c.viole(check_branches_tardives(_tardif(
        "{{ g2_err_vac != 'none' or g2_err_dock != 'ok' }}",
        "{{ g2_err_vac != 'none' }}")),
        "g2_err_dock != 'ok'", "CI-25 comparaison du dock retirée, nom conservé")
    # symétrique : erreur aspirateur
    c.viole(check_branches_tardives(_tardif(
        "{{ g2_err_vac != 'none' or g2_err_dock != 'ok' }}",
        "{{ g2_err_dock != 'ok' }}")),
        "g2_err_vac != 'none'", "CI-25 comparaison de l'aspirateur retirée")
    # témoin de session : comparaison faussée
    c.viole(check_branches_tardives(_tardif(
        '"{{ g2_session == \'on\' }}"', '"{{ g2_session == \'oui\' }}"')),
        "g2_session == 'on'", "CI-25 comparaison de session faussée")
    # état machine : classe de repos comparée au lieu de la classe d'activité
    c.viole(check_branches_tardives(_tardif(
        '"{{ g2_etat in classe_a }}"', '"{{ g2_etat in classe_r }}"')),
        "g2_etat in classe_a", "CI-25 comparaison d'activité détournée")
    # état machine : indisponibilité
    c.viole(check_branches_tardives(_tardif(
        '"{{ g2_etat in classe_e_indispo }}"', '"{{ g2_etat in indispo }}"')),
        "g2_etat in classe_e_indispo", "CI-25 comparaison d'indisponibilité détournée")
    # état machine : fourre-tout de classe N
    c.viole(check_branches_tardives(_tardif(
        '"{{ g2_etat not in classe_r }}"', '"{{ g2_etat not in classe_a }}"')),
        "g2_etat not in classe_r", "CI-25 fourre-tout de classe N détourné")

    # N4 — le motif du refus tardif `error` doit rester exact.
    m_n4 = copy.deepcopy(mot0)
    for st in m_n4[ID_MOTEUR]["sequence"]:
        if isinstance(st, dict) and "choose" in st:
            for o in st["choose"]:
                if "g2_etat == 'error'" in str(o.get("conditions")):
                    for pas in o["sequence"]:
                        if _service(pas) == "input_text.set_value":
                            pas["data"]["value"] = "REFUS/ROBOT_INDISPONIBLE"
    c.viole(check_branches_tardives(_aplatir(m_n4[ID_MOTEUR]["sequence"])),
            "ne produit pas `REFUS/ERREUR_EQUIPEMENT`",
            "CI-25/N4 état tardif `error` diagnostiqué en indisponibilité")

    # N4 bis — la branche `error` doit continuer d'arrêter la séquence.
    m_n4b = copy.deepcopy(mot0)
    for st in m_n4b[ID_MOTEUR]["sequence"]:
        if isinstance(st, dict) and "choose" in st:
            for o in st["choose"]:
                if "g2_etat == 'error'" in str(o.get("conditions")):
                    o["sequence"] = [p for p in o["sequence"]
                                     if not (isinstance(p, dict) and "stop" in p)]
    c.viole(check_branches_tardives(_aplatir(m_n4b[ID_MOTEUR]["sequence"])),
            "n'arrête pas la séquence",
            "CI-25/N4 branche `error` tardive sans `stop:`")

    # ---- ASP-CI-26 : chemins d'exception couverts ------------------------
    seq0 = mot0[ID_MOTEUR]["sequence"]
    c.conforme(check_chemins_silencieux(seq0), "CI-26 conforme")

    # La reproduction du DÉFAUT D'ORIGINE : sans `continue_on_error`, chacune
    # des trois écritures préparatoires laisse le verdict sur
    # `VALIDATION_EN_COURS`. C'est l'état observé en production le 2026-08-27.
    for svc, cible, _t, _r in ECRITURES_PREPARATOIRES:
        m = copy.deepcopy(mot0)
        # La visite emprunte le CHEMIN NOMINAL : la sélection de carte peut
        # être logée dans sa garde d'abstention (07 §3.2 bis), et une
        # mutation qui ne l'atteindrait pas ne prouverait plus rien.
        for _rang, st in _nominal(m[ID_MOTEUR]["sequence"]):
            if isinstance(st, dict) and _service(st) == svc and cible in _cibles(st):
                st.pop("continue_on_error", None)
        c.viole(check_chemins_silencieux(m[ID_MOTEUR]["sequence"]),
                "ne survit pas à un arrêt",
                f"CI-26 chemin silencieux réintroduit sur {cible}")

    # L'émission reste conforme SANS `continue_on_error` : son verdict, lui,
    # survit. C'est ce qui distingue les deux traitements sans cas particulier.
    m_em = copy.deepcopy(mot0)
    for st in m_em[ID_MOTEUR]["sequence"]:
        if isinstance(st, dict) and _service(st) == SVC_COMMANDE:
            st.pop("continue_on_error", None)
    c.conforme(check_chemins_silencieux(m_em[ID_MOTEUR]["sequence"]),
               "CI-26 émission conforme sans absorption")

    # Le verdict non survivant posé juste avant l'émission la rend fautive.
    m_vnc = copy.deepcopy(mot0)
    for st in m_vnc[ID_MOTEUR]["sequence"]:
        if (isinstance(st, dict) and _service(st) == "input_text.set_value"
                and ID_VERDICT in _cibles(st)
                and st["data"].get("value") == "COMMANDE/ISSUE_NON_ETABLIE"):
            st["data"]["value"] = "VALIDATION_EN_COURS"
    c.viole(check_chemins_silencieux(m_vnc[ID_MOTEUR]["sequence"]),
            "ne survit pas à un arrêt",
            "CI-26 émission sous un verdict qui n'affirme pas l'ignorance")

    # Un refus posé DANS une branche ne protège pas la suite : il est suivi
    # d'un `stop:`. Le lire comme verdict courant était le faux vert d'une
    # première version de ce contrôle.
    m_br = copy.deepcopy(mot0)
    for _rang, st in _nominal(m_br[ID_MOTEUR]["sequence"]):
        if isinstance(st, dict) and _service(st) == SVC_EAU and NATIF_CARTE in _cibles(st):
            st.pop("continue_on_error", None)
    assert any("VALIDATION_EN_COURS" in e
               for e in check_chemins_silencieux(m_br[ID_MOTEUR]["sequence"])), \
        "CI-26 : le verdict courant doit se lire sur le CHEMIN NOMINAL"
    c.violations += 1

    # ---- ASP-CI-27 : écritures préparatoires -----------------------------
    c.conforme(check_ecritures_preparatoires(seq0), "CI-27 conforme")

    def mut27(f):
        m = copy.deepcopy(mot0)
        f(m[ID_MOTEUR]["sequence"])
        return check_ecritures_preparatoires(m[ID_MOTEUR]["sequence"])

    def _i(seq, pred):
        return next(i for i, s in enumerate(seq) if isinstance(s, dict) and pred(s))

    def _i_wait(seq, instant):
        return _i(seq, lambda s: isinstance(s.get("wait_template"), str)
                  and instant in s["wait_template"])

    def _i_svc(seq, svc, cible):
        # Rang sur le CHEMIN NOMINAL : la sélection de carte peut être logée
        # dans sa garde d'abstention, et porte alors le rang du `choose`
        # qui la garde (07 §3.2 bis).
        return next(r for r, s in _nominal(seq)
                    if isinstance(s, dict) and _service(s) == svc
                    and cible in _cibles(s))

    # (1) confirmation carte replacée AVANT l'écriture d'eau : le
    #     rafraîchissement qui la rend probante n'a alors pas encore eu lieu.
    def _avant_eau(seq):
        i_w = _i_wait(seq, "t_carte")
        w, ch = seq.pop(i_w), seq.pop(i_w)
        j = _i_svc(seq, SVC_EAU, NATIF_EAU)
        seq[j - 1:j - 1] = [w, ch]
    c.viole(mut27(_avant_eau), "ordre non conforme",
            "CI-27/M1 confirmation carte avant l'eau")

    # (2) aspiration déplacée AVANT la confirmation de carte.
    def _asp_avant(seq):
        i_a = _i_svc(seq, SVC_ASPIRATION, NATIF_VACUUM)
        a = seq.pop(i_a)
        seq.insert(_i_wait(seq, "t_carte"), a)
    c.viole(mut27(_asp_avant), "ordre non conforme",
            "CI-27/M2 aspiration avant la confirmation de carte")

    # (3) commande déplacée AVANT la confirmation de carte : ASP-IMC-1.
    def _cmd_avant(seq):
        i_c = _i_svc(seq, SVC_COMMANDE, NATIF_VACUUM)
        cmd = seq.pop(i_c)
        seq.insert(_i_wait(seq, "t_carte"), cmd)
    c.viole(mut27(_cmd_avant), "violation directe d'ASP-IMC-1",
            "CI-27/M3 commande avant la confirmation cartographique")

    # (4) le rafraîchissement indirect disparaît : l'écriture d'eau est
    #     remplacée par une primitive qui ne passe pas par `send()`.
    def _sans_refresh(seq):
        i_e = _i_svc(seq, SVC_EAU, NATIF_EAU)
        seq[i_e] = {"action": "input_text.set_value", "continue_on_error": True,
                    "target": {"entity_id": ID_TRACE},
                    "data": {"value": "x"}}
    c.viole(mut27(_sans_refresh), "hors des trois écritures préparatoires",
            "CI-27/M4 écriture d'eau remplacée, plus aucun refresh")

    # (10) `last_updated` au lieu de `last_reported` : preuve inopérante.
    def _last_updated(seq):
        i = _i_wait(seq, "t_carte")
        seq[i]["wait_template"] = seq[i]["wait_template"].replace(
            "last_reported", "last_updated")
    c.viole(mut27(_last_updated), "n'exige pas la publication fraîche",
            "CI-27/M10 last_updated au lieu de last_reported")

    # (12 bis) comparaison `>=` : une publication contemporaine ne prouve rien.
    def _large(seq):
        i = _i_wait(seq, "t_aspiration")
        seq[i]["wait_template"] = seq[i]["wait_template"].replace(
            "> t_aspiration", ">= t_aspiration")
    c.viole(mut27(_large), "n'exige pas la publication fraîche",
            "CI-27/M-large comparaison non stricte")

    # (11) instant GLOBAL réutilisé pour les trois écritures.
    def _global(seq):
        for st in seq:
            if isinstance(st, dict) and isinstance(st.get("variables"), dict):
                for nom in ("t_eau", "t_aspiration"):
                    if nom in st["variables"]:
                        del st["variables"][nom]
                        st["variables"]["t_carte"] = "{{ now().timestamp() }}"
    c.viole(mut27(_global), "instant de référence",
            "CI-27/M11 instant global au lieu de trois instants propres")

    # (12) décision fondée sur `wait.completed` — or le wait n'est pas
    #      réveillé par une republication identique.
    def _wait_completed(seq):
        i = _i_wait(seq, "t_eau") + 1
        seq[i]["choose"][0]["conditions"][0]["value_template"] = \
            "{{ not wait.completed }}"
    c.viole(mut27(_wait_completed), "wait.completed",
            "CI-27/M12 décision fondée sur wait.completed")

    # L'instant capturé APRÈS son écriture ne borne plus rien.
    def _apres(seq):
        i_v = _i(seq, lambda s: isinstance(s.get("variables"), dict)
                 and "t_carte" in s["variables"])
        v = seq.pop(i_v)
        seq.insert(_i_svc(seq, SVC_EAU, NATIF_CARTE) + 1, v)
    c.viole(mut27(_apres), "capturé APRÈS son écriture",
            "CI-27/M-ordre instant capturé après l'appel")

    # `continue_on_timeout` retiré : le timeout deviendrait un arrêt sec, et la
    # relecture finale — seule preuve sur une republication identique — ne
    # serait jamais atteinte.
    def _sans_cot(seq):
        seq[_i_wait(seq, "t_carte")].pop("continue_on_timeout", None)
    c.viole(mut27(_sans_cot), "continue_on_timeout",
            "CI-27/M-cot confirmation sans continue_on_timeout")

    # Le refus attendu remplacé par l'autre code : carte et réglage ne se
    # substituent jamais l'un à l'autre.
    def _mauvais_refus(seq):
        i = _i_wait(seq, "t_carte") + 1
        for pas in seq[i]["choose"][0]["sequence"]:
            if _service(pas) == "input_text.set_value":
                pas["data"]["value"] = "REFUS/REGLAGE_NON_CONFIRME"
    c.viole(mut27(_mauvais_refus), "ne pose pas `REFUS/CARTE_NON_CONFIRMEE`",
            "CI-27/M-refus code permuté entre carte et réglage")

    # Le `stop:` retiré : la séquence poursuivrait après un refus.
    def _sans_stop(seq):
        i = _i_wait(seq, "t_eau") + 1
        seq[i]["choose"][0]["sequence"] = [
            p for p in seq[i]["choose"][0]["sequence"]
            if not (isinstance(p, dict) and "stop" in p)]
    c.viole(mut27(_sans_stop), "avec un `stop:`",
            "CI-27/M-stop refus de confirmation sans stop")

    # `continue_on_error` hors allowlist — l'émission, et une écriture de
    # helper. Les deux doivent tomber.
    for cible_svc, cible_ent in ((SVC_COMMANDE, NATIF_VACUUM),
                                 ("input_text.set_value", ID_VERDICT)):
        def _hors(seq, s=cible_svc, e=cible_ent):
            for st in seq:
                if isinstance(st, dict) and _service(st) == s and e in _cibles(st):
                    st["continue_on_error"] = True
        c.viole(mut27(_hors), "hors des trois écritures préparatoires",
                f"CI-27/M-allowlist continue_on_error sur {cible_svc}")

    # (5-9) LES CAS DE RENDU. La postcondition est jouée sur des états
    # simulés : c'est ici que « valeur juste mais périmée », « fraîche mais
    # fausse » et « une seule des deux lectures fraîche » sont opposables.
    for instant in INSTANTS_PREPARATOIRES:
        gabarit = next(s["wait_template"] for s in seq0
                       if isinstance(s, dict)
                       and isinstance(s.get("wait_template"), str)
                       and instant in s["wait_template"])
        c.conforme(_postcondition_rendue(instant, gabarit),
                   f"CI-27 postcondition rendue — {instant}")
        # La fraîcheur retirée — chirurgicalement : seules les conjonctions de
        # fraîcheur tombent, le gabarit reste SYNTAXIQUEMENT valide. Sans quoi
        # la mutation serait détectée pour une mauvaise raison (gabarit cassé)
        # et ne prouverait rien du contrôle de fraîcheur lui-même.
        sans = re.sub(r"\s*and as_timestamp\(states\.[^,]+,\s*0\)\s*>\s*t_\w+",
                      "", gabarit)
        assert sans != gabarit and "as_timestamp" not in sans, \
            f"mutation de fraîcheur inopérante sur {instant}"
        c.viole(_postcondition_rendue(instant, sans), "doit REFUSER",
                f"CI-27 fraîcheur retirée — {instant}")

    # ---- G : LA GARDE D'ABSTENTION de la sélection de carte (07 §3.2 bis) --
    # Cinq propriétés, et cinq seulement, sont ici opposables :
    #   1. carte demandée == carte active LISIBLE et concordante -> AUCUN appel
    #   2. carte active DIFFÉRENTE                               -> UN appel
    #   3. carte active `unknown`                                -> UN appel
    #   4. carte active `unavailable`                            -> UN appel
    #   5. la postcondition carte + pièces reste exigée sur TOUS les chemins.
    c.conforme(check_garde_abstention(seq0, corps0), "CI-27/G garde conforme")

    def _i_garde(seq):
        return next(i for i, s in enumerate(seq) if _action_gardee(s) is not None)

    def _cond_garde(seq, gabarit):
        seq[_i_garde(seq)]["choose"][0]["conditions"] = [
            {"condition": "template", "value_template": gabarit}]

    GARDE_REELLE = _texte_conditions(seq0[_i_garde(seq0)])

    # G1 — l'illisible réputé correct : `unknown` et `unavailable` admis comme
    #      carte active. C'est le fallback qu'ASP-INV-45 proscrit — le moteur
    #      s'abstiendrait sur une carte qu'il ne sait PAS être la bonne.
    def _g_illisible(seq):
        _cond_garde(seq, GARDE_REELLE.replace(
            f"states('{NATIF_CARTE}')\n          == ctx_carte.option",
            f"states('{NATIF_CARTE}')\n          in [ctx_carte.option, 'unknown', 'unavailable']"))
    errs_g1 = mut27(_g_illisible)
    assert any("`unknown`" in e and "attendu l'APPEL" in e for e in errs_g1), errs_g1
    assert any("`unavailable`" in e and "attendu l'APPEL" in e for e in errs_g1), errs_g1
    c.viole(errs_g1, "attendu l'APPEL",
            "CI-27/G1 garde admettant une carte active illisible")

    # G2 — la seconde lecture d'ASP-INV-29 retirée : le sélecteur seul dit ce
    #      qui a été DEMANDÉ, jamais ce qui a été CHARGÉ. Une carte dont les
    #      pièces manquent ferait s'abstenir.
    def _g_sans_pieces(seq):
        _cond_garde(seq, f"{{{{ states('{NATIF_CARTE}') != ctx_carte.option }}}}")
    errs_g2 = mut27(_g_sans_pieces)
    assert any("MANQUE" in e and "attendu l'APPEL" in e for e in errs_g2), errs_g2
    c.viole(errs_g2, "attendu l'APPEL",
            "CI-27/G2 garde sans la lecture des pièces exposées")

    # G3 — la garde qui s'abstient TOUJOURS : plus aucune sélection de carte.
    def _g_toujours(seq):
        _cond_garde(seq, "{{ false }}")
    c.viole(mut27(_g_toujours), "attendu l'APPEL",
            "CI-27/G3 garde s'abstenant inconditionnellement")

    # G4 — la garde qui ne s'abstient JAMAIS : l'appel redondant revient, et
    #      avec lui l'entrée ERREUR pour une opération nominale.
    def _g_jamais(seq):
        _cond_garde(seq, "{{ true }}")
    c.viole(mut27(_g_jamais), "attendu l'ABSTENTION",
            "CI-27/G4 garde n'écartant jamais l'appel redondant")

    # G5 — la garde qui EMPRUNTE la preuve de la confirmation. Aucune
    #      publication n'est postérieure à `t_carte` quand elle s'évalue :
    #      la garde s'abstiendrait toujours, et la fraîcheur perdrait son sens.
    for emprunt, ajout in (
            ("t_carte", " and 0 > t_carte"),
            ("last_reported",
             f" and as_timestamp(states.{NATIF_CARTE}.last_reported, 0) > 0")):
        def _g_emprunt(seq, a=ajout):
            _cond_garde(seq, GARDE_REELLE.replace(
                "== 0) }}", "== 0" + a + ") }}"))
        c.viole(mut27(_g_emprunt), f"invoque `{emprunt}`",
                f"CI-27/G5 garde empruntant `{emprunt}`")

    # G6 — la garde qui POSE un verdict, et celle qui ARRÊTE la séquence :
    #      une abstention n'est ni un refus ni une issue.
    def _g_ecrit(seq):
        seq[_i_garde(seq)]["choose"][0]["sequence"].append(
            {"action": "input_text.set_value",
             "target": {"entity_id": ID_VERDICT},
             "data": {"value": "REFUS/CARTE_NON_CONFIRMEE"}})
    c.viole(mut27(_g_ecrit), "écrit", "CI-27/G6 garde d'abstention posant un verdict")

    def _g_stop(seq):
        seq[_i_garde(seq)]["choose"][0]["sequence"].append({"stop": "abstention"})
    c.viole(mut27(_g_stop), "porte un `stop:`",
            "CI-27/G6 bis garde d'abstention arrêtant la séquence")

    # G7 — forme non fermée : une seconde branche, puis un `default:`.
    def _g_deux_branches(seq):
        g = seq[_i_garde(seq)]
        g["choose"].append({"conditions": [{"condition": "template",
                                            "value_template": "{{ true }}"}],
                            "sequence": [{"stop": "autre"}]})
    c.viole(mut27(_g_deux_branches), "forme fermée exigée",
            "CI-27/G7 garde à deux branches")

    def _g_default(seq):
        seq[_i_garde(seq)]["default"] = [{"stop": "autre"}]
    c.viole(mut27(_g_default), "forme fermée exigée",
            "CI-27/G7 bis garde portant un `default:`")

    # G8 — LA PROPRIÉTÉ 5, opposable : la confirmation carte + pièces rendue
    #      CONDITIONNELLE. Elle cesserait d'être exigée sur tous les chemins,
    #      et le chemin d'abstention émettrait sans postétat. La garde retire
    #      un appel ; elle ne retire JAMAIS la preuve.
    def _g_postcondition_conditionnelle(seq):
        i_w = _i_wait(seq, "t_carte")
        w, ch = seq.pop(i_w), seq.pop(i_w)
        seq.insert(i_w, {"choose": [{
            "conditions": [{"condition": "template",
                            "value_template": "{{ true }}"}],
            "sequence": [w, ch]}]})
    c.viole(mut27(_g_postcondition_conditionnelle),
            "aucune confirmation ne borne",
            "CI-27/G8 confirmation carte + pièces rendue conditionnelle")

    # G8 bis — la même preuve, prise par l'autre bout : la confirmation logée
    #          DANS la garde. Le contrôle refuse, quel que soit le chemin.
    def _g_postcondition_gardee(seq):
        i_w = _i_wait(seq, "t_carte")
        w, ch = seq.pop(i_w), seq.pop(i_w)
        seq[_i_garde(seq)]["choose"][0]["sequence"] += [w, ch]
    c.viole(mut27(_g_postcondition_gardee), "forme fermée exigée",
            "CI-27/G8 bis postcondition cartographique logée dans la garde")

    # ---- R1 : la visite doit être EXHAUSTIVE ------------------------------
    # Seize mutations passaient au vert tant que le parcours ne descendait que
    # dans `choose`. Chaque charge fautive est ici logée dans CHACUNE des
    # structures composites du schéma, et doit être vue.
    def _repeat(a):
        return {"repeat": {"count": 1, "sequence": [a]}}

    def _if_then(a):
        return {"if": [{"condition": "template", "value_template": "{{ true }}"}],
                "then": [a]}

    def _if_else(a):
        return {"if": [{"condition": "template", "value_template": "{{ false }}"}],
                "then": [{"stop": "rien"}], "else": [a]}

    def _parallel(a):
        return {"parallel": [{"sequence": [a]}]}

    def _choose_dans_repeat(a):
        return {"repeat": {"count": 1, "sequence": [
            {"choose": [{"conditions": [{"condition": "template",
                                         "value_template": "{{ true }}"}],
                         "sequence": [a]}]}]}}

    ENVELOPPES = (("repeat.sequence", _repeat), ("if.then", _if_then),
                  ("if.else", _if_else), ("parallel[].sequence", _parallel),
                  ("choose dans repeat", _choose_dans_repeat))

    def _cmd_en_trop():
        return {"action": SVC_COMMANDE, "continue_on_error": True,
                "target": {"entity_id": NATIF_VACUUM},
                "data": {"command": COMMANDE_SEGMENTEE,
                         "params": [{"segments": [16]}]}}

    def _writer_en_trop():
        return {"action": "input_text.set_value",
                "target": {"entity_id": ID_VERDICT},
                "data": {"value": "LANCEE/DEMARRAGE_OBSERVE"}}

    for nom_env, env in ENVELOPPES:
        # (a) seconde émission cachée -> unicité de la commande (ASP-CI-12/17)
        m = copy.deepcopy(mot0)
        m[ID_MOTEUR]["sequence"].append(env(_cmd_en_trop()))
        c.viole(check_charge_utile(_aplatir(m[ID_MOTEUR]["sequence"])),
                "EXACTEMENT un", f"CI-12/R1 seconde émission dans {nom_env}")
        # (b) la même porte `continue_on_error` -> allowlist (ASP-CI-27)
        c.viole(check_ecritures_preparatoires(m[ID_MOTEUR]["sequence"]),
                "hors des trois écritures préparatoires",
                f"CI-27/R1 continue_on_error dans {nom_env}")
        # (c) écrivain du verdict hors chemin nominal (ASP-CI-18)
        m2 = copy.deepcopy(mot0)
        m2[ID_MOTEUR]["sequence"].append(env(_writer_en_trop()))
        c.viole(check_vocabulaire_verdict(m2[ID_MOTEUR]["sequence"], rt0),
                "hors du chemin nominal",
                f"CI-18/R1 écrivain du verdict dans {nom_env}")

    # La visite elle-même : chaque structure doit être atteinte, avec chemin.
    for nom_env, env in ENVELOPPES:
        sonde = {"action": "vacuum.stop", "target": {"entity_id": NATIF_VACUUM}}
        chemins = [ch for ch, st in _actions([env(sonde)])
                   if _service(st) == "vacuum.stop"]
        assert len(chemins) == 1, \
            f"_actions n'atteint pas {nom_env} — trouvé {chemins}"
        c.conformes += 1

    # ---- R2 : forme ET typage de l'instant --------------------------------
    # `now().timestamp()` en sous-chaîne ne suffit pas : six variantes
    # passaient. La forme est désormais canonique, et le gabarit est RENDU.
    FORMES_FAUTIVES = (
        ("{{ now().timestamp() - 3600 }}", "antidate"),
        ("{{ now().timestamp() + 1 }}", "postdate"),
        ("{{ now().timestamp() | string }}", "retypage en chaîne"),
        ("{{ now().timestamp() | int }}", "troncature"),
        ("{{ now().timestamp() | default(0) }}", "repli"),
        ("{{ now().timestamp() > 0 }}", "booléen"),
        ("{{ 0 }}", "littéral"),
        ("{{ 1e309 * 10 }}", "non fini"),
        ("{{ t_carte }}", "référence à un autre instant"),
    )
    for gabarit, quoi in FORMES_FAUTIVES:
        def _forme(seq, g=gabarit):
            for st in seq:
                if isinstance(st, dict) and isinstance(st.get("variables"), dict) \
                        and "t_carte" in st["variables"]:
                    st["variables"]["t_carte"] = g
        c.viole(mut27(_forme), "doit être EXACTEMENT",
                f"CI-27/R2 instant — {quoi}")

    # Le typage est contrôlé SÉPARÉMENT de la forme : une forme canonique dont
    # le rendu ne serait pas numérique doit tomber elle aussi.
    for valeur, attendu in ((("texte"), "str"), ((True), "bool")):
        errs_typage = _postcondition_rendue(
            "t_aspiration",
            next(s["wait_template"] for s in seq0
                 if isinstance(s, dict) and isinstance(s.get("wait_template"), str)
                 and "t_aspiration" in s["wait_template"]),
            valeur)
        assert errs_typage, \
            f"une valeur d'instant {attendu} doit produire un écart"
        c.violations += 1

    # ---- M-A : MAPPINGS NUS dans les structures composites ----------------
    # `SCRIPT_SCHEMA` applique `ensure_list` : un mapping nu est une forme
    # VALIDE partout où une séquence est attendue, et `choose` accepte un
    # choix unique en mapping. Quarante-deux mutations passaient au vert — ou
    # faisaient PLANTER le checker — tant que ces formes n'étaient pas
    # normalisées.
    def _env_seq_nue(a):
        return {"sequence": a}

    def _env_choose_mapping(a):
        return {"choose": {"conditions": [{"condition": "template",
                                           "value_template": "{{ true }}"}],
                           "sequence": a}}

    def _env_choose_seq_nue(a):
        return {"choose": [{"conditions": [{"condition": "template",
                                            "value_template": "{{ true }}"}],
                            "sequence": a}]}

    def _env_default_nu(a):
        return {"choose": [{"conditions": [{"condition": "template",
                                            "value_template": "{{ false }}"}],
                            "sequence": [{"stop": "rien"}]}], "default": a}

    def _env_repeat_nu(a):
        return {"repeat": {"count": 1, "sequence": a}}

    def _env_then_nu(a):
        return {"if": [{"condition": "template", "value_template": "{{ true }}"}],
                "then": a}

    def _env_else_nu(a):
        return {"if": [{"condition": "template", "value_template": "{{ false }}"}],
                "then": [{"stop": "rien"}], "else": a}

    def _env_parallel_nu(a):
        return {"parallel": a}

    NUS = (("sequence nue", _env_seq_nue),
           ("choose en mapping", _env_choose_mapping),
           ("choose[].sequence nue", _env_choose_seq_nue),
           ("choose.default nu", _env_default_nu),
           ("repeat.sequence nue", _env_repeat_nu),
           ("if.then nu", _env_then_nu), ("if.else nu", _env_else_nu),
           ("parallel nu", _env_parallel_nu))

    def _verdict_hors():
        return {"action": "input_text.set_value",
                "target": {"entity_id": ID_VERDICT},
                "data": {"value": "MISSION/PRESQUE_LANCEE"}}

    def _writer_robot():
        return {"action": SVC_EAU, "target": {"entity_id": NATIF_CARTE},
                "data": {"option": "Annexe"}}

    for nom_nu, env in NUS:
        # (a) la visite ATTEINT la forme — sinon rien d'autre n'a de sens.
        sonde = {"action": "vacuum.stop", "target": {"entity_id": NATIF_VACUUM}}
        atteints = [ch for ch, st in _actions([env(sonde)])
                    if _service(st) == "vacuum.stop"]
        assert len(atteints) == 1, \
            f"_actions n'atteint pas « {nom_nu} » — trouvé {atteints}"
        c.conformes += 1
        # (b) seconde émission cachée sous la forme nue
        m = copy.deepcopy(mot0)
        m[ID_MOTEUR]["sequence"].append(env(_cmd_en_trop()))
        c.viole(check_charge_utile(_aplatir(m[ID_MOTEUR]["sequence"])),
                "EXACTEMENT un", f"CI-12/M-A seconde émission sous {nom_nu}")
        c.viole(check_ecritures_preparatoires(m[ID_MOTEUR]["sequence"]),
                "hors des trois écritures préparatoires",
                f"CI-27/M-A continue_on_error sous {nom_nu}")
        # (c) verdict hors vocabulaire
        m2 = copy.deepcopy(mot0)
        m2[ID_MOTEUR]["sequence"].append(env(_verdict_hors()))
        c.viole(check_vocabulaire_verdict(m2[ID_MOTEUR]["sequence"], rt0),
                "hors de son ensemble de dix-huit valeurs", f"CI-18/M-A verdict hors vocabulaire sous {nom_nu}")
        # (d) writer Roborock supplémentaire
        m3 = copy.deepcopy(mot0)
        m3[ID_MOTEUR]["sequence"].append(env(_writer_robot()))
        c.viole(check_ordre_sequence(m3[ID_MOTEUR]["sequence"]),
                "exactement une écriture",
                f"CI-16/M-A writer Roborock sous {nom_nu}")

    # m-C — un `choose` en mapping nu est ANALYSÉ, jamais un traceback.
    valide = copy.deepcopy(mot0)
    valide[ID_MOTEUR]["sequence"].append(
        _env_choose_mapping({"stop": "branche inerte"}))
    c.conforme(check_ecritures_preparatoires(valide[ID_MOTEUR]["sequence"]),
               "m-C choose en mapping nu : analysé sans écart")
    c.conforme(check_chemins_silencieux(valide[ID_MOTEUR]["sequence"]),
               "m-C choose en mapping nu : aucun chemin silencieux")

    # Une forme INVALIDE produit un écart lisible, jamais une exception.
    difforme = copy.deepcopy(mot0)
    difforme[ID_MOTEUR]["sequence"].append({"repeat": {"count": 1,
                                                       "sequence": 42}})
    c.viole(check_chemins_silencieux(difforme[ID_MOTEUR]["sequence"]),
            "conteneur d'actions de type int",
            "M-A forme invalide diagnostiquée, non levée")

    # ---- M-B : multiplicité ET position des verdicts structurants ----------
    def _ecrire(v):
        return {"action": "input_text.set_value",
                "target": {"entity_id": ID_VERDICT}, "data": {"value": v}}

    def _rang_cmd(seq):
        return next(i for i, s in enumerate(seq) if _service(s) == SVC_COMMANDE)

    for valeur, _nature, _cote in VERDICTS_STRUCTURANTS:
        # duplication : l'occurrence correcte ne doit plus masquer la fautive
        m = copy.deepcopy(mot0)
        seq = m[ID_MOTEUR]["sequence"]
        seq.insert(_rang_cmd(seq), _ecrire(valeur))
        c.viole(check_vocabulaire_verdict(seq, rt0), "EXACTEMENT une fois",
                f"CI-18/M-B duplication de {valeur}")
        # suppression : une issue muette
        m2 = copy.deepcopy(mot0)
        seq2 = m2[ID_MOTEUR]["sequence"]
        for ch, st in _actions(seq2):
            if (_service(st) == "input_text.set_value"
                    and ID_VERDICT in _cibles(st)
                    and (st.get("data") or {}).get("value") == valeur):
                # Remplacée par un refus NON structurant, déjà présent
                # plusieurs fois : la valeur supprimée passe à 0 occurrence
                # sans perturber les quatre autres.
                st["data"]["value"] = "REFUS/ROBOT_INDISPONIBLE"
                break
        c.viole(check_vocabulaire_verdict(seq2, rt0), "EXACTEMENT une fois",
                f"CI-18/M-B suppression de {valeur}")

    # permutation succès / échec de la transition
    m = copy.deepcopy(mot0)
    for ch, st in _actions(m[ID_MOTEUR]["sequence"]):
        if _service(st) == "input_text.set_value" and ID_VERDICT in _cibles(st):
            v = (st.get("data") or {}).get("value")
            if v == "LANCEE/DEMARRAGE_OBSERVE":
                st["data"]["value"] = "ECHEC/TRANSITION_NON_OBSERVEE"
            elif v == "ECHEC/TRANSITION_NON_OBSERVEE":
                st["data"]["value"] = "LANCEE/DEMARRAGE_OBSERVE"
    c.viole(check_vocabulaire_verdict(m[ID_MOTEUR]["sequence"], rt0),
            "attendu « branche", "CI-18/M-B succès et échec permutés")

    # une valeur structurante logée dans un composite imbriqué
    m = copy.deepcopy(mot0)
    seq = m[ID_MOTEUR]["sequence"]
    for i, st in enumerate(seq):
        if (_service(st) == "input_text.set_value" and ID_VERDICT in _cibles(st)
                and (st.get("data") or {}).get("value")
                == "EMISSION/COMMANDE_ACCEPTEE"):
            seq[i] = _env_repeat_nu(_env_choose_mapping(
                _ecrire("EMISSION/COMMANDE_ACCEPTEE")))
            break
    c.viole(check_vocabulaire_verdict(seq, rt0), "hors du chemin nominal",
            "CI-18/M-B ACCEPTEE dans un composite imbriqué")

    # ---- m-A : aucun ordre fabriqué entre branches exclusives -------------
    # Deux branches d'un même `choose`, PERMUTÉES : leur ordre textuel ne doit
    # rien changer, puisqu'elles sont mutuellement exclusives.
    def _permuter_branches(seq):
        for st in seq:
            if isinstance(st, dict) and isinstance(st.get("choose"), list) \
                    and len(st["choose"]) > 1:
                st["choose"].reverse()
    permute = copy.deepcopy(mot0)
    _permuter_branches(permute[ID_MOTEUR]["sequence"])
    c.conforme(check_ordre_sequence(permute[ID_MOTEUR]["sequence"]),
               "m-A ordre insensible à la permutation de branches exclusives")
    avant = check_vocabulaire_verdict(mot0[ID_MOTEUR]["sequence"], rt0)
    apres = check_vocabulaire_verdict(permute[ID_MOTEUR]["sequence"], rt0)
    assert avant == apres, \
        f"m-A : la permutation de branches exclusives change la conclusion — {apres}"
    c.conformes += 1

    # Une action ordonnée déplacée DANS une branche : l'ordre devient
    # indécidable, et le contrôle le DIT au lieu de l'inventer.
    m = copy.deepcopy(mot0)
    seq = m[ID_MOTEUR]["sequence"]
    i_asp = next(i for i, s in enumerate(seq) if _service(s) == SVC_ASPIRATION)
    seq[i_asp] = _env_then_nu(seq[i_asp])
    c.viole(check_ordre_sequence(seq), "absente(s) du chemin nominal",
            "m-A aspiration hors chemin nominal : ordre indécidable")

    # ---- m-B : deux contextes réellement distincts ------------------------
    ctxs = contextes_postcondition(corps0)
    assert len(ctxs) >= 2, f"m-B : moins de deux contextes — {ctxs}"
    a, b = ctxs[0], ctxs[1]
    for cle in ("eau_cible", "mode_attendu", "aspiration_cible"):
        assert a[cle] != b[cle], f"m-B : contextes non distincts sur {cle}"
    assert a["ctx_carte"]["option"] != b["ctx_carte"]["option"], \
        "m-B : contextes non distincts sur l'option de carte"
    assert a["ctx_carte"]["noms"] != b["ctx_carte"]["noms"], \
        "m-B : contextes non distincts sur les noms de pièces"
    c.conformes += 1

    # Chaque substitution par littéral doit être vue par le SECOND contexte.
    SUBSTITUTIONS = (("ctx_carte.option", "'RDC'"),
                     ("eau_cible", "'off'"),
                     ("mode_attendu", "'vacuum'"),
                     ("aspiration_cible", "'balanced'"))
    for avant_s, apres_s in SUBSTITUTIONS:
        m = copy.deepcopy(mot0)
        corps_m = m[ID_MOTEUR]
        for st in corps_m["sequence"]:
            if isinstance(st, dict) and isinstance(st.get("wait_template"), str):
                st["wait_template"] = st["wait_template"].replace(avant_s, apres_s)
        c.viole(check_ecritures_preparatoires(corps_m["sequence"], corps_m),
                "postcondition de",
                f"m-B littéral substitué à `{avant_s}`")

    # ---- m-C bis : LE CHEMIN RÉEL COMPLET, et l'anti-régression -----------
    #
    # Trois accès directs à `choose` avaient échappé au banc précédent parce
    # que celui-ci n'appelait qu'une SÉLECTION de contrôles. La leçon est
    # inscrite ici : les tests passent désormais par la liste EXHAUSTIVE des
    # contrôles runtime, et cette liste est confrontée à ce que `run()`
    # invoque réellement.

    CONTROLES_RUNTIME = (
        "check_ecrivain_unique", "check_charge_utile", "check_voies_interdites",
        "check_mode_jamais_ecrit", "check_ordre_sequence",
        "check_vocabulaire_verdict", "check_decompte_vocabulaire",
        "check_motif_total", "check_constantes_temporelles",
        "check_concordance_runtime", "check_rendus_moteur",
        "check_etat_canonique_rendu", "check_garde_rendue",
        "check_branches_tardives", "check_chemins_silencieux",
        "check_ecritures_preparatoires",
    )

    def _tous_controles(moteur_yaml, runtime):
        """Appelle TOUS les contrôles runtime, comme `run()` le fait."""
        corps_m = moteur_yaml.get(ID_MOTEUR) or {}
        top_m = corps_m.get("sequence") or []
        plat_m = _aplatir(top_m)
        helpers_m = yaml.safe_load(runtime[RUNTIME_HELPERS]) or {}
        out = []
        out += check_ecrivain_unique(moteur_yaml, runtime, {})
        out += check_charge_utile(plat_m)
        out += check_voies_interdites(runtime)
        out += check_mode_jamais_ecrit(plat_m)
        out += check_ordre_sequence(top_m)
        out += check_vocabulaire_verdict(top_m, runtime)
        out += check_decompte_vocabulaire(runtime, t09r)
        out += check_motif_total(t09r, t02r, runtime[RUNTIME_MOTIF])
        out += check_constantes_temporelles(runtime)
        out += check_concordance_runtime(corps_m, runtime, helpers_m, t02r,
                                         t03r, audit0)
        out += check_rendus_moteur(corps_m, plat_m, t02r)
        out += check_etat_canonique_rendu(runtime[RUNTIME_ETAT])
        out += check_garde_rendue(runtime[RUNTIME_GARDE])
        out += check_branches_tardives(plat_m)
        out += check_chemins_silencieux(top_m)
        out += check_ecritures_preparatoires(top_m, corps_m)
        return out

    # (i) la liste ci-dessus couvre EXACTEMENT ce que `run()` invoque.
    src_run = inspect.getsource(run)
    invoques = set(re.findall(r"\b(check_[a-z_]+)\(", src_run))
    normatifs = {"check_invariants", "check_referentiel", "check_codes",
                 "check_partition", "check_profils", "check_identifiants",
                 "check_lovelace", "check_referentiel_technique",
                 "check_etats_canoniques", "check_fenetres",
                 # Maintenance (M0) : contrôles de TEXTE contractuel, joués par
                 # la batterie de mutations ASP-CI-29 … ASP-CI-33 plus bas.
                 "check_perimetre_entretien", "check_echeance_entretien",
                 "check_primitive_irreversible", "check_remise_a_zero",
                 "check_notifications_entretien"}
    # M1 : controles de RUNTIME TEMPLATE, joues par la batterie de
    # mutations ASP-CI-34 … ASP-CI-36 plus bas, sur le fichier reel.
    controles_m1 = {"check_projection_entretien", "check_projection_rendue",
                    "check_interdits_projection"}
    # N1 : controles de RUNTIME D'AUTOMATION, joues par la batterie de
    # mutations ASP-CI-37 … ASP-CI-39 plus bas, sur le dossier reel.
    controles_n1 = {"check_writers_n1", "check_projection_n1_rendue",
                    "check_interdits_n1"}
    # L2 : controles de RUNTIME DE CONDUITE ET DE SUPERVISION, joues par la
    # batterie de mutations plus bas, sur les fichiers reels.
    controles_l2 = {"check_sequence_conduite", "check_supervision"}
    # U0 : confrontation de la COUCHE D'INTENTION, jouee par la batterie
    # ASP-CI-28 plus bas, sur les sept fichiers reels.
    controles_u0 = {"check_referentiel_intention"}
    # M2 : controles de la DECLARATION D'ENTRETIEN, joues par la batterie
    # ASP-CI-40 … ASP-CI-42 plus bas, sur les fichiers reels du lot.
    controles_m2 = {"check_declaration_entretien", "check_sequence_entretien",
                    "check_ui_entretien"}
    # C45 lot 3 : EGALITE des representations de classe, REGIME TRANSITOIRE du
    # code historique et OFFRE des gestes, joues par la batterie ASP-CI-43 …
    # ASP-CI-45 plus bas, sur les fichiers reels du depot.
    controles_c45 = {"check_representations_de_classe",
                     "check_ancien_code_transitoire", "check_offre_gestes"}
    manquants = (invoques - normatifs - set(CONTROLES_RUNTIME) - controles_m1
                 - controles_n1 - controles_l2 - controles_u0 - controles_m2
                 - controles_c45)
    assert not manquants, \
        f"m-C bis : `run()` invoque {sorted(manquants)}, absent(s) de la " \
        f"batterie du selftest — c'est exactement le trou qui a laissé " \
        f"passer trois accès non normalisés."
    c.conformes += 1

    # (ii) forme INTACTE et valide : le chemin complet ne plante pas.
    intact = copy.deepcopy(mot0)
    c.conforme(_tous_controles(intact, rt0), "m-C bis chemin complet conforme")

    # (iii) `choose` en MAPPING NU aux emplacements des trois sites.
    #       Le moteur reste fonctionnellement identique — seule la FORME
    #       change — donc le chemin complet doit rester conforme.
    def _choose_en_mapping(seq, predicat):
        touche = 0
        for st in seq:
            if (isinstance(st, dict) and isinstance(st.get("choose"), list)
                    and len(st["choose"]) == 1 and predicat(st)):
                st["choose"] = st["choose"][0]
                touche += 1
        return touche

    # site 1 — la garde de type de `segments`, lue par ASP-CI-22.
    m_g = copy.deepcopy(mot0)
    n = _choose_en_mapping(m_g[ID_MOTEUR]["sequence"],
                           lambda s: "segments is" in str(s.get("choose")))
    assert n == 1, f"m-C bis : garde `segments` non convertie ({n})"
    c.conforme(_tous_controles(m_g, rt0),
               "m-C bis site 1 — garde `segments` en mapping nu")

    # sites 2 et 3 — les deux arbitrages de `check_branches_tardives` sont des
    # `choose` à branches multiples : on éprouve la normalisation par un
    # mapping nu inséré JUSTE APRÈS chaque bloc `variables` de garde.
    for prefixe, libelle in (("g1_", "garde initiale"),
                             ("g2_", "arbitrage tardif")):
        m_b = copy.deepcopy(mot0)
        seq_b = m_b[ID_MOTEUR]["sequence"]
        i_v = next(i for i, s in enumerate(seq_b)
                   if isinstance(s, dict) and isinstance(s.get("variables"), dict)
                   and any(k.startswith(prefixe) for k in s["variables"]))
        seq_b.insert(i_v + 1, {"choose": {
            "conditions": [{"condition": "template",
                            "value_template": "{{ false }}"}],
            "sequence": {"stop": "branche inerte"}}})
        errs_b = _tous_controles(m_b, rt0)
        assert not any("Traceback" in e for e in errs_b)
        c.viole(errs_b, "ASP-CI-25",
                f"m-C bis site — mapping nu devant l'{libelle}")

    # (iv) type INVALIDE : diagnostic avec chemin, jamais un traceback.
    for valeur, quoi in ((42, "int"), ("texte", "str")):
        m_i = copy.deepcopy(mot0)
        seq_i = m_i[ID_MOTEUR]["sequence"]
        i_v = next(i for i, s in enumerate(seq_i)
                   if isinstance(s, dict) and isinstance(s.get("variables"), dict)
                   and any(k.startswith("g2_") for k in s["variables"]))
        seq_i.insert(i_v + 1, {"choose": valeur})
        c.viole(_tous_controles(m_i, rt0), f"de type {quoi}",
                f"m-C bis `choose` de type {quoi} — diagnostiqué")

    # (v) liste VIDE là où une branche est attendue : diagnostic, pas
    #     d'`IndexError`.
    m_v = copy.deepcopy(mot0)
    seq_v = m_v[ID_MOTEUR]["sequence"]
    i_v = next(i for i, s in enumerate(seq_v)
               if isinstance(s, dict) and isinstance(s.get("variables"), dict)
               and any(k.startswith("g2_") for k in s["variables"]))
    seq_v.insert(i_v + 1, {"choose": []})
    c.viole(_tous_controles(m_v, rt0), "AUCUNE branche",
            "m-C bis `choose` vide — diagnostiqué, sans IndexError")

    # (vi) ANTI-RÉGRESSION — aucun accès direct à `choose` hors `_ensure_list`.
    #      Vérifié sur l'AST du module lui-même : la forme du code ne peut
    #      plus régresser sans que ce test tombe.
    source = Path(__file__).read_text(encoding="utf-8")
    arbre = ast.parse(source)
    ligne_selftest = next(n.lineno for n in ast.walk(arbre)
                          if isinstance(n, ast.FunctionDef) and n.name == "selftest")
    enveloppes = {id(a) for n in ast.walk(arbre)
                  if isinstance(n, ast.Call)
                  and getattr(n.func, "id", None) == "_ensure_list"
                  for a in n.args[:1]}
    nus = []
    for n in ast.walk(arbre):
        if not isinstance(n, ast.Subscript):
            continue
        cle = getattr(n.slice, "value", None)
        if cle != "choose" or n.lineno >= ligne_selftest:
            continue
        if id(n) not in enveloppes:
            nus.append(n.lineno)
    assert not nus, (
        f"m-C bis : accès direct à `choose` hors `_ensure_list()` aux lignes "
        f"{nus} — un mapping nu y ferait itérer les CLÉS, ou lever. La "
        f"primitive de normalisation est unique et doit être traversée.")
    c.conformes += 1

    # Cohérence des deux ancres : l'allowlist de retypage doit contenir
    # exactement les trois instants, plus `passages_int`.
    assert VARIABLES_NUMERIQUES_ADMISES == {"passages_int"} | set(
        INSTANTS_PREPARATOIRES), \
        "VARIABLES_NUMERIQUES_ADMISES et INSTANTS_PREPARATOIRES divergent"
    c.conformes += 1

    # ═════════════════════════════════════════════════════════
    # MAINTENANCE — ASP-CI-29 … ASP-CI-33 (lot M0)
    #
    # F1 : les fixtures sont le CHAPITRE REEL et le CHAPITRE 08 REEL, pas un
    # texte plat reconstruit. Une garde qui passe sur une fixture simplifiee
    # ne prouve rien sur le contrat qu'elle protege.
    #
    # Chaque mutation part du chapitre conforme et n'altere QU'UNE structure.
    # Des LEURRES sont injectes : les mots-cles cherches subsistent ailleurs
    # dans le chapitre, si bien qu'un `in` global resterait vert — c'est
    # exactement le faux vert que l'audit a demontre.
    # ═════════════════════════════════════════════════════════

    dom_m0 = load_domain()
    T14 = sans_clotures(dom_m0).get(FICHIER_ENTRETIEN, "")
    T08 = sans_clotures(dom_m0).get(FICHIER_ETATS, "")
    REL = (RELEVE_ENTRETIEN.read_text(encoding="utf-8", errors="ignore")
           if RELEVE_ENTRETIEN.is_file() else "")
    assert T14 and T08 and REL, "selftest M0 : sources reelles introuvables"

    # Leurres : chaque mot-cle des gardes est REPETE hors de sa structure.
    LEURRE = ("\n\nNote de relecture — leurres deliberes : non evaluable, "
              "non du, du, Lovelace, automation, repeat, device_id, "
              "postcondition, relecture, une seule pression, "
              "Aucune historisation, statistiques d'usage, "
              "un seul objet, Entretien du, Cycle en cours, "
              "Erreur robot ou dock, 30 s.\n")
    T14L, T08L = T14 + LEURRE, T08 + LEURRE

    # ---- ASP-CI-29 : périmètre et entités ------------------------------
    c.conforme(check_perimetre_entretien(T14, REL), "CI-29 chapitre reel")
    c.conforme(check_perimetre_entretien(T14L, REL), "CI-29 leurres tolérés")
    c.viole(check_perimetre_entretien("", REL), "chapitre 14 introuvable",
            "CI-29 chapitre absent")
    c.viole(check_perimetre_entretien(T14, ""), "relevé d'attestation",
            "CI-29 relevé absent")
    _cap0 = sorted(CAPTEURS_ENTRETIEN)[0]
    _bt0 = sorted(BOUTONS_ENTRETIEN)[0]
    c.viole(check_perimetre_entretien(T14.replace(_cap0, "sensor.autre_chose"), REL),
            "ABSENT du chapitre 14", "CI-29 capteur retiré")
    c.viole(check_perimetre_entretien(T14, REL.replace(_bt0, "button.autre_chose")),
            "n'est pas attesté par le relevé", "CI-29 bouton non attesté")
    # F3 — cinquieme entite AJOUTEE, contrat ET releve coordonnes.
    _cinq = ("\n| **Moteur** | `sensor.roborock_q7_max_usure_moteur_principal` | "
             "`button.roborock_q7_max_reset_filtre_hepa` |\n")
    c.viole(check_perimetre_entretien(T14 + _cinq, REL + _cinq),
            "hors de la liste fermée", "F3/CI-29 cinquième entité coordonnée")
    c.viole(check_perimetre_entretien(
        T14.replace(_cap0, "sensor.roborock_q7_max_usure_moteur_principal"),
        REL.replace(_cap0, "sensor.roborock_q7_max_usure_moteur_principal")),
        "ASP-CI-29", "F3/CI-29 substitution de capteur")
    c.viole(check_perimetre_entretien(
        T14.replace(_bt0, "button.roborock_q7_max_reset_filtre_hepa"),
        REL.replace(_bt0, "button.roborock_q7_max_reset_filtre_hepa")),
        "ASP-CI-29", "F3/CI-29 substitution de bouton")
    c.viole(check_perimetre_entretien(T14.replace("**150 h**", "**540000 s**"), REL),
            "en HEURES", "CI-29 plafond en secondes")

    # ---- ASP-CI-30 : échéance -------------------------------------------
    c.conforme(check_echeance_entretien(T14), "CI-30 chapitre reel")
    c.conforme(check_echeance_entretien(T14L), "CI-30 leurres tolérés")
    # F1-a : la ligne « non evaluable » devient « non du » DANS LE TABLEAU,
    # alors que les deux libelles subsistent ailleurs (leurres).
    c.viole(check_echeance_entretien(T14L.replace(
        "| **non évaluable** | la mesure est **indisponible** ou inconnue |",
        "| **non dû** | la mesure est **indisponible** ou inconnue |")),
        "ASP-CI-30", "F1-a/CI-30 indisponible classée « non dû »")
    c.viole(check_echeance_entretien(T14L.replace(
        "| **non évaluable** | la mesure est **indisponible** ou inconnue |\n", "")),
        "trois situations", "F1/CI-30 ligne supprimée")
    c.viole(check_echeance_entretien(T14.replace(
        "inférieur ou égal à 10 %", "inférieur ou égal à 15 %")),
        "n'admet que 10 %", "CI-30 seuil faux")
    c.viole(check_echeance_entretien(T14L.replace(
        "**Le même\n> seuil s'applique aux quatre postes**", "**Chaque poste a le sien**")),
        "phrase normative", "F1/CI-30 uniformité supprimée")
    c.viole(check_echeance_entretien(T14L.replace(
        "**ni la dernière valeur\n> connue**", "**sinon la précédente**")),
        "dernière valeur connue", "CI-30 indispo assimilée")
    c.viole(check_echeance_entretien(T14L.replace(
        "**Aucune anticipation prédictive.**", "**Une projection est admise.**")),
        "anticipation prédictive", "CI-30 prédiction non exclue")

    # ---- ASP-CI-31 : primitive irréversible ------------------------------
    c.conforme(check_primitive_irreversible(T14, {}, {}), "CI-31 chapitre reel")
    c.conforme(check_primitive_irreversible(T14L, {}, {}), "CI-31 leurres tolérés")
    # F1-b : la phrase d'exclusivite est affaiblie, « un seul objet » restant
    # present dans les leurres.
    c.viole(check_primitive_irreversible(T14L.replace(
        "n'est appelable que par **un seul objet**",
        "est appelable par **tout objet**"), {}, {}),
        "phrase normative d'exclusivité", "F1-b/CI-31 exclusivité affaiblie")
    # F1-c : la LIGNE interdisant Lovelace est supprimee, le mot subsistant.
    c.viole(check_primitive_irreversible(T14L.replace(
        "| Appel depuis un **fichier Lovelace** ou un gabarit de carte | sans exception |\n",
        ""), {}, {}),
        "aucune ligne interdisant", "F1-c/CI-31 ligne Lovelace supprimée")
    c.viole(check_primitive_irreversible(T14L.replace(
        "| Appel depuis une **automation** | sans exception |\n", ""), {}, {}),
        "aucune ligne interdisant", "F1/CI-31 ligne automation supprimée")
    c.viole(check_primitive_irreversible(T14L.replace(
        "| **Boucle**, `repeat`, retry, seconde pression | sans exception |\n", ""), {}, {}),
        "aucune ligne interdisant", "F1/CI-31 ligne repeat supprimée")
    # F2 : le bouton interdit, dans chaque famille nouvellement couverte.
    _presse = f"  - action: button.press\n    entity_id: {_bt0}\n"
    for _f in ("configuration.yaml",
               "blueprints/automation/homeassistant/motion_light.yaml",
               "esphome/esp32-ble-proxy-1.yaml",
               "11_automations/aspirateur/x.yml"):
        c.viole(check_primitive_irreversible(T14, {_f: _presse}, {}),
                "hors allowlist nominative", f"F2/CI-31 pression dans {_f}")
    c.viole(check_primitive_irreversible(T14, {}, {"18_lovelace/y.yaml": _presse}),
            "hors allowlist nominative", "F2/CI-31 pression dans Lovelace")
    c.conforme(check_primitive_irreversible(
        T14, {"11_automations/z.yaml": f"# {_bt0} en commentaire\n"}, {}),
        "CI-31 mention en commentaire ignorée")

    # ---- F4/F8 : le verrou, DESSERRE PAR CE QUI LE REMPLACE ---------------
    # Le lot M2 leve le verrou en livrant le visiteur recursif. Le verrou
    # n'est pas SUPPRIME : il reste arme, et il se REFERME de lui-meme si le
    # visiteur regresse. C'est ce que les deux cas ci-dessous prouvent — le
    # desserrage n'est pas une modification de constante, c'est une
    # conditionnalite.
    global ALLOWLIST_PRESSION, VISITEUR_YAML_RECURSIF
    _sauv_allow, _sauv_vis = ALLOWLIST_PRESSION, VISITEUR_YAML_RECURSIF
    try:
        # (a) Visiteur regresse + allowlist non vide -> le verrou se referme.
        VISITEUR_YAML_RECURSIF = False
        _verrou = check_primitive_irreversible(T14, {}, {})
        c.viole(_verrou, "VERROU M0",
                "F4/CI-31 verrou refermé si le visiteur régresse")
        assert len(_verrou) == 1, \
            "F4 : le verrou doit court-circuiter TOUTE autre analyse"
        c.conformes += 1
        # (b) Visiteur complet + allowlist vide -> analyse normale.
        VISITEUR_YAML_RECURSIF = True
        ALLOWLIST_PRESSION = frozenset()
        c.conforme(check_primitive_irreversible(T14, {}, {}),
                   "F4/CI-31 allowlist vide : analyse normale")
        # (c) Autorisation DORMANTE : un fichier autorise qui n'existe pas.
        ALLOWLIST_PRESSION = frozenset({"10_scripts/aspirateur/fantome.yaml"})
        c.viole(check_primitive_irreversible(T14, {}, {}),
                "autorisation dormante",
                "F4/CI-31 allowlist nommant un fichier absent")
    finally:
        ALLOWLIST_PRESSION, VISITEUR_YAML_RECURSIF = _sauv_allow, _sauv_vis
    c.conforme(check_primitive_irreversible(T14, {}, {}),
               "F4/CI-31 état livré : allowlist M2, visiteur complet")

    # ---- ASP-CI-32 : séquence de remise à zéro ---------------------------
    c.conforme(check_remise_a_zero(T14), "CI-32 chapitre reel")
    c.conforme(check_remise_a_zero(T14L), "CI-32 leurres tolérés")
    # F1-d : l'ETAPE de relecture est supprimee du tableau, le mot subsistant.
    c.viole(check_remise_a_zero(T14L.replace(
        "| 3 | Relecture | Observation de la postcondition pendant **30 s au plus** |\n",
        "")), "séquence", "F1-d/CI-32 étape de relecture supprimée")
    # Ordre normatif : observer avant d'emettre est refuse.
    c.viole(check_remise_a_zero(T14L.replace(
        "| 2 | Émission | **Une seule pression** sur le **bouton exact** du poste |\n"
        "| 3 | Relecture | Observation de la postcondition pendant **30 s au plus** |\n",
        "| 2 | Relecture | Observation de la postcondition pendant **30 s au plus** |\n"
        "| 3 | Émission | **Une seule pression** sur le **bouton exact** du poste |\n")),
        "dans cet ordre", "F1/CI-32 ordre inversé")
    c.viole(check_remise_a_zero(T14L.replace(
        "| 2 | Émission | **Une seule pression** sur le **bouton exact** du poste |",
        "| 2 | Émission | Des pressions successives sur le **bouton exact** |")),
        "une seule pression", "CI-32 pression non unique")
    c.viole(check_remise_a_zero(T14L.replace(
        "pendant **30 s au plus**", "pendant **45 s au plus**")),
        "hors des constantes admises", "CI-32 durée non admise")
    c.viole(check_remise_a_zero(T14L.replace(
        "**Aucun retry**", "**Un retry est admis**")),
        "l'interdiction de retry", "CI-32 retry non interdit")
    c.viole(check_remise_a_zero(T14L.replace(
        "le poste **reste dû** ;", "le poste est soldé ;")),
        "maintien du poste", "CI-32 poste soldé à tort")
    c.viole(check_remise_a_zero(T14L.replace(
        "**ne conclut à aucune panne matérielle**", "**déclare le matériel en panne**")),
        "refus de conclure à la panne", "CI-32 panne conclue")
    c.viole(check_remise_a_zero(T14L.replace(
        "> geste manuel.**", "> relance automatique.**")),
        "reprise par geste manuel", "CI-32 relance automatique")

    # ---- ASP-CI-33 : notifications ---------------------------------------
    c.conforme(check_notifications_entretien(T14, T08), "CI-33 chapitres reels")
    c.conforme(check_notifications_entretien(T14L, T08L), "CI-33 leurres tolérés")
    # F1-e : la PUCE d'exclusion d'historisation est supprimee du 08, le mot
    # subsistant dans les leurres.
    c.viole(check_notifications_entretien(T14, "\n".join(
        l for l in T08L.splitlines()
        if not l.startswith("- **Aucune historisation.**"))),
        "exclusion d'historisation", "F1-e/CI-33 puce historisation supprimée")
    c.viole(check_notifications_entretien(T14, "\n".join(
        l for l in T08L.splitlines()
        if not l.startswith("- **Aucune position cartographique fine**"))),
        "exclusion de la position", "F1/CI-33 puce position supprimée")
    c.viole(check_notifications_entretien(T14, T08L.replace(
        "statistiques\n  d'usage", "toute mesure")),
        "statistiques d'usage", "CI-33 amendement 08 trop large")
    c.viole(check_notifications_entretien(T14, T08L.replace(
        "[`14`](14_entretien.md)", "un chapitre à venir")),
        "ne renvoie pas au", "CI-33 renvoi absent")
    c.viole(check_notifications_entretien(T14L.replace(
        "| **Entretien dû** | état durable | **persistant** — projection du lot `N1` |\n",
        ""), T08), "ligne propre", "F1/CI-33 objet retiré du cloisonnement")
    c.viole(check_notifications_entretien(T14L.replace(
        "**Aucune notification ajoutée**", "**Une notification est émise**"), T08),
        "AUCUNE", "CI-33 notification hors mission")


    # ═══════════════════════════════════════════════════════════════════
    # U0 — ASP-CI-28, joue sur les SEPT FICHIERS REELS de la couche
    # d'intention. Les mutations portent sur ce qui est livre : une
    # reecriture de la seconde materialisation fera ECHOUER cette batterie
    # plutot que passer en silence. C'est tout l'objet d'`A-13`.
    # ═══════════════════════════════════════════════════════════════════

    U0_0 = load_runtime_u0()
    T10R = doc0["10_raccourcis.md"]

    def u0_mut(rel: str, vieux: str, neuf: str) -> dict[str, str]:
        assert vieux in U0_0[rel], f"ancre U0 absente de {rel} : {vieux[:60]}"
        copie = dict(U0_0)
        copie[rel] = U0_0[rel].replace(vieux, neuf, 1)
        return copie

    def ci28(u0):
        return check_referentiel_intention(t02r, T10R, corps0, u0)

    c.conforme(ci28(U0_0), "CI-28 couche d'intention livree conforme")

    # ---- la couche doit exister en entier ---------------------------------
    c.viole(ci28({k: v for k, v in U0_0.items() if k != FICHIER_U0_SEGMENTS}),
            "incomplete", "CI-28 fichier de segments absent")

    # ---- les quatorze booleens : cle, carte, libelle ----------------------
    c.viole(ci28(u0_mut(FICHIER_U0_SEGMENTS,
                        "aspirateur_segment_0_16:", "aspirateur_segment_16:")),
            "paire canonique", "CI-28 index nu")
    c.viole(ci28(u0_mut(FICHIER_U0_SEGMENTS,
                        "Aspirateur — RDC — Séjour",
                        "Aspirateur — RDC — Salon")),
            "libelle canonique", "CI-28 libelle Roborock restitue")
    c.viole(ci28(u0_mut(FICHIER_U0_SEGMENTS,
                        "Aspirateur — Étage — WC Étage",
                        "Aspirateur — RDC — WC Étage")),
            "attendu", "CI-28 carte affichee fausse")
    c.viole(ci28(u0_mut(FICHIER_U0_SEGMENTS,
                        "aspirateur_segment_1_22:\n"
                        "  name: \"Aspirateur — Étage — WC Étage\"\n\n", "")),
            "le chapitre 02 §2 en compte", "CI-28 quatorzieme segment retire")
    c.viole(ci28(u0_mut(FICHIER_U0_SEGMENTS,
                        "aspirateur_segment_2_19:",
                        "aspirateur_segment_2_18:")),
            "en compte", "CI-28 segment hors referentiel V1")

    # ---- `initial:` reste interdit sur les dix-sept helpers ---------------
    c.viole(ci28(u0_mut(FICHIER_U0_CARTE,
                        "  options:", "  initial: Annexe\n  options:")),
            "initial", "CI-28 cle initiale sur un selecteur")

    # ---- les trois selecteurs ---------------------------------------------
    # Le scalaire plain de YAML mange l'espace finale : seule une valeur
    # CITEE peut la porter jusqu'a l'interface. C'est donc la forme citee que
    # la garde doit attraper — l'autre n'existe pas.
    c.viole(ci28(u0_mut(FICHIER_U0_CARTE, "    - Étage\n", '    - "Étage "\n')),
            "espace de bord", "CI-28 espace finale de la carte 1 en interface")
    c.viole(ci28(u0_mut(FICHIER_U0_PASSAGES,
                        "    - 3 passages\n", "    - 4 passages\n")),
            "attendu", "CI-28 quatrieme passage")
    c.viole(ci28(u0_mut(FICHIER_U0_PROFIL,
                        "    - Aspiration turbo\n", "    - Turbo\n")),
            "selecteur expose", "CI-28 vocabulaire de profil parallele")

    # ---- le mapping paire -> booleen --------------------------------------
    c.viole(ci28(u0_mut(FICHIER_U0_COMPOSITION,
                        "helper: input_boolean.aspirateur_segment_0_18",
                        "helper: input_boolean.aspirateur_segment_0_20")),
            "est associee a", "CI-28 mapping croise")
    c.viole(ci28(u0_mut(FICHIER_U0_COMPOSITION,
                        '"Étage": "1"', '"Étage": "2"')),
            "traduction des cartes", "CI-28 traduction de carte fausse")
    c.viole(ci28(u0_mut(FICHIER_U0_COMPOSITION,
                        '"Aspiration turbo": "aspiration_turbo"',
                        '"Aspiration turbo": "turbo"')),
            "le moteur connait", "CI-28 cle de profil inconnue du moteur")

    # ---- les trois raccourcis et leurs deux reglages par defaut -----------
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        'rdc_serpilliere:', 'rdc_serpillere:')),
            "attendu exactement", "CI-28 cle de raccourci renommee")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        'segments: ["0_16", "0_18", "0_20", "0_21"]',
                        'segments: ["0_16", "0_18", "0_20"]')),
            "le perimetre", "CI-28 perimetre ampute")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        'segments: ["0_16", "0_18", "0_20", "0_21"]',
                        'segments: ["0_16", "0_18", "0_20", "1_16"]')),
            "mono-carte", "CI-28 raccourci multi-carte")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        '            carte: "Étage"',
                        '            carte: "Annexe"')),
            "ne vaut pas l'index", "CI-28 carte du raccourci incoherente")
    # Les DEUX reglages sont desormais EXIGES, et confrontes au 10 §3.1.
    # Les autoriser n'est pas les laisser libres : un raccourci qui propose
    # autre chose que ce que le contrat lui attribue est refuse.
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        '            profil: "Serpillière moyenne"\n', "")),
            "ne propose aucun `profil`", "CI-28 reglage par defaut absent")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        '            profil: "Serpillière moyenne"',
                        '            profil: "Aspiration turbo"')),
            "le 10 §3.1 attribue", "CI-28 profil different du contrat")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        '            passages: "3 passages"',
                        '            passages: "1 passage"')),
            "le 10 §3.1 attribue", "CI-28 passages differents du contrat")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        '            passages: "3 passages"\n'
                        '          etage_aspiration:',
                        '            passages: "3 passages"\n'
                        '            lancer: true\n'
                        '          etage_aspiration:')),
            "porte le champ `lancer`", "CI-28 raccourci qui porterait un lancement")
    c.viole(ci28(u0_mut(FICHIER_U0_RACCOURCI,
                        '          - "2_19"\n', "")),
            "liste complete", "CI-28 liste d'extinction incomplete")

    # ---- la remise a zero eteint les quatorze -----------------------------
    c.viole(ci28(u0_mut(FICHIER_U0_REINIT,
                        "          - input_boolean.aspirateur_segment_2_19\n",
                        "")),
            "attendu les quatorze", "CI-28 remise a zero incomplete")

    # ═══════════════════════════════════════════════════════════════════
    # M1 — ASP-CI-34 / 35 / 36, joues sur le FICHIER RUNTIME REEL
    #
    # Les mutations portent sur le fichier tel qu'il est livre, jamais sur un
    # gabarit de laboratoire : une reecriture du runtime fera ECHOUER cette
    # batterie plutot que passer en silence. C'est la direction sure.
    # ═══════════════════════════════════════════════════════════════════

    M1_0 = (ROOT / RUNTIME_M1).read_text(encoding="utf-8")

    def m1_mut(vieux: str, neuf: str, tout: bool = False) -> str:
        assert vieux in M1_0, f"ancre M1 absente du runtime réel : {vieux[:70]}"
        return M1_0.replace(vieux, neuf) if tout \
            else M1_0.replace(vieux, neuf, 1)

    # ---- le runtime livre passe les trois controles -----------------------
    c.conforme(check_projection_entretien(M1_0), "CI-34 runtime M1 conforme")
    c.conforme(check_projection_rendue(M1_0), "CI-35 runtime M1 conforme")
    c.conforme(check_interdits_projection(M1_0), "CI-36 runtime M1 conforme")

    # ---- ASP-CI-34 : perimetre, plafonds, seuil, autorite -----------------
    c.viole(check_projection_entretien(""), "introuvable", "CI-34 M1 absent")
    c.viole(check_projection_entretien("- sensor: [\n"), "illisible",
            "CI-34 YAML illisible")
    c.viole(check_projection_entretien(m1_mut("seuil_pct: 10",
                                              "seuil_pct: 11")),
            "UN SEUL", "CI-34 seuil à 11 %")
    c.viole(check_projection_entretien(m1_mut("plafond_h: 300",
                                              "plafond_h: 250")),
            "le contrat en fixe", "CI-34 plafond erroné")
    c.viole(check_projection_entretien(m1_mut(
        "            plafond_h: 30\n",
        "            plafond_h: 30\n"
        "          - nom: \"Bac à poussière\"\n"
        "            source: sensor.roborock_q7_max_temps_restant_bac\n"
        "            plafond_h: 90\n")),
        "exactement", "CI-34 cinquième source")
    c.viole(check_projection_entretien(m1_mut(
        "source: sensor.roborock_q7_max_temps_restant_filtre",
        "source: sensor.roborock_q7_max_batterie")),
        "hors de la liste fermée", "CI-34 source substituée")
    c.viole(check_projection_entretien(m1_mut(
        "          - nom: \"Nettoyage des capteurs\"\n"
        "            source: sensor.roborock_q7_max_temps_restant_capteurs\n"
        "            plafond_h: 30\n", "")),
        "est ABSENT du périmètre", "CI-34 poste supprimé")
    c.viole(check_projection_entretien(m1_mut(
        "        seuil_pourcentage: \"{{ seuil_pct }}\"\n",
        "        seuil_pourcentage: \"{{ seuil_pct }}\"\n"
        "        source_bis: \"{{ "
        "states('sensor.roborock_q7_max_temps_restant_filtre') }}\"\n")),
        "est déclarée 2 fois", "CI-34 seconde déclaration d'une source")
    c.viole(check_projection_entretien(m1_mut(
        "        {{ state_attr('sensor.aspirateur_entretien_du',\n"
        "                      'postes_dus') | count > 0 }}",
        "        {{ states('sensor.roborock_q7_max_temps_restant_capteurs')\n"
        "           | float < 3 }}")),
        "seconde autorité de calcul", "CI-34 témoin qui recalcule")
    c.viole(check_projection_entretien(m1_mut(
        "      availability: >\n", "      indisponible_si: >\n")),
        "availability", "CI-34 témoin sans disponibilité")
    c.viole(check_projection_entretien(m1_mut(
        "        postes_non_evaluables: >", "        postes_illisibles: >")),
        "exactement", "CI-34 attribut renommé")
    c.viole(check_projection_entretien(m1_mut(
        "      default_entity_id: sensor.aspirateur_entretien_du",
        "      default_entity_id: sensor.aspirateur_entretien")),
        "n'épingle pas son identifiant", "CI-34 identifiant déplacé")
    c.viole(check_projection_entretien(m1_mut(
        "      unique_id: aspirateur_entretien_requis",
        "      unique_id: aspirateur_entretien_binaire")),
        "témoin binaire `aspirateur_entretien_requis` est absent",
        "CI-34 témoin renommé")

    # ---- ASP-CI-35 : les trois situations, RENDUES ------------------------
    #
    # Ces mutations laissent la STRUCTURE intacte : le périmètre, les
    # plafonds et le seuil déclaré restent exacts. Seul le rendu change — et
    # c'est le rendu qui les attrape.
    c.viole(check_projection_rendue(m1_mut(
        "else 'non_evaluable' if ns.illisibles", "else 'aucun' if ns.illisibles")),
        "attendu 'non_evaluable'", "CI-35 indisponibilité rabattue sur `aucun`")
    c.viole(check_projection_rendue(m1_mut(
        "            {% if not states(p.source) | is_number %}",
        "            {% if false %}")),
        "postes_non_evaluables", "CI-35 troisième situation vidée")
    c.viole(check_projection_rendue(m1_mut(
        "{{ dus is not none and illisibles is not none\n"
        "           and (dus | count > 0 or illisibles | count == 0) }}",
        "{{ dus is not none }}")),
        "attendu INDISPONIBLE", "CI-35 témoin toujours disponible")
    c.viole(check_projection_rendue(m1_mut(
        "p.plafond_h * seuil_pct / 100", "p.plafond_h * 5 / 100", tout=True)),
        "rend l'état", "CI-35 seuil recopié en dur dans les gabarits")
    c.viole(check_projection_rendue(m1_mut(
        "{% if (s | float) <= p.plafond_h * seuil_pct / 100 %}",
        "{% if (s | float) < p.plafond_h * seuil_pct / 100 %}")),
        "seuil atteint pile", "CI-35 seuil rendu strict")
    c.viole(check_projection_rendue(m1_mut(
        "'restant_h': none,", "'restant_h': 0,")),
        "valeur de repli est apparue", "CI-35 restant nul sur un illisible")
    c.viole(check_projection_rendue(m1_mut(
        "{% set s = states(p.source) %}\n"
        "          {% if s | is_number %}\n"
        "            {% if (s | float) <= p.plafond_h * seuil_pct / 100 %}\n"
        "              {% set ns.dus = ns.dus + [p.nom] %}\n"
        "            {% endif %}\n"
        "          {% else %}\n"
        "            {% set ns.illisibles = ns.illisibles + [p.nom] %}\n"
        "          {% endif %}",
        "{% set s = states(p.source) %}\n"
        "          {% if s | is_number and (s | float)\n"
        "                <= p.plafond_h * seuil_pct / 100 %}\n"
        "            {% set ns.dus = ns.dus + [p.nom] %}\n"
        "          {% endif %}")),
        "attendu 'non_evaluable'", "CI-35 branche illisible supprimée")

    # ---- ASP-CI-36 : ce que M1 ne fait pas --------------------------------
    c.viole(check_interdits_projection(""), "introuvable", "CI-36 M1 absent")
    c.viole(check_interdits_projection(m1_mut(
        "(s | float)", "(s | float(0))", tout=True)),
        "repli numérique", "CI-36 `| float(0)`")
    c.viole(check_interdits_projection(m1_mut(
        "| round(3)", "| default(0) | round(3)")),
        "repli numérique", "CI-36 `| default(0)`")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n      action: button.press\n")),
        "clé de service", "CI-36 button.press ajouté")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n      action: vacuum.start\n")),
        "clé de service", "CI-36 commande robot ajoutée")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n"
        "      declencheur: vacuum.roborock_q7_max\n")),
        "vacuum.roborock_q7_max", "CI-36 entité robot citée")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n"
        "      bouton: "
        "button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air\n")),
        "il ne remet rien à zéro", "CI-36 bouton d'entretien cité")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n      canal: persistent_notification\n")),
        "M1 ne notifie pas", "CI-36 notification ajoutée")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n      verdict: \"{{ states('"
        + ID_VERDICT + "') }}\"\n")),
        "ne lit ni n'écrit le verdict", "CI-36 lecture du verdict")
    c.viole(check_interdits_projection(m1_mut(
        "      icon: mdi:broom\n",
        "      icon: mdi:broom\n      trace: \"{{ states('"
        + ID_TRACE + "') }}\"\n")),
        "ne lit ni n'écrit le verdict", "CI-36 lecture de la trace")
    c.viole(check_interdits_projection(m1_mut(
        "{{ ns.dus | join(', ') if ns.dus",
        "{{ now().timestamp() }}{{ ns.dus | join(', ') if ns.dus")),
        "aucune tendance", "CI-36 prédiction ajoutée")
    c.viole(check_interdits_projection(m1_mut(
        "{% set s = states(p.source) %}\n"
        "            {% if s | is_number %}\n"
        "              {% set ns.items = ns.items + [{\n"
        "                'poste': p.nom,",
        "{% set s = states(p.source) %}\n"
        "            {% if s %}\n"
        "              {% set ns.items = ns.items + [{\n"
        "                'poste': p.nom,")),
        "sans la garde `is_number`", "CI-36 garde d'illisibilité retirée")


    # ---- Revue ciblée : les deux angles morts d'ASP-CI-35, et l'icône -----
    #
    # Toutes ces mutations SURVIVAIENT au checker de `f94108f2` : elles ne
    # touchaient ni au cardinal des listes, ni au plafond restitué, ni à la
    # structure — les seules choses que le contrôle regardait alors. Elles
    # sont ici pour qu'aucune ne revienne.

    NON_DUS = ("        postes_non_dus: >\n"
               "          {% set ns = namespace(items=[]) %}\n"
               "          {% for p in perimetre %}\n"
               "            {% set s = states(p.source) %}\n"
               "            {% if s | is_number and (s | float) > "
               "p.plafond_h * seuil_pct / 100 %}\n"
               "              {% set ns.items = ns.items + [p.nom] %}\n"
               "            {% endif %}\n"
               "          {% endfor %}\n"
               "          {{ ns.items }}\n")

    # ── §2 : la liste `postes_non_dus`, valeur par valeur ─────────────────
    c.viole(check_projection_rendue(m1_mut(
        NON_DUS, NON_DUS.replace("+ [p.nom] %}", "+ [p.source] %}"))),
        "identifiant d'entité", "CI-35 non_dus rend des entity_id")
    c.viole(check_projection_rendue(m1_mut(
        NON_DUS, NON_DUS.replace("+ [p.nom] %}", "+ [perimetre[0].nom] %}"))),
        "doublons", "CI-35 non_dus répète le premier libellé")
    c.viole(check_projection_rendue(m1_mut(
        NON_DUS, NON_DUS.replace("+ [p.nom] %}",
                                 "+ [p.nom ~ ' (à voir)'] %}"))),
        "hors du vocabulaire Arsenal", "CI-35 libellé substitué")
    c.viole(check_projection_rendue(m1_mut(
        "          {{ ns.items }}\n\n        # La troisième situation",
        "          {{ ns.items | reverse | list }}\n\n"
        "        # La troisième situation")),
        "ordre canonique", "CI-35 ordre de non_dus inversé")
    c.viole(check_projection_rendue(m1_mut(
        NON_DUS, NON_DUS.replace(
            "{% if s | is_number and (s | float) > "
            "p.plafond_h * seuil_pct / 100 %}",
            "{% if s | is_number %}"))),
        "se recoupent", "CI-35 un poste dans deux listes")
    c.viole(check_projection_rendue(m1_mut(
        NON_DUS, NON_DUS.replace(
            "p.plafond_h * seuil_pct / 100 %}",
            "p.plafond_h * seuil_pct / 100\n"
            "                  and p.nom != perimetre[0].nom %}"))),
        "nulle part", "CI-35 un poste dans aucune liste")

    # ── §3 : la charge numérique de `postes` ──────────────────────────────
    c.viole(check_projection_rendue(m1_mut(
        "'restant_h': (s | float) | round(3),",
        "'restant_h': (s | float * 2) | round(3),")),
        "`restant_h`", "CI-35 restant_h doublé")
    c.viole(check_projection_rendue(m1_mut(
        "'restant_h': (s | float) | round(3),",
        "'restant_h': (s | float * 3600) | round(3),")),
        "rendue en HEURES", "CI-35 restant_h en secondes")
    c.viole(check_projection_rendue(m1_mut(
        "'restant_pourcentage': ((s | float) / p.plafond_h * 100)",
        "'restant_pourcentage': ((s | float) / (p.plafond_h * 2) * 100)")),
        "restant_pourcentage", "CI-35 mauvais diviseur")
    c.viole(check_projection_rendue(m1_mut(
        "'restant_pourcentage': ((s | float) / p.plafond_h * 100)\n"
        "                                       | round(2) }] %}",
        "'restant_pourcentage': ((s | float) / p.plafond_h * 100)\n"
        "                                       | round(0) }] %}")),
        "au-delà de l'arrondi", "CI-35 pourcentage arrondi à l'entier")
    c.viole(check_projection_rendue(m1_mut(
        "'restant_pourcentage': ((s | float) / p.plafond_h * 100)\n"
        "                                       | round(2) }] %}",
        "'restant_pourcentage': 50 }] %}")),
        "restant_pourcentage", "CI-35 pourcentage constant")
    c.viole(check_projection_rendue(m1_mut(
        "'plafond_h': p.plafond_h,\n"
        "                'restant_pourcentage':",
        "'plafond_h': perimetre[(loop.index0 + 1) % 4].plafond_h,\n"
        "                'restant_pourcentage':")),
        "plafond restitué", "CI-35 plafond restitué permuté")

    # ── §4 : l'icône, dérivée de l'autorité ───────────────────────────────
    ICONE = ("        {{ 'mdi:broom'\n"
             "           if state_attr('sensor.aspirateur_entretien_du', "
             "'postes_dus')\n"
             "           else 'mdi:check-circle-outline' }}")
    c.viole(check_projection_entretien(m1_mut(
        ICONE,
        "        {{ 'mdi:broom'\n"
        "           if is_state('binary_sensor.aspirateur_entretien_requis', "
        "'on')\n"
        "           else 'mdi:check-circle-outline' }}")),
        "se relit lui-même", "CI-34 autoréférence de l'icône réintroduite")
    ECHO = '        seuil_pourcentage: "{{ seuil_pct }}"\n'
    c.viole(check_projection_entretien(m1_mut(
        ECHO, ECHO + '        echo: "{{ '
        "states('sensor.aspirateur_entretien_du') }}\"\n")),
        "se relit elle-même", "CI-34 autorité qui se relit")
    c.viole(check_projection_entretien(m1_mut(
        ECHO, ECHO + '        boucle: "{{ '
        "states('binary_sensor.aspirateur_entretien_requis') }}\"\n")),
        "relit le témoin", "CI-34 cycle autorité → témoin")
    c.viole(check_projection_rendue(m1_mut(ICONE, "        mdi:broom")),
            "l'icône du témoin", "CI-35 icône figée")
    c.viole(check_projection_rendue(m1_mut(
        ICONE,
        "        {{ 'mdi:check-circle-outline'\n"
        "           if state_attr('sensor.aspirateur_entretien_du', "
        "'postes_dus')\n"
        "           else 'mdi:broom' }}")),
        "l'icône du témoin", "CI-35 icône inversée")


    # ═══════════════════════════════════════════════════════════════════
    # N1 — ASP-CI-37 / 38 / 39, joues sur le DOSSIER RUNTIME REEL
    #
    # Comme pour M1, les mutations portent sur le fichier tel qu'il est livre.
    # Une reecriture du writer fera ECHOUER cette batterie plutot que passer
    # en silence.
    # ═══════════════════════════════════════════════════════════════════

    N1_0 = load_runtime_n1()
    M1_REEL = (ROOT / RUNTIME_M1).read_text(encoding="utf-8")
    DEPOT_0 = load_yaml_depot()
    assert N1_0, "selftest N1 : dossier runtime introuvable"
    F_N1 = RUNTIME_N1
    assert F_N1 in N1_0, f"selftest N1 : `{F_N1}` absent du dossier"

    def n1_mut(vieux: str, neuf: str, fichier: str = F_N1,
               tout: bool = False) -> dict[str, str]:
        """Le dossier N1, avec UNE substitution dans UN fichier."""
        base = dict(N1_0)
        src_f = base[fichier]
        assert vieux in src_f, f"ancre N1 absente du runtime réel : {vieux[:70]}"
        base[fichier] = (src_f.replace(vieux, neuf) if tout
                         else src_f.replace(vieux, neuf, 1))
        return base

    def n1_plus(rel: str, contenu: str) -> dict[str, str]:
        """Le dossier N1, augmente d'un fichier — un writer de plus."""
        base = dict(N1_0)
        base[rel] = contenu
        return base

    # ---- le runtime livre passe les trois controles -----------------------
    c.conforme(check_writers_n1(N1_0, DEPOT_0), "CI-37 runtime N1 conforme")
    c.conforme(check_projection_n1_rendue(N1_0, M1_REEL),
               "CI-38 runtime N1 conforme")
    c.conforme(check_interdits_n1(N1_0), "CI-39 runtime N1 conforme")

    # ---- ASP-CI-37 : writers, identifiants, cycle de vie ------------------
    c.viole(check_writers_n1({}, DEPOT_0), "introuvable", "CI-37 N1 absent")
    c.viole(check_writers_n1({F_N1: "- id: [\n"}, DEPOT_0), "illisible",
            "CI-37 YAML illisible")
    c.viole(check_writers_n1(n1_mut(f'- id: "{AID_N1_MAINTENANCE}"',
                                    '- id: "10280000000009"'), DEPOT_0),
            "hors des identifiants attribues au dossier",
            "CI-37 ID d'automation incorrect")
    c.viole(check_writers_n1(n1_mut(f'- id: "{AID_N1_MAINTENANCE}"',
                                    f'- id: "{AID_SUPERVISION}"'), DEPOT_0),
            "un identifiant deplace d'un fichier a l'autre",
            "CI-37 identifiant de supervision porte par le fichier d'entretien")
    # AMENDEMENT U0 — `...04` n'est plus reserve, il est ATTRIBUE a
    # l'automation de remise a zero. Le porter depuis un autre fichier reste
    # refuse, mais par la table `{identifiant -> fichier}` : c'est le
    # deplacement qui est detecte, et non plus l'usage d'un ID interdit.
    c.viole(check_writers_n1(n1_mut(f'- id: "{AID_N1_MAINTENANCE}"',
                                    f'- id: "{AID_U0_COMPOSITION}"'), DEPOT_0),
            "un identifiant deplace d'un fichier a l'autre",
            "CI-37 ID de remise a zero porte par le fichier d'entretien")
    c.viole(check_writers_n1(n1_mut(f'- id: "{AID_N1_MAINTENANCE}"',
                                    f"- id: {AID_N1_MAINTENANCE}"), DEPOT_0),
            "sans `id:` en CHAINE", "CI-37 identifiant en entier")

    # Troisieme writer : un fichier de plus dans le dossier.
    TROISIEME = (f'- id: "{AID_N1_MISSION}"\n'
                 '  alias: "Aspirateur - Notification cycle"\n'
                 '  mode: restart\n'
                 '  trigger:\n'
                 '    - platform: state\n'
                 f'      entity_id: {READINESS_N1}\n'
                 '      to: "on"\n'
                 '  action:\n'
                 '    - service: persistent_notification.create\n'
                 '      data:\n'
                 f'        notification_id: {NOTIF_N1_MISSION}\n'
                 '        title: "\U0001F916 Aspirateur – Cycle en cours"\n'
                 '        message: "Un cycle est en cours."\n')
    c.viole(check_writers_n1(
        n1_plus(DOSSIER_N1 + "/notification_cycle.yaml", TROISIEME), DEPOT_0),
        "un identifiant deplace d'un fichier a l'autre",
        "CI-37 projection de mission logee dans un fichier non attribue")
    QUATRIEME = TROISIEME.replace(f'"{AID_N1_MISSION}"', '"10280000000007"') \
                         .replace(NOTIF_N1_MISSION, NOTIF_N1_ENTRETIEN)
    c.viole(check_writers_n1(
        n1_plus(DOSSIER_N1 + "/troisieme.yaml", QUATRIEME), DEPOT_0),
        "hors des identifiants attribues au dossier",
        "CI-37 writer a identifiant invente")
    c.viole(check_writers_n1(
        n1_plus(DOSSIER_N1 + "/troisieme.yaml", QUATRIEME), DEPOT_0),
        "qu'UN writer", "CI-37 deux writers pour un meme etat metier")
    # Le DECOMPTE, atteint par deux fichiers de plus : trois automations pour
    # deux identifiants attribues. C'est la regle qui attrape un writer de
    # plus meme lorsqu'il emprunte, chacun, un identifiant admis.
    c.viole(check_writers_n1(
        n1_plus(DOSSIER_N1 + "/troisieme.yaml", QUATRIEME
                + "\n" + QUATRIEME.replace('"10280000000007"',
                                            '"10280000000008"')), DEPOT_0),
        "un writer de plus est apparu",
        "CI-37 automation surnumeraire dans le dossier")

    # Un identifiant du domaine cite HORS de la cle `id:` — forme que le
    # parseur YAML ne rattache a aucune automation. L'ancre est un
    # identifiant NON ATTRIBUE : `...04` l'est depuis le lot U0.
    c.viole(check_writers_n1(n1_mut(
        "  mode: restart", "  mode: restart\n  # voir 10280000000005"),
        DEPOT_0), "10280000000005",
        "CI-37 identifiant non attribue cite en commentaire")

    # Identifiant de notification : ferme, stable, non templatise.
    c.viole(check_writers_n1(n1_mut(
        f"notification_id: {NOTIF_N1_ENTRETIEN}",
        "notification_id: aspirateur_entretien_v2", tout=True), DEPOT_0),
        "hors de l'ensemble ferme", "CI-37 notification ID modifie")
    c.viole(check_writers_n1(n1_mut(
        f"notification_id: {NOTIF_N1_ENTRETIEN}\n"
        '                title:',
        'notification_id: "{{ \'aspirateur_entretien\' }}"\n'
        '                title:'), DEPOT_0),
        "TEMPLATISE", "CI-37 notification ID templatise")

    # Creation sans suppression, et suppression sans creation.
    SANS_DISMISS = ("            - service: persistent_notification.dismiss\n"
                    "              data:\n"
                    f"                notification_id: {NOTIF_N1_ENTRETIEN}\n")
    c.viole(check_writers_n1(n1_mut(
        SANS_DISMISS, "            - delay: \"00:00:01\"\n"), DEPOT_0),
        "'dismiss'", "CI-37 creation sans suppression")

    # Readiness, mode, declencheurs, titre, autorite du message.
    c.viole(check_writers_n1(n1_mut(
        "    - platform: state\n"
        f"      entity_id: {READINESS_N1}\n"
        '      to: "on"\n', ""), DEPOT_0),
        "declencheur", "CI-37 absence du trigger systeme_stable")
    c.viole(check_writers_n1(n1_mut(
        f'      entity_id: {READINESS_N1}\n      to: "on"',
        f'      entity_id: {READINESS_N1}'), DEPOT_0),
        "declencheur", "CI-37 readiness sans `to: on`")
    c.viole(check_writers_n1(n1_mut("  mode: restart", "  mode: single"),
                             DEPOT_0),
            "abandonnerait EN SILENCE", "CI-37 mode single")
    c.viole(check_writers_n1(n1_mut(
        f"      entity_id: {ENTITE_M1_LISTE}\n",
        "      entity_id: sensor.roborock_q7_max_temps_restant_filtre\n"),
        DEPOT_0), "rythme du coordinateur",
        "CI-37 declencheur sur un capteur natif")
    c.viole(check_writers_n1(n1_mut(
        f'title: "{TITRE_N1_ENTRETIEN}"',
        'title: "\U0001F9F0 Aspirateur — Entretien requis"'), DEPOT_0),
        "attendu", "CI-37 titre au cadratin")
    c.viole(check_writers_n1(n1_mut(
        "'postes_dus') | join(', ') }}",
        "'postes') | join(', ') }}"), DEPOT_0),
        "il ne lit QUE", "CI-37 message qui lit un autre attribut")
    c.viole(check_writers_n1(n1_mut(
        "**Postes dus :** {{ state_attr",
        "**Reste :** {{ states('sensor.roborock_q7_max_temps_restant_filtre') "
        "}} {{ state_attr"), DEPOT_0),
        "lecture libre", "CI-37 message qui lit une entite native")
    DEFAUT = ("      default:\n"
              "        - service: persistent_notification.dismiss\n"
              "          data:\n"
              f"            notification_id: {NOTIF_N1_ENTRETIEN}\n")
    c.viole(check_writers_n1({F_N1: N1_0[F_N1] + DEFAUT}, DEPOT_0),
            "`default:`", "CI-37 branche par defaut reintroduite")
    c.viole(check_projection_n1_rendue({F_N1: N1_0[F_N1] + DEFAUT}, M1_REEL),
            "conclut `dismiss`", "CI-38 branche par defaut qui supprime")

    # Un writer hors domaine qui ecrirait la meme notification.
    c.viole(check_writers_n1(N1_0, dict(
        DEPOT_0, **{"11_automations/modes/intrus.yaml":
                    f"  notification_id: {NOTIF_N1_ENTRETIEN}\n"})),
        "hors du domaine", "CI-37 writer concurrent hors domaine")

    # ---- ASP-CI-37 : le declencheur de liste est BORNE (correctif C-1) -----
    #
    # Un declencheur d'etat sans `to:`, sans `from:` et sans `attribute:`
    # passe en `match_all` cote Home Assistant : il part sur tout changement
    # d'attribut, `postes` compris, donc a chaque decroissance d'un compteur.
    DECL_LISTE = (f"      entity_id: {ENTITE_M1_LISTE}\n"
                  f"      attribute: {ATTRIBUT_N1_DECLENCHEUR}\n")
    c.viole(check_writers_n1(n1_mut(
        DECL_LISTE, f"      entity_id: {ENTITE_M1_LISTE}\n"), DEPOT_0),
        "attribute", "CI-37 declencheur de liste nu (attribut retire)")
    c.viole(check_writers_n1(n1_mut(
        DECL_LISTE,
        f"      entity_id: {ENTITE_M1_LISTE}\n"
        "      attribute: postes\n"), DEPOT_0),
        "attribute", "CI-37 declencheur borne au mauvais attribut `postes`")
    c.viole(check_writers_n1(n1_mut(
        DECL_LISTE,
        f"      entity_id: {ENTITE_M1_LISTE}\n"
        "      attribute: postes_non_dus\n"), DEPOT_0),
        "attribute", "CI-37 declencheur borne a `postes_non_dus`")
    # Le temoin, lui, doit rester generique : le borner a un attribut lui
    # ferait manquer le franchissement de seuil, qui est une transition
    # d'ETAT.
    c.viole(check_writers_n1(n1_mut(
        f"      entity_id: {ENTITE_M1_TEMOIN}\n",
        f"      entity_id: {ENTITE_M1_TEMOIN}\n"
        f"      attribute: {ATTRIBUT_N1_DECLENCHEUR}\n"), DEPOT_0),
        "temoin", "CI-37 declencheur du temoin borne a un attribut")

    # ---- ASP-CI-38 : les huit scenarios, RENDUS ---------------------------
    #
    # Ces mutations laissent la STRUCTURE intacte — identifiants, titre,
    # declencheurs, mode. Seule la CONCLUSION change, et c'est le rendu de la
    # chaine M1 -> N1 qui les attrape.
    c.viole(check_projection_n1_rendue({}, M1_REEL), "introuvable",
            "CI-38 N1 absent")
    c.viole(check_projection_n1_rendue(N1_0, ""), "M1 introuvable",
            "CI-38 autorite M1 disparue")

    # Suppression sur `unknown` / `unavailable` : le piege central du lot.
    SUPPR = ("        - conditions:\n"
             "            - condition: state\n"
             f"              entity_id: {ENTITE_M1_TEMOIN}\n"
             '              state: "off"\n'
             "            - condition: state\n"
             f"              entity_id: {ENTITE_M1_LISTE}\n"
             f'              state: "{ETAT_M1_AUCUN}"\n')
    c.viole(check_projection_n1_rendue(n1_mut(
        SUPPR,
        "        - conditions:\n"
        "            - condition: template\n"
        '              value_template: "{{ true }}"\n'), M1_REEL),
        "conclut `dismiss`", "CI-38 suppression inconditionnelle")
    c.viole(check_projection_n1_rendue(n1_mut(
        SUPPR,
        "        - conditions:\n"
        "            - condition: state\n"
        f"              entity_id: {ENTITE_M1_TEMOIN}\n"
        '              state:\n'
        '                - "off"\n'
        '                - "unavailable"\n'
        '                - "unknown"\n'), M1_REEL),
        "ne consulte pas", "CI-38 suppression sur unavailable/unknown")
    c.viole(check_projection_n1_rendue(n1_mut(
        f'              state: "{ETAT_M1_AUCUN}"\n',
        '              state:\n'
        f'                - "{ETAT_M1_AUCUN}"\n'
        f'                - "{ETAT_M1_NON_EVAL}"\n'), M1_REEL),
        "DEUX faces", "CI-38 non_evaluable traite comme aucun")
    c.viole(check_projection_n1_rendue(n1_mut(
        "            - condition: state\n"
        f"              entity_id: {ENTITE_M1_LISTE}\n"
        f'              state: "{ETAT_M1_AUCUN}"\n', ""), M1_REEL),
        "DEUX faces", "CI-38 suppression sur le seul temoin")

    # Le message se met a dependre de la CHARGE NUMERIQUE : deux releves de
    # meme `postes_dus` ne rendent plus la meme chose. Un reveil deviendrait
    # alors une reecriture reelle, au rythme du coordinateur.
    c.viole(check_projection_n1_rendue(n1_mut(
        f"'{ATTRIBUT_N1_MESSAGE}') | join(', ') }}}}",
        "'postes') | join(', ') }}"), M1_REEL),
        "charge numerique", "CI-38 message indexe sur la charge numerique")

    # La liste des postes dus, ignoree ou remplacee.
    c.viole(check_projection_n1_rendue(n1_mut(
        "**Postes dus :** {{ state_attr('sensor.aspirateur_entretien_du',\n"
        "                  'postes_dus') | join(', ') }}",
        "**Un entretien est du.**"), M1_REEL),
        "le message nomme", "CI-38 liste des postes dus ignoree")
    c.viole(check_projection_n1_rendue(n1_mut(
        "'postes_dus') | join(', ') }}",
        "'postes_non_evaluables') | join(', ') }}"), M1_REEL),
        "ASP-CI-38", "CI-38 message qui nomme les postes illisibles")

    # Un message qui predit ou qui chiffre.
    c.viole(check_projection_n1_rendue(n1_mut(
        "**Postes dus :** {{ state_attr",
        "**Echeance dans 12 h.** {{ state_attr"), M1_REEL),
        "une duree ou un pourcentage", "CI-38 message predisant une date")
    c.viole(check_projection_n1_rendue(n1_mut(
        "**Postes dus :** {{ state_attr",
        "**Reste 4 % du plafond.** {{ state_attr"), M1_REEL),
        "une duree ou un pourcentage", "CI-38 message chiffrant un restant")

    # Le seuil, rejoue cote N1 au lieu d'etre consomme.
    c.viole(check_projection_n1_rendue(n1_mut(
        "            - condition: state\n"
        f"              entity_id: {ENTITE_M1_TEMOIN}\n"
        '              state: "on"\n',
        "            - condition: template\n"
        "              value_template: >\n"
        "                {{ states('sensor.roborock_q7_max_temps_restant_capteurs')\n"
        "                   | float(99) <= 3 }}\n"), M1_REEL),
        "conclut", "CI-38 seuil recalcule cote N1")

    # L'anti-doublon, et le contenu qui doit suivre la liste.
    c.viole(check_projection_n1_rendue(n1_mut(
        f"                notification_id: {NOTIF_N1_ENTRETIEN}\n"
        f'                title: "{TITRE_N1_ENTRETIEN}"',
        "                notification_id: >\n"
        "                  aspirateur_entretien_{{ state_attr(\n"
        "                    'sensor.aspirateur_entretien_du',\n"
        "                    'postes_dus') | count }}\n"
        f'                title: "{TITRE_N1_ENTRETIEN}"'), M1_REEL),
        "identifiants de notification", "CI-38 identifiant qui empile")

    # Le declencheur de readiness, retire : le scenario 6 tombe.
    c.viole(check_projection_n1_rendue(n1_mut(
        "    - platform: state\n"
        f"      entity_id: {READINESS_N1}\n"
        '      to: "on"\n', ""), M1_REEL),
        "redemarrage avec un entretien du",
        "CI-38 reconciliation au readiness absente")

    # ---- ASP-CI-38 : la suppression est FERMEE (correctif C-2) ------------
    #
    # Toutes ces mutations laissent les scenarios nominaux INTACTS : la
    # suppression continue de partir sur `aucun`. Elles n'ajoutent qu'une
    # valeur acceptee de plus — et c'est exactement pour cela qu'aucun
    # scenario ne les attrape, et qu'il faut une garde de FORME.
    ETAT_SCALAIRE = (f"              entity_id: {ENTITE_M1_LISTE}\n"
                     f'              state: "{ETAT_M1_AUCUN}"\n')
    for ajout, nom in ((("unknown"), "unknown"),
                       (("unavailable"), "unavailable"),
                       ((ETAT_M1_NON_EVAL), "non_evaluable")):
        c.viole(check_projection_n1_rendue(n1_mut(
            ETAT_SCALAIRE,
            f"              entity_id: {ENTITE_M1_LISTE}\n"
            "              state:\n"
            f'                - "{ETAT_M1_AUCUN}"\n'
            f'                - "{ajout}"\n'), M1_REEL),
            "LISTE d'etats", f"CI-38 suppression elargie a `{nom}`")
    # Une liste qui ne contient QUE `aucun` reste une liste : la garde refuse
    # la forme, pas seulement les valeurs ajoutees.
    c.viole(check_projection_n1_rendue(n1_mut(
        ETAT_SCALAIRE,
        f"              entity_id: {ENTITE_M1_LISTE}\n"
        "              state:\n"
        f'                - "{ETAT_M1_AUCUN}"\n'
        '                - "aucun_entretien"\n'), M1_REEL),
        "LISTE d'etats", "CI-38 suppression elargie a une valeur voisine")
    # La garde de presence de l'attribut, telle qu'elle est ecrite.
    GARDE_ATTR = (
        "            - condition: template\n"
        "              value_template: >\n"
        f"                {{% set dus = state_attr('{ENTITE_M1_LISTE}',\n"
        f"                                        '{ATTRIBUT_N1_MESSAGE}') %}}\n"
        "                {{ dus is not none and dus | count == 0 }}\n")
    # La condition reduite au SEUL temoin : une face de l'autorite sur deux.
    c.viole(check_projection_n1_rendue(
        n1_mut("            - condition: state\n" + ETAT_SCALAIRE + GARDE_ATTR,
               ""), M1_REEL),
        "ne consulte pas", "CI-38 suppression sur le seul temoin binaire")
    # L'attribut d'autorite disparait, l'etat dit toujours `aucun`.
    c.viole(check_projection_n1_rendue(n1_mut(GARDE_ATTR, ""), M1_REEL),
            "ABSENT",
            "CI-38 suppression sans garde de presence de l'attribut")

    # Une condition que l'evaluateur ne sait pas rendre : ECHEC, jamais un vert.
    c.viole(check_projection_n1_rendue(n1_mut(
        "            - condition: state\n"
        f"              entity_id: {ENTITE_M1_TEMOIN}\n"
        '              state: "on"\n',
        "            - condition: numeric_state\n"
        f"              entity_id: {ENTITE_M1_LISTE}\n"
        "              above: 0\n"), M1_REEL),
        "ne sait pas rendre", "CI-38 condition non rendable")

    # ---- ASP-CI-39 : ce que N1 ne fait pas --------------------------------
    c.viole(check_interdits_n1({}), "introuvable", "CI-39 N1 absent")
    ANCRE_39 = "  mode: restart\n"
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - service: vacuum.start\n")),
        "commande jamais l'appareil", "CI-39 commande robot")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - action: roborock.get_maps\n")),
        "commande jamais l'appareil", "CI-39 commande roborock sous `action:`")
    # FLOW MAPPING — forme que le detecteur de service, ancre sur la LIGNE, ne
    # couvre pas. Elle est neanmoins refusee, par le balayage d'entites : la
    # projection ne connait que son autorite. La limite du premier parseur est
    # donc consignee, et elle n'ouvre rien.
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: {service: vacuum.start}\n")),
        "seconde autorite", "CI-39 commande robot en flow mapping")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - service: button.press\n")),
        "geste operateur explicite", "CI-39 pression de bouton")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: "
        "button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air\n")),
        "ne presse aucun bouton", "CI-39 bouton d'entretien nomme")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - service: "
        "input_text.set_value\n")),
        "hors des services admis", "CI-39 ecriture d'un helper")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + f"  bidon: \"{{{{ states('{ID_VERDICT}') }}}}\"\n")),
        "ni n'ecrit le verdict", "CI-39 lecture du verdict")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: LANCEE/DEMARRAGE_OBSERVE\n")),
        "n'observe aucune mission",
        "CI-39 cycle deduit d'un verdict de mission")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: "
        "binary_sensor.roborock_q7_max_nettoyage\n")),
        "mission externe", "CI-39 temoin natif de session lu")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - service: "
        "script.notification_envoyer\n")),
        "AUCUN envoi mobile", "CI-39 mobile push")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - service: notify.mobile_app_x\n")),
        "AUCUN envoi mobile", "CI-39 service notify en dur")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: "
        "sensor.roborock_q7_max_dock_erreur_de_dock\n")),
        "pas un entretien", "CI-39 erreur de dock projetee")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: ECHEC/ERREUR_EN_MISSION\n")),
        "pas un entretien", "CI-39 erreur en mission projetee")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: input_select.aspirateur_carte\n")),
        "helpers d'intention", "CI-39 lecture d'un helper d'intention")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + '  bidon: "{{ now().timestamp() }}"\n')),
        "ne se prevoit pas", "CI-39 primitive temporelle")
    c.viole(check_interdits_n1(n1_mut(
        "**Postes dus :**", "**Prochaine echeance :** dans environ")),
        "aucune date previsionnelle", "CI-39 date previsionnelle annoncee")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon:\n    - repeat:\n        count: 2\n")),
        "elle ne boucle pas", "CI-39 repetition")
    c.viole(check_interdits_n1(n1_mut(
        f"      entity_id: {READINESS_N1}\n",
        "      entity_id: binary_sensor.presence_maison\n")),
        "seconde autorite", "CI-39 entite etrangere lue")


    # ═════════════════════════════════════════════════════════════
    # RUNTIME L2 — conduite et supervision
    #
    # Une matrice VOLONTAIREMENT BORNEE : chaque mutation correspond a une
    # regression concrete que le lot pourrait subir — commander le robot a
    # tort, dupliquer une commande, ecrire un verdict impossible, briser
    # l'unicite d'un writer, ou perdre la garde de serialisation. Aucune
    # mutation adversariale sans risque reel n'est ajoutee.
    #
    # Les mutations portent sur les FICHIERS REELS, jamais sur des maquettes.
    # ═════════════════════════════════════════════════════════════

    ENG_PAUSE = (
        "            - action: input_text.set_value\n"
        "              target:\n"
        "                entity_id: input_text.aspirateur_mission_verdict\n"
        "              data:\n"
        '                value: "CONDUITE/PAUSE_ENGAGEE"\n')
    # L'emission porte desormais `continue_on_error` : l'ancre suit le
    # fichier reel, commentaires compris — une ancre approximative ferait
    # passer une mutation a cote de sa cible.
    _cnd0 = rt0[RUNTIME_L2_CONDUITE]
    _deb = _cnd0.index("            - action: vacuum.pause\n")
    _fin = _cnd0.index("                entity_id: vacuum.roborock_q7_max\n",
                       _deb) + len("                entity_id: "
                                   "vacuum.roborock_q7_max\n")
    CMD_PAUSE = _cnd0[_deb:_fin]
    WAIT_PAUSE = (
        "            - wait_template: >-\n"
        "                {{ is_state('sensor.roborock_q7_max_etat', 'paused') }}\n"
        '              timeout: "00:00:30"\n'
        "              continue_on_timeout: true\n")
    # Le bloc de conclusion du retour est le DERNIER du fichier : le retirer
    # laisse un YAML valide, et c'est ce qui rend la mutation utilisable.
    CONCLUSION_RETOUR = _cnd0[_cnd0.rindex("            - choose:"):]

    def l2_mut(fichier: str, vieux: str, neuf: str, n: int = 1):
        """Le runtime reel, avec UNE substitution dans UN fichier L2."""
        base = dict(rt0)
        assert vieux in base[fichier], \
            f"ancre L2 absente de {fichier} : {vieux[:70]!r}"
        base[fichier] = base[fichier].replace(vieux, neuf, n)
        return base

    F_CND = RUNTIME_L2_CONDUITE
    F_SUP = RUNTIME_L2_SUPERVISION
    F_PRJ = RUNTIME_L2_PROJECTION

    # ---- le runtime L2 livre passe les controles etendus ------------------
    c.conforme(check_sequence_conduite(rt0), "L2 conduite conforme")
    c.conforme(check_supervision(rt0), "L2 supervision conforme")
    c.conforme(check_table_writers(rt0), "L2 table des trois writers conforme")
    c.conforme(check_conduite_forme(rt0), "L2 forme du script de conduite")

    # ---- ASP-CI-18 : l'engagement precede la commande (garde A-11) --------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, ENG_PAUSE + "\n" + CMD_PAUSE,
               CMD_PAUSE + "\n" + ENG_PAUSE)),
        "APRÈS sa commande", "L2 engagement pose apres la commande")

    # ---- ASP-CI-18 : une commande, et une seule ---------------------------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, CMD_PAUSE, CMD_PAUSE + "\n" + CMD_PAUSE)),
        "émet 2 commande(s)", "L2 commande dupliquee dans un geste")

    # ---- ASP-CI-18 : le geste commande CE QU'IL ANNONCE -------------------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, "            - action: vacuum.pause",
               "            - action: vacuum.stop")),
        "commande le robot à tort", "L2 geste commandant une autre primitive")

    # ---- ASP-CI-18 : un geste n'ecrit que SES valeurs ---------------------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, 'value: "CONDUITE/PAUSE_CONFIRMEE"',
               'value: "CONDUITE/REPRISE_CONFIRMEE"')),
        "hors des valeurs de ce geste", "L2 valeur d'un autre geste ecrite")

    # ---- ASP-CI-18 : la relecture est unique, et elle existe --------------
    c.viole(check_sequence_conduite(l2_mut(F_CND, WAIT_PAUSE, "")),
            "relecture(s)", "L2 relecture supprimee")
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, WAIT_PAUSE, WAIT_PAUSE + WAIT_PAUSE)),
        "relecture(s)", "L2 seconde relecture ajoutee")

    # ---- ASP-CI-18 : aucune reemission ------------------------------------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, CMD_PAUSE,
               "            - repeat:\n                count: 2\n"
               "                sequence:\n" + CMD_PAUSE)),
        "répétition", "L2 commande sous un `repeat`")

    # ---- ASP-CI-18 : un geste conclut, ou il se tait -----------------------
    sans_conclusion = l2_mut(F_CND, CONCLUSION_RETOUR, "")
    c.viole(check_sequence_conduite(sans_conclusion),
            "ne conclut RIEN", "L2 geste sans issue apres relecture")
    c.viole(check_table_writers(sans_conclusion),
            "n'ecrit jamais", "L2 valeur de W2 devenue inatteignable")

    # ---- ASP-CI-11 : la table des writers, et sa disjonction ---------------
    c.viole(check_table_writers(
        l2_mut(F_CND, 'value: "CLOTURE/APRES_ARRET_CONFIRME"',
               'value: "CLOTURE/FIN_NOMINALE"')),
        "hors de son ensemble", "L2 la conduite ecrit une valeur de W3")
    c.viole(check_table_writers(
        l2_mut(F_SUP, 'value: "CLOTURE/FIN_NOMINALE"',
               'value: "CLOTURE/APRES_ARRET_CONFIRME"')),
        "hors de son ensemble", "L2 la supervision ecrit une valeur de W2")
    c.viole(check_table_writers(
        l2_mut(F_CND, 'value: "CONDUITE/PAUSE_CONFIRMEE"',
               'value: "{{ \'CONDUITE/PAUSE_\' ~ \'CONFIRMEE\' }}"')),
        "NON LITTERALE", "L2 verdict assemble en Jinja")

    # ---- ASP-CI-11 : la projection de mission ne peut pas ecrire -----------
    ecriture = (
        "    - action: input_text.set_value\n"
        "      target:\n"
        "        entity_id: input_text.aspirateur_mission_verdict\n"
        "      data:\n"
        '        value: "CLOTURE/FIN_NOMINALE"\n')
    c.viole(check_ecrivain_unique(
        mot0, l2_mut(F_PRJ, "  action:\n", "  action:\n" + ecriture),
        depot0),
        "ÉCRIT le verdict", "L2 la projection ecrit le verdict")

    # ---- ASP-CI-11 : forme du script de conduite --------------------------
    c.viole(check_conduite_forme(l2_mut(F_CND, "  mode: single",
                                        "  mode: parallel")),
            "mode: single", "L2 conduite en mode concurrent")
    c.viole(check_conduite_forme(
        l2_mut(F_CND, "    geste:\n", "    duree:\n      name: D\n"
               "      required: false\n    geste:\n")),
        "un seul champ", "L2 champ supplementaire au script de conduite")

    # ---- ASP-CI-14 : la primitive de demarrage, unique et gardee -----------
    c.viole(check_voies_interdites(
        l2_mut(F_CND, "            - action: vacuum.start",
               "            - action: vacuum.start\n"
               "              target:\n"
               "                entity_id: vacuum.roborock_q7_max\n"
               "            - action: vacuum.start")),
        "EXACTEMENT un", "L2 seconde occurrence de la primitive de demarrage")
    c.viole(check_voies_interdites(
        l2_mut(F_CND, "{% set session = states('binary_sensor."
                      "roborock_q7_max_nettoyage') %}",
               "{% set session = 'on' %}", 1)),
        "la garde de reprise ne lit pas",
        "L2 garde de reprise privee du temoin de session")
    c.viole(check_voies_interdites(
        l2_mut(F_SUP, "  mode: queued",
               "  mode: queued\n  bidon: vacuum.start")),
        "démarreur interdit", "L2 primitive de demarrage hors du fichier admis")

    # ---- ASP-CI-20 : les fenetres L2 -------------------------------------
    c.viole(check_constantes_temporelles(
        l2_mut(F_CND, '              timeout: "00:00:30"',
               '              timeout: "00:01:00"')),
        "durée(s) concurrente(s) dans le script de conduite",
        "L2 fenetre de relecture hors de la constante mutualisee")
    c.viole(check_constantes_temporelles(
        l2_mut(F_CND, WAIT_PAUSE, "")),
        "fenêtres de relecture", "L2 fenetre de relecture manquante")
    c.viole(check_constantes_temporelles(
        l2_mut(F_CND, CMD_PAUSE,
               '            - delay: "00:00:05"\n' + CMD_PAUSE)),
        "porte `delay:`", "L2 temporisation libre dans la conduite")
    c.viole(check_constantes_temporelles(
        l2_mut(F_SUP, "  mode: queued",
               '  mode: queued\n  timeout: "00:00:30"')),
        "ÉVÉNEMENTIELLES", "L2 attente bornee dans la supervision")

    # ---- check_supervision : porte d'entree, exclusion, reconciliation -----
    c.viole(check_supervision(
        l2_mut(F_SUP, '            - condition: template\n'
                      '              value_template: "{{ verdict in '
                      'verdict_ouvert }}"\n'
                      '            - condition: template\n'
                      '              value_template: >-\n'
                      "                {{ etat == 'error'",
               '            - condition: template\n'
               '              value_template: >-\n'
               "                {{ etat == 'error'")),
        "sans exiger un verdict de classe O",
        "L2 supervision ecrivant hors mission ouverte")
    c.viole(check_supervision(
        l2_mut(F_SUP, '            - condition: template\n'
                      '              value_template: "{{ verdict not in '
                      'engagements }}"\n', "")),
        "ne s'exclut pas pendant un engagement",
        "L2 garde de serialisation perdue")
    c.viole(check_supervision(
        l2_mut(F_SUP, "            - condition: trigger\n"
                      "              id: readiness\n", "")),
        "hors de la réconciliation de redémarrage",
        "L2 cloture opaque ecrite hors reconciliation")
    c.viole(check_supervision(
        l2_mut(F_SUP, "  mode: queued",
               "  mode: queued\n  bidon:\n    - repeat:\n"
               "        count: 2\n")),
        "répétition", "L2 repetition dans la supervision")

    # ═════════════════════════════════════════════════════════════
    # BATTERIE F1-F5 — chaque correction, confrontee a SA regression.
    # Une mutation par propriete, et chacune REJOUE le defaut d'origine :
    # ce n'est pas la presence du correctif qui est verifiee, c'est le fait
    # que son retrait redevienne ROUGE.
    # ═════════════════════════════════════════════════════════════

    # ---- F1 : la cessation ne s'etablit que sur l'etat atteste ------------
    REGLE_NEGATIVE = (
        '              value_template: >-\n'
        "                {{ etat not in classe_a\n"
        "                   and etat not in classe_e_indispo\n"
        "                   and etat != 'error' }}\n")
    c.viole(check_supervision(
        l2_mut(F_SUP, '              value_template: "{{ etat == '
                      'arret_atteste }}"\n', REGLE_NEGATIVE)),
        "par NÉGATION d'une classe",
        "F1 interruption conclue negativement sur toute la classe N")
    c.viole(check_supervision(
        l2_mut(F_SUP, '        arret_atteste: "idle"',
               '        arret_atteste: "docked"')),
        "arret_atteste: idle", "F1 etat d'arret atteste deplace")
    c.viole(check_supervision(
        l2_mut(F_SUP, '        arret_atteste: "idle"\n', "")),
        "arret_atteste", "F1 etat d'arret atteste retire des referentiels")

    # ---- F2 : l'emission absorbe son exception ---------------------------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND, "              continue_on_error: true\n", "", 4)),
        "n'absorbe pas son exception",
        "F2 exception de service laissant un engagement fige")

    # ---- F3 : la relecture du verdict avant chaque conclusion ------------
    c.viole(check_sequence_conduite(
        l2_mut(F_CND,
               "                        {{ states('input_text."
               "aspirateur_mission_verdict')\n"
               "                           == 'CONDUITE/RETOUR_ENGAGE'\n"
               "                           and states('sensor."
               "roborock_q7_max_etat')\n"
               "                               not in retour }}",
               "                        {{ states('sensor."
               "roborock_q7_max_etat')\n"
               "                           not in retour }}")),
        "sans relire le verdict",
        "F3 course W2/W3 : le retour conclut sans relire le verdict")
    c.viole(check_sequence_conduite(
        l2_mut(F_CND,
               "                - conditions:\n"
               "                    - condition: template\n"
               "                      value_template: >-\n"
               "                        {{ states('input_text."
               "aspirateur_mission_verdict')\n"
               "                           == 'CONDUITE/ARRET_ENGAGE' }}\n"
               "                  sequence:\n",
               "              default:\n", 1)),
        "porte un `default:`",
        "F3 conclusion d'arret rebasculee dans un `default`")

    # ---- F4 : l'amarrage se prouve, `docking` n'est pas une arrivee ------
    c.viole(check_supervision(
        l2_mut(F_SUP,
               "          {{ is_state('vacuum.roborock_q7_max', 'docked')\n"
               "             or is_state('sensor.roborock_q7_max_etat', "
               "'charging') }}",
               "          {{ etat in ['docking', 'charging'] }}")),
        "n'invoque pas `vacuum.roborock_q7_max`",
        "F4 preuve d'amarrage privee du seul temoin d'amarrage")
    c.viole(check_supervision(
        l2_mut(F_SUP,
               "          {{ is_state('vacuum.roborock_q7_max', 'docked')\n"
               "             or is_state('sensor.roborock_q7_max_etat', "
               "'charging') }}",
               "          {{ is_state('vacuum.roborock_q7_max', 'docked')\n"
               "             or is_state('sensor.roborock_q7_max_etat', "
               "'docking') }}")),
        "état de MOUVEMENT",
        "F4 `docking` reintroduit comme preuve d'arrivee")
    c.viole(check_supervision(
        l2_mut(F_SUP, '              value_template: "{{ amarre }}"',
               "              value_template: \"{{ etat == 'charging' }}\"",
               1)),
        "sans s'appuyer sur la preuve `amarre`",
        "F4 branche d'arrivee affranchie de la preuve d'amarrage")

    # ---- F5 : le moteur se tait sur une mission deja ouverte -------------
    _mot_txt = rt0[RUNTIME_MOTEUR]
    GARDE_L1 = _mot_txt[_mot_txt.index("    # \U0001F6E1\ufe0f ÉTAPE 0a"):
                        _mot_txt.index("    # \U0001F504 ÉTAPE 0 —")]

    def _mut_moteur(vieux, neuf, n=1):
        assert vieux in _mot_txt, f"ancre moteur absente : {vieux[:60]!r}"
        return (yaml.safe_load(_mot_txt.replace(vieux, neuf, n))
                [ID_MOTEUR]["sequence"])

    c.viole(check_ordre_sequence(_mut_moteur(GARDE_L1, "")),
            "AUCUNE garde de memoire de mission",
            "F5 garde de memoire de mission supprimee du moteur")
    c.viole(check_ordre_sequence(_mut_moteur(
        '            - stop: "Mission Arsenal deja ouverte : le verdict est '
        'de classe O, la memoire de mission est preservee"',
        "            - action: input_text.set_value\n"
        "              target:\n"
        "                entity_id: input_text.aspirateur_mission_verdict\n"
        "              data:\n"
        '                value: "REFUS/MISSION_DEJA_OUVERTE"')),
        "garde de memoire de mission ECRIT",
        "F5 la garde ecrit un refus au lieu de se taire")
    c.viole(check_ordre_sequence(_mut_moteur(
        '          - "CONDUITE/RETOUR_ENGAGE"\n', "", 1)),
        "valeurs de classe O et O-R",
        "F5 table de classe O incomplete dans le moteur")

    # ---- ASP-CI-37 : la projection de mission, symetrique de l'entretien ---
    N1_L2 = load_runtime_n1()
    c.viole(check_writers_n1(
        {**N1_L2, F_PRJ: N1_L2[F_PRJ].replace(
            f'title: "{TITRE_N1_MISSION}"',
            'title: "\U0001F916 Aspirateur — Mission en cours"')},
        DEPOT_0), "attendu", "CI-37 titre de la projection de mission au cadratin")
    c.viole(check_writers_n1(
        {**N1_L2, F_PRJ: N1_L2[F_PRJ].replace(
            f"      entity_id: {ID_VERDICT}\n",
            "      entity_id: sensor.roborock_q7_max_etat\n")},
        DEPOT_0), "adopterait une mission externe",
        "CI-37 projection de mission branchee sur un temoin natif")
    c.viole(check_writers_n1(
        {**N1_L2, F_PRJ: N1_L2[F_PRJ].replace(
            '          - "CLOTURE/FIN_NOMINALE"\n', "")},
        DEPOT_0), "declare `verdict_terminal`",
        "CI-37 classe terminale amputee dans la projection")
    c.viole(check_writers_n1(
        {**N1_L2, F_PRJ: N1_L2[F_PRJ].replace(
            '          - "CONDUITE/RETOUR_ENGAGE"\n', "")},
        DEPOT_0), "declare `verdict_ouvert`",
        "CI-37 classe ouverte amputee dans la projection")

    # ---- ASP-CI-39 : les trois natures du dossier -------------------------
    c.viole(check_interdits_n1(
        {**N1_L2, F_SUP: N1_L2[F_SUP].replace(
            "  mode: queued",
            "  mode: queued\n  bidon:\n    - action: vacuum.stop\n")}),
        "ne commande jamais l'appareil",
        "CI-39 la supervision commande l'appareil")
    c.viole(check_interdits_n1(
        {**N1_L2, F_SUP: N1_L2[F_SUP].replace(
            "  mode: queued",
            "  mode: queued\n  bidon:\n"
            "    - service: persistent_notification.create\n")}),
        "objet SEPARE", "CI-39 la supervision projette une persistante")
    c.viole(check_interdits_n1(
        {**N1_L2, F_PRJ: N1_L2[F_PRJ].replace(
            "  mode: restart",
            "  mode: restart\n  bidon:\n"
            "    - service: script.notification_envoyer\n")}),
        "AUCUN envoi mobile", "CI-39 envoi mobile depuis la projection")
    c.viole(check_interdits_n1(
        {**N1_L2, F_PRJ: N1_L2[F_PRJ].replace(
            "  mode: restart",
            "  mode: restart\n  bidon: sensor.roborock_q7_max_etat\n")}),
        "seconde autorite", "CI-39 projection lisant un temoin natif")
    c.viole(check_interdits_n1(
        {**N1_L2, DOSSIER_N1 + "/quatrieme.yaml": "- id: \"1028000000000X\"\n"}),
        "un quatrieme objet est apparu",
        "CI-39 fichier surnumeraire dans le dossier")

    # ═════════════════════════════════════════════════════════════
    # C-6 — SLOTS CRITIQUES LITTÉRAUX
    #
    # Une seule propriete est garantie, donc une seule est prouvee : dans les
    # fichiers que le module protege NOMMEMENT, un slot critique porteur de
    # Jinja est refuse. Les cas ci-dessous couvrent les quatre cles, les deux
    # formes d'ecriture (ligne et scalaire de bloc), les deux acceptations
    # (litteral nu, litteral cite), la correction d'alias conservee, la borne
    # de perimetre, et l'absorption des formes invalides.
    # ═════════════════════════════════════════════════════════════

    def n1_slot(bloc: str) -> dict[str, str]:
        """Le runtime N1 reel, augmente d'UN bloc d'action."""
        return n1_mut(ANCRE_39, ANCRE_39 + "  bidon:\n" + bloc)

    # ---- Jinja refuse dans chacune des quatre cles critiques -------------
    for _cle in ("service", "action", "perform_action"):
        c.viole(check_interdits_n1(n1_slot(
            f"    - {_cle}: \"{{{{ 'vacu' ~ 'um.start' }}}}\"\n")),
            "porte un gabarit Jinja", f"C-6/CI-39 Jinja dans `{_cle}`")
    c.viole(check_interdits_n1(n1_slot(
        "    - service: persistent_notification.create\n"
        "      target:\n"
        "        entity_id: \"{{ cible }}\"\n")),
        "porte un gabarit Jinja", "C-6/CI-39 Jinja dans `entity_id`")

    # ---- scalaire de bloc : le gabarit est sous la cle, pas sur sa ligne --
    c.viole(check_interdits_n1(n1_slot(
        "    - service: >-\n"
        "        {{ 'button' ~ '.press' }}\n")),
        "porte un gabarit Jinja", "C-6/CI-39 Jinja en scalaire de bloc")
    c.viole(check_interdits_n1(n1_slot(
        "    - service: persistent_notification.create\n"
        "      target:\n"
        "        entity_id: |\n"
        "          {% set b = 'button' %}{{ b ~ '.press' }}\n")),
        "porte un gabarit Jinja", "C-6/CI-39 `{% %}` en scalaire de bloc")

    # ---- les deux formes litterales restent acceptees --------------------
    c.conforme(check_interdits_n1(N1_0), "C-6/CI-39 runtime N1 reel conforme")
    c.conforme(check_interdits_n1(n1_slot(
        "    - service: persistent_notification.create\n")),
        "C-6/CI-39 litteral nu accepte")
    c.conforme(check_interdits_n1(n1_slot(
        "    - service: \"persistent_notification.create\"\n"
        "      target:\n"
        "        entity_id: \"sensor.aspirateur_entretien_du\"\n")),
        "C-6/CI-39 litteral cite accepte")

    # ---- ASP-CI-11 : la meme regle sur les CINQ fichiers runtime nommes ---
    c.conforme(check_ecrivain_unique(mot0, rt0, depot0),
               "C-6/CI-11 runtime L1 reel conforme")
    c.viole(check_ecrivain_unique(
        mot0, {**rt0, RUNTIME_MOTEUR: rt0[RUNTIME_MOTEUR]
               + "\n  - action: \"{{ 'vacu' ~ 'um.stop' }}\"\n"}, depot0),
        "porte un gabarit Jinja", "C-6/CI-11 Jinja dans un fichier nomme")

    # ---- corrections conservees : scalaire cite, et alias `perform_action`
    for _forme, _libelle in (('    - action: "vacuum.stop"\n', "scalaire cite"),
                             ("    - perform_action: vacuum.stop\n",
                              "alias `perform_action`")):
        c.viole(check_ecrivain_unique(mot0, rt0, dict(
            depot0, **{"11_automations/x.yaml": _forme})),
            "seuls le moteur et le script de conduite commandent",
            f"C-6/CI-11 primitive interdite — {_libelle}")

    # ---- BORNE DE PERIMETRE : hors des fichiers nommes, aucun refus -------
    # La regle ne balaie pas le depot et ne cherche aucun marqueur de
    # contenu. Un fichier tiers templatise n'est pas refuse — limite assumee.
    c.conforme(check_ecrivain_unique(mot0, rt0, dict(
        depot0, **{"11_automations/aspirateur/tiers.yaml":
                   '    - service: "{{ svc }}"\n'
                   '      target:\n'
                   '        entity_id: "{{ cible }}"\n'})),
        "C-6/CI-11 fichier hors perimetre nominatif non refuse")

    # ---- formes invalides : diagnostiquees, jamais une exception ----------
    _degats = []
    for _f in (None, 12, 3.5, True, ["service: x"], {"a": 1}, b"x", object(),
               "", "service: {{ 'a' ~ }}\n", "{{ unclosed",
               "a: &x 1\nb: *x\nc: {d: e}\nservice: >-\n  x\n"):
        try:
            slots_sensibles(_f)
            slots_templatises(_f)
            refus_slots_templatises("ASP-CI-39", "f.yaml", _f)
        except Exception as exc:                       # noqa: BLE001
            _degats.append(f"{type(_f).__name__} {_f!r:.30} leve {exc!r}")
    c.conforme(_degats, "C-6 formes invalides absorbees sans traceback")

    # ═════════════════════════════════════════════════════════════
    # MAINTENANCE — lot M2 : ASP-CI-40 … ASP-CI-42
    #
    # Joues sur les FICHIERS REELS, puis sur leurs mutants. Un controle qui
    # ne refuse rien ne prouve rien : chaque mutation ci-dessous retire une
    # garantie precise, et doit etre rattrapee.
    # ═════════════════════════════════════════════════════════════
    _m2 = (ROOT / RUNTIME_M2).read_text(encoding="utf-8") \
        if (ROOT / RUNTIME_M2).is_file() else ""
    _depot_m2 = {RUNTIME_M2: _m2}
    _lov_m2 = {rel: (ROOT / rel).read_text(encoding="utf-8")
               for rel in UI_M2 + (NAV_ASPIRATEUR,)
               if (ROOT / rel).is_file()}
    _dash_m2 = dashboards_declares()

    # ---- ASP-CI-40 : la forme du fichier M2 ------------------------------
    c.conforme(check_declaration_entretien(_depot_m2), "CI-40 fichier reel")
    c.viole(check_declaration_entretien({}), "introuvable",
            "CI-40 fichier M2 absent")
    c.viole(check_declaration_entretien(
        {RUNTIME_M2: _m2.replace("mode: single", "mode: restart")}),
        "mode: single", "CI-40 mode non single refuse")
    c.viole(check_declaration_entretien(
        {RUNTIME_M2: _m2.replace('- "nettoyage_capteurs"', '- "bac_a_poussiere"')}),
        "vocabulaire ferme", "CI-40 cinquieme poste refuse")
    c.viole(check_declaration_entretien(
        {RUNTIME_M2: _m2.replace(
            "entity_id: button.roborock_q7_max_reinitialiser_le_consommable_du_capteur",
            "device_id: 0123456789abcdef")}),
        "device_id", "CI-40 ciblage par device_id refuse")
    c.viole(check_declaration_entretien(
        {RUNTIME_M2: _m2.replace(
            "entity_id: button.roborock_q7_max_reinitialiser_le_consommable_du_capteur",
            'entity_id: "{{ cible }}"')}),
        "templatise", "CI-40 entity_id templatise refuse")
    c.viole(check_declaration_entretien(
        {RUNTIME_M2: _m2.replace(
            "            - action: button.press\n"
            "              continue_on_error: true\n"
            "              target:\n"
            "                entity_id: button.roborock_q7_max_reinitialiser_le_consommable_du_capteur\n",
            "")}),
        "appel(s) `button.press`", "CI-40 quatrieme branche retiree")
    c.viole(check_declaration_entretien(
        {RUNTIME_M2: _m2.replace("- action: button.press",
                                 "- action: vacuum.start", 1)}),
        "hors des services admis", "CI-40 commande robot refusee")

    # ---- ASP-CI-41 : la sequence rendue ----------------------------------
    c.conforme(check_sequence_entretien(_depot_m2), "CI-41 sequence reelle")
    c.viole(check_sequence_entretien(
        {RUNTIME_M2: _m2.replace('timeout: "00:00:30"', 'timeout: "00:02:00"')}),
        "fenetre de relecture", "CI-41 fenetre hors constante refusee")
    c.viole(check_sequence_entretien(
        {RUNTIME_M2: _m2.replace("continue_on_timeout: true",
                                 "continue_on_timeout: false")}),
        "continue_on_timeout", "CI-41 expiration silencieuse refusee")
    c.viole(check_sequence_entretien(
        {RUNTIME_M2: _m2.replace(
            "{{ v | is_number and (v | float) > (restant_avant | float) }}\n"
            "      timeout:",
            "{{ v | is_number and (v | float) == (plafond | float) }}\n"
            "      timeout:")}),
        "etat statique interdit", "CI-41 postcondition statique refusee")
    c.viole(check_sequence_entretien(
        {RUNTIME_M2: _m2.replace(
            "REMISE_A_ZERO_NON_CONFIRMEE", "REMISE_A_ZERO_CONFIRMEE")}),
        "issues terminales", "CI-41 issue non confirmee manquante")
    c.viole(check_sequence_entretien(
        {RUNTIME_M2: _m2.replace(
            "{{ (restant_avant | float) >= (plafond | float) }}",
            "{{ false }}")}),
        "STRICTEMENT INFERIEUR", "CI-41 garde d'objet retiree")
    c.viole(check_sequence_entretien(
        {RUNTIME_M2: _m2.replace(
            "value: \"ENTRETIEN/{{ poste | upper }}/REMISE_A_ZERO_CONFIRMEE\"",
            "value: \"ENTRETIEN/{{ poste | upper }}/REMISE_A_ZERO_CONFIRMEE\"\n"
            "            - action: persistent_notification.dismiss\n"
            "              data:\n"
            "                notification_id: aspirateur_entretien")}),
        "notification", "CI-41 acquittement de notification refuse")

    # ---- ASP-CI-42 : l'ecran d'entretien ---------------------------------
    c.conforme(check_ui_entretien(_lov_m2, _dash_m2), "CI-42 ecran reel")
    _rel_act = "18_lovelace/includes/cartes/aspirateur/entretien_action.yaml"
    c.viole(check_ui_entretien(
        {**_lov_m2, _rel_act: _lov_m2[_rel_act].replace(
            "service: script.aspirateur_declarer_entretien",
            "service: button.press", 1)}, _dash_m2),
        "button.press", "CI-42 pression directe en Lovelace refusee")
    c.viole(check_ui_entretien(
        {**_lov_m2, _rel_act: _lov_m2[_rel_act].replace(
            "poste: filtre",
            "poste: bac_a_poussiere", 1)}, _dash_m2),
        "vocabulaire ferme", "CI-42 poste hors vocabulaire refuse")
    c.viole(check_ui_entretien(
        {**_lov_m2, _rel_act: re.sub(
            r"          confirmation: >-\n(?:            .*\n)+", "",
            _lov_m2[_rel_act], count=1)}, _dash_m2),
        "confirmation", "CI-42 geste sans confirmation refuse")
    c.viole(check_ui_entretien(
        {**_lov_m2, NAV_ASPIRATEUR: _lov_m2[NAV_ASPIRATEUR].replace(
            "navigation_path: /aspirateur-entretien-dashboard",
            "navigation_path: /aspirateur-dashboard")}, _dash_m2),
        "cul-de-sac", "CI-42 ecran inatteignable refuse")
    c.viole(check_ui_entretien(_lov_m2, {}),
            "dashboards.yaml", "CI-42 cle de dashboard absente refusee")
    c.viole(check_ui_entretien({k: v for k, v in _lov_m2.items()
                                if k != _rel_act}, _dash_m2),
            "introuvable", "CI-42 carte d'action absente refusee")

    # ---- Le VISITEUR RECURSIF, et les six formes adverses ----------------
    for _i, _forme in enumerate(FORMES_ADVERSES_PRESSION, 1):
        assert pressions_entretien(_forme), \
            f"visiteur M2 : la forme adverse {_i} n'est pas rattrapee — le " \
            f"desserrage de l'allowlist reposerait sur un parseur incomplet."
    c.conformes += 1
    assert VISITEUR_YAML_RECURSIF, \
        "visiteur M2 : le drapeau doit DERIVER de l'essai des six formes."
    c.conformes += 1

    # ═════════════════════════════════════════════════════════════
    # C45 LOT 3 — ASP-CI-43, ASP-CI-44, ASP-CI-45
    #
    # Les mutations portent sur les FICHIERS REELS, jamais sur des
    # maquettes : une maquette prouverait que le controle sait lire ce que
    # le test lui donne, pas qu'il garde ce que le depot contient.
    # ═════════════════════════════════════════════════════════════

    _dep0 = load_yaml_depot()
    _lov0 = load_lovelace()
    _ui = FICHIER_UI_MISSION

    def _mut(base: dict, fichier: str, vieux: str, neuf: str, n: int = 1):
        """Les sources, avec UNE substitution dans UN fichier."""
        out = dict(base)
        assert vieux in out[fichier], \
            f"ancre lot 3 absente de {fichier} : {vieux[:70]!r}"
        out[fichier] = out[fichier].replace(vieux, neuf, n)
        return out

    # ---- ASP-CI-43 : le depot livre passe -------------------------------
    c.conforme(check_representations_de_classe(rt0, _dep0),
               "CI-43 les sept representations livrees sont exactes")

    # ---- ASP-CI-43 : AMPUTATION des sept, une par une --------------------
    # Les quatre dernieres n'etaient gardees par RIEN avant ce lot : c'est
    # l'ecart que le §3.2 du chantier avait recense, et que ce controle ferme.
    for _rel, _ancre, _quoi in (
            (RUNTIME_MOTEUR, '          - "CONDUITE/ARRET_ENGAGE"\n',
             "R1 verdict_ouvert du moteur"),
            (RUNTIME_L2_CONDUITE, '          - "CONDUITE/ARRET_ENGAGE"\n',
             "R4 verdict_ouvert de la conduite"),
            (RUNTIME_L2_SUPERVISION,
             '          - "CONDUITE/PAUSE_CONFIRMEE"\n',
             "R5 verdict_ouvert de la supervision"),
            (RUNTIME_L2_PROJECTION, '          - "CLOTURE/FIN_NOMINALE"\n',
             "R3 verdict_terminal de la projection")):
        c.viole(check_representations_de_classe(
            _mut(rt0, _rel, _ancre, ""), _dep0),
            "n'égale AUCUN ensemble canonique", f"CI-43 {_quoi} amputee")

    # `engagements` — sous-ensemble contractuellement nomme de la classe O.
    # La constante EXISTAIT au module sans etre confrontee a rien.
    c.viole(check_representations_de_classe(
        _mut(rt0, RUNTIME_L2_SUPERVISION,
             '        engagements:\n          - "CONDUITE/PAUSE_ENGAGEE"\n',
             '        engagements:\n'), _dep0),
        "les engagements de W2", "CI-43 R6 engagements amputee")

    # Les CLES d'une table sont une enumeration : la forme ne fait pas la
    # regle, l'enumeration la fait (ASP-INV-98).
    c.viole(check_representations_de_classe(
        _mut(rt0, RUNTIME_L2_PROJECTION,
             '          "CONDUITE/ARRET_ENGAGE": "Arrêt demandé, en attente '
             'de confirmation."\n', ""), _dep0),
        "clés de mapping", "CI-43 R7 cle de phrases retiree")

    # ---- ASP-CI-43 : valeur ETRANGERE, dans les deux sens ---------------
    c.viole(check_representations_de_classe(
        _mut(rt0, RUNTIME_L2_CONDUITE, '          - "CONDUITE/ARRET_ENGAGE"\n',
             '          - "CONDUITE/ARRET_ENGAGE"\n'
             '          - "CLOTURE/FIN_NOMINALE"\n'), _dep0),
        "en trop", "CI-43 valeur d'une AUTRE classe ajoutee")
    c.viole(check_representations_de_classe(
        _mut(rt0, RUNTIME_L2_SUPERVISION,
             '        engagements:\n',
             '        engagements:\n          - "CODE/HORS_VOCABULAIRE"\n'),
        _dep0),
        "en trop", "CI-43 valeur hors vocabulaire ajoutee")

    # ---- ASP-CI-43 : LE NOM DE LA CLE EST INDIFFERENT -------------------
    # Le test decisif. La representation est RENOMMEE et amputee : une garde
    # par cle litterale — celle d'ASP-CI-18, celle d'ASP-CI-37 — ne verrait
    # plus rien. C'est exactement ce qui avait manque `engagements` et les
    # cles de `phrases` lors du recensement d'ouverture du chantier.
    c.viole(check_representations_de_classe(
        _mut(rt0, RUNTIME_L2_SUPERVISION,
             '        engagements:\n          - "CONDUITE/PAUSE_ENGAGEE"\n',
             '        fenetre_de_relecture:\n'), _dep0),
        "fenetre_de_relecture", "CI-43 representation renommee ET amputee")

    # ---- ASP-CI-43 : le CARDINAL du recensement (condition d'arret A4) ---
    c.viole(check_representations_de_classe(
        _mut(rt0, RUNTIME_L2_CONDUITE, '        verdict_ouvert:\n',
             '        verdict_bis:\n          - "CLOTURE/FIN_NOMINALE"\n'
             '          - "CLOTURE/APRES_ARRET_CONFIRME"\n'
             '        verdict_ouvert:\n'), _dep0),
        "représentation(s) pour", "CI-43 huitieme representation refusee")
    c.viole(check_representations_de_classe(
        {k: v for k, v in rt0.items() if k != RUNTIME_L2_SUPERVISION},
        {k: v for k, v in _dep0.items() if k != RUNTIME_L2_SUPERVISION}),
        "non lue", "CI-43 fichier du perimetre non lu refuse")

    # ---- ASP-CI-44 : le depot livre passe -------------------------------
    _dom = sans_clotures(dom_m0)
    c.conforme(check_ancien_code_transitoire(rt0, _dep0, _dom),
               "CI-44 la population du code historique est celle du lot 2")

    # ---- ASP-CI-44 : une VRAIE occurrence technique supplementaire ------
    # Une SECONDE cle d'attribut, portee par un second capteur. Ce que la
    # detection compte est l'EMPLOI TECHNIQUE, pas le mot : un identifiant
    # VOISIN — `<code>_bis` — n'est pas une occurrence du code, et le
    # controle a raison de ne pas le compter.
    _second_capteur = (
        "- sensor:\n"
        '    - name: "Essai"\n'
        "      unique_id: aspirateur_essai\n"
        '      state: "x"\n'
        "      attributes:\n"
        f'        {ETAT_ORTHOGONAL}: "oui"\n'
        "- sensor:\n")
    c.viole(check_ancien_code_transitoire(
        _mut(rt0, RUNTIME_ETAT, "- sensor:\n", _second_capteur),
        _mut(_dep0, RUNTIME_ETAT, "- sensor:\n", _second_capteur), _dom),
        "attendu exactement un",
        "CI-44 seconde cle d'attribut chez le producteur")

    # ---- C2 : une MENTION n'est pas un EMPLOI — les deux restent verts ---
    # Un commentaire nommant le code ne repand rien : il ne cree ni cle
    # d'attribut, ni slot de restitution. Le refuser reviendrait a interdire
    # d'ecrire, dans le fichier meme qui le porte, ce que le lot 5 va faire.
    _note = f"\n# note de migration : {ETAT_ORTHOGONAL} bascule au lot 5\n"
    c.conforme(check_ancien_code_transitoire(
        _mut(rt0, RUNTIME_ETAT, "- sensor:\n", _note + "- sensor:\n"),
        _mut(_dep0, RUNTIME_ETAT, "- sensor:\n", _note + "- sensor:\n"),
        _dom),
        "CI-44 commentaire chez le producteur reste vert")
    c.conforme(check_ancien_code_transitoire(
        rt0, {**_dep0, _ui: _dep0[_ui] + _note}, _dom),
        "CI-44 commentaire dans le panneau reste vert")

    # ---- N1 : le COMMENTAIRE, sous ses trois formes ---------------------
    # Le helper est eprouve d'abord SEUL, sur des lignes construites : c'est
    # la seule facon de separer ce qu'il neutralise de ce que le controle en
    # fait ensuite. Puis les memes formes sont jouees sur les fichiers REELS.
    for _ligne, _att, _quoi in (
            (f"# {ETAT_ORTHOGONAL}", 0, "commentaire pleine ligne"),
            (f"    # {ETAT_ORTHOGONAL} indente", 0, "commentaire indente"),
            (f"attributes:  # {ETAT_ORTHOGONAL}, retire au lot 5", 0,
             "commentaire de fin de ligne, aucun emploi avant"),
            (f"      attribute: {ETAT_ORTHOGONAL}  # explicatif", 1,
             "EMPLOI avant le marqueur, commentaire apres"),
            (f'  c: "texte # {ETAT_ORTHOGONAL} en chaine"', 1,
             "marqueur DANS une chaine quotee"),
            (f'  couleur: "#ffffff"  # {ETAT_ORTHOGONAL}', 0,
             "marqueur colle a un mot, puis vrai commentaire")):
        _n = sans_commentaires_ligne(_ligne).count(ETAT_ORTHOGONAL)
        assert _n == _att, f"N1 : {_quoi} — compte {_n}, attendu {_att}"
        c.conformes += 1

    # Les memes formes, sur les fichiers geles : le controle reste VERT.
    for _rel, _forme, _quoi in (
            (RUNTIME_ETAT, f"\n# note : {ETAT_ORTHOGONAL} bascule au lot 5\n",
             "commentaire pleine ligne chez le producteur"),
            (RUNTIME_ETAT, f"\n    # {ETAT_ORTHOGONAL} — indente\n",
             "commentaire indente chez le producteur"),
            (_ui, f"\n# note : {ETAT_ORTHOGONAL} bascule au lot 5\n",
             "commentaire pleine ligne dans le panneau")):
        c.conforme(check_ancien_code_transitoire(
            rt0 if _rel == _ui else {**rt0, _rel: rt0[_rel] + _forme},
            {**_dep0, _rel: _dep0[_rel] + _forme}, _dom),
            f"CI-44 {_quoi} reste vert")

    # Un commentaire de FIN DE LIGNE, greffe sur une ligne qui ne porte aucun
    # emploi : le total ne doit pas bouger.
    _fin = _mut(_dep0, RUNTIME_ETAT, "      attributes:\n",
                f"      attributes:  # {ETAT_ORTHOGONAL}, migre au lot 5\n")
    assert yaml.safe_load(_fin[RUNTIME_ETAT]) is not None, \
        "N1 : la mutation de commentaire doit rester un YAML valide"
    c.conforme(check_ancien_code_transitoire(
        {**rt0, RUNTIME_ETAT: _fin[RUNTIME_ETAT]}, _fin, _dom),
        "CI-44 commentaire de fin de ligne reste vert")

    # L'EMPLOI reste compte quand un commentaire le suit sur la meme ligne :
    # la neutralisation coupe APRES le marqueur, jamais avant.
    _avant = _mut(_dep0, _ui,
                  f"              attribute: {ETAT_ORTHOGONAL}\n",
                  f"              attribute: {ETAT_ORTHOGONAL}\n"
                  f"              attribute: {ETAT_ORTHOGONAL}  # note\n")
    _errs_avant = check_ancien_code_transitoire(rt0, _avant, _dom)
    assert not any("illisible" in e for e in _errs_avant), \
        f"N1 : le rouge doit venir du COMPTAGE, pas d'un parse — {_errs_avant}"
    c.viole(_errs_avant, "occurrence(s) techniques",
            "CI-44 emploi suivi d'un commentaire reste compte")

    # ---- R1 : un EMPLOI qui n'est ni une cle ni un slot ------------------
    # Une lecture Jinja de l'attribut : l'analyse de FORME ne la voit pas —
    # ce n'est ni une cle d'attribut, ni un slot de restitution —, et seul
    # le TOTAL, commentaires neutralises, la rattrape. Les deux cas sont
    # joues sur les deux fichiers geles, car l'angle mort etait le meme.
    _jinja = (f"\n      lecture: \"{{{{ state_attr('sensor.{ID_ETAT_CANON}',"
              f" '{ETAT_ORTHOGONAL}') }}}}\"\n")
    c.viole(check_ancien_code_transitoire(
        _mut(rt0, RUNTIME_ETAT, "      attributes:\n",
             _jinja + "      attributes:\n"),
        _mut(_dep0, RUNTIME_ETAT, "      attributes:\n",
             _jinja + "      attributes:\n"), _dom),
        "occurrence(s) techniques",
        "CI-44 lecture Jinja de l'attribut chez le producteur")
    # La carte est inseree DANS la pile du panneau, a l'indentation reelle :
    # une mutation qui casserait le YAML rendrait rouge par illisibilite, et
    # ne prouverait rien du comptage qu'elle est censee eprouver.
    _carte = (f"  - type: markdown\n    content: \"{{{{ state_attr("
              f"'sensor.{ID_ETAT_CANON}', '{ETAT_ORTHOGONAL}') }}}}\"\n")
    _ui_carte = _mut(_dep0, _ui, "  - type: grid\n",
                     _carte + "  - type: grid\n")
    assert yaml.safe_load(_ui_carte[_ui]) is not None, \
        "R1 : la mutation de carte doit rester un YAML valide"
    _errs_carte = check_ancien_code_transitoire(rt0, _ui_carte, _dom)
    assert not any("illisible" in e for e in _errs_carte), \
        f"R1 : le rouge doit venir du COMPTAGE, pas d'un parse — {_errs_carte}"
    c.viole(_errs_carte, "occurrence(s) techniques",
            "CI-44 carte markdown lisant l'attribut dans le panneau")

    # Un CINQUIEME site de restitution : l'allowlist en gele quatre.
    _site = ("            - condition: state\n"
             "              entity: sensor.aspirateur_etat_canonique\n"
             f"              attribute: {ETAT_ORTHOGONAL}\n"
             "              state: oui\n")
    c.viole(check_ancien_code_transitoire(
        rt0, _mut(_dep0, _ui, _site, _site + _site), _dom),
        "slot(s) d'attribut", "CI-44 cinquieme site Lovelace refuse")

    # Une occurrence DEPLACEE hors allowlist : le fichier n'y figure pas.
    c.viole(check_ancien_code_transitoire(
        rt0, {**_dep0, RUNTIME_MOTIF: _dep0[RUNTIME_MOTIF]
              + f"\n# note : {ETAT_ORTHOGONAL}\n"}, _dom),
        "FERMÉE et NOMINATIVE", "CI-44 occurrence hors allowlist refusee")

    # ---- ASP-CI-44 : le NOUVEAU code, avant le lot 5 --------------------
    _prod_neuf = _mut(_dep0, RUNTIME_ETAT, "        classe_partition: >",
                      f'        {CODE_SESSION_LOT5}: "{{{{ 1 }}}}"\n'
                      "        classe_partition: >")
    c.viole(check_ancien_code_transitoire(
        _mut(rt0, RUNTIME_ETAT, "        classe_partition: >",
             f'        {CODE_SESSION_LOT5}: "{{{{ 1 }}}}"\n'
             "        classe_partition: >"), _prod_neuf, _dom),
        "aucune coexistence des deux noms",
        "CI-44 nouveau code au producteur refuse")
    c.viole(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, FICHIER_CONTRAT_TRANSITOIRE:
                    T08 + f"\n`{CODE_SESSION_LOT5}`\n"}),
            "le lot 2 aligne le LIBELLÉ",
            "CI-44 nouveau code au contrat refuse")

    # ---- ASP-CI-44 : le CONTRAT, et sa clause transitoire ---------------
    c.viole(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, FICHIER_CONTRAT_TRANSITOIRE:
                    T08.replace(ANCRE_CLAUSE_TRANSITOIRE, "Migration", 1)}),
        "a disparu du chapitre 08", "CI-44 clause 08 §1.3 effacee refusee")
    c.viole(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, FICHIER_CONTRAT_TRANSITOIRE:
                    T08 + f"\nRappel : `{ETAT_ORTHOGONAL}`.\n"}),
        "attendu 3", "CI-44 occurrence contractuelle ajoutee refusee")

    # ---- ASP-CI-44 / D4 : les chapitres AUTRES que le 08 ----------------
    # Le token technique n'a plus de place hors du 08 ; la formulation
    # METIER, elle, reste libre partout — c'est meme ce que le lot 2 y a
    # inscrit. Les trois cas sont joues separement pour que le vert du
    # troisieme prouve l'absence de faux positif, et non un oubli.
    _F15 = "15_conduite_et_supervision.md"
    assert _F15 in _dom, f"selftest D4 : `{_F15}` absent du domaine"
    c.viole(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, _F15: _dom[_F15] + f"\n`{ETAT_ORTHOGONAL}`\n"}),
        "hors du chapitre 08", "CI-44 ancien token porte au chapitre 15")
    c.viole(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, _F15: _dom[_F15] + f"\n`{CODE_SESSION_LOT5}`\n"}),
        "comme code technique", "CI-44 nouveau token porte au chapitre 15")
    c.conforme(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, _F15: _dom[_F15]
                     + "\nLa **session robot active** n'etablit pas la\n"
                     + "**mission Arsenal ouverte**.\n"}),
        "CI-44 formulation metier au chapitre 15 reste verte")

    # R2 — la CIBLE d'un lien est un chemin, pas du texte contractuel. Le
    # fichier d'arbitrage `Q1` porte le code de remplacement dans son NOM :
    # un chapitre doit pouvoir renvoyer a la note qui fonde la regle.
    _lien = ("\nVoir [`Q1`](../../audits/02_arbitrages/aspirateur/"
             "arbitrage_mission_arsenal_ouverte_et"
             "_session_robot_active.md).\n")
    assert CODE_SESSION_LOT5 in _lien, "R2 : le lien doit porter le token"
    c.conforme(check_ancien_code_transitoire(
        rt0, _dep0, {**_dom, _F15: _dom[_F15] + _lien}),
        "CI-44 lien Markdown vers Q1 au chapitre 15 reste vert")

    # ---- ASP-CI-45 : le runtime livre passe -----------------------------
    c.conforme(check_offre_gestes(rt0, _lov0),
               "CI-45 offre des gestes conforme au 15 §2.3")

    # ---- ASP-CI-45 : l'AUTORITE precede, et elle n'ecrit rien -----------
    _garde = ("    - choose:\n"
              "        - conditions:\n"
              "            - condition: template\n"
              "              value_template: >-\n"
              f"                {{{{ states('{ID_VERDICT}')\n"
              "                   not in verdict_ouvert }}\n"
              "          sequence:\n"
              "            - stop: \"Aucune mission Arsenal ouverte : le "
              "verdict n'est pas de classe O\"\n")
    c.viole(check_offre_gestes(_mut(rt0, RUNTIME_L2_CONDUITE, _garde, ""),
                               _lov0),
            "aucune garde de premier niveau", "CI-45 garde d'autorite absente")
    c.viole(check_offre_gestes(_mut(
        rt0, RUNTIME_L2_CONDUITE,
        "            - stop: \"Aucune mission Arsenal ouverte",
        "            - action: input_text.set_value\n"
        f"              target:\n                entity_id: {ID_VERDICT}\n"
        '              data:\n                value: "CLOTURE/FIN_NOMINALE"\n'
        "            - stop: \"Aucune mission Arsenal ouverte"), _lov0),
        "SANS RIEN ÉCRIRE", "CI-45 garde d'autorite qui ecrit le verdict")

    # ---- ASP-CI-45 : la POLARITE de la garde d'autorite -----------------
    # La mutation ATTEINT le controle : la garde reste reconnue — elle cite
    # toujours le helper et la table —, seule sa NEGATION disparait. Le
    # diagnostic attendu est donc celui de la polarite, jamais celui d'une
    # garde absente ; et l'ancre est asserte par `_mut`, de sorte qu'un test
    # vert par ancre evanouie est impossible.
    _pol = _mut(rt0, RUNTIME_L2_CONDUITE,
                f"                   {POLARITE_GARDE_AUTORITE} }}}}",
                "                   in verdict_ouvert }}")
    assert POLARITE_GARDE_AUTORITE not in _pol[RUNTIME_L2_CONDUITE], \
        "polarite : la mutation n'a pas retire la negation"
    assert ID_VERDICT in _pol[RUNTIME_L2_CONDUITE], \
        "polarite : la mutation a detruit la garde au lieu de l'inverser"
    c.viole(check_offre_gestes(_pol, _lov0),
            "polarité est INVERSÉE",
            "CI-45 garde d'autorite a la polarite inversee")

    # ---- ASP-CI-45 : ARRET — aucune restriction de sens physique --------
    c.viole(check_offre_gestes(_mut(
        rt0, RUNTIME_L2_CONDUITE,
        "              value_template: \"{{ geste == 'arret' }}\"\n"
        "          sequence:\n",
        "              value_template: \"{{ geste == 'arret' }}\"\n"
        "          sequence:\n"
        "            - choose:\n"
        "                - conditions:\n"
        "                    - condition: template\n"
        "                      value_template: >-\n"
        f"                        {{{{ not is_state('{NATIF_SESSION}', "
        "'on') }}\n"
        "                  sequence:\n"
        "                    - stop: \"Arret sans objet\"\n"), _lov0),
        "sans dépendre du témoin natif de session",
        "CI-45 garde de temoin natif posee sur l'arret")

    # ---- ASP-CI-45 : RETOUR BASE — trois exclusions, ni plus ni moins ---
    c.viole(check_offre_gestes(_mut(
        rt0, RUNTIME_L2_CONDUITE, '        retour: ["returning_home", '
        '"docking"]', '        retour: ["returning_home"]'), _lov0),
        "les deux états de la chaîne de retour",
        "CI-45 table retour amputee")
    c.viole(check_offre_gestes(_mut(
        rt0, RUNTIME_L2_CONDUITE, '        retour: ["returning_home", '
        '"docking"]', '        retour: ["returning_home", "docking", '
        '"paused"]'), _lov0),
        "les deux états de la chaîne de retour",
        "CI-45 exclusion surnumeraire refusee")
    c.viole(check_offre_gestes(_mut(
        rt0, RUNTIME_L2_CONDUITE, "{{ etat in retour or etat == 'charging' }}",
        "{{ etat in retour }}"), _lov0),
        "n'exclut pas `charging`", "CI-45 exclusion charging retiree")

    # ---- ASP-CI-45 : INTERFACE — non-regression AVANT le lot 6 ----------
    # Ces deux proprietes survivent au changement d'autorite du lot 6 : c'est
    # ce qui les rend gardables des maintenant, sans rien affirmer de faux
    # sur l'autorite que les sites lisent aujourd'hui.
    c.viole(check_offre_gestes(rt0, _mut(
        _lov0, _ui, "            - condition: state\n"
        "              entity: sensor.aspirateur_etat_canonique\n"
        "              state_not: amarrage\n", "")),
        "Renvoyer à la base", "CI-45 exclusion retiree du site retour")
    c.viole(check_offre_gestes(rt0, _mut(
        _lov0, _ui, f"              attribute: {ETAT_ORTHOGONAL}\n"
        "              state: oui\n          card:\n"
        "            type: custom:button-card\n"
        "            template: carte_action_standard_warning",
        f"              attribute: {ETAT_ORTHOGONAL}\n"
        "              state: oui\n"
        "            - condition: state\n"
        "              entity: sensor.aspirateur_etat_canonique\n"
        "              state_not: pause\n          card:\n"
        "            type: custom:button-card\n"
        "            template: carte_action_standard_warning")),
        "sans exclusion d'état", "CI-45 exclusion ajoutee au site arret")

    # ---- ASP-CI-11 etendu : l'allowlist n'est ni dormante ni une breche --
    c.conforme(refus_allowlist_lecteurs(LECTEURS_VERDICT),
               "CI-11 les deux lecteurs purs existent et sont hors Lovelace")
    c.viole(refus_allowlist_lecteurs(
        LECTEURS_VERDICT | {"12_template_sensors/aspirateur/"
                            "_essai_dormance.yaml"}),
        "autorisation DORMANTE",
        "CI-11 lecteur inscrit avant l'existence de son fichier")
    c.viole(refus_allowlist_lecteurs(LECTEURS_VERDICT | {_ui}),
            "arbre Lovelace", "CI-11 lecteur loge dans un arbre Lovelace")

    print(f"selftest OK — 45 contrôles logiques (ASP-CI-28 livré par le lot "
          f"U0 ; ASP-CI-43/44/45 par le lot 3 de C45), {c.total()} cas "
          f"({c.conformes} conformes, {c.violations} violations).")


# ═════════════════════════════════════════════════════════════
# NOTIFICATIONS — lot N1 : ASP-CI-37 … ASP-CI-39
#
# Les trois controles ne relisent pas le cadrage pour se donner raison. Ils
# confrontent le RUNTIME REEL a des constantes figees dans ce module, et —
# pour ASP-CI-38 — ils RENDENT la chaine complete : les gabarits M1 sur des
# etats natifs simules, puis les conditions de N1 sur la projection ainsi
# obtenue. Un faux vert supposerait donc de deplacer le juge, sous revue.
# ═════════════════════════════════════════════════════════════


def load_runtime_n1() -> dict[str, str]:
    """Tous les fichiers du dossier d'automations du domaine.

    On lit le DOSSIER, pas un fichier nomme : c'est ce qui rend detectable un
    TROISIEME writer glisse a cote. Chercher `RUNTIME_N1` seul laisserait
    passer exactement cela.
    """
    base = ROOT / DOSSIER_N1
    if not base.is_dir():
        return {}
    return {p.relative_to(ROOT).as_posix():
            p.read_text(encoding="utf-8", errors="ignore")
            for p in sorted(base.rglob("*.yaml")) if p.is_file()}


def _automations_n1(textes: dict[str, str]):
    """(fichier, mapping d'automation) pour chaque automation declaree."""
    out = []
    for rel, txt in sorted(textes.items()):
        try:
            doc = yaml.safe_load(txt)
        except yaml.YAMLError:
            out.append((rel, None))
            continue
        for a in (doc if isinstance(doc, list) else [doc]):
            if isinstance(a, dict):
                out.append((rel, a))
    return out


def _etapes_n1(noeud):
    """Aplatit une sequence d'actions, branches de `choose` comprises."""
    plat = []
    if isinstance(noeud, list):
        for x in noeud:
            plat += _etapes_n1(x)
    elif isinstance(noeud, dict):
        plat.append(noeud)
        for cle in ("sequence", "default", "then", "else", "actions"):
            plat += _etapes_n1(noeud.get(cle))
        for opt in noeud.get("choose") or []:
            if isinstance(opt, dict):
                plat += _etapes_n1(opt.get("sequence"))
    return plat


def _appels_notif(auto) -> list[tuple[str, dict]]:
    """(`create` | `dismiss`, data) de chaque appel de notification persistante."""
    out = []
    for st in _etapes_n1(auto.get("action") or auto.get("actions")):
        svc = st.get("service") or st.get("action")
        if not isinstance(svc, str):
            continue
        for verbe in ("create", "dismiss"):
            if svc == f"persistent_notification.{verbe}":
                out.append((verbe, st.get("data") or {}))
    return out


def check_writers_n1(n1: dict[str, str], depot: dict[str, str]) -> list[str]:
    """ASP-CI-37 — writers, identifiants, cycle de vie, readiness.

    Le point dur est la SYMETRIE : creation et suppression d'un meme
    identifiant de notification doivent vivre dans le MEME writer. Une
    creation sans suppression laisse une projection orpheline ; une
    suppression logee ailleurs fait deux autorites pour un seul etat.
    """
    errs: list[str] = []
    if not n1:
        return [f"ASP-CI-37 : dossier N1 introuvable — `{DOSSIER_N1}`. La "
                "projection persistante d'entretien n'existe pas."]

    autos = _automations_n1(n1)
    for rel, a in autos:
        if a is None:
            errs.append(f"ASP-CI-37 : `{rel}` est illisible en YAML.")
    autos = [(rel, a) for rel, a in autos if a is not None]
    if not autos:
        return errs or [f"ASP-CI-37 : aucune automation dans `{DOSSIER_N1}`."]

    # ── (a0) aucun identifiant du domaine hors des deux attribues, OU QUE
    # CE SOIT dans le texte du dossier — commentaires et formes non parsees
    # comprises. Le parseur YAML ne voit que ce qu'il sait lire ; cette garde
    # ne depend d'aucune forme.
    for rel, txt in sorted(n1.items()):
        for m in AID_DOMAINE.finditer(txt):
            aid = m.group(1)
            if aid in AID_N1_AUTORISES:
                continue
            motif = AID_HORS_N1.get(aid, "hors des identifiants attribues au "
                                          "lot N1")
            errs.append(f"ASP-CI-37 : `{rel}` porte l'identifiant `{aid}` — "
                        f"{motif}.")

    # ── (a) identifiants d'automation : exactement ceux qui sont autorises ──
    vus: dict[str, list[str]] = {}
    for rel, a in autos:
        aid = a.get("id")
        if not isinstance(aid, str):
            errs.append(f"ASP-CI-37 : `{rel}` declare une automation sans "
                        "`id:` en CHAINE (doctrine id_automatisations).")
            continue
        vus.setdefault(aid, []).append(rel)
        attendu = FICHIER_DE_L_AID.get(aid)
        if attendu and rel != attendu:
            errs.append(f"ASP-CI-37 : `{aid}` est declare dans `{rel}` — "
                        f"attendu `{attendu}`. La table nomme chaque "
                        "automation AVEC son fichier : un identifiant deplace "
                        "d'un fichier a l'autre change de nature sans que "
                        "rien ne le signale.")
        if aid in AID_HORS_N1:
            errs.append(f"ASP-CI-37 : `{rel}` porte `{aid}` — {AID_HORS_N1[aid]}. "
                        "Cet identifiant n'appartient pas au lot N1.")
        elif aid not in AID_N1_AUTORISES:
            errs.append(f"ASP-CI-37 : `{rel}` porte l'identifiant `{aid}`, hors "
                        f"des identifiants attribues au dossier "
                        f"{sorted(AID_N1_AUTORISES)} (ASP-INV-58 — aucun "
                        "identifiant invente).")
    for aid, fichiers in sorted(vus.items()):
        if len(fichiers) > 1:
            errs.append(f"ASP-CI-37 : l'identifiant `{aid}` est porte par "
                        f"{len(fichiers)} automations {fichiers} — un "
                        "identifiant n'est jamais reutilise.")

    # Le writer de maintenance existe, et il est unique.
    if AID_N1_MAINTENANCE not in vus:
        errs.append(f"ASP-CI-37 : le writer de la projection de maintenance "
                    f"`{AID_N1_MAINTENANCE}` est ABSENT du domaine.")

    # ── (b) aucun troisieme writer : le dossier ne porte que les autorises ──
    if len(autos) > len(AID_N1_AUTORISES):
        errs.append(f"ASP-CI-37 : `{DOSSIER_N1}` declare {len(autos)} "
                    f"automations pour au plus {len(AID_N1_AUTORISES)} "
                    "identifiants attribues — un writer de plus est apparu.")

    # ── (c) verrou de la projection de mission, differee ────────────────────
    if VERROU_N1_MISSION:
        if AID_N1_MISSION in vus:
            errs.append(
                f"ASP-CI-37 : `{AID_N1_MISSION}` — projection persistante de "
                "MISSION — est construite alors que son autorite d'EXTINCTION "
                "n'existe pas : la classe T du vocabulaire L1 est vide "
                "(07_MACHINE_L2 §4.1). Une projection creee ici ne pourrait "
                "plus s'eteindre. Le verrou `VERROU_N1_MISSION` se leve dans "
                "le lot qui livre un writer de classe T, sous revue.")
        # Ancre sur une INSTANCIATION reelle. Le nom nu `aspirateur_mission`
        # est un PREFIXE de `input_text.aspirateur_mission_verdict`, helper
        # legitime du lot L1 : le chercher tel quel accuserait trois fichiers
        # innocents et rendrait le controle inutilisable.
        for rel, txt in sorted(depot.items()):
            if re.search(rf"notification_id[ \t]*:[ \t]*[\"']?"
                         rf"{re.escape(NOTIF_N1_MISSION)}\b", txt):
                errs.append(f"ASP-CI-37 : `{rel}` instancie la notification "
                            f"`{NOTIF_N1_MISSION}`, dont le volet est DIFFERE "
                            "au lot L2.")

    # ── (d) identifiants de notification : fermes, uniques, un seul writer ──
    par_notif: dict[str, set[str]] = {}
    for rel, a in autos:
        appels = _appels_notif(a)
        if not appels and rel in PROJECTIONS_PURES:
            errs.append(f"ASP-CI-37 : `{rel}` ne projette aucune notification "
                        "persistante — un writer de projection sans projection.")
        verbes: dict[str, set[str]] = {}
        for verbe, data in appels:
            nid = data.get("notification_id")
            if not isinstance(nid, str) or not nid:
                errs.append(f"ASP-CI-37 : `{rel}` appelle "
                            f"`persistent_notification.{verbe}` sans "
                            "`notification_id` litteral — l'anti-doublon est "
                            "structurel, il exige un identifiant stable.")
                continue
            if "{{" in nid:
                errs.append(f"ASP-CI-37 : `{rel}` porte un `notification_id` "
                            f"TEMPLATISE `{nid}` — un identifiant qui se "
                            "calcule n'est plus stable, et il empile.")
                continue
            if nid not in NOTIF_N1_FERMES:
                errs.append(f"ASP-CI-37 : `{rel}` emploie le "
                            f"`notification_id` `{nid}`, hors de l'ensemble "
                            f"ferme {sorted(NOTIF_N1_FERMES)} "
                            "(08_NOTIFICATIONS.md §1).")
                continue
            verbes.setdefault(nid, set()).add(verbe)
            par_notif.setdefault(nid, set()).add(rel)
        # Creation ET suppression, dans le MEME writer.
        for nid, v in sorted(verbes.items()):
            if v != {"create", "dismiss"}:
                manque = {"create", "dismiss"} - v
                errs.append(f"ASP-CI-37 : `{rel}` porte `{nid}` sans "
                            f"{sorted(manque)} — creation et suppression "
                            "vivent dans le meme writer, faute de quoi la "
                            "projection survit a son etat (contrat "
                            "Notifications, § Cycle de vie).")
    for nid, fichiers in sorted(par_notif.items()):
        if len(fichiers) > 1:
            errs.append(f"ASP-CI-37 : `{nid}` est ecrit par {len(fichiers)} "
                        f"fichiers {sorted(fichiers)} — un etat metier n'a "
                        "qu'UN writer.")
    instancies = frozenset(par_notif)
    if instancies != NOTIF_N1_INSTANCIES:
        errs.append(f"ASP-CI-37 : le lot instancie {sorted(instancies)} ; il "
                    f"doit instancier exactement {sorted(NOTIF_N1_INSTANCIES)} "
                    "— le canal de mission est DIFFERE.")

    # ── (e) aucun writer hors du domaine ne touche les deux identifiants ────
    for rel, txt in sorted(depot.items()):
        if rel in n1:
            continue
        for nid in sorted(NOTIF_N1_FERMES):
            if re.search(rf"notification_id[ \t]*:[ \t]*[\"']?{re.escape(nid)}\b",
                         txt):
                errs.append(f"ASP-CI-37 : `{rel}` — hors du domaine — ecrit la "
                            f"notification `{nid}`.")

    # ── (f) writer de maintenance : mode, readiness, autorite, titre ────────
    cible = [(rel, a) for rel, a in autos
             if a.get("id") == AID_N1_MAINTENANCE]
    for rel, a in cible:
        if a.get("mode") not in MODES_N1:
            errs.append(f"ASP-CI-37 : `{rel}` porte `mode: {a.get('mode')!r}` "
                        f"— attendu l'un de {sorted(MODES_N1)}. `single` "
                        "abandonnerait EN SILENCE le second declenchement "
                        "d'un franchissement de seuil.")
        decl = a.get("trigger") or a.get("triggers") or []
        cibles_decl = set()
        readiness = False
        for t in decl if isinstance(decl, list) else [decl]:
            if not isinstance(t, dict):
                continue
            eids = t.get("entity_id")
            eids = [eids] if isinstance(eids, str) else list(eids or [])
            cibles_decl.update(eids)
            if READINESS_N1 in eids and t.get("to") == "on":
                readiness = True
            # ── Le declencheur de LISTE doit etre borne a `postes_dus`.
            # Un declencheur d'etat sans `to:`, sans `from:` et sans
            # `attribute:` passe en `match_all` cote Home Assistant : il part
            # alors sur tout changement d'etat OU D'ATTRIBUT. L'attribut
            # `postes` de l'autorite republiant `restant_h` et
            # `restant_pourcentage`, un declencheur nu reveillerait la
            # projection a chaque decroissance d'un compteur natif — le
            # rythme du coordinateur, precisement ce que l'interposition des
            # deux entites derivees du §4.2 sert a empecher.
            if ENTITE_M1_LISTE in eids:
                attr = t.get("attribute")
                if attr != ATTRIBUT_N1_DECLENCHEUR:
                    errs.append(
                        f"ASP-CI-37 : `{rel}` se declenche sur "
                        f"`{ENTITE_M1_LISTE}` avec "
                        f"`attribute: {attr!r}` — attendu "
                        f"`{ATTRIBUT_N1_DECLENCHEUR}`. Sans cette borne, Home "
                        "Assistant passe le declencheur en `match_all` et le "
                        "fait partir sur TOUT changement d'attribut, "
                        "`postes` compris : la notification serait reecrite "
                        "au rythme du coordinateur "
                        "(08_NOTIFICATIONS.md §4.2).")
            # ── Le declencheur du TEMOIN doit rester generique. Le borner a
            # un attribut lui ferait manquer ses transitions d'ETAT, qui sont
            # justement le franchissement de seuil.
            if ENTITE_M1_TEMOIN in eids and t.get("attribute") is not None:
                errs.append(
                    f"ASP-CI-37 : `{rel}` borne le declencheur du temoin "
                    f"`{ENTITE_M1_TEMOIN}` a l'attribut "
                    f"`{t.get('attribute')}` — le temoin doit se declencher "
                    "sur son ETAT : c'est lui qui porte le franchissement de "
                    "seuil.")
        if not readiness:
            errs.append(f"ASP-CI-37 : `{rel}` n'a pas de declencheur "
                        f"`{READINESS_N1}` -> `on`. Home Assistant NE RESTAURE "
                        "PAS les notifications persistantes : sans cette "
                        "re-projection, un entretien du devient silencieux "
                        "apres un redemarrage.")
        attendus = set(AUTORITE_N1) | {READINESS_N1}
        if cibles_decl != attendus:
            errs.append(f"ASP-CI-37 : `{rel}` se declenche sur "
                        f"{sorted(cibles_decl)} — attendu exactement "
                        f"{sorted(attendus)}. Se brancher sur un capteur natif "
                        "reecrirait la notification au rythme du coordinateur "
                        "(08_NOTIFICATIONS.md §4.2).")
        # Le titre exact, et lui seul.
        for verbe, data in _appels_notif(a):
            if verbe != "create":
                continue
            titre = str(data.get("title") or "")
            if titre != TITRE_N1_ENTRETIEN:
                errs.append(f"ASP-CI-37 : `{rel}` porte le titre {titre!r} — "
                            f"attendu {TITRE_N1_ENTRETIEN!r} "
                            "(08_NOTIFICATIONS.md §2).")
            msg = str(data.get("message") or "")
            lus = set(re.findall(
                r"state_attr\(\s*['\"]([a-z_.]+)['\"]\s*,\s*['\"]([a-z_]+)['\"]",
                msg))
            if lus != {(ENTITE_M1_LISTE, ATTRIBUT_N1_MESSAGE)}:
                errs.append(f"ASP-CI-37 : le message lit {sorted(lus)} — il ne "
                            f"lit QUE `{ATTRIBUT_N1_MESSAGE}` de "
                            f"`{ENTITE_M1_LISTE}`. Lire un autre attribut "
                            "ouvrirait la duree chiffree, proscrite par "
                            "08_NOTIFICATIONS.md §4.2.")
            if re.search(r"states\(", msg):
                errs.append("ASP-CI-37 : le message appelle `states(` — le "
                            "contenu derive de l'attribut d'autorite, jamais "
                            "d'une lecture libre.")

    # ── (f bis) writer de la projection de MISSION — lot L2 ────────────────
    #
    # Symetrique du (f), sur l'autre canal persistant. Son autorite n'est pas
    # une paire d'entites derivees mais le VERDICT lui-meme : c'est la seule
    # memoire de mission ouverte du domaine (D-08), et se brancher ailleurs
    # adopterait une mission externe.
    cible_mission = [(rel, a) for rel, a in autos
                     if a.get("id") == AID_N1_MISSION]
    if len(cible_mission) != 1:
        errs.append(f"ASP-CI-37 : {len(cible_mission)} writer(s) "
                    f"`{AID_N1_MISSION}` — la projection persistante de "
                    "mission doit exister exactement une fois : le lot L2 "
                    "livre l'autorite d'extinction qui lui manquait.")
    for rel, a in cible_mission:
        if a.get("mode") not in MODES_N1:
            errs.append(f"ASP-CI-37 : `{rel}` porte `mode: {a.get('mode')!r}` "
                        f"— attendu l'un de {sorted(MODES_N1)}. Un geste de "
                        "conduite ecrit son engagement puis son issue en deux "
                        "ecritures rapprochees : c'est la DERNIERE qui fait "
                        "foi.")
        decl = a.get("trigger") or a.get("triggers") or []
        cibles_decl = set()
        readiness = False
        for t in decl if isinstance(decl, list) else [decl]:
            if not isinstance(t, dict):
                continue
            eids = t.get("entity_id")
            eids = [eids] if isinstance(eids, str) else list(eids or [])
            cibles_decl.update(eids)
            if READINESS_N1 in eids and t.get("to") == "on":
                readiness = True
        if not readiness:
            errs.append(f"ASP-CI-37 : `{rel}` n'a pas de declencheur "
                        f"`{READINESS_N1}` -> `on`. Home Assistant NE RESTAURE "
                        "PAS les notifications persistantes, alors que le "
                        "verdict, lui, EST restaure : sans re-projection, une "
                        "mission ouverte devient silencieuse apres un "
                        "redemarrage.")
        attendus = {ID_VERDICT, READINESS_N1}
        if cibles_decl != attendus:
            errs.append(f"ASP-CI-37 : `{rel}` se declenche sur "
                        f"{sorted(cibles_decl)} — attendu exactement "
                        f"{sorted(attendus)}. Se brancher sur un temoin natif "
                        "adopterait une mission externe (ASP-INV-87, D-06).")
        for verbe, data in _appels_notif(a):
            if verbe != "create":
                continue
            titre = str(data.get("title") or "")
            if titre != TITRE_N1_MISSION:
                errs.append(f"ASP-CI-37 : `{rel}` porte le titre {titre!r} — "
                            f"attendu {TITRE_N1_MISSION!r} "
                            "(08_NOTIFICATIONS.md §2).")
        # Les deux ensembles de classe, confrontes au vocabulaire : une liste
        # de valeurs recopiee a la main derive tot ou tard.
        for st in _etapes_n1(a.get("action") or a.get("actions")):
            for cle, attendu_ens in (("verdict_ouvert", CLASSE_O),
                                     ("verdict_terminal", CLASSE_T)):
                val = (st.get("variables") or {}).get(cle)
                if val is None:
                    continue
                vus_ens = set(val) if isinstance(val, list) else set()
                if vus_ens != set(attendu_ens):
                    errs.append(
                        f"ASP-CI-37 : `{rel}` declare `{cle}` = "
                        f"{sorted(vus_ens)} — attendu exactement "
                        f"{sorted(attendu_ens)}. Une classe recopiee a la "
                        "main derive du vocabulaire, et la projection "
                        "cesserait alors de s'allumer ou de s'eteindre "
                        "(contrat 15 §2).")

    # ── (g) le `choose` du writer n'a AUCUNE branche par defaut ─────────────
    for rel, a in cible:
        for st in _etapes_n1(a.get("action") or a.get("actions")):
            if "choose" in st and st.get("default") is not None:
                errs.append(f"ASP-CI-37 : `{rel}` porte une branche "
                            "`default:` — elle ferait tomber la suppression "
                            "sur une projection INDISPONIBLE, convertissant un "
                            "trou d'information en « aucun entretien » "
                            "(ASP-INV-76).")
    return errs


# ── ASP-CI-38 : la chaine M1 -> N1, RENDUE ─────────────────────────────────

def _projeter_m1(m1: str, natifs: dict[str, object]) -> dict[str, object]:
    """Rend les gabarits REELS de M1 sur des etats natifs simules.

    C'est ce qui ancre N1 sur M1 et sur rien d'autre : la projection n'est pas
    ecrite a la main ici, elle est CALCULEE par le fichier M1 tel qu'il est
    livre. Reecrire M1 change donc ce que N1 recoit — et le rendu le voit.
    """
    liste, temoin, _ = entites_m1(m1)
    if not isinstance(liste, dict) or not isinstance(temoin, dict):
        raise AssertionError("projection M1 illisible")
    vars_m1 = liste.get("variables") or {}
    etat = str(rendu_m1(liste["state"], natifs, **vars_m1))
    attrs = {cle: rendu_m1(gab, natifs, **vars_m1)
             for cle, gab in (liste.get("attributes") or {}).items()}
    monde = {ENTITE_M1_LISTE: {"state": etat, "attrs": attrs}}
    dispo = rendu_m1(temoin["availability"], monde)
    if dispo is True:
        brut = rendu_m1(temoin["state"], monde)
        etat_temoin = "on" if brut is True else "off"
    else:
        etat_temoin = "unavailable"
    monde[ENTITE_M1_TEMOIN] = {"state": etat_temoin, "attrs": {}}
    return monde


def _condition_n1(cond, monde) -> bool:
    """Rend UNE condition Home Assistant. Refuse ce qu'elle ne sait pas rendre."""
    if not isinstance(cond, dict):
        raise AssertionError(f"condition non structuree : {cond!r}")
    kind = cond.get("condition")
    if kind not in CONDITIONS_N1_RENDABLES:
        raise AssertionError(
            f"ASP-CI-38 ne sait pas rendre `condition: {kind}` — un "
            "evaluateur silencieusement incomplet rendrait un faux vert.")
    if kind == "template":
        return rendu_m1(cond["value_template"], monde) is True
    eids = cond.get("entity_id")
    eids = [eids] if isinstance(eids, str) else list(eids or [])
    attendu = cond.get("state")
    attendus = attendu if isinstance(attendu, list) else [attendu]
    for eid in eids:
        v = monde.get(eid)
        courant = v["state"] if isinstance(v, dict) else v
        if str(courant) not in [str(x) for x in attendus]:
            return False
    return bool(eids)


def _resoudre_n1(auto, monde) -> tuple[str, str]:
    """(`create` | `dismiss` | `rien`, message rendu) sur un monde simule."""
    for st in _etapes_n1(auto.get("action") or auto.get("actions")):
        options = st.get("choose")
        if not isinstance(options, list):
            continue
        for opt in options:
            conds = opt.get("conditions") or []
            conds = conds if isinstance(conds, list) else [conds]
            if all(_condition_n1(c, monde) for c in conds):
                for verbe, data in _appels_notif({"action": opt.get("sequence")}):
                    msg = str(data.get("message") or "")
                    rendu = (str(rendu_m1(msg, monde)) if "{{" in msg else msg)
                    return verbe, rendu
                return "rien", ""
        if st.get("default") is not None:
            for verbe, data in _appels_notif({"action": st.get("default")}):
                return verbe, ""
    return "rien", ""


# Les huit scenarios exiges, plus les pieges adverses. Chaque ligne porte les
# QUATRE compteurs natifs — filtre, principale, laterale, capteurs, en heures,
# plafonds 150/300/200/30 — et l'issue ATTENDUE de la projection N1.
SCENARIOS_N1 = (
    # (libelle, natifs, action attendue, postes attendus dans le message)
    ("1 · aucun poste du, projection complete",
     (100.0, 200.0, 150.0, 10.0), "dismiss", ()),
    ("2 · un poste du",
     (100.0, 200.0, 150.0, 2.0), "create", ("Nettoyage des capteurs",)),
    ("3 · plusieurs postes dus",
     (10.0, 200.0, 150.0, 1.0), "create", ("Filtre", "Nettoyage des capteurs")),
    ("4 · un poste du + un poste NON EVALUABLE",
     ("unavailable", 200.0, 150.0, 2.0), "create", ("Nettoyage des capteurs",)),
    ("5 · projection ENTIEREMENT non evaluable",
     ("unavailable", "unavailable", "unknown", "unavailable"), "rien", ()),
    ("8 · entretien redevenu non du apres remise a zero M2",
     (100.0, 200.0, 150.0, 30.0), "dismiss", ()),
    # ── pieges adverses : aucune suppression sur un trou d'information ──
    ("adverse · un seul poste illisible, aucun autre du",
     (100.0, 200.0, 150.0, "unavailable"), "rien", ()),
    ("adverse · capteur absent du registre",
     (100.0, 200.0, 150.0, None), "rien", ()),
    ("adverse · valeur non numerique",
     (100.0, 200.0, 150.0, "abc"), "rien", ()),
    ("adverse · seuil atteint PILE (10 % exactement)",
     (100.0, 200.0, 150.0, 3.0), "create", ("Nettoyage des capteurs",)),
)


def _natifs_n1(valeurs) -> dict[str, object]:
    """Les quatre compteurs natifs, dans l'ordre du perimetre fige."""
    sources = [POSTES_ENTRETIEN[k][0]
               for k in ("filtre", "brosse principale", "brosse laterale",
                         "capteurs")]
    return {s: v for s, v in zip(sources, valeurs) if v is not None}


def check_projection_n1_rendue(n1: dict[str, str], m1: str) -> list[str]:
    """ASP-CI-38 — les huit scenarios, joues sur la chaine REELLE M1 -> N1.

    Rien n'est cherche a la regex : les gabarits M1 sont rendus sur des etats
    natifs simules, puis les conditions de N1 sont rendues sur la projection
    obtenue. Ce que le controle affirme, il l'a execute.
    """
    errs: list[str] = []
    if not n1:
        return [f"ASP-CI-38 : dossier N1 introuvable — `{DOSSIER_N1}`."]
    if not m1:
        return [f"ASP-CI-38 : runtime M1 introuvable — `{RUNTIME_M1}`. La "
                "projection de maintenance n'a plus d'autorite."]
    cible = [a for _, a in _automations_n1(n1)
             if isinstance(a, dict) and a.get("id") == AID_N1_MAINTENANCE]
    if len(cible) != 1:
        return [f"ASP-CI-38 : {len(cible)} writer(s) `{AID_N1_MAINTENANCE}` — "
                "il en faut exactement un pour rendre les scenarios."]
    auto = cible[0]

    # ── Prealable : TOUTE condition du writer doit etre d'un type que
    # l'evaluateur sait rendre fidelement. On le verifie AVANT de rendre quoi
    # que ce soit, et on s'arrete la si ce n'est pas le cas : un evaluateur
    # qui rencontrerait un type inconnu en cours de route rendrait un verdict
    # partiel, c'est-a-dire un faux vert sur les scenarios non atteints.
    inconnus = set()
    for st in _etapes_n1(auto.get("action") or auto.get("actions")):
        for opt in st.get("choose") or []:
            conds = opt.get("conditions") if isinstance(opt, dict) else None
            conds = conds if isinstance(conds, list) else [conds]
            for cond in conds:
                if not isinstance(cond, dict):
                    inconnus.add(repr(cond))
                elif cond.get("condition") not in CONDITIONS_N1_RENDABLES:
                    inconnus.add(str(cond.get("condition")))
    if inconnus:
        return [f"ASP-CI-38 ne sait pas rendre `condition: {k}` — un "
                "evaluateur silencieusement incomplet rendrait un faux vert. "
                "Etendre l'evaluateur est un changement de frontiere CI, "
                "soumis a revue." for k in sorted(inconnus)]

    libelles = list(ORDRE_M1)
    for nom, natifs, attendu, dus in SCENARIOS_N1:
        monde = _projeter_m1(m1, _natifs_n1(natifs))
        try:
            action, message = _resoudre_n1(auto, monde)
        except AssertionError as exc:
            errs.append(f"ASP-CI-38 : {nom} — {exc}")
            continue
        etat_l = monde[ENTITE_M1_LISTE]["state"]
        etat_t = monde[ENTITE_M1_TEMOIN]["state"]
        if action != attendu:
            errs.append(
                f"ASP-CI-38 : {nom} — la projection M1 rend "
                f"`{etat_l}` / temoin `{etat_t}`, et N1 conclut `{action}` ; "
                f"attendu `{attendu}`.")
            continue
        if action != "create":
            continue
        # Le message nomme EXACTEMENT les postes dus, dans l'ordre canonique.
        cites = [lib for lib in ORDRE_M1 if lib in message]
        if tuple(cites) != tuple(dus):
            errs.append(f"ASP-CI-38 : {nom} — le message nomme {cites} ; "
                        f"attendu {list(dus)}, dans l'ordre canonique.")
        for lib in libelles:
            if lib not in dus and lib in message:
                errs.append(f"ASP-CI-38 : {nom} — le message nomme « {lib} », "
                            "qui n'est pas du. Un poste illisible n'est ni du "
                            "ni solde (ASP-INV-76).")
        # Aucune duree chiffree, aucun pourcentage, aucune date.
        for motif, quoi in ((r"\d+([.,]\d+)?\s*(h|heure|%)", "une duree ou un "
                             "pourcentage"),
                            (r"\b20\d\d\b", "une annee")):
            m = re.search(motif, message, re.I)
            if m:
                errs.append(f"ASP-CI-38 : {nom} — le message porte "
                            f"{quoi} ({m.group(0)!r}) : une notification "
                            "persistante decrit un etat, pas une mesure qui "
                            "court (08_NOTIFICATIONS.md §4.2).")

    # ── scenario 7 : contenu devenu different, sans empilement ──────────────
    m_un = _resoudre_n1(auto, _projeter_m1(m1, _natifs_n1(
        (100.0, 200.0, 150.0, 2.0))))
    m_deux = _resoudre_n1(auto, _projeter_m1(m1, _natifs_n1(
        (10.0, 200.0, 150.0, 1.0))))
    if not (m_un[0] == m_deux[0] == "create"):
        errs.append("ASP-CI-38 : 7 · les deux etats successifs devraient tous "
                    f"deux creer — rendus {m_un[0]} puis {m_deux[0]}.")
    elif m_un[1] == m_deux[1]:
        errs.append("ASP-CI-38 : 7 · la liste des postes dus a change et le "
                    "message NE CHANGE PAS — la notification afficherait un "
                    "contenu perime.")
    # ── charge numerique qui bouge, `postes_dus` inchange ──────────────────
    # Les deux releves ci-dessous ne different que par le restant du FILTRE,
    # qui n'est du dans aucun des deux : la liste des postes dus est la meme.
    # La projection doit donc rendre EXACTEMENT la meme chose. Combine au
    # declencheur borne d'ASP-CI-37, cela ferme les deux faces du reveil
    # parasite : il n'a pas lieu, et il serait de toute facon sans effet.
    charge_a = _resoudre_n1(auto, _projeter_m1(m1, _natifs_n1(
        (100.0, 200.0, 150.0, 2.0))))
    charge_b = _resoudre_n1(auto, _projeter_m1(m1, _natifs_n1(
        (99.4, 200.0, 150.0, 2.0))))
    if charge_a != charge_b:
        errs.append(
            "ASP-CI-38 : une simple evolution de la charge numerique — "
            f"`{ATTRIBUT_N1_MESSAGE}` inchange — fait passer la projection de "
            f"{charge_a!r} a {charge_b!r}. Le message ne doit dependre QUE de "
            f"`{ATTRIBUT_N1_MESSAGE}` : sans quoi la notification suivrait le "
            "rythme du coordinateur (08_NOTIFICATIONS.md §4.2).")

    ids = {d.get("notification_id") for v, d in _appels_notif(auto)}
    if len(ids) != 1:
        errs.append(f"ASP-CI-38 : 7 · le writer emploie {len(ids)} "
                    f"identifiants de notification {sorted(map(str, ids))} — "
                    "l'anti-doublon est structurel, il exige UN identifiant "
                    "stable, sans quoi les notifications s'empilent.")

    # ── scenario 6 : redemarrage, entretien du ──────────────────────────────
    decl = auto.get("trigger") or auto.get("triggers") or []
    readiness = any(isinstance(t, dict) and t.get("to") == "on"
                    and READINESS_N1 in ([t.get("entity_id")]
                                         if isinstance(t.get("entity_id"), str)
                                         else list(t.get("entity_id") or []))
                    for t in decl)
    du, _ = _resoudre_n1(auto, _projeter_m1(m1, _natifs_n1(
        (100.0, 200.0, 150.0, 2.0))))
    if not (readiness and du == "create"):
        errs.append("ASP-CI-38 : 6 · redemarrage avec un entretien du — "
                    f"declencheur de readiness {'present' if readiness else 'ABSENT'}, "
                    f"issue rendue `{du}`. La re-projection au passage de "
                    f"`{READINESS_N1}` a `on` est la SEULE voie : Home "
                    "Assistant ne restaure pas les persistantes.")

    # ── piege : temoin faux ET liste non evaluable — jamais de suppression ──
    incoherent = {ENTITE_M1_LISTE: {"state": ETAT_M1_NON_EVAL,
                                    "attrs": {"postes_dus": []}},
                  ENTITE_M1_TEMOIN: {"state": "off", "attrs": {}}}
    action, _ = _resoudre_n1(auto, incoherent)
    if action != "rien":
        errs.append(f"ASP-CI-38 : temoin `off` alors que la liste vaut "
                    f"`{ETAT_M1_NON_EVAL}` — N1 conclut `{action}`. Les DEUX "
                    "faces de l'autorite sont exigees pour supprimer : une "
                    "seule, faussee, effacerait une dette reelle.")
    for etat_l in ("unknown", "unavailable"):
        monde = {ENTITE_M1_LISTE: {"state": etat_l, "attrs": {}},
                 ENTITE_M1_TEMOIN: {"state": "unavailable", "attrs": {}}}
        action, _ = _resoudre_n1(auto, monde)
        if action != "rien":
            errs.append(f"ASP-CI-38 : projection a `{etat_l}` — N1 conclut "
                        f"`{action}`. Une indisponibilite ne vaut ni « aucun "
                        "entretien », ni une dette (ASP-INV-45, ASP-INV-74).")

    # ── La suppression est FERMEE, sur deux plans complementaires ──────────
    #
    # (1) STRUCTURELLEMENT. La face « synthese » de l'autorite doit exiger le
    #     SCALAIRE `aucun`, jamais une liste de valeurs acceptees. Une liste
    #     elargie — `[aucun, unknown]` — laisse passer TOUS les scenarios
    #     nominaux : elle ne casse rien, et c'est precisement pourquoi seule
    #     une garde de forme l'attrape. Home Assistant accepte les deux
    #     ecritures ; le lot n'en accepte qu'une.
    errs += _suppression_fermee_n1(auto)

    # (2) PAR RENDU ADVERSE. Le temoin est faux, et la synthese n'etablit
    #     PAS un nominal fiable. Aucun de ces quatre mondes ne doit supprimer.
    #     Le quatrieme est le plus fin : l'etat DIT `aucun`, mais l'attribut
    #     d'autorite a disparu — un nominal porte par une entite dont
    #     l'attribut manque n'est pas une autorite.
    for libelle, etat_l, attrs in (
            ("synthese `unknown`", "unknown", {}),
            ("synthese `unavailable`", "unavailable", {}),
            (f"synthese `{ETAT_M1_NON_EVAL}`", ETAT_M1_NON_EVAL,
             {ATTRIBUT_N1_MESSAGE: []}),
            (f"etat `{ETAT_M1_AUCUN}` mais attribut "
             f"`{ATTRIBUT_N1_MESSAGE}` ABSENT", ETAT_M1_AUCUN,
             {"postes_non_dus": []})):
        monde = {ENTITE_M1_LISTE: {"state": etat_l, "attrs": attrs},
                 ENTITE_M1_TEMOIN: {"state": "off", "attrs": {}}}
        action, _ = _resoudre_n1(auto, monde)
        if action != "rien":
            errs.append(
                f"ASP-CI-38 : temoin `off` + {libelle} — N1 conclut "
                f"`{action}`. La suppression n'est autorisee que si les DEUX "
                f"faces etablissent un nominal FIABLE : temoin `off`, etat "
                f"`{ETAT_N1_SUPPRESSION}`, et attribut "
                f"`{ATTRIBUT_N1_MESSAGE}` present et vide. Une seule face, "
                "faussee, effacerait une dette reelle (ASP-INV-76).")
    return errs


def _branche_suppression_n1(auto):
    """L'option du `choose` dont la sequence supprime la notification."""
    for st in _etapes_n1(auto.get("action") or auto.get("actions")):
        for opt in st.get("choose") or []:
            if not isinstance(opt, dict):
                continue
            verbes = {v for v, _ in _appels_notif({"action": opt.get("sequence")})}
            if "dismiss" in verbes:
                return opt
    return None


def _suppression_fermee_n1(auto) -> list[str]:
    """La condition de suppression exige-t-elle le scalaire, et lui seul ?"""
    opt = _branche_suppression_n1(auto)
    if opt is None:
        return ["ASP-CI-38 : aucune branche du `choose` ne supprime la "
                "notification — la projection survivrait a son etat."]
    conds = opt.get("conditions") or []
    conds = conds if isinstance(conds, list) else [conds]
    vus = 0
    errs: list[str] = []
    for c in conds:
        if not isinstance(c, dict) or c.get("entity_id") != ENTITE_M1_LISTE:
            continue
        vus += 1
        etat = c.get("state")
        if isinstance(etat, str):
            if etat != ETAT_N1_SUPPRESSION:
                errs.append(
                    f"ASP-CI-38 : la suppression exige l'etat `{etat}` — "
                    f"attendu `{ETAT_N1_SUPPRESSION}`, et lui seul.")
        else:
            errs.append(
                f"ASP-CI-38 : la suppression accepte une LISTE d'etats "
                f"{etat!r} au lieu du seul scalaire "
                f"`{ETAT_N1_SUPPRESSION}`. Elargir cette liste — a "
                "`unknown`, `unavailable` ou `non_evaluable` — ne casse "
                "aucun scenario nominal et convertirait un trou "
                "d'information en « aucun entretien » (ASP-INV-45, "
                "ASP-INV-76).")
    if not vus:
        errs.append(
            f"ASP-CI-38 : la suppression ne consulte pas l'etat de "
            f"`{ENTITE_M1_LISTE}` — elle reposerait sur le seul temoin "
            "binaire, c'est-a-dire sur une face de l'autorite au lieu de "
            "deux.")
    return errs


def check_interdits_n1(n1: dict[str, str]) -> list[str]:
    """ASP-CI-39 — ce que le dossier d'automations du domaine ne fait pas.

    Le balayage porte sur le fichier ENTIER, commentaires compris : une
    projection qui NOMME un bouton de remise a zero est deja trop proche de
    la seule primitive irreversible du domaine.

    AMENDEMENT L2 — le dossier porte trois automations de NATURES DIFFERENTES,
    et le controle les distingue au lieu de leur appliquer une regle unique :

      · les deux PROJECTIONS sont des lecteurs purs — aucune commande, aucune
        ecriture de verdict, aucun envoi mobile, et une autorite de lecture
        FERMEE ;
      · la SUPERVISION est un ecrivain du verdict et le seul emetteur du
        canal mobile — mais elle ne commande jamais l'appareil, n'ecrit
        aucune notification persistante et ne connait que quatre entites.

    Un fichier absent de la table est REFUSE. C'est ce qui empeche un
    quatrieme objet d'apparaitre en silence a cote des trois autorises.
    """
    errs: list[str] = []
    if not n1:
        return [f"ASP-CI-39 : dossier N1 introuvable — `{DOSSIER_N1}`."]
    for rel, txt in sorted(n1.items()):
        nu = sans_commentaires_yaml(txt)
        if rel not in AUTORITE_PAR_FICHIER:
            errs.append(f"ASP-CI-39 : `{rel}` n'appartient a aucune des trois "
                        f"natures declarees du dossier "
                        f"{sorted(AUTORITE_PAR_FICHIER)} — un quatrieme objet "
                        "est apparu.")
            continue
        pure = rel in PROJECTIONS_PURES

        # C-6 : perimetre FERME, lu par dossier nomme. Ses slots critiques
        # sont litteraux — sans quoi aucun des interdits ci-dessous ne
        # pourrait etre etabli sur ce fichier.
        errs += refus_slots_templatises("ASP-CI-39", rel, nu)

        # ── Interdits COMMUNS aux trois natures ────────────────────────────
        for m in re.finditer(
                r"^[ \t]*-?[ \t]*(?:action|service|perform_action)[ \t]*:"
                r"[ \t]*[\"']?(vacuum\.[a-z_]+|roborock\.[a-z_]+)", nu, re.M):
            errs.append(f"ASP-CI-39 : `{rel}` appelle `{m.group(1)}` — ce "
                        "fichier ne commande jamais l'appareil : les deux "
                        "seuls chemins de commande du domaine sont le moteur "
                        "et le script de conduite (ASP-INV-31).")
        if PRESS_SERVICE.search(nu):
            errs.append(f"ASP-CI-39 : `{rel}` appelle `button.press` — la "
                        "remise a zero est un geste operateur explicite, "
                        "portee par le SEUL script du lot M2 (ASP-INV-77, "
                        "ASP-INV-81).")
        for m in BOUTON_ENTRETIEN_RE.finditer(txt):
            errs.append(f"ASP-CI-39 : `{rel}` nomme `{m.group(0)}` — ce "
                        "fichier ne presse aucun bouton et n'a pas a le "
                        "connaitre.")
        if REPETITION.search(nu):
            errs.append(f"ASP-CI-39 : `{rel}` porte une repetition — une "
                        "projection se recalcule et une supervision observe : "
                        "elle ne boucle pas.")
        for jeton in TEMPOREL_M1:
            if jeton in nu:
                errs.append(f"ASP-CI-39 : `{rel}` emploie `{jeton}` — le "
                            "domaine constate des faits : un seuil se "
                            "constate, il ne se prevoit pas, et un fait "
                            "physique ne se date pas (14 §2, A-15).")

        # ── Interdits propres aux LECTEURS PURS ───────────────────────────
        if pure:
            try:
                doc = yaml.safe_load(txt)
            except yaml.YAMLError:
                doc = None
            ecrites, _ = _verdicts_du_document(doc)
            if ecrites:
                errs.append(f"ASP-CI-39 : `{rel}` ECRIT le verdict "
                            f"{sorted(ecrites)} — une projection est un "
                            "lecteur pur ; l'ecrivain reste le trio W1/W2/W3 "
                            "(ASP-INV-86).")
            for jeton in MOBILE_N1:
                if jeton in nu:
                    errs.append(f"ASP-CI-39 : `{rel}` emploie `{jeton}` — "
                                "AUCUN envoi mobile depuis une projection : le "
                                "canal mobile appartient a la supervision, et "
                                "a elle seule (ASP-INV-95).")
            for jeton in SESSION_NATIVE_N1:
                if jeton in nu:
                    errs.append(f"ASP-CI-39 : `{rel}` lit `{jeton}` — adopter "
                                "le temoin natif de session reviendrait a "
                                "adopter une mission externe (07 §6.2, "
                                "ASP-INV-47, ASP-INV-87).")
            for jeton in PREDICTION_N1:
                if jeton in nu.lower():
                    errs.append(f"ASP-CI-39 : `{rel}` annonce « {jeton} » — "
                                "aucune date previsionnelle n'est inventee "
                                "(14 §2).")

        # ── Le lot d'entretien garde ses interdits propres ─────────────────
        if rel == RUNTIME_N1:
            for jeton in VERDICT_FIGE_N1:
                if jeton in txt:
                    errs.append(f"ASP-CI-39 : `{rel}` cite `{jeton}` — un "
                                "cycle en cours ne se deduit pas d'un verdict "
                                "de mission : la projection d'entretien "
                                "n'observe aucune mission (ASP-INV-83).")
            for helper in (ID_VERDICT, ID_TRACE):
                if helper in txt:
                    errs.append(f"ASP-CI-39 : `{rel}` cite `{helper}` — la "
                                "projection d'entretien ne lit ni n'ecrit le "
                                "verdict de mission (ASP-INV-83).")
            for jeton in ERREUR_N1:
                if jeton in nu:
                    errs.append(f"ASP-CI-39 : `{rel}` porte `{jeton}` — une "
                                "erreur robot ou dock n'est pas un entretien, "
                                "et hors mission le domaine n'ajoute AUCUNE "
                                "notification (ASP-INV-83, ASP-INV-84).")
            for jeton in INTENTION_N1:
                if jeton in nu:
                    errs.append(f"ASP-CI-39 : `{rel}` lit `{jeton}` — les "
                                "helpers d'intention relevent du lot U0, qui "
                                "n'existe pas.")

        # ── La supervision n'ecrit AUCUNE notification persistante ────────
        if rel not in PROJECTIONS_PURES:
            if "persistent_notification" in nu:
                errs.append(f"ASP-CI-39 : `{rel}` touche a une notification "
                            "persistante — la projection de cycle est un "
                            "objet SEPARE, et un etat metier n'a qu'un "
                            "writer (08_NOTIFICATIONS §7).")

        # ── Services : la liste FERMEE de la nature du fichier ────────────
        admis_svc = SERVICES_PAR_FICHIER[rel]
        for m in re.finditer(
                r"^[ \t]*-?[ \t]*(?:action|service|perform_action)[ \t]*:"
                r"[ \t]*[\"']?([a-z_]+\.[a-z_]+)", nu, re.M):
            svc = m.group(1)
            if svc.startswith("persistent_notification.") and pure:
                continue
            if svc in admis_svc:
                continue
            errs.append(f"ASP-CI-39 : `{rel}` appelle `{svc}` — hors des "
                        f"services admis pour ce fichier {sorted(admis_svc)}.")

        # ── Entites : l'autorite FERMEE de la nature du fichier ───────────
        admis_eid = AUTORITE_PAR_FICHIER[rel] | admis_svc
        for m in re.finditer(r"\b([a-z_]+\.[a-z0-9_]+)\b", nu):
            eid = m.group(1)
            if eid.split(".")[0] not in ("sensor", "binary_sensor",
                                         "input_boolean", "input_text",
                                         "input_select", "input_number",
                                         "vacuum", "button", "switch",
                                         "script", "automation", "notify"):
                continue
            if eid in admis_eid:
                continue
            errs.append(f"ASP-CI-39 : `{rel}` lit `{eid}` — hors de son "
                        f"autorite fermee {sorted(AUTORITE_PAR_FICHIER[rel])}. "
                        "Toute autre entite serait une seconde autorite.")
    return errs


# ═════════════════════════════════════════════════════════════
# MAINTENANCE — lot M2, DECLARATION D'ENTRETIEN (ASP-CI-40 … ASP-CI-42)
#
# M2 livre la SEULE primitive irreversible du domaine. Les trois controles
# ci-dessous ne relisent pas le contrat pour se donner raison : ils confrontent
# le fichier REEL a la sequence normative du chapitre 14 §3, a l'allowlist du
# §4 et aux sept obligations du §6.1.
#
# Les identifiants sont ATTRIBUES PAR L'OPERATEUR au lot M2 (ASP-INV-58 : le
# contrat n'en propose aucun). Figes ici : un renommage silencieux echoue.
# ═════════════════════════════════════════════════════════════

RUNTIME_M2 = "10_scripts/aspirateur/declarer_entretien.yaml"
ID_M2 = "aspirateur_declarer_entretien"
SERVICE_M2 = "script.aspirateur_declarer_entretien"
HELPERS_M2 = "04_input_texts/aspirateur/entretien.yaml"
ID_VERDICT_ENTRETIEN = "input_text.aspirateur_entretien_verdict"

# Le champ FERME, et sa cible litterale. L'ordre suit le contrat 14 §1.
CHAMP_M2 = "poste"
POSTES_M2 = {
    "filtre": ("Filtre",
               "button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air"),
    "brosse_principale": (
        "Brosse principale",
        "button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_principale"),
    "brosse_laterale": (
        "Brosse latérale",
        "button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_laterale"),
    "nettoyage_capteurs": (
        "Nettoyage des capteurs",
        "button.roborock_q7_max_reinitialiser_le_consommable_du_capteur"),
}

# Les deux issues terminales, transcrites du contrat 14 §3 et d'ASP-INV-80.
ISSUES_M2 = ("REMISE_A_ZERO_CONFIRMEE", "REMISE_A_ZERO_NON_CONFIRMEE")

# Ciblages indirects : le contrat les refuse SANS EXCEPTION (ASP-INV-81).
CIBLAGE_INDIRECT = ("device_id", "area_id", "label_id", "floor_id")

# L'ecran d'entretien : trois fichiers Lovelace, et trois seulement.
UI_M2 = (
    "18_lovelace/dashboards/aspirateur/entretien.yaml",
    "18_lovelace/includes/cartes/aspirateur/entretien.yaml",
    "18_lovelace/includes/cartes/aspirateur/entretien_action.yaml",
)
NAV_ASPIRATEUR = "18_lovelace/includes/navigation/aspirateur.yaml"
CLE_DASHBOARD_M2 = "aspirateur-entretien-dashboard"


def _appels_de_service(noeud):
    """Tout appel de service du document, sous ses trois cles et ses deux
    formes de ciblage. Visite RECURSIVE, jamais textuelle."""
    for n in _noeuds_yaml(noeud):
        if not isinstance(n, dict):
            continue
        for cle in ("service", "action", "perform_action"):
            svc = n.get(cle)
            if isinstance(svc, str):
                yield svc, n


def check_declaration_entretien(depot: dict[str, str]) -> list[str]:
    """ASP-CI-40 — le fichier M2 : forme, champ ferme, branches litterales.

    Confronte les sept obligations du chapitre 14 §6.1 au fichier reel :
    fichier hote unique, quatre boutons exacts et eux seuls, interdiction du
    ciblage indirect, interdiction de l'entite templatisee, pression unique.
    """
    errs: list[str] = []
    txt = depot.get(RUNTIME_M2)
    if txt is None:
        return [f"ASP-CI-40 : le fichier du lot M2 est introuvable — "
                f"`{RUNTIME_M2}`. L'allowlist nominative le designe."]
    try:
        doc = yaml.safe_load(txt) or {}
    except yaml.YAMLError as exc:
        return [f"ASP-CI-40 : `{RUNTIME_M2}` est illisible en YAML : {exc}."]
    if not isinstance(doc, dict) or list(doc) != [ID_M2]:
        return [f"ASP-CI-40 : `{RUNTIME_M2}` doit declarer EXACTEMENT le "
                f"script `{ID_M2}` — trouve {sorted(doc) if isinstance(doc, dict) else type(doc)}."]
    corps = doc[ID_M2] or {}

    # ── Obligation 7 : une pression unique, sans boucle ni retry ──────────
    if corps.get("mode") != "single":
        errs.append(f"ASP-CI-40 : `{ID_M2}` doit porter `mode: single` — "
                    f"trouve {corps.get('mode')!r}. Un autre mode rouvrirait "
                    "la voie a une pression pendant qu'une autre est en vol.")
    nu = sans_commentaires_yaml(txt)
    if REPETITION.search(nu):
        errs.append(f"ASP-CI-40 : `{RUNTIME_M2}` porte une repetition — "
                    "aucun `repeat`, aucun retry, aucune seconde pression, "
                    "quelle que soit l'issue (ASP-INV-78).")

    # ── Le champ FERME, et ses quatre valeurs ─────────────────────────────
    champs = corps.get("fields") or {}
    if set(champs) != {CHAMP_M2}:
        errs.append(f"ASP-CI-40 : le script expose {sorted(champs)} — un seul "
                    f"champ est admis, `{CHAMP_M2}` : une declaration porte "
                    "sur UN poste (14 §3, etape 1).")
    vocab = _vocabulaire_ferme(corps)
    if vocab != set(POSTES_M2):
        errs.append(f"ASP-CI-40 : le vocabulaire ferme du champ vaut "
                    f"{sorted(vocab)} ; attendu {sorted(POSTES_M2)}. Un champ "
                    "ferme ne s'ecrit pas sans son enumeration, et le "
                    "perimetre est ferme a quatre postes (ASP-INV-73).")

    # ── Obligation 6 : aucune entite templatisee, aucun service templatise ─
    errs += refus_slots_templatises("ASP-CI-40", RUNTIME_M2, nu)

    # ── Obligations 4 et 5 : les quatre boutons exacts, cibles en clair ───
    presses: list[tuple[str, dict]] = [
        (svc, n) for svc, n in _appels_de_service(doc) if svc == "button.press"]
    if len(presses) != len(POSTES_M2):
        errs.append(f"ASP-CI-40 : le script porte {len(presses)} appel(s) "
                    f"`button.press` ; il en faut exactement {len(POSTES_M2)} "
                    "— une branche litterale par poste, et une seule pression "
                    "par execution (ASP-INV-78).")
    cibles: set[str] = set()
    for _, n in presses:
        cible = n.get("target") or {}
        for indirect in CIBLAGE_INDIRECT:
            if (isinstance(cible, dict) and indirect in cible) or indirect in n:
                errs.append(f"ASP-CI-40 : une pression cible par `{indirect}` "
                            "— le ciblage indirect est refuse sans exception "
                            "(ASP-INV-81).")
        eid = cible.get("entity_id") if isinstance(cible, dict) else None
        if eid is None:
            eid = n.get("entity_id")
        if not isinstance(eid, str):
            errs.append("ASP-CI-40 : une pression ne porte pas d'`entity_id` "
                        "scalaire litteral — une liste ou une absence de cible "
                        "rend la garde textuelle aveugle.")
            continue
        if "{{" in eid or "{%" in eid:
            errs.append(f"ASP-CI-40 : une pression porte un `entity_id` "
                        f"templatise {eid!r} — interdit (14 §6.1, obligation 6).")
            continue
        cibles.add(eid.strip())
    attendues = {b for _, b in POSTES_M2.values()}
    if cibles != attendues:
        errs.append(f"ASP-CI-40 : les boutons presses sont {sorted(cibles)} ; "
                    f"attendus exactement les quatre du perimetre ferme "
                    f"{sorted(attendues)} (ASP-INV-73, ASP-INV-81).")

    # ── ASP-INV-82 : ce lot n'ouvre RIEN d'autre ──────────────────────────
    admis = {"button.press", "input_text.set_value"}
    for svc, _ in _appels_de_service(doc):
        if svc not in admis:
            errs.append(f"ASP-CI-40 : le script appelle `{svc}` — hors des "
                        f"services admis {sorted(admis)}. Ce chapitre "
                        "n'autorise aucune ecriture vers l'appareil au-dela de "
                        "`button.press` sur les quatre boutons (ASP-INV-82).")

    # ── La SECONDE MATERIALISATION du referentiel, confrontee a M1 ────────
    m1 = (ROOT / RUNTIME_M1).read_text(encoding="utf-8", errors="ignore") \
        if (ROOT / RUNTIME_M1).is_file() else ""
    for valeur, (libelle, _) in sorted(POSTES_M2.items()):
        if f'"{libelle}"' not in m1 and f"'{libelle}'" not in m1 \
                and f"nom: {libelle}" not in m1:
            errs.append(f"ASP-CI-40 : le libelle {libelle!r} n'apparait pas "
                        f"dans le perimetre de M1 (`{RUNTIME_M1}`) — la table "
                        "de traduction du lot M2 est une SECONDE copie du "
                        "referentiel : elle doit lui rester conforme (A-13).")
        if libelle not in txt:
            errs.append(f"ASP-CI-40 : le script ne nomme pas le libelle "
                        f"{libelle!r} — sans lui, la mesure du poste "
                        f"{valeur!r} ne peut pas etre retrouvee sur "
                        "l'autorite M1.")
    return errs


def _vocabulaire_ferme(corps: dict) -> set[str]:
    """Les valeurs du champ ferme, telles que le script les ENUMERE.

    Lues sur le bloc `variables:` de la sequence — la source unique — et non
    sur la description du champ, qui n'est qu'un texte d'aide.
    """
    for etape in _aplatir(corps.get("sequence")):
        if not isinstance(etape, dict):
            continue
        var = etape.get("variables") or {}
        valeurs = var.get("postes")
        if isinstance(valeurs, list) and valeurs:
            return {str(v) for v in valeurs}
    return set()


def check_sequence_entretien(depot: dict[str, str]) -> list[str]:
    """ASP-CI-41 — la sequence RENDUE : capture, gardes, transition, issues.

    Le controle porte sur le COMPORTEMENT, pas sur la presence de mots :
    l'ordre des etapes est verifie sur la sequence chargee, et la
    postcondition est confrontee au piege qu'elle doit eviter.
    """
    errs: list[str] = []
    txt = depot.get(RUNTIME_M2)
    if txt is None:
        return [f"ASP-CI-41 : `{RUNTIME_M2}` introuvable."]
    try:
        doc = yaml.safe_load(txt) or {}
    except yaml.YAMLError:
        return [f"ASP-CI-41 : `{RUNTIME_M2}` illisible en YAML."]
    corps = (doc.get(ID_M2) or {}) if isinstance(doc, dict) else {}
    sequence = corps.get("sequence") or []
    if not isinstance(sequence, list):
        return ["ASP-CI-41 : la sequence du script M2 n'est pas une liste."]

    def _rang_pression() -> int:
        for i, etape in enumerate(sequence):
            if any(svc == "button.press"
                   for svc, _ in _appels_de_service(etape)):
                return i
        return -1

    def _rang_capture() -> int:
        for i, etape in enumerate(sequence):
            if isinstance(etape, dict) and "restant_avant" in (
                    etape.get("variables") or {}):
                return i
        return -1

    def _rang_attente() -> int:
        for i, etape in enumerate(sequence):
            if isinstance(etape, dict) and "wait_template" in etape:
                return i
        return -1

    r_capture, r_pression, r_attente = (
        _rang_capture(), _rang_pression(), _rang_attente())

    # ── Q2, garde 1 : la mesure est CAPTUREE avant toute pression ─────────
    if r_capture < 0:
        errs.append("ASP-CI-41 : aucune capture de la mesure avant la "
                    "pression — la variable `restant_avant` est absente. Sans "
                    "valeur de reference, la confirmation ne peut etre qu'un "
                    "etat statique, donc fausse (ASP-INV-79).")
    elif r_pression >= 0 and r_capture > r_pression:
        errs.append("ASP-CI-41 : la mesure est capturee APRES la pression — "
                    "l'ordre est normatif : on n'observe pas avant d'emettre, "
                    "et on ne capture pas apres avoir agi (14 §3).")

    # ── L'ordre normatif : emission, PUIS relecture ───────────────────────
    if r_pression < 0:
        errs.append("ASP-CI-41 : aucune pression dans la sequence.")
    if r_attente < 0:
        errs.append("ASP-CI-41 : aucune relecture bornee — une confirmation "
                    "non bornee n'est pas une confirmation (14 §3, etape 3).")
    elif r_pression >= 0 and r_attente < r_pression:
        errs.append("ASP-CI-41 : la relecture precede l'emission — l'ordre est "
                    "normatif (14 §3).")

    # ── Q2, garde 2 : la remise a zero doit avoir un OBJET ────────────────
    nu = sans_commentaires_yaml(txt)
    if not re.search(r"restant_avant[^\n]*\|\s*float[^\n]*\)\s*>=\s*\(?\s*plafond",
                     nu) and ">= (plafond | float)" not in nu:
        errs.append("ASP-CI-41 : aucune garde ne refuse la pression lorsque le "
                    "restant n'est pas STRICTEMENT INFERIEUR au plafond. Un "
                    "compteur deja au plafond n'a rien a solder, et sa "
                    "confirmation serait vide de sens (Q2, garde 2).")

    # ── Q2, garde 3 : la postcondition est une TRANSITION ─────────────────
    attente = ""
    if r_attente >= 0:
        attente = str(sequence[r_attente].get("wait_template") or "")
    if "restant_avant" not in attente:
        errs.append("ASP-CI-41 : la relecture ne compare pas a la valeur "
                    "capturee avant la pression. Une postcondition ecrite "
                    "comme un ETAT est deja vraie sur un compteur au plafond : "
                    "elle produirait une confirmation FAUSSE (ASP-INV-79).")
    if re.search(r"==\s*\(?\s*plafond", attente) or "== plafond" in attente:
        errs.append("ASP-CI-41 : la relecture teste `== plafond` — c'est "
                    "exactement l'etat statique interdit. La preuve "
                    "contractuelle est une TRANSITION observee (14 §3).")
    if r_attente >= 0:
        fen = str(sequence[r_attente].get("timeout") or "")
        if fen not in ("00:00:30", 30, "30"):
            errs.append(f"ASP-CI-41 : la fenetre de relecture vaut {fen!r} — "
                        f"le contrat fixe {FENETRE_CONFIRMATION_S} s, et le "
                        "domaine ne compte que deux constantes temporelles "
                        "(ASP-INV-69, portee etendue).")
        if sequence[r_attente].get("continue_on_timeout") is not True:
            errs.append("ASP-CI-41 : la relecture n'est pas `continue_on_timeout: "
                        "true` — a l'expiration, la sequence DOIT poursuivre "
                        "vers son issue terminale, jamais s'interrompre en "
                        "silence (ASP-INV-80).")

    # ── L'etat du bouton n'est JAMAIS une preuve (ASP-INV-79) ─────────────
    for jeton in ("last_changed", "last_updated", "states('button.",
                  'states("button.', "is_state('button."):
        if jeton in nu:
            errs.append(f"ASP-CI-41 : le script lit `{jeton}` — l'horodatage "
                        "et l'etat du bouton attestent la PRESSION, jamais son "
                        "EFFET. Les employer serait une confirmation fausse "
                        "(ASP-INV-79).")

    # ── Les DEUX issues terminales, et elles seules ───────────────────────
    ecrites: set[str] = set()
    for svc, n in _appels_de_service(doc):
        if svc != "input_text.set_value":
            continue
        cible = n.get("target") or {}
        eid = cible.get("entity_id") if isinstance(cible, dict) else None
        if eid != ID_VERDICT_ENTRETIEN:
            errs.append(f"ASP-CI-41 : le script ecrit `{eid}` — le seul helper "
                        f"qu'il ecrit est `{ID_VERDICT_ENTRETIEN}`.")
            continue
        val = str((n.get("data") or {}).get("value") or "")
        for issue in ISSUES_M2:
            if issue in val:
                ecrites.add(issue)
    if ecrites != set(ISSUES_M2):
        errs.append(f"ASP-CI-41 : les issues terminales ecrites sont "
                    f"{sorted(ecrites)} ; les DEUX sont exigees "
                    f"{sorted(ISSUES_M2)}. Une pression a eu lieu : elle doit "
                    "produire une issue, confirmee ou non (14 §3, etape 4).")

    # ── Aucune conclusion de panne, aucun acquittement ────────────────────
    for jeton, quoi in (("persistent_notification", "une notification"),
                        ("notify.", "un envoi mobile"),
                        ("panne", "une conclusion de panne"),
                        ("echec materiel", "une conclusion d'echec materiel"),
                        ("échec matériel", "une conclusion d'echec materiel")):
        if jeton in nu.lower():
            errs.append(f"ASP-CI-41 : le script porte {quoi} (`{jeton}`) — "
                        "l'absence de confirmation ne prouve rien, et hors "
                        "mission le domaine n'ajoute aucune notification "
                        "(ASP-INV-80, ASP-INV-84).")
    return errs


class _LoaderHA(yaml.SafeLoader):
    """Chargeur tolerant aux tags Home Assistant.

    Un squelette de dashboard porte `!include`, `!include_dir_merge_named` et
    parfois `!secret` : `yaml.safe_load` les refuse. Les neutraliser laisse la
    STRUCTURE lisible, ce qui suffit — le contenu inclus est lu par ailleurs,
    fichier par fichier. Ne pas les neutraliser rendrait tout squelette
    illisible, donc invisible a la garde.
    """


_LoaderHA.add_multi_constructor(
    "", lambda loader, suffixe, noeud: None)


def charge_ha(txt: str):
    """Charge un YAML Home Assistant, tags neutralises. `None` si illisible."""
    try:
        return yaml.load(txt, Loader=_LoaderHA)
    except yaml.YAMLError:
        return None


def check_ui_entretien(lovelace: dict[str, str],
                       dashboards: dict) -> list[str]:
    """ASP-CI-42 — l'ecran d'entretien : appel exclusif du script backend.

    L'UI SOLLICITE, elle n'execute pas. Ce controle prouve qu'elle ne nomme
    aucune entite native de pression, qu'elle n'appelle que le script du lot
    M2, et que chaque geste porte une confirmation.
    """
    errs: list[str] = []
    for rel in UI_M2:
        if rel not in lovelace:
            errs.append(f"ASP-CI-42 : `{rel}` est introuvable — l'ecran "
                        "d'entretien compte trois fichiers, et trois seulement.")
    presents = {rel: lovelace[rel] for rel in UI_M2 if rel in lovelace}

    for rel, txt in sorted(presents.items()):
        # Aucune entite native de pression, meme citee.
        if pressions_entretien(txt) or BOUTON_ENTRETIEN_RE.search(txt):
            errs.append(f"ASP-CI-42 : `{rel}` nomme un bouton natif de remise "
                        "a zero — l'appel direct depuis Lovelace est interdit "
                        "sans exception, et l'UI n'a pas a le connaitre "
                        "(ASP-INV-81).")
        doc = charge_ha(txt)
        if doc is None and txt.strip():
            errs.append(f"ASP-CI-42 : `{rel}` illisible en YAML.")
            continue
        for svc, _ in _appels_de_service(doc):
            if svc == "button.press":
                errs.append(f"ASP-CI-42 : `{rel}` appelle `button.press` — "
                            "interdit sans exception depuis un fichier "
                            "Lovelace (ASP-INV-81).")

    # ── La carte d'action : quatre gestes, quatre confirmations ───────────
    rel_action = "18_lovelace/includes/cartes/aspirateur/entretien_action.yaml"
    if rel_action in presents:
        doc = charge_ha(presents[rel_action]) or {}
        gestes = [n for n in _noeuds_yaml(doc)
                  if isinstance(n, dict)
                  and isinstance(n.get("variables"), dict)
                  and "service" in n["variables"]]
        if len(gestes) != len(POSTES_M2):
            errs.append(f"ASP-CI-42 : la carte d'action porte {len(gestes)} "
                        f"geste(s) ; il en faut {len(POSTES_M2)}, un par poste "
                        "du perimetre ferme.")
        vus: set[str] = set()
        for g in gestes:
            v = g["variables"]
            if v.get("service") != SERVICE_M2:
                errs.append(f"ASP-CI-42 : un geste appelle {v.get('service')!r} "
                            f"— l'UI n'appelle QUE `{SERVICE_M2}` (contrat 11 "
                            "§1 : elle sollicite, elle n'execute pas).")
            if not str(v.get("confirmation") or "").strip():
                errs.append("ASP-CI-42 : un geste ne porte aucune "
                            "confirmation — la remise a zero est irreversible, "
                            "elle n'est jamais un basculement d'un clic "
                            "(contrat 11 §3.6).")
            valeur = (v.get("data") or {}).get(CHAMP_M2)
            if valeur not in POSTES_M2:
                errs.append(f"ASP-CI-42 : un geste passe `{CHAMP_M2}: "
                            f"{valeur!r}` — hors du vocabulaire ferme "
                            f"{sorted(POSTES_M2)}.")
            else:
                vus.add(valeur)
                libelle = POSTES_M2[valeur][0].split()[0].lower()
                if libelle[:5] not in str(v.get("confirmation")).lower():
                    errs.append(f"ASP-CI-42 : la confirmation du poste "
                                f"{valeur!r} ne le nomme pas — un libelle qui "
                                "ne dit pas sur quoi il porte n'est pas une "
                                "confirmation.")
        if vus and vus != set(POSTES_M2):
            errs.append(f"ASP-CI-42 : les gestes couvrent {sorted(vus)} ; les "
                        f"quatre postes sont exiges {sorted(POSTES_M2)}.")

    # ── La navigation : trois destinations, cles existantes ───────────────
    nav = lovelace.get(NAV_ASPIRATEUR)
    if nav is None:
        errs.append(f"ASP-CI-42 : bandeau de navigation introuvable — "
                    f"`{NAV_ASPIRATEUR}`.")
    else:
        doc = charge_ha(nav) or {}
        chemins = [n["tap_action"]["navigation_path"]
                   for n in _noeuds_yaml(doc)
                   if isinstance(n, dict)
                   and isinstance(n.get("tap_action"), dict)
                   and "navigation_path" in n["tap_action"]]
        if f"/{CLE_DASHBOARD_M2}" not in chemins:
            errs.append(f"ASP-CI-42 : le bandeau ne mene pas a "
                        f"`/{CLE_DASHBOARD_M2}` — l'ecran serait un "
                        "cul-de-sac inatteignable.")
        if len(chemins) != 3:
            errs.append(f"ASP-CI-42 : le bandeau porte {len(chemins)} "
                        "destination(s) ; le domaine en compte trois.")
        if len(set(chemins)) != len(chemins):
            errs.append("ASP-CI-42 : le bandeau porte une destination en "
                        "double.")
    if CLE_DASHBOARD_M2 not in (dashboards or {}):
        errs.append(f"ASP-CI-42 : `{CLE_DASHBOARD_M2}` n'est pas declaree dans "
                    "`18_lovelace/dashboards.yaml` — un `navigation_path` doit "
                    "cibler une cle existante (R-LL-NAV-1 R1).")
    return errs


# ═════════════════════════════════════════════════════════════
# C45 — PROPAGATION DES ARBITRAGES Q1 ET Q2 : ASP-CI-43 … ASP-CI-45
#
# Lot 3 du chantier C45. TROIS controles neufs, tous ACTIFS des ce lot.
#
# AUCUN NE GARDE UN OBJET QUI N'EXISTE PAS. Un controle vert parce que sa
# cible est absente est DORMANT, et il ment : il affiche une garantie que
# rien ne soutient. Le chantier l'exclut nommement, et c'est la raison pour
# laquelle la projection metier — qui n'existe pas encore — n'est inscrite
# nulle part ici. Son nom sera ajoute au lot 4, DANS LE MEME COMMIT que le
# fichier qu'il designe. Le lot 3 livre le MECANISME ; le lot 4 livre le NOM.
#
#   ASP-CI-43  Toute representation runtime d'une classe du verdict — ou
#              d'un SOUS-ENSEMBLE contractuellement nomme de classe — est
#              confrontee A EGALITE EXACTE a l'ensemble canonique ferme
#              correspondant. Le recensement suit l'ENUMERATION, jamais le
#              nom de la cle : chercher `verdict_ouvert` avait manque les
#              engagements de la supervision ET les cles de la table de
#              phrases de la projection, qui enumerent l'une et l'autre une
#              classe sous un autre nom (ASP-INV-98).
#
#   ASP-CI-44  Regime TRANSITOIRE du code historique du dixieme etat.
#              Allowlist FERMEE et NOMINATIVE qui GELE la population
#              existant au HEAD du lot 2 ; refus de toute occurrence
#              technique supplementaire ou deplacee ; refus du code de
#              REMPLACEMENT tant que le mouvement atomique du lot 5 n'a pas
#              eu lieu. Il ne cree AUCUN alias et n'autorise AUCUNE
#              coexistence : il n'ouvre pas un second nom, il ferme la
#              population du premier (08 §1.3). Ce controle a une MORT
#              PROGRAMMEE — le lot 5 supprime l'allowlist et lui substitue,
#              dans le meme mouvement, la regle permanente de ZERO
#              occurrence.
#
#   ASP-CI-45  Autorite et offre des gestes de conduite Arsenal
#              (ASP-INV-97). La moitie livree ici est celle qui est
#              REELLEMENT verifiable aujourd'hui : la garde d'autorite du
#              script de conduite, posee AVANT le dispatch des gestes ;
#              l'absence de toute restriction physique sur l'arret, des
#              deux cotes ; et les TROIS exclusions de sens physique du
#              retour a la base, des deux cotes egalement. L'AUTORITE des
#              quatre sites Lovelace — qui lisent encore l'attribut derive
#              du temoin natif — bascule au lot 6 et etendra ce meme
#              controle, SANS nouveau numero.
#
# CE QUE CES TROIS CONTROLES NE PROUVENT PAS. Ni que la projection metier
# derive de la seule classe O, ni qu'elle rend son indisponibilite comme un
# troisieme regime : ces deux proprietes portent sur un objet livre au lot
# 4, et les affirmer ici serait exactement le faux vert que ce module
# refuse partout ailleurs.
# ═════════════════════════════════════════════════════════════

# ── ASP-CI-43 : perimetre, ensembles et recensement fige ─────────────────

# Le perimetre est NOMME, jamais devine — meme discipline que
# `RUNTIME_FICHIERS` et `RUNTIME_L2_FICHIERS`.
#
# CE QUE CE PERIMETRE NE COUVRE PAS, dit ici plutot que passe sous silence.
# `ASP-CI-11` refuse un fichier hors allowlist SEULEMENT s'il MENTIONNE le
# helper de verdict. Une representation logee ailleurs et qui n'en cite pas
# le helper — une table de classe recopiee dans un fichier qui ne lit jamais
# le verdict lui-meme — echappe donc aux deux controles a la fois. Le
# cardinal fige ci-dessous ne la rattrape pas non plus : il compte ce que ce
# perimetre contient, pas ce qui vit dehors. Elargir le perimetre est un
# acte de lot, pas une correction de ce commentaire.
PERIMETRE_REPRESENTATIONS = (RUNTIME_FICHIERS + RUNTIME_L2_FICHIERS
                             + (RUNTIME_U0_AUTO,) + FICHIERS_U0)

# Les TROIS ensembles canoniques fermes auxquels une representation peut se
# confronter : les deux CLASSES du 15 §2, et le seul SOUS-ENSEMBLE que le
# contrat nomme — les quatre engagements de W2 (15 §4, ASP-INV-92).
ENSEMBLES_CANONIQUES = (
    ("la classe O, sous-classe O-R comprise", CLASSE_O),
    ("la classe T", CLASSE_T),
    ("les engagements de W2", frozenset(ENGAGEMENTS_W2)),
)

# A partir de DEUX valeurs du vocabulaire, un noeud ENUMERE. Une valeur
# isolee est un verdict ECRIT — l'objet d'ASP-CI-18 —, pas une
# representation de classe.
SEUIL_REPRESENTATION = 2

# Recensement FIGE, fichier par fichier. Le cardinal total — SEPT — est
# celui que le chantier C45 §3.2 etablit apres rectification. Le figer ici
# rend rouge la DISPARITION d'une representation autant que son APPARITION
# ailleurs : une huitieme representation doit etre QUALIFIEE avant d'etre
# admise, car une liste qui diverge peut etre la BONNE (condition d'arret
# A4 du chantier). Sans ce cardinal, le controle se contenterait de garder
# ce qu'il trouve, et une representation deplacee hors perimetre le
# laisserait vert.
REPRESENTATIONS_ATTENDUES = {
    RUNTIME_MOTEUR: 1,           # `verdict_ouvert` — la garde du moteur
    RUNTIME_L2_CONDUITE: 1,      # `verdict_ouvert` — la porte d'entree W2
    RUNTIME_L2_SUPERVISION: 2,   # `verdict_ouvert` et `engagements`
    RUNTIME_L2_PROJECTION: 3,    # `verdict_ouvert`, `verdict_terminal`,
                                 # et les cles de la table de phrases
}
NB_REPRESENTATIONS = sum(REPRESENTATIONS_ATTENDUES.values())


def _enumerations_de_classe(noeud, chemin="$"):
    """Tout noeud qui ENUMERE des valeurs de verdict, quel que soit son nom.

    Deux formes portent une enumeration en YAML, et deux seulement : une
    LISTE de scalaires, et les CLES d'un mapping. Les deux sont rendues.

    Le nom sous lequel le noeud est heberge n'entre A AUCUN MOMENT dans la
    decision. C'est la lettre d'ASP-INV-98 — « la regle suit l'enumeration,
    jamais la cle qui l'heberge » — et c'est ce qui distingue ce controle de
    la garde par cle litterale d'ASP-CI-37 : celle-ci reste en place et n'est
    pas affaiblie, mais elle ne voit que les deux cles qu'elle nomme.
    """
    if isinstance(noeud, dict):
        cles = frozenset(k for k in noeud if isinstance(k, str))
        if len(cles & VOCABULAIRE_VERDICT) >= SEUIL_REPRESENTATION:
            yield chemin, "clés de mapping", cles
        for cle, val in noeud.items():
            yield from _enumerations_de_classe(val, f"{chemin}.{cle}")
    elif isinstance(noeud, list):
        scalaires = frozenset(v for v in noeud if isinstance(v, str))
        if len(scalaires & VOCABULAIRE_VERDICT) >= SEUIL_REPRESENTATION:
            yield chemin, "liste", scalaires
        for i, val in enumerate(noeud):
            yield from _enumerations_de_classe(val, f"{chemin}[{i}]")


def check_representations_de_classe(textes_runtime, yaml_depot) -> list[str]:
    """ASP-CI-43 — egalite exacte de toute representation de classe.

    Ces ensembles sont FERMES, et ils vivent en deux endroits : le
    vocabulaire canonique de ce module, et chaque representation runtime qui
    l'embarque. Deux copies qui ne sont pas confrontees DIVERGENT. Une classe
    amputee d'une valeur laisse alors passer exactement les cas qu'elle
    devait retenir — et elle le fait EN SILENCE, ce qu'ASP-INV-49 proscrit.

    La comparaison porte sur le contenu ENTIER du noeud, pas sur sa seule
    intersection avec le vocabulaire : sans cela, une valeur etrangere glissee
    a cote des neuf bonnes ne changerait rien au verdict du controle.
    """
    errs: list[str] = []
    releve: dict[str, int] = {}
    for rel in PERIMETRE_REPRESENTATIONS:
        source = textes_runtime.get(rel)
        if source is None:
            source = yaml_depot.get(rel)
        if source is None:
            errs.append(f"ASP-CI-43 : `{rel}` appartient au périmètre du "
                        "recensement et n'a pas pu être lu — une "
                        "représentation non lue est une représentation non "
                        "gardée.")
            continue
        try:
            doc = yaml.safe_load(source)
        except yaml.YAMLError as exc:
            errs.append(f"ASP-CI-43 : `{rel}` est illisible ({exc}).")
            continue
        for chemin, forme, ens in _enumerations_de_classe(doc):
            releve[rel] = releve.get(rel, 0) + 1
            if any(ens == canon for _, canon in ENSEMBLES_CANONIQUES):
                continue
            # Le plus proche se mesure a la DIFFERENCE SYMETRIQUE, jamais
            # a la seule intersection : un sous-ensemble ampute a la meme
            # intersection avec la classe qui le contient qu'avec l'ensemble
            # dont il derive, et le diagnostic designerait alors la classe
            # entiere — envoyant corriger ce qui n'a pas bouge.
            nom, canon = min(ENSEMBLES_CANONIQUES,
                             key=lambda t: len(ens ^ t[1]))
            errs.append(
                f"ASP-CI-43 : `{rel}` porte en `{chemin}` ({forme}) une "
                f"énumération de {len(ens)} valeur(s) qui n'égale AUCUN "
                f"ensemble canonique. La plus proche est {nom} — manque "
                f"{sorted(canon - ens) or '—'}, en trop "
                f"{sorted(ens - canon) or '—'}. Une classe recopiée à la main "
                "dérive du vocabulaire, et laisse alors passer exactement les "
                "cas qu'elle devait retenir (ASP-INV-98, ASP-INV-49).")
    if releve != REPRESENTATIONS_ATTENDUES:
        manquantes = {k: v for k, v in REPRESENTATIONS_ATTENDUES.items()
                      if releve.get(k, 0) != v}
        surnumeraires = {k: v for k, v in releve.items()
                         if k not in REPRESENTATIONS_ATTENDUES}
        errs.append(
            f"ASP-CI-43 : le recensement rend {sum(releve.values())} "
            f"représentation(s) pour {NB_REPRESENTATIONS} attendues — écart "
            f"sur {sorted(manquantes) or '—'}, hors périmètre recensé "
            f"{sorted(surnumeraires) or '—'}. Une représentation qui "
            "disparaît cesse d'être confrontée ; une qui apparaît doit être "
            "QUALIFIÉE avant d'être admise — une liste qui diverge peut être "
            "la BONNE (C45, condition d'arrêt A4).")
    return errs


# ── ASP-CI-44 : regime transitoire du code historique ────────────────────

# Le code de REMPLACEMENT du dixieme etat, attribue par l'operateur et
# INTERDIT comme code technique tant que le mouvement atomique du lot 5 n'a
# pas eu lieu. Il est fige ici en tant que chaine A REFUSER, et ce module ne
# l'emploie nulle part ailleurs : declarer le nom qu'on refuse n'ouvre
# aucune coexistence des deux noms (08 §1.3, regle 3).
CODE_SESSION_LOT5 = "session_robot_active"

# Le SEUL arbre Lovelace qui restitue le dixieme etat. Nomme, jamais
# recherche : le perimetre vient de cette constante, pas d'un balayage.
FICHIER_UI_MISSION = ("18_lovelace/includes/cartes/aspirateur/"
                      "panneau_operationnel.yaml")

# ALLOWLIST TRANSITOIRE — FERMEE et NOMINATIVE.
#
# Elle enumere, fichier par fichier, les EMPLOIS TECHNIQUES du code
# historique qui existent au HEAD du lot 2, ET EUX SEULS. Elle n'autorise
# pas un nom : elle GELE une population. Tout emploi supplementaire, tout
# emploi deplace vers un autre fichier, est un ecart.
#
# Le cardinal vaut DEUX FOIS, et les deux lectures sont necessaires.
#
#   · en FORME — l'analyse STRUCTUREE compte les cles d'attribut chez le
#     producteur et les slots de restitution dans l'arbre Lovelace. Elle
#     seule fait autorite sur CE QUE SONT ces emplois ;
#   · en NOMBRE — le meme cardinal borne le total des occurrences du code
#     dans le fichier, COMMENTAIRES NEUTRALISES. C'est ce qui rattrape un
#     emploi technique qui ne serait ni une cle ni un slot : un
#     `state_attr(..., '<code>')` en Jinja, une carte markdown qui lit
#     l'attribut. La forme ne le verrait pas ; le total, si.
#
# Les commentaires sont neutralises AVANT ce comptage, et c'est tout ce qui
# separe cette regle d'un recomptage brut : une MENTION ne repand rien, un
# EMPLOI si. Un recomptage brut refuserait une ligne de prose ecrite dans le
# fichier meme qui porte le code — y compris la note de migration que le lot
# 5 aura toutes les raisons d'y laisser.
#
# Elle est SUPPRIMEE au lot 5, dans le commit meme de la migration, et
# remplacee par la recherche d'absence a zero occurrence.
ALLOWLIST_ANCIEN_CODE = {
    RUNTIME_ETAT: 1,          # le PRODUCTEUR — une cle d'attribut, une seule
    FICHIER_UI_MISSION: 4,    # les QUATRE sites de restitution (C45 §3.4)
}

# Le module lui-meme est le TROISIEME porteur, et l'item 5.2 du chantier
# exige qu'il bascule avec les autres : deux constantes, deux commentaires
# et les deux messages d'ASP-CI-23. Un renommage qui ne toucherait que les
# constantes laisserait ce module DECRIRE un nom qui n'existe plus — et
# l'en-tete vaut contrat local.
OCCURRENCES_ANCIEN_CODE_MODULE = 6

# Le chapitre 08 est le QUATRIEME porteur, et le SEUL chapitre ou le token
# technique historique reste admis : le code du tableau §1, et les deux
# occurrences de la clause d'etat transitoire §1.3. Cette clause est
# LEGITIME — elle ecrit l'ecart au lieu de le subir — et sa suppression est
# une obligation de preuve du lot 5, pas du lot 3.
#
# PARTOUT AILLEURS dans le contrat du domaine, le token est REFUSE : le lot
# 2 a aligne le libelle des chapitres 11 et 12 sur « session robot active »,
# et rien ne doit y ramener le code ambigu par la porte de derriere.
#
# La detection porte sur le TOKEN technique — celui qui s'ecrit avec des
# soulignes —, jamais sur la formulation metier, qui s'ecrit avec des
# espaces. Les deux ne se confondent pas : « session robot active » et
# « mission Arsenal ouverte » restent libres partout, et c'est bien ce que
# les chapitres doivent employer.
OCCURRENCES_ANCIEN_CODE_CONTRAT = 3
FICHIER_CONTRAT_TRANSITOIRE = FICHIER_ETATS
ANCRE_CLAUSE_TRANSITOIRE = "Migration atomique du nom du dixième état"

# Les cles de slot Lovelace qui DESIGNENT un attribut d'entite. La detection
# est structuree parce que c'est l'EMPLOI TECHNIQUE qui est gele, non le mot :
# le fichier livre ne cite le code que dans ces quatre slots, et rien
# n'empeche qu'un commentaire l'y mentionne demain sans rien repandre. Un
# recomptage textuel confondrait les deux et refuserait la ligne de prose.
CLES_ATTRIBUT_UI = ("attribute", "attribut")

# La CIBLE d'un lien Markdown est un CHEMIN, jamais du texte contractuel.
# Or le fichier d'arbitrage `Q1` porte dans son NOM le code de remplacement,
# et les chapitres ont toutes les raisons de le citer : sans neutralisation,
# un renvoi legitime vers l'arbitrage qui FONDE la regle la declencherait.
# Seule la cible est neutralisee — le libelle du lien et le reste de la
# ligne restent lus, de sorte qu'un emploi technique glisse dans le texte
# d'un lien reste refuse.
CIBLE_LIEN_MD = re.compile(r"\]\([^)]*\)")


def sans_commentaires_ligne(texte: str) -> str:
    """Neutralise les commentaires YAML, PLEINE LIGNE ET FIN DE LIGNE.

    `sans_commentaires_yaml` ne coupe que les lignes ENTIEREMENT commentees.
    Une note posee a droite d'une valeur — `attribute: <code>  # a migrer` —
    lui echappe, et un comptage textuel la prendrait pour un emploi.

    Deux precautions, et elles suffisent aux formes que ces fichiers portent.

      · un `#` n'ouvre un commentaire QUE s'il est en debut de ligne ou
        precede d'une espace : `#` colle a un mot appartient au mot, comme
        dans une couleur `#ffffff` ou une ancre ;
      · un `#` situe DANS une chaine quotee n'ouvre rien du tout. L'etat de
        citation est suivi caractere par caractere — un `split("#")` naif
        amputerait ici une valeur legitime.

    Ce n'est pas un parseur YAML, et cela ne pretend pas l'etre : les blocs
    litteraux `|` et `>` ne sont pas suivis, de sorte qu'un `#` precede d'une
    espace y serait coupe a tort. Aucun des deux fichiers geles n'en porte,
    et la coupure irait dans le sens du REFUS de compter — elle ne peut pas
    laisser passer un emploi, seulement en manquer un dans une forme absente
    du depot. La limite est ecrite plutot que passee sous silence.
    """
    out = []
    for ligne in sans_commentaires_yaml(texte).splitlines():
        quote = None
        coupe = None
        for i, ch in enumerate(ligne):
            if quote:
                if ch == quote:
                    quote = None
            elif ch in "\"'":
                quote = ch
            elif ch == "#" and (i == 0 or ligne[i - 1] in " \t"):
                coupe = i
                break
        out.append(ligne if coupe is None else ligne[:coupe])
    return "\n".join(out)


def _valeurs_de_slot(noeud, cles):
    """Les valeurs des slots dont la CLE appartient a `cles`."""
    if isinstance(noeud, dict):
        for cle, val in noeud.items():
            if cle in cles and isinstance(val, str):
                yield val
            yield from _valeurs_de_slot(val, cles)
    elif isinstance(noeud, list):
        for val in noeud:
            yield from _valeurs_de_slot(val, cles)


def _cles_d_attributs(doc):
    """Les cles declarees sous un bloc `attributes:` de capteur template."""
    for m in _mappings(doc):
        attrs = m.get("attributes")
        if isinstance(attrs, dict):
            for cle in attrs:
                if isinstance(cle, str):
                    yield cle


def check_ancien_code_transitoire(textes_runtime, yaml_depot,
                                  textes: dict) -> list[str]:
    """ASP-CI-44 — la population du code historique est GELEE, pas tolérée.

    La decision H-3 du chantier AUTORISE l'ancien code jusqu'au lot 5 : le
    controle ne peut donc pas exiger zero occurrence des maintenant. Il doit
    neanmoins etre IMMEDIATEMENT ACTIF ET UTILE, sans pretendre que la
    migration a deja eu lieu. C'est ce que fait l'allowlist : elle ne tolere
    pas un nom, elle interdit qu'il se REPANDE.

    CE QUE LE CONTROLE LIT, EXACTEMENT.

    Sur les DEUX FICHIERS GELES — le producteur et l'arbre Lovelace —, deux
    lectures se completent, et aucune ne remplace l'autre :

      · en FORME, l'analyse STRUCTUREE compte les cles declarees sous un bloc
        `attributes:` et les valeurs des slots d'attribut. Elle seule fait
        autorite sur CE QUE SONT ces emplois ;
      · en NOMBRE, le meme cardinal borne le total des occurrences du code
        dans le fichier, une fois NEUTRALISES les commentaires YAML — pleine
        ligne comme fin de ligne. C'est ce qui rattrape un emploi qui n'est ni
        cle ni slot : un `state_attr(..., '<code>')` en Jinja, une carte
        markdown qui restitue l'attribut. La forme ne le verrait pas.

    La neutralisation des commentaires est tout ce qui separe cette seconde
    lecture d'un recomptage brut : une MENTION ne repand rien, un EMPLOI si.

    SUR LES CONTRATS, la recherche porte sur le TOKEN technique — celui qui
    s'ecrit avec des soulignes —, jamais sur la formulation metier, qui
    s'ecrit avec des espaces et reste libre partout. Les DESTINATIONS de
    liens Markdown y sont neutralisees d'abord : un renvoi vers l'arbitrage
    `Q1` cite son NOM DE FICHIER, pas un code, et il serait absurde qu'un
    chapitre ne puisse plus renvoyer a la note qui fonde la regle. Le LIBELLE
    du lien, lui, reste lu. Le futur code technique y est refuse pendant tout
    le regime transitoire.

    CE QUI N'EST PAS BALAYE, et ce n'est pas un oubli. Les mentions
    documentaires — arbitrages, audits, chantier, registres, index — ne sont
    PAS des emplois techniques : elles nomment une decision, elles ne creent
    ni cle, ni slot, ni lecture. Le perimetre se borne donc au YAML de
    configuration, aux chapitres du contrat et a ce module. Un balayage plus
    large serait rouge des sa livraison, sur l'arbitrage meme qui le fonde.
    """
    errs: list[str] = []
    ancien = ETAT_ORTHOGONAL

    # ── (a) le PRODUCTEUR : une CLE d'attribut, et une seule ──────────────
    try:
        doc_etat = yaml.safe_load(textes_runtime.get(RUNTIME_ETAT) or "")
    except yaml.YAMLError as exc:
        doc_etat = None
        errs.append(f"ASP-CI-44 : `{RUNTIME_ETAT}` est illisible ({exc}).")
    if doc_etat is not None:
        attributs = list(_cles_d_attributs(doc_etat))
        if attributs.count(ancien) != 1:
            errs.append(
                f"ASP-CI-44 : le producteur `{RUNTIME_ETAT}` déclare "
                f"{attributs.count(ancien)} attribut(s) `{ancien}` — attendu "
                "exactement un. Le dixième état est ORTHOGONAL et se rend "
                "séparément : ni fondu dans la valeur d'état, ni dupliqué "
                "(ASP-INV-68).")
        if CODE_SESSION_LOT5 in attributs:
            errs.append(
                f"ASP-CI-44 : le producteur déclare déjà l'attribut "
                f"`{CODE_SESSION_LOT5}` — la substitution du code technique "
                "appartient au mouvement ATOMIQUE du lot 5, et aucune "
                "coexistence des deux noms n'est admise, fût-elle "
                "transitoire (08 §1.3, règle 3).")

    # ── (b) les QUATRE sites Lovelace, par leurs SLOTS ────────────────────
    src_ui = yaml_depot.get(FICHIER_UI_MISSION)
    if src_ui is None:
        errs.append(f"ASP-CI-44 : `{FICHIER_UI_MISSION}` est introuvable — "
                    "les quatre sites de restitution ne peuvent pas être "
                    "gelés s'ils ne sont pas lus.")
    else:
        try:
            doc_ui = yaml.safe_load(src_ui)
        except yaml.YAMLError as exc:
            doc_ui = None
            errs.append(f"ASP-CI-44 : `{FICHIER_UI_MISSION}` est illisible "
                        f"({exc}).")
        if doc_ui is not None:
            slots = list(_valeurs_de_slot(doc_ui, CLES_ATTRIBUT_UI))
            attendu = ALLOWLIST_ANCIEN_CODE[FICHIER_UI_MISSION]
            if slots.count(ancien) != attendu:
                errs.append(
                    f"ASP-CI-44 : `{FICHIER_UI_MISSION}` porte "
                    f"{slots.count(ancien)} slot(s) d'attribut `{ancien}` — "
                    f"l'allowlist transitoire en gèle exactement {attendu}. "
                    "Une restitution supplémentaire répandrait le code "
                    "ambigu que le lot 5 doit faire disparaître.")
            if CODE_SESSION_LOT5 in slots:
                errs.append(
                    f"ASP-CI-44 : `{FICHIER_UI_MISSION}` lit déjà l'attribut "
                    f"`{CODE_SESSION_LOT5}` — l'interface bascule au lot 6, "
                    "sur un code substitué au lot 5. L'anticiper produirait "
                    "une lecture d'un attribut qui n'existe pas encore.")

    # ── (c) le TOTAL des deux fichiers gelés, commentaires neutralisés ────
    #
    # L'analyse structurée ci-dessus dit ce que SONT les emplois ; elle ne
    # dit pas s'il en existe d'AUTRES. Un `state_attr(…, '<code>')` en Jinja,
    # une carte markdown qui lit l'attribut, ne sont ni une clé ni un slot :
    # la forme ne les voit pas. Le TOTAL, lui, les voit.
    #
    # Les commentaires sont neutralisés avant ce comptage — c'est tout ce qui
    # sépare cette règle d'un recomptage brut. Une MENTION ne répand rien ;
    # un EMPLOI, si.
    for rel, attendu in sorted(ALLOWLIST_ANCIEN_CODE.items()):
        txt = yaml_depot.get(rel)
        if txt is None:
            continue
        vus = sans_commentaires_ligne(txt).count(ancien)
        if vus != attendu:
            errs.append(
                f"ASP-CI-44 : `{rel}` porte {vus} occurrence(s) techniques de "
                f"`{ancien}` — l'allowlist transitoire en gèle exactement "
                f"{attendu}, commentaires neutralisés. Un emploi qui n'est ni "
                "une clé ni un slot — une lecture Jinja de l'attribut, une "
                "carte qui le restitue — répand le code que le lot 5 doit "
                "faire disparaître, et l'analyse de forme ne le verrait pas.")

    # ── (d) le reste du dépôt gouverné : AUCUNE autre occurrence ──────────
    for rel, txt in sorted(yaml_depot.items()):
        if rel not in ALLOWLIST_ANCIEN_CODE and ancien in txt:
            errs.append(
                f"ASP-CI-44 : `{rel}` emploie `{ancien}` — l'allowlist "
                "transitoire est FERMÉE et NOMINATIVE : elle gèle la "
                "population qui existe au HEAD du lot 2, elle n'ouvre aucun "
                "droit nouveau (C45 item 3.7, régime ①).")
        if CODE_SESSION_LOT5 in txt:
            errs.append(
                f"ASP-CI-44 : `{rel}` emploie déjà `{CODE_SESSION_LOT5}` — ce "
                "code n'entre au dépôt qu'au lot 5, en un seul mouvement avec "
                "le producteur, les contrats, le checker et l'interface "
                "(ASP-INV-52 par analogie : le renommage est un acte "
                "contractuel).")

    # ── (e) le MODULE lui-même — troisième porteur, item 5.2 du chantier ──
    try:
        source = Path(__file__).read_text(encoding="utf-8")
    except OSError as exc:                                # pragma: no cover
        source = ""
        errs.append(f"ASP-CI-44 : le module est illisible ({exc}).")
    if source:
        vus = source.count(ancien)
        if vus != OCCURRENCES_ANCIEN_CODE_MODULE:
            errs.append(
                f"ASP-CI-44 : ce module porte {vus} occurrence(s) de "
                f"`{ancien}` — l'allowlist transitoire en gèle "
                f"{OCCURRENCES_ANCIEN_CODE_MODULE} : deux constantes, deux "
                "commentaires et les deux messages d'ASP-CI-23. Un contrôle "
                "qui répandrait lui-même le code qu'il gèle serait sans "
                "autorité.")
    # ── (f) les CONTRATS du domaine — le 08 gèle, les autres refusent ────
    #
    # Le chapitre 08 est le seul où le token technique historique reste
    # admis, et à un cardinal exact. Partout ailleurs il est REFUSÉ : le lot
    # 2 a aligné le libellé des chapitres 11 et 12 sur « session robot
    # active », et rien ne doit y ramener le code ambigu.
    #
    # La détection porte sur le TOKEN — celui qui s'écrit avec des soulignés
    # —, jamais sur la formulation métier, qui s'écrit avec des espaces. Un
    # chapitre qui parle de « session robot active » ou de « mission Arsenal
    # ouverte » reste libre : c'est précisément ce qu'il doit employer.
    t08 = CIBLE_LIEN_MD.sub(
        "]()", textes.get(FICHIER_CONTRAT_TRANSITOIRE, ""))
    if not t08:
        errs.append(f"ASP-CI-44 : `{FICHIER_CONTRAT_TRANSITOIRE}` "
                    "introuvable — le code contractuel ne peut pas être gelé "
                    "s'il n'est pas lu.")
    else:
        vus = t08.count(ancien)
        if vus != OCCURRENCES_ANCIEN_CODE_CONTRAT:
            errs.append(
                f"ASP-CI-44 : le chapitre 08 porte {vus} occurrence(s) de "
                f"`{ancien}` — attendu {OCCURRENCES_ANCIEN_CODE_CONTRAT} : le "
                "code du tableau §1, et les deux de la clause d'état "
                "transitoire §1.3.")
        if ANCRE_CLAUSE_TRANSITOIRE not in t08:
            errs.append(
                f"ASP-CI-44 : la clause d'état transitoire « "
                f"{ANCRE_CLAUSE_TRANSITOIRE} » a disparu du chapitre 08. "
                "L'écart entre le libellé et le code est ÉCRIT, non subi : "
                "l'effacer sans avoir migré le rendrait silencieux. Sa "
                "suppression appartient au lot 5, avec la migration.")
    for rel, brut in sorted(textes.items()):
        txt = CIBLE_LIEN_MD.sub("]()", brut)
        if rel != FICHIER_CONTRAT_TRANSITOIRE and ancien in txt:
            errs.append(
                f"ASP-CI-44 : le chapitre `{rel}` emploie le token technique "
                f"`{ancien}` — hors du chapitre 08, le code historique n'a "
                "PLUS de place au contrat : le lot 2 y a aligné le libellé "
                "sur la notion, et la formulation métier — avec espaces — "
                "reste libre partout. Seul le 08 porte encore le code, et "
                "seulement le temps de sa clause transitoire §1.3.")
        if CODE_SESSION_LOT5 in txt:
            errs.append(
                f"ASP-CI-44 : le chapitre `{rel}` écrit déjà le token "
                f"`{CODE_SESSION_LOT5}` comme code technique — le lot 2 "
                "aligne le LIBELLÉ, le lot 5 substitue le CODE, et jamais "
                "l'inverse. La formulation métier « session robot active » "
                "est, elle, admise partout.")
    return errs


# ── ASP-CI-45 : autorite et offre des gestes de conduite ─────────────────

# Le geste qui, seul, ne connait AUCUNE restriction de sens physique.
# `ASP-INV-97` en fait une consequence directe d'`ASP-INV-43` : l'arret
# n'est jamais plus contraint que le lancement. Une garde d'abstention
# posee sur lui rendrait la mission Arsenal inarretable au moment meme ou
# l'operateur en a besoin.
GESTE_SANS_RESTRICTION = "arret"

# La garde d'autorite s'arrete sur la NEGATION, et cette polarite est la
# regle elle-meme : `not in verdict_ouvert` refuse le geste HORS classe O,
# la forme affirmative le refuserait PENDANT la classe O — soit exactement
# l'inverse. Les deux formes citent le helper et la table, et une garde qui
# ne verifierait que leur PRESENCE tiendrait l'inversion pour conforme.
POLARITE_GARDE_AUTORITE = "not in verdict_ouvert"

# Les TROIS exclusions de sens physique du retour a la base, cote backend :
# deja en retour, en cours d'amarrage, ou en charge. Elles sont de SENS
# PHYSIQUE (ASP-INV-48), non d'autorite — le geste n'aurait rien a ordonner.
EXCLUSIONS_PHYSIQUES_RETOUR = ("returning_home", "docking", "charging")

# Les MEMES trois exclusions, cote interface, dans le vocabulaire canonique
# du chapitre 08. Le lot 6 changera l'AUTORITE de ce site — l'attribut
# derive du temoin natif cede la place a la projection metier — mais il
# CONSERVE ces trois exclusions telles quelles (C45 item 6.5).
EXCLUSIONS_UI_RETOUR = frozenset({"retour_base", "amarrage", "charge"})


def _gestes_du_noeud(noeud):
    """Les gestes de conduite qu'un sous-arbre Lovelace demande au backend."""
    if isinstance(noeud, dict):
        for cle, val in noeud.items():
            if cle == "geste" and isinstance(val, str):
                yield val
            else:
                yield from _gestes_du_noeud(val)
    elif isinstance(noeud, list):
        for val in noeud:
            yield from _gestes_du_noeud(val)


def _branches_de_geste(top):
    """La branche de premier niveau qui traite chaque geste, par son rang."""
    for i, st in enumerate(top):
        if not (isinstance(st, dict) and isinstance(st.get("choose"), list)):
            continue
        trouve = {}
        for opt in st["choose"]:
            if not isinstance(opt, dict):
                continue
            cond = _conditions_option(opt)
            for geste in GESTES_L2:
                if f"geste == '{geste}'" in cond:
                    trouve[geste] = opt.get("sequence") or []
        if trouve:
            return i, trouve
    return None, {}


def check_offre_gestes(textes_runtime, lovelace) -> list[str]:
    """ASP-CI-45 — l'offre d'un geste se règle sur le verdict, et sur lui seul.

    Deux moities, et le chantier ne permet d'en rendre qu'une active
    aujourd'hui.

    ACTIVE ICI — l'autorite du BACKEND et les gardes de sens physique. La
    garde de classe O precede le dispatch des gestes ; l'arret ne porte
    aucune abstention ; le retour a la base porte ses trois exclusions, et
    exactement les siennes, des deux cotes.

    LOT 6 — l'AUTORITE des quatre sites Lovelace. Ils lisent aujourd'hui
    l'attribut derive du temoin natif, et non la projection metier, qui
    n'existe pas encore. L'affirmer maintenant serait faux ; le taire
    laisserait croire que ce controle couvre plus qu'il ne couvre.

    Ce qui EST deja opposable cote interface, et le restera apres le lot 6 :
    l'arret n'y porte aucune exclusion d'etat, et le retour a la base y porte
    les trois siennes. Ces deux proprietes survivent au changement
    d'autorite, et c'est ce qui les rend gardables des maintenant.
    """
    errs: list[str] = []
    try:
        doc = yaml.safe_load(textes_runtime.get(RUNTIME_L2_CONDUITE) or "")
    except yaml.YAMLError as exc:
        return [f"ASP-CI-45 : `{RUNTIME_L2_CONDUITE}` est illisible ({exc})."]
    corps = (doc or {}).get(ID_CONDUITE) or {}
    top = corps.get("sequence") or []

    # ── (a) l'AUTORITÉ précède le dispatch — la preuve est ORDINALE ───────
    rang_garde = None
    for i, st in enumerate(top):
        if not (isinstance(st, dict) and isinstance(st.get("choose"), list)):
            continue
        for opt in st["choose"]:
            if not isinstance(opt, dict):
                continue
            cond = _conditions_option(opt)
            if ID_VERDICT not in cond or "verdict_ouvert" not in cond:
                continue
            # La branche est reconnue sur la PRESENCE du helper et de la
            # table ; sa POLARITE est controlee ensuite, et separement. Les
            # confondre laisserait l'inversion se presenter comme une
            # absence de garde, et le diagnostic designerait le mauvais mal.
            if POLARITE_GARDE_AUTORITE not in cond:
                errs.append(
                    "ASP-CI-45 : la garde d'autorité ne porte pas "
                    f"`{POLARITE_GARDE_AUTORITE}` — sa polarité est "
                    "INVERSÉE. Écrite à l'affirmative, elle arrête le script "
                    "PENDANT la classe `O` et le laisse passer en dehors : "
                    "le geste serait refusé sur la mission qu'Arsenal tient, "
                    "et conduit sur celle qu'il ne tient plus (ASP-INV-97, "
                    "ASP-INV-87).")
            corps_opt = opt.get("sequence") or []
            ecrit, _ = _verdicts_du_document(corps_opt)
            if ecrit:
                errs.append(
                    "ASP-CI-45 : la garde d'autorité écrit "
                    f"{sorted(ecrit)} — hors classe O le geste n'a PAS "
                    "d'objet : le script s'arrête SANS RIEN ÉCRIRE, et la "
                    "mémoire d'une éventuelle mission reste intacte "
                    "(ASP-INV-87, ASP-INV-91).")
            if not any(isinstance(s, dict) and "stop" in s for s in corps_opt):
                errs.append(
                    "ASP-CI-45 : la garde d'autorité ne s'arrête pas — sans "
                    "`stop:`, la séquence poursuivrait vers le geste que la "
                    "garde vient de refuser.")
            if rang_garde is None:
                rang_garde = i
    rang_dispatch, branches = _branches_de_geste(top)
    if rang_garde is None:
        errs.append(
            "ASP-CI-45 : aucune garde de premier niveau ne confronte "
            f"`{ID_VERDICT}` à `verdict_ouvert`. L'offre d'un geste de "
            "conduite Arsenal se règle sur le verdict, et sur lui seul : "
            "sans cette garde, une activité qu'Arsenal n'a jamais ouverte "
            "serait conduite (ASP-INV-97, ASP-INV-87).")
    elif rang_dispatch is None:
        errs.append("ASP-CI-45 : aucune étape de premier niveau ne dispatche "
                    "les quatre gestes.")
    elif rang_garde >= rang_dispatch:
        errs.append(
            f"ASP-CI-45 : la garde d'autorité est au rang {rang_garde}, le "
            f"dispatch des gestes au rang {rang_dispatch} — la garde doit "
            "PRÉCÉDER. Une garde postérieure au geste ne refuse plus rien "
            "qui n'ait déjà été fait.")
    if set(branches) != set(GESTES_L2):
        errs.append(f"ASP-CI-45 : le dispatch traite {sorted(branches)} — "
                    f"attendu exactement {sorted(GESTES_L2)} (D-02).")

    # ── (b) ARRÊT — aucune restriction de sens physique, jamais ───────────
    corps_arret = branches.get(GESTE_SANS_RESTRICTION)
    if corps_arret is None:
        errs.append(f"ASP-CI-45 : la branche `{GESTE_SANS_RESTRICTION}` est "
                    "introuvable.")
    else:
        stops = [s for s in _aplatir(corps_arret)
                 if isinstance(s, dict) and "stop" in s]
        if stops:
            errs.append(
                f"ASP-CI-45 : la branche `{GESTE_SANS_RESTRICTION}` porte "
                f"{len(stops)} abstention(s) `stop:` — l'arrêt est proposé "
                "PENDANT TOUTE la classe O, sans dépendre du témoin natif de "
                "session. Son offre ne se règle pas sur l'activité physique "
                "observée : c'est la conséquence directe d'`ASP-INV-43` — "
                "l'arrêt n'est jamais plus contraint que le lancement "
                "(ASP-INV-97).")
        premier = corps_arret[0] if corps_arret else None
        engage = ENGAGEMENT_DU_GESTE[GESTE_SANS_RESTRICTION]
        ecrit, _ = _verdicts_du_document(premier)
        if ecrit != {engage}:
            errs.append(
                f"ASP-CI-45 : la première étape de `{GESTE_SANS_RESTRICTION}` "
                f"écrit {sorted(ecrit) or 'rien'} — attendu `{engage}` et lui "
                "seul. L'engagement s'écrit AVANT la commande, et rien ne "
                "s'interpose entre la garde d'autorité et lui (ASP-INV-88).")

    # ── (c) RETOUR BASE — trois exclusions de sens physique, backend ──────
    corps_retour = branches.get("retour_base")
    if corps_retour is None:
        errs.append("ASP-CI-45 : la branche `retour_base` est introuvable.")
    else:
        garde = ""
        for st in corps_retour:
            if isinstance(st, dict) and isinstance(st.get("choose"), list):
                for opt in st["choose"]:
                    if isinstance(opt, dict):
                        garde += _conditions_option(opt)
                break
        # Deux des trois exclusions sont portees par la TABLE `retour`,
        # declaree au premier niveau ; la troisieme est litterale dans la
        # garde. On relit donc la table ET la garde, jamais l'une pour
        # l'autre : une table amputee laisserait la garde inchangee, et une
        # garde qui n'interroge plus la table laisserait la table intacte.
        variables = {}
        for st in top:
            if isinstance(st, dict) and isinstance(st.get("variables"), dict):
                variables.update(st["variables"])
        portee_table = set(variables.get("retour") or [])
        attendu_table = set(EXCLUSIONS_PHYSIQUES_RETOUR) - {"charging"}
        if portee_table != attendu_table:
            errs.append(
                f"ASP-CI-45 : la table `retour` porte {sorted(portee_table)} "
                f"— attendu exactement {sorted(attendu_table)}, les deux "
                "états de la chaîne de retour. Une exclusion retirée offre un "
                "geste sans objet ; une exclusion de plus retire une offre "
                "que rien ne fonde (ASP-INV-48).")
        if "retour" not in garde:
            errs.append(
                "ASP-CI-45 : la garde de `retour_base` n'interroge pas la "
                "table `retour` — les exclusions « déjà en retour » et "
                "« en cours d'amarrage » cesseraient de s'appliquer, et le "
                "geste serait offert sans rien avoir à ordonner "
                "(ASP-INV-48, ASP-INV-97).")
        if "'charging'" not in garde:
            errs.append(
                "ASP-CI-45 : la garde de `retour_base` n'exclut pas "
                "`charging` — un robot déjà en charge est arrivé : le "
                "renvoyer "
                "à sa base est un geste sans objet (ASP-INV-48).")

    # ── (d) INTERFACE — non-régression des deux sites, avant le lot 6 ─────
    src = lovelace.get(FICHIER_UI_MISSION)
    if src is None:
        errs.append(f"ASP-CI-45 : `{FICHIER_UI_MISSION}` est introuvable.")
        return errs
    try:
        doc_ui = yaml.safe_load(src)
    except yaml.YAMLError as exc:
        errs.append(f"ASP-CI-45 : `{FICHIER_UI_MISSION}` est illisible "
                    f"({exc}).")
        return errs
    sites = {}
    for n in _mappings(doc_ui):
        if n.get("type") != "conditional":
            continue
        gestes = set(_gestes_du_noeud(n.get("card")))
        if len(gestes) == 1:
            sites[gestes.pop()] = n.get("conditions") or []
    for geste in ("arret", "retour_base"):
        if geste not in sites:
            errs.append(f"ASP-CI-45 : aucun site d'offre isolé pour le geste "
                        f"`{geste}` dans `{FICHIER_UI_MISSION}`.")
    exclus_ui = {c.get("state_not") for c in sites.get("retour_base", [])
                 if isinstance(c, dict) and "state_not" in c}
    if "retour_base" in sites and exclus_ui != EXCLUSIONS_UI_RETOUR:
        errs.append(
            f"ASP-CI-45 : le site « Renvoyer à la base » exclut "
            f"{sorted(exclus_ui)} — attendu exactement "
            f"{sorted(EXCLUSIONS_UI_RETOUR)}. Le lot 6 changera l'AUTORITÉ de "
            "ce site ; il conserve ces trois exclusions TELLES QUELLES "
            "(ASP-INV-48).")
    exclus_arret = [c for c in sites.get(GESTE_SANS_RESTRICTION, [])
                    if isinstance(c, dict) and "state_not" in c]
    if exclus_arret:
        errs.append(
            f"ASP-CI-45 : le site « Arrêter la mission » exclut "
            f"{sorted(c['state_not'] for c in exclus_arret)} — l'arrêt est "
            "offert PENDANT TOUTE la classe O, sans exclusion d'état. Un "
            "bouton retiré alors que le backend l'accepterait est une "
            "sous-offre, exactement le défaut que ce chantier lève "
            "(ASP-INV-97, RC-02).")
    return errs

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Vérification contractuelle du domaine Aspirateur.")
    ap.add_argument("--selftest", action="store_true",
                    help="exécute les cas de test internes puis sort.")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    return run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
