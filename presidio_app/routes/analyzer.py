import logging
from typing import Any, Tuple, Any, List

from fastapi import APIRouter, HTTPException, Request

from presidio_analyzer.analyzer_engine import AnalyzerEngine

from presidio_app.models.analyzer import AnalyzeRequest, AnalyzeResult
from presidio_app.config import AnalyzerSettings
from presidio_analyzer.nlp_engine.nlp_engine_provider import NlpEngineProvider

logger = logging.getLogger(__name__)

router = APIRouter()

analyzer_settings = AnalyzerSettings()

if analyzer_settings.enabled:
  nlp_engine = NlpEngineProvider(conf_file=analyzer_settings.nlp_config_file_path).create_engine()
  analyzer_engine = AnalyzerEngine(
    nlp_engine=nlp_engine
  )
  logger.info("Initialized analyzer")
else:
  analyzer_engine = None
  logger.warning(f"Unable to load analyzer with config {analyzer_settings}")


@router.post("/analyze", response_model=List[AnalyzeResult])
def analyze(request: AnalyzeRequest) -> Any:
  """Execute the analyzer function.

  Args:
      request (AnalyzeRequest): _description_

  Raises:
      HTTPException: _description_

  Returns:
      Any: _description_
  """
  if analyzer_engine is None:
    raise HTTPException(503, "presidio-analyzer not installed")
  recognizers = []
  if request.ad_hoc_recognizers:
    for r in request.ad_hoc_recognizers:
      if r.patterns or r.deny_list:
        recognizers.append(r.model_dump(exclude=["supported_entities"]))
  recognizer_result_list = analyzer_engine.analyze(
      ad_hoc_recognizers=recognizers,
      **request.model_dump(exclude=["ad_hoc_recognizers"]),
  )
  return [AnalyzeResult(**d.to_dict()) for d in recognizer_result_list]

@router.get("/recognizers", response_model=List[str])
def recognizers(language: str | None = "en"):
  """Return a list of supported recognizers.

  Args:
      language (str | None): Two-letter abbreviation of requested language. Defaults to 'en'.
  """
  if analyzer_engine is None:
    raise HTTPException(503, "presidio-analyzer not installed")
  return [r.name for r in analyzer_engine.get_recognizers(language=language)]

@router.get("/supportedentities", response_model=List[str])
def supported_entities(language: str | None = "en"):
  """Return a list of supported entities.

  Args:
      language (str | None, optional): _description_. Defaults to "en".
  """
  if analyzer_engine is None:
    raise HTTPException(503, "presidio-analyzer not installed")
  return analyzer_engine.get_supported_entities(language)