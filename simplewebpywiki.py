import web
import markdown
import pickle
import os.path

urls = ('/(.*)','view')
pages = {}
if os.path.isfile("pages.p"):
  pages = pickle.load(open("pages.p")).copy()

class view:
  def GET(self,name):
    output = []
    if not name:
      web.redirect('/FrontPage')
    else:
      output.append('<html><head><title>%s</title></head>' %name)
      output.append('<body><h3>%s</h3>' % name)
      if name in pages and not 'e' in web.input():
        output.append(markdown.markdown(pages[name]))
        output.append('<p><a href="?e=1">Edit this page</a></p>')
      else:
        current=''
        if name in pages: current=pages[name]
        output.append("""<b>Enter contents for %s</b>
                <form method="POST">
                  <textarea name="c" 
                  rows=20 cols=60>%s</textarea>
                  <p><input type="submit"/></p>
                </form>""" % (name,current))
      output.append('</body></html>')
      return ''.join(output)
      
  def POST(self,name):
      pages[name]=web.input().c
      pickle.dump( pages, open("pages.p", "w"))
      web.redirect('/%s' % (name))    

if __name__ == '__main__': 
  web.application(urls, globals()).run()
