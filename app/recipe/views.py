from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base Viewset for user owned recipe attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    ## We are overriding getting all the tags/ingredients in queryset (overriding the queryset)
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    # overriding the create option to assign the tag/ingredients to the correct user
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


# mixins contains the options supported here example list, create
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage Ingeredients in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


##ModelViewSet support all the operations needed, get, update ,delete, ....
class RecipeViewSets(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # __ for filter on foreign keys objects tags__id
            # the other __ id__in return all the with the id in this list we provide
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredients_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # ModelViewSet support the retrive but we want it to
        # use the new details serializer that's why we override
        # the method it use to get the right serializer
        if self.action == "retrieve":
            return serializers.RecipeDetailSerializer
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user)

    # detail means that we are going to use the ID
    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # this will get the object based on the id passed in the URL
        recipe = self.get_object()
        ### we could use here RecipeImageSerializer but we used get_serializer method
        # then we update get_serializet_class method, so it can select the correct serializer
        # this is a best bractise and allow the browseable API to works right
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            # since we are using Modelserializer it allow us to save with the update data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            # serializer will do automatic validation on our data types
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
