from __future__ import annotations

from io import BytesIO
from typing import Any

import pandas as pd
from digitalhub_data.readers.objects.base import DataframeReader
from digitalhub_data.utils.data_utils import build_data_preview, get_data_preview


class DataframeReaderPandas(DataframeReader):
    """
    Pandas reader class.
    """

    ###################################
    # Read methods
    ###################################

    @staticmethod
    def read_df(path: str, extension: str, **kwargs) -> pd.DataFrame:
        """
        Read DataFrame from path.

        Parameters
        ----------
        path : str
            Path to read DataFrame from.
        extension : str
            Extension of the file.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame.
        """
        if extension == "csv":
            return pd.read_csv(path, **kwargs)
        return pd.read_parquet(path, **kwargs)

    ###################################
    # Write methods
    ###################################

    def write_df(self, df: pd.DataFrame, dst: str | BytesIO, extension: str | None = None, **kwargs) -> None:
        """
        Write DataFrame as parquet.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str | BytesIO
            The destination of the dataframe.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        None
        """
        if extension == "csv":
            return self.write_csv(df, dst, **kwargs)
        self.write_parquet(df, dst, **kwargs)

    @staticmethod
    def write_csv(df: pd.DataFrame, dst: str | BytesIO, **kwargs) -> None:
        """
        Write DataFrame as csv.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str | BytesIO
            The destination of the dataframe.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        None
        """
        df.to_csv(dst, index=False, **kwargs)

    @staticmethod
    def write_parquet(df: pd.DataFrame, dst: str | BytesIO, **kwargs) -> None:
        """
        Write DataFrame as parquet.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str | BytesIO
            The destination of the dataframe.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        None
        """
        df.to_parquet(dst, index=False, **kwargs)

    @staticmethod
    def write_table(df: pd.DataFrame, table: str, engine: Any, schema: str, **kwargs) -> None:
        """
        Write DataFrame as table.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        table : str
            The destination table.
        engine : Any
            The SQLAlchemy engine.
        schema : str
            The destination schema.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        None
        """
        df.to_sql(table, engine, schema=schema, index=False, **kwargs)

    ###################################
    # Utils
    ###################################

    @staticmethod
    def get_schema(df: pd.DataFrame) -> Any:
        """
        Get schema.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe.

        Returns
        -------
        Any
            The schema.
        """
        schema = {"fields": []}

        for column_name, dtype in df.dtypes.items():
            field = {"name": column_name, "type": ""}

            if pd.api.types.is_integer_dtype(dtype):
                field["type"] = "integer"
            elif pd.api.types.is_float_dtype(dtype):
                field["type"] = "number"
            elif pd.api.types.is_bool_dtype(dtype):
                field["type"] = "boolean"
            elif pd.api.types.is_string_dtype(dtype):
                field["type"] = "string"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                field["type"] = "datetime"
            else:
                field["type"] = "any"

            schema["fields"].append(field)

        return schema

    @staticmethod
    def get_preview(df: pd.DataFrame) -> Any:
        """
        Get preview.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe.

        Returns
        -------
        Any
            The preview.
        """
        columns = df.columns.tolist()
        head = df.head(10).values.tolist()
        preview = get_data_preview(columns, head)
        len_df = len(df)
        return build_data_preview(preview, len_df)
