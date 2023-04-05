from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

# read csv and create dictionary
df = pd.read_csv("data/french_words.csv")
df['learned'] = False
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    # filter out the words that have already been learned
    available_words = df[df['learned'] == False]
    if len(available_words) == 0:
        # if all words have been learned, reset the learned column
        df['learned'] = False
        available_words = df
    # get a random word and its translation
    row = available_words.sample().iloc[0]
    word = row['French']
    translation = row['English']
    # store the current card for later use
    current_card['row'] = row
    current_card['word'] = word
    current_card['translation'] = translation
    # display the word on the front of the card
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=word, fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    window.update()
    # schedule the card flip after a delay of 3 seconds
    flip_timer = window.after(3000, flip_card)


def flip_card():
    # display the English translation on the back of the card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card['translation'], fill="white")
    canvas.itemconfig(card_image, image=card_back_img)

    # create the buttons to mark the card as correct or incorrect
    def update_learned(learned):
        current_card['row']['learned'] = learned
        df.loc[current_card['row'].name] = current_card['row']
        df.to_csv('data/french_words.csv', index=False)
        next_card()

    unknown_button = Button(image=cross_image, command=lambda: update_learned(False))
    unknown_button.grid(column=0, row=1, padx=10, pady=10)
    known_button = Button(image=check_image, command=lambda: update_learned(True))
    known_button.grid(column=1, row=1, padx=10, pady=10)
    window.update()


# window and canvas
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=flip_card)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
