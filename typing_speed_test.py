from tkinter import *

window = Tk()
window.title("Typing Speed Test")
window.minsize(width=600, height=600)
window.config(bg='#DDDAD0')
default_font = ("Arial",26)

outcome_comment = {20: "You have to up your game dude", 40: "Practice more", 60:"Thats the average speed", 70: "Impressive!", 90: "Daamn dude thats amazing!"}
pride_and_prejudice = ['The Bennets were engaged to dine with the Lucases, and again, during the chief of the day, was Miss Lucas so kind as to listen to Mr. Collins.',
                       'Elizabeth took an opportunity of thanking her. It keeps him in good humour - said she - and I am more obliged to you than I can express.',
                       'Charlotte assured her friend of her satisfaction in being useful, and that it amply repaid her for the little sacrifice of her time.',
                       'This was very amiable, but Charlotte’s kindness extended farther than Elizabeth had any conception of its object was nothing less than to secure her from any return of Mr. Collins’s addresses, by engaging them towards herself.',
                       'Such was Miss Lucas’s scheme, and appearances were so favourable, that when they parted at night, she would have felt almost sure of success if he had not been to leave Hertfordshire so very soon.',
                       'But here she did injustice to the fire and independence of his character, for it led him to escape out of Longbourn House the next morning with admirable slyness, and hasten to Lucas Lodge to throw himself at her feet.',
                       'He was anxious to avoid the notice of his cousins, from a conviction that, if they saw him depart, they could not fail to conjecture his design, and he was not willing to have the attempt known till its success could be known likewise, for, though feeling almost secure, and with reason, for Charlotte had been tolerably encouraging, he was comparatively diffident since the adventure of Wednesday.',
                       'His reception, however, was of the most flattering kind. Miss Lucas perceived him from an upper window as he walked towards the house, and instantly set out to meet him accidentally in the lane.','But little had she dared to hope that so much love and eloquence awaited her there.',
                       'In as short a time as Mr. Collins’s long speeches would allow, everything was settled between them to the satisfaction of both and as they entered the house, he earnestly entreated her to name the day that was to make him the happiest of men and though such a solicitation must be waived for the present, the lady felt no inclination to trifle with his happiness.',
                       'The stupidity with which he was favoured by nature must guard his courtship from any charm that could make a woman wish for its continuance, and Miss Lucas, who accepted him solely from the pure and disinterested desire of an establishment, cared not how soon that establishment were gained.']
class PNP():
    def __init__(self):
        self.time_started = False
        self.text = Text(height=4, width=90, wrap="word")
        self.text.config(bg='#DDDAD0', fg='#57564F', font=("Arial",20))
        self.text.grid(row=1,column=0)
        self.text_no = 0
        self.previous_text_count = 0
        self.previous_char_count = 0
        self.mistakes = False
        self.iterations = 5
        self.counter = 0
        self.init_label = Label(text="Start writing the text below", bg='#DDDAD0', bd=0)
        self.init_label.config(font=("Arial", 20, "bold"), bg='#DDDAD0', fg='#57564F')
        self.init_label.grid(row=0, column=0, pady=(40, 20))
        self.speed_label = Label(text="Your average speed is 0 WPM", bg='#DDDAD0', bd=0, pady=20)
        self.speed_label.config(font=default_font, bg='#DDDAD0', fg='#57564F')
        self.speed_label.grid(row=4, column=0)
        self.cps_label = Label(text="Characters per second: 0", bg='#DDDAD0', bd=0, pady=20)
        self.cps_label.config(font=default_font, bg='#DDDAD0', fg='#57564F')
        self.cps_label.grid(row=5, column=0)
        self.text.tag_config("wrong", foreground="RED")
        self.pap_text = Text(wrap="word", height=6)
        self.pap_text.insert("1.0",' '.join(pride_and_prejudice[self.text_no:(self.text_no+2)]))
        self.pap_text.config(font=default_font, state="disabled", bg='#DDDAD0', fg='#57564F', highlightthickness=0)
        self.pap_text.grid(row=2,column=0, padx=60, pady=40)
        self.pap_text.tag_config("current", background="#F8F3CE")
        self.pap_words = pride_and_prejudice[self.text_no].split()
    def start_timer(self, event):
        if not self.time_started:
            if not event.keycode in [16,17,18]:
                self.time_started = True
                self.char_per_second()
                self.repeat_task()

    def time_finished(self):
        print("Time finished")
        final_text = self.text.get("1.0", "end-1c")
        print(len(final_text.split()))
        self.text.unbind("<Key>")

    def repeat_task(self):
        final_text = self.text.get("1.0", "end-1c")
        text_count=len(final_text.split()) + self.previous_text_count

        self.speed_label.config(text=f"Your average speed is {int(text_count/(self.iterations/60))} WPM")
        if self.iterations < 60:
            self.iterations += 5
            self.text.after(5000, self.repeat_task)
        else:
            for value in outcome_comment:
                if value > text_count:
                    outcome_label = Label(text=outcome_comment[value], bg='#DDDAD0', bd=0, pady=20)
                    outcome_label.config(font=default_font, bg='#DDDAD0', fg='#57564F')
                    outcome_label.grid(row=3,column=0)
                    self.text.config(state="disabled")
                    self.time_started = False
                    break
            if text_count >= 90:
                outcome_label = Label(text="Bruh, youre deadass pro", bg='#DDDAD0', bd=0, pady=20)
                outcome_label.config(font=default_font, bg='#DDDAD0', fg='#57564F')
                outcome_label.grid(row=3,column=0)
                self.text.config(state="disabled")
                self.time_started = False

    def char_per_second(self):
        if self.time_started:
            self.counter += 0.1
            cps = round((len(self.text.get("1.0", "end-1c"))+self.previous_char_count)/self.counter, 1)
            self.cps_label.config(text=f"Characters per second: {cps}")
            self.text.after(100, self.char_per_second)
    def check_word(self, event):
        self.typed = self.text.get("1.0", "end-1c").split()
        index = len(self.typed) -1 
        

        self.pap_text.tag_remove("current", "1.0", "end")

        if 0 <= index < len(self.pap_words):
            start = f"1.{sum(len(w)+1 for w in self.pap_words[:index])}"
            end = f"1.{sum(len(w)+1 for w in self.pap_words[:index+1])-1}"
            self.pap_text.tag_add("current", start, end)

        typing = self.text.get("1.0", "end-1c")
        for i, letter in enumerate(typing):
            if i >= len(pride_and_prejudice[self.text_no]):
                if not self.text.tag_ranges("wrong"):
                    self.text_no += 1
                    self.previous_text_count += len(self.text.get("1.0", "end-1c").split())
                    self.previous_char_count += len(self.text.get("1.0", "end-1c"))
                    self.text.delete("1.0", "end-1c")
                    self.pap_text.config(state="normal") 
                    self.pap_text.delete("1.0", "end-1c")
                    self.pap_text.insert("1.0", ' '.join(pride_and_prejudice[self.text_no:(self.text_no+2)]))
                    self.pap_text.config(font=default_font, state="disabled", bg='#DDDAD0', fg='#57564F', highlightthickness=0)
                    self.pap_text.tag_config("current", background="#F8F3CE")
                    self.pap_words = pride_and_prejudice[self.text_no].split()
                    self.text.bind("<KeyRelease>", pnp.check_word)
                    break
            start = f"1.{i}"
            end = f"1.{i+1}"
            if i < len(pride_and_prejudice[self.text_no]):
                if letter.lower() != pride_and_prejudice[self.text_no][i].lower():
                    self.text.tag_add("wrong",start,end)

pnp = PNP()
pnp.text.bind("<KeyRelease>", pnp.check_word)
pnp.text.bind("<Key>", pnp.start_timer)
window.mainloop()