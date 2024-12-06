import os
import json

class SimConfigFiles():
    def __init__(self, saved_dir):

        self.required_files = {
            'main': os.path.join(saved_dir, 'simconfig.json'),
            'eav24': os.path.join(saved_dir, 'Objects', 'Eav24_default.json'),
            'yas': os.path.join(saved_dir, 'Environments', 'yasmarina_env.json')
        }
        self.files = {}

        ok, status = self.valdiate()
        if ok:
            for name, path in self.required_files.items():
                with open(path, 'r', encoding='utf-8') as f:
                    self.files[name] = json.load(f)

    def valdiate(self):
        for name, path in self.required_files.items():
            if not os.path.exists(path):
                return (False, '{} not found'.format(path))
        return (True, '')

    def save(self):
        for name, path in self.required_files.items():
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.files[name], f, ensure_ascii=False, indent=4)

def apply_simconfig_preset(sim_saved_dir, preset_name):
    cfg_files = SimConfigFiles(sim_saved_dir)
    ok, status = cfg_files.valdiate()
    if not ok:
        print(status)
        return

    presets = {
        'default': apply_default_simconfig_preset,
        'lightweight': apply_lightweight_simconfig_preset,
        'a2rl': apply_a2rl_simconfig_preset
    }
    presets[preset_name](cfg_files)    

def apply_default_simconfig_preset(cfg_files):
    files = cfg_files.files
    
    print('globally enabling ROS2 and CAN')
    files['main']['interfaces']['bEnableRos2'] = True
    files['main']['interfaces']['bEnableCan'] = True

    print('ensuring default eav24 and yasmarina are reference in main config')
    if not 'Environments/yasmarina_env.json' in files['main']['environmentPaths']:
        print('missing yas environment. adding')
        print('{}'.format(files['main']['environmentPaths']))
    if not 'Objects/Eav24_default.json' in files['main']['objectTemplatePaths']:
        print('missing eav24. adding')

    cfg_files.save()


def apply_lightweight_simconfig_preset(cfg_files):
    files = cfg_files.files
    
    cfg_files.save()

def apply_a2rl_simconfig_preset(cfg_files):
    files = cfg_files.files
    
    cfg_files.save()