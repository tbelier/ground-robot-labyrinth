# DartV3 Challenge 2022 - Groupe DARTatouille

![Regardez c'est Ratatouille](../../images/ratatouille.jpg)


<h5 align="center"> Projet ROB 2A - <a href="https://www.ensta-bretagne.fr/fr">ENSTA Bretagne</a> (Automne 2022) </h5>

<!-- Auteurs -->
<h2 id="auteurs"> :pencil2: Auteurs</h2>

* **MUSTIERE Ludovic** <ludovic.mustiere@ensta-bretagne.org> (Promotion ENSTA Bretagne 2024 - Spécialité Robotique Autonome)
* **BELIER Titouan** <titouan.belier@ensta-bretagne.org> (Promotion ENSTA Bretagne 2024 - Spécialité Robotique Autonome)
* **MIALLIER Marguerite** <marguerite.miallier@ensta-bretagne.org> (Promotion ENSTA Bretagne 2024 - Spécialité Robotique Autonome)

<!-- Description -->
<h2 id="description"> :scroll: Description</h2>

Le projet a pour objectif de faire effectuer un **circuit** à un robot **Dart**, d'abord sur le simulateur **V-Rep**, puis sur circuit réel. Nous devrons pour cela nous servir des différents capteurs présents sur le robot :
* sonars
* odomètres
* boussole

Le projet sera codé en **Python3**. 

Voici le schéma de Machine à Etats Finis (FSM) de notre programme :
![schema du FSM](../../images/FSM.png)




<!-- Sommaire -->
<h2 id="table-of-contents"> :book: Sommaire</h2>

<details open="open">
  <summary>Sommaire</summary>
  <ol>
    <li><a href="#structure-du-git"> ➤ Structure du Git</a></li>
    <li><a href="#lancer-le-programme"> ➤ Lancer le programme</a></li>
    <li><a href="#fonctions-boucle-principale"> ➤ Les fonctions de la boucle principale</a></li>
    <li><a href="#fonctions-base-drivers"> ➤ Fonctionnalités de base des drivers</a></li>
    <li><a href="#informations-générales"> ➤ Informations générales </a></li>
  </ol>
</details>


<!-- Structure du Git -->
<h2 id="structure-du-git"> :floppy_disk: Structure du Git</h2>


Ce git a pour but de **détailler les fonctions utilisées dans le programme**. En particulier ceux qui se trouvent dans le main. Vous trouverez aussi à la suite une explication brève des fonctions les plus importantes dans les **drivers**. Avec l'explication du code principal puis des différents drivers, vous serez en mesure de comprendre sans souci comment se déplace notre robot ! L'architecture du Git peut se résumer comme ceci :

* `VREP_PRO_EDU`... fichier qui mène vers le **simulateur VREP** 
    * `vrep.sh` : le programme a exécuter pour lancer VREP
    * autres programmes utiles au lancement, l'installation etc.
* `scenes`
    * comporte le **fichier challenge** à lancer dans VREP pour avoir la simulation
* `py` 
    * `dartv2b.py` : programme comportant la **boucle principale** et l'**architecture** de plus haut niveau pour faire fonctionner DARTatouille
    * `robot_cmd_X_qY.py` : programme à lancer pour répondre à la **question Y du TD X**.
    * `stop.py` : programme à lancer impérativement pour **stopper l'avancée du robot** en cas de problème.
    * fichier drivers : comporte tous les **drivers** utiles à l'exécution de dartv2b.py.
    * `dartatouille.py` : contient la **classe Dartatouille**, qui définit toutes les fonctions de mouvement du robot sur simulateur.
    * `dartatouille_real.py` : de même, mais sur circuit réel.
    * `my_own_fsm.py` : contient la **machine à états** de notre robot sur simulateur. C'est le fichier qu'il faudra lancer sur simulateur. 
    * `my_own_fsm_real.py` : contient la **machine à états** du robot réel. C'est ce programme qu'il faudra lancer pour effectuer le circuit réel.
* autres dossiers 


<!-- Structure du Git -->
<h2 id="lancer-le-programme"> :clipboard: Lancer le programme</h2>


Pour lancer le programme il faut **ouvrir Vrep**, mais aussi le code sur Python. **Vous avez de la chance!** En téléchargeant le projet, tout sera à votre disposition : Vrep, les scènes et les codes pythons !

### Lancer Vrep

Pour **lancer Vrep**, il faudra naviguer dans les dossiers. **Suivez le chemin suivant** : `dartv2_mustiere_miallier_belier > VREP_PRO_EDU`.. Lorsque vous êtes dans ce dossier, **clic droit dans la fenêtre > ouvrir un terminal (sur ubuntu) > et entrez la commande** `./vrep.sh`. 

![VREP légendé](../../images/VREP_legend.png)
*VREP avec en légende les fonctionnalités utilisées*

Et voilà, **votre simulateur est ouvert !**

### Ouvrir la scène

Pour **ouvrir la scène**, rien de plus simple. Cliquez tout en haut à gauche sur *File* puis sur *Open scene*. Cherchez votre scene dans le dossier : `dartv2_mustiere_miallier_belier > scenes > dartv2_ue32_2021_challenge.ttt` 

Et voilà **votre simulation est lancée !**

### Ouvrir python

Votre simulateur est maitenant ouvert, mais DARTatouille ne va pas avancer si vous ne lui dites pas quoi faire ! Il vous suffit d'**ouvrir ce code** : `dartv2_mustiere_miallier_belier > py > dartv2b.py`

C'est bon **votre programme est prêt au lancement !**

### Lancer la simulation

Maintenant que tout est fait, appuyez sur la flèche pour lancer la simulation. Une fois que c'est fait, lancez le programme principal sur python. Et voilà ! Vous pouvez retourner sur Vrep pour observer DARTatouille en mouvement !

### Lancer le robot sur circuit réel

Il suffit pour faire effectuer au robot le circuit réel de lancer le programme ```my_own_fsm_real.py``` qui se situe dans le dossier ```.py```.


<!-- Structure du Git -->
<h2 id="informations-générales"> :book: Informations générales</h2>


Ce projet est réalisé par **trois étudiants de 2ème année de l'école d'Ingénieur de l'ENSTA Bretagne**. Lors de ce projet, nous tentons de développer nos compétences en robotique, à la fois sur la partie **simulation** mais aussi avec des **tests réels** sur un circuit grandeur nature.

Si la première partie nous permet de développer notre **réflexion théorique** sans se préocupper des complications techniques, la seconde partie, nous permettra d'apprendre à "bidouiller" pour obtenir des **résultats concluants** dans la vie réelle.


### Etat du projet

A ce stade du projet, le robot effectue avec succès un tour sur le simulateur sans heurter les murs. Sur circuit réel, le robot parvient la plupart du temps à effectuer un tour, mais il arrive régulièrement qu'il frôle ou heurte les murs, ce qui le met en difficulté pour finir le circuit. Nous essayons de résoudre le problème en améliorant le suivi de mur. Les virages sont corrects et n'induisent pas de problèmes.



### Travaux effectués et en cours

Nous avons commencé par **mettre en commun nos idées** sur les fonctionnalités principales à réaliser. Nous avons travaillé sur ce type de projet python par le passé. Le plus important pour ces premières scéances était de mettre en place le **Gitlab**, créer le **README** et réfléchir aux **fonctions à mettre en place**.

**Résumé du travail effectué**
- [X] Suivi de mur
- [X] Choix de la direction où tourner
- [X] Tourner de 90 degré dans un sens défini
- [X] Filtre pour les valeurs absurdes 
- [X] Filtre médian pour lisser les valeurs
- [X] Boucle principale de plus haut niveau qui fusionne les autres fonctions
- [X] Amélioration des coefficients des correcteurs
- [X] Passage à une utilisation de la boussole au lieu des odomètres pour les virages
- [X] Amélioration du suivi de mur afin d'éviter les trop grandes oscillations

**Séance du 02/11** 
- Création de la FSM 
- Test sur un aller-retour
- Création du fichier dartatouille.py contenant la classe Dartatouille. Celle-ci contient les fonctions de contrôle du robot (détection du voltage de la batterie, détection d'obstacle, suivi de mur, choix de la direction à suivre, rotation...), qui sont en cours d'implémentation.

**Séance du 2/12 et précédente**

Le robot a effectué le circuit avec succès sur simulateur, nous sommes donc passés au robot réel. Sur simulateur, nous utilisions les odomètres pour les virages, mais sur le robot réel nous nous sommes rendus compte que cette méthode accumulait trop d'erreurs et ne permettait pas de finir le circuit. Nous avons alors changé de méthode et utilisons la boussole pour tourner avec le robot réel.

**Séance du 12/12 et précédente**

Notre robot a réussi plusieurs fois à faire le circuit complet. Nous avons aussi changé nos régulateur de suivi de mur en ajoutant un régulateur proportionnel et dérivé. Nous avons ensuite testé le robot dans des conditions défavorables en l'initialisant avec un angle pour le forcer à utiliser ce régulateur.

Ensuite nous nous sommes concentrés sur la rotation du robot. Au départ, le robot tournait grâce à la mesure du cap en lui demandait de tourner de 90 degrés par rapport à sa normale avant de tourner. Or cette méthode ne fait qu'ajouter de l'erreur. En effet, si notre robot n'est pas bien aligné il continuera d'ajouter de l'erreur en tournant d'une valeur fixe. Pour corriger cette erreur, nous avons fait le choix d'initialiser les directions vers lequel peut tourner le robot au tout début. Il faut donc bien positionner le robot au tout début, puis il initialise les angles en cap pour aller à gauche et droite dans une liste. A chaque prise de décision il regarde s'il doit tourner à droite ou à gauche et valide le cap qu'il faut choisir en se décalant dans la liste. De cette façon, s'il a un peut trop tourné au début, il se recale quand même dans la bonne direction à la fin de son virage.

Voici une première vidéo de notre robot se déplaçant dans le parcours : https://youtu.be/w9SPToD5MVE. Nous mettrons les nouvelles vidéos des avancées pour les prochaines scéances.

**Séance du 4/01**

Cette ultime séance nous a permis de faire les dernières modifications sur les coefficients proportionnel et dérivé du régulateur de Dartatouille ainsi que la distance à laquelle il doit s'arrêter. Nous avions également des soucis pour communiquer avec le robot 11 donc nous avons changé pour le **robot 6**. Après une calibration de la boussole, nous l'avons lancé et il a réalisé un tour complet qui s'est passé à **10h30min45s (le 04 janvier 2023)**. 



