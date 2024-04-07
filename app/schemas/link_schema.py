from pydantic import BaseModel, Field, HttpUrl


class Link(BaseModel):
    rel: str = Field(..., description="The relation type of the link.")
    href: HttpUrl = Field(..., description="The URL of the link.")
    method: str = Field(..., description="The HTTP method for the link.")
