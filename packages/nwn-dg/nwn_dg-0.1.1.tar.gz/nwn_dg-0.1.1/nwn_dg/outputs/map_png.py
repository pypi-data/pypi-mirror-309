import contextlib
import os
import tempfile

# pylint: disable=no-name-in-module
from cairo import FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD, Context, SVGSurface

from ..constants import DEFAULT_GRID_SIZE
from ..proxy import DungeonProxy

OFFSET = 1


class MapPNG(DungeonProxy):
    def __init__(self, dungeon, args):
        DungeonProxy.__init__(self, dungeon)
        self._filepath = args["filepath"]
        self._grid_size = args.get("png_grid_size", DEFAULT_GRID_SIZE)
        self._output_png = args.get("output_png", False)
        self._png_room_ids = args.get("pnt_room_ids", True)

        self._svgfilename = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
        self._surface = SVGSurface(
            self._svgfilename.name,
            (self.width + OFFSET * 2) * self._grid_size,
            (self.height + OFFSET * 2) * self._grid_size,
        )
        self._context = Context(self._surface)

    def __del__(self):
        self.draw()
        self.save_to_file()

        self._surface.finish()
        with contextlib.suppress(FileNotFoundError):
            os.remove(self._svgfilename.name)

    def save_to_file(self):
        self._context.save()
        if self._output_png:
            filename = self._filepath + ".png"
            self._surface.write_to_png(filename)

    def draw(self):
        ctx = self._context

        # Draw a full black background
        ctx.set_source_rgb(0, 0, 0)
        ctx.paint()

        # Draw an internal white square inside
        ctx.set_source_rgb(1, 1, 1)
        self.rectangle(0, 0, self.width, self.height)
        ctx.fill()
        ctx.stroke()

        # Draw gray grid lines, by skipping first and last lines
        ctx.set_line_width(1.0)
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        for i in range(self.width + 1):
            if i in [0, self.width]:
                continue
            self.line(i, 0, 0, self.height)
            ctx.stroke()
        for j in range(self.height + 1):
            if j in [0, self.height]:
                continue
            self.line(0, j, self.width, 0)
            ctx.stroke()

        # Blacken every empty cell
        for i in range(self.width):
            for j in range(self.height):
                cell = self.cells[i][j]
                if not cell.is_empty():
                    continue
                ctx.set_source_rgb(0, 0, 0)
                self.rectangle(i, j, 1, 1)
                ctx.fill()
                ctx.stroke()

        self.draw_png_room_ids()

    def draw_png_room_ids(self):
        if not self._png_room_ids:
            return

        ctx = self._context
        gs = self._grid_size

        ctx.set_source_rgb(0, 0, 1)
        ctx.set_font_size(gs * 16 / DEFAULT_GRID_SIZE)
        ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD)
        for room in self._dg.walk_rooms():
            identifier = str(room._orig_identifier)
            # Calculate middle:
            # Add almost one, since the baseline is the top of the cell
            x = room.x + 0.3 + (room.width // 2)
            if len(str(identifier)) >= 2:
                x -= 0.2
            y = room.y + 0.8 + (room.height // 2)
            ctx.move_to((x + OFFSET) * gs, (y + OFFSET) * gs)
            ctx.show_text(identifier)
            ctx.stroke()

            # # TODO: print cell identifiers
            # ctx.set_source_rgb(1, 0, 0)
            # ctx.set_font_size(12)
            # ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
            # for i in range(self.width):
            #     for j in range(self.height):
            #         cell = self.cells[i][j]
            #         identifier = cell._orig_identifier
            #         if identifier is None:
            #             continue
            #         msg = str(identifier)
            #         ctx.move_to((i + 0.1 + OFFSET) * gs, (j + 0.6 + OFFSET) * gs)
            #         ctx.show_text(msg)

        ##  # TODO:print deadends
        ##  ctx.set_source_rgb(1, 0, 0)
        ##  ctx.set_font_size(12)
        ##  ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
        ##  for i in range(self.width):
        ##      for j in range(self.height):
        ##          cell = self.cells[i][j]
        ##          if not cell._deadend:
        ##              continue
        ##          msg = "D"
        ##          ctx.move_to((i + 0.1 + OFFSET) * gs, (j + 0.6 + OFFSET) * gs)
        ##          ctx.show_text(msg)

        ## # print cell id according to nwn tileset
        ## ctx.set_source_rgb(1, 0, 0)
        ## ctx.set_font_size(10)
        ## ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
        ## identifier = 0
        ## for j in range(self._dg.height, 0, -1):
        ##     j -= 1
        ##     for i in range(self._dg.width):
        ##         cell = self.cells[i][j]
        ##         ctx.move_to((i + 0.1 + OFFSET) * gs, (j + 0.6 + OFFSET) * gs)
        ##         ctx.show_text(str(identifier))
        ##         identifier += 1

        ## # print cell id according to nwn tileset
        ## ctx.set_source_rgb(1, 0, 0)
        ## ctx.set_font_size(10 * gs / DEFAULT_GRID_SIZE)
        ## ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
        ## for x in range(self.width):
        ##     ctx.move_to((x + 0.3 + OFFSET) * gs, 0.7 * gs)
        ##     ctx.show_text(str(x + 0))
        ## for y in range(self.width):
        ##     ctx.move_to(0.2 * gs, (y + 0.5 + OFFSET) * gs)
        ##     ctx.show_text(str(y + 0))

    def rectangle(self, x, y, width, height):
        ctx = self._context
        gs = self._grid_size

        x += OFFSET
        y += OFFSET
        ctx.rectangle(x * gs, y * gs, width * gs, height * gs)

    def line(self, x1, y1, width, height):
        self.move_to(x1, y1)
        self.line_to(x1 + width, y1 + height)

    def move_to(self, x, y):
        ctx = self._context
        gs = self._grid_size

        x += OFFSET
        y += OFFSET
        ctx.move_to(x * gs, y * gs)

    def line_to(self, x, y):
        ctx = self._context
        gs = self._grid_size

        x += OFFSET
        y += OFFSET
        ctx.line_to(x * gs, y * gs)
