from django.shortcuts import render
from . import util


def index(request):
    query = request.GET.get("q")
    if query:
        query = query.upper()
        content = util.get_entry(query)
        if content is None:
            content = ""
        content = util.markdown_to_html_v1(content)
        if content:
            return render(
                request,
                "encyclopedia/entry/index.html",
                {"title": query.upper(), "content": content},
            )
        entries = [
            entry for entry in util.list_entries() if query.lower() in entry.lower()
        ]
        if entries:
            return render(
                request,
                "encyclopedia/search/index.html",
                {"title": "Search", "content": entries, "query": query},
            )
        return render(request, "errors/404.html", status=404)
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    content = util.get_entry(title)
    if content:
        content = util.markdown_to_html_v1(content)
        return render(
            request,
            "encyclopedia/entry/index.html",
            {"title": title, "content": content},
        )
    return render(request, "errors/404.html", status=404)


def page_no_found(request, _unused_exception):
    return render(request, "errors/404.html", status=404)


def new_page(request):
    if request.method == "POST":
        title = request.POST["title"].capitalize()
        content = request.POST["content"]
        if util.get_entry(title):
            return render(
                request,
                "encyclopedia/new/index.html",
                {"error": "<span class='error'>Entry already exists!</span>"},
            )
        util.save_entry(title, content)
        content = util.markdown_to_html_v1(content)
        return render(
            request,
            "encyclopedia/entry/index.html",
            {"title": title.upper(), "content": content},
        )
    return render(request, "encyclopedia/new/index.html")


def edit_page(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        content = util.markdown_to_html_v1(content)
        return render(
            request,
            "encyclopedia/entry/index.html",
            {"title": title, "content": content},
        )
    content = util.get_entry(title)
    if content:
        return render(
            request,
            "encyclopedia/edit/index.html",
            {"title": title, "content": content},
        )
    return render(request, "errors/404.html", status=404)


def random_page(request):
    import random

    entries = util.list_entries()
    title = random.choice(entries)
    content = util.get_entry(title)
    content = util.markdown_to_html_v1(content)
    return render(
        request,
        "encyclopedia/entry/index.html",
        {"title": title.upper(), "content": content},
    )
