CMP-5036A Search Engine Project
Student ID: yrj24guu
Domain: Video Games

1. REQUIRED LIBRARIES

To run this search engine, the following Python libraries must be installed. 
You can install them via your terminal/command prompt:

   pip install pandas
   pip install nltk
   pip install customtkinter
   pip install spacy
   
3. REQUIRED LANGUAGE MODELS (CRITICAL)

After installing the libraries, you MUST download the specific language models 
for NLTK and spaCy, or the script will not function correctly.

Run these commands in your terminal:

   python -m spacy download en_core_web_sm
   python -m nltk.downloader stopwords
   python -m nltk.downloader punkt_tab
   
3. FILE STRUCTURE

Ensure the following files are in the same directory as the script:
   - search_engine.py      (The main application)
   - videogame.csv         (The dataset)
   - /videogame/           (Folder containing the raw HTML files)

4. HOW TO RUN

1. Open your terminal or IDE (VS Code / PyCharm).
2. Navigate to the project folder.
3. Run the script:
   python search_engine.py

The GUI will launch automatically. 
Note: The console will verify "NER Success" upon startup.
