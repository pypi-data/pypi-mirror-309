from typing import Any, Callable, Optional, overload

from ._data_server_connection import DataServerConnection
from ._data_source import DataSource
from ._data_source_spec import DataSourceSpec
from ._result_set import ResultSet

__version__ = "0.0.1"
version_info = [int(x) for x in __version__.split(".")]


@overload
def query(func: Callable) -> Callable:
    ...


@overload
def query(
    *, is_consequential: Optional[bool] = None, display_name: Optional[str] = None
) -> Callable:
    ...


def query(*args, **kwargs):
    """
    Decorator for queries which can be executed by `sema4ai.actions`.

    i.e.:

    If a file such as actions.py has the contents below:

    ```python
    from sema4ai.data import query

    @query
    def query_invoices(date: str, datasource: DataSource[Literal["invoices-datasource"]]) -> list[str]:
        ...
    ```

    Note that a query needs sema4ai actions to be executed.
    The command line to execute it is:

    python -m sema4ai.actions run actions.py -a query_invoices

    Args:
        func: A function which is a query to `sema4ai.data`.
        is_consequential: Whether the action is consequential or not.
            This will add `x-openai-isConsequential: true` to the action
            metadata and shown in OpenApi spec.
        display_name: A name to be displayed for this action.
            If given will be used as the openapi.json summary for this action.
    """
    from sema4ai.actions import action

    kwargs["kind"] = "query"
    return action(*args, **kwargs)


@overload
def predict(
    *, is_consequential: Optional[bool] = None, display_name: Optional[str] = None
) -> Callable:
    ...


@overload
def predict(func: Callable) -> Callable:
    ...


def predict(*args, **kwargs):
    """
    Decorator for predictions based on data models which can be executed by `sema4ai.actions`.

    i.e.:

    If a file such as actions.py has the contents below:

    ```python
    from sema4ai.data import predict

    @predict
    def cashflow_prediction(scenario: str, datasource: DataSource[Literal["reports-datasource"]]) -> list[str]:
        ...
    ```

    Note that a prediction needs sema4ai actions to be executed.
    The command line to execute it is:

    python -m sema4ai.actions run actions.py -a cashflow_prediction

    Args:
        func: A function which is a prediction to `sema4ai.data`.
        is_consequential: Whether the action is consequential or not.
            This will add `x-openai-isConsequential: true` to the action
            metadata and shown in OpenApi spec.
        display_name: A name to be displayed for this action.
            If given will be used as the openapi.json summary for this action.
    """
    from sema4ai.actions import action

    kwargs["kind"] = "predict"
    return action(*args, **kwargs)


def metadata() -> dict:
    """
    Returns something like this:
    {
        // This is added by sema4ai-data
        'data-spec-version': 'v1',
        'data': {
            'datasources': [
                {
                    'name': 'datasource-name',
                    'engine': 'sqlite',
                    'description': 'description of the datasource',
                    'setup-sql': ['sql-to-execute'],
                    'defined-at': {
                        'file': 'path/to/definition_file.py',
                        'line': 123,
                    },

                    # Only for files engine
                    'file': 'path/to/definition_file.py',  # Relative to package root.
                    'created-table': 'name-of-created-table',

                    # Only if a model is created (prediction engine or custom engine)
                    'model-name': 'name-of-model',

                },
                ...
            ]
        },
    }
    """
    from sema4ai.data._data_source_spec import (
        _global_internal_data_server_datasources_spec_instances,
    )

    ret: dict[str, Any] = {}
    datasources: list[dict[str, Any]] = []
    for (
        dataserver_datasource_spec
    ) in _global_internal_data_server_datasources_spec_instances:
        datasources.append(dataserver_datasource_spec.get_metadata())

    ret["data"] = {"datasources": datasources}
    ret["data-spec-version"] = "v1"
    return ret


def get_connection() -> "DataServerConnection":
    from ._data_source import _ConnectionHolder

    return _ConnectionHolder.connection()


__all__ = [
    "query",
    "predict",
    "metadata",
    "DataSource",
    "ResultSet",
    "DataSourceSpec",
    "get_connection",
]
