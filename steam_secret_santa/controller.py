import shelve
import argparse
import yaml


def get_db(path):
    """
    Open and return the shelve database at path.
    """
    return shelve.open(path)


def get_config(path):
    """
    Open and return the yaml config file at path.
    """
    return yaml.load(open(path))


def put_participants_in_db(db, config, sync=True):
    """
    Enters each participant into the db with their secret_email as the key.
    """
    for participant in config["participants"]:
        secret_email = participant["secret_email"]
        db[secret_email] = participant
    if sync:
        db.sync()


def assign_gift_url(db, secret_email, url):
    """
    Adds a "gift_url" key to the database entry for a given user, identified by their secret_email.
    """
    entry = db[secret_email]
    entry["gift_url"] = url
    db[secret_email] = entry


def participants_without_gifts(db):
    """
    Returns a list of participant names who don't yet have a gift_url in their database entry.
    """
    return [x["name"] for x in db if "gift_url" not in x]
