import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pygame

# Initialisation de pygame mixer
pygame.mixer.init()

albums = {
    "effect.jpg": "BUTTERFLY EFFECT",
    "goosebumps.jpg": "Goosebumps",
    "myeyes.jpg": "my eyes",
    "raindrops.jpg": "Raindrops"
}

# Correspondance image et audio
audio_samples = {
    "effect.jpg": "effect.mp3",
    "goosebumps.jpg": "goosebumps.mp3",
    "myeyes.jpg": "myeyes.mp3",
    "raindrops.jpg": "raindrops.mp3"
}

# Dictionnaire de couleurs pour musiques
theme_colors = {
    "effect.jpg": "#02398B",
    "goosebumps.jpg": "#910000",
    "myeyes.jpg": "#000000",
    "raindrops.jpg": "#9C00A7"
}

class AlbumQuiz:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#1e1e1e")
        self.master.geometry("400x600")
        self.master.resizable(False, False)
        self.master.title("Quiz Pochette d'Album")
        
        self.album_files = list(albums.keys())
        self.index = 0
        self.score = 0
        
        self.time_left = 0
        self.timer_id = None
        
        self.mode = tk.StringVar(value="simple")
        
        mode_frame = tk.Frame(master, bg="#1e1e1e")
        mode_frame.pack(pady=10)

        mode_label = tk.Label(master, text="Choisis ton mode :", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white")
        mode_label.pack()

        tk.Radiobutton(mode_frame, text="Simple", variable=self.mode, value="simple",
               bg="#1e1e1e", fg="white", selectcolor="#333").pack(side="left", padx=10)
        tk.Radiobutton(mode_frame, text="Hardcore", variable=self.mode, value="hardcore",
               bg="#1e1e1e", fg="white", selectcolor="#333").pack(side="left", padx=10)
        
        self.timer_label = tk.Label(master, text="", font=("Arial", 14, "bold"), fg="red", bg="#1e1e1e")
        self.timer_label.pack(pady=5)
        
        self.entry = tk.Entry(master, font=("Arial", 14), bg="#333", fg="white", insertbackground="white")
        self.entry.pack(pady=10)

        self.entry.bind("<Return>", lambda event: self.check_answer())
        
        self.button = tk.Button(master, text="Valider", command=self.check_answer,
                        bg="#444", fg="white", activebackground="#666", font=("Arial", 12, "bold"))
        self.button.pack(pady=5)

        self.score_label = tk.Label(master, text="Score: 0", font=("Arial", 12), bg="#1e1e1e", fg="white")
        self.score_label.pack(pady=10)

        self.label_image = None
        
        self.load_image_and_audio()

    def set_theme_by_album(self):
        album_name = self.album_files[self.index]
        bg_color = theme_colors.get(album_name, "#1e1e1e")
        self.master.configure(bg=bg_color)
        self.score_label.config(bg=bg_color, fg="white")
        self.timer_label.config(bg=bg_color)
        self.entry.config(bg="#333", fg="white", insertbackground="white")
        self.button.config(bg="#444", fg="white", activebackground="#666")
        if self.label_image:
            self.label_image.config(bg=bg_color)
    
    def load_image_and_audio(self):
        img_path = os.path.join("covers", self.album_files[self.index])
        image = Image.open(img_path)
        image = image.resize((300, 300))
        self.photo = ImageTk.PhotoImage(image)
        
        if self.label_image:
            self.label_image.config(image=self.photo)
        else:
            self.label_image = tk.Label(self.master, image=self.photo, bg="#1e1e1e")
            self.label_image.pack(pady=10)
        
        self.set_theme_by_album()
        
        self.play_audio_sample()
        
        if self.mode.get() == "hardcore":
            self.start_timer()
        else:
            self.timer_label.config(text="")
            if self.timer_id:
                self.master.after_cancel(self.timer_id)
                self.timer_id = None

    def play_audio_sample(self):
        pygame.mixer.music.stop()
        
        audio_file = audio_samples.get(self.album_files[self.index])
        if audio_file:
            audio_path = os.path.join("samples", audio_file)
            if os.path.exists(audio_path):
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
            else:
                print(f"Fichier audio introuvable : {audio_path}")
        else:
            print("Pas d'audio pour cet album")

    def start_timer(self):
        self.time_left = 5
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Temps restant : {self.time_left} sec")
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Temps écoulé !")
            self.timer_id = None
            messagebox.showerror("Temps écoulé", "Vous n'avez pas répondu à temps !")
            self.next_question()

    def check_answer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        
        user_answer = self.entry.get().strip()
        correct_answer = albums[self.album_files[self.index]]
        
        if self.mode.get() == "simple":
            if user_answer.lower() in correct_answer.lower():
                self.score += 1
                messagebox.showinfo("Bravo !", "Bonne réponse !")
            else:
                messagebox.showerror("Raté", f"Mauvaise réponse...\nLa bonne réponse était : {correct_answer}")
        elif self.mode.get() == "hardcore":
            if user_answer.lower() == correct_answer.lower():
                self.score += 1
                messagebox.showinfo("Bravo !", "Bonne réponse !")
            else:
                messagebox.showerror("Raté", f"Mauvaise réponse...\nLa bonne réponse était : {correct_answer}")
        
        self.score_label.config(text=f"Score: {self.score}")
        self.entry.delete(0, tk.END)
        self.next_question()

    def next_question(self):
        self.index += 1
        if self.index >= len(self.album_files):
            messagebox.showinfo("Fin du quiz", f"Quiz terminé ! Votre score final est {self.score}/{len(self.album_files)}")
            self.score = 0
            self.index = 0
            self.score_label.config(text=f"Score: {self.score}")
        
        self.load_image_and_audio()


if __name__ == "__main__":
    root = tk.Tk()
    quiz = AlbumQuiz(root)
    root.mainloop()
