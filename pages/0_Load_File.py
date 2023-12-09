# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import numpy as np
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code


def load_file() -> None:

    upload_data = st.file_uploader(
        "Bank / Credit Card Spreadsheet", type=["csv", "xls", "xlsx", "xlsm"]
    )

    if upload_data is None:
        st.info(
            "No File uploaded. Using example data from a [Kaggle Dataset](https://www.kaggle.com/datasets/apoorvwatsky/bank-transaction-data). Upload a CSV to use your own data!"
        )
        upload_data = open("data/bank.xlsx", mode="rb")
        separator = ","
        use_sample = True
    else:
        separator = st.text_input(
            "CSV Delimiter",
            value=",",
            max_chars=1,
            help="How your CSV values are separated (doesn't matter for excel)",
        )
        use_sample = False


   # @st.cache_data
    def read_csv_or_excel(data, sep):
        try:
            raw_df = pd.read_csv(data, sep=sep)
        except UnicodeDecodeError:
            try:
                raw_df = pd.read_excel(data)
            except Exception as e:
                raise e
        return raw_df


    raw_df = read_csv_or_excel(upload_data, separator)
    with st.expander("Show Raw Data"):
        st.json(raw_df.iloc[:100].to_json())

    columns = list(raw_df.columns)
    with st.expander("Show all columns"):
        st.write(" | ".join(columns))

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


st.set_page_config(page_title="Load file", page_icon="📹")
st.markdown("# Load file")
st.sidebar.header("Load file")
st.write(
    """Check out the example bank dataset or upload your own bank / debit card / credit card / spending spreadsheet!
Analyze your total and average spending over each month / week / day / year / quarter.
See what the minimum / maximum / total number of purchases were in each period.

If your data has a description / name / category column, view how many times you've made those purchases.
Or use it on other roughly timeseries aggregated univariate data!
type supported =["csv", "xls", "xlsx", "xlsm"] """
)

load_file()

show_code(load_file)
