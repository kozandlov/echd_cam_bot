from configparser import ConfigParser
from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[str]

    @staticmethod
    def from_env(env: Env):
        token = env.str("BOT_TOKEN")
        admin_ids = env.list("ADMINS")
        return TgBot(
            token=token,
            admin_ids=admin_ids
        )


@dataclass
class Camera:
    address: str
    name: str
    ip_address: str
    login: str
    password: str

    @staticmethod
    def from_conf() -> list:
        config_parser = ConfigParser()
        config_parser.read("config.ini")
        return [
            Camera(
                name=section,
                address=config_parser.get(section, "address"),
                ip_address=config_parser.get(section, 'ip'),
                login=config_parser.get(section, "login"),
                password=config_parser.get(section, "password")
            )
            for section in config_parser.sections()
        ]

    def save_to_conf(self):
        config_parser = ConfigParser()
        config_parser.read("config.ini")
        if f"{self.name}" not in config_parser.sections():
            config_parser.add_section(f"{self.name}")
        config_parser.set(section=f"{self.name}", option='address', value=self.address)
        config_parser.set(section=f"{self.name}", option='ip', value=self.ip_address)
        config_parser.set(section=f"{self.name}", option='login', value=self.login)
        config_parser.set(section=f"{self.name}", option='password', value=self.password)
        with open("config.ini", 'w') as configfile:
            config_parser.write(configfile)

    def delete_from_conf(self):
        config_parser = ConfigParser()
        config_parser.read("config.ini")
        config_parser.remove_section(f"{self.name}")
        with open("config.ini", 'w') as configfile:
            config_parser.write(configfile)



@dataclass
class Building:
    address: str
    cameras: list[Camera]

    @staticmethod
    def from_conf() -> list:
        result = []
        cameras = Camera.from_conf()
        for camera in cameras:
            if camera.address not in [building.address for building in result]:
                result.append(
                    Building(
                        address=camera.address,
                        cameras=[camera]
                    )
                )
            else:
                for building in result:
                    if camera.address == building.address:
                        building.cameras.append(camera)
        return result


@dataclass
class Config:
    tg_bot: TgBot
    buildings: list[Building] = None


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        buildings=Building.from_conf()
    )
