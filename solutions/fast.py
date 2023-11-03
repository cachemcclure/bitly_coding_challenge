# Import Modules
import pandas as pd
from pathlib import Path
from json import loads as jloads


# Function(s)
def extract_info(encode_fp: Path, decode_fp: Path, debug: bool = False) -> dict:
    """
    :param encode_fp: File path to encode file
    :param decode_fp: File path to decode file
    :param debug: Print intermediate steps if True
    :return: dict: Ordered list of clicks by long-form url
    """
    # Initialize variables and load data
    out = {}
    encode_df = pd.read_csv(encode_fp, delimiter=",")
    decode_df = pd.read_json(decode_fp, lines=True)

    # Transform data
    filter_list = list(set("http://" + encode_df["domain"] + "/" + encode_df["hash"]))
    filter_decode_df = decode_df.query("bitlink in @filter_list")
    filter_decode_df = filter_decode_df[
        filter_decode_df["timestamp"].astype(str).str.startswith("2021")
    ]
    out_df = filter_decode_df.groupby("bitlink").count()

    # Convert output to correct order and format
    out_init = jloads(out_df.to_json())["user_agent"]
    if debug:
        print(out_init)
    out_init = dict(sorted(out_init.items(), key=lambda item: item[1], reverse=True))
    if debug:
        print(out_init)
    for xx in out_init:
        out[
            encode_df[encode_df["hash"] == xx[xx.rfind("/") + 1 :]].iloc[0]["long_url"]
        ] = out_init[xx]
    return out
