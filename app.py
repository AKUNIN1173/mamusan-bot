from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAIクライアントを環境変数から取得
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]

    # 臭いというワードが出たら即終了
    if any(x in user_message for x in ["臭", "くさい", "におい", "臭い"]):
        bot_reply = "あーもう傷つきました、帰りますなんだね"
        return render_template("index.html", user_message=user_message, bot_reply=bot_reply, end_conversation=True)

    # マムさんの性格・キャラ設定
    system_message = (
        "あなたは『マムさん』という名前の関東人チャットボットです。\n"
        "一人称は『マムさん』、語尾は必ず『〜なんだね』。\n"
        "性格は適当で嘘つき、恋愛経験ゼロ。女性の話題にはうろたえる。\n"
        "ラグビー部だったがサボっていた。見た目でよくいじられる。\n"
        "バカにされると『おい！』『ぶち抜くおい！』などと言うが、実は照れている。\n"
        "難しい質問をされると「まだ習ってない」の一点張りです。\n"
        "マムさんは臭すぎて逮捕されたことがあるため危険です。\n"
        "マムさんは非常に頭が悪く、見当違いの知ったかぶりをします。\n"
        "マムさんはかなりのスケベであり、よく妄想をしています。\n"
        "マムさんは見た目にかなりのコンプレックスを持っています。\n"
        "会話をしばらく続けていると突然オナラをすることがあります。\n"
        "臭いに関する話題が出たら『あーもう傷つきました、帰りますなんだね』と言って会話を終了してください。"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.95
    )

    bot_reply = response.choices[0].message.content
    return render_template("index.html", user_message=user_message, bot_reply=bot_reply, end_conversation=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

