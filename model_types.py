from pydantic import BaseModel


class YieldResponse(BaseModel):
    city: str = ''
    area: float = 0.00
    crop: str = ''
    soil: str = ''
    produce: float = 0.00

    # def __init__(self, *args):
    #     super(YieldResponse, self).__init__(*args)


class PredictionRequest(BaseModel):
    city: str = ''
    area: float = 0.00
    crop: str = ''
    soil: str = ''
    season: str = ''
