# noqa
"""
Take in a YAML, and output all "other" splits with this YAML
"""

import argparse
import logging
import os

import yaml
from tqdm import tqdm


eval_logger = logging.getLogger(__name__)


SUBJECTS = {
    'Accounting (University)': 'social sciences',
    'Arabic Language (General)': 'language',
    'Arabic Language (Grammar)': 'language',
    'Arabic Language (High School)': 'language',
    'Arabic Language (Middle School)': 'language',
    'Arabic Language (Primary School)': 'language',
    'Biology (High School)': 'stem',
    'Civics (High School)': 'social sciences',
    'Civics (Middle School)': 'social sciences',
    'Computer Science (High School)': 'stem',
    'Computer Science (Middle School)': 'stem',
    'Computer Science (Primary School)': 'stem',
    'Computer Science (University)': 'stem',
    'Driving Test': 'other',
    'Economics (High School)': 'social sciences',
    'Economics (Middle School)': 'social sciences',
    'Economics (University)': 'social sciences',
    'General Knowledge': 'other',
    'General Knowledge (Middle School)': 'other',
    'General Knowledge (Primary School)': 'other',
    'Geography (High School)': 'social sciences',
    'Geography (Middle School)': 'social sciences',
    'Geography (Primary School)': 'social sciences',
    'History (High School)': 'humanities',
    'History (Middle School)': 'humanities',
    'History (Primary School)': 'humanities',
    'Islamic Studies': 'humanities',
    'Islamic Studies (High School)': 'humanities',
    'Islamic Studies (Middle School)': 'humanities',
    'Islamic Studies (Primary School)': 'humanities',
    'Law (Professional)': 'humanities',
    'Management (University)': 'other',
    'Math (Primary School)': 'stem',
    'Natural Science (Middle School)': 'stem',
    'Natural Science (Primary School)': 'stem',
    'Philosophy (High School)': 'humanities',
    'Physics (High School)': 'stem',
    'Political Science (University)': 'social sciences',
    'Social Science (Middle School)': 'social sciences',
    'Social Science (Primary School)': 'social sciences'
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_yaml_path", required=True)
    parser.add_argument("--save_prefix_path", default="mmlu_arabic")
    parser.add_argument("--cot_prompt_path", default=None)
    parser.add_argument("--task_prefix", default="")
    parser.add_argument("--group_prefix", default="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # get filename of base_yaml so we can `"include": ` it in our "other" YAMLs.
    base_yaml_name = os.path.split(args.base_yaml_path)[-1]
    with open(args.base_yaml_path, encoding="utf-8") as f:
        base_yaml = yaml.full_load(f)

    if args.cot_prompt_path is not None:
        import json

        with open(args.cot_prompt_path, encoding="utf-8") as f:
            cot_file = json.load(f)

    ALL_CATEGORIES = []
    for subject, category in tqdm(SUBJECTS.items()):
        if category not in ALL_CATEGORIES:
            ALL_CATEGORIES.append(category)

        if args.cot_prompt_path is not None:
            description = cot_file[subject]
        else:
            description = f"The following are multiple choice questions (with answers) about {subject.lower()}.\n\n"

        yaml_dict = {
            "include": base_yaml_name,
            "tag": f"mmlu_arabic_{args.task_prefix}_{category.repalce(' ', '_')}_tasks"
            if args.task_prefix != ""
            else f"mmlu_arabic_{category.replace(' ', '_')}_tasks",
            "task": f"mmlu_arabic_{args.task_prefix}_{subject}"
            if args.task_prefix != ""
            else f"mmlu_arabic_{subject}",
            "task_alias": subject.lower(),
            "dataset_name": subject,
            "description": description,
        }

        file_save_path = args.save_prefix_path + f"_{subject.translate({ord(i): None for i in '()'}).lower().replace(" ", "_")}.yaml"
        eval_logger.info(f"Saving yaml for subset {subject} to {file_save_path}")
        with open(file_save_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(
                yaml_dict,
                yaml_file,
                allow_unicode=True,
                default_style='"',
            )

    if args.task_prefix != "":
        mmlu_subcategories = [
            f"mmlu_arabic_{args.task_prefix}_{category}" for category in ALL_CATEGORIES
        ]
    else:
        mmlu_subcategories = [f"mmlu_arabic_{category}" for category in ALL_CATEGORIES]

    if args.group_prefix != "":
        file_save_path = args.group_prefix + ".yaml"
    else:
        file_save_path = args.save_prefix_path + ".yaml"

    eval_logger.info(f"Saving benchmark config to {file_save_path}")
    with open(file_save_path, "w", encoding="utf-8") as yaml_file:
        yaml.dump(
            {
                "group": f"mmlu_arabic_{args.task_prefix}"
                if args.task_prefix != ""
                else "mmlu_arabic",
                "task": mmlu_subcategories,
            },
            yaml_file,
            indent=4,
            default_flow_style=False,
        )
