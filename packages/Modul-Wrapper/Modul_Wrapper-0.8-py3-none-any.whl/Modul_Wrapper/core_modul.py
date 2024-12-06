import importlib, ast, json

class Wrap:
	def __init__(kimin, modul_path):
		kimin.modul = kimin.Modul_Selector(modul_path)
		
	def Modul_Selector(kimin, cfg, **parameter):
		with open(cfg, 'r', encoding='UTF-8') as dataku:
			model = json.loads(dataku.read())['modul']
		modul = {i['class'] if i['defined'] == "" or not 'defined' in i else i['defined']:kimin.Path_Function(i) for i in model}
		no = 0
		for i in modul:
			if parameter.get('debug', True):
				print(f"[*] Import {model[no]['folder']} Load {model[no]['class']} as {i}")
			no +=1
		return modul
	
	def Path_Function(kimin, config, *args, **kwargs):
		class_name = config['class']
		path = f"{config['folder']}"
		if path == "":
			modul = __import__(class_name)
		else:
			if not config['file'] == "" and len(config['file']) > 0:
				ext = ".".join(config['file'])
				path = f"{path}.{ext}"
				modul = importlib.import_module(path)
				modul = getattr(modul, class_name)
			else:
				modul = importlib.import_module(path)
				modul = getattr(modul, class_name)
		
		
		return modul