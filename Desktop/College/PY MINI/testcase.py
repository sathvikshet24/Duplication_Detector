import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as font
import pandas as pd
from tkinter import filedialog,messagebox,Listbox,END,ttk
import pandas as pd
import os,re,shutil,glob

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
global sim_score,directory


window = tk.Tk()
window.state('zoomed')
window.title("DUPLICATION DETECTOR")
window['background']='#F9F6F0'
image1 = Image.open("C:/Users/SathviK_24/Desktop/College/PY MINI/Duplication_Detector.png")
test = ImageTk.PhotoImage(image1)

label1 = tk.Label(image=test)
label1.image = test

label1.place(x=0,y=0)

def select_files():
    files = filedialog.askopenfilenames()

def button1_callback(): 
    #Teacher's Module
    window.destroy()
    def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
    def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])

    def check_plagiarism(txt_files):
        global sim_score
        student_notes = [open(_file, encoding='utf-8').read() for _file in txt_files]
        vectors = vectorize(student_notes)
        s_vectors = list(zip(txt_files, vectors))
        plagiarism_results = {}
        for student_a, text_vector_a in s_vectors:
            new_vectors = s_vectors.copy()
            current_index = new_vectors.index((student_a, text_vector_a))
            del new_vectors[current_index]
            for student_b, text_vector_b in new_vectors:
                sim_score = similarity(text_vector_a, text_vector_b)[0][1]
                if(sim_score > 0):
                    sim_score = round(sim_score, 1)
                    student_pair = sorted((os.path.splitext(student_a)[0], os.path.splitext(student_b)[0]))
                    res = (student_pair[0]+' similar to '+ student_pair[1] + '------->>>>>  ')
                    plagiarism_results[res] = sim_score*100
        return plagiarism_results

    def show_results(results):
        res = ''
        for key, value in results.items():
            res += key + ' ' + str(value) + '\n' +'\n'
        result_text.set(res)

    root = tk.Tk()
    root.title("Plagiarism Checker")
    root.state('zoomed')
    root.title("Teacher's Module")
    root['background']='#F9F6F0'

    combo = tk.ttk.Combobox(root,values=['Assignment 1','Assignment 2'])
    combo.current(0)
    combo.place(x = 680,y = 75)

    value1 = combo.get()
    if(value1 == 'Assignment 1'):
        curr_dirc='C:/Users/SathviK_24/Desktop/College/PY MINI/Assignment 1'
    else:
        curr_dirc='C:/Users/SathviK_24/Desktop/College/PY MINI/Assignment 2'
    os.chdir(curr_dirc)
    txt_files = []
    for file in glob.glob("*.txt"):
        txt_files.append(file)

    check_button = tk.Button(root, text="Check Plagiarism",width=20,height=6, command=lambda : show_results(check_plagiarism(txt_files)))
    check_button.place(x = 680,y = 150)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text)
    result_label.place(x = 640,y = 260)

    def save_to_file():
        temp_file = "C:/Users/SathviK_24/Desktop/College/PY MINI/"+value1+".txt"
        text = result_text.get()
        with open(temp_file, "w") as file:
            file.write(text)
            messagebox.showinfo("Data stored in file")

    save_button = tk.Button(root, text="Save to File", command=save_to_file)
    save_button.place(x = 490, y = 650)

    def delete_directory():
        if os.path.exists(curr_dirc):
            shutil.rmtree(curr_dirc)
            print(f"{curr_dirc} has been deleted.")
        else:
            print(f"{curr_dirc} does not exist.")

    delete_button = tk.Button(root, text="Delete Directory", command=delete_directory)
    delete_button.place(x = 720 , y = 650)
    root.mainloop()

def button2_callback():
    # Student Window
    window.destroy()

    class App:
        def __init__(self, master):
            self.master = master
            self.name_label = tk.Label(master, text="Enter your USN:",font=('Times', 24))
            self.name_entry = tk.Entry(master)
            self.email_label = tk.Label(master, text="Enter your email:",font=('Times', 24))
            self.email_entry = tk.Entry(master,width=35)
            self.file_label = tk.Label(master, text="Select file(s):",font=('Times', 24))
            self.file_button = tk.Button(master, text="Browse", command=self.select_files)
            self.run_button = tk.Button(master, text="Run", command=self.run_script)
            self.name_label.place(x = 680,y = 50)
            self.name_entry.place(x = 680,y = 100,width=280,height=40)
            self.email_label.place(x = 680,y = 150)
            self.email_entry.place(x = 680,y = 200,width=280,height=40)
            self.file_label.place(x = 680,y = 250)
            self.file_button.place(x = 680,y = 300,width=100,height=40)
            self.selected_files_label = tk.Label(master, text="")
            self.selected_files_label.place(x = 680,y = 330)
            #self.combobox_var = tk.StringVar()
            self.combobox = tk.ttk.Combobox(master,values=["Assignment 1","Assignment 2"])
            self.combobox.current(0)
            self.combobox.place(x = 680,y = 400)
            self.file_button.place(x = 680,y = 470)
            self.run_button.place(x = 680,y = 530,width=100,height=40)

        
        def select_files(self):
            self.files = filedialog.askopenfilenames()
            self.selected_files_label.config(text="/n".join(self.files))

        def run_script(self):
            global directory
            if not self.name_entry.get() or not self.email_entry.get():
                tk.messagebox.showerror("Error", "Please enter your USN and email")
                return

            usn_pattern = r"^\d{1}[a-z-A-Z]{2}\d{2}[a-z-A-Z]{2}\d{3}$"
            if not re.match(usn_pattern, self.name_entry.get()):
                tk.messagebox.showerror("Error", "Invalid USN format")
                return

            email_pattern = r"^[\w\.\+-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, self.email_entry.get()):
                tk.messagebox.showerror("Error", "Invalid email format")
                return

            if self.selected_files_label.cget("text")=="":
                tk.messagebox.showerror("Error", "Please select a file")
                return

            self.name = self.name_entry.get()
            self.email = self.email_entry.get()

            #temp_name = self.combobox_var
            #print(temp_name)
            value = self.combobox.get()
            directory = os.path.join("C:/Users/SathviK_24/Desktop/College/PY MINI/",str(value))

            if not os.path.exists(directory):
                os.makedirs(directory)
            
            file_name = os.path.basename(str(self.files[0]))
            file_names = file_name.replace(os.path.splitext(file_name)[1], "")

            file_dirc = os.path.join(directory,file_name)
            shutil.copy(str(self.files[0]), file_dirc)

            df = pd.read_excel("C:/Users/SathviK_24/Desktop/College/PY MINI/input_data.xlsx")

            data = {"USN": self.name, "Email": self.email, "Files": file_names,"Assignment":value}

            df = df.append(data, ignore_index=True)

            df.to_excel("input_data.xlsx", index=False)
            tk.messagebox.showinfo("showinfo","The Data is Added to the excel sheet")
            
    root = tk.Tk()
    root.state('zoomed')
    root.config(background='#F9F6F0')
    app = App(root)
    root.mainloop()




myFont = font.Font(size=30)
# first button
button1 = tk.Button(text="Teacher", command=button1_callback)
button1['font'] = myFont
button1.place(x=350, y=700,height=70,width=250)

#second button
button2 = tk.Button(text="Student", command=button2_callback)
button2['font'] = myFont
button2.place(x=1000, y=700,height=70,width=250)

window.mainloop()
