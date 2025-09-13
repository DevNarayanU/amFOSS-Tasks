## time_tick_quiz.py

import requests
import html
import random
import threading
import time
from urllib.parse import unquote
# ------------------ user input selection ------------------
def fetch_categories():
    print("Welcome to TimeTickQuiz")
    CATEGORY_URL = "https://opentdb.com/api_category.php"
    r=requests.get(CATEGORY_URL)
    return (r.json()) 

def select_category():
    r=fetch_categories()
    for i in r["trivia_categories"]:
        print(i['id'],i['name'])
    return int(input("Enter catagory number"))
def select_difficulty():
    return input("enter difficulty from easy,medium,hard").lower()

def select_question_type():
    dif=int(input("Enter 1 for  Multiple choice 2 for True/False"))
    if dif==1:
        return "multiple"
    if dif==2:
        return "boolean"
    else:
        print("Please provide valid option")
    pass

def timed_input(inp, timeout=15):

    result = [None]
    ans=[False]
    def get_input():
        try:
            result[0] = input(inp)
            ans[0]=True
        except EOFError:
            result[0] = None
    def cd():
        for r in range(15,0,-1):
            if ans[0]:
                break
            print(f"\rTime left: {r}s",end="",flush=True)
            time.sleep(1)
        print("\r",end="")
    t = threading.Thread(target=get_input)
    tc=threading.Thread(target=cd)

    t.daemon = True
    tc.daemon=True
    t.start()
    tc.start()
    t.join(timeout)

    return result[0] 
    

TIME_LIMIT = 15  # seconds per question

# ------------------ api functionss ------------------




# ------------------ quiz logicc ------------------
def fetch_questions(amount=10):
    cat=select_category()
    dif=select_difficulty()
    ty=select_question_type()
    QUESTION_URL = f"https://opentdb.com/api.php?amount={amount}&category={cat}&difficulty={dif}&type={ty}&encode=url3986"
    return (requests.get(QUESTION_URL).json())



def ask_question():
    
    global c 
    c=0
    l=0
    for i in fetch_questions()['results']:
            print(f"Score={c}/10")   
            if i['type']=="multiple":
                l+=1
                q=unquote(i['question'])
                a=[unquote(i["correct_answer"])]
                for h in i["incorrect_answers"]:
                    a+=[unquote(h)]

                
                print(l ,q)
                random.shuffle(a)
                print("Options:")
                for x, option in enumerate(a, 1):
                    print(x, option)
                D=timed_input("your option number (15s)\n\n\n",TIME_LIMIT )
                if D is None:
                    print("Time's up")
                    continue
                try:

                    D=int(D)-1

                    if a[D] == unquote(i["correct_answer"]):
                        print("correct")

                        c+=1
                    else:
                        print("incorrect,correct was",unquote(i["correct_answer"]))
                except(ValueError,IndexError):
                    print("Invalid input,next")
            elif i['type']=="boolean":
                l+=1
                q=unquote(i['question'])
                print(q)
                D=timed_input("your option t for true or f for false (15s)", TIME_LIMIT )
                if D is None:
                    print("Time's up")
                    continue
                if  D.upper() == i["correct_answer"][0]:
                    c+=1
                   
    requests.get("https://opentdb.com/api_token.php?command=reset&token")




def select_quiz_options(select_category,select_difficulty,select):
    """
    gathers all the quiz options and fetch questions accordingly.
    """
    pass

# ------------------ main fucntion ------------------

def main():
    ask_question()
    print(f"!!!!!!Final score== {c}/10  !!!!!!")
    print("Thank you for playing TimeTickQuiz")
    

if __name__ == "__main__":
    main()

