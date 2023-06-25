# coding=utf-8

import os
import logging
import uuid
import shutil
import argparse
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader


UPPER_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 模板文件都在上级目录的 fwtemplates 目录下
TEMPLATE_ROOT = os.path.join(UPPER_PATH, "fwtemplates")


logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)d@%(funcName)s) -> %(message)s')
logger = logging.getLogger("generate_ge_skeleton")
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def parse_input():
    parser = argparse.ArgumentParser(
        description = "Generate skeleton files for using Great Expectations.",
        formatter_class = argparse.RawTextHelpFormatter
    )

    parser.add_argument("--name", dest="project_name", type=str, required=True,
                        help="Name of target project.")

    parser.add_argument("--rootdir", dest="project_root", type=str, required=True,
                        help="Root directory of target project.")

    parsed_args = parser.parse_args()
    return vars(parsed_args)


TemplateMapping = namedtuple(
        "TemplateMapping",
        ["src_template_name",
         "dst_file_path",
         "render_value_map"
        ])

def render_template_file(render_env, to_render_template):
    if not os.path.exists(to_render_template.dst_file_path):
        template = render_env.get_template(to_render_template.src_template_name)
        rendered_content = template.render(**to_render_template.render_value_map)

        with open(to_render_template.dst_file_path, "w") as wf:
            wf.write(rendered_content)
        return 1
    else:
        return 0

def put_init_py(target_dir):
    source_path = os.path.join(TEMPLATE_ROOT, "__init__.py")
    target_path = os.path.join(target_dir, "__init__.py")
    if not os.path.exists(target_path):
        shutil.copyfile(source_path, target_path)

def process(rid, project_name, project_root):
    render_env = Environment(loader=FileSystemLoader(TEMPLATE_ROOT))
    templates = []

    put_init_py(project_root)

    # Generate configuration files
    tpl_config_ini = TemplateMapping(
        "config.ini",
        os.path.join(project_root, "config.ini"),
        {"project_name": project_name}
    )
    templates.append(tpl_config_ini)

    tpl_config_py = TemplateMapping(
        "config.py",
        os.path.join(project_root, "config.py"),
        {"render_id": rid,
         "project_name": project_name,
         "project_root": project_root}
    )
    templates.append(tpl_config_py)

    # Generate helper files
    tpl_mapping_py = TemplateMapping(
        "mapping.py",
        os.path.join(project_root, "mapping.py"),
        {"render_id": rid,
         "project_root": project_root}
    )
    templates.append(tpl_mapping_py)

    tpl_main_py = TemplateMapping(
        "main.py",
        os.path.join(project_root, "main.py"),
        {"render_id": rid,
         "project_root": project_root}
    )
    templates.append(tpl_main_py)


    # Rules (expectation suite)files, post-configure needed.
    rules_root = os.path.join(project_root, "rules")
    rule_template_path = lambda x: f"rules/{x}"
    put_init_py(rules_root)

    tpl_rule_value_is_zero = TemplateMapping(
        rule_template_path("rule_value_is_zero.py"),
        os.path.join(rules_root, "rule_value_is_zero.py"),
        {"render_id": rid}
    )
    templates.append(tpl_rule_value_is_zero)


    # Dataset files.
    dataset_root = os.path.join(project_root, "data_assets")
    dataset_template_path = lambda x: f"data_assets/{x}"
    put_init_py(dataset_root)

    tpl_ds_base = TemplateMapping(
        dataset_template_path("dataset.py"),
        os.path.join(dataset_root, "dataset.py"),
        {"render_id": rid}
    )
    templates.append(tpl_ds_base)

    tpl_ds_example001 = TemplateMapping(
        dataset_template_path("dataset_example_data_001.py"),
        os.path.join(dataset_root, "dataset_example_data_001.py"),
        {"render_id": rid,
         "project_root": project_root}
    )
    templates.append(tpl_ds_example001)


    rendered_number = sum([render_template_file(render_env, template) for template in templates])
    return rendered_number


def main():
    in_args = parse_input()

    project_name = in_args["project_name"]
    project_root = in_args["project_root"]

    this_render_id = uuid.uuid5(uuid.NAMESPACE_URL, project_name)

    rn = process(this_render_id, project_name, project_root)
    logger.info(f"Rendered {rn} files.")


if __name__ == "__main__":
    main()

