from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description="summary of the person")
    facts: list[str] = Field(description="two interesting facts about them")

    def to_dict(self):
        return {"summary": self.summary, "facts": self.facts}
    
summary_parser = PydanticOutputParser(pydantic_object=Summary)