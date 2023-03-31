from typing import Any, Callable


class PrintLogHelper:
    """Classe d'aide pour gérer l'affichage d'un log se complétant au fur et à mesure."""

    log = ""

    @staticmethod
    def reset() -> Any:
        """Reset le log"""
        PrintLogHelper.log = ""

    @staticmethod
    def print(full_log: str, print_fct: Callable[[object], None] = print) -> None:
        """Affiche le nouveau log en utilisant la fonction indiquée.

        Args:
            full_log (str): log entier
            print_fct (Callable[[object], None], optional): Fonction d'affichage à utiliser.

        Returns:
            Any: _description_
        """
        s_old_log = PrintLogHelper.log
        s_new_log = full_log.replace(s_old_log, "")
        s_new_log = s_new_log[1:] if s_new_log.startswith("\n") else s_new_log
        PrintLogHelper.log = full_log
        if s_new_log != "":
            print_fct(s_new_log)
