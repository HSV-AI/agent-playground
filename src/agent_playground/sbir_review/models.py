from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Topic(BaseModel):
    """Structured data about a single product."""
    title: str = Field(description="The title of the topic.")
    open_date: datetime = Field(description="The date when the topic was opened.")
    close_date: datetime = Field(description="The date when the topic was closed.")
    component: str = Field(description="The component associated with the topic. This should be an acronym in all capital letters.")
    technology_areas: List[str] = Field(description="A list of technology areas related to the topic.")
    modernization_priorities: List[str] = Field(description="A list of modernization priorities for the topic.")
    keywords: List[str] = Field(description="A list of keywords associated with the topic.")
    objective: str = Field(description="The main objective of the topic.")
    phases: str = Field(description="The phases involved in the topic. This should be a combination of Phase 1, Phase 2, and Phase 3 as applicable.")
    references: List[str] = Field(description="A list of references or links related to the topic.")

class ScrapeResult(BaseModel):
    """The collection of all extracted product information."""
    topics: List[Topic]
    error_message: str = Field(description="An error message if the scraping failed, otherwise empty.")
