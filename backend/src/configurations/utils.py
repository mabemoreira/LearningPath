from typing import Callable


def remove_swagger_generation_endpoint_preprocessing_hook(
    endpoints: list[tuple[str, str, str, Callable]]
):
    # your modifications to the list of operations that are exposed in the schema
    for path, path_regex, method, callback in endpoints:
        if path == "/swagger/schema/":
            endpoints.remove((path, path_regex, method, callback))
            break

    return endpoints
