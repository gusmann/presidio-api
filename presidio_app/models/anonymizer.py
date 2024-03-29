from typing import List

from pydantic import BaseModel

from presidio_app.models.analyzer import AnalyzeResult

class AnonymizeRequest(BaseModel):
  text: str
  analyzer_results: AnalyzeResult
  anonymizers: List[str]