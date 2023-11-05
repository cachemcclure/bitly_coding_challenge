# Import Modules
from pathlib import Path
from json import loads as jloads


# Function(s)
def interpret_file(fp: Path, count_dict: dict, timestamp_filter: int = None) -> dict:
    """
    This function interprets a JSON line-separated file to extract clicks based on a supplied dictionary. It works
    on the same principle as a streaming data application and could easily be modified for that approach to utilize
    a data buffer in place of a file path.
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
    This function builds a translation dictionary from a CSV file with a given structure. Rather than using a library
    specifically built to handle CSV data, this reads the raw text and interprets it. While this approach is faster, it
    relies on a consistent format and would break with even basic changes. However, since it is dealing with an assumed
    static dictionary, this approach can be considered valid.
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
    This function combines the two above to process a data file (or data stream) to aggregate the number of clicks
    based on the created dictionary, then reorders the results into descending order (something that is inefficient in
    Python but understandable for the output).
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
