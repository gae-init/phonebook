# coding: utf-8

from google.appengine.ext import ndb

import model


class Contact(model.Base):
  user_key = ndb.KeyProperty(kind=model.User, required=True)
  name = ndb.StringProperty(required=True)
  email = ndb.StringProperty(default='')
  phone = ndb.StringProperty(default='')
  address = ndb.StringProperty(default='')
