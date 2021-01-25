'''
simple GUI, 
args: array from final_data26486.pickle
click car model => car details
'''
import tkinter as tk
from main import load_pickle

class Car_Frame(tk.Tk):
    def __init__(self, pickle_file):
        super().__init__()
        
        self.car_arr = load_pickle(pickle_file)
        
        self.title('Autocentrum - baza danych')
        self.geometry("1200x900")
        self.resizable(width = False, height = False)

        self.listbox_car_list = tk.Listbox(self, height = 50, width = 90)
        self.listbox_car_list.grid(row = 1, column = 0, padx = 5)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row = 1, column = 1 ,sticky="nsw", padx = 1, ipady = 1)
        self.scrollbar.config(command = self.listbox_car_list.yview)
        self.listbox_car_list.config(yscrollcommand = self.scrollbar.set)
        self.listbox_car_list.bind("<<ListboxSelect>>", self.listbox_car_list_callback)
    
        self.frame1 = tk.Frame(self, borderwidth = 1, height = 10, width = 200, relief = 'groove')
        self.current_car_text = tk.StringVar()
        self.current_car_text.set('')
        self.label_car_from_list = tk.Label(self.frame1, textvariable = self.current_car_text, width = 80, pady = 5, padx = 5) #, anchor = 'w'
        self.label_car_from_list.grid(row = 0, column = 0)
        self.frame1.grid(row = 0, column = 0, columnspan = 2, pady = 5)
        
        self.text_box = tk.Text(self, height = 50, width = 75)        
        self.text_box.grid(row = 1, column = 2, padx = 5)
        self.run_me()

        
    def listbox_car_list_callback(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        data = event.widget.get(index)
        for ind, el in enumerate(self.car_arr):
            if data == el['car_id']:
                self.current_car_text.set(data)
                self.text_box.delete('1.0', 'end')
                self.text_box.insert('end', '{}\n\n'.format(data))
                for key, values in el['car_primary'].items():
                    self.text_box.insert('end', '{}: {}\n'.format(key,values))
                self.text_box.insert('end', '\n')
                for item in el['transmission']:
                    for key, values in item.items():
                        self.text_box.insert('end', '{}: {}\n'.format(key,values))
                    self.text_box.insert('end', '\n')
        
    def run_me(self):
        new_arr = []
        self.listbox_car_list.delete(0, 'end')
        for ind, el in enumerate(self.car_arr): 
            if el['car_id']:
                new_arr.append(el['car_id'])
        new_arr.sort()
        for ind, el in enumerate(new_arr):
            self.listbox_car_list.insert(ind,el)
                
        
if __name__ == "__main__":
    root = Car_Frame('final_data26486.pickle')
    root.mainloop()
    
    

