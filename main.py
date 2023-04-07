# encoding=utf-8
import asyncio
import random
import re
from functools import partial
from pathlib import Path

import gradio as gr
import httpcore
from EdgeGPT import Chatbot, ConversationStyle
from utils import postprocess

cookiePath = r"./cookiePath"  # 填写存放Bing的cookies目录
cookieList = [_ for _ in Path(cookiePath).iterdir()]
cookieDict = {}  # {IP: [bot, Bing]}
IP = ""
QUESTION = []

gr.Chatbot.postprocess = postprocess
# 读取css文件
with open("./static/main.css", "r", encoding="utf-8") as f:
    my_css = f.read()


async def get_message(message):
    """
    从Bing请求数据.
    """
    try:
        rs = await cookieDict[IP][1](prompt=message)
    except httpcore.ConnectTimeout as exc:
        return ["请求失败，请重试……", []]
    except Exception as exc:
        return ["请求失败，请重试……", []]

    try:
        association = [
            _["text"] for _ in rs["item"]["messages"][1]["suggestedResponses"]
        ]
    except KeyError:
        association = []

    try:
        quotes = rs["item"]["messages"][1]["adaptiveCards"][0]["body"]
    except KeyError:
        quotes = []

    if quotes.__len__() == 1:
        body, quotes = quotes[0]["text"], []
    elif quotes.__len__() > 1:
        quotes = quotes[0]["text"]
        split = quotes.find("\n\n")
        body = quotes[split + 2 :]
        quotes = quotes[:split]
        quotes_ = []
        quotes = quotes.split("\n")
        count = 1
        for quote in quotes:
            quote = quote[quote.find(": ") + 2 :]
            s = quote.find(" ")
            # quotes_.append({"url": quote[:s], "title": quote[s + 2 : -1]})
            quotes_.append(
                f"""<a href={quote[:s]} target="_blank">[{count}]: {quote[s+2:-1]}</a>"""
            )
            count += 1
        quotes = "\n".join(quotes_)
        body += "\n了解详细信息：\n" + quotes
    else:
        body = ""
    body = re.sub(r"\[\^(\d+)\^\]", "", body)
    return [body, association]


# 创建一个 Gradio Blocks 对象
with gr.Blocks(css=my_css) as demo:
    # 创建一个Radio用于选择聊天风格
    with gr.Accordion(label="点这里切换Ai风格", open=False):
        chat_style = gr.Radio(
            ["🥳更有创造性", "😊两者间平衡", "🤓更有精确性"],
            value="😊两者间平衡",
            show_label=False,
            elem_id="style_select",
        )
    # 创建一个聊天机器人
    chatbot = gr.Chatbot(show_label=False, elem_id="chat_window")
    chatbot.style(height="100%")
    # 创建三个备选项
    with gr.Row():
        question1 = gr.Button("你好，Bing。你可以帮我做什么？").style(size="sm")
        question2 = gr.Button("你好，Bing。请随便写一首诗。").style(size="sm")
        question3 = gr.Button("你好，Bing。帮我搜索最近的新闻。").style(size="sm")

    # 创建一个文本框
    msg = gr.Textbox(show_label=False, elem_id="user_input", placeholder="有问题尽管问我……")

    with gr.Row():
        # 创建一个清除按钮
        clear = gr.Button("🧹打扫干净屋子再请客🤖").style(size="sm")
        # 创建一个提交按钮
        btn = gr.Button(value="⬆️把消息告诉Bing🅱️").style(size="sm")

    # chat_style改变时的事件
    def change_style(choice, history, request: gr.Request):
        global IP
        IP = request.client.host
        if IP not in cookieDict:
            cookieDict[IP] = [Chatbot(random.choice(cookieList)), None]
        if choice == "🥳更有创造性":
            cookieDict[IP][1] = partial(
                cookieDict[IP][0].ask, conversation_style=ConversationStyle.creative
            )
            return history + [[None, "好的我会更有创造性，让我们重新开始"]]
        elif choice == "😊两者间平衡":
            cookieDict[IP][1] = partial(
                cookieDict[IP][0].ask, conversation_style=ConversationStyle.balanced
            )
            return history + [[None, "好的我会尽量保持平衡，让我们重新开始"]]
        else:
            cookieDict[IP][1] = partial(
                cookieDict[IP][0].ask, conversation_style=ConversationStyle.precise
            )
            return history + [[None, "好的我会更有精确性，让我们重新开始"]]

    # 绑定chat_style选择时的事件
    chat_style.change(fn=change_style, inputs=[chat_style, chatbot], outputs=chatbot)

    # 用户输入的回调函数
    def user(user_message, history, choice, request: gr.Request):
        """
        user 函数的目的是将用户输入添加到历史记录中。history 参数实际上是 chatbot 对象，而不是一个列表。但是，chatbot 对象是一个包含历史记录的列表，第一个返回值作为点击submit后的输入框值。
        """
        global IP
        if user_message == "" or user_message == None:
            return "", history
        IP = request.client.host
        if IP not in cookieDict:
            cookieDict[IP] = [Chatbot(random.choice(cookieList)), None]
            if choice == "🥳更有创造性":
                cookieDict[IP][1] = partial(
                    cookieDict[IP][0].ask, conversation_style=ConversationStyle.creative
                )
            elif choice == "😊两者间平衡":
                cookieDict[IP][1] = partial(
                    cookieDict[IP][0].ask, conversation_style=ConversationStyle.balanced
                )
            else:
                cookieDict[IP][1] = partial(
                    cookieDict[IP][0].ask, conversation_style=ConversationStyle.precise
                )
        return "", history + [[user_message, None]]

    # 机器人回复的回调函数
    def bing(history):
        global QUESTION
        if history:
            user_message = history[-1][0]
            # bot_message = random.choice(["# Yes", "## No"])
            # bot_message = [r'<a href="www.baidu.com">百度</a>']
            bot_message = asyncio.run(get_message(user_message))
            # bot_message = ['1', ['1','2','3']]
            history[-1][1] = bot_message[0]
            QUESTION = bot_message[1]
        return history

    def change_question():
        """
        更改快速选项
        """
        global QUESTION
        match len(QUESTION):
            case 0:
                gr.Button.update(visible=False), gr.Button.update(
                    visible=False
                ), gr.Button.update(visible=False)
            case 1:
                return (
                    gr.Button.update(value=QUESTION[0]),
                    gr.Button.update(visible=False),
                    gr.Button.update(visible=False),
                )
            case 2:
                return (
                    gr.Button.upda1te(value=QUESTION[0]),
                    gr.Button.update(value=QUESTION[1]),
                    gr.Button.update(visible=False),
                )
            case _:
                return (
                    gr.Button.update(value=QUESTION[1]),
                    gr.Button.update(value=QUESTION[1]),
                    gr.Button.update(value=QUESTION[2]),
                )

    # 快速选择时的事件
    question1.click(
        fn=user,
        inputs=[question1, chatbot, chat_style],
        outputs=[msg, chatbot],
        queue=False,
    ).then(fn=bing, inputs=[chatbot], outputs=[chatbot], queue=False).then(
        fn=change_question, inputs=[], outputs=[question1, question2, question3]
    )
    question2.click(
        fn=user,
        inputs=[question2, chatbot, chat_style],
        outputs=[msg, chatbot],
        queue=False,
    ).then(fn=bing, inputs=chatbot, outputs=chatbot, queue=False).then(
        fn=change_question, inputs=[], outputs=[question1, question2, question3]
    )
    question3.click(
        fn=user,
        inputs=[question3, chatbot, chat_style],
        outputs=[msg, chatbot],
        queue=False,
    ).then(fn=bing, inputs=chatbot, outputs=chatbot, queue=False).then(
        fn=change_question, inputs=[], outputs=[question1, question2, question3]
    )

    # 将用户输入和机器人回复绑定到 msg.submit() 方法上
    msg.submit(
        fn=user, inputs=[msg, chatbot, chat_style], outputs=[msg, chatbot], queue=False
    ).then(fn=bing, inputs=chatbot, outputs=chatbot, queue=False)

    # 发送按钮的事件
    btn.click(
        fn=user, inputs=[msg, chatbot, chat_style], outputs=[msg, chatbot], queue=False
    ).then(fn=bing, inputs=chatbot, outputs=chatbot, queue=False)

    def clean():
        return (
            gr.Button.update(value="你好，Bing。你可以帮我做什么？"),
            gr.Button.update(value="你好，Bing。请随便写一首诗。"),
            gr.Button.update(value="你好，Bing。帮我搜索最近的新闻。"),
        )

    # 将清除按钮绑定到 clear.click() 方法上
    clear.click(lambda: None, None, chatbot, queue=False).then(
        fn=clean, inputs=[], outputs=[question1, question2, question3]
    )

if __name__ == "__main__":
    # demo.queue(concurrency_count=9)
    demo.title = "Bing本地服务"
    demo.launch(server_name="0.0.0.0", server_port=5000)
