from rest_framework import serializers


class SubscribeMixin(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
                user.is_authenticated
                and obj.following.filter(user=user).exists()
        )
