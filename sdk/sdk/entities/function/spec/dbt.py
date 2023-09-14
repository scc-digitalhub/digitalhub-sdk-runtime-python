"""
DBT Function specification module.
"""
from sdk.entities.function.spec.base import FunctionSpec
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import decode_string, encode_string


class FunctionSpecDBT(FunctionSpec):
    """
    Specification for a Function DBT.
    """

    def __init__(
        self,
        source: str = "",
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        sql: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        sql : str
            SQL query to run inside DBT.
        """
        super().__init__(source, image, tag, handler, command, **kwargs)
        if sql is None:
            raise EntityError("SQL query must be provided.")

        try:
            sql = decode_string(sql)
        except Exception:
            pass
        self.sql = encode_string(sql)
