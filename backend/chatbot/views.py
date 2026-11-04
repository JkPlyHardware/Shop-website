from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from .serializers import ChatRequestSerializer
from .services import answer_message, BudgetExceeded
from .throttles import DailyChatThrottle

class ChatbotView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle, DailyChatThrottle]; throttle_scope = "chatbot"
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        try:
            reply, mode = answer_message(serializer.validated_data["message"], serializer.validated_data.get("history", []))
            return Response({"reply": reply, "mode": mode})
        except BudgetExceeded as exc:
            return Response({"error": str(exc)}, status=429)
        except Exception:
            return Response({"error": "The assistant is temporarily unavailable. Please contact the workshop directly."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
