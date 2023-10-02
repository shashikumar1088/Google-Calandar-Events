import tkinter as tk
from tkinter import ttk, messagebox
from events import Events
from datetime import datetime
import time
import threading
import pyttsx3


class AppWindow(tk.Tk, Events):
    def __init__(self):
        super().__init__()
        self._initiateEt()
        self.createWindow()
        self.startThread()
    
    def startThread(self):
        # Create a thread to run the function in the background.
        thread = threading.Thread(target=self.getUpcomingFirst)

        # Start the thread.
        thread.start()

    def getUpcomingFirst(self):
        while True:
            time.sleep(1)
            eList = self.getUpcoming(0, 1)
            if not eList:
                break
            event = eList[0]
            eventDate = self._formatDate(event['start_date'])
            today = self._formatDate(self._today())
            print(f"{today} != {eventDate}")
            if today != eventDate:
                break

            evtDateTime = self._formatToDateTimeObj(event['start_date'])
            todayObj = self._formatToDateTimeObj(self._today())
            minutes = (evtDateTime - todayObj).total_seconds() / 60
            print(minutes)
            if 10 == minutes :
                msg = f'''Your upcoming event "{event['summary']}" is scheduled at "{eventDate}"'''
                self.speak(msg)            
                messagebox.showinfo("Reminder", msg)
            if 0 == minutes :
                msg = f'''Your schedule for "{event['summary']}" is lined up.'''
                messagebox.showinfo("Reminder", msg)
                self.speak(msg)
                self.refreshData()
    
    def createWindow(self):
        self.title("Google Calander Events")
        wWidth = 400
        wHeight = 300
        sWidth = self.winfo_screenwidth()
        sHeight = self.winfo_screenheight()
        xAxis = sWidth - wWidth
        yAxis = sHeight - wHeight - 70
        self.geometry(f"{wWidth}x{wHeight}+{xAxis}+{yAxis}")

        self.createTable()
        self.addClearBtn()
        self.addSyncBtn()

    def refreshData(self):        
        if self.table.winfo_exists():
            for row in self.table.get_children():
                self.table.delete(row)
            for i, event in enumerate(self.getUpcoming()):
                bg_color = "lightblue" if i % 2 == 0 else "lightgreen"
                self.table.insert("", "end", values=(event['summary'],event['start_date'],), tags=(bg_color,))
                self.table.tag_configure(bg_color, background=bg_color)
        
        self.startThread()

    def createTable(self):
        # Create a Treeview widget (table)
        self.table = ttk.Treeview(self, columns=("Event", "Schedule"), show="headings")
        self.table.heading("Event", text="Event")
        
        self.table.heading("Schedule", text="Scheduled On")
        self.table.pack(fill=tk.BOTH, expand=True)

        for i, event in enumerate(self.getUpcoming()):
            bg_color = "lightblue" if i % 2 == 0 else "lightgreen"
            self.table.insert("", "end", values=(event['summary'],event['start_date'],), tags=(bg_color,))
            self.table.tag_configure(bg_color, background=bg_color)

    def addClearBtn(self):
        # Create a Sync button
        clear_button = ttk.Button(self, text="Clear", style="TButton", command=self.doClear)
        clear_button.pack(side='left', padx=10, pady=10, anchor="se")

    def addSyncBtn(self):
        # Create a Sync button
        sync_button = ttk.Button(self, text="Sync", style="TButton", command=self.doSync)
        sync_button.pack(side='right', padx=10, pady=10)

    def doClear(self):
        self.clear()
        self.refreshData()
        messagebox.showinfo("Clear Alert", "Data is cleared!")

    def doSync(self):
        try:
            self.syncFromGoogle()
            self.refreshData()
            messagebox.showinfo("Sync Alert", "Data refreshed!")
        except Exception as e:
            messagebox.showinfo("Sync Alert", e)
    
    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
    # app.getUpcomingFirst()
