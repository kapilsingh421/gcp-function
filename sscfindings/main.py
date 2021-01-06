mport os
import json
from google.cloud import storage

destination_bucket_name = os.environ.get('destination_bucket_name', 'nothing')
destination_bucket_name = destination_bucket_name
def test_list_all_findings(request , destination_bucket_name = destination_bucket_name):
    if request.method != 'POST':
        return abort(405)
    request_json = request.get_json()
    # [START list_all_findings]
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()
    storage_client = storage.Client()
    cuid = request_json['cuid']
    organization_id = request_json['organization_id']
    # organization_id is the numeric ID of the organization. e.g.:
    organization_id = organization_id
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    # The "sources/-" suffix lists findings across all sources.  You
    # also use a specific source_name instead.
    all_sources = "{org_name}/sources/-".format(org_name=org_name)
    finding_result_iterator = client.list_findings(all_sources)
    destination_bucket = storage_client.bucket(destination_bucket_name)
    destination_bucket_folder = cuid+".cc-data/"+cuid+".cc-data-sccfindings/"
    #destination_bucket = storage_client.get_bucket(destination_bucket_name)
    #destination_folder = cuid+".cc-data/"+cuid+".cc-data-auditlogs/"
    blob = destination_bucket.blob(destination_bucket_folder + "findings.json")
    
    f=open("/tmp/findings.json", "a+")
    for i, finding_result in enumerate(finding_result_iterator):
        s = "{}) 'name': {}, resource: {}, destination_bucket ,destination_bucket_folder: {}".format(
            i, finding_result.finding.name, finding_result.finding.resource_name, destination_bucket.name , destination_bucket_folder)
        print(s)
        f.write(str(finding_result))
        f.write(",\n")
    f.close()
    blob.upload_from_filename('/tmp/findings.json')
    os.remove("/tmp/findings.json")
    # [END list_all_findings] 
