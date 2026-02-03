import tkinter as tk
from tkinter import messagebox
import random

# ---------------------------
# Quiz Data (add/edit freely)
# ---------------------------
QUESTIONS = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars",
        "category": "Science"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen"],
        "answer": "William Shakespeare",
        "category": "Literature"
    },
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Rome", "Madrid"],
        "answer": "Paris",
        "category": "Geography"
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
        "answer": "Carbon Dioxide",
        "category": "Science"
    },
    {
        "question": "In computing, what does 'CPU' stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Control Program Utility", "Central Peripheral Unit"],
        "answer": "Central Processing Unit",
        "category": "Tech"
    },
    {
        "question": "Which is the largest ocean on Earth?",
        "options": ["Indian Ocean", "Atlantic Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": "Pacific Ocean",
        "category": "Geography"
    },
    {
        "question": "Which Bollywood actor is nicknamed 'King Khan'?",
        "options": ["Salman Khan", "Aamir Khan", "Shah Rukh Khan", "Saif Ali Khan"],
        "answer": "Shah Rukh Khan",
        "category": "Entertainment"
    },
    {
        "question": "What is 15 % of 200?",
        "options": ["25", "30", "35", "40"],
        "answer": "30",
        "category": "Math"
    },
    {
        "question": "Which language is used for styling web pages?",
        "options": ["HTML", "CSS", "Python", "SQL"],
        "answer": "CSS",
        "category": "Tech"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Claude Monet"],
        "answer": "Leonardo da Vinci",
        "category": "Art"
    },
    {
        "question": "Cricket: How many players per side on the field?",
        "options": ["9", "10", "11", "12"],
        "answer": "11",
        "category": "Sports"
    },
    {
        "question": "What does 'AI' stand for?",
        "options": ["Artificial Intelligence", "Automated Internet", "Advanced Interface", "Applied Informatics"],
        "answer": "Artificial Intelligence",
        "category": "Tech"
    },
    {
        "question": "The chemical symbol 'Na' stands for?",
        "options": ["Neon", "Sodium", "Nickel", "Nitrogen"],
        "answer": "Sodium",
        "category": "Science"
    },
    {
        "question": "Which Indian city is known as the 'Silicon Valley of India'?",
        "options": ["Hyderabad", "Bengaluru", "Pune", "Chennai"],
        "answer": "Bengaluru",
        "category": "Geography"
    },
    {
        "question": "What is the value of π (pi) approximately?",
        "options": ["2.14", "3.14", "3.41", "4.13"],
        "answer": "3.14",
        "category": "Math"
    },
]

# ---------------------------
# Config
# ---------------------------
TOTAL_QUESTIONS = 10           # how many questions per quiz (randomly sampled)
SECONDS_PER_QUESTION = 20      # countdown per question

# ---------------------------
# UI Theme Colors
# ---------------------------
COLORS = {
    "bg": "#121826",          # deep navy
    "card": "#1F2937",        # slate
    "accent": "#22D3EE",      # cyan
    "accent2": "#A78BFA",     # purple
    "text": "#F9FAFB",        # near white
    "muted": "#CBD5E1",       # gray-300
    "danger": "#F87171",      # red-400
    "success": "#34D399",     # green-400
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Master (Tkinter)")
        self.root.geometry("800x520")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(720, 480)

        self.all_questions = QUESTIONS[:]  # copy
        random.shuffle(self.all_questions)
        self.questions = self.all_questions[:TOTAL_QUESTIONS]

        # State
        self.current_index = -1
        self.score = 0
        self.timer_seconds = SECONDS_PER_QUESTION
        self.timer_id = None
        self.selected_option = tk.StringVar(value="")
        self.current_correct = None
        self.current_options = []

        # Header
        self.header_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.header_frame.pack(fill="x", pady=(18, 10), padx=18)

        self.title_label = tk.Label(
            self.header_frame,
            text="🎯 Quiz Master",
            font=("Segoe UI", 24, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["bg"]
        )
        self.title_label.pack(side="left")

        self.progress_label = tk.Label(
            self.header_frame,
            text="Question 0/0",
            font=("Segoe UI", 12),
            fg=COLORS["muted"],
            bg=COLORS["bg"]
        )
        self.progress_label.pack(side="right")

        # Card area
        self.card = tk.Frame(self.root, bg=COLORS["card"], bd=0, highlightthickness=0)
        self.card.pack(fill="both", expand=True, padx=18, pady=10)

        # Category + Timer
        topbar = tk.Frame(self.card, bg=COLORS["card"])
        topbar.pack(fill="x", padx=18, pady=(18, 8))

        self.category_label = tk.Label(
            topbar,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["accent2"],
            bg=COLORS["card"]
        )
        self.category_label.pack(side="left")

        self.timer_label = tk.Label(
            topbar,
            text=f"⏳ {SECONDS_PER_QUESTION}s",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["card"]
        )
        self.timer_label.pack(side="right")

        # Question text
        self.question_label = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 16, "bold"),
            wraplength=720,
            justify="left",
            fg=COLORS["text"],
            bg=COLORS["card"],
            padx=18,
            pady=10
        )
        self.question_label.pack(fill="x")

        # Options
        self.options_frame = tk.Frame(self.card, bg=COLORS["card"])
        self.options_frame.pack(fill="x", padx=12, pady=(4, 16))

        self.option_widgets = []
        for i in range(4):
            btn = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_option,
                value="",
                font=("Segoe UI", 12),
                fg=COLORS["text"],
                selectcolor=COLORS["card"],
                bg=COLORS["card"],
                activebackground=COLORS["card"],
                activeforeground=COLORS["text"],
                anchor="w",
                padx=14,
                pady=8,
                indicatoron=False,  # makes it look like buttons
                relief="ridge",
                bd=2,
                highlightthickness=0
            )
            btn.pack(fill="x", pady=6, padx=6)
            self.option_widgets.append(btn)

        # Footer buttons
        self.footer = tk.Frame(self.root, bg=COLORS["bg"])
        self.footer.pack(fill="x", padx=18, pady=(6, 16))

        self.next_btn = tk.Button(
            self.footer,
            text="Next ▶",
            command=self.next_question,
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["bg"],
            bg=COLORS["success"],
            activebackground=COLORS["success"],
            activeforeground=COLORS["bg"],
            padx=16,
            pady=10,
            bd=0
        )
        self.next_btn.pack(side="right", padx=(8, 0))

        self.quit_btn = tk.Button(
            self.footer,
            text="Quit ✖",
            command=self.quit_quiz,
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["bg"],
            bg=COLORS["danger"],
            activebackground=COLORS["danger"],
            activeforeground=COLORS["bg"],
            padx=16,
            pady=10,
            bd=0
        )
        self.quit_btn.pack(side="right", padx=(0, 8))

        # Keyboard shortcuts
        self.root.bind("<n>", lambda e: self.next_question())
        self.root.bind("<N>", lambda e: self.next_question())
        self.root.bind("<q>", lambda e: self.quit_quiz())
        self.root.bind("<Q>", lambda e: self.quit_quiz())

        # Start quiz
        self.go_to_next()

    # ---------------------------
    # Quiz Flow
    # ---------------------------
    def go_to_next(self):
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.finish_quiz()
            return

        q = self.questions[self.current_index]
        self.current_correct = q["answer"]

        # shuffle options fresh each time
        self.current_options = q["options"][:]
        random.shuffle(self.current_options)

        # reset selection & UI
        self.selected_option.set("")
        self.progress_label.config(text=f"Question {self.current_index + 1}/{len(self.questions)}")
        self.category_label.config(text=f"Category: {q.get('category','')}")
        self.question_label.config(text=q["question"])

        for i, opt_text in enumerate(self.current_options):
            w = self.option_widgets[i]
            w.config(text=opt_text, value=opt_text, state="normal", bg=COLORS["card"], fg=COLORS["text"], relief="ridge", bd=2)

        self.reset_timer()

    def next_question(self):
        # Check answer (if any selected)
        chosen = self.selected_option.get()
        if chosen:
            if chosen == self.current_correct:
                self.score += 1

        # Stop any running timer and proceed
        self.cancel_timer()
        self.go_to_next()

    def finish_quiz(self):
        self.cancel_timer()
        total = len(self.questions)
        percent = (self.score / total) * 100
        msg = f"Your Score: {self.score}/{total}\nAccuracy: {percent:.1f}%"
        # Replace card with summary
        for c in self.card.winfo_children():
            c.destroy()

        result_title = tk.Label(
            self.card, text="🏁 Quiz Complete!", font=("Segoe UI", 22, "bold"),
            fg=COLORS["accent2"], bg=COLORS["card"], pady=10
        )
        result_title.pack(pady=(40, 10))

        result_msg = tk.Label(
            self.card, text=msg, font=("Segoe UI", 16),
            fg=COLORS["text"], bg=COLORS["card"]
        )
        result_msg.pack(pady=10)

        tip = tk.Label(
            self.card,
            text="Tip: Press 'Q' to quit, or run again for a new random set!",
            font=("Segoe UI", 11),
            fg=COLORS["muted"], bg=COLORS["card"]
        )
        tip.pack(pady=(6, 20))

        self.next_btn.config(state="disabled")

    def quit_quiz(self):
        if messagebox.askyesno("Quit", "Do you really want to quit the quiz?"):
            self.root.destroy()

    # ---------------------------
    # Timer Logic
    # ---------------------------
    def reset_timer(self):
        self.cancel_timer()
        self.timer_seconds = SECONDS_PER_QUESTION
        self.timer_label.config(text=f"⏳ {self.timer_seconds}s", fg=COLORS["accent"])
        self.tick_timer()

    def tick_timer(self):
        self.timer_label.config(text=f"⏳ {self.timer_seconds}s")
        if self.timer_seconds <= 5:
            self.timer_label.config(fg=COLORS["danger"])
        elif self.timer_seconds <= 10:
            self.timer_label.config(fg=COLORS["accent2"])
        else:
            self.timer_label.config(fg=COLORS["accent"])

        if self.timer_seconds == 0:
            # time's up -> auto-next (no score change if not answered)
            self.timer_id = None
            self.auto_reveal_then_next()
            return

        self.timer_seconds -= 1
        self.timer_id = self.root.after(1000, self.tick_timer)

    def cancel_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def auto_reveal_then_next(self):
        # Briefly flash correct answer (visual feedback)
        try:
            for w in self.option_widgets:
                if w.cget("text") == self.current_correct:
                    w.config(bg=COLORS["success"], fg=COLORS["bg"], relief="solid", bd=2)
                else:
                    w.config(state="disabled", relief="ridge")
        except Exception:
            pass
        # move on after a short pause
        self.root.after(800, self.go_to_next)

# ---------------------------
# Boot
# ---------------------------
if __name__ == "__main__":
    # Sample a fresh random subset every run
    if TOTAL_QUESTIONS > len(QUESTIONS):
        TOTAL_QUESTIONS = len(QUESTIONS)  # guard

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
