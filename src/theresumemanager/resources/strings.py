import json
from ..core.tools.dictionary.dictTools import dict2obj

strings = dict2obj(json.load(open("src/theresumemanager/resources/strings.json", "r")))