from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from groq import Groq # type: ignore
import json
from django.http import JsonResponse # type: ignore
import subprocess
import os

groq = Groq(api_key='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')

class CommandView(APIView):
    def post(self, request):
        
        task = request.data.get("command")

        if task:
            try:
                # 1. Get subtasks from Groq
                subtasks = self.decompose_task(task)
                
                # 2. Execute each subtask and collect results
                final_results = {}
                for subtask in subtasks:
                    result = self.execute_puppeteer_task(subtask)
                    final_results.update(result)
                
                return Response({"results": final_results}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "No task provided"}, status=status.HTTP_400_BAD_REQUEST)

    def decompose_task(self, task):
        """Break down complex task into subtasks using Groq"""
        system_prompt = """
        You are a task decomposition expert. Break down complex web automation tasks into sequential subtasks.
        Each subtask should be a specific action that can be automated with Puppeteer.
        Return ONLY a JSON array where each object has:
        - action: the specific action to perform
        - url: the starting URL if needed
        - selectors: any CSS selectors needed
        - data_to_extract: what data to collect
        DO NOT include any explanation text or markdown formatting.
        DO NOT wrap the JSON in code blocks.
        ONLY return the JSON array.
        """
        
        try:
            # print("Decomposition task:-",)
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
            # If response contains markdown code blocks, extract the JSON
            if "```json" in content:
                # Extract content between ```json and ```
                content = content.split("```json")[1].split("```")[0].strip()
            
            # Parse the JSON content
            subtasks = json.loads(content)
            # Debug logging
            print("Parsed subtasks:", json.dumps(subtasks, indent=2))
            return subtasks
            
            
        except Exception as e:
            print("Error parsing subtasks:", str(e))
            raise Exception(f"Task decomposition failed: {str(e)}")

    def execute_puppeteer_task(self, subtask):
        """Execute a single subtask using Puppeteer"""
        try:
            script_path = '/Users/riteshbiswas/AiAgent/my-web-automation-app/puppeteer_script.js'
            
            # Convert subtask to JSON string to pass to Node script
            subtask_json = json.dumps(subtask)
            print("Subtask JSON:", subtask_json) 
            
            result = subprocess.run(
                ['node', script_path, subtask_json],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"Puppeteer execution failed: {result.stderr}")
                
            return json.loads(result.stdout)
            
        except Exception as e:
            raise Exception(f"Subtask execution failed: {str(e)}")