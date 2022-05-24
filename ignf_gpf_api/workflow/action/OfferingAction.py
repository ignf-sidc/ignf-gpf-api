from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract


class OfferingAction(ActionAbstract):
    """classe dédiée aux Offering"""

    def run(self) -> None:
        raise NotImplementedError()
