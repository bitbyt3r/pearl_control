import requests

class PearlMini():
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.auth = (username, password)

    def get_params(self, params):
        r = requests.get(f"{self.url}/admin/get_params.cgi", params={k: 1 for k in params}, auth=self.auth)
        results = {}
        for line in r.text.split("\n"):
            if not " = " in line:
                continue
            key, value = line.split(" = ", 1)
            results[key] = value
        return results

    def set_params(self, params):
        pass

    def check_source_status(self):
        r = requests.get(f"{self.url}/api/sources", auth=self.auth)
        sources = r.json()['result']
        r = requests.get(f"{self.url}/api/sources/status?ids={','.join([x['id'] for x in sources])}", auth=self.auth)
        sources = {x['id']: x for x in sources}
        for source in r.json()['result']:
            if source['id'] in sources:
                sources[source['id']]['status'] = source['status']
        return sources

    def get_system_info(self):
        return self.get_params([
            "name",
            "description",
            "mac_address"
        ])
    
    def get_channels(self):
        return requests.get(f"{self.url}/api/channels", auth=self.auth).json()['result']

    def get_layouts(self, channel):
        return requests.get(f"{self.url}/api/channels/{channel}/layouts", auth=self.auth).json()['result']

    def change_layout(self, channel, layout):
        print(f"Changing layout of {channel} to {layout}")
        return
        r = requests.put(f"{self.url}/api/channels/{channel}/layouts/active", json={"id": layout}, auth=self.auth)
        return r.status_code == 200