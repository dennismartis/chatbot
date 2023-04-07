import customtkinter
import openai
import threading


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("small example app")
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.entry = customtkinter.CTkEntry(master=self)
        self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.entry.bind("<Return>", self.submit_text)
        self.button = customtkinter.CTkButton(master=self, command=self.submit_text, text="Send message")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    def submit_text(self, *args, **kwargs):
        self.textbox.insert("1.0", "You: " + self.entry.get() + "\n\n")
        self.text = self.entry.get()
        self.entry.delete(0, "end")
        self.chat_response_threaded(self.text)
        
    def chat_response_threaded(self, text):
        # Define a worker function to execute chat_response in a separate thread
        def worker(text):
            response = self.chat_response(text)
            self.textbox.insert("1.0", "Bot: " + response + "\n\n")
            
        # Create a new thread and start it
        t = threading.Thread(target=worker, args=(text,))
        t.start()
        

    def chat_response(self, text):
        self.completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}])

        return(self.completion.choices[0].message["content"])

if __name__ == "__main__":
    app = App()
    app.mainloop()