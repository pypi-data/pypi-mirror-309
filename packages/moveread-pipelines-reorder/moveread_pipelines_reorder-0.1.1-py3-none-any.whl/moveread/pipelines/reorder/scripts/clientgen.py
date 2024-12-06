from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-o', '--output', required=True)
  args = parser.parse_args()

  from openapi_ts import generate_client
  from pipeteer import Context
  from moveread.pipelines.reorder import reorder

  app = reorder.call({}, {}, Context({})) # type: ignore
  spec = app.openapi()
  generate_client(spec, args.output, args={
    '--client': '@hey-api/client-fetch',
    '--services': '{ asClass: false }',
    '--schemas': 'false'
  })

if __name__ == '__main__':
  main()