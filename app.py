import random
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from random import sample

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catcafe.db'
db = SQLAlchemy(app)


# БАЗА ДАННЫХ (таблички)


# коты
class Catsinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about_cat = db.Column(db.Text, nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return '<Catsinfo %r>' % self.id


# отзывы
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Reviews %r>' % self.id


# анкеты укотовительства
class Getcat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.Text, nullable=False)
    cat_name = db.Column(db.Text, nullable=False)
    info_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Getcat %r>' % self.id


# СТРАНИЦЫ САЙТА


# главная страница
@app.route('/')
def index():
    return render_template('index.html')


# страница с кошками
@app.route('/cats')
def cats():
    catss = Catsinfo.query.all()
    return render_template('cats.html', cats=catss)


# прайс и бронь
@app.route('/price')
def price():
    return render_template('price.html')


# укотовительство
@app.route('/get-cat', methods=['POST', 'GET'])
def get_cat():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        cat_name = request.form['cat_name']
        info_text = request.form['info_text']

        form = Getcat(name=name, phone_number=phone_number, email=email,
                        cat_name=cat_name, info_text=info_text)

        try:
            db.session.add(form)
            db.session.commit()
            return render_template('get_cat.html')
        except:
            return 'произошла ошибка:(('
    else:
        return render_template('get_cat.html')


# отзывы
@app.route('/reviews')
def reviews():
    # обращение к бд
    all_rev = Reviews.query.all()
    return render_template('reviews.html', all_rev=all_rev)


# страница с созданием отзыва
@app.route('/add-rev', methods=['POST', 'GET'])
def add_rev():
    if request.method == 'POST':
        user_name = request.form['user_name']
        text = request.form['text']

        review = Reviews(user_name=user_name, text=text)

        try:
            db.session.add(review)
            db.session.commit()
            return redirect('/reviews')
        except:
            return 'произошла ошибка:(('
    else:
        return render_template('add_rev.html')


# КВИЗ


# все все все вопросы для квиза
quiz_db = [
    {'question': 'Какая кличка была у кота из мультипликационного сериала «Возвращение блудного попугая»?',
     'options': ['Василий', 'Барсик', 'Мурзик', 'Геннадий'],
     'answer': 'Василий'},
    {'question': 'Сколько костей у кошек?',
     'options': ['460', '120', '240', '186'],
     'answer': '240'},
    {'question': 'Сколько зубов должно быть у взрослого кота?',
     'options': ['30', '32', '45', '43'],
     'answer': '32'},
    {'question': 'В какой стране кошки считаются священными животным?',
     'options': ['Африка', 'Турция', 'Марокко', 'Египет'],
     'answer': 'Египет'},
    {'question': 'Как зовут кота из мастера и маргариты?',
     'options': ['Бегемот', 'Богомол', 'Уголь', 'Воланд'],
     'answer': 'Бегемот'},
    {'question': 'В какой священной книге нет ни одного упоминания о кошке?',
     'options': ['Коран', 'Библия', 'Танах', 'Трипитака'],
     'answer': 'Библия'},
    {'question': 'Вылизывая себя, кошка получает порцию витамина. какого?',
     'options': ['Витамин A', 'Витамин B', 'Витамин C', 'Витамин D'],
     'answer': 'Витамин D'},
    {'question': 'На каком инструменте играл кот из «бременских музыкантов»?',
     'options': ['Гитара', 'Балалайка', 'Барабаны', 'Контрабас'],
     'answer': 'Гитара'},
    {'question': 'Кто писал о «коте учёном»?',
     'options': ['Пушкин', 'Крылов', 'Чехов', 'Гоголь'],
     'answer': 'Пушкин'},
    {'question': 'Кто из перечисленных котов призывал «жить дружно»?',
     'options': ['Гарфилд', 'Том', 'Матроскин', 'Леопольд'],
     'answer': 'Леопольд'},
    {'question': 'Какой вкус коты не распознают?',
     'options': ['Сладкий', 'Солёный', 'Горький', 'Кислый'],
     'answer': 'Сладкий'},
    {'question': 'Какая знаменитость является хозяином одной из самых богатых кошек в мире Оливии Бенсон?',
     'options': ['Кэтти Перри', 'Джиджи Хадид', 'Уилл Смит', 'Тейлор Свифт'],
     'answer': 'Тейлор Свифт'},
    {'question': 'Как звали кота-мошенника из сказки «Буратино»?',
     'options': ['Артемон', 'Базилио', 'Черныш', 'Джузеппе'],
     'answer': 'Базилио'},
    {'question': 'Кто был хозяином коровы Мурки?',
     'options': ['Матроскин', 'Леопольд', 'Базилио', 'Гав'],
     'answer': 'Матроскин'},
    {'question': 'В каком городе кошки являются его полноправными жителями, а горожане '
           'о них заботятся и даже строят целые кошачьи деревни?',
     'options': ['Токио', 'Стамбул', 'Астрахань', 'Тбилиси'],
     'answer': 'Стамбул'},
    {'question': 'В каком году состоялась самая первая выставка кошек?',
     'options': ['1973', '1921', '1786', '1895'],
     'answer': '1895'},
    {'question': 'Около скольки разнообразных звуков может издавать кот?',
     'options': ['200', '100', '80', '350'],
     'answer': '100'},
    {'question': 'Как называется порода кошек с очень короткими лапками?',
     'options': ['Манчкин', 'Бурма', 'Рэгдолл', 'Бурмилла'],
     'answer': 'Манчкин'},
    {'question': 'Где появились первые котокафе?',
     'options': ['Япония', 'Сингапур', 'Тайвань', 'Южная Корея'],
     'answer': 'Тайвань'},
    {'question': 'В каком американском штате на законодательном уровне запрещены драки между кошками и собаками?',
     'options': ['Южная Каролина', 'Северная Каролина', 'Флорида', 'Техас'],
     'answer': 'Северная Каролина'},
    {'question': 'Сколько мышц в одном кошачьем ухе?',
     'options': ['22', '14', '32', '36'],
     'answer': '32'},
    {'question': 'Какая порода кошек считается самой дорогой?',
     'options': ['Саванна', 'Ориентал', 'Сфинкс', 'Манул'],
     'answer': 'Саванна'},
    {'question': 'Какой континент является родиной домашних кошек?',
     'options': ['Африка', 'Австралия', 'Южная Америка', 'Северная Америка'],
     'answer': 'Африка'},
    {'question': 'Сколько котов было у писателя Марка Твена?',
     'options': ['10', '4', '6', '19'],
     'answer': '19'},
    {'question': 'Как называется порода лысых кошек?',
     'options': ['Египетская мау', 'Сфинкс', 'Корниш рекс', 'Ликой'],
     'answer': 'Сфинкс'},
    {'question': 'Какая страна в мире занимает первое место в мире по численности домашних кошек?',
     'options': ['США', 'Тайланд', 'Япония', 'Россия'],
     'answer': 'США'},
    {'question': 'Как звали любимого кота Виктора Гюго?',
     'options': ['Табби', 'Гаврош', 'Джолин', 'Робин'],
     'answer': 'Гаврош'}
         ]

# берутся рандомные 10 вопросов и выгружаются пользователю
selected_questions = sample(quiz_db, 10)
for item in selected_questions:
    random.shuffle(item['options'])


# главная квиза
@app.route('/quiz-main')
def quiz_main():
    return render_template('quiz_main.html')


@app.route('/quiz-pass', methods=['GET', 'POST'])
def quiz_pass():
    answers = []
    questionsss = []
    correct_ans = []
    if request.method == 'POST':
        # проверка ответов
        score = 0
        for question in selected_questions:
            questionsss.append(question["question"])
            correct_ans.append(question["answer"])
            user_answer = request.form.get(question['question'])
            answers.append(user_answer)
            if user_answer == question["answer"]:
                score += 1
        return render_template('quiz_res.html', score=score, total=len(selected_questions),
                               answers=answers, questionsss=questionsss, correct_ans=correct_ans)
    return render_template('quiz_pass.html', questions=selected_questions)


if __name__ == '__main__':
    app.run(debug=True)
