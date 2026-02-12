
from typing import List, Optional
from fastapi import HTTPException
from bson import ObjectId
import logging

from repository.QuestionRepository import QuestionRepository
from repository.RubricRepository import RubricRepository 
from schemas.QuestionSchema import QuestionCreate, QuestionResponse, QuestionUpdate
from schemas.RubricSchema import RubricResponse
from models.QuestionModel import Question

logger = logging.getLogger(__name__)

class QuestionService:
    def __init__(self):
        self.questionRepository = QuestionRepository()
        self.rubricRepository = RubricRepository()

    async def createQuestion(self, data: QuestionCreate) -> QuestionResponse:
        try:
            questionModel = Question(**data.model_dump())
            createdQuestion = await self.questionRepository.create(questionModel)
            questionList = await self.getQuestionWithDetailRubrics([createdQuestion])

            return questionList[0]
        
        except Exception as e:
            logger.error(f"Error creating question: {e}", exc_info=True )
            raise HTTPException(status_code=500, detail="Server error")
    
    #Gom tất cả các rubricid của các question để truy vấn các rubric trong 1 lần
    async def getQuestionWithDetailRubrics(self, questions: List[Question]) -> List[QuestionResponse]:
        if not questions:
            return []
        
        allRubricIds = set()
        for q in questions: 
            for rid in q.rubrics:
                allRubricIds.add(str(rid))

        rubricModels = await self.rubricRepository.getByIds(list(allRubricIds))

        rubricMap = {
            str(r.rubricId): RubricResponse(**r.model_dump(by_alias = True)) for r in rubricModels
        }

        results = []
        for question in questions:
            questionData = question.model_dump(by_alias=True)
            questionData['rubrics'] = [
                rubricMap[str(rid)] for rid in question.rubrics if str(rid) in rubricMap
            ]
            results.append(QuestionResponse(**questionData))

        return results
    
    #Lấy danh sách câu hỏi theo đúng thứ tự của danh sách id được yêu cầu
    async def getQuestionsOrderedByIds(self, idList: List[str]) -> List[QuestionResponse]:
        try:
            questions = await self.questionRepository.getByIds(idList)
            if not questions:
                return []
            
            questionsWithRubrics = await self.getQuestionWithDetailRubrics(questions)
            questionMap = {
                str(q.questionId): q for q in questionsWithRubrics
            }

            orderedQuestions = []
            for qid in idList:
                if qid in map:
                    orderedQuestions.append(questionMap[qid])
            
            return orderedQuestions
        
        except Exception as e:
            logger.error(f"Error fetching ordered questions: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
        
    async def getAllQuestions(self) -> List[QuestionResponse]:   
        try:
            questions = await self.questionRepository.getAll()
            return await self.getQuestionWithDetailRubrics(questions)
        
        except Exception as e:
            logger.error(f"Error fetching questions list {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")

    async def getQuestionById(self, questionId: str) -> Optional[QuestionResponse]:
        if not ObjectId.is_valid(questionId):
            raise HTTPException(status_code=400, detail="Invalid question ID")
        
        try:
            question = await self.questionRepository.getById(questionId)
            if not question:
                raise HTTPException(status_code=404, detail="Required question not found")
            questionList = await self.getQuestionWithDetailRubrics([question])
            return questionList[0]
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching required question: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
    
    async def updateQuestion(self, questionId: str, data: QuestionUpdate) -> bool:  
        if not ObjectId.is_valid(questionId):
            raise HTTPException(status_code=400, detail="Invalid question ID")
        
        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return False
        try:
            isUpdated = await self.questionRepository.update(questionId, updateData)
        except Exception as e:
            logger.error(f"Error updating question: {e}")
            raise HTTPException(status_code=500, detail="Server error")

        if not isUpdated:
            existedQuestion = await self.questionRepository.getById(questionId)
            if not existedQuestion:
                raise HTTPException(status_code=404, detail="Question not found")
            return False
        return True
    
    async def deleteQuestion(self, questionId: str) -> bool:
        if not ObjectId.is_valid(questionId):
            raise HTTPException(status_code=400, detail="Invalid question ID")
        
        try:
            isDeleted = await self.questionRepository.delete(questionId)
            if not isDeleted:
                raise HTTPException(status_code=404, detail="Question not found")
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting question: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Server error")
    