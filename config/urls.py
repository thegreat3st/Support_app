from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpRequest
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
import json
import requests


def filter_by_keys(source: dict, keys: list[str]) -> dict:
    filtered_data = {}
    for key, value in source.items():
        if key in keys:
            filtered_data[key] = value
    return filtered_data


@dataclass
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> "Pokemon":
        filtered_data = filter_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),
        )
        return cls(**filtered_data)


TTL = timedelta(minutes=5)
POKEMONS: dict[str, Pokemon] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon.from_raw_data(raw_data)


def pokemon_del(name):
    del POKEMONS[name]


def _get_pokemon(name) -> Pokemon:
    """
    Take pokemon from the cache or
    fetch it from the API and then save it to the cache.
    """

    if name in POKEMONS:
        pokemon, created_at = POKEMONS[name]

        if datetime.now() > created_at + TTL:
            pokemon_del(name)
            return _get_pokemon(name)
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = [pokemon, datetime.now()]

    return pokemon


@csrf_exempt
def get_pokemon(request, name: str):
    if request.method == "GET":
        pokemon: Pokemon = _get_pokemon(name)
    elif request.method == "DELETE":
        pokemon_del(name)
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(asdict(pokemon)),
    )


@csrf_exempt
def get_pokemon_for_mobile(request, name: str):
    if request.method == "GET":
        pokemon: Pokemon = _get_pokemon(name)
        result = filter_by_keys(
            asdict(pokemon),
            ["id", "name", "base_experience"],
        )
    elif request.method == "DELETE":
        pokemon_del(name)
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


@csrf_exempt
def get_from_cache(request) -> dict:
    if request.method == "GET":
        pokemon_cache = {}
        for name, pokes_info in POKEMONS.items():
            pokemon_cache[name] = asdict(pokes_info[0])

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(pokemon_cache),
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemon/<str:name>/", get_pokemon),
    path("api/pokemon/mobile/<str:name>/", get_pokemon_for_mobile),
    path("api/pokemon/", get_from_cache),
]
