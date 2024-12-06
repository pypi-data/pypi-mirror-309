from caqtus.extension import Experiment

from caqtus.session.sql import PostgreSQLConfig


if __name__ == "__main__":
    # experiment = Experiment(storage_config=SQLiteConfig("sqlite.db"))
    # # upgrade_database(experiment)
    # #
    experiment = Experiment(storage_config=PostgreSQLConfig.from_file("config.yaml"))
    experiment.setup_default_extensions()
    # sqlite_storage_manager = experiment.build_storage_manager(
    #     SQLiteStorageManager, config=SQLiteConfig("sqlite.db")
    # )
    # copy_path(
    #     PureSequencePath.root() / "new folder",
    #     experiment.get_storage_manager(),
    #     sqlite_storage_manager,
    # )
    experiment.launch_condetrol()
