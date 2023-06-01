# La configuration en détails

Comme indiqué dans la page précédente, la majorité de la configuration est déjà définie et n'a pas besoin d'être modifiée à priori.

Cette page présente de manière exhaustive toutes les propriétés de configuration existante par section, cela est utile si jamais vous souhaitez avoir une utilisation avancée de ce module ou que les spécifications de l'API changent.

Le fichier de configuration par défaut utilisé est accessible ici : [ignf_gpf_api/_conf/default.ini](https://github.com/ignf-sidc/ignf-gpf-api/blob/prod/ignf_gpf_api/_conf/default.ini)

## Section `logging`

La première section concerne le logging de l'application.

| Paramètre   | Type | Défaut         | Description                                                   |
| ----------- | ---- | -------------- | ------------------------------------------------------------- |
| `log_level` | str  | INFO           | Niveau de log minimal pour afficher/sauvegarder les messages. |


## Section `store_authentification`

La deuxième section concerne l'authentification.

Cette partie de la configuration permet au module de vous authentifier et de récupérer un jeton pour utiliser l'API.

| Paramètre              | Type | Défaut         | Description                                                     |
| ---------------------- | ---- | -------------- | --------------------------------------------------------------- |
| `token_url`            | str  | URL officielle | URL du service d'authentification de la Géoplateforme. Elle n'est à priori pas à changer, sauf si vous utilisez un environnement particulier (test, qualification, ...). |
| `login`                | str  | `null`         | Indiquez ici le nom d’utilisateur du compte à utiliser.         |
| `password`             | str  | `null`         | Indiquez ici le mot de passe du compte à utiliser.              |
| `client_id`            | str  | `null`         | Indiquez ici le groupe d’appartenance du compte à utiliser.     |
| `nb_attempts`          | int  | 5              | Nombre de tentatives de récupération du jeton à effectuer en cas d'erreur avant de lever une erreur. |
| `sec_between_attempt`  | int  | 1              | Délai à attendre entre deux tentatives de récupération du jeton. |


## Section `store_api`

La troisième section concerne la connexion à l'entrepôt.

| Paramètre              | Type | Défaut         | Description                                                     |
| ---------------------- | ---- | -------------- | --------------------------------------------------------------- |
| `root_url `            | str  | URL officielle | URL racine de l'API Géoplateforme. Elle n'est à priori pas à changer, sauf si vous utilisez un environnement particulier (test, qualification, ...). |
| `datastore`            | str  | `null`         | Indiquez ici l'identifiant de l'entrepôt (`datastore`) à utiliser. |
| `root_datastore`       | str  | `${store_api:root_url}/datastores/${store_api:datastore}` | Chemin racine des routes permettant de faire des action sur cet entrepôt (`datastore`). |
| `client_id`            | str  | `null`         | Indiquez ici le groupe d’appartenance du compte à utiliser.     |
| `nb_attempts`          | int  | 5              | Nombre de requêtes à tenter en cas d'erreur avant de lever une erreur. |
| `sec_between_attempt`  | int  | 1              | Délai à attendre entre deux requêtes.                           |
| `nb_limit`             | int  | 10             | Nombre d'éléments à récupérer lors des requêtes de listing d'entités. |
| `regex_content_range`  | int  | `(?P<i_min>[0-9]+)-(?P<i_max>[0-9]+)/(?P<len>[0-9]+)` | Délai à attendre entre deux tentatives de récupération du jeton. |


## Section `routing`

Cette section concerne la définition des routes.

Chaque route permet de faire une action via l'API. Tous ces paramètres n'ont à priori pas à être modifiés, sauf changement des spécifications de l'API.

| Paramètre                            | Type | Défaut                                                  | Description                             |
| -------------------------------------| ---- | ------------------------------------------------------- | --------------------------------------- |
| **Routes concernant l'entité User** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }           |
| `user_get`                           | str  | `${store_api:root_url}/users/me`                        | Route pour récupérer les informations de l'utilisateur authentifié. |
| **Routes concernant l'entité Datastore** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }      |
| `datastore_get`                      | str  | `${store_api:root_datastore}`                           | Route pour récupérer les information d'un entrepôt (`datastore`). |
| **Routes concernant l'entité Upload** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }         |
| `upload_list`                        | str  | `${store_api:root_datastore}/uploads`                   | Route pour lister les livraisons (`uploads`) associées à un entrepôt. |
| `upload_create`                      | str  | `${routing:upload_list}`                                | Route pour créer une nouvelle livraison associé à un entrepôt. |
| `upload_get`                         | str  | `${routing:upload_list}/{upload}`                       | Route pour récupérer le détail d'une livraison. |
| `upload_delete`                      | str  | `${routing:upload_list}/{upload}`                       | Route pour supprimer une livraison. |
| `upload_add_tags`                    | str  | `${upload_get}/tags`                                    | Route pour ajouter/modifier les étiquette(s) d'une livraison. |
| `upload_delete_tags`                 | str  | `${upload_get}/tags`                                    | Route pour supprimer un (des) étiquette(s) d'une livraison. |
| `upload_push_data`                   | str  | `${upload_get}/data`                                    | Route pour téléverser des fichiers de données associés à une livraison. |
| `upload_delete_data`                 | str  | `${upload_push_data}`                                   | Route pour supprimer des fichiers de données associés à une livraison. |
| `upload_push_md5`                    | str  | `${upload_get}/md5`                                     | Route pour téléverser des fichiers de clefs md5 associés à une livraison. |
| `upload_delete_md5`                  | str  | `${upload_push_md5}`                                    | Route pour supprimer des fichiers de clefs md5 associés à une livraison. |
| `upload_close`                       | str  | `${upload_get}/close`                                   | Route pour fermer une livraison. |
| `upload_open`                        | str  | `${upload_get}/open`                                    | Route pour ouvrir une livraison. |
| `upload_tree`                        | str  | `${upload_get}/tree`                                    | Route pour récupérer l'arborescence des fichiers associés à une livraison. |
| `upload_list_checks`                 | str  | `${upload_get}/checks`                                  | Route pour lister les vérifications (checks) liées à une livraison. |
| `upload_run_checks`                  | str  | `${upload_get}/checks`                                  | Route pour ajouter une vérification à une livraison. |
| `upload_list_comment`                | str  | `${upload_get}/comments`                                | Route pour lister les commentaires associés à une livraison. |
| `upload_add_comment`                 | str  | `${upload_list_comment}`                                | Route pour ajouter un commentaire à une livraison. |
| `upload_edit_comment`                | str  | `${upload_list_comment}/{comment}`                      | Route pour modifier un commentaire associé à une livraison. |
| `upload_remove_comment`              | str  | `${upload_list_comment}/{comment}`                      | Route pour supprimer un commentaire associé à une livraison. |
| `upload_list_sharings`               | str  | `${upload_get}/sharings`                                | Route pour lister les partages (sharings) de cette livraison avec d'autres entrepôts. |
| `upload_add_sharing`                 | str  | `${upload_list_sharings}`                               | Route pour partager cette livraison avec d'autres entrepôts. |
| `upload_remove_sharing`              | str  | `${upload_list_sharings}`                               | Route pour supprimer des partages de cette livraison avec d'autres entrepôts. |
| `upload_list_events`                 | str  | `${upload_get}/events`                                  | Route pour lister les événements (event) ayant eu lieu en rapport avec cette livraison. |
| **Routes concernant l'entité StoredData** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }     |
| `stored_data_list`                   | str  | `${store_api:root_datastore}/stored_data`               | todo |
| `stored_data_get`                    | str  | `${stored_data_list}/{stored_data}`                     | todo |
| `stored_data_delete`                 | str  | `${stored_data_list}/{stored_data}`                     | todo |
| `stored_data_add_tags`               | str  | `${stored_data_get}/tags`                               | todo |
| `stored_data_delete_tags`            | str  | `${stored_data_get}/tags`                               | todo |
| `stored_data_list_comment`           | str  | `${stored_data_get}/comments`                           | todo |
| `stored_data_add_comment`            | str  | `${stored_data_list_comment}`                           | todo |
| `stored_data_edit_comment`           | str  | `${stored_data_list_comment}/{comment}`                 | todo |
| `stored_data_remove_comment`         | str  | `${stored_data_list_comment}/{comment}`                 | todo |
| `stored_data_list_sharings`          | str  | `${stored_data_get}/sharings`                           | todo |
| `stored_data_add_sharing`            | str  | `${stored_data_list_sharings}`                          | todo |
| `stored_data_remove_sharing`         | str  | `${stored_data_list_sharings}`                          | todo |
| `stored_data_list_events`            | str  | `${stored_data_get}/events`                             | todo |
| **Routes concernant l'entité Processing** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }     |
| `processing_list`                    | str  | `${store_api:root_datastore}/processings`               | todo |
| `processing_get`                     | str  | `${processing_list}/{processing}`                       | todo |
| **Routes concernant l'entité Processing** Execution {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn } |
| `processing_execution_list`          | str  | `${processing_list}/executions`                         | todo |
| `processing_execution_create`        | str  | `${processing_execution_list}`                          | todo |
| `processing_execution_get`           | str  | `${processing_execution_list}/{processing_execution}`   | todo |
| `processing_execution_delete`        | str  | `${processing_execution_get}`                           | todo |
| `processing_execution_launch`        | str  | `${processing_execution_get}/launch`                    | todo |
| `processing_execution_abort`         | str  | `${processing_execution_get}/abort`                     | todo |
| `processing_execution_logs`          | str  | `${processing_execution_get}/logs`                      | todo |
| **Routes concernant l'entité Configuration** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }  |
| `configuration_list`                 | str  | `${store_api:root_datastore}/configurations`            | todo |
| `configuration_get`                  | str  | `${configuration_list}/{configuration}`                 | todo |
| `configuration_create`               | str  | `${configuration_list}`                                 | todo |
| `configuration_delete`               | str  | `${configuration_get}`                                  | todo |
| `configuration_put`                  | str  | `${configuration_get}`                                  | todo |
| `configuration_add_tags`             | str  | `${configuration_get}/tags`                             | todo |
| `configuration_delete_tags`          | str  | `${configuration_get}/tags`                             | todo |
| `configuration_list_comment`         | str  | `${configuration_get}/comments`                         | todo |
| `configuration_add_comment`          | str  | `${configuration_list_comment}`                         | todo |
| `configuration_edit_comment`         | str  | `${configuration_list_comment}/{comment}`               | todo |
| `configuration_remove_comment`       | str  | `${configuration_list_comment}/{comment}`               | todo |
| `configuration_list_offerings`       | str  | `${configuration_get}/offerings`                        | todo |
| **Routes concernant l'entité Offering** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }       |
| `offering_list`                      | str  | `${store_api:root_datastore}/offerings`                 | todo |
| `offering_get`                       | str  | `${offering_list}/{offering}`                           | todo |
| `offering_create`                    | str  | `${configuration_list_offerings}`                       | todo |
| `offering_delete`                    | str  | `${offering_get}`                                       | todo |
| `offering_patch`                     | str  | `${offering_get}`                                       | todo |
| **Routes concernant l'entité Check** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn }          |
| `check_list`                         | str  | `${store_api:root_datastore}/checks`                    | todo |
| `check_get`                          | str  | `${routing:check_list}/{check}`                         | todo |
| **Routes concernant l'entité CheckExecution** {: colspan=4 } | &#8288 {: .dn }| &#8288 {: .dn }| &#8288 {: .dn } |
| `check_execution_list`               | str  | `${routing:check_list}/executions`                      | todo |
| `check_execution_get`                | str  | `${routing:check_execution_list}/{check_execution}`     | todo |
| `check_execution_delete`             | str  | `${routing:check_execution_list}/{check_execution}`     | todo |
| `check_execution_logs`               | str  | `${routing:check_execution_get}/logs`                   | todo |


## Section `upload`

Cette section concerne les paramètres de gestion des livraisons (`upload`).

| Paramètre                        | Type | Défaut      | Description                                                     |
| -------------------------------- | ---- | ----------- | --------------------------------------------------------------- |
| `uniqueness_constraint_infos `   | str  | `name`      | Attributs à considérer pour tester l'unicité d'une livraison.   |
| `uniqueness_constraint_tags`     | str  | `empty str` | Étiquettes à considérer pour tester l'unicité d'une livraison.  |
| `behavior_if_exists`             | str  | `STOP`      | Comportement à adopter si la livraison à créer existe déjà (`DELETE` : on la supprime et on la recrée, `CONTINUE` : on reprendre le téléversement, `STOP` : on lève une exception). |
| `md5_pattern`                    | str  | `{md5_key}  data/{file_path}` | Modèle des fichiers de clés md5 à livrer.     |
| `push_data_file_key`             | int  | `filename`  | Nom de la clé pour téléverser des fichiers de données.          |
| `push_md5_file_key`              | int  | `filename`  | Nom de la clé pour téléverser des fichiers de clé md5.          |
| `nb_sec_between_check_updates`   | int  | 10          | Nombre de secondes entre deux mises à jour du statut de la livraison lors des vérifications. |
| `check_message_pattern`          | int  | `Vérifications : {nb_asked} en attente, {nb_in_progress} en cours, {nb_failed} en échec, {nb_passed} en succès` | Modèle du message à afficher pendant la vérification d'une livraison. |
| `open_status`                    | int  | `OPEN`      | Constante représentant le statut ouvert d'une livraison.        |
| `close_status`                   | int  | `CLOSE`     | Constante représentant le statut fermer d'une livraison.        |


## Section `processing_execution`

Cette section concerne les paramètres de gestion des exécutions de traitement (`processing_execution`).

| Paramètre                        | Type | Défaut      | Description                                                     |
| -------------------------------- | ---- | ----------- | --------------------------------------------------------------- |
| `nb_sec_between_check_updates`   | int  | 10          | Nombre de secondes entre deux mises à jour du statut de l'exécution des vérifications. |
| `uniqueness_constraint_infos `   | str  | `name`      | Attributs à considérer pour tester l'unicité d'une entité en sortie de l'exécution de traitement (livraison ou donnée stockée).   |
| `uniqueness_constraint_tags`     | str  | `empty str` | Étiquettes à considérer pour tester l'unicité d'une entité en sortie de l'exécution de traitement (livraison ou donnée stockée).  |
| `behavior_if_exists`             | str  | `STOP`      | Comportement à adopter si l'entité en sortie de l'exécution de traitement (livraison ou donnée stockée) existe déjà (`DELETE` : on la supprime et on la recrée, `STOP` : on lève une exception). |


## Section `configuration`

Cette section concerne les paramètres de gestion des configurations (`configuration`).

| Paramètre                        | Type | Défaut      | Description                                                        |
| -------------------------------- | ---- | ----------- | ------------------------------------------------------------------ |
| `uniqueness_constraint_infos `   | str  | `name`      | Attributs à considérer pour tester l'unicité de la configuration.  |
| `uniqueness_constraint_tags`     | str  | `empty str` | Étiquettes à considérer pour tester l'unicité de la configuration. |


## Section `miscellaneous`

Cette section concerne les paramètres divers.

| Paramètre                  | Type | Défaut            | Description                                                               |
| -------------------------- | ---- | ----------------- | ------------------------------------------------------------------------- |
| `data_directory_on_store ` | str  | `name;layer_name` | Préfixe des fichiers de données téléversés sur une livraison.             |
| `tmp_workdir`              | str  | `empty str`       | Répertoire local et existant permettant d'écrire des données temporaires. |


## Section `workflow_resolution_regex`

Cette section concerne la configuration des expression régulières (regex) permettant de résoudre des workflows.

Ces regex vont être notamment utilisées par les résolveurs (`resolver`) (cf. la classe Python `ignf_gpf_api.workflow.resolver.AbstractResolver`).

### Option `filter_infos`

Configuration de la manière de récupérer les filtres sur les attributs (infos) afin de résoudre une entité.
La chaîne capturée doit être nommée `filter_infos`.

* Type : str
* Valeur par défaut : `((\s*)INFOS(\s*)\((?P<filter_infos>.*?)\)(\s*))?`

### Option `filter_tags`

Configuration de la manière de récupérer les filtres sur les étiquettes (tags) afin de résoudre une entité.
La chaîne capturée doit être nommée `filter_tags`.

* Type : str
* Valeur par défaut : `((\s*)TAGS(\s*)\((?P<filter_tags>.*?)\)(\s*))?`

### Option `filter`

Configuration de la manière de récupérer les filtres sur les attributs et les étiquettes afin de résoudre une entité.

* Type : str
* Valeur par défaut : `((\s*)\[${filter_infos},?${filter_tags}\])`

Les chaînes capturées doivent respectivement être nommées `filter_infos` et `filter_tags` et sont ensuite traitées
par les regex configurées dans les options `filter_infos` et `filter_tags`.

### Option `store_entity_regex`

Configuration de la regex de résolution une entité.

* Type : str
* Valeur par défaut : `(?P<entity_type>(upload|stored_data|processing_execution|offering|processing|configuration|endpoint))\.(?P<selected_field_type>(tags|infos))\.(?P<selected_field>\w*)${filter}`

Les chaînes capturées doivent être nommées :

* `entity_type` : pour la chaîne récupérant le type de l'entité à résoudre (`upload`, `stored_data`, ...) ;
* `selected_field_type` : pour la chaîne récupérant le type de champ à renvoyer (attribut `infos` ou étiquette `tags`) ;
* `selected_field` : pour la chaîne récupérant le champ à renvoyer (`_id_`, `name`, ...) ;
* `filter_infos` : pour la chaîne récupérant les critères de filtre sur les attributs (dans la config par défaut, cela est délégué à l'option `filter`) ;
* `filter_tags` : pour la chaîne récupérant les critères de filtre sur les étiquettes (dans la config par défaut, cela est délégué à l'option `filter`).

### Option `global_regex`

Configuration de la regex de détection de l'appel à un résolveur.

* Type : str
* Valeur par défaut : `(?P<param>{(?P<resolver_name>[a-z_]+)\.(?P<to_solve>.*)})`

Les chaînes capturées doivent être nommées :

* `param` : pour la chaîne complète ;
* `resolver_name` : pour la chaîne donnant le nom du résolveur à appeler ;
* `to_solve` : pour la chaîne donnant la chaîne à résoudre.

### Option `file_regex`

Configuration de la regex du résolveur de fichier (classe `ignf_gpf_api.workflow.resolver.FileResolver`).

* Type : str
* Valeur par défaut : `(?P<resolver_type>str|list|dict)\((?P<resolver_file>.*)\)`

Les chaînes capturées doivent être nommées :

* `resolver_type` : pour la chaîne donnant le type de fichier à résoudre (`str`, `list` ou `dict`) ;
* `resolver_file` : pour la chaîne donnant le chemin du fichier à résoudre.


## Section `json_converter`

Cette section concerne les paramètres de conversion en JSON des types non gérés de base par Python.

| Paramètre            | Type | Défaut               | Description                                    |
| -------------------- | ---- | -------------------- | ---------------------------------------------- |
| `datetime_pattern `  | str  | `%Y-%m-%dT%H:%M:%S`  | Modèle de formatage des `datetime` en string.  |
| `date_pattern`       | str  | `%Y-%m-%d`           | Modèle de formatage des `date` en string.      |
| `time_pattern`       | str  | `%H:%M:%S`           | Modèle de formatage des `time` en string.      |


## Section `json_schemas`

Cette section concerne le paramétrage des schémas JSON utilisés. Par défaut, les chemins sont définis relativement à `ignf_gpf_api/_conf`, mais peuvent également être absolus.

| Paramètre          | Type | Défaut                                     | Description                                                                    |
| ------------------ | ---- | ------------------------------------------ | ------------------------------------------------------------------------------ |
| `descriptor_file ` | str  | `json_schemas/upload_descriptor_file.json` | Chemin vers le schéma JSON définissant les fichiers descripteurs de livraison. |
| `workflow_config`  | str  | `json_schemas/workflow_config.json`        | Chemin vers le schéma JSON définissant les fichiers workflow.                  |
