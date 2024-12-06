from typing import Literal

def api_request(uri, new_headers=None, new_data=None,
                method: Literal["GET", "PUT", "POST", "DELETE"] = "GET",
                request: Literal['basic', 'full'] = "basic", full_uri=False):
    if new_data is None:
        new_data = {}
    if new_headers is None:
        new_headers = {}
    if full_uri:
        url = uri
    else:
        url = f"http://{server}{api_base_dir}/{uri}"
    print(url)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": TOKEN,
        **new_headers
    }
    # data = {
    #    **new_data
    # }
    proxies = {
        "http": "",
        "https": "",
    }
    if method == "GET":
        response = requests.get(url, headers=headers, data=new_data, proxies=proxies)
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=new_data, proxies=proxies)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=new_data, proxies=proxies)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, data=new_data, proxies=proxies)
    else:
        return

    if request == "basic":
        return response.text
    elif request == "full":
        return response
    else:
        return response.text
