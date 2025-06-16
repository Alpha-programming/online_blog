from ninja import NinjaAPI # type: ignore
from .categories import router as categories_router
from .slider import router as slider_router
from .faq import router as faq_router
from .comments import router as comments_router
from .articles import router as articles_router
from .auth import router as auth_router

api_router = NinjaAPI()

api_router.add_router(prefix='/api/' ,router=categories_router)
api_router.add_router(prefix='/api/' ,router=slider_router)
api_router.add_router(prefix='/api/' ,router=faq_router)
api_router.add_router(prefix='/api/' ,router=comments_router)
api_router.add_router(prefix='/api/' ,router=articles_router)
api_router.add_router(prefix='/api/' ,router=auth_router)

