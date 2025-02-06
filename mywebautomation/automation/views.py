from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from groq import Groq  # type: ignore
import subprocess
import json
from django.http import JsonResponse  # type: ignore
import os
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.conf import settings # type: ignore

# Initialize Groq API client
groq = Groq(api_key='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')

class CommandView(APIView):
    def post(self, request):
        user_command = request.data.get("command")
        if user_command:
            try:
                # Get response from Groq API
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

@csrf_exempt
def execute_puppeteer_script(request):
    try:
        print("1. Request received")
        
        # Parse the incoming request body
        data = json.loads(request.body)
        command = data.get('command')
        print(f"2. Command received: {command}")

        script_path = '/Users/riteshbiswas/AiAgent/my-web-automation-app/puppeteer_script.js'
        abs_script_path = os.path.abspath(script_path)
        
        print(f"3. Checking script at: {abs_script_path}")
        
        if not os.path.exists(abs_script_path):
            print("4. Script not found")
            return JsonResponse({
                'error': 'Puppeteer script not found',
                'path_checked': abs_script_path
            }, status=404)

        # Run the script with the command as an argument
        result = subprocess.run(
            ['node', script_path, command],  # Pass command as argument
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("The Result I got",result)
        
        print("5. Script execution output:", result.stdout)
        print("6. Script execution error:", result.stderr)

        if result.returncode != 0:
            print("7. Script execution failed")
            return JsonResponse({
                'error': 'Script execution failed',
                'details': result.stderr
            }, status=500)

        try:
            lines = result.stdout.strip().split('\n')
            top_restaurants = json.loads(lines[-1])
            # top_restaurants = json.loads(result.stdout)
            return JsonResponse({'results': top_restaurants})
        except json.JSONDecodeError as e:
            print(f"8. JSON parsing error: {str(e)}")
            return JsonResponse({
                'error': 'Failed to parse script output as JSON',
                'raw_output': result.stdout
            }, status=500)
            
    except Exception as e:
        print(f"9. Unexpected error: {str(e)}")
        return JsonResponse({
            'error': str(e),
            'type': type(e).__name__
        }, status=500)