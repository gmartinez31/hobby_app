import os
import boto3

import tornado.ioloop
import tornado.web
import tornado.log

from jinja2 import \
  Environment, PackageLoader, select_autoescape


from dotenv import load_dotenv
load_dotenv('.env')
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")


#get port var, if no var, the secong arg is the default
PORT = int(os.environ.get('PORT','8888'))

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

client = boto3.client(
  'ses',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)

#whenever you wanna make a template, this func is called
class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, **context):
      template = ENV.get_template(tpl)
      self.write(template.render(**context))


#for Home Page
class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("index.html")


#for Ultimate Frisbee HTML Page
class UltimateHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("ultfris.html")


#for form-sample HTML Page
class FormHandler(TemplateHandler):
  def post(self, page):
    name = self.get_body_argument('name')
    email = self.get_body_argument('email')
    text = self.get_body_argument('text')
    
    response = client.send_email(
      Destination={
        'ToAddresses': ['zmgoose13@gmail.com'],
      },
      Message={
        'Body': {
          'Text': {
            'Charset': 'UTF-8',
            'Data': "Name: {}\nemail: {}\nText: {}\n".format(name, email, text),
          },
        },
        'Subject': {'Charset': 'UTF-8', 'Data': ''},
      },
      Source='zmgoose13@gmail.com',
    self.write('Thanks got your data<br>')
    self.write('Email: ' + email)
    self.redirect('/thank-you-for-submitting')
)


#for Hiking HTML Page
class HikingHandler(TemplateHandler):
  def get(self):
    self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("hiking.html")


#for Weightlifting HTML Page
class WeightliftingHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("weightlifting.html")    


#for Video Games HTML Page
class VideoHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("videogames.html")


#for Coding HTML Page
class CodingHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("coding.html")


def make_app():
    return tornado.web.Application([
        # Routes
        (r"/", MainHandler),
        (r"/form-sample", FormHandler)
        (r"/ultfris", UltimateHandler),
        (r"/hiking", HikingHandler),
        (r"/weightlifting", WeightliftingHandler),
        (r"/videogames", VideoHandler),
        (r"/coding", CodingHandler),
        (r"/static/(.*)",
        tornado.web.StaticFileHandler,
        {'path': 'static'})
    ], autoreload=True)
    # autoreload will restart server with any changes

if __name__ == "__main__":
    # Logs information in terminal, feedback
    tornado.log.enable_pretty_logging()
    app = make_app()
    # Listening on port 8888
    app.listen(PORT, print('Server started on localhost: ' + str(PORT)))
    # Infinite Loop on 8888
    tornado.ioloop.IOLoop.current().start()