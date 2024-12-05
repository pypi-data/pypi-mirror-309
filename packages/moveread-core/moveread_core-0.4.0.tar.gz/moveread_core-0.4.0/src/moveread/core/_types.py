from typing_extensions import Literal, Sequence, Iterable, ClassVar, Any, NamedTuple
from pydantic import BaseModel, Field
from haskellian import iter as I, either as E, Left, Right, Either, promise as P
from kv import KV
import pure_cv as vc
import chess_pairings as cp
from chess_notation import Language
import scoresheet_models as sm
import sequence_edits as se
from .labels import StylesNA, NA

ImageSource = Literal['robust-extraction', 'manual'] | str

class BoxContours(BaseModel):
  tag: Literal['box-contours'] = 'box-contours'
  contours: 'vc.Contours'
  relative: bool | None = None

class GridCoords(BaseModel):
  tag: Literal['grid-coords'] = 'grid-coords'
  model: sm.Model
  coords: 'vc.Rect'
  # always relative

class Corners(BaseModel):
  corners: vc.Corners
  relative: bool | None = None

Boxes = BoxContours | GridCoords

class Image(BaseModel):
  Source: ClassVar = ImageSource
  BoxContours: ClassVar = BoxContours
  GridCoords: ClassVar = GridCoords
  Boxes: ClassVar = Boxes
  Corners: ClassVar = Corners

  class Meta(BaseModel):
    source: ImageSource | None = None
    perspective_corners: 'Corners | vc.Corners | None' = None
    boxes: 'Image.Boxes | None' = Field(None, discriminator='tag')
    # bad_contours: bool | None = None # old -> switched to validated_contours
    validated_contours: bool | None = None
    """Manually validated to train TATR?"""

  url: str
  meta: Meta = Field(default_factory=lambda: Image.Meta(boxes=None))

  async def export(self, blobs: KV[bytes], *, pads: vc.Pads = {}):
    from .export import boxes
    return await boxes(self, blobs, pads=pads)
  
  def exportable(self):
    return self.meta.boxes is not None


class Sheet(BaseModel):
  class Meta(BaseModel):
    model: str
  images: list[Image]
  meta: Meta

  async def boxes(self, blobs: KV[bytes], *, pads: vc.Pads = {}) -> Either[Any, list[vc.Img]]:
    """Export boxes of the first exportable image. Returns `Left` if none of the images are exportable"""
    for image in self.images:
      boxes = await image.export(blobs, pads=pads)
      if boxes.tag == 'right':
        return boxes
    return Left('No exportable images')
  
class Sample(NamedTuple):
  img: vc.Img
  lab: str

class Player(BaseModel):
  class Meta(BaseModel):
    language: Language | NA | None = None
    styles: StylesNA = StylesNA()
    end_correct: int | None = None
    manual_labels: dict[int, str] = {}
    edits: Sequence[se.Edit[None]] = []
    @property
    def language_no_na(self) -> Language | None:
      if self.language != 'N/A':
        return self.language
      
  sheets: list[Sheet]
  meta: Meta = Field(default_factory=Meta)

  def labels(self, pgn: Iterable[str]):
    from .export import labels
    return labels(pgn, self.meta)

  def exportable(self):
    lang_ok = self.meta.language and self.meta.language != 'N/A'
    boxes_ok = any(img.exportable() for sheet in self.sheets for img in sheet.images)
    return lang_ok and boxes_ok
  
  async def boxes(self, blobs: KV[bytes], *, pads: vc.Pads = {}) -> Either[Any, list[vc.Img]]:
    """Export boxes of all exportable sheets.
    - Only the first exportable image of each sheet is taken.
    - Returns `Left` if the first sheet is not exportable. Otherwise returns as many consecutive exportable sheets as there are."""
    all_boxes = await P.all([sheet.boxes(blobs, pads=pads) for sheet in self.sheets])
    if not all_boxes or all_boxes[0].tag == 'left':
      return Left('No exportable sheets')
    return Right(I.flatten(E.take_while(all_boxes)).sync())
  
  @E.do()
  async def ocr_samples(self, pgn: Iterable[str], blobs: KV[bytes], *, pads: vc.Pads = {}) -> list[Sample]:
    """Export samples of all exportable sheets.
    - Only the first exportable image of each sheet is taken.
    - Returns `Left` if the first sheet is not exportable. Otherwise returns as many consecutive exportable sheets as there are.
    """
    labs = self.labels(pgn).unsafe()
    boxes = (await self.boxes(blobs, pads=pads)).unsafe()
    edited_boxes = se.apply(self.meta.edits, boxes)
    return [Sample(img, lab) for img, lab in zip(edited_boxes, labs) if lab is not None and img is not None]

class Game(BaseModel):
  class Meta(BaseModel):
    tournament: cp.GameId | None = None
    pgn: Sequence[str] | None = None
    early: bool | None = None
    """Whether the `PGN` stops before the game actually finished"""

  players: list[Player]
  meta: Meta = Field(default_factory=Meta)
  version: int = 0

  @property
  @I.lift
  def sheets(self) -> Iterable[tuple[tuple[int, int], Sheet]]:
    for i, player in enumerate(self.players):
      for j, sheet in enumerate(player.sheets):
        yield (i, j), sheet

  @property
  @I.lift
  def images(self) -> Iterable[tuple[tuple[int, int, int], Image]]:
    for (i, j), sheet in self.sheets:
      for k, image in enumerate(sheet.images):
        yield (i, j, k), image

  async def ocr_samples(self, blobs: KV[bytes], *, pads: vc.Pads = {}) -> Either[Any, list[list[Sample]]]:
    """Export OCR samples of all players.
    - Only the first exportable image of each sheet is taken.
    - Returns `Left` if the game's meta has no PGN or no player is exportable"""
    if not self.meta.pgn:
      return Left('No PGN')
    samples = await P.all([player.ocr_samples(self.meta.pgn, blobs, pads=pads) for player in self.players])
    return E.sequence(samples)
  