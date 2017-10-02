import os

import tornado.ioloop
import tornado.web
import tornado.log

from jinja2 import \
  Environment, PackageLoader, select_autoescape


#load_dotenv('.env')

#get port var, if no var, the secong arg is the default
PORT = int(os.environ.get('PORT','8888'))

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
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