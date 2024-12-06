

from mtmai.workflows.showtimer import DemoTimerFlow
from mtmai.workflows.wfapp import wfapp
from mtmai.workflows.basicrag import BasicRagWorkflow


def deploy_mtmai_workers():
    worker = wfapp.worker("basic-rag-worker2")
    worker.register_workflow(BasicRagWorkflow())
    worker.register_workflow(DemoTimerFlow())


    worker.start()
