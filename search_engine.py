import pandas as pd
import nltk
import math
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import customtkinter as ctk
import webbrowser
import os
# nltk.download('stopwords')
# nltk.download('punkt_tab')

stopwords = set(stopwords.words('english'))
stemmer = PorterStemmer()

def tokenize(text):
    if type(text) == str:
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        removed_stopwords = [i for i in tokens if i not in stopwords]
        stemmed_tokens = [stemmer.stem(i) for i in removed_stopwords]
        return stemmed_tokens
    else:
        return []


def tfidf(token):
    idf_dict = {}
    tf_dict = {}
    tfidf_dict = {}
    matches = {}

    exists = False

    for i in inverted_index:
        idf = math.log10(len(df) / len(inverted_index[i]))
        idf_dict[i] = idf

    for i, row in df.iterrows():
        tokens = row['processed_html']
        tf_dict[i] = {}

        for t in set(tokens):
            tf = tokens.count(t) / len(tokens)
            tf_dict[i][t] = tf

    for i in tf_dict:
        tfidf_dict[i] = {}
        for x in tf_dict[i]:
            tfidf_dict[i][x] = tf_dict[i][x] * idf_dict[x]

    for i in tfidf_dict:
        if token in tfidf_dict[i]:
            # print(token + "'s TF-IDF in document: " + str(i) + " is: " + str(tfidf_dict[i][token]))
            matches[i] = tfidf_dict[i][token]
            exists = True

    if exists == False:
        print(token + " not found in any document")

    return matches

def readFile(file):
    clean_file = file.split('/')[-1]
    # path = "C:\\Users\\josh\\PycharmProjects\\IR_Search_Engine\\videogame\\"
    path = os.getcwd() + "\\videogame\\"
    full_path = path + clean_file
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        clean = re.sub('<[^<]+?>', '', content)
        return clean
    except FileNotFoundError:
        return ""

def search(query):
    tokens = tokenize(query)
    scores = {}
    for i in tokens:
        matches = tfidf(i)
        for x in matches:
            if x in scores:
                scores[x] = scores[x] + matches[x]
            else:
                scores[x] = matches[x]
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return(ranked[:10])

def gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()
    app.geometry("800x700")
    app.title("Video Game Dataset Search Engine")

    app.configure(fg_color="#000000")

    retro_font = ("Courier New", 20, "bold")
    console_font = ("Consolas", 12)

    def on_search():
        query = search_bar.get()

        for widget in output.winfo_children():
            widget.destroy()

        if query == "":
            err = ctk.CTkLabel(output, text="ERROR: NO QUERY INPUTTED", font=retro_font, text_color="#FF0055")
            err.pack(pady=20)
            return

        results = search(query)

        if results == []:
            err = ctk.CTkLabel(output, text="ERROR: NO MATCHES FOUND", font=retro_font, text_color="#FF0055")
            err.pack(pady=20)
        else:
            a = 1
            for i in results[:10]:
                id = i[0]
                score = i[1]
                url = df['url'][id]

                filename = url.split('/')[-1]
                # full_path = "C:\\Users\\josh\\PycharmProjects\\IR_Search_Engine\\videogame\\" + filename
                full_path = os.getcwd() + "\\videogame\\" + filename

                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        title_match = re.search(r'<title>(.*?)</title>', f.read(), re.IGNORECASE)
                        if title_match == None:
                            game_title = "Unknown"
                        else:
                            game_title = title_match.group(1).replace(" at Nintendo :: Games", "")
                except:
                    game_title = "Unknown"

                card = ctk.CTkFrame(output, fg_color="#0d0d0d", border_color="#39FF14", border_width=2)
                card.pack(fill="x", pady=5, padx=5)

                text = ("Result " + str(a) + ": " + game_title + " " + url + " Score: " + str(score) + "\n")

                label = ctk.CTkLabel(card, text=text, font=console_font, text_color="#39FF14", justify="left", anchor="w", wraplength=500)
                label.pack(side="left", padx=10, pady=10)

                btn_open = ctk.CTkButton(card, text="OPEN FILE", width=100, fg_color="#39FF14", text_color="#000000", hover_color="#2ebf11", font=("Courier New", 12, "bold"), command=lambda p=full_path: webbrowser.open(p))
                btn_open.pack(side="right", padx=10)
                a=a+1


    title = ctk.CTkLabel(app, text="INSERT COIN TO SEARCH", font=("Courier New", 28, "bold"), text_color="#39FF14")
    title.pack(pady=(30, 10))

    search_bar = ctk.CTkEntry(app, placeholder_text="Type Your Query Here", font=retro_font, width=500, height=50, fg_color="#1a1a1a", border_color="#39FF14", border_width=2, text_color="#FFFFFF")
    search_bar.pack(pady=10)

    search_btn = ctk.CTkButton(app, text="PRESS START", command=lambda: on_search(), font=retro_font, fg_color="#FF0055", hover_color="#CC0044", width=200, height=50, corner_radius=0)
    search_btn.pack(pady=10)

    output = ctk.CTkScrollableFrame(app, width=700, height=350, fg_color="#000000", border_color="#39FF14", border_width=2, corner_radius=0)
    output.pack(pady=20)

    title = ctk.CTkLabel(app, text="CLOSE THIS TO USE THE COMMAND LINE INTERFACE", font=("Courier New", 28, "bold"), text_color="#39FF14")
    title.pack(pady=(30, 10))

    app.mainloop()


df = pd.read_csv('videogame.csv')
df['processed_html'] = df['url'].apply(lambda x: tokenize(readFile(x)))

inverted_index = {}

for i, row in df.iterrows():
    tokens = row['processed_html']

    for token in set(tokens):
        if token in inverted_index:
            inverted_index[token].append(i)
        else:
            inverted_index[token] = [i]

gui()

print("Training questions: ")
training_questions = ["Pokémon Trozei", "Tony Hawk's Downhill Jam", "Arcade type games", "London Taxi: Rush Hour", "Game published by Atari", "The Sims 2 Apartment Pets"]
for i in training_questions:
    results = search(i)
    print(i)
    for x in results[:10]:
        id = x[0]
        score = x[1]
        url = df['url'][id]
        publisher = str(df['STRING : publisher'][id])
        # path = "C:\\Users\\josh\\PycharmProjects\\IR_Search_Engine\\videogame\\"
        path = os.getcwd() + "\\videogame\\"
        try:
            with open(path + url.split('/')[-1], 'r', encoding='utf-8', errors='ignore') as f:
                title_match = re.search(r'<title>(.*?)</title>', f.read(), re.IGNORECASE)
                if title_match == None:
                    title = "Unknown"
                else:
                    title = title_match.group(1).replace(" at Nintendo :: Games", "")
        except:
            title = "Unknown"
        print("Found " + url + " │ Name: " + title + " │ Made By: " + publisher + " │ Score: " + str(score))

quit = ""
while quit!="q":
    user_input = input("Enter a query (Type Q to quit):\n")
    quit = user_input.lower()
    if quit != "q":
        results = search(user_input)
        for i in results[:10]:
            id = i[0]
            score = i[1]
            url = df['url'][id]
            publisher = str(df['STRING : publisher'][id])
            # path = "C:\\Users\\josh\\PycharmProjects\\IR_Search_Engine\\videogame\\"
            path = os.getcwd() + "\\videogame\\"
            try:
                with open(path + url.split('/')[-1], 'r', encoding='utf-8', errors='ignore') as f:
                    title_match = re.search(r'<title>(.*?)</title>', f.read(), re.IGNORECASE)
                    if title_match == None:
                        title = "Unknown"
                    else:
                        title = title_match.group(1).replace(" at Nintendo :: Games", "")
            except:
                title = "Unknown"
            print("Found " + url + " │ Name: " + title + " │ Made By: " + publisher + " │ Score: " + str(score))


