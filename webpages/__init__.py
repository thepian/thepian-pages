import sys, os, site, logging

def start_server(script_path,script_name,options):
	import tornado.httpserver
	import tornado.web
	import tornado.ioloop
	import tornado.autoreload

	from handlers import urls
	
	logging.info('Running Server on port %s' % options.port) 

	ioloop = tornado.ioloop.IOLoop.instance()

	settings = dict(
		debug=options.debug,
		template_path=site.TEMPLATES_DIR,
		static_path=site.SITE_DIR,
        xsrf_cookies=True,
        cookie_secret="91oETzKXQAGaYDkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        # login_url="/auth/login",
	)
	application = tornado.web.Application(urls,settings)
	if settings["debug"]:
		setattr(application,"ioloop",ioloop) # for the stop-server button
	http_server = tornado.httpserver.HTTPServer(application)

	http_server.listen(options.port)
	
	tornado.autoreload.start(io_loop=ioloop)
	ioloop.start()

def apply_site_dirs():
	import fs
	from os.path import join, exists

	project_path = os.getcwd()
	setattr(site, "PROJECT_DIR", project_path)
	setattr(site, "SITE_DIR", project_path)
	setattr(site, "SCSS_DIR", project_path)
	setattr(site, "PARTS_DIR", project_path)
	setattr(site, "TEMPLATES_DIR", project_path)

	if exists(join(project_path,"_scss")):
		setattr(site, "SCSS_DIR", join(project_path,"_scss"))
	if exists(join(project_path,"_parts")):
		setattr(site, "PARTS_DIR", join(project_path,"_parts"))
	elif exists(join(project_path,"parts")):
		setattr(site, "PARTS_DIR", join(project_path,"parts"))

def runserver():
	import fs, optparse, daemon
	from os.path import join, exists
	from base import enable_logging
	from cached import populate_cache

	parser = optparse.OptionParser()
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true")
	parser.add_option("--pygments", dest="pygments", default=False, action="store_true")
	parser.add_option("--port", dest="port", default=4444)
	options, remainder = parser.parse_args()

	apply_site_dirs()
	enable_logging(options)

	populate_cache()
	pid = os.fork()
	if pid == 0: 
		# The Child Process
		with daemon.DaemonContext():
			start_server(site.PROJECT_DIR,"runserver",options)
	else:
		print "Forked a Daemon as", pid

def populatecache():
	import fs, optparse
	from os.path import join, exists

	apply_site_dirs()

	from cached import populate_cache
	populate_cache()
