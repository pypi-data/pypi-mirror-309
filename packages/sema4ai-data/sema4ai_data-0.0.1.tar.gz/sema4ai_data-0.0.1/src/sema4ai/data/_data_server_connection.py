import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from sema4ai.data._result_set import ResultSet


class _MySqlConnectionWrapper:
    def __init__(
        self, host: str, port: int, user: Optional[str], password: Optional[str]
    ):
        import pymysql

        # Handle situation with e.g. localhost connections without login/passwd
        try:
            kwargs: dict[str, typing.Any] = {}

            assert host is not None
            assert port is not None

            kwargs["host"] = host
            kwargs["port"] = port
            if user:
                kwargs["user"] = user
            if password:
                kwargs["password"] = password

            self._base_kwargs = kwargs
        except Exception:
            raise Exception(
                f"Failed to connect to the data server mysql api with host: {host} and port: {port}"
            )
        self._connection_pool: dict[str, pymysql.connections.Connection] = {}

    def connection_for_database(self, database_name: str):
        """
        Returns a connection to the database.
        """

        # TODO: Can we use self._connection.select_db(database_name) instead
        # of creating a new connection for each database?
        # Need to check if we can open go to the "global" namespace in this case
        # (or maybe we can have one for global and one for database specific).

        import pymysql

        if database_name not in self._connection_pool:
            self._connection_pool[database_name] = pymysql.connect(
                **self._base_kwargs, database=database_name
            )

        return self._connection_pool[database_name]


class DataServerConnection:
    def __init__(
        self,
        http_url: str,
        http_user: Optional[str],
        http_password: Optional[str],
        mysql_host: str,
        mysql_port: int,
        mysql_user: Optional[str],
        mysql_password: Optional[str],
    ):
        """
        Creates a connection to the data server.
        """
        self._mysql_connection = _MySqlConnectionWrapper(
            mysql_host, mysql_port, mysql_user, mysql_password
        )

    def query(
        self,
        database_name: str,
        query: str,
        params: Optional[dict[str, str | int | float] | list[str | int | float]] = None,
    ) -> "ResultSet":
        """
        Simple API to query a database in MindsDB with parameters. Always loads
        all the results into memory.

        Args:
            database_name: The name of the database to query.
            query: The SQL query to execute.
            params: A list of parameters to inject into the query.

        Returns:
            ResultSet: The query result as a ResultSet.
        """
        from sema4ai.data._result_set import ResultSet
        from sema4ai.data._sql_handling import (
            build_query_from_dict_params,
            build_query_from_list_params,
        )

        if isinstance(params, list):
            query = build_query_from_list_params(query, params)
        else:
            query = build_query_from_dict_params(query, params)

        connection = self._mysql_connection.connection_for_database(database_name)
        with connection.cursor() as cursor:
            cursor.execute(query)
            return ResultSet(cursor)

    # It's actually the same thing internally, so we can just alias it.
    predict = query
