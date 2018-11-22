-[_Parcours Open Classrooms_][oc]-
# [PyDev] Projet 10

## _Note_

_La version permanente de ce document restera disponible via [ce lien][readmev04] après la livraison._

_La documentation le l'application web est disponible à cette [addresse][doc]._

## Contexte

La startup [**Pur Beurre**][purbeurre], avec laquelle vous travaillez [depuis quelques mois][p5] déjà, vous à fait développer une application web proposant de trouver un substitut sain à un aliment considéré comme _trop gras, trop sucré et/ou trop salé_ en utilisant :

- les données du projet : [OpenFoodFacts][off]
- le _[framework][wikiframe] web Python_ : [Django][wikidjango]

Jusqu’à maintenant, vous avez déployé l'application en utilisant une solution [_PaaS_][wikipaas] (via [Heroku][heroku]), cette solution facilite le développement mais fait perdre la maîtrise d'une grande partie du processus de déploiement et de la configuration de l'hébergement.

## Historique

* [Livraison][v01] du [projet initial][p8], conformément au [cahier des charges][cdc]
* [Livraison][v03] d'un [1er lot d'évolutions][p11] (voir le [_verbatim_ des échanges client][verbatim] )


## Nouvelle mission

* Héberger l'[environement de production][wikienv] sur un [VPS][wikivps]
* Mettre en place une [Intégration Continue][wikici](CI) avec [Travis CI][ci]
* Suivre l'activité :
    - du serveur avec le monitoring de l'hébergeur
    - de l'application avec [Sentry][sentry]
* Déploiement en production via [CLI][wikicli]
* Utiliser [`cron`][cron] pour automatiser une [tâche de maintenance][issue64] sur le serveur

_Bonus perso :_

* Déploiement automatisé dans un [environnement de qualification][wikienv] (_staging environment_) via [Heroku][herokuapp] après [réussite des tests][ci]

### Livrables

* [Document écrit expliquant votre démarche][approach] de création, les difficultés rencontrées et la manière dont vous les avez résolues. Il doit être en format PDF et ne pas excéder 2 pages A4. Rédigé en anglais ou français.
* Copie d’écran des configurations de :
    - [Travis CI][screenshot]
    - [l'hébergeur][screenshot]
    - [votre tâche `cron`][doccron]
* lien vers votre [tableau agile][P10]
* lien vers votre [projet “déployé”][prod]


[approach]: https://github.com/freezed/ocp8/blob/v0.1/doc/approach.md
[cdc]: https://github.com/freezed/ocp8/blob/v0.1/README.md#cahier-des-charges
[cid]: http://www.alalettre.com/corneille-oeuvres-le-cid.php
[ci]: https://travis-ci.com/freezed/ocp8/builds "Liens vers l'historique des builds sur le site Travis CI"
[cron]: https://fr.wikipedia.org/wiki/Cron "Lien vers la page «cron» sur wikipedia"
[doccron]: https://github.com/freezed/ocp8/blob/v0.4/doc/
[doc]: https://github.com/freezed/ocp8/blob/master/doc/documentation.md
[screenshot]: https://github.com/freezed/ocp8/blob/v0.4/doc/img/
[herokuapp]: https://ocp8-1664.herokuapp.com/
[heroku]: https://www.heroku.com/
[issue64]: https://github.com/freezed/ocp8/issues64
[oc]: https://openclassrooms.com/fr/projects/deployez-votre-application-sur-un-serveur-comme-un-e-pro "Énoncé du P10 sur le site d'OpenClassrooms"
[off]: https://world-fr.openfoodfacts.org/decouvrir "Lien vers la page de présentation du projet OpenFoodFacts"
[p10]: https://github.com/freezed/ocp8/projects/3
[p11]: https://github.com/freezed/ocp8/projects/2
[p5]: https://github.com/freezed/ocp5#pydev-projet-5
[p8]: https://github.com/freezed/ocp8/projects/1
[prod]: http://68.183.223.134/
[purbeurre]: http://68.183.223.134/#about
[readmev04]: https://github.com/freezed/ocp10/blob/v0.4/README.md
[sentry]: https://sentry.io/ "Lien vers le site Sentry.io"
[v01]: https://github.com/freezed/ocp8/releases/tag/v0.1
[v03]: https://github.com/freezed/ocp8/releases/tag/v0.3
[v04]: https://github.com/freezed/ocp8/releases/tag/v0.4
[verbatim]: https://github.com/freezed/ocp8/blob/v0.3/doc/chat-history.md#trancriptions-des-%C3%A9changes--avec-le-client
[wikici]: https://fr.wikipedia.org/wiki/Int%C3%A9gration_continue "Lien vers la page «Intégration continue» sur wikipedia"
[wikicli]: https://fr.wikipedia.org/wiki/Command-line_interface "Lien vers la page «Command Line Interface» sur wikipedia"
[wikidjango]: https://fr.wikipedia.org/wiki/Django_(framework)  "Lien vers la page «Django (framework)» sur wikipedia"
[wikienv]: https://fr.wikipedia.org/wiki/Environnement_(informatique) "Lien vers la page «Environnement (informatique)» sur wikipedia"
[wikiframe]: https://fr.wikipedia.org/wiki/Framework "Lien vers la page «Framework» sur wikipedia"
[wikipaas]: https://fr.wikipedia.org/wiki/Plate-forme_en_tant_que_service "Lien vers la page «Plate-forme en tant que service» sur wikipedia"
[wikivps]: https://fr.wikipedia.org/wiki/Serveur_d%C3%A9di%C3%A9_virtuel "Lien vers la page «Serveur dédié virtuel» sur wikipedia"
