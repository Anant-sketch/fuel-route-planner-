from urllib.parse import urlencode

from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TripRequestSerializer
from .services.geocode import GeocodeError
from .services.osrm import RoutingError
from .services.planner import InfeasibleRoute
from .services.trip import TripParams, plan_trip


class RoutePlanView(APIView):
    """GET ?start=&finish= or POST {"start": ..., "finish": ...} -> route + cheapest fuel stops."""
    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        return self._handle(request, request.query_params)

    def post(self, request):
        return self._handle(request, request.data)

    def _handle(self, request, data):
        ser = TripRequestSerializer(data=data)
        ser.is_valid(raise_exception=True)
        v = ser.validated_data
        params = TripParams(
            start=v["start"], finish=v["finish"], range_mi=v["range_miles"], mpg=v["mpg"],
            corridor_mi=v["corridor_miles"], initial_fuel_mi=v["initial_fuel_miles"],
        )
        try:
            result = plan_trip(params)
        except GeocodeError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except InfeasibleRoute as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except RoutingError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        qs = request.build_absolute_uri(reverse("route-map")) + "?" + urlencode(
            {"start": v["start"], "finish": v["finish"]})
        result["map_url"] = qs
        result["author"] = "Anant Sharma"
        return Response(result)


def map_page(request):
    """Interactive Leaflet map; fetches the JSON from the API with query string."""
    params = request.GET.copy()
    if not params.get("start") and not params.get("finish"):
        params["start"] = "Los Angeles, CA"
        params["finish"] = "New York, NY"

    return render(request, "routing/map.html", {
        "api_url": reverse("route-plan") + "?" + params.urlencode(),
        "default_start": params.get("start", "Los Angeles, CA"),
        "default_finish": params.get("finish", "New York, NY"),
        "default_range": params.get("range_miles", "500"),
        "default_mpg": params.get("mpg", "10"),
    })
