from django.shortcuts import render
from django.http import HttpResponseNotFound
import requests
root_url = "http://127.0.0.1:8000/"  # url at which the page should be available


def index(request):
    """
    View for index/main page of "GUI"
    :param request: Request from service
    :return: Renders the page
    """
    msgs = False                    # msgs will store either received message or no message (False)
    url = root_url + "api/msg/"     # url for API request

    if request.POST.get("msgID"):   # if "find" button is pressed

        # url for API request with msgID
        url = url + str(request.POST.get("ID"))
        # call API and check response
        response = requests.get(url=url)
        if response.status_code == 400:
            msgs = False
        else:
            msgs = response.json()
    elif request.POST.get("userID"):
        msgs = False

    # render the page
    return render(request, "index.html", {"msgs": msgs})


def msg_detail_view(request, msgID):
    """
    View for message detail
    :param request: Request from service
    :param msgID: ID of message to render
    :return: Renders the page
    """
    # url for API request with msgID
    url = root_url + "api/msg/" + str(msgID)
    # call API and check response
    response = requests.get(url)
    if response.status_code != 200:
        return HttpResponseNotFound("Message not found")
    msg = response.json()
    delete = False                  # "switch" used in html to render some parts

    if request.POST.get("delete"):  # if "delete" button is pressed

        # url for API DELETE request with msgID
        url = url + "/delete"
        # call API and check response
        response = requests.delete(url=url)
        # Not sure if this ever happens
        if response.status_code != 204:
            raise Exception
        delete = True

    # renders the page
    return render(request, "msg_detail.html", {"msg": msg, "deleted": delete})


def edit_message_view(request, msgID):
    """
    View for message editing
    :param request: Request from service
    :param msgID: ID of message to render/edit
    :return: Renders the page
    """
    opened = True                   # "switch" used in html to render some parts
    edit = False                    # same
    # url for API request with msgID
    url = root_url + "api/msg/" + str(msgID)
    # call API and check response
    response = requests.get(url=url)
    if response.status_code != 201:
        opened = False
        edit = False
    msg = response.json()

    if request.POST.get("edit"):    # if "edit" button is pressed

        # url for API request with msgID
        url = root_url + "api/msg/" + str(msgID) + "/edit"
        # call POST API and check response
        response = requests.post(url=url, data={"title": request.POST.get("title"),
                                                "body": request.POST.get("body")
                                                })
        if response.status_code != 201:
            edit = False
        else:
            edit = True
        opened = False

    # renders the page
    return render(request, "edit_msg.html", {"msg": msg, "edit": edit, "opened": opened})


def new_message_view(request):
    """
    View for new message creation
    :param request: Request from service
    :return: Renders the page
    """
    ok = True                       # "switch" used in html to render some parts
    opened = True                   # same

    if request.POST.get("create"):  # if "create" button is pressed

        url = root_url + "api/new_msg/"
        # call POST API and check response
        response = requests.post(url=url, data={"userID": request.POST.get("userID"),
                                                "title": request.POST.get("title"),
                                                "body": request.POST.get("body")})
        if response.status_code != 201:
            ok = False
        else:
            ok = True
        opened = False

    # renders the page
    return render(request, "new_msg.html", {"ok": ok, "opened": opened})














