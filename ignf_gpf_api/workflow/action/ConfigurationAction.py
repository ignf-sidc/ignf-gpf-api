from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract


class ConfigurationAction(ActionAbstract):
    """classe dédiée aux Configuration"""

    def run(self) -> None:
        raise NotImplementedError()
