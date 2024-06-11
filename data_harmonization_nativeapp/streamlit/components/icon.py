from utils import assets
from typing_extensions import Literal

class Icon:

    def __init__(self, 
        name: str, 
        width: int = 24, 
        height: int = 24, 
        alignment: Literal["left", "right", "center"] = "center"
    ):
        self.name = name
        self.width = width
        self.height = height
        self.alignment = alignment
        self.image = assets.image_b64(name)

    def get_bg_style(self) -> str:
        return f"""
            background-size: {self.width}px {self.height}px;
            background-repeat: no-repeat; 
            background-image: url({self.image});
            background-position: {self.alignment} center;
            """
