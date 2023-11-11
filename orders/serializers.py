from rest_framework import serializers
from orders.models import LinkOrder
from links.models import LinkProvider
from links.serializers import LinkProviderSerializer
from authentication.serializers import UserSerializer
from authentication.models import User
 

class OrderSerializer(serializers.ModelSerializer):
    link_provider = LinkProviderSerializer(read_only=True)
    # link_provider = LinkProviderSerializer()
    buyer = UserSerializer(read_only=True)

    def create(self,validated_data):
        buyer = validated_data.pop("buyer",None)
        link_provider = validated_data.pop("link_provider",None)
        link_provider = LinkProvider.objects.get(id = link_provider)
        validated_data["link_provider"] = link_provider
        print(link_provider)
        if buyer:
            buyer = User.objects.get(id=buyer)
            validated_data["buyer"] = buyer
            # validated_data["link_provider"] = link_provider
        else:
            raise serializers.ValidationError({"status":False,"errors":"Something is wrong with buyer!!"})
        order= LinkOrder.objects.create(**validated_data)
        if order:
            return order
        else:
            raise serializers.ValidationError({"status":False,"errors":"Order Already Exist!"})


    def update(self,order,validated_data):
        order.proposed_title = validated_data.pop("proposed_title",order.proposed_title)
        order.proposed_content = validated_data.pop("proposed_content",order.proposed_content)
        order.backlink = validated_data.pop("backlink",order.backlink)
        order.anchor_text = validated_data.pop("anchor_text",order.anchor_text)
        order.proposed_meta_title = validated_data.pop("proposed_meta_title",order.proposed_meta_title)
        order.proposed_meta_description = validated_data.pop("proposed_meta_description",order.proposed_meta_description)
        order.save()
        return order
    class Meta:
        model = LinkOrder
        fields = "__all__"