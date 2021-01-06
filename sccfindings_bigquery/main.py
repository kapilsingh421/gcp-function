import os
import json
from google.cloud import bigquery
dataset_id = os.environ.get('dataset_id', 'nothing')


def test_list_all_findings(request):
    if request.method != 'POST':
        return abort(405)
    request_json = request.get_json()
    # [START list_all_findings]
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()
    cuid = request_json['cuid']
    organization_id = request_json['organization_id']
    # organization_id is the numeric ID of the organization. e.g.:
    organization_id = organization_id
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    # The "sources/-" suffix lists findings across all sources.  You
    # also use a specific source_name instead.
    all_sources = "{org_name}/sources/-".format(org_name=org_name)
    finding_result_iterator = client.list_findings(all_sources)
  
    
    f=open("/tmp/findings.json", "a+")
    for i, finding_result in enumerate(finding_result_iterator):
        s = "{}) 'name': {}, resource: {}".format(
            i, finding_result.finding.name, finding_result.finding.resource_name)
        print(s)
        f.write(str(finding_result))
        f.write(",\n")
    
    bigquery_client= bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_id = cuid+"_cc_gcp_data_sccfindings"
    filename = '/tmp/findings.json'
    #dataset_id = dataset_id
    #table_id = "cc_data_sccfindings_"+cuid
    #dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = "WRITE_TRUNCATE"
    #job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.autodetect = True

    with open(filename, "rb") as source_file:
        job = bigquery_client.load_table_from_file(
               source_file,
               table_ref,
               location="US",  # Must match the destination dataset location.
               job_config=job_config,
        )  # API request
    f.close()
    job.result()  # Waits for table load to complete.

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
