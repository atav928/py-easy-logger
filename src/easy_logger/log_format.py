"""Log Formats."""

import datetime
from typing import Any
from collections import OrderedDict
import re

def splunk_format(**kwargs: Any) -> str:
    """
    Reformat a list of key:value pairs into a simple logging message for Splunk.

    :return: _description_
    :rtype: str
    """
    ordered: OrderedDict[str, Any] = OrderedDict(sorted(kwargs.items()))
    string: list[str] = [f"{str(key)}=\"{value}\"" for key, value in ordered.items()]
    return ','.join(string)


def splunk_hec_format(host: str, source: str,
                      sourcetype: str,
                      metrics_list: list[str] = None,
                      **kwargs: Any) -> dict[str, Any]:
    """
    Create a JSON style hec format.

    :param host: hostname
    :type host: str
    :param source_name: source of dataa
    :type source_name: str
    :param time: epoch timestamp. Defaults to System time now
    :type time: float
    :param metrics_list: list of metrics type fileds found in arguments
    :type metrics_list: list[str]
    :param index: Splunk Index Value
    :type index: str
    :param kwargs: key:value pairs to extract and format data structure
    :return: Splunk Hec Datastructure
    :rtype: dict[str,Any]
    """
    hec_json: dict[str, Any] = {
        "time": kwargs.pop("time", datetime.datetime.now().timestamp()),
        "host": host,
        "source": source,
        "sourcetype": sourcetype,
        "events": {}
    }
    if kwargs.get("index"):
        hec_json["index"] = kwargs.pop("index")
    if metrics_list:
        # Build HEC style Metrics
        hec_json["fields"] = {f"metric_name:{metric}": kwargs.pop(
            metric, None) for metric in metrics_list}
        hec_json["fields"] = dict(sorted(hec_json["fields"].items()))
    hec_json["events"] = {**hec_json["events"], **kwargs}
    hec_json["events"] = dict(sorted(hec_json["events"].items()))
    return hec_json


def reformat_exception(error: Exception) -> str:
    """
    Reformates Exception to print out as a string pass for logging

    :param error: caught excpetion
    :type error: Exception
    :return: error as string
    :rtype: str
    """
    resp: str = f"{type(error).__name__}: {str(error)}" if error else ""
    resp = re.sub(r"(\]|\[|\')", "", resp)
    return resp
