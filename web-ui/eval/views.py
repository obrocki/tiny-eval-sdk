import csv
import os
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import time
import random
import json
import io
from .models import PromptParam
from . import models

from prompt_eval_sdk.evaluation import Evaluation, EvaluationResult
from prompt_eval_sdk.code_evaluator import CodeQualityEvaluator

# Configure logger
logger = logging.getLogger(__name__)

model_config = {
    "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
    "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
}

evaluation = Evaluation(model_config)
code_evaluator = CodeQualityEvaluator(model_config=model_config)

def index(request):    
    logger.info("Table view accessed")

    grid_data = PromptParam.objects.all()
    if grid_data == 0:
        PromptParam.objects.create(row_number=0, eval_query="What is the capital of Japan?", eval_response="The capital of Japan is Tokyo.", ground_truth="The capital of Japan is Tokyo")
        PromptParam.objects.create(row_number=1, eval_query="What is the capital of France?", eval_response="The capital of France is Paris.", ground_truth="The capital of France is Paris")
        PromptParam.objects.create(row_number=2, eval_query="What is the capital of Canada?", eval_response="The capital of Canada is Ottawa.", ground_truth="The capital of Canada is Ottawa")
        grid_data = PromptParam.objects.all()
    
    context = {
        'grid_data': grid_data,
    }
    return render(request, 'eval.html', context)

def async_operation(request):
    if request.method == 'POST':        
        
        try:
            start_time = time.time()
            data = json.loads(request.body)
            eval_query = data.get('eval_query', '')
            eval_response = data.get('eval_response', '')
            ground_truth = data.get('ground_truth', '')
            logger.info(f"Async operation called with eval_query: {eval_query}, eval_response: {eval_response}, ground_truth: {ground_truth}")
            
            result: EvaluationResult = evaluation.evaluate_combined(eval_query, eval_response, ground_truth)
            
            logger.info(f"Combined result to dict: {result.to_dict()}")
        except Exception as e:
            logger.exception(f"Error during async operation: {e}")
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_formatted = f"{elapsed_time:.2f} seconds"
            logger.info(f"Async operation took {elapsed_time_formatted}")
            return JsonResponse({'status': 'completed', 'duration': elapsed_time_formatted, 'result': result.to_dict()})        
        
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def analyse_code(request):
    if request.method == 'POST':                
        try:
            start_time = time.time()
            data = json.loads(request.body)
            files = data.get('files', [])

            results = []
            for file in files:
                source_code = file.get('content', '')
                file_name = file.get('name', '')

                logger.info(f"Async operation called for file: {file_name}")

                result = code_evaluator(response=source_code)
                results.append({
                    'name': file_name,
                    'result': result
                })

                logger.info(f"Result for {file_name}: {result}")

            duration = time.time() - start_time
            return JsonResponse({
                'status': 'completed',
                'duration': f"{duration:.2f} seconds",
                'result': results
            })
        except Exception as e:
            logger.exception(f"Error during async operation: {e}")
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def save_all(request):
    if request.method == 'POST':
        data = json.loads(request.body).get('data', [])
        for item in data:
            prompt_param, created = PromptParam.objects.update_or_create(
                row_number=item['row_number'],
                defaults={
                    'eval_query': item['eval_query'],
                    'eval_response': item['eval_response'],
                    'ground_truth': item['ground_truth'],
                    'status': item['status'],
                    'result': item['result']
                }
            )
        logger.info("Save all called")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def reset_all(request):
    if request.method == 'POST':
        PromptParam.objects.all().delete()
        logger.info("Reset all called")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def upload_data(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv-file')
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'error': 'File is not CSV type'})

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string, delimiter=',', quotechar='"')
            PromptParam.objects.all().delete()
            for row in reader:
                PromptParam.objects.create(
                    row_number=row[0],
                    eval_query=row[1],
                    eval_response=row[2],
                    ground_truth=row[3]
                )
            logger.info("Data uploaded successfully")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error uploading data: {e}")
            return JsonResponse({'status': 'error', 'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def log_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        level = data.get('level', 'info')
        if level == 'info':
            logger.info(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        elif level == 'debug':
            logger.debug(message)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
