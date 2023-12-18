import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
import pytesseract
import openai

# path to tesseract file
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.2_1/bin/tesseract'
filePath = ""

# Create a Tkinter root window (it won't be shown)
root = tk.Tk()
root.title("OCR Engine")
root.geometry("1000x600")

file_path = ""
extracted_text = ""

# please add your api key below
openai.api_key = "<Plaese add your api key here>"


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.9,
    )
    return response.choices[0].message["content"]


def pick_pdf_file():
    # Open a file dialog for selecting a PDF file
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")],
    )
    if file_path:
        print(f"Selected PDF file: {file_path}")
        training_data_entry.delete(0, tk.END)
        training_data_entry.insert(0, file_path)
    else:
        print("No file selected.")


# Load the PDF using pdf2image and extract text from the specified pages
def extract_text_from_pdf(pdf_path, start_page, end_page):
    text = []

    pages = convert_from_path(pdf_path)
    for page_num, page in enumerate(pages, start=1):
        if start_page <= page_num <= end_page:
            text.append(pytesseract.image_to_string(page))

    return text


def evaluate_function():
    start_page = 10
    end_page = 15

    # Extract text from the specified pages
    extracted_text = extract_text_from_pdf(file_path, start_page, end_page)
    tk.Button(root, text="Next", command=evaluate_function_1).pack(pady=10)


prompt_for_question = f"""Your task is to understand and make 2 questions from the \
    text given below.
Text: ```{extracted_text}```
"""

prompt = f"""Your task is to determine if the student's solution \
is correct or not. \

If its more than 50% correct then classify it as correct. \

To solve the problem do the following:\

- First, work out your own solution to the problem.\

- Then compare your solution to the student's solution \
and evaluate if the student's solution is correct or not.\

Don't decide if the student's solution is correct until you have done the problem yourself.\

Use the following format:\

Question:\n
---\n
put the question here\n
---\n
Student's solution:\n
---\n
Write Student's solution here\n
---\n
Actual solution:\n
---\n
write steps to work out the solution and your solution here. If there are no steps then you can just write your solution here \n
---\n
Is the student's solution the same as actual solution you just calculated? \n
---\n
yes or no\n
---\n
Student grade:\n
---\n
correct or incorrect\n
---\n

Solution: ```{extracted_text}```
"""


def evaluate_function_1():
    print(prompt_for_question)
    # response = get_completion(prompt_for_question)
    # print(response)


# Create and place labels and entry widgets for training data
tk.Label(root, text="Pick PDF File:").pack(pady=10)
training_data_entry = tk.Entry(root, width=50)
training_data_entry.pack(padx=10)
tk.Button(root, text="Browse", command=lambda: pick_pdf_file()).pack()

# Create and place an "Ok" button
tk.Button(root, text="Next (1/3)", command=evaluate_function).pack(pady=10)

# Run the tkinter main loop
root.mainloop()
