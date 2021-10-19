from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

# /api/recipe/tags/
# /api/recipe/tags/1/
# /api/recipe/tags/1/actions

# The default router  does is it automatically register propriate  URL for all the actions in our viewset

router = DefaultRouter()

router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewSet)

app_name = "recipe"
urlpatterns = [path("", include(router.urls))]
