from organisation.models import Organisation
from rest_framework import serializers



class OrgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = '__all__'
