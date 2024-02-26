# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 22:33:51 2024

@author: shabirahmad.magray
"""

from __future__ import absolute_import

import datetime
import os
import subprocess
import sys
import time

import regex

import shutil

# Source and destination file paths
source_file = 'relevance_tmp.txt'
destination_file = 'relevance_tmp_original.txt'

# Copy the file
shutil.copy(source_file, destination_file)

DEFAULT_INPUT_FILE = "relevance_tmp.txt"

OUTPUT_FILE = "relevance_out.txt"
PROCESSED_FILE = "relevance_processed.txt"


def get_path_qna():
    """find path for the QNA binary"""
    test_file_paths = [
        "QnA",
        "/usr/local/bin/QnA",
        "/Library/BESAgent/BESAgent.app/Contents/MacOS/QnA",
        "/opt/BESClient/bin/QnA",
        "C:/Program Files (x86)/BigFix Enterprise/BES Client/qna.exe",
    ]

    for file_path in test_file_paths:
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path

    raise FileNotFoundError("Valid QNA path not found!")


def parse_raw_result_array(result):
    """parse a raw relevance result into an array"""
    results_array_raw = regex.regex.split("\r\n|\r|\n", result)
    results_array = []
    for result_raw in results_array_raw:
        if result_raw.startswith("A: "):
            results_array.append(result_raw.split("A: ", 1)[1])
    return results_array


def EvaluateRelevanceString(relevance, separator="\n"):
    """get string with newlines from relevance results"""
    return separator.join(EvaluateRelevanceArray(relevance))


def EvaluateRelevanceArray(relevance):
    """get array from relevance results"""
    return parse_raw_result_array(EvaluateRelevanceRaw(relevance))


def EvaluateRelevanceRawFile(rel_file=DEFAULT_INPUT_FILE):
    """This function will get raw text client relevance results from a file"""
    start_time = time.monotonic()
    qna_run = subprocess.run(
        [get_path_qna(), "-t", "-showtypes", rel_file],
        check=True,
        capture_output=True,
        text=True,
    )
    end_time = time.monotonic()

    output_data = qna_run.stdout
    error_data = qna_run.stderr

    output_data += (
        "Time Taken: "
        + str(datetime.timedelta(seconds=end_time - start_time))
        + " as measured by python.\n"
    )
    if error_data:
        print("Error: " + error_data)

    if 'E: The operator "string" is not defined.' in output_data:
        output_data += "\nInfo: This error means a result was found, but it does not have a string representation."

    with open(OUTPUT_FILE, "a") as rel_output:
        rel_output.write(output_data)

    with open(PROCESSED_FILE, "a") as rel_processed:
        rel_processed.write(output_data)

    with open("relevance_str.txt", "w") as rel_output:
        rel_output.write("\n".join(parse_raw_result_array(output_data)))

    return output_data


def EvaluateRelevanceRaw(relevance="TRUE"):
    """This function will get raw text client relevance results"""
    with open(DEFAULT_INPUT_FILE, "w") as rel_file:
        rel_file.write("Q: " + relevance)

    return EvaluateRelevanceRawFile(DEFAULT_INPUT_FILE)


def main():
    """Execution starts here:"""
  
    with open(DEFAULT_INPUT_FILE, "r") as file:
        for line in file:
            relevance = line.strip()
            print(EvaluateRelevanceRaw(relevance))
    try:
        os.remove(DEFAULT_INPUT_FILE)
        os.remove(PROCESSED_FILE)
        
    except FileNotFoundError:
        pass
    
    # Source and destination file paths
    source_file = 'relevance_tmp_original.txt'
    destination_file = 'relevance_tmp.txt'
    

    # Copy the file
    shutil.copy(source_file, destination_file)


if __name__ == "__main__":
    main()
