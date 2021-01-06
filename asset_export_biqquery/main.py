import os
import argparse
dataset = os.environ.get('dataset', 'nothing')
def export_client_assets(request):
    if request.method != 'POST':
        return abort(405)
    request_json = request.get_json()
    
    # [START bigquery_query_destination_table]
    from google.cloud import asset_v1
    from google.cloud.asset_v1.proto import asset_service_pb2
    cuid = request_json['cuid']
    project_id = request_json['project_id'] 
   # if the table not exists a new table will be created
    #dataset = dataset
    #table= cuid+"_cc_gcp_data_cloudassets"

# If the destination table already exists and Force is TRUE, the table will be overwritten, if Force is not set or is FALSE and the table already exists, the export returns an error.

    #force = True

    client = asset_v1.AssetServiceClient()
    parent = client.project_path(project_id)
    output_config = asset_service_pb2.OutputConfig()
    output_config.bigquery_destination.dataset = dataset
    table= cuid+"_cc_gcp_data_cloudassets"
    force = True
    output_config.bigquery_destination.table = table
    output_config.bigquery_destination.force = force
    response = client.export_assets(parent, output_config)
    print(response.result())
