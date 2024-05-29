from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from accounts.models import UserProfile
from . import models
from discussion.models import Discussion, Message
from django.db.models import Subquery, OuterRef, Prefetch , Q
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required



@login_required()  # Set the custom login URL
def retrievePosts(request):
    user_id = request.user.id
    user = request.user
    try:
        user_profile = UserProfile.objects.select_related('user').get(user=request.user)
        categories = models.Category.objects.all()
        discussions = Discussion.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).annotate(
            last_message_content=Subquery(
                Message.objects.filter(discussion=OuterRef('pk'))
                            .order_by('-timestamp')
                            .values('content')[:1]
            ),
            last_message_timestamp=Subquery(
                Message.objects.filter(discussion=OuterRef('pk'))
                            .order_by('-timestamp')
                            .values('timestamp')[:1]
            ),
            last_message_sender=Subquery(
                Message.objects.filter(discussion=OuterRef('pk'))
                            .order_by('-timestamp')
                            .values('sender__username')[:1]
            ),
            last_message_sender_image=Subquery(
                Message.objects.filter(discussion=OuterRef('pk'))
                            .order_by('-timestamp')
                            .values('sender__userprofile__ProfilePic')[:1]
            ),
        ).order_by('-last_message_timestamp')

        # Convert discussions to dictionaries
        discussions_data = [
            {
                'discussionId': discussion.id,
                'title': discussion.title,
                'created_at': discussion.created_at,
                'last_message_content': discussion.last_message_content,
                'last_message_timestamp': discussion.last_message_timestamp,
                'last_message_sender': discussion.last_message_sender,
                'sender_image': discussion.last_message_sender_image,
            } for discussion in discussions
        ]

        categories_data = [
            {
                'catId' : categorie.id,
                'name' : categorie.name,

            } for categorie in categories
        ]


        # Use prefetch_related to fetch related ProductImage, Like, and Review data for all products
        products = models.Product.objects.select_related('category', 'shared_by', 'shared_by__user').prefetch_related(
                Prefetch('productimage_set', queryset=models.ProductImage.objects.all(), to_attr='images'),
                Prefetch('like_set', queryset=models.Like.objects.all(), to_attr='likes'),
                Prefetch('review_set', queryset=models.Review.objects.all(), to_attr='reviews'),
            ).order_by('-created_at')

        products_data = [
            {
            'id':product.id,
            'name': product.name,
            'description': product.description,
            'price': intcomma(product.price),
            'category': product.category.name,
            'created_at': product.created_at,
            'shared_by_username': product.shared_by.user.username,
            'shared_by_firstname': product.shared_by.firstName,
            'shared_by_lastname': product.shared_by.lastName,
            'shared_by_email': product.shared_by.user.email,
            'shared_by_ProfilePic': product.shared_by.ProfilePic,

            'images': [image.image.url for image in product.images],
            'likes': [like.user.username for like in product.likes],
            'reviews': [{'user': review.user.username, 'text': review.text} for review in product.reviews],
            } for product in products
        ]

        user_profile = UserProfile.objects.get(user=request.user)
        userp = [
            {
            'username': user_profile.user.username,
            'firstname': user_profile.firstName,
            'lastname': user_profile.lastName,
            'email': user_profile.user.email,  # Access email from the related User model
            }
        ] 



        profile_picture = user_profile.ProfilePic.url if user_profile.ProfilePic else None

        context = {'discussions':discussions_data,'products': products_data, 'profile_picture': profile_picture , 'user_profile':userp , 'categories':categories_data}
        print(context)
        return render(request, 'home/index.html', context)
    except ObjectDoesNotExist as e:
        # Handle the exception, log it, or return an empty queryset as needed
        print(f"Error fetching product feed: {e}")
        return render(request, 'home/index.html')  # You can create an error page template

@login_required()  # Set the custom login URL
def save_product(request):
    if request.method == 'POST':
        # Assuming the user is authenticated, you can customize this part as needed
        user_profile = UserProfile.objects.select_related('user').get(user=request.user)

        # Get form data
        name = request.POST.get('designation')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')

        # Create a new Product instance
        product = models.Product.objects.create(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            shared_by=user_profile
        )

        # Create a ProductImage instance
        images = request.FILES.getlist('image')
        for image in images:
            models.ProductImage.objects.create(product=product, image=image)

        # You can add more logic here, such as redirecting to a success page
        # or returning a JSON response indicating success
        return JsonResponse({'status': 'success', 'message': 'Product saved successfully'})

    # If not a POST request, you may want to handle differently (e.g., show a form)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required()
def add_like(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Perform logic to add a like
        product = models.Product.objects.get(pk=product_id)
        like, created = models.Like.objects.get_or_create(user=request.user, product=product)

        if created:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'already_liked'})
    else:
        return JsonResponse({'status': 'error'})