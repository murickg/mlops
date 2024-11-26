import hydra
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import TensorBoardLogger
from lightning_modules.data_module import MNISTDataModule
from lightning_modules.model import MNISTClassifier
from omegaconf import DictConfig


@hydra.main(version_base="1.3", config_path="conf", config_name="config")
def main(cfg: DictConfig):
    pl.seed_everything(42)

    # Инициализация
    data_module = MNISTDataModule(cfg.data.data_dir, cfg.data.batch_size)
    model = MNISTClassifier(int(cfg.model.input_size), int(cfg.model.num_classes), cfg.model.lr)
    logger = TensorBoardLogger(
        save_dir=cfg.logger.save_dir,
        name=cfg.logger.name
    )

    # Обучение
    trainer = Trainer(logger=logger, **cfg.trainer)
    trainer.fit(model, data_module)


if __name__ == "__main__":
    main()
