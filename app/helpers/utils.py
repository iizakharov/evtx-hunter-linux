import os
import glob
import logging
import jsonlines
import vars
import json
import pandas as pd


def create_log_fields_string(event, log_fields):
    output_strings = list()
    for field in log_fields:
        if field in event["data"]["Event"]["EventData"]:
            output_strings.append(field + ":" + event["data"]["Event"]["EventData"][field])

    return "\n\n".join(output_strings)


def dict_flatten(in_dict, dict_out=None, parent_key=None, separator="."):
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def normalize_event(event):
    flattened_dict = dict_flatten(event['data'])

    event_id = event["data"]["Event"]["System"]["EventID"]
    if type(event_id) != int:
        event["data"]["Event"]["System"]["EventID"] = event_id["#text"]

    if "EventData" not in event["data"]["Event"].keys() or event["data"]["Event"]["EventData"] is None:
        event["data"]["Event"]["EventData"] = dict()

    for k in event["data"]["Event"]["System"].keys():
        event["data"]["Event"]["EventData"][k] = event["data"]["Event"]["System"][k]

    for k in event["data"]["Event"].keys():
        if k != "EventData":
            event["data"]["Event"]["EventData"][k] = event["data"]["Event"][k]

    if "UserData" in event["data"]["Event"].keys():
        for k in event["data"]["Event"]["UserData"].keys():
            event["data"]["Event"]["EventData"][k] = dict()
            for k_ in event["data"]["Event"]["UserData"][k].keys():
                event["data"]["Event"]["EventData"][k][k_] = event["data"]["Event"]["UserData"][k][k_]

    for k, v in flattened_dict.items():
        event["data"]["Event"]["EventData"][k.split(".")[-1]] = v

    return event


def retrieve_all_occurence_rules():
    file = json.load(open(vars.RULE_DIR + "interesting_events.json", 'r'))
    # print(file)
    for rule_info in file["rules"]:
        yield rule_info


def retrieve_all_first_occurence_rules():
    for rule_info in json.load(open(vars.RULE_DIR + "first_occurence.json", 'r'))["rules"]:
        yield rule_info


def retrieve_all_events():
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        with open(file_info["json_dump_filename"], 'r') as jdf:
            reader = json.loads(jdf.read())
            for item in reader:
                yield item




def get_description_for_event_id(event_id):
    event_id = int(event_id)
    description_loc = vars.EVENT_ID_MAPPING[vars.EVENT_ID_MAPPING['event_id'] == event_id]
    return ', '.join(description_loc["description"].tolist())


def load_event_id_mappings():
    df = pd.read_csv(vars.EXTERNAL_DIR + "event_id_mapping.csv", delimiter=";")

    # using dictionary to convert specific columns
    convert_dict = {'event_id': int}
    df = df.astype(convert_dict)
    vars.EVENT_ID_MAPPING = df


def get_all_event_channels():
    event_channels = set()
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        event_channels.update(list(file_info["event_channel_counts"].keys()))

    return list(event_channels)


def get_recursive_filenames(path, file_suffix):
    filenames = list()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(subdir, file)
            if filename.endswith(file_suffix):
                filenames.append(filename)

    return filenames


def remove_all_tmp_json_files():
    files = glob.glob(vars.TMP_DIR + "/evtx_dump/*.json")
    for f in files:
        os.remove(f)


def setup_logger():
    logger = logging.getLogger('sc-evtx-parser')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


def sort_dict(_dict, reverse=False):
    event_summary_list = sorted(_dict.items(), key=lambda x: x[1], reverse=reverse)
    return dict(event_summary_list)
