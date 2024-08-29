import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime

def init_db():
    """Initialize the database and create the table if it doesn't exist"""
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                firm TEXT,
                phone TEXT,
                email TEXT,
                note TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                date TEXT NOT NULL,
                topics TEXT NOT NULL,
                follow_up TEXT,
                outcome TEXT,
                FOREIGN KEY(contact_id) REFERENCES Contacts(id))''')
    conn.commit()
    conn.close()


def add_contact(name: str, role: str, firm: str, 
                phone: str, email: str, note: str):
    """
    Add a new contact to the database
    
    Args:
        name (str): Name of the contact, NOT NULL
        role (str): Role of the contact
        firm (str): Firm of the contact
        phone (str): Phone number of the contact
        email (str): Email of the contact
        note (str): Note about the contact
    """
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('INSERT INTO Contacts (name, role, firm, phone, email, note) VALUES (?, ?, ?, ?, ?, ?)',
              (name, role, firm, phone, email, note))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Contact added successfully')


def add_meeting(contact_id: int, date: str, topics: str, 
                follow_up: str, outcome: str):
    """
    Add a new meeting to the database
    
    Args:
        contact_id (int): ID of the contact, NOT NULL
        date (str): Date of the meeting, NOT NULL
        topics (str): Topics of the meeting, NOT NULL
        follow_up (str): Follow-up of the meeting
        outcome (str): Outcome of the meeting
    """
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    data = datetime.strptime(date, '%Y-%m-%d')
    c.execute('INSERT INTO Meetings (contact_id, date, topics, follow_up, outcome) VALUES (?, ?, ?, ?, ?)',
              (contact_id, data, topics, follow_up, outcome))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Meeting added successfully')


def get_contacts()->list:
    """Get all contacts from the database"""
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Contacts')
    contacts = c.fetchall()
    conn.close()
    return contacts


def get_meetings(contact_id: int)->list:
    """Get all meetings of a contact from the database"""
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Meetings WHERE contact_id=?', (contact_id,))
    meetings = c.fetchall()
    conn.close()



def main():

    # Initialize the database
    init_db()

    # Create GUI with Tkinter
    root = Tk()
    root.title('Personal CRM')

    # Add contact form
    Label(root, text="Name").grid(row=0)
    Label(root, text="Role").grid(row=1)
    Label(root, text="Firm").grid(row=2)
    Label(root, text="Phone").grid(row=3)
    Label(root, text="Email").grid(row=4)
    Label(root, text="Note").grid(row=5)

    name_entry = Entry(root)
    role_entry = Entry(root)
    firm_entry = Entry(root)
    phone_entry = Entry(root)
    email_entry = Entry(root)
    note_entry = Entry(root)

    name_entry.grid(row=0, column=1)
    role_entry.grid(row=1, column=1)
    firm_entry.grid(row=2, column=1)
    phone_entry.grid(row=3, column=1)
    email_entry.grid(row=4, column=1)
    note_entry.grid(row=5, column=1)

    # Contact list
    contacts_list = Listbox(root)
    contacts_list.grid(row=0, column=2, rowspan=4, padx=20)

    def update_contacts_list():
        contacts_list.delete(0, END)
        contacts = get_contacts()
        for contact in contacts:
            contacts_list.insert(END, f"{contact[0]} - {contact[1]}")

    def add_contact_callback():
        name = name_entry.get()
        role = role_entry.get()
        firm = firm_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        note = note_entry.get()
        if name:
            add_contact(name, role, firm, phone, email, note)
            name_entry.delete(0, END)
            role_entry.delete(0, END)
            firm_entry.delete(0, END)
            phone_entry.delete(0, END)
            email_entry.delete(0, END)
            note_entry.delete(0, END)
            update_contacts_list()
        else:
            messagebox.showerror('Error', 'Name is required')

    Button(root, text='Add Contact', command=add_contact_callback).grid(row=4, column=1, sticky=W, pady=4)

    # Add meeting form
    metings_text = Text(root, height=10, width=50)
    metings_text.grid(row=5, column=0, columnspan=3)

    def show_meetings_callback():
        contact_id = contacts_list.get(ACTIVE).split(' - ')[0]
        meetings = get_meetings(contact_id)
        metings_text.delete(1.0, END)
        for meeting in meetings:
            metings_text.insert(END, f"Data: {meeting[2]}\nArgomenti Discussi: {meeting[3]}\nFollow-up: {meeting[4]}\nRisultato: {meeting[5]}\n\n")

    Button(root, text='Show Meetings', command=show_meetings_callback).grid(row=4, column=2, sticky=W, pady=4)

    # Interface to add a meeting
    Label(root, text="Discussion Topics").grid(row=6)
    Label(root, text="Follow-up").grid(row=7)
    Label(root, text="Outcome").grid(row=8)

    topics_entry = Entry(root)
    follow_up_entry = Entry(root)
    outcome_entry = Entry(root)

    topics_entry.grid(row=6, column=1)
    follow_up_entry.grid(row=7, column=1)
    outcome_entry.grid(row=8, column=1)

    def add_meeting_callback():
        contact_id = contacts_list.get(ACTIVE).split(' - ')[0]
        discussion_topics = topics_entry.get()
        follow_up = follow_up_entry.get()
        outcome = outcome_entry.get()
        if contact_id and discussion_topics:
            add_meeting(contact_id, datetime.now().strftime('%Y-%m-%d'), discussion_topics, follow_up, outcome)
            topics_entry.delete(0, END)
            follow_up_entry.delete(0, END)
            outcome_entry.delete(0, END)
        else:
            messagebox.showerror('Error', 'Contact and Discussion Topics are required')
    
    Button(root, text='Add Meeting', command=add_meeting_callback).grid(row=9, column=1, sticky=W, pady=4)

    update_contacts_list()
    root.mainloop()


if __name__ == '__main__':
    main()
