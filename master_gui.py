from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar, OptionMenu, Checkbutton, IntVar, messagebox
import numpy as np
import read_ped_db
import collections
import matplotlib.pyplot as plt
import json
class MyFirstGUI:


    def __init__(self, master, dataframe):
        self.master = master

        master.title("EUROFUSION pedestal database filtering and plotting tool")
        with open('./filter_parameter.json', 'r') as read_file:
            filter_list = json.load(read_file)

        self.filter_store = filter_list

        # avialable plotting colours
        self.colours = ['black', 'red','green','blue','cyan']
        # Set up filter lists
        column_no = 0
        row_no = 0
        row_no_flag = 0

        # what column and row to start the flags
        self.row_no_flag=0
        self.column_no_flag = 5

        for filter in filter_list.keys():
            self.set_up_selction(master,row_no,row_no_flag,column_no,getattr(dataframe,filter),
                                 filter_list[filter],filter, set_size=0.1)
            if column_no > self.column_no_flag:
                # ensures no over lap with flag checkboxes
                column_no=0
            else:
                column_no+=1


        self.plot_button = Button(master, text="Plot selected filtered data", command=lambda: self.filter_db(dataframe))
        self.plot_button.grid(row=5, column=0, columnspan = 2, rowspan=2, sticky='NSEW',ipadx=20,ipady=20)

        self.setup_plotting_of_filter(dataframe)



    def setup_plotting_of_filter(self,dataframe):
        self.x_plot_label = Label(self.master, text='X axis')
        self.x_plot_label.grid(row=5, column=2, sticky=W)

        self.y_plot_label = Label(self.master, text='Y axis')
        self.y_plot_label.grid(row=6, column=2, sticky=W)

        # Variable for max current range
        xplot_selection = StringVar(self.master)
        xplot_selection.set(dataframe.columns[0])
        yplot_selection = StringVar(self.master)
        yplot_selection.set(dataframe.columns[0])

        self.x_plot_selection = OptionMenu(self.master, xplot_selection, *dataframe.columns)
        self.x_plot_selection.value = xplot_selection
        self.x_plot_selection.grid(row=5, column=3, sticky='NSEW')


        self.y_plot_selection = OptionMenu(self.master, yplot_selection, *dataframe.columns)
        self.y_plot_selection.value = yplot_selection
        self.y_plot_selection.grid(row=6, column=3, sticky='NSEW')



    def filter_db(self,df):
        for filter in self.filter_store:
            # print(filter)
            checkbox_attr_string = filter+'_checkbox'
            checkbox = getattr(self,checkbox_attr_string)
            if self.filter_store[filter]["var_type"] == 'min_max':
                # this means its drop down box with min and max values
                if (checkbox.var.get()) == 1:
                    # the user has selected this to be filtered upon
                    print("Filtering on - " + self.filter_store[filter]["label_name"])

                    minoption_attr_string = filter + '_options_min'
                    min_options = getattr(self, minoption_attr_string)

                    maxoption_attr_string = filter + '_options_max'
                    max_options = getattr(self, maxoption_attr_string)

                    min_val = (min_options.value.get())

                    max_val = (max_options.value.get())

                    try:
                        float(min_val)
                    except ValueError:
                        messagebox.showerror(title='Selection error',
                                               message='Please choose a min value for selected filter - '
                                                       + str(checkbox.cget("text")))
                        return

                    try:
                        float(max_val)
                    except ValueError:
                        messagebox.showerror(title='Selection error',
                                               message='Please choose a max value for selected filter - '
                                                       + str(checkbox.cget("text")))
                        return

                    df = df[(df[filter] >= float(min_val)) & (df[filter] <= float(max_val))]
            if self.filter_store[filter]["var_type"] == 'flag':
                # Filter on flags
                if checkbox.var.get() == 1:
                    # filter ON on checkbox
                    print('Filtering on - '+self.filter_store[filter]["label_name"])
                    df = df[(df[filter] == 1)]
                    print(df)


        self.df_filtered = df
        self.plot_plot_filtered_data()


    def plot_plot_filtered_data(self):
        selected_xdata_label = self.x_plot_selection.value.get()
        selected_ydata_label = self.y_plot_selection.value.get()

        filtered_df = self.df_filtered
        print('FILTER DATA')
        print(filtered_df)
        # Plot filtered selected data
        fig, ax = plt.subplots()
        ax.plot(filtered_df[selected_xdata_label],filtered_df[selected_ydata_label],'r*')
        plt.show(block=False)


    def get_df_limits(self,data,step_size):
        maxlim  = max(data)
        minlim  = min(data)
        # set up set size
        # note: we max_lim+step_size because np.arange doesn't include the end point. See docs.
        array = np.arange(minlim,maxlim+step_size,step_size)
        array = array.round(decimals=2)
        return array


    def set_up_selction(self,master,row_no, row_no_flag, column_no,data,filter_data,filter_name, set_size=0.1):

        # get max and min of the data
        data_range = self.get_df_limits(data,set_size)

        var1 = IntVar()
        obj=filter_name+'_checkbox'
        setattr(self,obj, Checkbutton(master, text=filter_data["label_name"], variable=var1, onvalue=1, offvalue=0))
        checkbox = getattr(self,obj)
        checkbox.var = var1

        if filter_data["var_type"] == 'flag':

            checkbox.grid(row=self.row_no_flag, column=self.column_no_flag, sticky='NSEW',padx=10,pady=10)

            # set up colour selectors for each flag
            # Variable for max current range
            flag_colour_data = StringVar(master)
            flag_colour_data.set('black')  # default value
            #
            obj = filter_name + '_flag_colour_option'
            setattr(self, obj, OptionMenu(master, flag_colour_data, *self.colours))
            flag_colour_selector = getattr(self, obj)
            flag_colour_selector.grid(row=self.row_no_flag, column=self.column_no_flag + 1, sticky='NSEW', padx=10,
                                      pady=10)
            flag_colour_selector.value = flag_colour_data

            self.row_no_flag += 1
        else:
            checkbox.grid(row=row_no, column=column_no, sticky='NSEW',padx=10,pady=10)



        if filter_data["var_type"] == "min_max":
            # Variable for max current range
            min_data = StringVar(master)
            # min_data.set(min(data_range))  # default value
            min_data.set('min')  # default value

            max_data = StringVar(master)
            # max_data.set(max(data_range))  # default value
            max_data.set('max')  # default value
            #
            obj=filter_name+'_options_min'
            setattr(self,obj,OptionMenu(master, min_data, *data_range))
            options_min_data = getattr(self,obj)
            options_min_data.grid(row=row_no+1, column=column_no, sticky='NSEW',padx=10,pady=10)
            options_min_data.value = min_data
            #
            obj=filter_name+'_options_max'
            setattr(self, obj, OptionMenu(master, max_data, *data_range))
            options_max_data = getattr(self, obj)
            options_max_data.grid(row=row_no+2, column=column_no, sticky='NSEW',padx=10,pady=10)
            options_max_data.value = max_data



root = Tk()
data_frame = read_ped_db.read_ped()
my_gui = MyFirstGUI(root,data_frame)
root.mainloop()