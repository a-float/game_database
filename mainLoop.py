import PySimpleGUI as sg
from GameDataBase import *

sg.theme('Default1')

# ------ Make the Table Data ------
def createTableData(gdb, sortby = "id", sortdir = "ascending"):
	print(f"-sorting by {sortby} {sortdir}")
	rev = False if sortdir=="ascending" else True

	if sortby != "id":
		sort_key = lambda x: x[1][sortby]
	else:
		sort_key = lambda x: x[0]
	sorted_dict = {k: v for k, v in sorted(gdb.data.items(), key=sort_key, reverse=rev)}
	data = [[k]+list(v.values()) for k,v in sorted_dict.items()]
	print(data)
	for row in data:		#TODO possibly change it so its not that hardcoded like this
		if row[1+1] is not None:
			row[1+1] = "{:.1f}".format(float(row[1+1]))
		if row[3+1] is not None:
			row[3+1] = "{:.1f}".format(float(row[3+1]))
		if row[4+1] is not None:
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
						tooltip='Ma tabela')
	
	addRemoveFrame = sg.Frame(title="Record management", layout=[[sg.Button('Add record'), sg.Button('Remove records')]])
	sortingFrame = sg.Frame(title="Sort by", layout= [[ 
							 sg.Listbox(["id"] + gdb.headers,
								   size=(11,len(gdb.headers)+1),
								   default_values="id",
								   select_mode='LISTBOX_SELECT_MODE_SINGLE',
								   enable_events=True, 
								   k='-SORTBY-'),
						 	 sg.Listbox(["ascending", "descending"], 
								   size=(12,2),
								   default_values="ascending",
								   select_mode='LISTBOX_SELECT_MODE_SINGLE',
								   enable_events=True,
								   k='-SORTDIR-')]])
	rightContent = [
					  [addRemoveFrame],
					  [sortingFrame]
				   ]

	rightPanel = sg.Column(rightContent, 
							vertical_alignment="top",
							pad=(5,10),
							# expand_y=True,
							# background_color='lightyellow'
							)

	layout = [[leftPanel, sg.VSeperator(color='grey90'), rightPanel]]
	return layout

def createInputWindow(gdb):
	layout = [[sg.Text("{:10}:".format(h)), sg.Input(h[1:4])] for h in gdb.headers]
	layout.append([sg.Button("Add"), sg.Button("Cancel")])
	return sg.Window("Add a new record", keep_on_top="True", layout=layout, finalize=True)

def GUI(gdb):
	window1 = sg.Window('The Table Element', layout=createLayout(gdb), font=('Helvetica', 14), finalize=True)
	window2 = None

	while True:
		window, event, values = sg.read_all_windows()
		# print(event, values)
		if event == sg.WIN_CLOSED:
			window.close()
			if window == window2:       # if closing win 2, mark as closed
				window2 = None
			elif window == window1:     # if closing win 1, exit program
				break
		elif window == window2:
			if event == "Add":  #TODO add type parsing
				gdb.add_record(list(values.values())) #values is a dict with keys 0,1,2,3,..,len(inputs)
				print("Adding")
				window1['-TABLE-'].update(values = createTableData(gdb))
			window.close()  #close window2 anyway
			window2 = None
		elif window == window1:
			if event == 'Add record' and not window2:
				window2 = createInputWindow(gdb)
			elif event in ['-SORTBY-','-SORTDIR-']:
				window1['-TABLE-'].update(values = createTableData(gdb, values['-SORTBY-'][0], values['-SORTDIR-'][0]))
			elif event == "Remove records":
				ids_to_remove = sg.popup_get_text("Input multiple ids separated by space:", title="Remove record", size=(30,45))
				print(f"-removing {ids_to_remove}")
				for i in ids_to_remove.split(' '):
					try:
						i = int(i)
					except:
						print(f"invalid id {i}")
					gdb.remove_record(i)
				window1['-TABLE-'].update(values = createTableData(gdb))
	window.close()

GUI(gdb)