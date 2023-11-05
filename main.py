# Import Functions and Modules
from solutions.fast import extract_info
from solutions.comprehensive import process_click_data
from pathlib import Path
import time
from json import dump as jdump


# Execute methods
def main(encode_fp: Path, decode_fp: Path) -> (dict, dict):
    """
    A main function to execute both solution approaches and evaluate efficiency and output. Each solution has a
    timer for a basic performance evaluation.
    :param encode_fp: file path to encode csv
    :param decode_fp: file path to click data
    :return: tuple of solution dictionaries
    """
    start_fast = time.perf_counter()
    fast_out = extract_info(encode_fp=encode_fp, decode_fp=decode_fp)
    fast_out = [{xx: fast_out[xx]} for xx in fast_out]
    end_fast = time.perf_counter()
    comp_out = process_click_data(encode_fp=encode_fp, decode_fp=decode_fp)
    comp_out = [{xx: comp_out[xx]} for xx in comp_out]
    end_comp = time.perf_counter()
    fast_time = end_fast - start_fast
    comp_time = end_comp - end_fast
    print(f"Fast and Dirty Solution execution time: {fast_time} seconds")
    print(f"Comprehensive Solution execution time: {comp_time} seconds")
    print(
        f"Comprehensive Solution performance benefit: {round(fast_time / comp_time,1)}x"
    )
    print("\n")
    return fast_out, comp_out


if __name__ == "__main__":
    encode_fp = Path("data").joinpath("encodes.csv")
    decode_fp = Path("data").joinpath("decodes.json")
    fast_output, comprehensive_output = main(encode_fp=encode_fp, decode_fp=decode_fp)
    print("Fast and Dirty Solution Output:")
    print(fast_output)
    print("\n")
    print("Comprehensive Solution Output")
    print(comprehensive_output)
    print("\n")
    jdump(comprehensive_output, open("final_output.json", "w"))
    print("Output saved to final_output.json in project directory")
