import tornado.ioloop
import tornado.web
import tornado.log

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # set_header - Content-Type - How browser interprets content (ex: text/plain)
        # self.set_header('Content-Type', 'text/plain')
        name = 'Gustavo'
        self.write("Hello, {}!".format(name))

class YouHandler(tornado.web.RequestHandler):
    def get(self, name):
        self.write("Hello, {}!".format(name))

# class YouTooHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.set_header('Content-Type', 'text/plain')
#         name = self.get_query_argument('name', 'Nobody')
#         self.write("Hello, {}!".format(name))

# class YouThreeHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header('Content-Type', 'text/plain')
        names = self.get_query_arguments('name')
        for name in names:
            self.write("Hello, {}!\n".format(name))

def make_app():
    return tornado.web.Application([
        # Routes
        (r"/", MainHandler),
        # (r"/hello/(.*)", YouHandler),
        # (r"/hello2", YouTooHandler),
        # (r"/hello3", YouThreeHandler),
        
    ], autoreload=True)
    # autoreload will restart server with any changes

if __name__ == "__main__":
    # Logs information in terminal, feedback
    tornado.log.enable_pretty_logging()
    app = make_app()
    # Listening on port 8888
    app.listen(8888), print('Server started on localhost: 8888')
    # Infinite Loop on 8888
    tornado.ioloop.IOLoop.current().start()