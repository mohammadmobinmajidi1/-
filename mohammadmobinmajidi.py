import tkinter as tk
from tkinter import messagebox, filedialog
import os

class PhonebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("دفترچه تلفن دیجیتال")
        self.root.geometry("500x400")
        self.contacts = []
        
        # Create file if not exists
        self.filename = "phonebook.txt"
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()
        
        self.load_contacts()
        
        # GUI Elements
        self.create_widgets()
    
    def create_widgets(self):
        # Frame for input fields
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        # Labels and Entry widgets for contact information
        tk.Label(input_frame, text="نام:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="شماره تلفن:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(input_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="آدرس ایمیل:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="اضافه کردن", command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="حذف انتخاب شده", command=self.delete_contact).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="جستجو", command=self.search_contact).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="ذخیره", command=self.save_contacts).grid(row=0, column=3, padx=5)
        
        # Listbox to display contacts
        self.contacts_list = tk.Listbox(self.root, width=60, height=15)
        self.contacts_list.pack(pady=10)
        
        # Populate listbox
        self.update_listbox()
    
    def update_listbox(self):
        self.contacts_list.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_list.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")
    
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not name or not phone:
            messagebox.showerror("خطا", "نام و شماره تلفن الزامی هستند")
            return
        
        new_contact = {
            'name': name,
            'phone': phone,
            'email': email
        }
        
        self.contacts.append(new_contact)
        self.update_listbox()
        self.clear_entries()
        messagebox.showinfo("موفق", "مخاطب با موفقیت اضافه شد")
    
    def delete_contact(self):
        try:
            index = self.contacts_list.curselection()[0]
            self.contacts.pop(index)
            self.update_listbox()
            messagebox.showinfo("موفق", "مخاطب با موفقیت حذف شد")
        except IndexError:
            messagebox.showerror("خطا", "لطفاً مخاطبی را انتخاب کنید")
    
    def search_contact(self):
        search_term = tk.simpledialog.askstring("جستجو", "نام یا شماره تلفن را وارد کنید:")
        if search_term:
            found = False
            for contact in self.contacts:
                if search_term.lower() in contact['name'].lower() or search_term in contact['phone']:
                    messagebox.showinfo("نتایج جستجو", 
                                      f"نام: {contact['name']}\nشماره: {contact['phone']}\nایمیل: {contact['email']}")
                    found = True
            if not found:
                messagebox.showinfo("نتایج جستجو", "مخاطب یافت نشد")
    
    def save_contacts(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for contact in self.contacts:
                    f.write(f"{contact['name']},{contact['phone']},{contact['email']}\n")
            messagebox.showinfo("موفق", "مخاطبین با موفقیت ذخیره شدند")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ذخیره فایل: {str(e)}")
    
    def load_contacts(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        name, phone, email = line.strip().split(',', 2)
                        self.contacts.append({
                            'name': name,
                            'phone': phone,
                            'email': email
                        })
        except FileNotFoundError:
            pass
    
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookApp(root)
    root.mainloop()

