import web
from Models import RegisterModel, LoginModel,Posts

web.config.debug = False

urls = (
    '/', "Home",
    '/register', "Register",
     '/login' , "Login",
    '/logout', "Logout",
    '/postregistration', 'PostRegistration',
    '/check-login', 'CheckLogin',
    '/post-activity', 'PostActivity'
)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("session"), initializer={'user': None})

session_data = session._initializer


render = web.template.render("Views/Templates", base="mainlayout", globals={'session': session_data, 'current_user': session_data["user"]})

# Classes/Routes
class Home:
    def GET(self):
        data = type('obj', (object,), {"username": "hello", "password": "avocado1"})
        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data['user'] = isCorrect

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()
        return render.home(posts)

class Register:
    def GET(self):
        return render.Register()

class Login:
    def GET(self):
        return render.login()


class PostRegistration:
    def POST(self):
        data = web.input()
        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data.username


class CheckLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)
        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect
        return "error"


class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


if __name__ == "__main__":
    app.run()