from django.shortcuts import render
from django.http import HttpResponse
from . import movierec


# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# from chatterbot.trainers import ChatterBotCorpusTrainer
#
# # Creating ChatBot Instance
# chatbot = ChatBot('CoronaBot')
#
#  # Training with Personal Ques & Ans
# conversation = [
#     "Hello",
#     "Hi there!",
#     "How are you doing?",
#     "I'm doing great.",
#     "That is good to hear",
#     "Thank you.",
#     "You're welcome."
# ]
#
# trainer = ListTrainer(chatbot)
# trainer.train(conversation)
#
# # Training with English Corpus Data
# trainer_corpus = ChatterBotCorpusTrainer(chatbot)
# trainer_corpus.train(
#     'chatterbot.corpus.english'
# )
#

# Create your views here.


def home(request):
    return render(request, 'index.html')
    #return HttpResponse("Hello Dina")

def get(request):

    msg = request.GET['msg']
    print(msg)
    msg = msg.strip()
    movies = movierec.movie_recommendation(msg)
    #str(chatbot.get_response(msg))

    return HttpResponse(movies)