# pylint: disable=import-outside-toplevel

import logging
import requests

_LOGGER = logging.getLogger(__name__)


def http_connect(host, port):
    """Establish connection with host/vcenter."""
    session = requests.Session()
    url = f'http://{host}:{port}/state'
    response = session.get(url)
    if response.ok:
        return True
    _LOGGER.error(response.text)
    return False


def get_datastore_info(datastore):
    """Get datastore information."""
    ds_summary = datastore.summary
    ds_name = ds_summary.name.replace(" ", "_").lower()
    ds_capacity = round(ds_summary.capacity / 1073741824, 2)
    ds_freespace = round(ds_summary.freeSpace / 1073741824, 2)
    ds_type = ds_summary.type.lower()

    ds_data = {
        "name": ds_name,
        "type": ds_type,
        "free_space_gb": ds_freespace,
        "total_space_gb": ds_capacity,
        "connected_hosts": len(datastore.host),
        "virtual_machines": len(datastore.vm),
    }

    _LOGGER.debug(ds_data)

    return ds_data
