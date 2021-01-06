import argparse
import os

from google.cloud import logging

# [START logging_create_sink]
def create_sink(sink_name, filter_="project", unique_writer_identity=True):
    """Creates a sink to export logs to the given Cloud Storage bucket.

    The filter determines which logs this sink matches and will be exported
    to the destination. For example a filter of 'severity>=INFO' will send
    all logs that have a severity of INFO or greater to the destination.
    See https://cloud.google.com/logging/docs/view/advanced_filters for more
    filter information.
    """
    sink_name = os.environ.get('sink_name')
    sink_name = sink_name
    destination_bucket = os.environ.get('destination_bucket', 'nothing')
    logging_client = logging.Client()
    # The destination can be a Cloud Storage bucket, a Cloud Pub/Sub topic,
    # or a BigQuery dataset. In this case, it is a Cloud Storage Bucket.
    # See https://cloud.google.com/logging/docs/api/tasks/exporting-logs for
    # information on the destination format.
    destination = 'storage.googleapis.com/{bucket}'.format(
        bucket=destination_bucket)

    sink = logging_client.sink(
        sink_name,
        filter_,
        destination)

    if sink.exists():
        print('Sink {} already exists.'.format(sink.name))
        return

    sink.create()
    print('Created sink {}'.format(sink.name))
# [END logging_create_sink]
