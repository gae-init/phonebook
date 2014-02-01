from flask.ext import wtf
import flask

import auth
import model
import util

from main import app


class ContactUpdateForm(wtf.Form):
  name = wtf.StringField('Name', [wtf.validators.required()])
  email = wtf.StringField('Email', [wtf.validators.optional(), wtf.validators.email()])
  phone = wtf.StringField('Phone', [wtf.validators.optional()])
  address = wtf.TextAreaField('Address', [wtf.validators.optional()])


@app.route('/contact/create/', methods=['GET', 'POST'])
@auth.login_required
def contact_create():
  form = ContactUpdateForm()
  if form.validate_on_submit():
    contact_db = model.Contact(
        user_key=auth.current_user_key(),
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        address=form.address.data,
      )
    contact_db.put()
    flask.flash('New contact was successfully created!', category='success')
    return flask.redirect(flask.url_for('contact_list', order='-created'))
  return flask.render_template(
      'contact_update.html',
      html_class='contact-create',
      title='Create Contact',
      form=form,
    )


@app.route('/contact/')
@auth.login_required
def contact_list():
  contact_dbs, more_cursor = util.retrieve_dbs(
      model.Contact.query(),
      limit=util.param('limit', int),
      cursor=util.param('cursor'),
      order=util.param('order') or 'name',
    )
  return flask.render_template(
      'contact_list.html',
      html_class='contact-list',
      title='Contact List',
      contact_dbs=contact_dbs,
      more_url=util.generate_more_url(more_cursor),
    )


@app.route('/contact/<int:contact_id>/')
@auth.login_required
def contact_view(contact_id):
  contact_db = model.Contact.get_by_id(contact_id)
  if not contact_db or contact_db.user_key != auth.current_user_key():
    flask.abort(404)
  return flask.render_template(
      'contact_view.html',
      html_class='contact-view',
      title=contact_db.name,
      contact_db=contact_db,
    )


@app.route('/contact/<int:contact_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def contact_update(contact_id):
  contact_db = model.Contact.get_by_id(contact_id)
  if not contact_db or contact_db.user_key != auth.current_user_key():
    flask.abort(404)
  form = ContactUpdateForm(obj=contact_db)
  if form.validate_on_submit():
    form.populate_obj(contact_db)
    contact_db.put()
    return flask.redirect(flask.url_for('contact_list', order='-modified'))
  return flask.render_template(
      'contact_update.html',
      html_class='contact-update',
      title=contact_db.name,
      form=form,
      contact_db=contact_db,
    )
