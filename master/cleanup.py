import cherrypy

from multiprocessing import Process, Pipe


class BaseHandler(Process):
    def __init__(self, conn):
        Process.__init__(self)
        self.conn = conn

class HelloHandler(BaseHandler):
    def run(self):
        msg = self.conn.recv()
        while msg != 'close':
            self.conn.send('hello world from another process')


class HelloPage(object):
    def __init__(self):
        self.conn, child_conn = Pipe()
        self.hello_processor = HelloHandler(child_conn)
        self.hello_processor.start()

    def index(self, *args, **kw):
        self.conn.send(args)
        return self.conn.recv()
    index.exposed = True


def run():
    cherrypy.tree.mount(HelloPage(), '/')
    cherrypy.quickstart()


if __name__ == '__main__':
    run()
