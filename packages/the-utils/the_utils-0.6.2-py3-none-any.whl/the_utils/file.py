"""File Management.
"""

import csv
import os
from pathlib import Path
from pathlib import PurePath
from typing import Any
from typing import List
from typing import Union

import pandas as pd


def csv_to_table(
    raw_path: str,
    save_path: str,
    row_key: str,
    col_key: str,
    val_key: str,
    fillna: Union[float, str] = None,
    row_order: List[str] = None,
    col_order: List[str] = None,
    average_rank: bool = True,
    bold_max: bool = True,
) -> pd.DataFrame:
    """Transfer a csv into table.

    Args:
        raw_path (str): raw csv path.
        save_path (str): path to save the table.
        row_key (str): key for row index.
        col_key (str): key for column index.
        val_key (str): key for value index.
        fillna (Union[float, str], optional): fill empty cell with the value given. \
            Defaults to None.
        row_order (List[str], optional): sort the rows with given order list. Defaults to None.
        col_order (List[str], optional): sort the columns with given order list. Defaults to None.
        average_rank (bool, optional): whether to add a column with average ranks. Defaults to True.
        bold_max (bool, optional): whether to wrap the maximum value of each column \
            with `**value**`. Defaults to True.

    Returns:
        pd.DataFrame: table.
    """
    pivot_df = pd.read_csv(raw_path).pivot(
        index=row_key,
        columns=col_key,
        values=val_key,
    )

    if fillna is not None:
        pivot_df = pivot_df.fillna(fillna)
    if row_order is not None:
        pivot_df = pivot_df.reindex(row_order)
    if col_order is not None:
        pivot_df = pivot_df[col_order]
    if average_rank:
        AR = "Avg. Rank"
        ranks_df = pivot_df.applymap(
            lambda x: pd.to_numeric(
                f"{x}".split("±")[0],
                errors="coerce",
            )
        ).rank(
            axis=0,
            method="min",
            ascending=False,
        )
        pivot_df[AR] = ranks_df.mean(axis=1).apply(lambda x: float(f"{x:.2f}"))

    if bold_max:
        for col in pivot_df.columns:
            # Parse numeric values for comparison
            numeric_values = pivot_df[col].apply(
                lambda x: pd.to_numeric(str(x).split("±")[0], errors="coerce")
            )
            if numeric_values.notna().any():
                chosen = (
                    numeric_values.min() if average_rank and col == AR else numeric_values.max()
                )
                pivot_df[col] = pivot_df[col].apply(
                    lambda x: (
                        f"**{x}**"
                        if pd.to_numeric(str(x).split("±")[0], errors="coerce") == chosen else x
                    )
                )

    pivot_df.to_csv(save_path)
    return pivot_df


def make_parent_dirs(target_path: PurePath) -> None:
    """make all the parent dirs of the target path.

    Args:
        target_path (PurePath): target path.
    """
    if not target_path.parent.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)


def refresh_file(target_path: str = None) -> None:
    """clear target path

    Args:
        target_path (str): file path
    """
    if target_path is not None:
        target_path: PurePath = Path(target_path)
        if target_path.exists():
            target_path.unlink()

        make_parent_dirs(target_path)
        target_path.touch()


def csv2file(
    target_path: str,
    thead: List[str] = None,
    tbody: List[Any] = None,
    refresh: bool = False,
    is_dict_list: bool = False,
    sort_head: bool = False,
) -> None:
    """save data to target_path of a csv file.

    Args:
        target_path (str): target path
        thead (List[str], optional): csv table header, only written into the file when\
            it is not None and file is empty. Defaults to None.
        tbody (List, optional): csv table content. Defaults to None.
        refresh (bool, optional): whether to clean the file first. Defaults to False.
        is_dict_list (bool, optional): whether the tbody is in the format of a list of dicts. \
            Defaults to False.
        sort_head (bool, optional): whether to sort the head with lowercase before writing. \
            Defaults to False.

    Example:
        .. code-block:: python

            from the_utils import csv2file
            save_file = "./results/example.csv"
            final_params = {
                "dataset": "cora",
                "acc": "99.1",
                "NMI": "89.0",
            }
            thead=[]
            # list of values
            csv2file(
                target_path=save_file,
                thead=list(final_params.keys()),
                tbody=list(final_params.values()),
                refresh=False,
                is_dict_list=False,
            )
            # list of dicts
            csv2file(
                target_path=save_file,
                tbody=[
                    {
                        "a": 1,
                        "b": 2
                    },
                    {
                        "a": 2,
                        "b": 1
                    },
                ],
                is_dict_list=True,
            )
    """
    target_path: PurePath = Path(target_path)
    if refresh:
        refresh_file(target_path)

    make_parent_dirs(target_path)

    with open(target_path, "a+", newline="", encoding="utf-8") as csvfile:
        csv_write = csv.writer(csvfile)
        if tbody is not None:
            if is_dict_list:
                if sort_head:
                    keys = sorted([h.lower() for h in list(tbody[0].keys())])
                    if os.stat(target_path).st_size == 0:
                        csv_write.writerow(keys)
                    tbody = [{k: b[k] for k in keys} for b in tbody]
                else:
                    if os.stat(target_path).st_size == 0:
                        keys = list(tbody[0].keys())
                        csv_write.writerow(keys)

                dict_writer = csv.DictWriter(
                    csvfile,
                    fieldnames=tbody[0].keys(),
                )
                for elem in tbody:
                    dict_writer.writerow(elem)
            else:
                if thead is not None:
                    if sort_head:
                        thead, tbody = list(
                            zip(*sorted(zip(thead, tbody), key=lambda x: x[0].lower()))
                        )
                    if os.stat(target_path).st_size == 0:
                        csv_write.writerow(thead)
                csv_write.writerow(tbody)


def save_to_csv_files(
    results: dict,
    csv_name: str,
    insert_info: dict = None,
    append_info: dict = None,
    save_path="./results",
    sort_head: bool = False,
) -> None:
    """Save the evaluation results to a local csv file.

    Args:
        results (dict): Evaluation results document.
        csv_name (str): csv file name to store.
        insert_info (dict): Insert information in front of the results. Defaults to None.
        append_info (dict): Append information after the results. Defaults to None.
        save_path (str, optional): Folder path to store. Defaults to './results'.
        sort_head (bool, optional): whether to sort the head before writing. Defaults to False.

    Example:
        .. code-block:: python

            from the_utils import evaluate_from_embed_file
            from the_utils import save_to_csv_files

            method_name='orderedgnn'
            data_name='texas'

            clustering_res, classification_res = evaluate_from_embed_file(
                f'{data_name}_{method_name}_embeds.pth',
                f'{data_name}_data.pth',
                save_path='./save/',
            )

            insert_info = {'data': data_name, 'method': method_name,}
            save_to_csv_files(clustering_res, insert_info, 'clutering.csv')
            save_to_csv_files(classification_res, insert_info, 'classification.csv')
    """
    # save to csv file
    results = {
        **(insert_info or {}),
        **results,
        **(append_info or {}),
    }

    # list of values
    csv2file(
        target_path=os.path.join(save_path, csv_name),
        thead=list(results.keys()),
        tbody=list(results.values()),
        refresh=False,
        is_dict_list=False,
        sort_head=sort_head,
    )
