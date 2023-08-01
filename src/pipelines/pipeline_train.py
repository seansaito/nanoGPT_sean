"""
Main pipeline for running GPT training
"""
import argparse
import logging

import box

from src import CONFIG_DIR
from src.modules.train.trainer import GPTTrainer
from src.utils import read_config, set_logging, timeit


@timeit
def main(config: dict, quick_test: bool):
    config = box.Box(config)
    device_type = "cuda" if "cuda" in config.device else "cpu"

    trainer = GPTTrainer(
        n_layers=config.n_layers,
        n_head=config.n_head,
        n_embed=config.n_embed,
        block_size=config.block_size,
        batch_size=config.batch_size,
        device=config.device,
        device_type=device_type,
        dataset=config.dataset,
        bias=config.bias,
        dropout=config.dropout,
        compile=config.compile,
        weight_decay=config.weight_decay,
        learning_rate=config.learning_rate,
        beta1=config.beta1,
        beta2=config.beta2,
        decay_lr=config.decay_lr,
        warmup_iters=config.warmup_iters,
        lr_decay_iters=config.lr_decay_iters,
        base_lr=config.learning_rate,
        min_lr=config.min_lr,
        max_iters=config.max_iters,
        eval_interval=config.eval_interval,
        eval_iters=config.eval_iters,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        grad_clip=config.grad_clip,
        log_interval=config.log_interval,
        quick_test=quick_test,
    )

    _ = trainer.train()


if __name__ == "__main__":
    set_logging(loglevel="info")
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(
        prog="Train the model",
        description="Trains GPT model",
    )

    parser.add_argument(
        "--config_path",
        type=str,
        help="Path to the config file",
        default=CONFIG_DIR / "train_shakespeare.yml",
    )

    parser.add_argument(
        "--quick_test",
        type=bool,
        action="store_true",
        help="Whether to run quick test",
        default=False,
    )

    args = parser.parse_args()
    config = read_config(args.config_path)
    quick_test = bool(args.quick_test)

    logger.info("Config: {}".format(config))

    main(config=config, quick_test=quick_test)
