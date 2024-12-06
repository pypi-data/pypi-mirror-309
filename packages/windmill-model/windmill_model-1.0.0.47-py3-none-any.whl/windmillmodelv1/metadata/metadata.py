#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/2
# @Author  : yanxiaodong
# @File    : model_metadata_update.py
"""
import os
from collections import defaultdict
from typing import Dict, List
import yaml

import bcelogger
from pygraphv1.client.graph_api_graph import GraphContent
from windmillmodelv1.client.model_api_model import Category, Label


def update_metadata(graph: GraphContent, model_metadata: Dict, input_uri: str = "/home/windmill/tmp/model"):
    """
    Update the model metadata.
    兼容以前算法定义的模型包描述文件规范 https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/0ebIgLpF-L/I1E7bZqZ7Q/SA_YV6fjalxz2M
    """
    postprocess_filename = "parse.yaml"
    infer_config_filename = "config.yaml"
    whitelist_filename = "white_list.yaml"

    track_flag = "track"

    postprocess_file = None
    track_file = None
    infer_config_files = []
    whitelist_file = None
    for root, dirs, files in os.walk(input_uri):
        for file in files:
            absolute_file = os.path.join(root, file)
            if postprocess_filename == os.path.basename(absolute_file):
                postprocess_file = absolute_file
            elif infer_config_filename == os.path.basename(absolute_file) and track_flag in absolute_file:
                track_file = absolute_file
            elif infer_config_filename == os.path.basename(absolute_file):
                infer_config_files.append(absolute_file)
            elif whitelist_filename == os.path.basename(absolute_file):
                whitelist_file = absolute_file
            else:
                continue

    # 1. 获取推理配置信息
    bcelogger.info(f"Infer config files: {infer_config_files}")
    infer_config, infer_config_name2value = get_infer_config(input_uris=infer_config_files,
                                                             postprocess_file=postprocess_file,
                                                             track_file=track_file)
    bcelogger.info(f"Infer config: {infer_config} from files {infer_config_files}")

    # 2. 获取白名单信息
    bcelogger.info(f"Whitelist file: {whitelist_file}")
    whitelist, whitelist_id2value = get_whitelist(input_uri=whitelist_file, postprocess_file=postprocess_file)
    bcelogger.info(f"Whitelist: {whitelist} from file {whitelist_file}")

    # 3. 获取标签信息
    bcelogger.info(f"Postprocess file: {postprocess_file}")
    labels, model2label_id = get_labels(input_uri=postprocess_file,
                                        infer_config_name2value=infer_config_name2value,
                                        whitelist_id2value=whitelist_id2value)
    bcelogger.info(f"Labels: {labels} from file {postprocess_file}")

    # 4. 更新推理配置信息
    bcelogger.info(f"Updated infer config from {model2label_id}")
    infer_config = update_infer_config(infer_config=infer_config, model2label_id=model2label_id)
    bcelogger.info(f"Updated infer config: {infer_config}")

    model_metadata["labels"] = labels
    model_metadata["inferConfig"] = infer_config
    model_metadata["graphContent"] = graph.dict(by_alias=True, exclude_none=True)


def get_infer_config(input_uris: List[str], postprocess_file: str, track_file: str):
    """
    Get the infer config.
    """
    if len(input_uris) == 0 or postprocess_file is None:
        return {}, {}

    postprocess_content = yaml.load(open(postprocess_file, "r"), Loader=yaml.FullLoader)
    track_type = postprocess_content.get("track_type", False)

    infer_config = defaultdict(list)

    if track_file is not None and track_type:
        content = yaml.load(open(track_file, "r"), Loader=yaml.FullLoader)
        for item in content["model_parameters"]:
            item["is_track"] = True
        infer_config["model_parameters"].extend(content["model_parameters"])

    for file in input_uris:
        content = yaml.load(open(file, "r"), Loader=yaml.FullLoader)
        infer_config["model_parameters"].extend(content["model_parameters"])

    infer_config_name2value = {}
    for item in infer_config.get("model_parameters", []):
        model_name = item["master_model"]
        if item.get("is_track", False):
            continue
        for parameter in item["parameters"]:
            infer_config_name2value[(model_name, parameter["namespace"])] = parameter["default"]

    return infer_config, infer_config_name2value


def update_infer_config(infer_config: Dict, model2label_id: Dict):
    """
    Update the infer config.
    """
    infer_config_id2value = defaultdict(dict)
    new_infer_config = {"inferParameters": []}

    for item in infer_config.get("model_parameters", []):
        item["model"] = item.pop("master_model", "")
        item["isTrack"] = item.pop("is_track", False)
        for parameter in item["parameters"]:
            parameter["nameCN"] = parameter.pop("name_cn", "")
            infer_config_id2value[parameter["namespace"]] = parameter
        if item["isTrack"]:
            new_infer_config["inferParameters"].append(item)

    for model_name, labels in model2label_id.items():
        current_infer_config = []
        for label_name, label_id in labels.items():
            if label_id not in infer_config_id2value:
                current_infer_config.append({
                    "default": 0.5,
                    "labelName": label_name,
                    "namespace": label_id,
                    "range": "0,1",
                    "step": 0.01,
                    "type": "float"
                })
            else:
                infer_config_id2value[label_id]["labelName"] = label_name
                current_infer_config.append(infer_config_id2value[label_id])

        new_infer_config["inferParameters"].append({
            "model": model_name,
            "isTrack": False,
            "parameters": current_infer_config
        })

    return new_infer_config


def get_whitelist(input_uri: str, postprocess_file: str):
    """
    Get the whitelist.
    """
    if input_uri is None or postprocess_file is None:
        return {}, {}

    postprocess_content = yaml.load(open(postprocess_file, "r"), Loader=yaml.FullLoader)
    if postprocess_content.get("support_white_list", "false") == "false":
        return {}, {}

    whitelist_content = yaml.load(open(input_uri, "r"), Loader=yaml.FullLoader)

    whitelist_id2value = {}
    for item in whitelist_content.get("white_list", []):
        whitelist_id2value[item["category"]["id"]] = item["similarity_threshold"]

    return whitelist_content, whitelist_id2value


def get_labels(input_uri: str, infer_config_name2value: Dict, whitelist_id2value: Dict):
    """
    Get the labels.
    """
    if input_uri is None:
        bcelogger.warning("No postprocess file found")
        return []

    content = yaml.load(open(input_uri, "r"), Loader=yaml.FullLoader)
    assert len(content["outputs"]) > 0, f"No output found in {content}"
    assert "fields_map" in content["outputs"][0], f'Field fields_map not in {content["outputs"][0]}'

    labels = []
    model2label_id = defaultdict(dict)
    label_names = set()
    output = content["outputs"][0]
    for item in output["fields_map"]:
        model_name = item["model_name"].split("|")[0]
        label_index = -1

        if len(item["categories"]) == 0:
            continue
        elif isinstance(item["categories"][0], list):
            for sub_item in item["categories"]:
                label_index = parse_labels(model_labels=sub_item,
                                           labels=labels,
                                           model2label_id=model2label_id,
                                           model_name=model_name,
                                           label_names=label_names,
                                           label_index=label_index,
                                           infer_config_name2value=infer_config_name2value,
                                           whitelist_id2value=whitelist_id2value)
        elif isinstance(item["categories"][0], dict):
            parse_labels(model_labels=item["categories"],
                         labels=labels,
                         model2label_id=model2label_id,
                         model_name=model_name,
                         label_names=label_names,
                         label_index=label_index,
                         infer_config_name2value=infer_config_name2value,
                         whitelist_id2value=whitelist_id2value)
        else:
            bcelogger.error(f'Model name {item["model_name"]} labels {item["categories"]} is invalid')

    return labels, model2label_id


def parse_labels(model_labels: List[Dict],
                 labels: List[Dict],
                 model2label_id: Dict,
                 model_name: str,
                 label_names: set,
                 label_index: int,
                 infer_config_name2value: Dict,
                 whitelist_id2value: Dict):
    """
    Parse the labels.
    """
    parent_name2id = {}

    for label in model_labels:
        bcelogger.info(f'Model {model_name} label: {label}')
        parent_name = None
        parent_id = None

        # label id 处理未int,目前包括遗下几种情况:
        # 1. 数字字符串 "1"
        # 2. 字符串 "che"
        # 3. 带父类的字符串 "安全帽｜0"
        # 4. 整数
        label_id = label["id"]
        if isinstance(label_id, str) and label_id.isdigit():
            label_id = int(label_id)
        elif isinstance(label_id, str) and len(label_id.split("|")) > 1:
            parent_name = label_id.split("|")[0]
            label_id = int(label_id.split("|")[-1])
        elif isinstance(label_id, int):
            label_id = label_id
        else:
            label_index += 1
            label_id = label_index

        # parent id 和 parent name 处理
        if "super_category" in label:
            parent_name = label["super_category"]
        if parent_name is not None:
            if "super_category_id" in label:
                parent_id = label["super_category_id"]
            if parent_id is None:
                if parent_name not in parent_name2id:
                    label_index += 1
                parent_id = label_index
            parent_name2id[parent_name] = parent_id

        # 校验多个模型标签是否有相同的name，有的话过滤
        label_name = label["name"]
        if parent_name is not None and parent_name in label_names:
            continue
        if parent_name is None and label_name in label_names:
            continue

        if parent_id is not None:
            label_instance = Label(id=label_id, name=label_name, parentID=parent_id, modelName=model_name)
        else:
            label_instance = Label(id=label_id, name=label_name, modelName=model_name)
            label_names.add(label_name)

        if label["id"] in whitelist_id2value:
            label_instance.whitelistThreshold = whitelist_id2value[label["id"]]

        if (model_name, label["id"]) in infer_config_name2value:
            label_instance.threshold = infer_config_name2value[(model_name, label["id"])]

        model2label_id[model_name][label_name] = label["id"]
        labels.append(label_instance.dict(exclude_none=True))

    for parent_name, parent_id in parent_name2id.items():
        label_names.add(parent_name)
        labels.append(Label(id=parent_id, name=parent_name, modelName=model_name).dict(exclude_none=True))

    return label_index
