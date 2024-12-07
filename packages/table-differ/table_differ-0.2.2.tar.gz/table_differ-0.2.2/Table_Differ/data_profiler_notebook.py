#! /usr/bin/env python3

# long-help
"""
Intention here is that this can be imported into a notebook and provides reporting back
"""

# BUILT-INS
import logging

# THIRD PARTY
from rich import print as rprint

# PERSONAL
from Table_Differ.modules.pydantic_models import DataProfileArgs


class DataProfiler:
    def __init__(self, conn, args):
        rprint("[bold red blink]START RUN")
        self.conn = conn
        self.args = self.get_args(args)

        self.create_data_profile()

    def get_args(self, args):
        try:
            args = DataProfileArgs(**args)
        except ValidationError as e:
            rprint(e)
        logging.info(args)
        return args

    def create_data_profile(self) -> dict:
        assert self.conn
        cols = self.conn.sql(
            f"DESCRIBE {self.args.table_catalog}.{self.args.table_schema}.{self.args.table_name}"
        )
        col_list = [row.col_name for row in cols.select("col_name").collect()]

        result_dict = {
            "SUM": {},
            "MIN": {},
            "MAX": {},
            "AVG": {},
            "UNIQUENESS": {},
            "NULL_PERC": {},
        }

        for field in result_dict:
            select_clause = ""
            where_clause = ""
            for col in col_list:
                comma = ","
                if col == col_list[-1]:
                    comma = ""

                if field == "NULL_PERC":
                    select_clause += f"\n100.0 * SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) / COUNT(*) AS {col}{comma}"
                elif field == "UNIQUENESS":
                    select_clause += (
                        f"\n( COUNT({col}) / COUNT(DISTINCT {col}) ) as {col}{comma}"
                    )
                else:
                    select_clause += f" {field}({col}) as {col}{comma}"

            query = f"""
                SELECT
                    {select_clause}
                FROM
                    {self.args.table_catalog}.{self.args.table_schema}.{self.args.table_name}
                {where_clause}
                """
            result_dict[field]["result"] = self.conn.sql(query).collect()
            result_dict[field]["query"] = query

        for field in result_dict:
            rprint(
                f"\n[bold red]{field}",
                "\n",
                result_dict[field]["query"],
                "\n",
                result_dict[field]["result"],
            )
