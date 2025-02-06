from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from groq import Groq # type: ignore


groq = Groq(api_key='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')
    
class CommandView(APIView):
    def post(self, request):
        user_command = request.data.get("command")
        if user_command:
            try:
                chat_response = self.get_groq_response(user_command)
                return Response({"message": chat_response}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "No command provided"}, status=status.HTTP_400_BAD_REQUEST)
    def get_groq_response(self, user_command):
        # Chat completion using the Groq API
        try:
            print(f"Received user command: {user_command}")

            response = groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_command},
                ],
                temperature=0.5,
                max_completion_tokens=1024,

            )

            print(f"Groq response: {response}")

            # Return the response content if available
            chat_content = response.choices[0].message.content if response.choices else "No response"
            return chat_content
        
        except Exception as e:
            print(f"Error in Groq response: {e}")
            return f"Error: {str(e)}"


