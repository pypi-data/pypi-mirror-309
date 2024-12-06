from dataclasses import dataclass
from fastapi import FastAPI, Request, Response, status
from kv import LocatableKV
from pipeteer import task, Context
from pipeteer.queues import ReadQueue, WriteQueue, Transaction, InexistentItem
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from moveread.pipelines.reorder import Input, Item, Result, Output

@dataclass
class ReorderContext(Context):
  blobs: LocatableKV[bytes]

@task()
def reorder(Qin: ReadQueue[Input], Qout: WriteQueue[Output], ctx: ReorderContext):
  
  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=ctx.log.format(ACCESS_FORMATTER),
      uvicorn=ctx.log.format(DEFAULT_FORMATTER),
    )
  )

  @app.get('/tasks')
  async def get_tasks(req: Request) -> list[Item]:
    return [Item.of(ctx.blobs, k, v) async for k, v in Qin.items()]

  @app.post('/validate')
  async def validate(id: str, result: Result, res: Response):
    try:
      async with Transaction(Qin, Qout, autocommit=True):
        await Qout.push(id, Output.of(result))
        await Qin.pop(id)
    except InexistentItem:
      res.status_code = status.HTTP_404_NOT_FOUND

  return app
