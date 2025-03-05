import os

def hide_text(file_path, message, new_file_path):
    message += "\0"
    message_bytes = message.encode()
    size = len(message_bytes).to_bytes(4, byteorder="big")

    with open(file_path, "rb") as src, open(new_file_path, "wb") as dst:
        header = src.read(54)
        dst.write(header)
        pixels = bytearray(src.read())

        data = size + message_bytes
        data_bits = "".join(f"{byte:08b}" for byte in data)

        if len(data_bits) > len(pixels):
            raise ValueError("Файлға сыймайтын тым ұзақ хабарлама!")

        for i in range(len(data_bits)):
            pixels[i] = (pixels[i] & 0b11111110) | int(data_bits[i])

        dst.write(pixels)


def reveal_text(file_path):
    with open(file_path, "rb") as file:
        file.seek(54)
        pixels = file.read()

        bits = [str(pixels[i] & 1) for i in range(32)]
        size = int("".join(bits), 2)

        bits = [str(pixels[i] & 1) for i in range(32, 32 + size * 8)]
        message_bytes = bytes(int("".join(bits[i:i + 8]), 2) for i in range(0, len(bits), 8))

        return message_bytes.split(b"\0")[0].decode()


if __name__ == "__main__":
    action = input("1: Текст жасыру\n2: Текст шығару\nТаңдау: ")

    if action == "1":
        print("1: Фото (PNG, JPG)\n2: Видео (MP4)\n3: Аудио (WAV)")
        file_type = input("Таңдау: ")

        if file_type == "1":
            extension = ["png", "jpg", "bmp"]
        elif file_type == "2":
            extension = ["mp4"]
        elif file_type == "3":
            extension = ["wav"]
        else:
            print("Қате таңдау. Бағдарлама тоқтады.")
            exit()

        file_path = input(f"Енгізу файлының атын жаз ({'/'.join(extension)} форматында): ")
        new_file_path = input("Шығу файлының атын жаз: ")

        if not os.path.exists(file_path):
            print(f"Файл табылмады: {file_path}")
        else:
            secret_message = input("Жасырын текст: ")
            hide_text(file_path, secret_message, new_file_path)
            print(f"Текст жасырылды: {new_file_path}")

    elif action == "2":
        file_path = input("Шифрланған файлдың атын жаз: ")

        if not os.path.exists(file_path):
            print(f"Файл табылмады: {file_path}")
        else:
            extracted_message = reveal_text(file_path)
            print("Жасырын текст:", extracted_message)

    else:
        print("Енгізуде қателік.")


