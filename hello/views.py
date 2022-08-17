import json

import requests
from django.shortcuts import render, redirect, HttpResponse

from .models import Greeting
from .models import Person


# import requests ok


# Create your views here.
# <<<---- Login Page Starts Here ---->>
def bookssearch(request):
    searchValue = ""
    b={}
    if request.GET:
        searchValue = request.GET["searchValue"]

        path = "https://www.googleapis.com/books/v1/volumes?q={0}".format(searchValue)
        # print(path)
        url = requests.get(path)
        # print(response.json())
        books = json.loads(url.text)
        print(len(books), type(books))
        for book in books:
            print(book)
        # b = json.dumps(books)
        b = books["items"]
        print(b)
    return render(request, "bookslist.html", {"books": b,"searchValue":searchValue})
    #return HttpResponse(json.dumps(books), content_type='application/json')


def statecapital(request):
    states = {"up": "Lucknow", "bihar": "Patna"}
    try:
        state = request.GET["state"]
        state.lower()
        capital = states.get(state)
        if capital is None:
            output = {"status": "error", "state": "not found".lower(), "capital": "not found".upper()}
            return HttpResponse(json.dumps(output), content_type='application/json')
        else:

            output = {"status": "ok", "state": state.lower(), "capital": capital.upper()}
            return HttpResponse(json.dumps(output), content_type='application/json')
    except:
        output = {"status": "error", "state": "not found".lower(), "capital": "not found".upper()}
        return HttpResponse(json.dumps(output), content_type='application/json')


def login(request):
    title = ""
    session = request.session
    try:

        del session["answers"]
    except:
        pass
    if request.POST:
        # email = request.POST['email']
        # password = request.POST['password']
        title = request.POST['title']
        session["name"] = title
        return redirect("/quiz/")
        # return render(request, "quiz.html", {"title": title, "session": session})
    return render(request, "login.html", {"session": session})


# <<<---- Login Page Ends Here ---->>

def quiz(request):
    answers = request.session.get("answers")
    if answers == None:
        answers = []

    q1 = {"question": "What is C?", "op1": "Language", "op2": "Alphabet", "op3": "Ascii character",
          "op4": "All of these", "correct": "a"}
    q2 = {"question": "Who developed Python Programming language?", "op1": "Wick van rossum", "op2": "Dennis Ritchie",
          "op3": "Guido van Rossum", "op4": "none", "correct": "c"}
    q3 = {"question": "Which of the following is the correct extension of the python file?", "op1": ".python",
          "op2": ".pl", "op3": ".py", "op4": ".p", "correct": "c"}
    q4 = {"question": "Who developed C programming language ?", "op1": "denies ritchies", "op2": "Guido van Rossum",
          "op3": "harsh", "op4": "none", "correct": "a"}
    q5 = {"question": "Django is  a ?", "op1": "Programming Language", "op2": "Framework",
          "op3": "Python Web Framework", "op4": "None", "correct": "c"}
    questions = [q1, q2, q3, q4, q5]
    questionno = 0
    givenanswer = ""
    correctanswer = ""
    result = ""
    totalmarks = 0
    if not request.POST:
        try:
            del request.session["answers"]
        except:
            pass
    if request.POST:
        givenanswer = request.POST["option"]
        questionno = int(request.POST["qno"])
        totalmarks = int(request.POST["totalmarks"])
        correctanswer = questions[questionno].get("correct")
        questionno += 1
        totalmarks += 1
        result = "Yes"

        if givenanswer != correctanswer:
            result = "No"
            totalmarks -= 1
        data = {"qno": (questionno - 1), "answer": givenanswer, "correct": correctanswer, "result": result}
        answers.append(data)
        if questionno >= len(questions):
            return render(request, 'result.html', {"totalmarks": totalmarks,
                                                   "answers": answers})
    # return httpResponse('python quiz!')
    request.session["answers"] = answers
    return render(request, "quiz.html",
                  {"question": questions[questionno],
                   "showqno": questionno + 1,
                   "qno": questionno,
                   "givenanswer": givenanswer,
                   "correctanswer": correctanswer,
                   "result": result,
                   "totalmarks": totalmarks, "answers": answers})


def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def newbase(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "newindex.html")


def use(request):
    requests.get("https://google.com")
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def personentry(request):
    person = Person()
    person.name = "Champak"
    person.address = "Varanasi"
    person.age = 30
    person.save()
    # hfhfhgf

    persons = Person.objects.all()

    return render(request, "personenter.html", {"persons": persons})


def birthday(request):
    names = {"avinash": "28-08-1995", "shyam": "08-07-2000", "rohit": "15-08-2000",
             "sachin": "19-01-2002", "harsh": "29-02-2000", "shivam": "07-04-2000",
             "abhishek": "13-09-1991", "sagar": "27-07-2000", "chandan": "13-04-2000",
             "ashutosh": "12-03-2000", "saktiman": "12-07-2001"}

    try:
        name = request.GET["name"]
        name.lower()
        birth = names.get(name)
        if birth is None:
            output = {"status": "error", "name": "not found".lower(),
                      "birth": "not found".upper()}
            return HttpResponse(json.dumps(output), content_type='application/json')
        else:

            output = {"status": "ok", "name": name.lower(), "birth": birth.upper()}
            return HttpResponse(json.dumps(output), content_type='application/json')
    except:
        output = {"status": "error", "name": "not found".lower(),
                  "birth": "not found".upper()}
        return HttpResponse(json.dumps(output), content_type='application/json')


def trail(request):
    output = {"Hello Mr.Samrat": "Helo"}
    return HttpResponse(json.dumps(output), content_type='application/json')


def add(request):
    a = 0
    b = 0
    result = 0
    if request.GET:
        a = int(request.GET["a"])
        b = int(request.GET["b"])
        result = a + b
    return HttpResponse(json.dumps(result))


def python(request):
    quesions = '''
    {
        "Python": [
            {
                "questionno": 1,
                "question": "Who developed Python Programming Language?",
                "a": "Wick van Rossum",
                "b": "Rasmus Lerdorf",
                "c": "Guido van Rossum",
                "d": "Niene Stom",
                "correctanswer": "c"
            },
            {
                "questionno": 2,
                "question": "Which type of Programming does Python support?",
                "a": "object-oriented programming",
                "b": "structured programming",
                "c": "functional programming",
                "d": "all of the mentioned",
                "correctanswer": "d"
            },

            {
                "questionno": 3,
                "question": "Is Python case sensitive when dealing with identifiers?",
                "a": "no",
                "b": "yes",
                "c": "machine dependent",
                "d": "none of the mentioned",
                "correctanswer": "b"
            },

            {
                "questionno": 4,
                "question": "Which of the following is the correct extension of the Python file?",
                "a": ".python",
                "b": ".pi",
                "c": ".py",
                "d": ".p",
                "correctanswer": "c"
            },

            {
                "questionno": 5,
                "question": "Is Python code compiled or interpreted?",
                "a": "Python code is both compiled and interpreted",
                "b": "Python code is neither compiled nor interpreted",
                "c": "Python code is only compiled",
                "d": "Python code is only interpreted",
                "correctanswer": "a"
            },

            {
                "questionno": 6,
                "question": "Which of the following is used to define a block of code in Python language?",
                "a": "Indentation",
                "b": "Key",
                "c": "Brackets",
                "d": "All of the mentioned",
                "correctanswer": "a"
            },

            {
                "questionno": 7,
                "question": "Which keyword is used for function in Python language?",
                "a": "Function",
                "b": "Def",
                "c": "Fun",
                "d": "Define",
                "correctanswer": "b"
            },

            {
                "questionno": 8,
                "question": "Which of the following character is used to give single-line comments in Python?",
                "a": "//",
                "b": "#",
                "c": "!",
                "d": "/*",
                "correctanswer": "a"
            },

            {
                "questionno": 9,
                "question": "Which of the following functions can help us to find the version of python that we are currently working on?",
                "a": "sys.version(1)",
                "b": "sys.version(0)",
                "c": "sys.version()",
                "d": "sys.version",
                "correctanswer": "a"
            },

            {
                "questionno": 10,
                "question": "Python supports the creation of anonymous functions at runtime, using a construct called __________",
                "a": "pi",
                "b": "anonymous",
                "c": "lambda",
                "d": "non of the mentioned",

                "correctanswer": "c"
            }

        ]
    }'''

    return HttpResponse(json.dumps(quesions))

    # <!--- Java Question Below--->


def dsa(request):
    Questions = '''


    {
        "Data Structure": [
            {
                "questionno": 1,
                "question": " How can we describe an array in the best possible way? ",
                "a": "The Array shows a hierarchical structure.",
                "b": " Arrays are immutable.",
                "c": "Container that stores the elements of similar types",
                "d": "The Array is not a data structure ",
                "Correct  Answer": "C"
            },
            {
                "questionno": 2,
                "question": "Which of the following is the correct way of declaring an array?",
                "a": "int javatpoint[10];",
                "b": "int javatpoint;",
                "c": "javatpoint{20}",
                "d": "array javatpoint[10];",
                "correctanswer": "a"
            },
            {
                "questionno": 3,
                "question": "How can we initialize an array in C language?",

                "a": "int arr[2]=(10, 20);",
                "b": "int arr(2)={10, 20}",
                "c": "int arr[2] = {10, 20}",
                "d": "int arr(2) = (10, 20)",
                "correctanswer": "c"
            },
            {
                "questionno": 4,
                "question": "Which one of the following is the size of int arr[9] assuming that int is of 4 bytes?",
                "a": "9",
                "b": "36",
                "c": "35",
                "d": "None of the above",
                "correctanswer": "b"
            },
            {
                "questionno": 5,
                "question": "Which one of the following is the process of inserting an element in the stack?",
                "a": "Insert",
                "b": "Add",
                "c": "Push",
                "d": "None of the above",
                "correctanswer": "c"
            },
            {
                "questionno": 6,
                "question": " What is the outcome of the prefix expression +, -, *, 3, 2, /, 8, 4, 1?",
                "a": "12",
                "b": "11",
                "c": "5",
                "d": "7",
                "correctanswer": "c"
            },
            {
                "questionno": 7,
                "question": " The minimum number of stacks required to implement a stack is __",
                "a": "12",
                "b": "11",
                "c": "5",
                "d": "7",
                "correctanswer": "c"
            },
            {
                "questionno": 8,
                "question": "Which of the following principle does Queue use? ",
                "a": "LIFO principle",
                "b": "FIFO principle",
                "c": "Linear tree",
                "d": "Ordered array",
                "correctanswer": "b"
            },
            {
                "questionno": 9,
                "question": "Which one of the following is not the type of the Queue? ",
                "a": "Linear Queue",
                "b": "Circular Queue",
                "c": "Double ended Queue",
                "d": "Single ended Queue",
                "correctanswer": "d"
            },
            {
                "questionno": 10,
                "question": "The time complexity of enqueue operation in Queue is __",
                "a": "O(1)",
                "b": "O(n)",
                "c": "O(logn)",
                "d": "O(nLogn)",
                "correctanswer": "a"
            },

        ]

    }'''
    return HttpResponse(json.dumps(Questions))
