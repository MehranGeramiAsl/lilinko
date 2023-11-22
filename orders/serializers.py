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
        validated_data["initial_price"] = link_provider.price
        validated_data["updated_price"] = link_provider.price
        if buyer:
            buyer = User.objects.get(id=buyer)
            validated_data["buyer"] = buyer
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['buyer'] = instance.buyer.id if instance.buyer else None
        representation['link_provider'] = instance.link_provider.id if instance.link_provider else None
        return representation
    

class OrderPriceSerializer(serializers.ModelSerializer):
    link_provider = LinkProviderSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)
    def update_price(self,order,price):
            order.updated_price = price
            order.seller_status = "PC"
            order.save()
    def update(self,order,validated_data):
        if float(validated_data["updated_price"]) != float(order.updated_price):
            if order.seller_status == "PC":
                if order.buyer_status == "NS":
                    self.update_price(order=order,price=validated_data["updated_price"])
                else:
                    raise serializers.ValidationError({"status":False,"errors":"buyer change the status"})
            elif order.seller_status == "NS":
                self.update_price(order=order,price=validated_data["updated_price"])
        return order
    

    class Meta:
        model = LinkOrder
        fields = "__all__"
        extra_kwargs = {
            'proposed_title': {'read_only': True},
            'proposed_content': {'read_only': True},
            'backlink': {'read_only': True},
            'anchor_text': {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['buyer'] = instance.buyer.id if instance.buyer else None
        representation['link_provider'] = instance.link_provider.id if instance.link_provider else None
        return representation
    
class OrderSellerStatusSerializer(serializers.ModelSerializer):
    link_provider = LinkProviderSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)
    def update_seller_status(self,order,status):
            order.seller_status = status
            order.save()
    def update(self,order,validated_data):
        if order.seller_status == "NS":
            if validated_data["seller_status"] == "A" or validated_data["seller_status"] == "R":
                self.update_seller_status(order,status=validated_data["seller_status"])
            else:
                raise serializers.ValidationError({"status":False,"errors":"Unknown Status"})
        elif order.seller_status == "PC" and order.buyer_status == "A":
            if validated_data["seller_status"] == "A" or validated_data["seller_status"] == "R":
                self.update_seller_status(order,status=validated_data["seller_status"])
            else:
                raise serializers.ValidationError({"status":False,"errors":"Unknown Status"})
        elif order.seller_status == "PC" and order.buyer_status == "NS":
            raise serializers.ValidationError({"status":False,"errors":"Unable to modify status; please await customer feedback."})
        elif order.seller_status == "PC" and order.buyer_status == "R":
            raise serializers.ValidationError({"status":False,"errors":"Customer rejected price change; status cannot be altered."})

        return order
    

    class Meta:
        model = LinkOrder
        fields = "__all__"
        extra_kwargs = {
            'proposed_title': {'read_only': True},
            'proposed_content': {'read_only': True},
            'backlink': {'read_only': True},
            'anchor_text': {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['buyer'] = instance.buyer.id if instance.buyer else None
        representation['link_provider'] = instance.link_provider.id if instance.link_provider else None
        return representation