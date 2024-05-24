from pathlib import Path
import os
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .scheduler import scheduler
import csv
from datetime import datetime
from drf_spectacular.utils import extend_schema, extend_schema_view


from .serializers import (
    CarEntrySerializer,
    IDSerializer,
    CreateRouteSerializer,
    OperationSerializer,
)
from .application_service import (
    create_route,
    location_cars,
    notify,
    cars,
)
from .operations_service import (
    create_operation,
    finish_operation,
    get_operation,
)

@extend_schema_view(
    get_cars=extend_schema(
        summary="Get a list of cars",
        responses={
            200: CarEntrySerializer,
            404: None,
        }
    ),
    create=extend_schema(
        summary="Create a route",
        request=CreateRouteSerializer,
        responses={
            201: CarEntrySerializer,
        }
    ),
    notify=extend_schema(
        summary="Change status",
        responses={
            200: CarEntrySerializer,
            404: None,
        }
    ),

)
class CarEntryViewSet(ViewSet):
    def get_cars(self, _ ):

        entries = location_cars()
        if entries is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CarEntrySerializer(entries, many=True)
            return Response(serializer.data)



    def create(self, request):
        serializer = CreateRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tt = create_route(id = serializer.validated_data['id'], coordinate_x = serializer.validated_data['coordinate_x'] , coordinate_y = serializer.validated_data['coordinate_y'])
        response_serializer = CreateRouteSerializer(tt)
        return Response(response_serializer.data,status=status.HTTP_201_CREATED)



    def notify(self,_, id):
        try:
            entry = notify(id)
            serializer = IDSerializer(entry)
            return Response(serializer.data)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)



@extend_schema_view(
    retrieve=extend_schema(
        summary="Get an operation by ID",
        responses={
            200: OperationSerializer,
            404: None,
        }
    ),
    export_data=extend_schema(
        summary="Export data for an operation",
        responses={
            202: None,
        }
    ),
)
class OperationsViewSet(ViewSet):

    def retrieve(self, request, operation_id):
        try:
            operation = get_operation(operation_id)
            serializer = OperationSerializer(operation)
            return Response(serializer.data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def export_data(self, request):
        operation_id = create_operation()

        # Запланировать задачу выгрузки данных в фоновом режиме
        scheduler.add_job(
            self._export_data_task,
            args=[operation_id],
            id=str(operation_id),
            replace_existing=True,
        )

        return Response({'operation_id': str(operation_id)}, status=status.HTTP_202_ACCEPTED)

    def _export_data_task(self, operation_id):
        try:
            # Получить все записи во всех очередях
            all_cars_entries = []

            for id, entries in cars.items():
                all_cars_entries.append(entries)

            # Создать имя файла с текущей датой и временем
            filename = f"cars_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            reports_dir = os.path.join(settings.BASE_DIR, 'applications', 'static', 'reports')
            file_path = os.path.join(reports_dir, filename)

            # Убедитесь, что директория существует
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            # Выгрузить данные в CSV-файл
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['id', 's_location', 'f_location', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for entry in all_cars_entries:
                    writer.writerow({
                        'id': str(entry.id),
                        's_location':str(entry.s_location),
                        'f_location': str(entry.f_location),
                        'created_at': entry.created_at.isoformat(),
                    })

            # Завершить операцию и сохранить результат
            finish_operation(operation_id, {'file': file_path})
        except Exception as e:
            # В случае ошибки завершить операцию с ошибкой
            finish_operation(operation_id, {'error': str(e)})

