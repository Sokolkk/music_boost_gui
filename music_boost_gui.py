import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

# === Настройки по умолчанию ===
music_gain_default = 1.5
voc_gain_default = 0.7
bass_gain_default = 6
supported_formats = (".mp3", ".wav", ".flac", ".ogg", ".m4a")

# === Функция обработки трека ===
def process_track(file_path, music_gain, voc_gain, bass_gain):
    try:
        track_name = os.path.splitext(file_path)[0]
        output_file = f"{track_name}_enhanced.mp3"

        # Проверяем наличие ffmpeg
        if not shutil.which("ffmpeg"):
            messagebox.showerror("Ошибка", "ffmpeg не найден в PATH!")
            return

        # Усиление музыки, вокала и баса с очисткой метаданных
        ffmpeg_cmd = f'''ffmpeg -y -i "{file_path}" -filter_complex "[0:a]volume={music_gain}[mus];[0:a]volume={voc_gain}[voc];[mus][voc]amix=inputs=2:normalize=0, bass=g={bass_gain}[a]" -map "[a]" -map_metadata -1 "{output_file}"'''
        subprocess.run(ffmpeg_cmd, shell=True, check=True)

        # Удаляем исходный файл
        os.remove(file_path)
        print(f"✅ {output_file} готов!")

    except Exception as e:
        print(f"❌ Ошибка с {file_path}: {e}")

# === GUI ===
from tkinter import ttk

def browse_folder():
    folder = filedialog.askdirectory()
    folder_path.set(folder)

def start_processing():
    folder = folder_path.get()
    if not folder:
        messagebox.showwarning("Внимание", "Выберите папку с треками!")
        return

    music_gain = music_slider.get()
    voc_gain = voc_slider.get()
    bass_gain = bass_slider.get()

    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(supported_formats)]
    if not files:
        messagebox.showinfo("Инфо", "В папке нет поддерживаемых аудиофайлов.")
        return

    for f in files:
        process_track(f, music_gain, voc_gain, bass_gain)

    messagebox.showinfo("Готово", "Все треки обработаны!")

# === Настройка окна GUI ===
root = tk.Tk()
root.title("Music Boost GUI — Clean Metadata")

folder_path = tk.StringVar()

# --- Выбор папки ---
frame_folder = tk.Frame(root)
frame_folder.pack(pady=5, padx=10, fill=tk.X)
tk.Label(frame_folder, text="Папка с треками:").pack(side=tk.LEFT)
tk.Entry(frame_folder, textvariable=folder_path, width=50).pack(side=tk.LEFT, padx=5)
tk.Button(frame_folder, text="Обзор", command=browse_folder).pack(side=tk.LEFT, padx=5)

# --- Ползунки ---
tk.Label(root, text="Громкость музыки (фон)").pack(pady=5)
music_slider = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL)
music_slider.set(music_gain_default)
music_slider.pack(fill=tk.X, padx=20)

tk.Label(root, text="Громкость вокала").pack(pady=5)
voc_slider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
voc_slider.set(voc_gain_default)
voc_slider.pack(fill=tk.X, padx=20)

tk.Label(root, text="Усиление баса (дБ)").pack(pady=5)
bass_slider = tk.Scale(root, from_=0, to=12, resolution=1, orient=tk.HORIZONTAL)
bass_slider.set(bass_gain_default)
bass_slider.pack(fill=tk.X, padx=20)

# --- Кнопка старта ---
tk.Button(root, text="Запустить обработку", command=start_processing, bg="green", fg="white").pack(pady=20)

root.mainloop()
