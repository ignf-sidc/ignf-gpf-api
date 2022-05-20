from ignf_gpf_api.action.ActionAbstract import ActionAbstract


class ConfigurationAction(ActionAbstract):
    """classe dédiée aux Configuration"""

    def run(self) -> None:
        raise NotImplementedError()
