""" Export Quran """

import os
import sqlite3
from pathlib import Path
from typing import Annotated, Optional
import pandas as pd
import typer
from rich import print

from quran_cli import DataFormat


def export(
    database: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Database name"),
    ],
    output: Annotated[
        Optional[Path],
        typer.Option(
            "-o", "--output", file_okay=False, dir_okay=True, help="Output folder"
        ),
    ] = Path("quran"),
    format: Annotated[
        Optional[DataFormat],
        typer.Option("-f", "--format", help="Export format."),
    ] = DataFormat.JSON,
) -> None:
    """
    Export Quran data to csv, json, xml format.

    Args:
        database (Path): Database filename.
        output (Path, optional): Output folder.
        format (str, optional): Export format.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3

    # Normalize initial database
    quran-cli normalize db.sqlite3

    # Export normalized database
    quran-cli export db.sqlite3 -f json
    ```
    """

    try:
        connection = sqlite3.connect(database.name)
        os.makedirs(output, exist_ok=True)

        tables = [
            "chapters",
            "parts",
            "groups",
            "quarters",
            "pages",
            "verses",
            "al_quran",
        ]

        for table in tables:
            print(f"Exporting [bold]{table}[/bold] table...", end=" ")
            data = pd.read_sql(sql=f'SELECT * FROM "{table}"', con=connection)

            filename = os.path.join(output.name, table)

            match format:
                case "csv":
                    with open(
                        f"{filename}.csv",
                        mode="w",
                        encoding="utf-8",
                    ) as file:
                        data.to_csv(file, index=False)

                case "json":
                    with open(
                        f"{filename}.json",
                        mode="w",
                        encoding="utf-8",
                    ) as file:
                        data.to_json(
                            file,
                            orient="records",
                            indent=2,
                            force_ascii=False,
                        )

                case "xml":
                    with open(
                        f"{filename}.xml",
                        mode="w",
                        encoding="utf-8",
                    ) as file:
                        data.to_xml(file)

            print("[bold green]Done[/bold green]")

        connection.close()

        print(
            f"Export to [bold yellow]{format.value}[/bold yellow] completed [bold green]successfully[/bold green]."
        )

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
