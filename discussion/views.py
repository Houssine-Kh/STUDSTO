from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Discussion, Message
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Subquery, OuterRef
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from products.models import Product




# Create your views here.
@login_required(login_url='/home/')  # Set the custom login URL
def send_message(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        content = request.POST.get('content')
        discId = request.POST.get('discId')

        # Get the discussion based on discId
        discussion = get_object_or_404(Discussion, id=discId)

        # Determine the sender and recipient based on the current user ('userId')
        sender = get_object_or_404(User, id=userId)
        recipient = discussion.user1 if sender != discussion.user1 else discussion.user2

        # Create a new message using the actual discussion ID
        message = Message.objects.create(
            discussion=discussion,
            sender=sender,
            recipient=recipient,
            content=content
        )

        # Update the discussion's timestamp to indicate a new message
        discussion.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@login_required(login_url='/home/')  # Set the custom login URL
def import_messages(request):
    user_id = request.user.id

    # Get discussions with their last sent messages
    discussions = Discussion.objects.filter(creator_id=user_id).annotate(
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
            'discussionId':discussion.id,
            'title': discussion.title,
            'created_at': discussion.created_at,
            'last_message_content': discussion.last_message_content,
            'last_message_timestamp': discussion.last_message_timestamp,
            'last_message_sender': discussion.last_message_sender,
            'last_message_sender_image': discussion.last_message_sender_image,
        } for discussion in discussions
    ]

    # Return a JSON response
    return JsonResponse({'discussions': discussions_data})

@login_required(login_url='/home/')  # Set the custom login URL
def load_messages(request):
    return render(request, 'home/index.html')

@login_required(login_url='/home/')  # Set the custom login URL
def get_discussion(request, discussion_id):
    # Get the discussion based on discussion_id
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    # Retrieve all messages related to the discussion, ordered by timestamp
    messages = Message.objects.filter(discussion=discussion).order_by('-timestamp').values(
        'content',
        'timestamp',
        'sender__username',
        'sender__userprofile__ProfilePic',
    )
    # Determine the connected user and the second user in the discussion
    connected_user = get_object_or_404(User, id=request.user.id)
    other_user = discussion.user1 if connected_user != discussion.user1 else discussion.user2
    # Create a list of maps with message details
    messages_data = [
        {
            'content': message['content'],
            'timestamp': message['timestamp'],
            'sender': {
                'username': message['sender__username'],
                'image': message['sender__userprofile__ProfilePic'],
            },
        } for message in messages
    ]
    # Create a map with the discussion details and messages
    discussion_data = {
        'discId': discussion_id,
        'title': discussion.title,
        'created_at': discussion.created_at,
        'messages': messages_data,
        'connected': {
            'firstname':connected_user.first_name,
            'username': connected_user.username,
            'image': connected_user.userprofile.ProfilePic.url if connected_user.userprofile.ProfilePic else None,
        },
        'recipient': {
            'username': other_user.username,
            'image': other_user.userprofile.ProfilePic.url if other_user.userprofile.ProfilePic else None,
        },
    }
    return JsonResponse(discussion_data)

@login_required()
def create_conversation(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Assuming you want the product name as the conversation title
        title = product.name

        # Assuming user1 is the connected user
        user1 = request.user

        # Assuming user2 is the shared_by user in the product
        user2 = product.shared_by.user

        # Check if a discussion already exists for the same product and users
        existing_discussion = Discussion.objects.filter(
            title=title,
            user1=user1,
            user2=user2
        ).first()

        if existing_discussion:
            # Return existing discussion details
            discussion_details = {
                'id': existing_discussion.id,
                'title': existing_discussion.title,
                'created_at': existing_discussion.created_at,
                'user1': existing_discussion.user1.username,
                'user2': existing_discussion.user2.username,
            }
            return JsonResponse({'success': True, 'discussion': discussion_details})

        # Creating a new conversation
        discussion = Discussion.objects.create(title=title, user1=user1, user2=user2)

        # Return the new discussion details along with the success message
        discussion_details = {
            'id': discussion.id,
            'title': discussion.title,
            'created_at': discussion.created_at,
            'sender': discussion.user1.username,
            'recipient': discussion.user2.username,
        }

        return JsonResponse({'success': True, 'discussion': discussion_details})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})