# terraform-hcl-builder

Build terraform HCL/import CMD from data resource output_file.

This tool can help generate the Terraform HCL code from data resource's output_file; it also can help to generate the tfstate file with terraform import CMD.

## How to use

### Prerequisites

- Python3 "Tested by Python 3.6.6"

- Install `pip3 install git+https://github.com/georgedriver/terraform-hcl-builder.git`

- Basic knowledge about Terraform

### IMPORTANT: Must read

1; This tool "hcl-builder.py" will need the `output_file` generated from terraform data resource, below is the example data resource:

```hcl
data "alicloud_dns_records" "records_ds" {
  domain_name = "xxxxxx.com"
  // is_locked = false
  // host_record_regex = "^@"
  output_file = "records.txt"
}

The result of above code will generate a new file named `records.txt` and this will be the data source file for `hcl-builder.py`
```

2; DO NOT DAMAGE YOUR REMOTE tfstate file: Please use `terraform local backend` type when you're working for rebuild the tfstate with `import comand`

[Local backend](https://www.terraform.io/docs/backends/types/local.html)

Example:
Please make sure you understand the command generated by:

`hcl_builder cmd records.txt alicloud_dns_record record_id "domain_name=name, host_record, type, value"`

## Usage

```bash
hcl_builder --help
usage: hcl-builder.py [-h]
                    ACTION RECORDS_OUTPUT_FILE resource_type ID_FIELD_NAME
                    KEYWORDS_NAMES

TF_HCL_GENERATOR.

positional arguments:
  ACTION               "hcl" or "cmd": generate hcl or import cmd
  RECORDS_OUTPUT_FILE  records_output_file name from data source
  resource_type        resource_type like alicloud_dns_record,
                       alicloud_instance, etc
  ID_FIELD_NAME        id_field_name the name of the ID field in
                       records_output_file
  KEYWORDS_NAMES       keywords_names example: "domain_name=name, host_record,
                       type, value"

optional arguments:
  -h, --help           show this help message and exit
```

## Example

Go to ./example

### Generate Terraform HCL

1. `terraform init`

2. `terraform plan`

This will generate the new output_file "records.txt"

The example output_file can be found [records.txt](./example/records.txt)

```json
[
	{
		"domain_name": "xxxxxxx.com",
		"host_record": "mail.awsdm",
		"line": "default",
		"locked": false,
		"priority": 1,
		"record_id": "3178431122706432",
		"status": "enable",
		"ttl": 600,
		"type": "MX",
		"value": "mx01.dm.sss.com."
	},
  .......
```

3. Build the parameters for `hcl_builder`

From above steps, we know the ID filed name for each resource is `record_id`, this will be our `ID_FIELD_NAME`

From [DNS Record resource](https://www.terraform.io/docs/providers/alicloud/r/dns_record.html) we know we need below keywords to build our HCL

```hcl
# Example: Create a new Domain record
resource "alicloud_dns_record" "record" {
  name        = "domainname"
  host_record = "@"
  type        = "A"
  value       = "192.168.99.99"
}
```

*BE NOTICE:*

- The key_names almost are the same as the `records.txt`, except the `Name of the domain`, it's should be the `name`, not the `domain_name` in output_file of "records.txt", so we need map `domain_name` to `name`.

- Also we don't want some filed like "line", "status", "locked", etc into hcl code, so we need `KEYWORDS_NAMES` to control how we generate the hcl code.

- The `KEYWORDS_NAMES` will be "domain_name=name, host_record, type, value"

- If you want more keywords, you can add them into KEYWORDS_NAMES.

*Final Parameters:*

```bash
ACTION                = hcl
RECORDS_OUTPUT_FILE   = records.txt
RESOURCE_TYPE         = alicloud_dns_record
ID_FIELD_NAME         = record_id
KEYWORDS_NAMES        = "domain_name=name, host_record, type, value"
```

4. Run `hcl_builder hcl records.txt alicloud_dns_record record_id "domain_name=name, host_record, type, value"`

Example Results:

```txt
bash-4.4# hcl_builder hcl records.txt alicloud_dns_record record_id "domain_name=name, host_record, type, value"

{
  "resource": {
    "alicloud_dns_record": {
      "alicloud_dns_record-3178387884972032": {
        "host_record": "submail.mail.submail",
        "name": "xxxxxxx.com",
        "type": "TXT",
        "value": "v=submail p=xxxxxxxx"
      },
......
```

Use [json2hcl](https://github.com/kvz/json2hcl) to generate HCL code.

```txt
hcl_builder hcl records.txt alicloud_dns_record record_id "domain_name=name, host_record, type, value" | json2hcl

"resource" "alicloud_dns_record" "alicloud_dns_record-3178387884972032" {
  "host_record" = "submail.mail.submail"

  "name" = "xxxxxxx.com"

  "type" = "TXT"

  "value" = "v=submail p=xxxxxxxx"
}
......
```

### Generate Terraform Import Commands

Follow above steps to build parameters and change "ACTION" to "cmd"

*Final Parameters:*

```bash
ACTION                = cmd
RECORDS_OUTPUT_FILE   = records.txt
RESOURCE_TYPE         = alicloud_dns_record
ID_FIELD_NAME         = record_id
KEYWORDS_NAMES        = "domain_name=name, host_record, type, value"
```

Run `hcl_builder cmd records.txt alicloud_dns_record record_id "domain_name=name, host_record, type, value"`

```txt
hcl_builder cmd records.txt alicloud_dns_record record_id "domain_name=name, host_record, type, value"
terraform import alicloud_dns_record.alicloud_dns_record-3178431122706432 3178431122706432
terraform import alicloud_dns_record.alicloud_dns_record-3178430699278336 3178430699278336
terraform import alicloud_dns_record.alicloud_dns_record-3178430192735232 3178430192735232
terraform import alicloud_dns_record.alicloud_dns_record-3178396024671232 3178396024671232
terraform import alicloud_dns_record.alicloud_dns_record-3178391278917632 3178391278917632
terraform import alicloud_dns_record.alicloud_dns_record-3178387884972032 3178387884972032
terraform import alicloud_dns_record.alicloud_dns_record-3178390481556480 3178390481556480
terraform import alicloud_dns_record.alicloud_dns_record-90748956 90748956
terraform import alicloud_dns_record.alicloud_dns_record-90748405 90748405
terraform import alicloud_dns_record.alicloud_dns_record-90748402 90748402
terraform import alicloud_dns_record.alicloud_dns_record-90644090 90644090
terraform import alicloud_dns_record.alicloud_dns_record-90748301 90748301
terraform import alicloud_dns_record.alicloud_dns_record-90748292 90748292
```

## How to rebuild tfstate file from HCL and CMD

Save the HCL to <your_named.tf> file

Make sure you read about "IMPORTANT: Must read"

Use the CMD "terraform import" to rebuild tfstate file.

## Demo

![demo](./img/demo.gif)

## TODO

- Test cases for python

- CI/CD
