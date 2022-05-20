from xml.dom.minidom import Document
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

from markdown2 import Markdown
from random import randint

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")

# Randomize an entry page
def random():
    entries = util.list_entries()
    random = randint(0, len(entries)) - 1
    randomEntry = entries[random]
    return randomEntry

def index(request):
    query = request.GET.get("q")
    entries = util.list_entries()
        # If query has a value method user har searched
    if query:
        print(query)
        # If search matches an entry, go to url otherwise show all matches
        if query in entries:
            return redirect("entries", query)
        else:
            title = "Search Results"
            entries = [match for match in entries if query in match]
    title = "All Pages"
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "title": title,
        "random": random()
    })


def entries(request, entry):
    # Compare the url with all the entries, if it's valid load the page.
    currentEntry = util.get_entry(entry)
    query = request.GET.get("q")
    if query:
        return HttpResponseRedirect(reverse("index", query))
    if currentEntry:
        return render(request, "encyclopedia/display.html", {
            "text": currentEntry,
            "title": entry,
            "random": random()
        })
    else:
        return HttpResponse(f"{entry} is not a valid entry.")

# Create a new wiki entry
def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = request.POST.get("text")
            print(title)
            print(text)
            # If it exists already display error msg
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": EntryForm(),
                    "createError": "This entry has already been created",
                    "random": random()
                })
                # Otherwise save it and redirect user to new page
            else:
                util.save_entry(title, text)
                return redirect("entries", title)
    return render(request, "encyclopedia/create.html", {
        "form": EntryForm(),
        "random": random()
    })

# Edit existing wiki entries
def edit(request, entry):
    if request.method == "POST":
        text = request.POST.get("text")
        print(entry)
        print(text)
        util.save_entry(entry, text)
        # If successful redirect user
        return redirect("entries", entry)
        # Pass in the existing entry value to display it
    return render(request, "encyclopedia/edit.html", {
        "form": EntryForm(),
        "title": entry,
        "text": util.get_entry(entry),
        "random": random()
    })