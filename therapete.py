import os
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail

class MainPage(webapp.RequestHandler):
  def get(self):

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))

class Bookings(webapp.RequestHandler):
  def get(self):

    path = os.path.join(os.path.dirname(__file__), 'bookings.html')
    self.response.out.write(template.render(path, {}))

class SendMail(webapp.RequestHandler):
  def post(self):

    valid = True

    if self.request.get('name') == '':
       valid = False
    elif self.request.get('phone') == '' and self.request.get('email') == '':
       valid = False
       
    if not valid:
      template_values = {'error': '<div class="error">Please provide a name and one method of contact</div>'}
      path = os.path.join(os.path.dirname(__file__), 'bookings.html')
      self.response.out.write(template.render(path, template_values))
    else:
      c_name = "Name:" + cgi.escape(self.request.get('name'))
      c_phone = "Phone:" + cgi.escape(self.request.get('phone'))
      c_email = "Email:" + cgi.escape(self.request.get('email'))
      c_message = "Message:" + cgi.escape(self.request.get('message'))
      c_therapy = "Therapy:" + cgi.escape(self.request.get('therapy'))
      c_booking = "Booking:" + cgi.escape(self.request.get('booking'))
      c_people = "People:" + cgi.escape(self.request.get('people'))
  
      message = mail.EmailMessage()
      message.sender = "blair.nicholas@googlemail.com"
      message.to = "info@therapete.co.uk"
      message.subject = "Booking"
      message.body = c_name + "\n" + c_phone + "\n" + c_email + "\n" + c_message + "\n" + c_therapy + "\n" + c_booking + "\n" + c_people
  
      message.send()
  
      message_body = c_name + "<br />" + c_phone + "<br />" + c_email + "<br />" + c_message + "<br />" + c_therapy + "<br />" + c_booking + "<br />" + c_people
      template_values = {'message_body':message_body}
  
      path = os.path.join(os.path.dirname(__file__), 'booking-sent.html')
      self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
                                     [('/', MainPage),('/booking-sent', SendMail),('/bookings', Bookings)]
                                     ,debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()