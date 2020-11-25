import json
import tabulate as tb

class GameDataBase():
	def __init__(self):
		self.data = {}
		self.headers = ["name","size","company","rating","price"]
		self.types = {"name":str, "size":float, "company":str, "rating":float, "price":float}
		self.formatting = {"size":"{:.1f}","rating":"{:.1f}","price":"{:.2f}"}
		self.head_extras = {"size":" [Gb]","price":" [zł]"}
	#verifies ans parses the user input.
	def parse_input(self, raw_data):		
		if len(raw_data) != len(self.headers):
			return []

		clean_data = {}

		for i in range(len(self.headers)):
			h = self.headers[i]
			if self.types[h] == float:		#parse float values
				try:
					clean_data[h] = float(raw_data[i])
				except:
					print(f"-{h} isn't a float: \n\tdefaults to -1")
					clean_data[h] = -1
			elif self.types[h] == str:		#parse string values
				try:
					clean_data[h] = str(raw_data[i])
				except:
					print(f"-{h} isn't a string: \n\tdefaults to 'null'")
					clean_data[h] = 'null'
		return clean_data

	#Adds the record created from the parsed used input
	def add_record(self, raw_data, target_id = None):	#target id used for editing records
		clean_data = self.parse_input(raw_data)
		if target_id is None:
			i = 0	#finding the smallest available id
			while i in self.data.keys():	#may be changed later
				i+=1
		else:
			i = target_id	#using the prechosen id
		self.data.update({i : clean_data}) #adding the new record
		print("-added new record at index {}".format(i))

	#Removes record at the specified index if it exists, does nothing otherwise
	def remove_record(self, index):
		if(index in self.data.keys()):
			del self.data[index]
			print("-record {} has been deleted".format(index))
		else:
			print("-record {} does not exist".format(index))

	#Prints the database content to the command line using tabulate
	def show(self):
		if len(self.data) == 0:
			print("-the database is empty")
		else: 
			table = [[k]+list(v.values()) for k,v in self.data.items()]
			keys = ["id"]+self.headers
			print(tb.tabulate(table, headers=keys, numalign="right", showindex=True, floatfmt=("","",".1f","",".1f",".2f")))

	#return an array containing self.data as dict with keys from self.headers but with "id" as well
	def get_data(self):
		res = [dict({"id":k}, **v) for k,v in self.data.items()]
		return res
	
	#Allows for adding records via the command line
	def input_record(self):
		res = []
		for h in self.headers:
			res.append(input(f"Input {h} ({self.types[h]}): "))
		self.add_record(res)

	#Allows for removing records via the command line
	def input_remove(self):
		i = input("-Type the id of the record to be deleted: ")
		try:
			i = int(i)
			gdb.remove_record(i)
		except:
			print("-Invalid record id")
	
	# TODO maybe
	# def save_data(self):
	# def load_data(self):	


gdb = GameDataBase()
gdb.show()
gdb.add_record(["Battlefield", 30, "EA", 6.5, 69.99])
gdb.add_record(["Skyrim", 50, "Bethesda", 9, 45.99])
gdb.add_record(["IceTower", 0.5, "Bethesda", 3.7, 0])
gdb.add_record(["ImmortalPlanet", 2, "MonsterCouch", 9, 19.99])
gdb.add_record(["Fallout 97", 34.8, "Bethesda", 9, 37.13])
gdb.add_record(["Nostale", 3.2, "Gameforge", 8.3, 0])
	# gdb.remove_record(1)
gdb.show()

# print(gdb.get_data())

#Command line user interface
def loop():
	print("---The Game Data Base---")
	print("Type ADD to add a new record.")
	print("Type VIEW to display the table.")
	print("Type REM to remove a record.")
	print("Type EXIT to close the program.")
	while True:
		choice = input("Choose action: ")
		if choice == "ADD":
			gdb.input_record()
		elif choice == "VIEW":
			gdb.show()
		elif choice == "REM":
			gdb.input_remove();
		elif choice == "EXIT":
			break;
		else:
			print("Command unknown")

if __name__ == '__main__':
	loop()