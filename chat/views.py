from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Conversation, Message
from students.models import Student
from tutors.models import Tutor
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def conversation_list(request):
    # Get all conversations where the current user is a participant
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants', 'messages').distinct()

    # Get a list of all available students/tutors to start new conversations
    if request.user.role == 'student':
        available_users = Student.objects.exclude(user=request.user).select_related('user')
    elif request.user.role == 'tutor':
        available_users = Tutor.objects.exclude(user=request.user).select_related('user')
    else:
        available_users = []

    context = {
        'conversations': conversations,
        'available_users': available_users
    }
    return render(request, 'chat/conversation_list.html', context)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('messages', 'participants'),
        id=conversation_id,
        participants=request.user
    )
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Broadcast the message to the room group
            channel_layer = get_channel_layer()

            if channel_layer is None:
                print("Channel layer is not configured.")
            else:
                async_to_sync(channel_layer.group_send)(
                    f'chat_{conversation_id}',
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'sender': message.sender.username,
                    })
            
            
            return JsonResponse({'status': 'success'})

    # Mark unread messages as read
    conversation.messages.filter(
        ~Q(sender=request.user), 
        is_read=False
    ).update(is_read=True)

    context = {
        'conversation': conversation,
        'user_role': request.user.role
    }
    return render(request, 'chat/conversation_detail.html', context)

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(request.user.__class__, id=user_id)
    
    # Check if a conversation already exists between these users
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_conversation:
        return redirect('chat:conversation_detail', conversation_id=existing_conversation.id)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    return redirect('chat:conversation_detail', conversation_id=conversation.id)

@login_required
def get_messages(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    # Get messages after a certain ID if specified
    last_message_id = request.GET.get('after', 0)
    messages = conversation.messages.filter(id__gt=last_message_id)

    # Mark messages as read
    messages.filter(
        ~Q(sender=request.user),
        is_read=False
    ).update(is_read=True)

    # Render template with messages context
    context = {'conversation': conversation, 'messages': messages}
    return render(request, 'chat/message_list.html', context)

@login_required
def get_unread_count(request):
    count = Message.objects.filter(
        ~Q(sender=request.user),
        conversation__participants=request.user,
        is_read=False
    ).count()
    return count 
    
    return JsonResponse({'unread_count': count})