import operator
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Optional, TypedDict

import typer
from heroku3.models.addon import Addon
from rich.progress import track

from heroku_audit.client import heroku
from heroku_audit.format import Format, FormatOption, display_data
from heroku_audit.options import TeamOption
from heroku_audit.style import style_backup_schedules
from heroku_audit.utils import (
    SHOW_PROGRESS,
    get_addon_plan,
    get_addons,
    get_apps_for_teams,
    zip_map,
)

app = typer.Typer(name="redis", help="Report on Heroku Data for Redis.")

HEROKU_REDIS = "heroku-redis:"


class HerokuRedisDetails(TypedDict):
    version: str
    maxmemory_policy: str
    maintenance_window: Optional[str]


def get_heroku_redis_details(addon: Addon) -> dict:
    response = heroku._session.get(
        f"https://redis-api.heroku.com/redis/v0/databases/{addon.id}"
    )
    response.raise_for_status()
    data = response.json()

    # Reshape for easier parsing
    data["info"] = {i["name"]: i["values"] for i in data["info"]}

    return {
        "version": data["info"]["Version"][0],
        "maxmemory_policy": data["info"]["Maxmemory"][0],
        "maintenance_window": data["info"].get("Maintenance window", [None])[0],
    }


@app.command()
def major_version(
    target: Annotated[
        Optional[int],
        typer.Option(help="Version to look for"),
    ] = None,
    team: TeamOption = None,
    display_format: FormatOption = Format.TABLE,
) -> None:
    """
    Audit the available redis database versions
    """
    with ThreadPoolExecutor() as executor:
        apps = heroku.apps() if team is None else get_apps_for_teams(team)

        redis_addons = [
            addon
            for addon in get_addons(executor, apps)
            if addon.plan.name.startswith(HEROKU_REDIS)
        ]

        results = []
        for addon, addon_details in track(
            zip_map(executor, get_heroku_redis_details, redis_addons),
            description="Probing databases...",
            total=len(redis_addons),
            disable=not SHOW_PROGRESS,
        ):
            if target and addon_details["version"].split(".", 1)[0] != str(target):
                continue

            results.append(
                {
                    "App": addon.app.name,
                    "Addon": addon.name,
                    "Plan": get_addon_plan(addon),
                    "Version": addon_details["version"],
                }
            )

    display_data(sorted(results, key=operator.itemgetter("Version")), display_format)


@app.command()
def plan(
    plan: Annotated[
        Optional[str],
        typer.Argument(help="Plan to look for"),
    ] = None,
    team: TeamOption = None,
    display_format: FormatOption = Format.TABLE,
) -> None:
    """
    Find Redis instances with a given plan
    """
    # HACK: https://github.com/martyzz1/heroku3.py/pull/132
    Addon._strs.append("config_vars")  # type:ignore

    with ThreadPoolExecutor() as executor:
        apps = heroku.apps() if team is None else get_apps_for_teams(team)

        redis_addons = [
            addon
            for addon in get_addons(executor, apps)
            if addon.plan.name.startswith(HEROKU_REDIS)
        ]

    if plan:
        redis_addons = [
            addon for addon in redis_addons if get_addon_plan(addon) == plan
        ]

    display_data(
        sorted(
            (
                {
                    "App": addon.app.name,
                    "Addon": addon.name,
                    "Attachments": ", ".join(sorted(addon.config_vars)),
                    "Plan": get_addon_plan(addon),
                }
                for addon in redis_addons
            ),
            key=operator.itemgetter("App"),
        ),
        display_format,
    )


@app.command()
def count(
    minimum: Annotated[
        int,
        typer.Option(
            "--min",
            help="Acceptable number of instances (greater than this will be shown)",
        ),
    ] = 1,
    team: TeamOption = None,
    display_format: FormatOption = Format.TABLE,
) -> None:
    """
    Find apps with a given number of instances
    """
    # HACK: https://github.com/martyzz1/heroku3.py/pull/132
    Addon._strs.append("config_vars")  # type: ignore

    with ThreadPoolExecutor() as executor:
        apps = heroku.apps() if team is None else get_apps_for_teams(team)

        app_to_addons = defaultdict(list)

        for addon in get_addons(executor, apps):
            if not addon.plan.name.startswith(HEROKU_REDIS):
                continue

            app_to_addons[addon.app].append(addon)

    display_data(
        sorted(
            (
                {
                    "App": app.name,
                    "Instances": len(addons),
                    "Addon Names": ", ".join(sorted([a.name for a in addons])),
                }
                for app, addons in app_to_addons.items()
                if len(addons) >= minimum
            ),
            key=operator.itemgetter("Instances"),
            reverse=True,
        ),
        display_format,
    )


@app.command()
def maxmemory_policy(
    policy: Annotated[
        Optional[str],
        typer.Argument(help="Policy to look for"),
    ] = None,
    team: TeamOption = None,
    display_format: FormatOption = Format.TABLE,
) -> None:
    """
    Audit the redis `maxmemory-policy`
    """
    with ThreadPoolExecutor() as executor:
        apps = heroku.apps() if team is None else get_apps_for_teams(team)

        redis_addons = [
            addon
            for addon in get_addons(executor, apps)
            if addon.plan.name.startswith(HEROKU_REDIS)
        ]

        results = []
        for addon, addon_details in track(
            zip_map(executor, get_heroku_redis_details, redis_addons),
            description="Probing databases...",
            total=len(redis_addons),
            disable=not SHOW_PROGRESS,
        ):
            if policy and addon_details["maxmemory_policy"] != policy:
                continue

            results.append(
                {
                    "App": addon.app.name,
                    "Addon": addon.name,
                    "Plan": get_addon_plan(addon),
                    "Policy": addon_details["maxmemory_policy"],
                }
            )

    display_data(sorted(results, key=operator.itemgetter("Policy")), display_format)


@app.command()
def maintenance_window(
    missing_only: Annotated[
        Optional[bool],
        typer.Option(help="Only show instances without maintenance windows"),
    ] = False,
    team: TeamOption = None,
    display_format: FormatOption = Format.TABLE,
) -> None:
    """
    Audit the maintenance window of redis databases
    """
    with ThreadPoolExecutor() as executor:
        apps = heroku.apps() if team is None else get_apps_for_teams(team)

        redis_addons = [
            addon
            for addon in get_addons(executor, apps)
            if addon.plan.name.startswith(HEROKU_REDIS)
        ]

        results = []
        for addon, addon_details in track(
            zip_map(executor, get_heroku_redis_details, redis_addons),
            description="Probing databases...",
            total=len(redis_addons),
            disable=not SHOW_PROGRESS,
        ):
            if missing_only and addon_details["maintenance_window"]:
                continue
            results.append(
                {
                    "App": addon.app.name,
                    "Addon": addon.name,
                    "Plan": get_addon_plan(addon),
                    "Maintenance_window": style_backup_schedules(
                        addon_details["maintenance_window"]
                    ),
                }
            )

    display_data(sorted(results, key=operator.itemgetter("App")), display_format)
