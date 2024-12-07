#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module generates standard files & documentation.
"""
from types import SimpleNamespace

import frictionless as fl
import json
from .paths import docs_path, standard_path
from .markdown import to_markdown
from .meta import package_from_kwargs, gen_metadata
from . import VERSION

def _make_standard_package(*args, **kwargs):
    with (standard_path / "package_spec.json").open('r', encoding="utf-8") as flow:
        package_infos = json.load(flow)
        package_infos["version"] = VERSION

    with (standard_path / "columns_spec.json").open('r', encoding="utf-8") as flow:
        columns = json.load(flow)

    with (standard_path / "files_spec.json").open('r', encoding="utf-8") as flow:
        resources = json.load(flow)["resources"]

    new_resources = []
    for res in resources:
        # replace column names by their full definition
        if res["path"].endswith(".csv"):
            res["schema"]["fields"] = [dict(columns[f]) for f in res["schema"]["fields"]]

        if res["name"] == "forms":
            for col in res["schema"]["fields"]:
                if col["name"] in ["lexeme", "cell"]:
                    col["constraints"] =  {"required": True }

        new_resources.append(fl.Resource(res))

    package = package_from_kwargs(resources=new_resources, **package_infos)

    package.to_json(str(standard_path / "paralex.package.json"))


def _write_doc(*args, **kwargs):
    to_markdown(fl.Package(standard_path / "paralex.package.json"),
                docs_path / "specs.md")

    # generate json files for examples
    examples_dir = docs_path / "examples"
    for directory in examples_dir.glob("*/"):
        print(directory)
        gen_metadata(SimpleNamespace(config=directory / "paralex-infos.yml", basepath=directory))


