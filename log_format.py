"""Log Formats."""

import datetime
from typing import Any
from collections import OrderedDict


def splunk_format(**kwargs: Any) -> str:
    """Reformat a list of key:value pairs into a simple logging message for Splunk.

    :return: _description_
    :rtype: str
    """
    ordered: OrderedDict[str, Any] = OrderedDict(sorted(kwargs.items()))
    string: list[str] = [f"{str(key)}=\"{value}\"" for key, value in ordered.items()]
    return ','.join(string)


def splunk_hec_format(host: str, source_name: str, metrics_list: list[str],
                      **kwargs: Any) -> dict[str, Any]:
    """Create a JSON style hec format.

    :param host: _description_
    :type host: str
    :param source_name: _description_
    :type source_name: str
    :param metrics_list: _description_
    :type metrics_list: list[str]
    :return: _description_
    :rtype: dict[str,Any]
    """
    hec_json: dict[str, Any] = {
        "time": datetime.datetime.utcnow().timestamp(),
        "host": host,
        "source_name": source_name,
        "fields": {f"metric_name:{metric}": kwargs.pop(metric, None) for metric in metrics_list}
    }
    hec_json["fields"] = {**hec_json["fields"], **kwargs}
    return hec_json
