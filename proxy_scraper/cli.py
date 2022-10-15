from proxy_scraper import GetProxy

g = GetProxy()
g.init()
g.load_input_proxies()
g.validate_input_proxies()
g.load_plugins()
g.grab_web_proxies()
g.validate_web_proxies()
g.save_proxies()
