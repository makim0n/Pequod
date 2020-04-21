#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DB
class Manifest(db.Model):
    id            = db.Column('id', db.Integer, primary_key=True)
    arch          = db.Column(db.String(500))
    startcmd      = db.Column(db.String(500))
    entrypoint    = db.Column(db.String(500))
    volume        = db.Column(db.String(500))
    workdir       = db.Column(db.String(500))
    envvar        = db.Column(db.String(500))

class Files(db.Model):
    id            = db.Column('id', db.Integer, primary_key=True)
    filename      = db.Column(db.String(500))
    file_size     = db.Column(db.String(500))
    file_perm     = db.Column(db.String(500))
    owner         = db.Column(db.String(500))
    date          = db.Column(db.String(500))
    timestamp     = db.Column(db.String(500))
    file_content  = db.Column(db.Text)
    layer         = db.Column(db.String(500))