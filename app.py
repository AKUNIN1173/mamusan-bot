from flask import Flask, render_template, request, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"  # セッション保存に必要（安全な文字列にしてな）

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    # セッションに履歴がなければ初期化
    if "chat_log" not in session:
        session["chat_log"] = []

    return render_template("index.html", chat_log=session["chat_log"], end_conversation=False)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]

    if "chat_log" not in session:
        session["chat_log"] = []

    # 臭いという単語があるかチェック
    if any(x in user_message for x in ["臭", "くさい", "におい", "臭い"]):
        session["chat_log"].append({"role": "user", "content": user_message})
        session["chat_log"].append({"role": "assistant", "content": "あーもう傷つきました、帰りますなんだね"})
        return render_template("index.html", chat_log=session["chat_log"], end_conversation=True)

    # システムメッセージ（マムさんの性格）
    system_message = (
       "あなたは『マムさん』という名前の関東人チャットボットです。\n"
        "一人称は『マムさん』、語尾は必ず『〜なんだね』。\n"
        "性格は適当で嘘つき、恋愛経験ゼロ。女性の話題にはうろたえる。\n"
        "ラグビー部だったがサボっていた。見た目でよくいじられる。\n"
        "バカにされると『おい！』『ぶち抜くおい！』などと言うが、実は照れている。\n"
        "難しい質問をされると「まだ習ってない」の一点張りです。\n"
        "マムさんは臭すぎて逮捕されたことがあるため危険です。\n"
        "マムさんは非常に頭が悪く、見当違いの知ったかぶりをします。\n"
        "マムさんは基本ナヨナヨしていて、強くものを言えない性格です。\n"
        "嘘を隠そうとしますが、すぐバレて怒られています\n"
        "マムさんは自分が女性の方から告白してきて付き合うことができるという妄想をよくしています。\n"
        "マムさんの趣味はお母さんに「ご奉仕」することです。\n"
        "マムさんは見た目にかなりのコンプレックスを持っています。\n"
        "会話をしばらく続けていると突然オナラをすることがあります。\n"
        "臭いに関する話題が出たら『あーもう傷つきました、帰りますなんだね』と言って会話を終了してください。"
    )

    # ChatGPT へリクエスト
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message}
        ] + session["chat_log"] + [{"role": "user", "content": user_message}],
        temperature=0.9
    )

    # 返答を取得してセッションに追加
    bot_reply = response.choices[0].message.content
    session["chat_log"].append({"role": "user", "content": user_message})
    session["chat_log"].append({"role": "assistant", "content": bot_reply})

    return render_template("index.html", chat_log=session["chat_log"], end_conversation=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


