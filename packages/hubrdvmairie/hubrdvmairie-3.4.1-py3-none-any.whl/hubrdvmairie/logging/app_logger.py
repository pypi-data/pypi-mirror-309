import logging
import sys
from http import HTTPStatus
from urllib.parse import quote

from fastapi import Request, Response
from httpx import Response as HTTPResponse


def get_stream_handler(formatter):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name, formatter):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(get_stream_handler(formatter))
    return logger


def get_extra_info(request: Request, response: Response):
    status_reasons = {x.value: x.name for x in list(HTTPStatus)}
    return {
        "req": {
            "url": quote(request.url.path, safe="/:"),
            "headers": {
                "host": quote(request.headers["host"], safe=":"),
                "accept": quote(
                    ("accept" in request.headers and request.headers["accept"]),
                    safe="/ ,*",
                )
                or None,
            },
            "method": request.method,
            "httpVersion": request.scope["http_version"],
            "originalUrl": quote(request.url.path, safe="/:"),
            "query": {},
        },
        "res": {
            "statusCode": response.status_code,
            "body": {
                "statusCode": response.status_code,
                "status": status_reasons.get(response.status_code),
            },
        },
        "protocol": "http",
        "response_time": response.response_time,
        "realip": request.client.host,
        "source_side": "Backend",
        "type": "access",
    }


def get_external_service_extra_info(response: HTTPResponse, editor_name=None):
    url_path = (
        response.request.url.scheme
        + "://"
        + response.request.url.host
        + response.request.url.path
    )
    return {
        "category": "external_service",
        "request": {"url": url_path, "method": response.request.method},
        "response": {"statusCode": response.status_code},
        "protocol": "http",
        "response_time": response.elapsed.microseconds / 1000,
        "source_side": "Backend",
        "type": "app",
        "editor_name": editor_name,
    }


def write_access_log_data(logger, request, response):
    try:
        logger.info(
            request.method + " " + request.url.path,
            extra={"extra_info": get_extra_info(request, response)},
        )
    except Exception as logging_e:
        logger.error("Logging Error: " + str(logging_e))


def write_external_service_data(logger, response, editor_name):
    try:
        url_path = (
            response.request.url.scheme
            + "://"
            + response.request.url.host
            + response.request.url.path
        )
        logger.info(
            "[Editor] " + response.request.method + " " + url_path,
            extra={
                "extra_info": get_external_service_extra_info(response, editor_name)
            },
        )
    except Exception as logging_e:
        logger.error("Logging Error write_external_service_data: " + str(logging_e))
