"""
invalid_records_visualization.py

Visualize invalid records report.
"""

import pandas as pd
import matplotlib.pyplot as plt

from config.config import Config

import warnings
warnings.filterwarnings("ignore")
from src.logger import logger


def visualize_invalid_records():


    df = pd.read_csv(
        Config.INVALID_RECORDS_REPORT
    )

    if df.empty:
        return

    summary = (

        df["error_reason"]

        .value_counts()

        .reset_index()
    )

    summary.columns = [

        "error_reason",

        "count"
    ]

    total_invalid = (
        summary["count"].sum()
    )

    summary["percentage"] = (

        summary["count"]

        / total_invalid

        * 100
    )

    summary = summary.sort_values(
        "count",
        ascending=True
    )

    # =====================================
    # CHART 1
    # HORIZONTAL BAR
    # =====================================

    plt.figure(
        figsize=(14, 8)
    )

    bars = plt.barh(

        summary["error_reason"],

        summary["count"]
    )

    for bar, count, pct in zip(

            bars,

            summary["count"],

            summary["percentage"]
    ):

        plt.text(

            bar.get_width() + 10,

            bar.get_y() +
            bar.get_height() / 2,

            f"{count:,} ({pct:.1f}%)",

            va="center"
        )

    plt.title(

        f"Invalid Records Analysis\n"

        f"Total Invalid Records: "
        f"{total_invalid:,}"
    )

    plt.xlabel(
        "Record Count"
    )

    plt.ylabel(
        "Error Type"
    )



    plt.tight_layout()

    plt.savefig(

        Config.CHARTS_DIR /

        "invalid_records_analysis.png",

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()

    logger.info(
        "Invalid records analysis chart generated."
    )

def data_quality_summary():

    import matplotlib.pyplot as plt

    categories = [

        "Departments",

        "Employees",

        "Attendance"
    ]

    extracted = [

        20,

        1100,

        15000
    ]

    valid = [

        19,

        789,

        9193
    ]

    invalid = [

        1,

        311,

        5807
    ]

    x = range(
        len(categories)
    )

    width = 0.25

    plt.figure(
        figsize=(14, 8)
    )

    extracted_bars = plt.bar(

        [i - width for i in x],

        extracted,

        width,

        label="Extracted"
    )

    valid_bars = plt.bar(

        x,

        valid,

        width,

        label="Valid"
    )

    invalid_bars = plt.bar(

        [i + width for i in x],

        invalid,

        width,

        label="Invalid"
    )

    # =====================================
    # ADD VALUES ON TOP OF BARS
    # =====================================

    for bars in [

        extracted_bars,

        valid_bars,

        invalid_bars

    ]:

        for bar in bars:

            plt.text(

                bar.get_x()
                + bar.get_width() / 2,

                bar.get_height(),

                f"{int(bar.get_height()):,}",

                ha="center",

                va="bottom",

                fontsize=9,

                fontweight="bold"
            )

    plt.xticks(

        list(x),

        categories
    )

    plt.ylabel(
        "Record Count"
    )

    plt.xlabel(
        "Data Source"
    )

    plt.title(

        "Data Quality Summary\n"
        "Extracted vs Valid vs Invalid Records",

        fontsize=14,

        fontweight="bold"
    )

    plt.legend()

    plt.grid(

        axis="y",

        linestyle="--",

        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(

        Config.CHARTS_DIR /

        "data_quality_summary.png",

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()

    logger.info(
        "Data quality summary chart generated."
    )