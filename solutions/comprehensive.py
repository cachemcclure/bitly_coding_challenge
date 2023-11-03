# Import Modules
from pathlib import Path
from json import loads as jloads


# Function(s)
def interpret_line(
    data_input: dict, bitlink_filter: list = None, timestamp_filter: int = None
) -> bool:
    """
    :param data_input: Input line as Python dict
    :param bitlink_filter: List filter for bitlinks
    :param timestamp_filter: Integer filter for timestamp year
    :return: Boolean if input meets filter constraints
    """
    out = False
    req_fields = ["bitlink", "timestamp"]
    for field in req_fields:
        if field not in data_input:
            raise Exception(f"ERROR: missing required field {field} in input")
    if ~(bitlink_filter is None) and (data_input["bitlink"] in bitlink_filter):
        out = True
    elif bitlink_filter is None:
        out = True
    else:
        out = False
    if ~(timestamp_filter is None) and (
        str(data_input["timestamp"]).startswith(str(timestamp_filter))
    ):
        out = True
    elif timestamp_filter is None:
        out = True
    else:
        out = False
    return out


def interpret_file(fp: Path, count_dict: dict, timestamp_filter: int = None) -> dict:
    """
    :param fp: filepath to emulate stream of data
    :param count_dict: storage dictionary to count clicks (doubles as bitlink filter)
    :param timestamp_filter: filter for timestamp
    :return: unsorted storage dictionary for click count
    """
    with open(fp, "r") as file:
        for line in file:
            i_line = jloads(line.rstrip())
            if ("bitlink" not in i_line) or ("timestamp" not in i_line):
                continue
            if (i_line["bitlink"] in count_dict) and str(
                i_line["timestamp"]
            ).startswith(str(timestamp_filter)):
                count_dict[i_line["bitlink"]] += 1
    return count_dict


def build_bitlink_dict(fp: Path) -> dict:
    """
    :param fp: file path to encoding file
    :return: dict of bitly url with value full url
    """
    out = {}
    with open(fp) as f:
        header = f.readline()
        for line in f:
            line_data = line.replace("\n", "").split(",")
            out["http://" + line_data[1] + "/" + line_data[2]] = line_data[0]
    return out


def process_click_data(encode_fp: Path, decode_fp: Path, debug: bool = False) -> dict:
    """
    :param encode_fp: file path to encoded links
    :param decode_fp: file path to click data
    :param debug: print intermediate steps if True
    :return: sorted dictionary of clicks
    """
    out = {}
    bitlink_dict = build_bitlink_dict(fp=encode_fp)
    if debug:
        print(bitlink_dict)
    init_store_dict = {}
    for link in bitlink_dict:
        init_store_dict[link] = 0
    if debug:
        print(init_store_dict)
    init_store_dict = interpret_file(
        fp=decode_fp, count_dict=init_store_dict, timestamp_filter=2021
    )
    if debug:
        print(init_store_dict)
    for link in init_store_dict:
        out[bitlink_dict[link]] = init_store_dict[link]
    out = dict(sorted(out.items(), key=lambda item: item[1], reverse=True))
    return out
