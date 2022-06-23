from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.show import Show

@app.route("/shows/form")
def show_form():
    if not "user_id" in session:
        redirect("/")
    return render_template("form.html")

@app.route("/shows/<int:id>")
def view_show(id):
    show_data = {
        "id" : id
    }
    show = Show.show_by_id(show_data)
    return render_template("view.html", show = show)

@app.route("/shows/<int:id>/edit")
def edit_form(id):
    if not "user_id" in session:
        redirect("/")
    show_data = {
        "id" : id
    }
    show = Show.show_by_id(show_data)
    return render_template("edit_form.html", show = show)

@app.route("/shows/save", methods=["post"])
def save_show():
    if not "user_id" in session:
        redirect("/")
    if not Show.validate_show(request.form):
        return redirect("/shows/form")
    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "descr" : request.form["descr"],
        "user_id" : session["user_id"]
    }
    Show.save_show(data)
    return redirect("/dashboard")

@app.route("/shows/<int:id>/update", methods=["post"])
def update_show(id):
    if not "user_id" in session:
        redirect("/")
    if not Show.validate_show(request.form):
        return redirect(f"/shows/{id}/edit")
    data = {
        "id" : id,
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "descr" : request.form["descr"]
    }
    Show.update_show(data)
    return redirect("/dashboard")

@app.route("/shows/<int:id>/delete")
def delete_show(id):
    show_data = {
        "id" : id
    }
    Show.delete_show(show_data)
    return redirect("/dashboard")