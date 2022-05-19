from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")


def index(request):
    ## if method is post search
    query = request.GET.get("q")
    entries = util.list_entries()
    title = "All Pages"
    # If query has a value method is post
    if query:
        print(query)
        # If search matches an entry, go to url otherwise show all matches
        if query in entries:
            return redirect("entries", query)
        else:
            entries = [match for match in entries if query in match]
            title = "Search Results"
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "title": title
    })


def entries(request, entry):
    # Compare the url with all the entries, if it's valid load the page.
    currentEntry = util.get_entry(entry)
    if currentEntry:
        return HttpResponse(currentEntry)
    else:
        return HttpResponse(f"{entry} is not a valid entry.")


def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = request.POST.get("text")
            print(text)
            print(title)
    return render(request, "encyclopedia/create.html", {
        "form": EntryForm()
    })
