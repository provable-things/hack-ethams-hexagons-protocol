import sys
import json

import twitter
import provable


def load_config(file):
    """ Read the configuration file from a file """
    c = {}
    with open(file) as f:
        try:
            c = json.load(f)
        except Exception as e:
            print('Error: failed to load the configuration', e)
            sys.exit(1)
    return c

def get_module_from_str(module_name):
  """ Loads the correct module from the given name """
  if module_name == 'provable':
    return provable
  elif module_name == 'twitter':
    return twitter
  # Add more modules here...
  else:
    raise f"Error: module {module_name} not supported!"

def main():
    config = load_config('./config.json')
    
    print("Configuration loaded!")

    identity = config['identity']
    modules_enabled = config['modules_enabled']

    for module_entry in modules_enabled:
      social_module = get_module_from_str(module_entry['social_type'])
      oracle_module = get_module_from_str(module_entry['oracle_type'])

      args = module_entry['args']

      social_module.run(args, identity, oracle_module)


if __name__ == "__main__":
    main()
