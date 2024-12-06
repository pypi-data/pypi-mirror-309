import typing
from typing import Any, Iterator

if typing.TYPE_CHECKING:
    import pandas as pd
    import pymysql.cursors


T = typing.TypeVar("T")


class ResultSet:
    def __init__(self, cursor: "pymysql.cursors.Cursor"):
        self._columns = [desc[0].lower() for desc in cursor.description]
        self._data = cursor.fetchall()

    def as_dataframe(self) -> "pd.DataFrame":
        """
        Converts the result set to a pandas DataFrame.
        """
        import pandas as pd

        return pd.DataFrame(self._data, columns=self._columns)

    def _iter_as_dicts(self) -> Iterator[dict[str, Any]]:
        """
        Iterates over the result set as a list of dictionaries.
        """
        for row in self._data:
            yield dict(zip(self._columns, row))

    def build_list(self, item_class: type[T]) -> list[T]:
        """
        Builds a list of objects of the given class from the result set.

        Args:
            item_class: The class to build the list of.

        Returns:
            A list of objects of the given class.

        Note: The class must have a constructor that accepts each item in the
        result set as keyword arguments.
        """
        return [item_class(**row) for row in self._iter_as_dicts()]

    def to_markdown(self) -> str:
        """
        Converts the result set to a markdown table.
        """
        return self.as_dataframe().to_markdown()
