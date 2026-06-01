import tkinter as tk

root = tk.Tk()
root.title("Todo App")
root.geometry("400x500")


entry = tk.Entry(root)
entry.pack(pady=10)

listbox = tk.Listbox(root)
listbox.pack(pady=10)

task_label = tk.Label(root, text='Tasks: 0')
task_label.pack()

completed_label = tk.Label(root, text='Completed: 0')
completed_label.pack()


scrollbar=tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

try:
    file=open('TODO list.txt','r', encoding='utf-8')
    read=file.readlines()
    for item in read:
        listbox.insert(tk.END,item.strip())
    file.close()
    

except FileNotFoundError:
    pass


def add_task():
    task = entry.get()
    if task!='':
        listbox.insert(tk.END, task)
        entry.delete(0,tk.END)
        save_tasks()
    count()
    update_completed()

def del_task():
    selected=listbox.curselection()
    if selected:
        listbox.delete(selected[0])
        save_tasks()
    count()
    update_completed()

def completed(event):
    selected = listbox.curselection()
    if selected:
        task = listbox.get(selected[0])

        if not task.startswith('\u2714'):
            listbox.delete(selected[0])
            listbox.insert(selected[0], '\u2714 ' + task)
        else:
            listbox.delete(selected[0])
            listbox.insert(selected[0],task[2:])

        save_tasks()
        update_completed()
    
def count():
    task_label.config(text=f"tasks:{listbox.size()}")


def del_all():
    listbox.delete(0,tk.END)
    save_tasks()
    count()
    update_completed()

def save_tasks():
    content=listbox.get(0,tk.END)
    file=open('TODO list.txt','w', encoding='utf-8')
    for item in content:
        file.write(item+'\n')
    file.close()

def update_completed():
    task=listbox.get(0,tk.END)
    completed=0
    for i in task:
        if i.startswith('\u2714'):
            completed+=1
    completed_label.config(text=f"completed:{completed}")
    save_tasks()
    print(completed)

def search_task():
    tasks = listbox.get(0, tk.END)
    search = entry.get()

    for index, task in enumerate(tasks):
        if search.lower() in task.lower():
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(index)
            listbox.see(index)
            break

edit_index = None

def edit_task():
    global edit_index
    selected = listbox.curselection()

    if selected:
        edit_index = selected[0]
        entry.delete(0, tk.END)
        entry.insert(0, listbox.get(edit_index))

def enter_pressed(event):
    if edit_index is not None:
        finish_edit()
    else:
        add_task()
    

def finish_edit(event=None):
    global edit_index

    if edit_index is not None:
        listbox.delete(edit_index)
        listbox.insert(edit_index, entry.get())
        entry.delete(0, tk.END)
        save_tasks()
        edit_index = None

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button = tk.Button(button_frame, text="Add", command=add_task)
button.pack(side=tk.LEFT, padx=2)

del_button = tk.Button(button_frame, text="Delete", command=del_task)
del_button.pack(side=tk.LEFT, padx=2)

search_button = tk.Button(button_frame, text="Search", command=search_task)
search_button.pack(side=tk.LEFT, padx=2)

edit_button = tk.Button(button_frame, text="Edit", command=edit_task)
edit_button.pack(side=tk.LEFT, padx=2)

save_button = tk.Button(button_frame, text="Save", command=save_tasks)
save_button.pack(side=tk.LEFT, padx=2)

del_all_button = tk.Button(button_frame, text="Delete All", command=del_all)
del_all_button.pack(side=tk.LEFT, padx=2)

root.bind('<Return>', enter_pressed)
listbox.bind('<Double-Button-1>',completed)

count()
update_completed()
root.mainloop()