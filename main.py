import init_django_orm  # noqa: F401

import json

from db.models import Race, Skill, Player, Guild


def main() -> None:

    with open("players.json", "r") as f:
        data = json.load(f)

    for name, data_info in data.items():

        race_name = data_info["race"]["name"]
        race_note = data_info["race"]["description"]
        if not Race.objects.filter(name=race_name).exists():
            Race.objects.get_or_create(
                name=race_name,
                description=race_note
            )

        race = Race.objects.get(name=race_name)

        if data_info["race"]["skills"]:
            skills = data_info["race"]["skills"]
            for skill in skills:
                if not Skill.objects.filter(name=skill["name"]).exists():
                    Skill.objects.get_or_create(
                        name=skill["name"],
                        bonus=skill["bonus"],
                        race_id=race.id
                    )

        guild = None

        if data_info["guild"]:
            guild_name = data_info["guild"]["name"]
            guild_note = data_info["guild"]["description"]
            if not Guild.objects.filter(name=guild_name).exists():
                Guild.objects.get_or_create(
                    name=guild_name,
                    description=guild_note
                )
            guild = Guild.objects.get(name=guild_name)

        Player.objects.get_or_create(
            nickname=name,
            email=data_info["email"],
            bio=data_info["bio"],
            race_id=race.id,
            guild_id=guild.id if data_info["guild"] else None
        )


if __name__ == "__main__":
    main()
