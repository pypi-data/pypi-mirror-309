import os
from argparse import ArgumentParser

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser()
  parser.add_argument('--blobs', type=str, **env('BLOBS_URL'), help='Blobs KV connection string')
  parser.add_argument('--host', type=str, default='0.0.0.0')
  parser.add_argument('-p', '--port', type=int, **env('PORT', default=8000))

  args = parser.parse_args()

  import uvicorn
  from fastapi import Request, Response
  from fastapi.middleware.cors import CORSMiddleware
  from kv import KV, LocatableKV, ServerKV
  from pipeteer import Backend
  from moveread.pipelines.reorder import ReorderContext, reorder

  secret = os.environ['SECRET']
  blobs = KV.of(args.blobs, bytes)
  if not isinstance(blobs, LocatableKV):
    blobs = blobs.served(os.environ['PUBLIC_URL'].rstrip('/') + '/blobs', secret=secret)

  backend = Backend.sql()
  ctx = ReorderContext(backend, blobs=blobs)

  backend.mount(reorder, ctx)

  api = reorder.run(ctx)
  @api.middleware('http')
  async def check_token(req: Request, call_next):
    if req.headers.get('Authorization') == f'Bearer {secret}' or req.url.path.startswith('/blobs/'):
      return await call_next(req)
    else:
      ctx.log(f'Unautorized request to {req.url.path}. Authorization header: {req.headers.get("Authorization")}', level='WARNING')
      return Response(status_code=401, content='Unauthorized')
    
  backend.app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
  backend.app.mount('/blobs', ServerKV(blobs, type=bytes, secret=secret))
  backend.app.mount('/api', api)

  uvicorn.run(backend.app, host=args.host, port=args.port)

if __name__ == '__main__':
  os.chdir('/home/m4rs/mr-github/rnd/pipelines-v2')
  default_env = {
    'DB_URL': 'sqlite+aiosqlite:///docker/data/reorder.db',
    'BLOBS_URL': 'file://docker/data/blobs',
    'PUBLIC_URL': 'http://localhost:8004',
    'PORT': '8004',
    'SECRET': 'secret'
  }
  for k, v in default_env.items():
    if k not in os.environ:
      os.environ[k] = v
  main()