import logging
import json
import os
import atexit

from lxfx.utils import createLogger, handleExit
from lxfx.data import TimeSeriesDatasetManager
from lxfx.trainers import ModelTrainer
from lxfx.predPlotter import PredPlotter
from lxfx.models import FxFCModel, FxFCAutoEncoder

class XFX:
    def __init__(self, config_file_path = None, _config_dict = None, 
                 model_type = None, manual_seed = None):
        self.console_logger = createLogger(is_consoleLogger=True)
        self.config_file_path = config_file_path
        self._config_dict = _config_dict
        self.model_type = model_type
        self.dataset_manager = None 

        self.dataset_config = None
        self.trainer_config = None
        self.FxFCModel_config = None
        self.FxFCAutoEncoder_config = None

        self.trainer = None 
        self.dataset_manager = None
        self.model = None

        self.get_config()

        self.dataset_manager = self.get_dataset_manager()
        if manual_seed:
            self.dataset_manager.set_seed(manual_seed)
        self.model = self.get_model()
        self.trainer = self.get_trainer()

        atexit.register(self.save_config)

    def get_config(self):
        if self.config_file_path:
            try:
                self.config = json.load(open(self.config_file_path))
            except Exception as e:
                self.console_logger.error(f"Error loading config file: {e}")
        else:
            self.config = self._config_dict

        # get datasetManager and trainer 
        try:
            self.dataset_config = self.config["TimeSeriesDatasetManager"]
        except Exception as e:
            self.console_logger.error(f"Error loading dataset config: {e}")
        try:
            self.trainer_config = self.config["ModelTrainer"]
        except Exception as e:
            self.console_logger.error(f"Error loading trainer config: {e}")

        # FxFCModel config
        try:
            self.FxFCModel_config = self.config["FxFCModel"]
        except Exception as e:
            if self.model_type == "FxFCModel":
                self.console_logger.error(f"Error loading FxFCModel config: {e}")
                self.console_logger.error("Please check the config file for the FxFCModel section.")
            else:
                self.FxFCModel_config = None

        try:
            self.FxFCAutoEncoder_config = self.config["FxFCAutoEncoder"]
        except Exception as e:
            if self.model_type == "FxFCAutoEncoder":
                self.console_logger.error(f"Error loading FxFCAutoEncoder config: {e}")
                self.console_logger.error("Please check the config file for the FxFCAutoEncoder section.")
            else:
                self.FxFCAutoEncoder_config = None

    def get_dataset_manager(self):
        if self.dataset_manager is None:
            self.dataset_manager = TimeSeriesDatasetManager(
                data=None,
                file_path=self.dataset_config.get("file_path"),
                targets=None,
                future_pred_length=self.dataset_config.get("future_pred_length", 1),
                targetIndices=self.dataset_config.get("targetIndices", None),
                target_names=self.dataset_config.get("target_names"),
                drop_names=self.dataset_config.get("drop_names", None),
                date_col=self.dataset_config.get("date_col"),
                sequence_length=self.dataset_config.get("sequence_length", 5),
                stride=self.dataset_config.get("stride", 1),
                scaler_feature_range=self.dataset_config.get("scaler_feature_range", [0, 1]),
                transform=self.dataset_config.get("transform", None),
                use_default_scaler=self.dataset_config.get("use_default_scaler", True),
                split_criterion=self.dataset_config.get("split_criterion", [0.7, 0.15, 0.15]),
                batchsize=self.dataset_config.get("batchsize", 8),
                is_fx=self.dataset_config.get("is_fx", False),
                transform_targets=self.dataset_config.get("transform_targets", True),
                index_col=self.dataset_config.get("index_col", None),
                manual_seed=self.dataset_config.get("manual_seed", None),
                is_autoregressive=self.dataset_config.get("is_autoregressive", False),
                test_sequence_length=self.dataset_config.get("test_sequence_length", None), 
                test_stride=self.dataset_config.get("test_stride", None)
            )
        return self.dataset_manager

    def get_trainer(self):
        if self.trainer is None:
            self.trainer = ModelTrainer(
                model=self.model,
                dataset_manager=self.dataset_manager,
                loss_fn=self.trainer_config.get("loss_fn", "mse"),
                optimizer=self.trainer_config.get("optimizer", "adam"),
                epochs=self.trainer_config.get("epochs", 3),
                accuracy_fn=self.trainer_config.get("accuracy_fn", None),
                lr=self.trainer_config.get("lr", 0.001),
                project_path=self.trainer_config.get("project_path"),
                is_logging=self.trainer_config.get("is_logging", True),
                resume=self.trainer_config.get("resume", False),
            )
        return self.trainer

    def get_model(self): 
        if self.model is None:
            if self.model_type == "FxFCModel":
                self.model = FxFCModel(
                    num_features=self.FxFCModel_config.get("num_features"),
                    block_type=self.FxFCModel_config.get("block_type", "lstm"),
                    out_features=self.FxFCModel_config.get("out_features", 1),
                    units=self.FxFCModel_config.get("units"),
                    num_layers=self.FxFCModel_config.get("num_layers", 1),
                    is_encoder=self.FxFCModel_config.get("is_encoder", False),
                    encoder_latent_dim=self.FxFCModel_config.get("encoder_latent_dim"),
                    is_decoder=self.FxFCModel_config.get("is_decoder", False),
                    out_units=self.FxFCModel_config.get("out_units"),
                    activation=self.FxFCModel_config.get("activation", "tanh"),
                    bidirectional=self.FxFCModel_config.get("bidirectional", False),
                    pass_states=self.FxFCModel_config.get("pass_states", False),
                    use_batch_norm=self.FxFCModel_config.get("use_batch_norm", False),
                    pass_block_hidden_state=self.FxFCModel_config.get("pass_block_hidden_state", False),
                    decoder_out_features=self.FxFCModel_config.get("decoder_out_features")
                )
            elif self.model_type == "FxFCAutoEncoder":
                self.model = FxFCAutoEncoder(
                    num_features=self.FxFCAutoEncoder_config.get("num_features"),
                    target_features=self.FxFCAutoEncoder_config.get("target_features", 1),
                    future_pred_length=self.FxFCAutoEncoder_config.get("future_pred_length", 1),
                    block_types=self.FxFCAutoEncoder_config.get("block_types", ["lstm", "lstm"]),
                    units=self.FxFCAutoEncoder_config.get("units"),
                    out_units=self.FxFCAutoEncoder_config.get("out_units"),
                    num_layers=self.FxFCAutoEncoder_config.get("num_layers", [1, 1]),
                    activations=self.FxFCAutoEncoder_config.get("activations", ["tanh", "tanh"]),
                    latent_dim=self.FxFCAutoEncoder_config.get("latent_dim", 32),
                    dropout=self.FxFCAutoEncoder_config.get("dropout", [0.2, 0.2]),
                    bidirectional=self.FxFCAutoEncoder_config.get("bidirectional", [False, False]),
                    use_batch_norm=self.FxFCAutoEncoder_config.get("use_batch_norm", [False, False]),
                    pass_block_hidden_state=self.FxFCAutoEncoder_config.get("pass_block_hidden_state", [False, False])
                )
            else:
                self.console_logger.error(f"Invalid model type: {self.model_type}")
                handleExit()
        return self.model
        
    def train(self, epochs = None):
        self.trainer.trainModel(epochs=epochs)
        self.save_config()

    def predict(self):
        self.trainer.predict()

    def save_config(self):
        config_dict = {}
        config_dict["model_type"] = self.model_type
        config_dict["model"] = self.model.config_dict()
        config_dict["dataset"] = self.dataset_manager.config_dict()
        config_dict["trainer"] = self.trainer.config_dict()

        project_dir = self.trainer.project_path
        config_file_path = os.path.join(project_dir, "config.json")
        with open(config_file_path, "w") as f:
            json.dump(config_dict, f, indent=4)
        print(f"Config file saved to: {config_file_path}")

    def plotPredictions(self, preds, figsize = (6,6), test_only=False,
                        _len = 100, test_plots = None):
        """
        Plots a graph(s) showing the predictions against the actual values.
        """
        predPlotter = PredPlotter(preds, self.dataset_manager, test_only=test_only,
                                  length = _len, figsize = figsize, test_plots = test_plots)
        predPlotter.plotPredictions()