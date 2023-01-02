from flask import Flask, render_template, url_for, request
import bot

app = Flask(__name__)

#Need to come up with a way to take notes on the fly
#Decorators are function triggers ***we do not call the index function in the script bc the decorator tells python to call index whenever the root url is accessed
# the route method is used as a decorator. It makes use of another method called add_url_rule
@app.route('/')
def index():
    return render_template("index.html")

#Flask comes with a cli commands
#still needs to figure out how to make the development server visible to other devices on the network

#HTML Escaping
#any user provided value must be escaped to prevent injection attacks

#eg
#from markupsafe import escape
#@app.route("/<name>")
#def hello(name):
#   return f"Hello, {escape(name)}!"

#useful everytime the user enters something in the webapp and that input will be part of the route or used as a function input

#the way we handle data from the internet is with the module called request after writing the handling function and decorating it with the appropriate route we can add if statememnts to classify requests by methods (POST or GET)

@app.route("/scrap", methods=["GET", "POST"])
def scrap():
    print("Scrapping...")
    if request.method == "POST":
        print("POSTING DATA")
        concept = request.form.get("concept")
        print("GOT concept")
        scrapper = bot.Bot(concept)
        print("Bot initialized with the keyword")
        article, title = scrapper.scrap_article()
        print("Scrapped article and generated the title")
        print(article)
        
    return article

#Routing

# variable rules
#app.route("/user/<username>")
#def show_user_profile(username):
    #return f"User {escape(username)}"



if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")