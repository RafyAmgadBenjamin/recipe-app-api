from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""

    # since "ingredients","tags" are not part
    # of serializer they reference another model, we need to define them as special fields
    # it list object(ingredients) with the primary key ID (this what we want we don't want )
    # to list all the data we just want here the ids of the ingredients
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ("id", "title", "ingredients", "tags", "time_minutes", "price", "link")
        read_only_fields = ("id",)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe details"""

    # we can nest serializers and use them
    # many as it is many to many relationship and read_only mean
    # read_only means you can't create a recipe by providing this values
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ("id", "image")
        read_only_fields = ("id",)
