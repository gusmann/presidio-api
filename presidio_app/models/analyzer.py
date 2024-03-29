from typing import List, Dict, Any
from pydantic import (
  BaseModel,
  Field,
)


class EntityRecognizer(BaseModel):
  supported_entity: str | None = None
  """"""
  supported_entities: List[str] | None = Field(default_factory=list)
  """"""
  name: str | None = None
  """"""
  supported_language: str = "en"
  """"""
  version: str = "0.0.1"
  """"""
  context: List[str] | None = None
  """"""
  patterns: List[Dict[str, Any]] | None = Field(default_factory=dict)
  """"""
  deny_list: List[str] | None = Field(default_factory=list)

class AnalyzeRequest(BaseModel):
  text: str
  """the text to analyze"""
  language: str
  """the language of the text"""
  entities: List[str] | None = None
  """List of PII entities that should be looked for in the text."""
  correlation_id: str | None = None
  """cross call ID for this request"""
  score_threshold: float | None = None
  """A minimum value for which"""
  return_decision_process: bool = False
  """Whether the analysis decision process steps"""
  ad_hoc_recognizers: List[EntityRecognizer] | None = None
  """List of recognizers which will be used on this request"""
  context: List[str] | None = None
  """List of context words to enhance confidence score if matched"""
  allow_list: List[str] | None = None
  """List of words that the user defines as being allowed to keep"""
  model_config = {
        "json_schema_extra": {
            "examples": [
                {
                  "text": "John Smith drivers license is AC432223 and the zip code is 12345",
                  "language": "en",
                  "return_decision_process": False,
                  "correlation_id": "123e4567-e89b-12d3-a456-426614174000",
                  "score_threshold": 0.6,
                  "entities": ["US_DRIVER_LICENSE", "ZIP"],
                  "ad_hoc_recognizers":[
                    {
                    "name": "Zip code Recognizer",
                    "supported_language": "en",
                    "patterns": [
                        {
                        "name": "zip code (weak)", 
                        "regex": "(\\b\\d{5}(?:\\-\\d{4})?\\b)", 
                        "score": 0.01
                        }
                    ],
                    "context": ["zip", "code"],
                    "supported_entity":"ZIP"
                    }
                  ]
                }
            ]
        }
    }


  
class RecognizedMetadata(BaseModel):
  recognizer_name: str
  """ """
 
class AnalysisExplanation(BaseModel):
  recognizer: str
  """ """
  pattern_name: str
  """ """
  pattern: str
  """ """
  original_score: float
  """ """
  score: float
  """ """
  textual_explanation: str
  """ """
  score_context_improvement: float
  """ """
  supportive_context_word: str
  """ """
  validation_result: float
  """ """
  
class AnalyzeResult(BaseModel):
  start: int
  """ """
  end: int
  """ """
  score: float
  """ """
  entity_type: str
  """ """
  recognition_metadata: RecognizedMetadata
  """ """
  analysis_explanation: AnalysisExplanation | None = None
  """ """
 