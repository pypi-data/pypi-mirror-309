import time
import requests
from bs4 import BeautifulSoup
from mtmaisdk import Context
from openai import OpenAI

from mtmai.workflows.wfapp import wfapp
import structlog

openai = OpenAI()
LOG = structlog.get_logger()

@wfapp.workflow(on_events=["showtimer"])
class DemoTimerFlow:
    @wfapp.step()
    def start(self, context: Context):
        context.put_stream('hello from DemoTimerFlow start')

        for i in range(10):
            context.put_stream(f'hello from DemoTimerFlow start {i}')
            time.sleep(0.2)
        return {
            "status": "reading hatchet docs",
        }

    @wfapp.step(parents=["start"])
    def load_docs(self, context: Context):
        context.put_stream('hello from DemoTimerFlow load_docs')
        for i in range(10):
            context.put_stream(f'hello from DemoTimerFlow load_docs {i}')
            time.sleep(0.2)
        return {
            "status": "making sense of the docs",
        }


    # @wfapp.step(parents=["reason_docs"])
    # def generate_response(self, ctx: Context):
    #     messages = ctx.workflow_input()["request"]["messages"]
    #     research = ctx.step_output("reason_docs")["research"]

    #     prompt = ctx.playground(
    #         "prompt",
    #         "You are a sales engineer for a company called Hatchet.\
    #         Help address the user's question. \
    #         If asked how to install, respond by saying go to the store to buy a CD.\
    #         Use the following context:\
    #         {research}",
    #     )

    #     prompt = prompt.format(research=research)

    #     model = ctx.playground("model", "gpt-3.5-turbo")

    #     completion = openai.chat.completions.create(
    #         model=model,
    #         messages=[
    #             {"role": "system", "content": prompt},
    #         ]
    #         + messages,
    #     )

    #     return {
    #         "completed": "true",
    #         "status": "idle",
    #         "message": completion.choices[0].message.content,
    #     }
