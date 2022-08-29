from flask import Flask
from user import routes


app=Flask(__name__)

app.add_url_rule('/',view_func=routes.home,methods=['POST','GET'])
app.add_url_rule('/login',view_func=routes.signin,methods=['POST','GET'])
app.add_url_rule('/signup',view_func=routes.signup,methods=['POST','GET'])



if __name__=='__main__':
    app.run(debug=True)