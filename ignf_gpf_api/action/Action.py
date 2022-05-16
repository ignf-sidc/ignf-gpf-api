from typing import Any, Dict, Optional


class Action:
    """Classe représentant une action d'un workflow.

    Attributes :
        __workflow_name (str) : nom du workflow
        __definition_dict (Dict[str, Any]) : définition de l'action
        __parent_action (Action) : action parente
    """

    def __init__(self, workflow_name: str, definition_dict: Dict[str, Any], parent_action: Optional["Action"] = None) -> None:
        super().__init__()
        self.__workflow_name: str = workflow_name
        self.__definition_dict: Dict[str, Any] = definition_dict
        self.__parent_action: Optional["Action"] = parent_action

    @property
    def workflow_name(self) -> str:
        return self.__workflow_name

    @property
    def definition_dict(self) -> Dict[str, Any]:
        return self.__definition_dict

    @property
    def parent_action(self) -> Optional["Action"]:
        return self.__parent_action
