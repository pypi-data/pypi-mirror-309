from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from stripe.error import StripeError

from drf_stripe.models import SubscriptionItem, Product, Price, Subscription
from drf_stripe.stripe_api.checkout import stripe_api_create_checkout_session
from drf_stripe.stripe_api.customers import get_or_create_stripe_user


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "subscription_id", "period_start", "period_end", "status", "cancel_at", "cancel_at_period_end",
            "trial_start", "trial_end"
        )


class SubscriptionItemSerializer(serializers.ModelSerializer):
    """Serializes SubscriptionItem model with attributes pulled from related Subscription instance"""
    product_id = serializers.CharField(source="price.product.product_id")
    product_name = serializers.CharField(source="price.product.name")
    product_description = serializers.CharField(source="price.product.description")
    price_id = serializers.CharField(source="price.price_id")
    price_nickname = serializers.CharField(source="price.nickname")
    price = serializers.CharField(source="price.price")
    freq = serializers.CharField(source="price.freq")
    services = serializers.SerializerMethodField(method_name='get_feature_ids')
    subscription_status = serializers.CharField(source='subscription.status')
    period_start = serializers.DateTimeField(source='subscription.period_start')
    period_end = serializers.DateTimeField(source='subscription.period_end')
    trial_start = serializers.DateTimeField(source='subscription.trial_start')
    trial_end = serializers.DateTimeField(source='subscription.trial_end')
    ended_at = serializers.DateTimeField(source='subscription.ended_at')
    cancel_at = serializers.DateTimeField(source='subscription.cancel_at')
    cancel_at_period_end = serializers.BooleanField(source='subscription.cancel_at_period_end')

    def get_feature_ids(self, obj):
        return [{"feature_id": link.feature.feature_id, "feature_desc": link.feature.description} for link in
                obj.price.product.linked_features.all().prefetch_related('feature')]

    def get_subscription_expires_at(self, obj):
        return obj.subscription.period_end or \
               obj.subscription.cancel_at or \
               obj.subscription.trial_end or \
               obj.subscription.ended_at

    class Meta:
        model = SubscriptionItem
        fields = (
            "product_id", "product_name", "product_description", "price_id", "price_nickname", "price", "freq",
            "subscription_status", "period_start", "period_end",
            "trial_start", "trial_end", "ended_at", "cancel_at", "cancel_at_period_end", "services")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.product_id")
    name = serializers.CharField(source="product.name")
    avail = serializers.BooleanField(source="active")
    services = serializers.SerializerMethodField(method_name='get_feature_ids')

    def get_feature_ids(self, obj):
        return [{"feature_id": prod_feature.feature.feature_id, "feature_desc": prod_feature.feature.description} for
                prod_feature in
                obj.product.linked_features.all().prefetch_related("feature")]

    class Meta:
        model = Price
        fields = ("price_id", "product_id", "name", "price", "freq", "avail", "services", "currency")


class CheckoutRequestSerializer(serializers.Serializer):
    """Handles request data to create a Stripe checkout session."""
    price_id = serializers.CharField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        stripe_user = get_or_create_stripe_user(user_id=self.context['request'].user.id)
        try:
            checkout_session = stripe_api_create_checkout_session(
                customer_id=stripe_user.customer_id,
                price_id=attrs['price_id'],
                trial_end='auto' if stripe_user.subscription_items.count() == 0 else None
            )
            attrs['session_id'] = checkout_session['id']
        except StripeError as e:
            raise ValidationError(e.error)
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
