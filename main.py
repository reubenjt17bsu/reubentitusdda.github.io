import tkinter as tk
from tkinter import messagebox
import requests
import html
import random
from PIL import Image, ImageTk

class TriviaGame:
    def __init__(self, root):
        # Initialize the TriviaGame class
        self.root = root
        self.root.title("Miss or Match - Trivia Challenge")

        # Load and display the start screen image
        self.start_screen_image = Image.open("Movie trivia.jpg")
        self.start_screen_image = self.start_screen_image.resize((700, 500), Image.BILINEAR)
        self.start_screen_image = ImageTk.PhotoImage(self.start_screen_image)
        
        self.start_screen_label = tk.Label(root, image=self.start_screen_image)
        self.start_screen_label.pack()

        # Add a button to start the quiz
        self.start_button = tk.Button(root, text="Begin Quiz", command=self.show_question_screen)
        self.start_button.pack()

        # Initialize variables for score and question counter
        self.score = 0
        self.question_counter = 1
        self.total_questions = 15

    def show_question_screen(self):
        # Remove the start screen components
        self.start_screen_label.pack_forget()
        self.start_button.pack_forget()

        # Set up a canvas for the background color
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='purple')
        self.canvas.pack()

        # Set up the rest of the GUI components for the quiz
        self.question_label = self.canvas.create_text(400, 150, text="", width=400, justify='center', fill='black', font=('Aptos', 15))
        self.answer_entry = tk.Entry(self.root)
        self.canvas.create_window(400, 400, window=self.answer_entry)

        self.options_frame = tk.Frame(self.root, bg='lightgray')
        self.canvas.create_window(400, 500, window=self.options_frame)

        self.score_label = tk.Label(self.root, text="Score: 0", font=('Aptos', 14), bg='lightgray')
        self.canvas.create_window(100, 50, window=self.score_label)

        self.question_counter_label = tk.Label(self.root, text="Question: 1", font=('Aptos', 15), bg='lightgray')
        self.canvas.create_window(700, 50, window=self.question_counter_label)

        self.submit_button = tk.Button(self.root, text="Submit Answer", command=self.check_answer)
        self.canvas.create_window(400, 550, window=self.submit_button)

        self.restart_button = tk.Button(self.root, text="Restart Quiz", command=self.restart_quiz, state=tk.DISABLED)
        self.canvas.create_window(400, 600, window=self.restart_button)

        # Fetch and display the first question
        self.get_question()

    def get_question(self):
        # Fetch a new trivia question from the Open Trivia Database API
        if self.question_counter <= self.total_questions:
            url = "https://opentdb.com/api.php?amount=1&category=11&difficulty=easy&type=multiple"
            response = requests.get(url)
            data = response.json()

            # Check if the API request was successful
            if data['response_code'] == 0:
                question = data['results'][0]['question']
                options = data['results'][0]['incorrect_answers']
                correct_answer = data['results'][0]['correct_answer']

                # Include the correct answer in the options list
                options.append(correct_answer)
                options = [html.unescape(option) for option in options]

                self.correct_answer = html.unescape(correct_answer)

                # Display the question text on the canvas
                self.canvas.itemconfig(self.question_label, text=html.unescape(question))

                # Clear the answer entry field and set default text
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.insert(0, "Your answer will appear here.")

                self.radio_var = tk.StringVar()
                self.radio_var.set(None)

                # Clear existing Radiobuttons
                for widget in self.options_frame.winfo_children():
                    widget.destroy()

                # Add new Radiobuttons for the current question
                random.shuffle(options)
                for i, option in enumerate(options):
                    tk.Radiobutton(self.options_frame, text=option, variable=self.radio_var, value=option, bg='lightgray').pack(side=tk.LEFT, padx=10)

                # Update question counter
                self.question_counter_label.config(text=f"Question: {self.question_counter}")

            else:
                # Display an error message if the API request fails
                messagebox.showerror("Error", "Failed to fetch question. Please try again.")
        else:
            # If all questions are answered, show the end of the quiz
            self.show_end_of_quiz()

    def check_answer(self):
        # Check if the user-selected answer is correct
        user_answer = self.radio_var.get()

        if user_answer is not None:
            # Update the answer entry field
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, user_answer)

            if user_answer == self.correct_answer:
                # If correct, update the score label and show a correct message box
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.show_correct_message_box()
            else:
                # If incorrect, show an incorrect message box
                self.show_incorrect_message_box()

            self.question_counter += 1

            if self.question_counter <= self.total_questions:
                # If there are more questions, get the next question after a delay
                self.root.after(1000, self.get_question)
            else:
                # If all questions are answered, show the end of the quiz
                self.show_end_of_quiz()
        else:
            # Warn the user if no answer is selected
            messagebox.showwarning("Warning", "Please select an answer.")

    def show_correct_message_box(self):
        # Display a correct answer message box in a separate window
        correct_window = tk.Toplevel(self.root)
        correct_window.title("Correct Answer")
        tk.Label(correct_window, text="Congratulations! Your answer is correct.", font=('Aptos', 14)).pack(padx=20, pady=20)

    def show_incorrect_message_box(self):
        # Display an incorrect answer message box in a separate window
        incorrect_window = tk.Toplevel(self.root)
        incorrect_window.title("Incorrect Answer")
        tk.Label(incorrect_window, text=f"Sorry, the correct answer is:\n{self.correct_answer}", font=('Aptos', 15)).pack(padx=20, pady=20)

    def show_end_of_quiz(self):
        # Display a message box at the end of the quiz with the final score
        messagebox.showinfo("End of Quiz", f"Quiz Completed!\nYour final score is: {self.score}")
        self.restart_button.config(state=tk.NORMAL)

    def restart_quiz(self):
        # Reset the game state for a new quiz
        self.score = 0
        self.question_counter = 1
        self.score_label.config(text="Score: 0")  # Reset the score label
        self.restart_button.config(state=tk.DISABLED)
        self.get_question()

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    game = TriviaGame(root)
    root.mainloop()
