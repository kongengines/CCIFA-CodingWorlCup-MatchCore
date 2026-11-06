# Règlement Officiel CCIFA

**Code & Craft International Federation Association (CCIFA)**
**Coupe du Monde de Coding — Statuts souverains du sport-coding**

> Version v1.0 — Copie certifiée en français. En cas de divergence,
> le texte maître en anglais prévaut.

---

## Préambule

La Code & Craft International Federation Association (« CCIFA ») est la
fédération internationale gouvernant la Coupe du Monde de Coding,
compétition quadriennale de sport-coding organisée entre les cinq
confédérations continentales et leurs fédérations nationales affiliées.

MatchCore est le moteur vivant, en ligne et souverain qui gère toutes
les dimensions de la vie du sport-coding : fédérations, confédérations,
ligues, clubs, codeurs, drafts, licences, transferts, classements,
calendriers, arbitrage, matchs et Coupe du Monde.

Seuls les **matchs officiels** se jouent **100% hors ligne** dans des
arènes souveraines. Chaque match officiel est scellé par un hachage
SHA-256 chaîné et une signature Ed25519 de l'arbitre (le « Sceau
Souverain ») et enregistré de manière immuable dans le Grand Livre
Souverain.

---

## Article 1 — Définitions

1.1 **CCIFA** : la Code & Craft International Federation Association.

1.2 **MatchCore** : le moteur souverain du CCIFA, comprenant son pack
   de règles, son API REST, sa CLI, son tableau de bord et le Grand
   Livre Souverain.

1.3 **Confédération** : l'un des cinq organismes continentaux —
   Africaine (AF), Amériques (AM), Asiatique (AS), Européenne (EU)
   et Océanienne (OC).

1.4 **Ligue** : compétition annuelle (nationale, continentale ou
   Coupe du Monde) avec calendrier et classement.

1.5 **Club** : club de sport-coding affilié, avec effectif, budget
   et sponsor optionnel.

1.6 **Codeur** : athlète licencié de l'un des quatre domaines —
   Coder, Designer, Maker, Strategist.

1.7 **Match officiel** : match joué 100% hors ligne dans une arène
   souveraine, scellé et enregistré dans le Grand Livre Souverain.

1.8 **Sceau Souverain** : enregistrement cryptographique comprenant
   un hachage racine SHA-256 chaîné et une signature Ed25519 de
   l'arbitre.

1.9 **Grand Livre Souverain** : journal JSONL à ajout unique, chaîné
   par SHA-256, de chaque événement CCIFA.

1.10 **Langues certifiées** : EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR.

---

## Article 2 — Structure de la Fédération

2.1 Le CCIFA est composé d'un Président, de trois Vice-Présidents et
    de quatre comités permanents : Comité Exécutif, Comité de
    Sport-Coding, Comité d'Arbitrage, et Comité d'Éthique et
    d'Intégrité.

2.2 Le Président est élu pour un mandat renouvelable de quatre ans
    par l'Assemblée Générale.

2.3 Le Comité Exécutif gère les affaires courantes du CCIFA.

2.4 Le Comité de Sport-Coding gouverne le pack de règles.

2.5 Le Comité d'Arbitrage accrédite les arbitres et statue sur les
    appels.

2.6 Le Comité d'Éthique et d'Intégrité fait appliquer le Code
    Disciplinaire.

2.7 Les cinq confédérations sont autonomes en leurs affaires internes
    mais liées par le présent Règlement.

---

## Article 3 — Licences

3.1 Trois niveaux de licences existent : **PRO**, **SEMI** et
    **AMATEUR**.

3.2 Seuls les titulaires d'une licence PRO ou SEMI peuvent participer
    aux matchs officiels.

3.3 Les licences sont délivrées pour une saison et expirent le 31 août.

3.4 Elles requièrent l'aval de la fédération, un contrôle médical
    (compétence) et une vérification éthique.

3.5 Elles peuvent être révoquées pour dopage, trucage de match,
    plagiat répété ou manquement éthique.

3.6 Des plafonds salariaux s'appliquent par niveau.

---

## Article 4 — Clubs et Ligues

4.1 Un club doit détenir une licence de club CCIFA pour concourir.

4.2 Effectifs de 5 à 25 codeurs, dont au moins 3 licences PRO.

4.3 Les ligues attribuent 3 points pour une victoire, 1 pour un
    nul, 0 pour une défaite.

4.4 Promotion et relégation suivent la règle des 2 premiers / 2
    derniers.

4.5 Critères de départage : points, différence de buts, buts pour,
    confrontation directe, fair-play.

4.6 Des ligues continentales existent par confédération ; la Coupe
    du Monde est le tournoi final quadriennal.

---

## Article 5 — Drafts et Transferts

5.1 Un draft annuel est organisé ; l'ordre est l'inverse du
    classement de la saison précédente.

5.2 Éligibilité : âge minimum 16 ans, licence amateur ou semi, sans
    contrat PRO antérieur.

5.3 Trois tours ; chaque club sélectionne un codeur par tour.

5.4 Les transferts se font uniquement en fenêtres officielles et
    nécessitent les signatures des deux clubs, du codeur, un contrôle
    médical et l'aval de la fédération.

5.5 Le Fair-Play Financier plafonne le ratio salaires/recettes à 0,7.

---

## Article 6 — Matchs officiels et Sceau Souverain

6.1 Les matchs officiels se jouent 100% hors ligne dans des arènes
    souveraines.

6.2 Le réseau de l'arène doit être **physiquement coupé** pendant le
    match.

6.3 Chaque match officiel a un seul arbitre président, qui signe le
    Sceau Souverain avec une clé Ed25519.

6.4 Le sceau comprend un hachage racine (SHA-256 de la charge utile
    canonique du match), la signature et un hachage de chaîne lié à
    l'événement précédent.

6.5 L'enregistrement scellé est exporté de l'arène par un coursier
    assermenté sur support physique (USB) et importé dans MatchCore.

6.6 Pas de sceau, pas de résultat. Un match sans Sceau Souverain
    valide est nul et non avenu.

---

## Article 7 — Arbitrage

7.1 Les arbitres sont accrédités par le Comité d'Arbitrage pour un
    mandat renouvelable de deux ans.

7.2 Chaque match officiel a un arbitre président.

7.3 Les arbitres peuvent rendre quatre décisions : VALIDE, INVALIDE,
    PÉNALITÉ, DISQUALIFICATION.

7.4 Les appels sont recevables sous 48 heures ; le Comité d'Arbitrage
    les réexamine.

7.5 Les arbitres sont liés par la Charte des Arbitres.

---

## Article 8 — Coupe du Monde

8.1 La Coupe du Monde de Coding est le tournoi final quadriennal du
    CCIFA.

8.2 Chaque confédération organise ses qualifications ; l'hôte
    tourne parmi les cinq confédérations.

8.3 Le format des finales comprend une phase de groupes, un tableau
    à élimination directe et une finale unique.

8.4 Le vainqueur de la finale est sacré Champion du Monde de
    sport-coding.

8.5 Chaque match de la Coupe du Monde est un match officiel et
    scellé.

---

## Article 9 — Souveraineté du Grand Livre

9.1 Le Grand Livre Souverain est la source unique de vérité pour
    chaque événement CCIFA.

9.2 Il est à ajout unique ; aucune entrée ne peut être modifiée ou
    supprimée.

9.3 La vérification est déterministe et rejouable depuis le hachage
    de genèse.

9.4 Toute partie peut vérifier le grand livre à tout moment via
    l'endpoint REST `POST /ledger/verify`.

9.5 Un grand livre qui échoue à la vérification est nul ; la
    fédération doit déclarer un incident de continuité (voir le PCA).

---

## Article 10 — Dispositions finales

10.1 Le présent Règlement est certifié en 11 langues ; le texte
     maître en anglais prévaut en cas de divergence.

10.2 Les amendements requièrent une majorité des deux tiers du
     Comité Exécutif et ratification par l'Assemblée Générale.

10.3 Le présent Règlement entre en vigueur à la date de son scellement.

10.4 Toute question non couverte est gouvernée par le Comité de
     Sport-Coding, sous réserve d'appel au Comité d'Arbitrage.


---

## Bloc de Certification CCIFA

| Champ | Valeur |
|-------|--------|
| Document | Règlement Officiel CCIFA |
| Langue | Français (copie certifiée) |
| Version | v1.0 |
| Émis par | Comité Exécutif CCIFA |
| Langues certifiées | EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR |
| Sceau | SHA-256(ccifa-legal-regulations) |
| Statut | Certifié |

> Ce document est certifié dans les 11 langues officielles du CCIFA. En
> cas de divergence, le texte maître en anglais prévaut.

Certifié par le **Comité Exécutif du CCIFA** au nom de la Code & Craft
International Federation Association.
