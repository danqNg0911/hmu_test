from fastapi import APIRouter, Body
from typing import List

from models.exam_session import ExamSession
from schemas.exam_session import ExamSessionCreate, ExamSessionResponse

router = APIRouter()