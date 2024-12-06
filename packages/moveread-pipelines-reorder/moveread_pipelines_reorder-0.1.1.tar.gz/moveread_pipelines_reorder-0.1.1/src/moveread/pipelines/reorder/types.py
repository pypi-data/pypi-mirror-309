from typing_extensions import Sequence, TypedDict
from dataclasses import dataclass
from kv import LocatableKV

class GameId(TypedDict):
  group: str
  round: str
  board: str

class Input(TypedDict):
  gameId: GameId
  tournId: str
  imgs: Sequence[str]

@dataclass
class Img:
  url: str
  id: str

@dataclass
class Item:
  gameId: GameId
  id: str
  tournId: str
  imgs: Sequence[Img]

  @classmethod
  def of(cls, images: LocatableKV[bytes], id: str, inp: Input) -> 'Item':
    return cls(
      gameId=inp['gameId'], id=id, tournId=inp['tournId'],
      imgs=[Img(id=img, url=images.url(img)) for img in inp['imgs']]
    )
  
@dataclass
class Result:
  # gameId: GameId
  imgs: Sequence[Img]
  
@dataclass
class Output:
  # gameId: GameId
  imgs: Sequence[str]

  @classmethod
  def of(cls, result: Result) -> 'Output':
    return cls(
      # gameId=result.gameId,
      imgs=[img.id for img in result.imgs]
    )