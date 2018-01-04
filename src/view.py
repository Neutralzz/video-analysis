#coding=utf-8
import sys,os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis
import base64

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


global redis_cli,log_path
log_path = '../log'

def addNewLink(link):
    global redis_cli
    task_list = list(redis_cli.lrange("TASK",0,-1))
    if bytes(link, encoding='utf-8') in task_list:
        return False
    redis_cli.rpush("TASK",link)
    return True

def queryLink(link):
    global redis_cli,log_path
    link = bytes(link, encoding='utf-8')
    task_list = list(redis_cli.lrange("TASK",0,-1))
    if link in task_list:
        return "Waiting"
    else:
        logfile = log_path+'/'+str(base64.b64encode(link),encoding='utf-8') + '.log'
        log = open(logfile,'r')
        rate = ""
        speed = ""
        for line in log:
            if '%' in line and 'B/s' in line:
                items = line.split(' ')
                for i in range(len(items)):
                    if '%' in items[i]:
                        rate = items[i]
                    elif 'B/s' in items[i]:
                        speed = items[i-1]+' '+items[i][0:-1]
        log.close()
        if rate == '':
            return "None"
        else:
            return rate+'\t'+speed

class VideoHandler(tornado.web.RequestHandler):
    def get(self,input):
        if input == "list":
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            L = os.listdir('../static/video')
            self.write(json.dumps(L))
        elif input == "newtab":
            link = self.get_argument('link')
            if addNewLink(link):
                self.write("Add link success")
            else:
                self.write("Add failed : be in queue")
        elif input == "loginfo":
            link = self.get_argument('link')
            self.write(queryLink(link))

class H5VideoHandler(tornado.web.RequestHandler):
    def get(self,input):
        pass

class H5TaskHandler(tornado.web.RequestHandler):
    def get(self,input):
        pass



if __name__ == '__main__':
    global redis_cli
    redis_cli = redis.StrictRedis(host='127.0.0.1',port='6379')

    tornado.options.parse_command_line()
    settings = {
        "template_path":os.path.join(os.path.dirname(__file__), "../templates"),
        "static_path":os.path.join(os.path.dirname(__file__), "../static")
    }
    app = tornado.web.Application(
        handlers=[
            (r"/video/(\w+)", VideoHandler),
            (r"/h5/video/(\w+)",H5VideoHandler),
            (r"/h5/task/(\w+)",H5TaskHandler)
        ],
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(int(options.port), "0.0.0.0")# listen local only "127.0.0.1"
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()
