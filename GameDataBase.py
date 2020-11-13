
import tabulate as tb

#TODO add max data size

class GameDataBase():
	headers = ["name","size","company","rating","price"]
	types = [str, float, str, float, float]
	def __init__(self):
		self.data = {}

	def parse_input(self, raw_data):
		if len(raw_data) != len(GameDataBase.headers):
			return []
		types = GameDataBase.types;
		clean_data = [None]*len(raw_data)
		for i in range(len(raw_data)):
			try:
				if types[i] == float:
					clean_data[i] = float(raw_data[i])
				elif types[i] == str and raw_data[i] != "":
					clean_data[i] = str(raw_data[i])
			except:
				print("ivalid input, defaults to None")
		return clean_data

	def add_record(self, raw_data):
		headers = GameDataBase.headers
		clean_data = GameDataBase.parse_input(self, raw_data)
		if clean_data == []:
			return False
		i = 0	#finding the smalles available id
		while i in self.data.keys():	#may be changed later
			i+=1
		print(clean_data)
		self.data.update({i : clean_data}) #adding the new record

		print("-added new record at index {}".format(i))


	def remove_record(self, index):
		if(index in self.data.keys()):
			del self.data[index]
			print("-record {} has been deleted.".format(index))
		else:
			print("-record {} does not exist.".format(index))

	def show(self):
		if len(self.data) == 0:
			print("-the database is empty.")
		else: 
			table = self.data.values()
			print(tb.tabulate(table, headers="keys", numalign="right", showindex=True,tablefmt="psql", floatfmt=("id","name",".1f","comp",".1f",".2f")))

# if __name__ != '__main__':
gdb = GameDataBase()
gdb.show()
gdb.add_record(["Battlefield", 30, "EA", 6.5, 69.99])
gdb.add_record(["Skyrim", 50, "Bethesda", 9, 45.99])
gdb.add_record(["IceTower", 0.5, "Bethesda", 3.7, 3.89])
gdb.add_record(["ImmortalPlanet", 2, "MonsterCouch", 9, 19.99])
gdb.add_record(["Fallout 97", 34.8, "Bethesda", 9, 37.13])
gdb.add_record(["Nostale", 3.2, "Gameforge", 8.3, 0])
	# gdb.remove_record(1)
	# gdb.show()
