import json

def load_config(config_file):
    import json
    with open(config_file, 'r') as file:
        return json.load(file)

def format_response(response):
    if isinstance(response, dict):
        return json.dumps(response, indent=4)
    return str(response)