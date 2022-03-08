import yaml


def read_yaml(yaml_file):
    """读取yaml"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        print(value)
        return value


def write_yaml(data, yaml_file):
    """写yaml"""
    with open(yaml_file, 'w') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def truncate_yaml(yaml_file):
    """清空yaml"""
    with open(yaml_file, 'w') as f:
        f.truncate()

