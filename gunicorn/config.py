import multiprocessing

proc_name = "pjc_mc_django"
bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
threads = workers
loglevel = 'info'


def pre_request(worker, req):
    if req.path.startswith('/static') or req.path.startswith('/display'):
        return

    worker.log.info("%s %s received" % (req.method, req.path))


def post_request(worker, req, environ, resp):
    if req.path.startswith('/static') or req.path.startswith('/display'):
        return

    worker.log.info("%s %s --> %s" % (req.method, req.path, resp.status))
