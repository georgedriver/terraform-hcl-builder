# coding=utf-8
from pprint import pprint

name = "hcl_builder"

import argparse
import json
from terrascript import Terrascript
from terrascript.alicloud.r import alicloud_instance

str_template = """{resource_or_data} "{resource_type}" "{resource_name}" {{
{resource_content}
}}
"""


def factory(alicloud_instance, new_resource_type):
    class NewClass(alicloud_instance): pass

    NewClass.__name__ = new_resource_type
    return NewClass


def printjson2hcl(json_str):
    """
    Just print json2hcl data
    :param json_str:
    :return:
    """
    json_data = json.loads(json_str)
    for resource_or_data, resource_or_data_value in json_data.items():
        for resource_type, resource_type_value in resource_or_data_value.items():
            for resource_name, resource_name_value in resource_type_value.items():
                resource_content = '\n'.join("  {} = {}{}{}".format(
                    k, '' if type(v) == int else '"', v, '' if type(v) == int else '"'
                ) for k, v in resource_name_value.items())

                print(str_template.format(resource_or_data=resource_or_data, resource_type=resource_type,
                                          resource_name=resource_name, resource_content=resource_content))


class TerraformHclFromDataSource:

    def __init__(self, record_file_name, resource_type, id_field_name, keywords_names):

        keywords_names_list = str(keywords_names).replace(" ", "").split(',')
        keywords_in_record = [str(v).replace(" ", "").split('=')[0] for v in keywords_names_list]
        keywords_in_hcl = [str(v).replace(" ", "").split('=')[1] if '=' in str(v)
                           else str(v).replace(" ", "").split('=')[0]
                           for v in keywords_names_list]
        keywords_names_dict = dict(zip(keywords_in_record, keywords_in_hcl))

        self.file = open(record_file_name, 'r')

        json_data = json.load(self.file)

        alicloud_factory = factory(alicloud_instance, str(resource_type))

        self.alicloud_hcl_store = Terrascript()
        self.alicloud_cmd_store = []

        for record in json_data:
            assert record.get(id_field_name, "") != ""
            factory_parameter_dict = {}
            for k_record, k_hcl in keywords_names_dict.items():
                factory_parameter_dict[k_hcl] = record[k_record]

            resource_name = str(resource_type) + '-' + str(record[id_field_name])

            one_hcl_item = alicloud_factory(resource_name, **factory_parameter_dict)
            one_cmd_item = "terraform import {}.{} {}".format(resource_type, resource_name, str(record[id_field_name]))

            self.alicloud_hcl_store.add(one_hcl_item)
            self.alicloud_cmd_store.append(one_cmd_item)

    def dump_hcl(self):
        """Dump Terraform Code."""

        printjson2hcl(self.alicloud_hcl_store.dump())

    def dump_cmd(self):
        """Dump Terraform import Command."""

        for cmd in self.alicloud_cmd_store:
            print(cmd)

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


def main():
    parser = argparse.ArgumentParser(description='TF_HCL_GENERATOR.')

    parser.add_argument('action', metavar='ACTION', type=str,
                        help='"hcl" or "cmd": generate hcl or import cmd')

    parser.add_argument('records_output_file', metavar='RECORDS_OUTPUT_FILE', type=str,
                        help='records_output_file name from data source')

    parser.add_argument('resource_type', metavar='RESOURCE_TYPE', type=str,
                        help='resource_type like alicloud_dns_record, alicloud_instance, etc')

    parser.add_argument('id_field_name', metavar='ID_FIELD_NAME', type=str,
                        help='id_field_name the name of the ID field in records_output_file')

    parser.add_argument('keywords_names', metavar='KEYWORDS_NAMES', type=str,
                        help='keywords_names example: "domain_name=name, host_record, type, value"')

    action = parser.parse_args().action
    records_output_file = parser.parse_args().records_output_file
    resource_type = parser.parse_args().resource_type
    id_field_name = parser.parse_args().id_field_name
    keywords_names = parser.parse_args().keywords_names

    t_hcl = TerraformHclFromDataSource(records_output_file, resource_type, id_field_name, keywords_names)

    if action == "hcl":
        t_hcl.dump_hcl()
    elif action == "cmd":
        t_hcl.dump_cmd()
    else:
        raise Exception("Wrong action gave! Use -h to check the validate action")


if __name__ == '__main__':
    main()
