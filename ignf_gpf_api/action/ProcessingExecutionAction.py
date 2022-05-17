from ignf_gpf_api.action.ActionAbstract import ActionAbstract


class ProcessingExecutionAction(ActionAbstract):
    """classe dédiée aux processing execution"""

    def run(self) -> None:
        raise NotImplementedError()
