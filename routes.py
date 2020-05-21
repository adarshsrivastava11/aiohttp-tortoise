from views import *

def setupRouter(app): 
	 app.router.add_get('/', handle)
	 app.router.add_get('/{name}', handle)