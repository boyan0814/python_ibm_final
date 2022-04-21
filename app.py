from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random;

app = Flask(__name__)
#時間轉毫秒
time = {"30秒":30000, "1分鐘":60000, "5分鐘":300000}
#Keyword轉文章
word = {"A PIGEON":"A pigeon, oppressed by excessive thirst, saw a goblet of water painted on a signboard. Not supposing it to be only a picture, she flew towards it with a loud whir and unwittingly dashed against the signboard, jarring herself terribly. Having broken her wings by the blow, she fell to the ground, and was caught by one of the bystanders.",
"The Raven and the Swan":"A raven saw a Swan and desired to secure for himself the same beautiful plumage. Supposing that the Swans splendid white color arose from his washing in the water in which he swam, the Raven left the altars in the neighborhood where he picked up his living, and took up residence in the lakes and pools. But cleansing his feathers as often as he would, he could not change their color, while through want of food he perished.",
"The Bat and the Weasels":"Abat who fell upon the ground and was caught by a Weasel pleaded to be spared his life. The Weasel refused, saying that he was by nature the enemy of all birds. The Bat assured him that he was not a bird, but a mouse, and thus was set free. Shortly afterwards the Bat again fell to the ground and was caught by another Weasel, whom he likewise entreated not to eat him. The Weasel said that he had a special hostility to mice. The Bat assured him that he was not a mouse, but a bat, and thus a second time escaped.",
"The Ass and the Grasshopper":"An ass having heard some Grasshoppers chirping, was highly enchanted; and, desiring to possess the same charms of melody, demanded what sort of food they lived on to give them such beautiful voices. They replied, The dew. The Ass resolved that he would live only upon dew, and in a short time died of hunger.",
"The Dog and the Shadow":"It happened that a Dog had got a piece of meat and was carrying it home in his mouth to eat it in peace. Now, on his way home he had to cross a plank lying across a running brook. As he crossed, he looked down and saw his own shadow reflected in the water beneath. Thinking it was another dog with another piece of meat, he made up his mind to have that also. So he made a snap at the shadow in the water, but as he opened his mouth the piece of meat fell out, dropped into the water and was never seen more.",
"Apple":"A man was going to the house of some rich person. As he went along the road, he saw a box of good apples at the side of the road. He said, I do not want to eat those apples; for the rich man will give me much food; he will give me very nice food to eat. Then he took the apples and threw them away into the dust. He went on and came to a river. The river had become very big; so he could not go over it. He waited for some time; then he said, I cannot go to the rich mans house today, for I cannot get over the river. He began to go home. He had eaten no food that day. He began to want food. He came to the apples, and he was glad to take them out of the dust and eat them.",
"A bird in a dunghill":"A little bird fly to south for the winter. It was very cold, almost frozen bird. Hence, fly to a large space, after a cow there, in a pile of cow dung upon the bird, frozen bird lying on the dunghill, feel very warm, gradually recovered, it is warm and comfortable lying, and soon began to sing songs, a passing wildcat hear voices, see, follow the voice, wildcats quickly found lying on the dunghill bird,pull it out and eat it.",
"The lion in love":"A lion once fell in love with a beautiful girl, so he went to her parents and asked them to marry her to him.The old parents did not know what to say. They did not like the idea of giving their daughter to the lion, but they did not want to enrage the king of beasts. At last the father said, We are glad to marry our daughter to you, but we fear that you might possibly hurt her. So if you remove your claws and teeth, we will give her to you. The lion loved the girl very much, so he trimmed his claws and took out his big teeth. When he came to the parents again, they simply laughed in his face, and beat him out of their house.",
"Hercules and Pallas":"When Hercules was walking in the forest, he saw a ball lying on the ground. He kicked it because it blocked his way.To his surprise, the ball did not roll away, but grew much bigger than before. So he kicked it again much harder.The harder he kicked, the bigger the ball grew. At last it completely filled up the road.Pallas then appeared. Stop, Hercules, she said. Stop kicking. The balls name is Strife.Let it alone and it will soon become small again.",
"The hare and the tortoise":"The hare was once boasting of his speed before the other animals. I have never been beaten, he said, when I run at full speed, no one is faster than me. The tortoise said quietly, I will race with you. That is a good joke, said the hare. I could dance around you the whole way. The race started. The hare darted almost out of sight at once. He soon stopped and lay down to have a nap.The tortoise plodded on and on. When the hare awoke from his nap, he saw the tortoise was near the finish line, and that he had lost the race."
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#排行榜資料庫
class leadboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    usedtime = db.Column(db.Integer,nullable=False)
    correct_percent = db.Column(db.Float, nullable=False)
#首頁
@app.route('/',  methods=['GET','POST'])
def index():
    all_leadboardlist = leadboard.query.order_by(leadboard.correct_percent.desc()).order_by(leadboard.usedtime).all()
    # all_leadboardlist = leadboard.query.order_by(leadboard.correct_percent).all()
    return render_template('main.html', all_leadboardlist = all_leadboardlist)

#遊玩頁
@app.route('/start',  methods=['POST'])
def start():
    global article 
    if request.method == 'POST':
        Choose = request.form['timeDataList']
        article = request.form['articleDataList']
        print(Choose+" "+article)
        if article == "隨機文章":
            ranword =  random.choice(list(word))
            article = ranword
            return render_template('start.html',  word = word[article], time = time[Choose])
        else:
            return render_template('start.html',  word = word[article], time = time[Choose])
    else:
        return render_template('start.html')

#結算頁
@app.route('/score', methods=['POST'])
def score():
    if request.method == 'POST':
        answer = request.form['alreadyinput']

        clocktime = request.form['clocktime']
        clocktime = clocktime.replace("秒","")

        settime = request.form['settime']
        usedtime = int((int(settime)/1000)-int(clocktime))

        print(str(CheckAnswer(answer))+" "+article+" "+answer)
        print(settime)
        all_leadboardlist = leadboard.query.order_by(leadboard.correct_percent.desc()).order_by(leadboard.usedtime).all()
        return render_template('score.html', score = CheckAnswer(answer), usedtime = usedtime, all_leadboardlist = all_leadboardlist)
    else:
        return render_template('score.html')

#正確度運算
def CheckAnswer(answer):
    score = 0
    ArticleWord = word[article]
    if len(answer) < len(ArticleWord):
        answer = answer+"〃"
    print(answer+" "+str(len(answer)))
    for i in range(0,len(answer)):
        print(answer[i]+" "+str(i))
    for i in range(0,len(ArticleWord)):
        if answer[i] == ArticleWord[i]:
            score+=1
        elif answer[i] == "〃":
            break
        elif answer[i] != ArticleWord[i]:
            continue
        print(i)
    return round(score/len(ArticleWord)*100, 2)

#排行榜中繼頁面
@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    if request.method == 'POST':
        name = request.form['name']
        usedtime = request.form['usedtime']
        score = request.form['score']
        print(score)
        new_leadboard = leadboard(name=name, usedtime=int(usedtime), correct_percent=float(score))
        db.session.add(new_leadboard)
        db.session.commit()
        # 建立資料庫將資料存入，並將資料庫資料更新回 main.html
        all_leadboardlist = leadboard.query.order_by(leadboard.correct_percent.desc()).all()
        # return render_template('main.html', all_leadboardlist = all_leadboardlist)
        return redirect("/")
    else:
        return redirect("/")

import os
port = int(os.getenv('PORT', 8080))
if __name__ == '__main__':
    app.secret_key = 'f14c3a5accf691a6bd6355a8ca27d56e'
    app.run(host='0.0.0.0', port=port)