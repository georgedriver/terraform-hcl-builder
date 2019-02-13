// terraform {
//   required_version = "= 0.11.10"

//   backend "s3" {
//     bucket         = "terraform-state-xxxx-service-infrastructure"
//     dynamodb_table = "TerraformStatelock"
//     key            = "self-service/dns/alicloud/terraform.tfstate"
//     region         = "us-west-2"
//     profile        = "saml"
//   }
// }

data "alicloud_dns_records" "records_ds" {
  domain_name = "xxxxxxxx.com"
  // is_locked = false
  // host_record_regex = "^@"
  output_file = "records.txt"
}
