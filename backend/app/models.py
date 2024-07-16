from flask_sqlalchemy import SQLAlchemy
from app.auth.utils import unique_id
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ENUM
from sqlalchemy import Enum
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    email = db.Column(db.String(325), unique=True, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(325), nullable=False)
    isEmailVerified = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id', name='fk_subscription_user'), nullable=False)
    searches_remaining = db.Column(db.Integer, default=10)

    subscription = db.relationship('UserSubscription', back_populates='users')
    payments = db.relationship('Payment', back_populates='user')
    recipes = db.relationship('Recipe', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')
    favorites = db.relationship('Favorite', back_populates='user')
    meal_plans = db.relationship('MealPlan', back_populates='user')
    shopping_lists = db.relationship('ShoppingList', back_populates='user')


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    email = db.Column(db.String(325), unique=True, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(325), nullable=False)
    isEmailVerified = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plan'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(ENUM('Monthly', 'Quarterly', 'Annually', name='billing_cycle'), nullable=False)
    features = db.Column(JSON, nullable=True)

    user_subscriptions = db.relationship('UserSubscription', back_populates='plan')
    plan_features = db.relationship('PlanFeature', back_populates='plan')


class UserSubscription(db.Model):
    __tablename__ = 'user_subscription'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_subscription_user'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.id', name='fk_user_subscription_plan'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(ENUM('Active', 'Cancelled', 'Expired', name='subscription_status'), nullable=False)
    auto_renew = db.Column(db.Boolean, default=True)

    user = db.relationship('User', back_populates='subscriptions')
    plan = db.relationship('SubscriptionPlan', back_populates='user_subscriptions')
    payments = db.relationship('PaymentTransaction', back_populates='subscription')


class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transaction'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_payment_transaction_user'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('user_subscription.id', name='fk_payment_transaction_subscription'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='payments')
    subscription = db.relationship('UserSubscription', back_populates='payments')


class SubscriptionFeature(db.Model):
    __tablename__ = 'subscription_feature'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    plan_features = db.relationship('PlanFeature', back_populates='feature')
    user_usage = db.relationship('UserUsage', back_populates='feature')


class PlanFeature(db.Model):
    __tablename__ = 'plan_feature'
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.id', name='fk_plan_feature_plan'), primary_key=True, nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey('subscription_feature.id', name='fk_plan_feature_feature'), primary_key=True, nullable=False)
    limit = db.Column(db.Integer, nullable=True)

    plan = db.relationship('SubscriptionPlan', back_populates='plan_features')
    feature = db.relationship('SubscriptionFeature', back_populates='plan_features')


class UserUsage(db.Model):
    __tablename__ = 'user_usage'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_usage_user'), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey('subscription_feature.id', name='fk_user_usage_feature'), nullable=False)
    usage_count = db.Column(db.Integer, default=0)
    last_used_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='usage')
    feature = db.relationship('SubscriptionFeature', back_populates='user_usage')


class PromotionalCode(db.Model):
    __tablename__ = 'promotional_code'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(ENUM('Percentage', 'Fixed Amount', name='discount_type'), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)
    max_uses = db.Column(db.Integer, nullable=False)

    user_promo_usages = db.relationship('UserPromoUsage', back_populates='promocode')


class UserPromoUsage(db.Model):
    __tablename__ = 'user_promo_usage'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_promo_usage_user'), primary_key=True, nullable=False)
    promocode_id = db.Column(db.Integer, db.ForeignKey('promotional_code.id', name='fk_user_promo_usage_promocode'), primary_key=True, nullable=False)
    used_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship('User', back_populates='promo_usages')
    promocode = db.relationship('PromotionalCode', back_populates='user_promo_usages')


class ReferralProgram(db.Model):
    __tablename__ = 'referral_program'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    referrer_user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_referral_program_referrer'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_referral_program_referred'), nullable=False)
    status = db.Column(ENUM('Pending', 'Completed', 'Cancelled', name='referral_status'), nullable=False)
    referral_date = db.Column(db.DateTime, default=datetime.now)
    reward_claimed = db.Column(db.Boolean, default=False)

    referrer = db.relationship('User', foreign_keys=[referrer_user_id], back_populates='referrals_made')
    referred = db.relationship('User', foreign_keys=[referred_user_id], back_populates='referrals_received')


class SubscriptionTier(db.Model):
    __tablename__ = 'subscription_tier'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    name = db.Column(db.String(150), nullable=False)
    minimum_spend = db.Column(db.Float, nullable=False)
    benefits = db.Column(JSON, nullable=True)

    user_tiers = db.relationship('UserTier', back_populates='tier')
    content_access = db.relationship('ContentAccess', back_populates='tier')


class UserTier(db.Model):
    __tablename__ = 'user_tier'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_tier_user'), primary_key=True, nullable=False)
    tier_id = db.Column(db.Integer, db.ForeignKey('subscription_tier.id', name='fk_user_tier_tier'), primary_key=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='tiers')
    tier = db.relationship('SubscriptionTier', back_populates='user_tiers')


class ContentAccess(db.Model):
    __tablename__ = 'content_access'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    type = db.Column(ENUM('Recipe', 'Article', 'Video', name='content_type'), nullable=False)
    minimum_tier_id = db.Column(db.Integer, db.ForeignKey('subscription_tier.id', name='fk_content_access_tier'), nullable=False)

    tier = db.relationship('SubscriptionTier', back_populates='content_access')


class SubscriptionGifting(db.Model):
    __tablename__ = 'subscription_gifting'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    giver_user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_subscription_gifting_giver'), nullable=False)
    receiver_email = db.Column(db.String(325), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.id', name='fk_subscription_gifting_plan'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in months
    gift_date = db.Column(db.DateTime, default=datetime.now)
    redeem_status = db.Column(ENUM('Pending', 'Redeemed', 'Expired', name='redeem_status'), nullable=False)

    giver = db.relationship('User', back_populates='gifts_given')
    plan = db.relationship('SubscriptionPlan', back_populates='gifts')
    

class UserEngagementMetric(db.Model):
    __tablename__ = 'user_engagement_metric'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_engagement_metric_user'), nullable=False)
    login_frequency = db.Column(db.Integer, nullable=False)
    recipe_creation_count = db.Column(db.Integer, nullable=False)
    comment_count = db.Column(db.Integer, nullable=False)
    last_active_date = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='engagement_metrics')


class SubscriptionFeedback(db.Model):
    __tablename__ = 'subscription_feedback'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_subscription_feedback_user'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('user_subscription.id', name='fk_subscription_feedback_subscription'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    feedback_date = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='feedback')
    subscription = db.relationship('UserSubscription', back_populates='feedback')
class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_recipe_user'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    prep_time = db.Column(db.Integer, nullable=True)
    cook_time = db.Column(db.Integer, nullable=True)
    total_time = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Integer, nullable=True)
    difficulty = db.Column(Enum('Easy', 'Medium', 'Hard', name='difficulty'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_public = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='recipes')
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe')
    instructions = db.relationship('Instruction', back_populates='recipe')
    tags = db.relationship('RecipeTag', back_populates='recipe')
    nutrition = db.relationship('Nutrition', uselist=False, back_populates='recipe')
    reviews = db.relationship('Review', back_populates='recipe')
    favorites = db.relationship('Favorite', back_populates='recipe')
    meal_plan_recipes = db.relationship('MealPlanRecipe', back_populates='recipe')
    versions = db.relationship('RecipeVersion', back_populates='recipe')
    equipments = db.relationship('RecipeEquipment', back_populates='recipe')
    dietary_restrictions = db.relationship('RecipeDietaryRestriction', back_populates='recipe')


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    nutritional_info = db.Column(JSON, nullable=True)

    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient')
    shopping_list_items = db.relationship('ShoppingListItem', back_populates='ingredient')


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_recipe_ingredient_recipe'), primary_key=True, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', name='fk_recipe_ingredient_ingredient'), primary_key=True, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')


class Instruction(db.Model):
    __tablename__ = 'instruction'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_instruction_recipe'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    recipe = db.relationship('Recipe', back_populates='instructions')


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    recipe_tags = db.relationship('RecipeTag', back_populates='tag')


class RecipeTag(db.Model):
    __tablename__ = 'recipe_tag'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_recipe_tag_recipe'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', name='fk_recipe_tag_tag'), primary_key=True, nullable=False)

    recipe = db.relationship('Recipe', back_populates='tags')
    tag = db.relationship('Tag', back_populates='recipe_tags')


class Nutrition(db.Model):
    __tablename__ = 'nutrition'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_nutrition_recipe'), nullable=False)
    calories = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    fiber = db.Column(db.Float, nullable=True)
    sugar = db.Column(db.Float, nullable=True)
    sodium = db.Column(db.Float, nullable=True)

    recipe = db.relationship('Recipe', back_populates='nutrition')


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_review_recipe'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_review_user'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.now)

    recipe = db.relationship('Recipe', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')


class Favorite(db.Model):
    __tablename__ = 'favorite'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_favorite_user'), primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_favorite_recipe'), primary_key=True, nullable=False)

    user = db.relationship('User', back_populates='favorites')
    recipe = db.relationship('Recipe', back_populates='favorites')


class MealPlan(db.Model):
    __tablename__ = 'meal_plan'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_meal_plan_user'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='meal_plans')
    meal_plan_recipes = db.relationship('MealPlanRecipe', back_populates='meal_plan')


class MealPlanRecipe(db.Model):
    __tablename__ = 'meal_plan_recipe'
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id', name='fk_meal_plan_recipe_meal_plan'), primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_meal_plan_recipe_recipe'), primary_key=True, nullable=False)
    meal_type = db.Column(Enum('Breakfast', 'Lunch', 'Dinner', 'Snack', name='meal_type'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)

    meal_plan = db.relationship('MealPlan', back_populates='meal_plan_recipes')
    recipe = db.relationship('Recipe', back_populates='meal_plan_recipes')


class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_shopping_list_user'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='shopping_lists')
    shopping_list_items = db.relationship('ShoppingListItem', back_populates='shopping_list')


class ShoppingListItem(db.Model):
    __tablename__ = 'shopping_list_item'
    list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id', name='fk_shopping_list_item_list'), primary_key=True, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', name='fk_shopping_list_item_ingredient'), primary_key=True, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    is_purchased = db.Column(db.Boolean, default=False)

    shopping_list = db.relationship('ShoppingList', back_populates='shopping_list_items')
    ingredient = db.relationship('Ingredient', back_populates='shopping_list_items')


class CookingTip(db.Model):
    __tablename__ = 'cooking_tip'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)


class RecipeVersion(db.Model):
    __tablename__ = 'recipe_version'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_recipe_version_recipe'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    changes = db.Column(JSON, nullable=False)
    date_modified = db.Column(db.DateTime, default=datetime.now)

    recipe = db.relationship('Recipe', back_populates='versions')


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=True)

    recipe_equipments = db.relationship('RecipeEquipment', back_populates='equipment')


class RecipeEquipment(db.Model):
    __tablename__ = 'recipe_equipment'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_recipe_equipment_recipe'), primary_key=True, nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id', name='fk_recipe_equipment_equipment'), primary_key=True, nullable=False)

    recipe = db.relationship('Recipe', back_populates='equipments')
    equipment = db.relationship('Equipment', back_populates='recipe_equipments')


class DietaryRestriction(db.Model):
    __tablename__ = 'dietary_restriction'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    recipe_dietary_restrictions = db.relationship('RecipeDietaryRestriction', back_populates='restriction')


class RecipeDietaryRestriction(db.Model):
    __tablename__ = 'recipe_dietary_restriction'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_recipe_dietary_restriction_recipe'), primary_key=True, nullable=False)
    restriction_id = db.Column(db.Integer, db.ForeignKey('dietary_restriction.id', name='fk_recipe_dietary_restriction_restriction'), primary_key=True, nullable=False)

    recipe = db.relationship('Recipe', back_populates='dietary_restrictions')
    restriction = db.relationship('DietaryRestriction', back_populates='recipe_dietary_restrictions')
