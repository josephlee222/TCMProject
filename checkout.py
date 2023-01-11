import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from forms import loginUserForm, registerUserForm
from functions import flashFormErrors, goBack, unloginAccess
from classes.User import User

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
@loginAccess