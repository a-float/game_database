import PySimpleGUI as sg
from piotroprojekt import *

sg.theme('Default1')

# ------ Make the Table Data ------
def createTableData():
	data = list(gdb.data.values())
	print("The data is:")
	print(data)
	print("original data:")
	print(gdb.data)
	for row in data:		#TODO possibly change it so its not that hardcoded like this
		print(row)
		if row[1]:
			row[1] = "{:.1f}".format(float(row[1]))
		if row[3]:
			row[3] = "{:.1f}".format(float(row[3]))
		if row[4]:
			row[4] = "{:.2f}".format(float(row[4]))
	return data

def createHeaders():
	heds = GameDataBase.headers[:] #using [:] to make a copy of the list
	heds[1] += ' [Gb]'
	heds[4] += ' [zł]'
	return heds


# ------ Window Layout ------
leftPanel = sg.Table(values=createTableData(), headings=createHeaders(), max_col_width=25,
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
rightContent = [
				  [sg.Button('Read'), sg.Button('Double'), sg.Button('New record'), sg.Button('New record')],
				  [sg.Text('Read = read which rows are selected')],
				  [sg.Text('Double = double the amount of data in the table')],
				  [sg.Text('Change Colors = Changes the colors of rows 8 and 9')]
			   ]

rightPanel = sg.Column(rightContent, 
						vertical_alignment="top",
						pad=(5,10),
						# expand_y=True,
						background_color='lightyellow')

layout = [[leftPanel, sg.VSeperator(color='grey90'), rightPanel]]

# ------ Create Window ------
window1 = sg.Window('The Table Element', layout=layout, font=('Helvetica', 11), finalize=True)
window2 = None

def createInputWindow():
	layout = [[sg.Text("{:10}:".format(h)), sg.Input(h[1:4])] for h in createHeaders()]
	layout.append([sg.Button("Add"), sg.Button("Cancel")])
	return sg.Window("Add a new record", keep_on_top="True", layout=layout, finalize=True)

# ------ Event Loop ------
while True:
	window, event, values = sg.read_all_windows()
	print(window, event, values)
	if event == sg.WIN_CLOSED:
		window.close()
		if window == window2:       # if closing win 2, mark as closed
			window2 = None
		elif window == window1:     # if closing win 1, exit program
			break
	elif window == window2:
		if event == "Add":  #TODO add type parsing
			print(list(values.values()))
			gdb.add_record(list(values.values())) #values is a dict with keys 0,1,2,3,..,len(inputs)
			print("Adding")
			window1['-TABLE-'].update(values = createTableData())
		window.close()  #close window2 anyway
		window2 = None
	elif window == window1:
		if event == 'Double':
			for i in range(len(data)):
				data.append(data[i])
			window['-TABLE-'].update(values=data)
		elif event == 'New record' and not window2:
			window2 = createInputWindow()
window.close()