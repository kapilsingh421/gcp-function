import argparse
def export_assets_gcs(request , filename = 'assest.json'): 
    if request.method != 'POST':
        return abort(405)
    request_json = request.get_json()
    print("data from function request")
    print(request_json)
    # [START asset_quickstart_export_assets] 
    from google.cloud import asset_v1 
    from google.cloud.asset_v1.proto import asset_service_pb2
    cuid = request_json['cuid']
    organization_id = request_json['organization_id']
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    dump_file_path = 'gs://assestinventory/'
    destination_bucket_folder = cuid+".gcp-data/"+cuid+".data-cloudassetinventory/"
    client = asset_v1.AssetServiceClient() 
    #parent = client.project_path(project_id) 
    output_config = asset_service_pb2.OutputConfig() 
    output_config.gcs_destination.uri = dump_file_path + destination_bucket_folder + filename
    response = client.export_assets(org_name, output_config) 
    print(response.result()) 
    # [END asset_quickstart_export_assets] 
    return "done", 200
