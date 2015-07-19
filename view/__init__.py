__author__ = 'zhuzhiying'
from flask import blueprints
from flask import Flask, render_template, flash, request, redirect, url_for
from flask.ext.login import LoginManager, login_user, login_required, logout_user, current_user
from config import *
