from django.http import HttpResponse, JsonResponse
from fastapi import FastAPI
from .models import Message
import requests

app = FastAPI()


@app.get("/")
def index(request):
    """
    Index url of API, does nothing
    :param request: Request from service
    :return: HTML response 200
    """
    return HttpResponse(status=200)


@app.post("/new_msg")
def create_msg(request):
    """
    Create message endpoint
    :param request: Request
    :return: HTML response 201 if OK and created or 400 if error
    """
    # get wanted parameters from request and check them
    try:
        title = request.POST["title"]
        body = request.POST["body"]
        userID = request.POST["userID"]
    except KeyError:
        return HttpResponse(status=400)
    if title == "" or body == "" or userID == "":
        return HttpResponse(status=400)

    # check if user exits
    user = get_by_api(userID=userID)
    if not user:
        return HttpResponse(status=400)

    # create and return message as JSON
    Message.objects.create(userID=user, title=title, body=body)
    return HttpResponse(status=201)


@app.get("msg/user/{userID}")
def get_user_messages(request, userID):
    """
    Get message endpoint
    :param request: Request
    :param userID: ID of wanted user
    :return: JSON if OK or HTML response 400 if error
    """
    # first, check if user exists
    if not get_by_api(userID=userID):
        return HttpResponse(status=400)
    # get messages from database
    db_msgs = Message.objects.filter(userID=userID)
    if not db_msgs:
        return HttpResponse(status=400)

    # create a JSON and return it
    msgs = []
    for msg in db_msgs:
        msgs.append({"id": msg.pk, "userID": msg.userID, "title": msg.title, "body": msg.body})
    return JsonResponse(msgs, safe=False)


@app.get("/msg/{msgID}")
def get_message(request, msgID):
    """
    Get message endpoint
    :param request: Request
    :param msgID: ID of wanted message
    :return: JSON if OK or HTML response 400 if error
    """
    msg = None
    # get message from database or external API, check and return it as JSON
    try:
        msg = Message.objects.get(pk=msgID)
    except Message.DoesNotExist:
        msg = get_by_api(msgID=msgID)
    if not msg:
        return HttpResponse(status=400)
    return JsonResponse({"id": msg.pk, "userID": msg.userID, "title": msg.title, "body": msg.body})


@app.post("/msg/{msgID}/edit")
def edit_message(request, msgID):
    """
    Edit message endpoint
    :param request: Request
    :param msgID: ID of wanted message
    :return: HTML response 201 if OK and edited or 400 if error
    """
    # get wanted parameters from request and check them
    try:
        title = request.POST.get("title")
        body = request.POST.get("body")
    except KeyError:
        return HttpResponse(status=400)
    if title == "" or body == "":
        return HttpResponse(status=400)

    # get message and check it
    msg = None
    try:
        msg = Message.objects.get(pk=msgID)
    except Message.DoesNotExist:
        msg = get_by_api(msgID=msgID)
    if not msg:
        return HttpResponse(status=400)

    # edit values, save to database and return OK
    msg.title = title
    msg.body = body
    msg.save()
    return HttpResponse(status=201)


@app.delete("/msg/{msgID}/delete")
def delete_message(request, msgID):
    """
    Delete message endpoint
    :param request: Request
    :param msgID: ID of wanted message
    :return: HTML response 204 if deleted or 400 if error
    """
    # try to get message from database, check and return response
    try:
        Message.objects.filter(id=msgID).delete()
    except Message.DoesNotExist:
        return HttpResponse(status=400)
    return HttpResponse(status=204)


def get_by_api(userID=-1, msgID=-1):
    """
    Auxiliary function for getting messages from external API
    :param userID: optional. Get messages of this user
    :param msgID: optional. Get message with this ID
    :return: Message from external API or False if it does not exist
    """

    # check if api is available
    url = "https://jsonplaceholder.typicode.com/"
    response = requests.get(url)
    if response.status_code != 200:
        return False

    # get user by his ID / check if he exists
    if userID != -1:

        url = url + "users/" + str(userID)
        response = requests.get(url)
        if response.status_code != 200:
            return False

        data = response.json()
        return data["id"]

    # get by userID
    elif msgID != -1:

        # url for wanted message
        url = url + "posts/" + str(msgID)
        # call API and check response
        response = requests.get(url)
        if response.status_code != 200:
            return False
        # response to JSON
        data = response.json()
        uID = int(data["userId"])
        # check if user exists
        user = get_by_api(userID=uID)
        if not user:
            return False
        # get wanted data
        title = data["title"]
        body = data["body"]

        # create new object in database and return
        msg = Message.objects.create(pk=msgID, userID=user, title=title, body=body)
        return msg

