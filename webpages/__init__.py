
def start_server(script_path,script_name):
	import tornado.httpserver
	import tornado.web
	import tornado.ioloop
	import tornado.autoreload
	import site

	from handlers import PORT,SITE,urls
	
	print 'Running Server on port %s' % PORT

	ioloop = tornado.ioloop.IOLoop.instance()

	settings = dict(
		debug=True,
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

	http_server.listen(SITE["port"])
	
	tornado.autoreload.start(io_loop=ioloop)
	ioloop.start()

def apply_site_dirs():
	import os, fs, site
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
	import os, fs, site
	from os.path import join, exists

	apply_site_dirs()

	import logging
	# print 'logging to testing.log', structure.DEFAULT_HOSTNAME
	LOG_FILENAME = join(site.PROJECT_DIR,'testing.log')
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

	from cached import populate_cache
	populate_cache()
	start_server(site.PROJECT_DIR,"runserver")

def populatecache():
	import os, fs, site
	from os.path import join, exists

	apply_site_dirs()

	from cached import populate_cache
	populate_cache()
