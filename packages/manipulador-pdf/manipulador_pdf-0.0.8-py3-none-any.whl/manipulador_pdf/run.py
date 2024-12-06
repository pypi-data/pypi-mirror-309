from .update import update
from .configs.main_hub import main_hub
from .configs.configure import configure


def run():
    update()
    configure()
    main_hub()
