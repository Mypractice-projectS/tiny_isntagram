from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.models import User
from permissions import IsOwnerOrReadOnly
from .models import follow
from .serializers import UserListSerializer



class PostView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)


    def get(self, request, post_pk):
        try:
            post = Post.objects.get(pk=post_pk, user=request.user)
            self.check_object_permissions(request, post)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, post_pk):
        post = Post.objects.get(pk=post_pk, user=request.user)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def delete(self, request, post_pk):
        post = Post.objects.get(pk=post_pk, user=request.user)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PostListView(APIView):
    permission_classes = [ IsOwnerOrReadOnly,]

    def get(self, request):
        posts = Post.objects.filter(is_active=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    
class CommentView(APIView):
    permission_classes = [ IsOwnerOrReadOnly,]

    def get_post(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return False

    def get(self, request, post_pk):
        post = self.get_post(post_pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # comments = Comment.objects.filter(post=post, is_approved=True)
        comments = post.comments.filter(is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        post = self.get_post(post_pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#    Like


class LikeView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_post(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return False

    def get(self, request, post_pk):
        post = self.get_post(post_pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        likes = post.likes.filter(is_liked=True).count()
        return Response({'likes': likes})

    def post(self, request, post_pk):
        post = self.get_post(post_pk)
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def get(self, request):
        # users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
        q = request.query_params.get('q')
        if q:
            users = User.objects.filter(username__icontains=q)
        else:
            users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class RequestView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def post(self, request):
        user_id = request.data.get('user')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.get_or_create(request_from=request.user, request_to=user)

        return Response({'detail': 'Request sent'}, status=status.HTTP_201_CREATED)


class RequestListView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def get(self, request):
        friendship = Friendship.objects.filter(request_to=request.user, is_accepted=False)
        users = [fr.request_from for fr in friendship]
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class AcceptView(APIView):
    permission_classes = [IsOwnerOrReadOnly, ]

    def post(self, request):
        user_id = request.data.get('user')

        try:
            user = User.objects.get(pk=user_id)
            friendship = Friendship.objects.get(request_from=user, request_to=request.user, is_accepted=False)
        except (User.DoesNotExist, Friendship.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        friendship.is_accepted = True
        friendship.save()

        return Response({'detail': 'Connected'})


class FriendListView(APIView):
    permission_classes = [IsOwnerOrReadOnly,]

    def get(self, request):
        friendship = Friendship.objects.filter(
            Q(request_from_id=request.user) | Q(request_to=request.user),
            is_accepted=True
        )
        users = [fr.request_from for fr in friendship]
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)