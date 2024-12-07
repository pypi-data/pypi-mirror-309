__version__ = "0.0.1"

from dataclasses import dataclass
import io
from abc import ABC, abstractmethod
from fastapi.responses import Response
from typing import List, Dict

import PIL.Image


class PILResponse(Response):
    media_type = "image/png"

    def render(self, content: 'PIL.Image') -> bytes:
        img_byte_arr = io.BytesIO()
        content.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return img_byte_arr.read()

async def ggrid(image_bytes: bytes):
    import time
    timings = {}

    # Image loading
    t_start = time.time()
    from PIL import Image, ImageDraw, ImageOps, ImageFont
    image = Image.open(io.BytesIO(image_bytes))

    ratio = image.height / image.width
    # compress to lossy JPEG old_img
    # old_img.save("old_img.jpg", "JPEG", quality=80)

    image = image.convert("RGBA")

    image = image.resize((300, int(300 * ratio))).convert("RGB")
    # compress to loss
    old_img = image.copy()
    timings['image_loading'] = time.time() - t_start

    # Grid setup
    t_start = time.time()
    grid_rows, grid_cols = 8, 8
    # if image.width > image.height:
    #     grid_rows = 8
    cell_width = image.width // grid_cols
    cell_height = image.height // grid_rows
    timings['grid_setup'] = time.time() - t_start

    # Font setup
    t_start = time.time()
    optimal_for_size = 18
    if image.width < 350:
        optimal_for_size = 14
    if image.width > 1000:
        optimal_for_size = 24
    font = ImageFont.truetype("DejaVuSans.ttf", optimal_for_size)
    timings['font_setup'] = time.time() - t_start

    # Grid drawing
    t_start = time.time()
    coords = {}
    for row in range(grid_rows):
        for col in range(grid_cols):
            tile_number = row * grid_cols + col + 1
            x0, y0 = col * cell_width, row * cell_height
            x1, y1 = x0 + cell_width, y0 + cell_height
            coords[str(tile_number)] = [x0, y0, x1, y1]

            draw_rect = ImageDraw.Draw(image)

            # draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0, 50), width=1)
            text_position = (x0 + 5, y0 + 5)
            text_position_shadow1 = (x0 + 6, y0 + 6)
            text_position_shadow2 = (x0 + 4, y0 + 4)
            text_position_shadow3 = (x0 + 5, y0 + 4)
            text_position_shadow4 = (x0 + 4, y0 + 5)

            draw_rect.text(text_position_shadow1, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position_shadow2, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position_shadow3, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position_shadow4, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position, str(tile_number), fill=(255, 255, 255, 150), font=font)
    timings['grid_drawing'] = time.time() - t_start

    # Image conversion and ChatGPT setup
    t_start = time.time()
    json_ex = '{"handles": {"35": true}, "straps": {"22": true, "20": true}, "wheels": []}'
    timings['conversion_setup'] = time.time() - t_start

    ex2 = '{ "straps": ["22", "50"], "wheels": ["12"]}'
    # ChatGPT API call
    t_start = time.time()
    call2 = await gemini(any_json=True, file=image, noresize=True,
                         prompt=f"Return the overlay grid's tile numbers that contain luggage straps, handles and wheels as JSON. The final output should look liks this: {ex2}")
    # parse {"bounding_boxes": [[8, 224, 352, 704]], "straps": ["4", "5", "6", "12", "13", "14"], "wheels": ["35", "37"]}

    timings['chatgpt_call'] = time.time() - t_start

    # Point drawing
    t_start = time.time()
    bboxes = []
    # draw = ImageDraw.Draw(old_img  )

    for object_type, items in call2.items():
        if isinstance(items, list):
            for item in items:
                tile_bbox = coords[str(item)]
                position = True
                x_center = (tile_bbox[0] + tile_bbox[2]) / 2
                y_center = (tile_bbox[1] + tile_bbox[3]) / 2

                if isinstance(position, list) and len(position) == 2:
                    x_rel, y_rel = position
                    point = (
                        tile_bbox[0] + x_rel * (tile_bbox[2] - tile_bbox[0]),
                        tile_bbox[1] + y_rel * (tile_bbox[3] - tile_bbox[1])
                    )
                elif isinstance(position, bool):
                    point = (x_center, y_center)

                draw_rect.ellipse([point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5], fill="blue")

    if bboxes:
        for bbox in bboxes:
            draw_rect.rectangle([bbox['x'], bbox['y'], bbox['x2'], bbox['y2']], outline="red", width=2)
    timings['point_drawing'] = time.time() - t_start

    # Log timings
    print("Performance measurements:")
    for operation, duration in timings.items():
        print(f"{operation}: {duration:.4f} seconds")

    return PILResponse(image)


async def ggrid2():
    import time
    timings = {}

    # Image loading
    t_start = time.time()
    from PIL import Image, ImageDraw, ImageOps, ImageFont
    image = Image.open(io.BytesIO(await m.read()))

    ratio = image.height / image.width
    # compress to lossy JPEG old_img
    # old_img.save("old_img.jpg", "JPEG", quality=80)

    image = image.convert("RGBA")
    image = image.resize((300, int(300 * ratio))).convert("RGB")
    # compress to loss
    old_img = image.copy()
    timings['image_loading'] = time.time() - t_start

    # Grid setup
    t_start = time.time()
    grid_rows, grid_cols = 8, 8
    # if image.width > image.height:
    #     grid_rows = 8
    cell_width = image.width // grid_cols
    cell_height = image.height // grid_rows
    timings['grid_setup'] = time.time() - t_start

    # Font setup
    t_start = time.time()
    optimal_for_size = 18
    if image.width < 350:
        optimal_for_size = 14
    if image.width > 1000:
        optimal_for_size = 24
    font = ImageFont.truetype("DejaVuSans.ttf", optimal_for_size)
    timings['font_setup'] = time.time() - t_start

    # Grid drawing
    t_start = time.time()
    coords = {}
    for row in range(grid_rows):
        for col in range(grid_cols):
            tile_number = row * grid_cols + col + 1
            x0, y0 = col * cell_width, row * cell_height
            x1, y1 = x0 + cell_width, y0 + cell_height
            coords[str(tile_number)] = [x0, y0, x1, y1]

            draw_rect = ImageDraw.Draw(image)

            # draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0, 50), width=1)
            text_position = (x0 + 5, y0 + 5)
            text_position_shadow1 = (x0 + 6, y0 + 6)
            text_position_shadow2 = (x0 + 4, y0 + 4)
            text_position_shadow3 = (x0 + 5, y0 + 4)
            text_position_shadow4 = (x0 + 4, y0 + 5)

            draw_rect.text(text_position_shadow1, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position_shadow2, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position_shadow3, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position_shadow4, str(tile_number), fill=(0, 0, 0, 50), font=font)
            draw_rect.text(text_position, str(tile_number), fill=(255, 255, 255, 150), font=font)
    timings['grid_drawing'] = time.time() - t_start

    # Image conversion and ChatGPT setup
    t_start = time.time()
    json_ex = '{"handles": {"35": true}, "straps": {"22": true, "20": true}, "wheels": []}'
    timings['conversion_setup'] = time.time() - t_start

    ex2 = '{ "straps": ["22", "50"], "wheels": ["12"]}'
    # ChatGPT API call
    t_start = time.time()
    call2 = await gemini(any_json=True, file=image, noresize=True,
                         prompt=f"Return the overlay grid's tile numbers that contain luggage straps, handles and wheels as JSON. The final output should look liks this: {ex2}")
    # parse {"bounding_boxes": [[8, 224, 352, 704]], "straps": ["4", "5", "6", "12", "13", "14"], "wheels": ["35", "37"]}

    timings['chatgpt_call'] = time.time() - t_start

    # Point drawing
    t_start = time.time()
    bboxes = []
    # draw = ImageDraw.Draw(old_img  )

    for object_type, items in call2.items():
        if isinstance(items, list):
            for item in items:
                tile_bbox = coords[str(item)]
                position = True
                x_center = (tile_bbox[0] + tile_bbox[2]) / 2
                y_center = (tile_bbox[1] + tile_bbox[3]) / 2

                if isinstance(position, list) and len(position) == 2:
                    x_rel, y_rel = position
                    point = (
                        tile_bbox[0] + x_rel * (tile_bbox[2] - tile_bbox[0]),
                        tile_bbox[1] + y_rel * (tile_bbox[3] - tile_bbox[1])
                    )
                elif isinstance(position, bool):
                    point = (x_center, y_center)

                draw_rect.ellipse([point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5], fill="blue")

    if bboxes:
        for bbox in bboxes:
            draw_rect.rectangle([bbox['x'], bbox['y'], bbox['x2'], bbox['y2']], outline="red", width=2)
    timings['point_drawing'] = time.time() - t_start

    # Log timings
    print("Performance measurements:")
    for operation, duration in timings.items():
        print(f"{operation}: {duration:.4f} seconds")

    return PILResponse(image)

@dataclass
class Bbox:
    x1: float
    y1: float
    x2: float
    y2: float

class Annotator(ABC):
    @abstractmethod
    def annotate(self, image: List, ontology: List[str]) -> Dict[str, List[Bbox]]:
        pass

    # @abstractmethod
    def query(self, image: PIL.Image.Image):
        pass

class ChatGpt(Annotator):
    def annotate(self, image: List, ontology: List[str]) -> Dict[str, List[Bbox]]:
        pass
    pass


class Gemini(Annotator):
    def annotate(self, image: List, ontology: List[str]) -> Dict[str, List[Bbox]]:
        pass
    pass

__all__ = ["__version__", "add", "subtract", "Annotator", "ChatGpt"]
