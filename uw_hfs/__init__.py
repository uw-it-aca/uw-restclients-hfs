"""
This is the interface for interacting with the HFS Web Service.
"""

import logging
import json
from uw_hfs.dao import Hfs_DAO
from restclients_core.exceptions import DataFailureException


DAO = Hfs_DAO()
ERROR_MSG = "An error has occurred"
INVALID_ID_MSG = "not found in IDCard Database"
INVALID_PARAM_MSG = "Input for this method must be either"
logger = logging.getLogger(__name__)


def get_resource(url):
    response = DAO.getURL(url, {})
    logger.debug("%s ==status==> %s", url, response.status)

    response_data = str(response.data)

    if response.status != 200:
        raise DataFailureException(url, response.status, response_data)

    # 'Bug' with lib API causing requests with no/invalid user to return a 200
    if INVALID_PARAM_MSG in response_data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 400, json_data["Message"])

    if INVALID_ID_MSG in response_data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 404, json_data["Message"])

    if ERROR_MSG in response_data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 500, json_data["Message"])

    try:
        logger.debug("%s ==data==> %s", url, response.data.decode('utf-8'))
    except Exception as ex:
        # MUWM-2414
        logger.debug(
            "%s ==data==> Data not decodable to log file: %s", url, str(ex))

    return response.data
