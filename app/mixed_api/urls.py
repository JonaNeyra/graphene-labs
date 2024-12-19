from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, MedicalHistoryViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'records', MedicalHistoryViewSet)

urlpatterns = router.urls
