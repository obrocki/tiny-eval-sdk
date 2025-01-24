import csv
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import time
import random
import json
import io
from .models import Grid
from . import models
# Configure logger
logger = logging.getLogger(__name__)

def table_view(request):    
    logger.info("Table view accessed")
    if Grid.objects.count() == 0:
        for i in range(1, 11):
            Grid.objects.create(row_number=i, text_field=f"Sample text {i}")

    grid_data = Grid.objects.all()
    context = {
        'grid_data': grid_data
    }
    return render(request, 'table_view.html', context)

def async_operation(request):
    if request.method == 'POST':        
        data = json.loads(request.body)
        text = data.get('text', '')
        logger.info(f"Async operation called with text: {text}")
        delay = random.randint(1, 10)
        time.sleep(delay)
        result = text.upper()
        logger.info(f"Async operation ended with result: {result}, delay: {delay}s")
        return JsonResponse({'status': 'completed', 'delay': delay, 'result': result})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def save_all(request):
    if request.method == 'POST':
        data = json.loads(request.body).get('data', [])
        for item in data:
            grid_item, created = Grid.objects.update_or_create(
                row_number=item['row_number'],
                defaults={
                    'text_field': item['text_field'],
                    'status': item['status'],
                    'result': item['result']
                }
            )
        logger.info("Save all called")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def reset_all(request):
    if request.method == 'POST':
        Grid.objects.all().delete()
        for i in range(1, 11):
            Grid.objects.create(row_number=i, text_field=f"Sample text {i}")
        logger.info("Reset all called")
        return JsonResponse({'status': 'success'})
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

def upload_data(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv-file')
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'error': 'File is not CSV type'})

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string, delimiter=',', quotechar='"')
            Grid.objects.all().delete()
            for row in reader:
                Grid.objects.create(
                    row_number=row[0],
                    text_field=row[1],
                    status=row[2],
                    result=row[3]
                )
            logger.info("Data uploaded successfully")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error uploading data: {e}")
            return JsonResponse({'status': 'error', 'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



class gridDetailView(generic.DetailView):
    model = models.Grid
    template_name = 'grid_detail.html'
    context_object_name = 'grid'