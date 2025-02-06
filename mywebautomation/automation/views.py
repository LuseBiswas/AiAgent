from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

class CommandView(APIView):
    def post(self, request):
        user_command = request.data.get("command")
        if user_command:
            # For now, log the command and send a response back
            print(f"Received command: {user_command}")
            return Response({"message": "Command received"}, status=status.HTTP_200_OK)
        return Response({"error": "No command provided"}, status=status.HTTP_400_BAD_REQUEST)
