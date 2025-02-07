from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from groq import Groq # type: ignore
import json
from django.http import JsonResponse
import subprocess
import traceback

# Replace with your actual API key
groq = Groq(api_key='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')

class CommandView(APIView):
    def post(self, request):
        task = request.data.get("command")
        if task:
            try:
                # 1. Decompose the task into subtasks
                subtasks = self.decompose_task(task)
                # Debug: Print the parsed subtasks
                print("Parsed subtasks:", json.dumps(subtasks, indent=2))
                
                # 2. Execute each subtask and collect results
                final_results = {}
                for subtask in subtasks:
                    result = self.execute_puppeteer_task(subtask)
                    # result is now a dictionary, so update() works as expected.
                    final_results.update(result)
                
                return Response({"results": final_results}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "No task provided"}, status=status.HTTP_400_BAD_REQUEST)

    def decompose_task(self, task):
        """Break down a complex task into subtasks using Groq"""
        system_prompt = """
        You are a task decomposition expert. Break down complex web automation tasks into sequential subtasks.
        Each subtask should be a specific action that can be automated with Puppeteer.
        Use only these allowed actions:
        - navigate: to open or visit a page
        - click: to click an element
        - extract: to extract data from a page
        - loop: to loop through multiple elements
        - limit: to limit the results
        Each subtask object must have:
        - action: one of the allowed actions
        - url: the starting URL if required (only for navigate actions)
        - selectors: any CSS selectors needed to perform the action
        - data_to_extract: the data to collect (only for extract actions, otherwise leave it empty)
        DO NOT include any explanation text or markdown formatting.
        DO NOT wrap the JSON in code blocks.
        ONLY return the JSON array.
        """
        try:
            response = groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Break down this task into subtasks: {task}"}
                ],
                temperature=0.1,
                max_completion_tokens=1024,
            )
            content = response.choices[0].message.content.strip()
            # If the response is wrapped in markdown code blocks, extract the JSON inside
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            subtasks = json.loads(content)
            return subtasks
        except Exception as e:
            print("Error parsing subtasks:", str(e))
            raise Exception(f"Task decomposition failed: {str(e)}")
        
    def execute_puppeteer_task(self, subtask):
        try:
            script_path = '/Users/riteshbiswas/AiAgent/my-web-automation-app/puppeteer_script.js'
        
            # Convert the subtask (a Python dict) into a JSON string to pass to Node
            subtask_json = json.dumps(subtask)
        
            result = subprocess.run(
            ['node', script_path, subtask_json],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
            print("Raw stdout from Puppeteer script:", result.stdout)
            print("Raw stderr from Puppeteer script:", result.stderr)
            if result.returncode != 0:
                raise Exception(f"Puppeteer execution failed: {result.stderr}")
        
            # Split stdout into lines and pick the last non-empty line (which should be our JSON result)
            stdout_lines = result.stdout.strip().split('\n')
            final_line = next((line for line in reversed(stdout_lines) if line.strip()), None)
            if final_line is None:
                raise Exception("No valid JSON output from Puppeteer script.")
        
            # Parse the JSON string into a Python dictionary
            output_dict = json.loads(final_line)
            print("Parsed output dict:", output_dict)
            return output_dict
        
        except Exception as e:
            detailed_error = traceback.format_exc()
            raise Exception(f"Subtask execution failed: {str(e)}\nDetailed error:\n{detailed_error}")
    def post(self, request):
        task = request.data.get("command")
        if task:
            try:
                # 1. Decompose the task into subtasks
                subtasks = self.decompose_task(task)
                print("Parsed subtasks:", json.dumps(subtasks, indent=2))
                # 2. Execute each subtask sequentially and collect results
                result = self.execute_puppeteer_task(subtasks)
                
                return Response({"results": result}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "No task provided"}, status=status.HTTP_400_BAD_REQUEST)
   
   

    
