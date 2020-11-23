import PySimpleGUI as sg
from GameDataBase import *

sg.theme('Default1')

# ------ Make the Table Data ------
def createTableData(gdb, sortby = "id", sortdir = "ascending"):
	rev = False if sortdir=="ascending" else True

	if sortby != "id":
		sort_key = lambda x: x[1][sortby]
	else:
		sort_key = lambda x: x[0]
	sorted_dict = {k: v for k, v in sorted(gdb.data.items(), key=sort_key, reverse=rev)}
	data = [[k]+list(v.values()) for k,v in sorted_dict.items()]
	#print(data)
	for row in data:		#TODO possibly change it so its not that hardcoded like this
		if row[1+1] != 'null':
			row[1+1] = "{:.1f}".format(float(row[1+1]))
		if row[3+1] != 'null':
			row[3+1] = "{:.1f}".format(float(row[3+1]))
		if row[4+1] != 'null':
			row[4+1] = "{:.2f}".format(float(row[4+1]))
	return data

def createHeaders(gdb):
	heds = gdb.headers[:] #using [:] to make a copy of the list
	heds[1] += ' [Gb]'
	heds[4] += ' [zł]'
	heds = ["id"] + heds
	return heds

def createLayout(gdb):
	leftPanel = sg.Table(values=createTableData(gdb), headings=createHeaders(gdb), max_col_width=25,
						# background_color='light blue',
						# auto_size_columns=True,
						display_row_numbers=True,
						justification='center',
						num_rows=18,
						alternating_row_color='grey90',
						key='-TABLE-',
						row_height=24,
						selected_row_colors=('black','SteelBlue2'),
						header_background_color='SteelBlue2',
						vertical_scroll_only=False,
						enable_events=True,
						tooltip='The GameDataBase table')
	
	addRemoveFrame = sg.Frame(title="Record management", layout=[[sg.Button('Add record'), sg.Button('Remove records')],[sg.Button('Edit record')]])
	sortingFrame = sg.Frame(title="Sort by", layout= [[ 
							 sg.Listbox(["id"] + gdb.headers,
								   size=(11,len(gdb.headers)+1),
								   default_values="id",
								   select_mode='LISTBOX_SELECT_MODE_SINGLE',
								   enable_events=True, 
								   k='-SORTBY-'),
						 	 sg.Listbox(["ascending", "descending"], 
							 	   pad=((0,60),(0,0)),
								   size=(12,2),
								   default_values="ascending",
								   select_mode='LISTBOX_SELECT_MODE_SINGLE',
								   enable_events=True,
								   k='-SORTDIR-')]])

	logFrame = sg.Frame(title="Log", font=12, layout = [[sg.Output(size=(30,9))]])

	rightContent = [
					  [addRemoveFrame],
					  [sortingFrame],
					  [logFrame]
				   ]

	rightPanel = sg.Column(rightContent, 
							vertical_alignment="top",
							pad=(5,10),
							)

	layout = [[leftPanel, sg.VSeperator(color='grey90'), rightPanel]]
	return layout

	#TODO add a global font setting

def createInputWindow(gdb):
	layout = [[sg.Text("{:10}:".format(h)), sg.Input(h[1:4])] for h in gdb.headers]
	layout.append([sg.Button("Add"), sg.Button("Cancel")])
	return sg.Window("Add a new record", font=('Helvetica', 14), keep_on_top="True", layout=layout, finalize=True)

def createEditWindow(gdb, id_to_edit):
	layout = [[sg.Text("{:10}:".format(h)), sg.Input(gdb.data[id_to_edit][h])] for h in gdb.headers]
	layout.append([sg.Button("Apply"), sg.Button("Cancel")])
	return sg.Window("Edit a record", font=('Helvetica', 14), keep_on_top="True", layout=layout, finalize=True)

def GUI(gdb):
	window1 = sg.Window('The Table Element', layout=createLayout(gdb), font=('Helvetica', 14), finalize=True)
	window2 = None
	window3 = None
	edited_id = None
	sortby = "id"		#kinga sketchy, should probably be changed
	sortdir = "ascending"

	while True:
		window, event, values = sg.read_all_windows()
		# print(event, values)
		if event == sg.WIN_CLOSED:
			window.close()
			if window == window2:       # if closing win 2, mark as closed
				window2 = None
			elif window == window1:     # if closing win 1, exit program
				break
		
		elif window == window2:	#ADD window
			if event == "Add":
				gdb.add_record(list(values.values())) #values is a dict with keys 0,1,2,3,..,len(inputs)
				updateTable(window1, sortby, sortdir)
			window.close()  #close window2 anyway
			window2 = None
		
		elif window == window3:	#EDIT window
			if event == "Apply":
				gdb.remove_record(edited_id)
				gdb.add_record(list(values.values()))
				updateTable(window1, sortby, sortdir)
			window.close()  #close window2 anyway
			window3 = None
		
		elif window == window1:
			if event == 'Add record' and not window2:
				window2 = createInputWindow(gdb)
			
			elif event in ['-SORTBY-','-SORTDIR-']:
				sortby = values['-SORTBY-'][0]
				sortdir = values['-SORTDIR-'][0]
				print(f"-sorting by {sortby} {sortdir}")
				updateTable(window1, sortby, sortdir)

			elif event == "Remove records":
				ids_to_remove = sg.popup_get_text("Input multiple ids separated by space:", title="Remove record", size=(30,45))
				print(f"-removing {ids_to_remove}")
				if ids_to_remove is not None: #if user cancelled the action
					for i in ids_to_remove.split(' '):
						try:
							i = int(i)
						except:
							print(f"invalid id {i}")
						gdb.remove_record(i)
				updateTable(window1, sortby, sortdir)
			
			elif event == "Edit record":
				#need to get the actual id taking sorting into account
				selected_ids = values['-TABLE-'] #currently selected table records
				if len(selected_ids) > 0: #at least one selected
					#chosing the most recent one, and [0] to acces the id column
					real_id = int(window['-TABLE-'].get()[selected_ids[-1]][0]) 
					edited_id = real_id
					window3 = createEditWindow(gdb, real_id)
				else:
					print("-select a table record first")
	window.close()

def updateTable(window1, sortby, sortdir):
	window1['-TABLE-'].update(values = createTableData(gdb, sortby, sortdir))

GUI(gdb)