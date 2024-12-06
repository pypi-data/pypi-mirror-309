from pydantic import BaseModel
from typing import Union, Optional
from openai.types.chat import ChatCompletion


class AInsightsEvent(BaseModel):
    response: ChatCompletion

    messages: Union[str, list[str], list[dict]]
    args: dict

    user_id: Optional[str]
