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

2. La **conduite runtime** (ASP-CI-11 … ASP-CI-27). Les obligations que le
   contrat énonçait sans pouvoir les confronter — écrivain unique, forme
   enveloppée de la charge utile, convention de passages, interdiction
   d'écrire le mode dérivé, ordre de la séquence, unicité de la commande,
   fermeture du vocabulaire de verdict, totalité du motif lisible, constantes
   temporelles — le sont désormais.

CE QUE LE LOT L1 NE COUVRE PAS, ET POURQUOI C'EST ÉCRIT ICI. L1 porte le seul
lancement : ni conduite d'une mission ouverte, ni supervision continue, ni UI.
Trois codes du catalogue restent donc sans écrivain — `MISSION_INTERROMPUE` et
`ERREUR_EN_MISSION` (supervision continue, lot ultérieur) et
`CANAL_INDISPONIBLE` (diagnostic de l'APPELANT : si la demande n'atteint pas
Home Assistant, aucun moteur ne s'exécute pour l'écrire). Un quatrième,
`COMMANDE_REJETEE`, est **structurellement** hors de portée : Home Assistant
n'expose aucune construction YAML d'attrapage d'erreur, et distinguer un rejet
d'une interruption d'exécution exigerait un observateur survivant à l'appel,
donc un second script. ASP-CI-18 **interdit** au moteur d'écrire ces codes — un
verdict anticipé affirmerait un rejet avant qu'un rejet soit observable —
pendant qu'ASP-CI-19 **exige** leur traduction dans le motif lisible : le
catalogue reste total, sans qu'aucun verdict ne dépasse la connaissance acquise.

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
  ASP-CI-5  Profils     — cinq profils exactement, `gentle` exclu, valeurs
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

Dix-sept contrôles de CONDUITE, adossés au runtime L1 :

  ASP-CI-11 Écrivain unique — un seul script, `mode: single`, quatre champs ;
                          AUCUN autre YAML de configuration n'écrit les deux
                          helpers ni n'appelle `vacuum.*` / `roborock.*` ; la
                          garde template et le moteur appliquent la MÊME règle
                          sur les MÊMES témoins (ASP-INV-31/32/61).
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
                          déclencherait lui-même (07 §6).
  ASP-CI-15 Mode dérivé — `select.entree_…_mode_de_nettoyage` n'est jamais la
                          CIBLE d'une écriture : l'écrire écrase le profil
                          d'aspiration (ASP-INV-12).
  ASP-CI-16 Ordre       — carte, puis EAU, puis ASPIRATION, puis commande, et
                          une relecture des gardes INTERCALÉE entre le dernier
                          réglage et l'émission, portant sur les QUATRE témoins
                          (ASP-INV-34/36).
  ASP-CI-17 Commande    — exactement une émission de démarrage (ASP-INV-35).
  ASP-CI-18 Verdict     — DÉCOMPTE du vocabulaire RECALCULÉ et confronté au
                          texte du helper : les valeurs de verdict et les codes
                          du catalogue comptent 18 éléments chacun et SE
                          RECOUPENT, un décompte qui les dirait disjoints est
                          faux ; vocabulaire FERMÉ et intégralement atteignable ;
                          `ISSUE_NON_ETABLIE` posé AVANT l'appel avec la
                          trace, `COMMANDE_ACCEPTEE` seulement au retour
                          réussi ; aucun `continue_on_error` ; aucun des quatre
                          codes hors de portée de L1 (ASP-INV-37/38/49).
  ASP-CI-19 Motif       — les 18 codes du catalogue et les 4 valeurs de cycle
                          de vie traduits, chacun sous 255 caractères, sans
                          index nu, sans libellé d'appareil, sans nom d'entité
                          (ASP-INV-6/7/50/53).
  ASP-CI-20 Constantes  — trois fenêtres de 30 s et une de 60 s dans le moteur,
                          aucune autre temporisation, aucun helper temporel
                          (ASP-INV-69).
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
# MAINTENANCE — ASP-CI-29 … ASP-CI-33 (lot M0, chapitre 14)
#
# ASP-CI-28 est RESERVE a la confrontation du referentiel embarque de la
# couche d'intention (arbitrage A-13, lot U0). Il n'est pas libre : il est
# pris. La numerotation du domaine se lit donc 1..27 + [28 reserve] + 29..33.
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

# ── F4/F8 : VERROU TRANSITOIRE. L'allowlist est vide en M0, et elle doit le
# rester : le visiteur YAML recursif complet n'existe pas encore. Le desserrer
# avant M2 exposerait la seule primitive irreversible du domaine derriere un
# parseur qui ne couvre ni le flow mapping, ni `tap_action: call-service`, ni
# le scalaire replie, ni les alias YAML, ni le ciblage par `device_id`, ni
# l'entite templatisee. Toute allowlist non vide leve donc une ERREUR, avant
# toute analyse permissive.
ALLOWLIST_PRESSION: frozenset[str] = frozenset()
VISITEUR_YAML_RECURSIF = False   # M2 le passera a True, avec le parseur

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
AID_N1_AUTORISES = frozenset({AID_N1_MISSION, AID_N1_MAINTENANCE})
# Hors perimetre N1, et pour des raisons distinctes : `...01` est la
# supervision W3 (ecrivain du verdict, lot L2) ; `...04` la remise a zero de
# la composition d'intention (lot U0, bloque par `A-5`).
AID_HORS_N1 = {"10280000000001": "supervision de mission W3 — lot L2",
               "10280000000004": "remise a zero de la composition — lot U0"}
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
VERROU_N1_MISSION = True

# Identifiants de notification. FERMES : 08_NOTIFICATIONS.md §1 en fixe deux,
# un par canal persistant, et le lot n'en instancie qu'un.
NOTIF_N1_ENTRETIEN = "aspirateur_entretien"
NOTIF_N1_MISSION = "aspirateur_mission"
NOTIF_N1_FERMES = frozenset({NOTIF_N1_ENTRETIEN, NOTIF_N1_MISSION})
# Ce que N1 instancie REELLEMENT. La difference avec l'ensemble ferme est le
# volet differe, et elle est verifiee — pas seulement commentee.
NOTIF_N1_INSTANCIES = frozenset({NOTIF_N1_ENTRETIEN})

TITRE_N1_ENTRETIEN = "\U0001F9F0 Aspirateur \u2013 Entretien requis"
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
# Toute mention d'un bouton d'entretien, ou l'un des quatre boutons nommes.
BOUTON_ENTRETIEN_RE = re.compile(
    r"button\.roborock_q7_max_reinitialiser_le_consommable_[a-z_]+")
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
    if len(profils) != 5:
        errs.append(f"ASP-CI-5 : la table des profils doit en compter 5 "
                    f"(trouvé {len(profils)}).")
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
    """
    errs = []
    corps = corps if corps is not None else {"sequence": top}
    idx_svc, idx_var, idx_wait = {}, {}, {}

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
        svc = _service(step)
        if svc:
            for cible in _cibles(step):
                idx_svc.setdefault((svc, cible), i)

    # (a) allowlist FERMÉE — nulle part ailleurs, à AUCUNE profondeur.
    #     La visite est exhaustive : `repeat`, `if`, `parallel` et toute
    #     séquence imbriquée sont inspectés, et le CHEMIN est cité.
    autorisees = {(s, c) for s, c, _t, _r in ECRITURES_PREPARATOIRES}
    au_premier_niveau = {id(s) for s in top}
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
                f"premier niveau de la séquence (07 §3).")

    for svc, cible, instant, refus in ECRITURES_PREPARATOIRES:
        i_svc = idx_svc.get((svc, cible))
        if i_svc is None:
            errs.append(f"ASP-CI-27 : écriture préparatoire `{svc}` vers "
                        f"`{cible}` introuvable (07 §3).")
            continue
        # (b) l'écriture DOIT absorber l'exception, sinon le moteur se tait.
        if not top[i_svc].get("continue_on_error"):
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

# Vocabulaire FERMÉ du verdict — 18 valeurs, aucune autre.
VOCABULAIRE_VERDICT = frozenset({
    "VALIDATION_EN_COURS",
    "REFUS/SELECTION_VIDE", "REFUS/SEGMENT_INCONNU", "REFUS/SELECTION_MULTI_CARTE",
    "REFUS/CARTE_NON_CONFIRMEE", "REFUS/PROFIL_INCONNU",
    "REFUS/PASSAGES_HORS_CONTRAT", "REFUS/PREREQUIS_MATERIEL_ABSENT",
    "REFUS/ROBOT_INDISPONIBLE", "REFUS/ETAT_NON_QUALIFIE",
    "REFUS/ERREUR_EQUIPEMENT", "REFUS/MISSION_DEJA_OUVERTE",
    "REFUS/SESSION_INACHEVEE", "REFUS/REGLAGE_NON_CONFIRME",
    "COMMANDE/ISSUE_NON_ETABLIE", "EMISSION/COMMANDE_ACCEPTEE",
    "ECHEC/TRANSITION_NON_OBSERVEE", "LANCEE/DEMARRAGE_OBSERVE"})

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
# 18 codes du catalogue.
CYCLE_DE_VIE = ("VALIDATION_EN_COURS", "ISSUE_NON_ETABLIE",
                "COMMANDE_ACCEPTEE", "DEMARRAGE_OBSERVE")

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
    for i, step in enumerate(top):
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
    for rel, txt in sorted(yaml_depot.items()):
        if rel in RUNTIME_FICHIERS:
            continue
        for helper in (ID_VERDICT, ID_TRACE):
            if helper in txt:
                errs.append(f"ASP-CI-11 : {rel} référence `{helper}` — les "
                            f"helpers du domaine n'ont qu'UN écrivain, le "
                            f"moteur (ASP-INV-31).")
        # `- action: vacuum.stop` comme `  action: vacuum.stop` : le tiret de
        # liste fait partie de la ligne, l'oublier laisserait passer la forme
        # la plus courante. Le guillemet est optionnel — un scalaire cite est
        # le meme appel — et `perform_action` est l'alias moderne de
        # `service`, que la forme anterieure ignorait.
        for m in re.finditer(r'^[ \t]*-?[ \t]*(?:action|service|perform_action)'
                             r'[ \t]*:[ \t]*["\']?'
                             r'(vacuum\.[a-z_]+|roborock\.[a-z_]+)["\']?[ \t]*$',
                             sans_commentaires_yaml(txt), re.M):
            errs.append(f"ASP-CI-11 : {rel} appelle `{m.group(1)}` — seul le "
                        f"moteur commande l'appareil (ASP-INV-31).")

    # C-6 : dans les CINQ fichiers runtime que ce module nomme, les slots
    # critiques sont litteraux. Les balayages ci-dessus sont textuels ; sans
    # cette regle, `service: "{{ 'vacu' ~ 'um.start' }}"` les traversait sans
    # qu'aucune sous-chaine interdite n'apparaisse. Le perimetre vient de
    # `RUNTIME_FICHIERS`, pas d'une recherche de mots dans le contenu.
    for rel in RUNTIME_FICHIERS:
        errs += refus_slots_templatises(
            "ASP-CI-11", rel,
            sans_commentaires_yaml(textes_runtime.get(rel, "")))

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
    """ASP-CI-14 / ASP-CI-15 — voie zonée, mode dérivé, démarreurs interdits."""
    errs = []
    for rel in RUNTIME_FICHIERS:
        txt = sans_commentaires_yaml(textes_runtime.get(rel, ""))
        for interdit in VOIES_INTERDITES:
            if re.search(rf'\b{re.escape(interdit)}\b', txt):
                errs.append(f"ASP-CI-14 : {rel} emploie `{interdit}` — voie "
                            f"zonée ou démarreur interdit (07 §6, "
                            f"ASP-INV-19).")
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

    def _partout(pred):
        return [ch for ch, s in _actions(top) if pred(s)]

    def _au_premier_niveau(pred):
        return [i for i, s in enumerate(top) if pred(s)]

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
    hors = valeurs - VOCABULAIRE_VERDICT
    if hors:
        errs.append(f"ASP-CI-18 : vocabulaire de verdict NON fermé — valeurs "
                    f"hors contrat : {sorted(hors)} (ASP-INV-52).")
    absentes = VOCABULAIRE_VERDICT - valeurs
    if absentes:
        errs.append(f"ASP-CI-18 : le moteur n'écrit jamais {sorted(absentes)} "
                    f"— le vocabulaire fermé doit être intégralement "
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
    for rel in RUNTIME_FICHIERS:
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

    # c) profils : les cinq du contrat, valeurs natives bornées
    profils = variables.get("profils") or {}
    contrat_profils = parse_profils(t03)
    if len(profils) != 5 or len(contrat_profils) != 5:
        errs.append(f"ASP-CI-21 : cinq profils exactement — moteur "
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
    """Les cinq fichiers du lot L1, tels quels — commentaires compris."""
    out: dict[str, str] = {}
    for rel in RUNTIME_FICHIERS:
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
        ("ASP-CI-11 écrivain unique",
         check_ecrivain_unique(moteur_yaml, runtime, depot)),
        ("ASP-CI-12 charge utile enveloppée · ASP-CI-13 passages",
         check_charge_utile(etapes)),
        ("ASP-CI-14 voies interdites", check_voies_interdites(runtime)),
        ("ASP-CI-15 mode dérivé jamais écrit", check_mode_jamais_ecrit(etapes)),
        ("ASP-CI-16 ordre · ASP-CI-17 commande unique",
         check_ordre_sequence(corps.get("sequence") or [])),
        ("ASP-CI-18 vocabulaire de verdict",
         check_vocabulaire_verdict(corps.get("sequence") or [], runtime)
         + check_decompte_vocabulaire(runtime,
                                      textes.get(FICHIER_CATALOGUE, ""))),
        ("ASP-CI-19 motif lisible total",
         check_motif_total(textes.get(FICHIER_CATALOGUE, ""),
                           textes.get("02_referentiel_cartes_et_pieces.md", ""),
                           runtime[RUNTIME_MOTIF])),
        ("ASP-CI-20 constantes temporelles du moteur",
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
        # ASP-CI-28 : RÉSERVÉ — confrontation du référentiel embarqué de la
        # couche d'intention (A-13, lot U0). Non libre, non réutilisable.
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
    )

    erreurs: list[str] = []
    for label, errs in controles:
        print(f"  {'✗' if errs else '✔'} {label}")
        erreurs.extend(errs)

    attestes_audit = tous_les_jetons(attestation)
    print(f"\n  périmètre : {len(textes)} fichiers de contrat · "
          f"{len(lovelace)} fichiers Lovelace balayés · "
          f"{len(runtime)} fichiers runtime L1 · "
          f"{len(depot)} fichiers YAML balayés par ASP-CI-11 · "
          f"{len(fonctionnel)} fichiers YAML fonctionnels balayés par ASP-CI-31 · "
          f"{len(attestes_audit)} identifiants attestés (audit + relevé) · "
          f"{1 if m1 else 0} fichier runtime M1 (projection d'entretien) · "
          f"{len(n1)} fichier(s) runtime N1 (projection persistante)")
    if erreurs:
        print("\nAspirateur — écarts contractuels détectés :")
        for e in erreurs:
            print(f"- {e}")
        return 1
    print("\nOK - domaine Aspirateur : intégrité normative, conduite "
          "runtime, acte contractuel Maintenance, projection "
          "d'entretien et projection persistante vérifiées — "
          f"{len(controles)} lignes affichées pour 38 contrôles logiques, "
          "0 écart.")
    print("     décompte : ASP-CI-12/13 et ASP-CI-16/17 partagent chacun une "
          "ligne ; ASP-CI-28 est RÉSERVÉ au lot U0 et n'est pas exécuté.")
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
    for source, ensemble in (("configuration fonctionnelle", fonctionnel),
                             ("Lovelace", lovelace)):
        for rel, txt in sorted(ensemble.items()):
            nu = sans_commentaires_yaml(txt)
            boutons = set(BOUTON_ENTRETIEN_RE.findall(nu))
            if not boutons:
                continue
            if rel not in ALLOWLIST_PRESSION:
                errs.append(f"ASP-CI-31 : {rel} ({source}) mentionne "
                            f"{', '.join('`' + b + '`' for b in sorted(boutons))} "
                            "— hors allowlist nominative (ASP-INV-81).")
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
    lignes = [("Normale", "balanced", "off"), ("Turbo", "turbo", "off"),
              ("Max", "max", "off"), ("Moyenne", "quiet", "medium"),
              ("Intensive", "quiet", "high")]

    def t03(rows):
        corps = "".join(f"| **{n}** | `{f}` | `{e}` |\n" for n, f, e in rows)
        return "## 1. Table canonique\n" + corps + "\n## 2. suite\n"
    c.conforme(check_profils(t03(lignes)), "CI-5 conforme")
    c.viole(check_profils(t03(lignes[:4])), "compter 5", "CI-5 cardinalité")
    c.viole(check_profils(t03(lignes[:4] + [("Douce", "gentle", "off")])),
            "gentle", "CI-5 gentle réintroduit")
    c.viole(check_profils(t03(lignes[:4] + [("Bizarre", "ultra", "off")])),
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
    assert len(rt0) == len(RUNTIME_FICHIERS), \
        f"runtime L1 introuvable : {sorted(set(RUNTIME_FICHIERS) - set(rt0))}"
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
        "n'ont qu'UN écrivain", "CI-11 second écrivain du verdict")
    c.viole(check_ecrivain_unique(
        mot0, rt0, dict(depot0, **{"11_automations/x.yaml":
                                   "    - action: vacuum.stop\n"})),
        "seul le moteur commande", "CI-11 commande concurrente du robot")
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
        "NON fermé", "CI-18 valeur hors vocabulaire")
    r_sup = mot_txt('value: "LANCEE/DEMARRAGE_OBSERVE"',
                    'value: "EMISSION/COMMANDE_ACCEPTEE"')
    c.viole(check_vocabulaire_verdict(
        _aplatir(yaml.safe_load(r_sup[RUNTIME_MOTEUR])[ID_MOTEUR]["sequence"]),
        r_sup),
        "n'écrit jamais", "CI-18 valeur du vocabulaire inatteignable")
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
        '      data: "{{ {\'option\': ctx_carte.option} }}"',
        '      data:\n        option: "{{ ctx_carte.option }}"')
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
        "14 codes du catalogue figurent", "13 codes du catalogue figurent")
    c.viole(check_decompte_vocabulaire({**rt0, RUNTIME_HELPERS: faux}, t09_n),
            "décompte FAUX", "CI-18 codes présents sous-comptés (13 au lieu de 14)")
    faux = rt0[RUNTIME_HELPERS].replace(
        "4 codes du catalogue en sont ABSENTS",
        "5 codes du catalogue en sont ABSENTS")
    c.viole(check_decompte_vocabulaire({**rt0, RUNTIME_HELPERS: faux}, t09_n),
            "décompte FAUX", "CI-18 codes absents sur-comptés (5 au lieu de 4)")
    faux = rt0[RUNTIME_HELPERS].replace(
        "4 valeurs de CYCLE DE VIE", "5 valeurs de CYCLE DE VIE")
    c.viole(check_decompte_vocabulaire({**rt0, RUNTIME_HELPERS: faux}, t09_n),
            "décompte FAUX", "CI-18 valeurs de cycle de vie sur-comptées")
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
        for st in m[ID_MOTEUR]["sequence"]:
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
    for st in m_br[ID_MOTEUR]["sequence"]:
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
        return _i(seq, lambda s: _service(s) == svc and cible in _cibles(s))

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
                "NON fermé", f"CI-18/M-A verdict hors vocabulaire sous {nom_nu}")
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
    manquants = (invoques - normatifs - set(CONTROLES_RUNTIME) - controles_m1
                 - controles_n1)
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

    # ---- F4/F8 : verrou transitoire --------------------------------------
    global ALLOWLIST_PRESSION
    _sauv = ALLOWLIST_PRESSION
    try:
        ALLOWLIST_PRESSION = frozenset({"10_scripts/aspirateur/declarer.yaml"})
        _verrou = check_primitive_irreversible(T14, {}, {})
        c.viole(_verrou, "VERROU M0", "F4/CI-31 allowlist non vide refusée")
        assert len(_verrou) == 1, \
            "F4 : le verrou doit court-circuiter TOUTE autre analyse"
        c.conformes += 1
    finally:
        ALLOWLIST_PRESSION = _sauv
    c.conforme(check_primitive_irreversible(T14, {}, {}),
               "F4/CI-31 allowlist vide : analyse normale")

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
            "hors des deux identifiants", "CI-37 ID d'automation incorrect")
    c.viole(check_writers_n1(n1_mut(f'- id: "{AID_N1_MAINTENANCE}"',
                                    '- id: "10280000000001"'), DEPOT_0),
            "supervision de mission W3", "CI-37 ID reserve a L2 employe")
    c.viole(check_writers_n1(n1_mut(f'- id: "{AID_N1_MAINTENANCE}"',
                                    '- id: "10280000000004"'), DEPOT_0),
            "remise a zero de la composition", "CI-37 ID reserve a U0 employe")
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
        "projection persistante de MISSION", "CI-37 projection de cycle batie")
    QUATRIEME = TROISIEME.replace(f'"{AID_N1_MISSION}"', '"10280000000007"') \
                         .replace(NOTIF_N1_MISSION, NOTIF_N1_ENTRETIEN)
    c.viole(check_writers_n1(
        n1_plus(DOSSIER_N1 + "/troisieme.yaml", QUATRIEME), DEPOT_0),
        "hors des deux identifiants", "CI-37 writer a identifiant invente")
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
        "troisieme writer", "CI-37 troisieme automation dans le dossier")

    # Un identifiant du domaine cite HORS de la cle `id:` — forme que le
    # parseur YAML ne rattache a aucune automation.
    c.viole(check_writers_n1(n1_mut(
        "  mode: restart", "  mode: restart\n  # voir 10280000000001"),
        DEPOT_0), "10280000000001", "CI-37 identifiant reserve cite en commentaire")

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
        "seul service admis", "CI-39 ecriture d'un helper")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + f"  bidon: \"{{{{ states('{ID_VERDICT}') }}}}\"\n")),
        "ni n'ecrit le verdict", "CI-39 lecture du verdict")
    c.viole(check_interdits_n1(n1_mut(
        ANCRE_39, ANCRE_39 + "  bidon: LANCEE/DEMARRAGE_OBSERVE\n")),
        "verdict FIGE", "CI-39 cycle deduit du verdict fige")
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
            "seul le moteur commande",
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

    print(f"selftest OK — 38 contrôles logiques (ASP-CI-28 réservé, non "
          f"exécuté), {c.total()} cas "
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
        if aid in AID_HORS_N1:
            errs.append(f"ASP-CI-37 : `{rel}` porte `{aid}` — {AID_HORS_N1[aid]}. "
                        "Cet identifiant n'appartient pas au lot N1.")
        elif aid not in AID_N1_AUTORISES:
            errs.append(f"ASP-CI-37 : `{rel}` porte l'identifiant `{aid}`, hors "
                        f"des deux identifiants attribues au lot "
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
                    "identifiants attribues — un troisieme writer est apparu.")

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
        if not appels:
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
    """ASP-CI-39 — ce que N1 ne fait pas, prouve sur le texte livre.

    Le balayage porte sur le fichier ENTIER, commentaires compris : une
    projection qui NOMME un bouton de remise a zero est deja trop proche de
    la seule primitive irreversible du domaine.
    """
    errs: list[str] = []
    if not n1:
        return [f"ASP-CI-39 : dossier N1 introuvable — `{DOSSIER_N1}`."]
    for rel, txt in sorted(n1.items()):
        nu = sans_commentaires_yaml(txt)
        # C-6 : N1 est un perimetre FERME, lu par dossier nomme. Ses slots
        # critiques sont litteraux — sans quoi aucun des interdits ci-dessous
        # ne pourrait etre etabli sur ce fichier.
        errs += refus_slots_templatises("ASP-CI-39", rel, nu)
        # Le lexique de prediction est cherche dans le CODE, jamais dans les
        # commentaires : un en-tete qui s'INTERDIT nommement une tendance ou
        # une date previsionnelle ne la produit pas — l'y refuser rendrait
        # l'interdit indicible dans le fichier qui le porte.
        bas = nu.lower()

        for m in re.finditer(
                r"^[ \t]*-?[ \t]*(?:action|service|perform_action)[ \t]*:"
                r"[ \t]*[\"']?(vacuum\.[a-z_]+|roborock\.[a-z_]+)", nu, re.M):
            errs.append(f"ASP-CI-39 : `{rel}` appelle `{m.group(1)}` — une "
                        "projection ne commande jamais l'appareil "
                        "(ASP-INV-31).")
        if PRESS_SERVICE.search(nu):
            errs.append(f"ASP-CI-39 : `{rel}` appelle `button.press` — la "
                        "remise a zero est un geste operateur explicite, "
                        "portee par le SEUL script du lot M2 (ASP-INV-77, "
                        "ASP-INV-81).")
        for m in BOUTON_ENTRETIEN_RE.finditer(txt):
            errs.append(f"ASP-CI-39 : `{rel}` nomme `{m.group(0)}` — N1 ne "
                        "presse aucun bouton et n'a pas a le connaitre.")
        if REPETITION.search(nu):
            errs.append(f"ASP-CI-39 : `{rel}` porte une repetition — une "
                        "projection se recalcule, elle ne boucle pas.")
        for helper in (ID_VERDICT, ID_TRACE):
            if helper in txt:
                errs.append(f"ASP-CI-39 : `{rel}` cite `{helper}` — N1 ne lit "
                            "ni n'ecrit le verdict de mission (ASP-INV-31).")
        for jeton in VERDICT_FIGE_N1:
            if jeton in txt:
                errs.append(f"ASP-CI-39 : `{rel}` cite `{jeton}` — un cycle en "
                            "cours ne se deduit pas d'un verdict FIGE. La "
                            "classe T du vocabulaire L1 est vide : cette "
                            "valeur ne s'eteint jamais.")
        for jeton in SESSION_NATIVE_N1:
            if jeton in nu:
                errs.append(f"ASP-CI-39 : `{rel}` lit `{jeton}` — adopter le "
                            "temoin natif de session reviendrait a adopter une "
                            "mission externe (07 §6.2, ASP-INV-47).")
        for jeton in MOBILE_N1:
            if jeton in nu:
                errs.append(f"ASP-CI-39 : `{rel}` emploie `{jeton}` — AUCUN "
                            "envoi mobile dans N1 : le canal 3 est differe a "
                            "L2/W3, faute d'autorite pour etablir « pendant "
                            "une mission » (ASP-INV-84).")
        for jeton in ERREUR_N1:
            if jeton in nu:
                errs.append(f"ASP-CI-39 : `{rel}` porte `{jeton}` — une erreur "
                            "robot ou dock n'est pas un entretien, et hors "
                            "mission le domaine n'ajoute AUCUNE notification "
                            "(ASP-INV-83, ASP-INV-84).")
        for jeton in INTENTION_N1:
            if jeton in nu:
                errs.append(f"ASP-CI-39 : `{rel}` lit `{jeton}` — les helpers "
                            "d'intention relevent du lot U0, qui n'existe pas.")
        for jeton in TEMPOREL_M1:
            if jeton in nu:
                errs.append(f"ASP-CI-39 : `{rel}` emploie `{jeton}` — le seuil "
                            "se constate, il ne se prevoit pas (14 §2).")
        for jeton in PREDICTION_N1:
            if jeton in bas:
                errs.append(f"ASP-CI-39 : `{rel}` annonce « {jeton} » — aucune "
                            "date previsionnelle n'est inventee (14 §2).")
        # Aucune ecriture, d'aucune sorte : un lecteur pur n'ecrit rien.
        for m in re.finditer(
                r"^[ \t]*-?[ \t]*(?:action|service|perform_action)[ \t]*:"
                r"[ \t]*[\"']?([a-z_]+\.[a-z_]+)", nu, re.M):
            svc = m.group(1)
            if not svc.startswith("persistent_notification."):
                errs.append(f"ASP-CI-39 : `{rel}` appelle `{svc}` — le seul "
                            "service admis dans N1 est "
                            "`persistent_notification.*`.")
        # La projection ne lit QUE son autorite et le temoin de readiness.
        for m in re.finditer(r"\b([a-z_]+\.[a-z0-9_]+)\b", nu):
            eid = m.group(1)
            if eid.split(".")[0] not in ("sensor", "binary_sensor",
                                         "input_boolean", "input_text",
                                         "input_select", "input_number",
                                         "vacuum", "button", "switch",
                                         "script", "automation", "notify"):
                continue
            if eid in AUTORITE_N1 or eid == READINESS_N1:
                continue
            errs.append(f"ASP-CI-39 : `{rel}` lit `{eid}` — la projection ne "
                        f"connait que {sorted(AUTORITE_N1)} et "
                        f"`{READINESS_N1}`. Toute autre entite serait une "
                        "seconde autorite.")
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
