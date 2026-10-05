from flask import Blueprint, flash, redirect, render_template, request, url_for

from .extensions import db
from .models import Todo

bp = Blueprint("todos", __name__)

@bp.route("/")
def index():
    todos = Todo.query.order_by(Todo.completed.asc(), Todo.created_at.desc()).all()
    return render_template("index.html", todos=todos)

@bp.route("/todos", methods=["POST"])
def create():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Title is required.", "error")
        return redirect(url_for("todos.index"))
    
    db.session.add(Todo(title=title, description=...))
    db.session.commit()
    flash("Todo created.", "success")
    return redirect(url_for("todos.index"))