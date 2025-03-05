import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def hide_text():

    file_path = filedialog.askopenfilename(title="Хабарламаны жасыру үшін файлды таңдаңыз")
    if not file_path:
        return

    secret_message = simpledialog.askstring("Құпия хабарлама", "Құпия хабарламаны енгізіңіз:")
    if not secret_message:
        return

    secret_message += "\0"
    message_bytes = secret_message.encode()
    size = len(message_bytes).to_bytes(4, byteorder="big")

    new_file_path = os.path.splitext(file_path)[0] + "_lsb" + os.path.splitext(file_path)[1]

    with open(file_path, "rb") as src, open(new_file_path, "wb") as dst:
        header = src.read(100)
        dst.write(header)
        data_bytes = bytearray(src.read())

        data = size + message_bytes
        data_bits = "".join(f"{byte:08b}" for byte in data)

        if len(data_bits) > len(data_bytes):
            messagebox.showerror("Қате", "Хабарлама бұл файлға сыймайды!")
            return

        for i in range(len(data_bits)):
            data_bytes[i] = (data_bytes[i] & 0b11111110) | int(data_bits[i])

        dst.write(data_bytes)

    messagebox.showinfo("Дайын", f"Хабарлама {new_file_path} файлына жасырылды")

def reveal_text():

    file_path = filedialog.askopenfilename(title="Хабарламаны шығару үшін файлды таңдаңыз")
    if not file_path:
        return

    with open(file_path, "rb") as file:
        file.seek(100)
        data_bytes = file.read()

        bits = [str(data_bytes[i] & 1) for i in range(32)]
        size = int("".join(bits), 2)

        bits = [str(data_bytes[i] & 1) for i in range(32, 32 + size * 8)]
        message_bytes = bytes(int("".join(bits[i:i + 8]), 2) for i in range(0, len(bits), 8))

        message = message_bytes.split(b"\0")[0].decode()

    messagebox.showinfo("Жасырылған хабарлама", message)

def main():
    root = tk.Tk()
    root.title("Стеганография")
    root.geometry("400x400")
    root.configure(bg="#f4f4f4")

    tk.Label(root, text="Әрекетті таңдаңыз:", font=("Arial", 14), bg="#f4f4f4").pack(pady=15)

    tk.Button(root, text="Хабарламаны жасыру", command=hide_text, width=30, height=2, bg="#4CAF50", fg="white").pack(pady=5)
    tk.Button(root, text="Хабарламаны шығару", command=reveal_text, width=30, height=2, bg="#008CBA", fg="white").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

