import PySimpleGUI as sg
from GameDataBase import *

sg.theme('Default1')

# ------ Make the Table Data ------
def createTableData(gdb, sortby = "id", sortdir = "ascending"):
	rev = False if sortdir=="ascending" else True
	sort_key = lambda x: x[sortby]
	
	sorted_data = sorted(gdb.get_data(), key=sort_key, reverse=rev)
	
	for row in sorted_data:								#for every dict
		for to_format, fmt in gdb.formatting.items():	#format every field that needs it
			row[to_format] = fmt.format(row[to_format]) 
	
	#returns list of lists
	return [list(x.values()) for x in sorted_data]	

def createHeaders(gdb):
	heds = ["id"]+gdb.headers[:] #using [:] to make a copy of the list
	for i in range(len(heds)):
		if heds[i] in gdb.head_extras:
			heds[i] += gdb.head_extras[heds[i]]
	return heds

def createLayout(gdb):
	leftPanel = sg.Table(values=createTableData(gdb), headings=createHeaders(gdb), max_col_width=25,
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
	
	btnPad = ((6,7),(0,6))
	mngmtFrame = sg.Frame(title="Record management", font=11, layout=[[sg.Button('Add record',pad=btnPad), sg.Button('Remove',pad=btnPad),sg.Button('Edit record',pad=btnPad)]])
	sortingFrame = sg.Frame(title="Sort by", font=11, layout= [[ 
							 sg.Listbox(["id"] + gdb.headers,
								   size=(11,len(gdb.headers)+1),
								   default_values="id",
								   select_mode='LISTBOX_SELECT_MODE_SINGLE',
								   enable_events=True, 
								   k='-SORTBY-'),
						 	 sg.Listbox(["ascending", "descending"], 
							 	   pad=((0,43),(0,0)),
								   size=(12,2),
								   default_values="ascending",
								   select_mode='LISTBOX_SELECT_MODE_SINGLE',
								   enable_events=True,
								   k='-SORTDIR-')]])

	#logFrame = sg.Frame(title="Log", font=12, layout = [[sg.Output(size=(30,9))]])
	logFrame = sg.Frame(title="Log", font=11, layout = [[sg.Text("qweqwe",size=(30,9))]])
	rightContent = [
					  [mngmtFrame],
					  [sortingFrame],
					  [logFrame]
				   ]

	rightPanel = sg.Column(rightContent, 
							vertical_alignment="top",
							pad=(0,0),
							)

	layout = [[leftPanel, sg.VSeperator(color='grey90'), rightPanel]]
	return layout

	#TODO add a global font setting

def createInputWindow(gdb):
	names = sg.Column([[sg.Text(h)] for h in gdb.headers ])
	inputs = sg.Column([[sg.Input(h[1:4], size=(30,1))] for h in gdb.headers ])
	layout = [[names, inputs]]
	layout.append([sg.Button("Add"), sg.Button("Cancel")])
	return sg.Window("Add a new record", font=('Helvetica', 14), keep_on_top="True", layout=layout, finalize=True)

def createEditWindow(gdb, id_to_edit):
	names = sg.Column([[sg.Text(h)] for h in gdb.headers ])
	inputs = sg.Column([[sg.Input(gdb.data[id_to_edit][h], size=(30,1))] for h in gdb.headers])
	layout = [[names, inputs]]
	layout.append([sg.Button("Apply"), sg.Button("Cancel")])
	return sg.Window("Edit a record", font=('Helvetica', 14), keep_on_top="True", layout=layout, finalize=True)

def GUI(gdb):
	window1 = sg.Window('The Table Element', layout=createLayout(gdb), font=('Helvetica', 14), finalize=True)
	window2 = None	#add new record window
	window3 = None	#edit exsiting record window
	edited_id = None	#the id of the last selected table record
	sortby = "id"		#kinda sketchy, should probably be changed
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
				gdb.remove_record(edited_id)			#delete the old one
				gdb.add_record(list(values.values()))	#add the new one
				updateTable(window1, sortby, sortdir)
			window.close() 								#close window3 anyway
			window3 = None
		
		elif window == window1:
			if event == 'Add record' and not window2:	#dont create window if its already open
				window2 = createInputWindow(gdb)
			
			elif event in ['-SORTBY-','-SORTDIR-']:
				sortby = values['-SORTBY-'][0]
				sortdir = values['-SORTDIR-'][0]
				print(f"-sorting by {sortby} {sortdir}")
				updateTable(window1, sortby, sortdir)

			elif event == "Remove":
				ids_to_remove = sg.popup_get_text("Input multiple ids separated by space:", title="Remove", font=('Helvetica', 11), size=(30,45))
				print(f"-removing {ids_to_remove}")
				if ids_to_remove is not None: #if user cancelled the action
					for i in ids_to_remove.split(' '):
						try:
							i = int(i)
						except:
							print(f"invalid id {i}")
						gdb.remove_record(i)
				updateTable(window1, sortby, sortdir)
			
			elif event == "Edit record" and not window3:	#dont create window if its already open
				#need to get the actual id taking sorting into account
				selected_ids = values['-TABLE-'] 			#currently selected table records
				if len(selected_ids) > 0: 					#at least one selected
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