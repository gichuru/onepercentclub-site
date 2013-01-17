from apps.bluebottle_drf2.serializers import  TimeSinceField, OEmbedField, PolymorphicSerializer, AuthorSerializer, ToModelIdField, ManyRelatedSerializer
from apps.projects.models import Project
from apps.reactions.serializers import ReactionSerializer
from apps.wallposts.models import WallPost
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from .models import MediaWallPost, TextWallPost


class WallPostTypeField(serializers.Field):
    """ A DRF2 Field for adding a type to WallPosts. """

    def __init__(self, type, **kwargs):
        super(WallPostTypeField, self).__init__(source='*', **kwargs)
        self.type = type

    def to_native(self, value):
        return self.type


class WallPostReactionSerializer(ReactionSerializer):
    wallpost_id = ToModelIdField(to_model=WallPost)

    class Meta(ReactionSerializer.Meta):
        fields = ReactionSerializer.Meta.fields + ('wallpost_id',)


class WallPostSerializerBase(serializers.ModelSerializer):
    """
        Base class serializer for wallposts.
        This is not used directly. Please subclass it.
    """
    id = serializers.Field(source='wallpost_ptr_id')
    author = AuthorSerializer()
    timesince = TimeSinceField(source='created')
    reactions = ManyRelatedSerializer(WallPostReactionSerializer)

    class Meta:
        fields = ('id', 'url', 'type', 'author', 'created', 'timesince', 'reactions')


class MediaWallPostSerializer(WallPostSerializerBase):
    video_html = OEmbedField(source='video_url', maxwidth='560', maxheight='315')
    type = WallPostTypeField(type='media')

    class Meta:
        model = MediaWallPost
        fields = WallPostSerializerBase.Meta.fields + ('title', 'text', 'video_html', 'video_url')


class TextWallPostSerializer(WallPostSerializerBase):
    type = WallPostTypeField(type='text')

    class Meta:
        model = TextWallPost
        fields = WallPostSerializerBase.Meta.fields + ('text',)


class WallPostSerializer(PolymorphicSerializer):

    class Meta:
        child_models = (
            (TextWallPost, TextWallPostSerializer),
            (MediaWallPost, MediaWallPostSerializer),
            )


# Serializers specific to the ProjectWallPosts:

class ProjectTextWallPostSerializer(TextWallPostSerializer):
    """ TextWallPostSerializer with project specific customizations. """

    project_id = ToModelIdField(to_model=Project)
    url = serializers.HyperlinkedIdentityField(view_name='project-textwallpost-detail')

    class Meta(TextWallPostSerializer.Meta):
        # Add the project_id field.
        fields = TextWallPostSerializer.Meta.fields + ('project_id',)

    def save(self):
        # Save the project content type on save.
        project_type = ContentType.objects.get_for_model(Project)
        self.object.content_type_id = project_type.id
        super(ProjectTextWallPostSerializer, self).save()


class ProjectMediaWallPostSerializer(MediaWallPostSerializer):
    """ MediaWallPostSerializer with project specific customizations. """

    project_id = ToModelIdField(to_model=Project)
    url = serializers.HyperlinkedIdentityField(view_name='project-mediawallpost-detail')

    class Meta(MediaWallPostSerializer.Meta):
        # Add the project_id field.
        fields = MediaWallPostSerializer.Meta.fields + ('project_id',)

    def save(self):
        # Save the project content type on save.
        project_type = ContentType.objects.get_for_model(Project)
        self.object.content_type_id = project_type.id
        super(ProjectMediaWallPostSerializer, self).save()


class ProjectWallPostSerializer(PolymorphicSerializer):
    """ Polymorphic WallPostSerializer with project specific customizations. """

    class Meta:
        child_models = (
            (TextWallPost, ProjectTextWallPostSerializer),
            (MediaWallPost, ProjectMediaWallPostSerializer),
            )
