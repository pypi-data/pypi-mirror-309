import torch
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from lxfx.data import TimeSeriesDatasetManager

class PredPlotter():
    """
    This handles all instances of plotting predictions in different ways.
    """
    def __init__(self, preds, dataset_manager:TimeSeriesDatasetManager,
                 autoreg_batch_plots:bool = False, test_only:bool = False, 
                 length:int = None, show_gridlines = True, interactive_cursor = True,
                 figsize = (6,6), test_plots = 1, is_production = False):
        self.is_production = is_production
        self.preds = preds
        self.dataset_manager = dataset_manager
        self.autoreg_batch_plots = autoreg_batch_plots
        self.test_plots = test_plots
        self.test_only = test_only
        self.length = length
        self.show_gridlines = show_gridlines
        self.interactive_cursor = interactive_cursor

        self.figsize = figsize
        self.figure = plt.figure(figsize = self.figsize)
        self.num_rows = self.test_plots
        self.idx_count = 0

        self.train_targets = self.dataset_manager.train_targets
        self.val_targets = self.dataset_manager.val_targets
        self.test_data = self.dataset_manager.test_targets
        self.test_eq_target_seqs = self.dataset_manager.test_eq_target_seqs
        self.test_target_seqs = self.dataset_manager.test_seq_targets
        self.transform = self.dataset_manager.transform if self.dataset_manager.transform is not None else self.dataset_manager.default_transform

        self.plot_train_targets = None
        self.plot_val_targets = None
        self.plot_test_data = None
        self.plot_pred_data = None

        self.train_y_axes = None 
        self.val_y_axes = None 
        self.test_y_axes = None 
        self.pred_y_axes = None

        self.train_x_axes = None
        self.val_x_axes = None
        self.test_x_axes = None
        self.pred_x_axes = None

        self.val_start_index = None
        self.val_end_index = None
        self.test_start_index = None
        self.test_end_index = None
        self.pred_start_index = None
        self.pred_end_index = None

    def get_prev_batch_time_steps(self, seq_index = None):
        if seq_index > 0:
            additional_seqs = self.test_eq_target_seqs[:seq_index]
        else:
            additional_seqs = []
        return additional_seqs
    
    def get_plot_data(self, preds, seq_index = None, column_idx = 0):
        self.plot_train_targets = self.dataset_manager.inverse_targets(self.train_targets)[:,column_idx]

        self.plot_val_targets = self.dataset_manager.inverse_targets(self.val_targets)[:,column_idx]

        if self.autoreg_batch_plots:
            # add previous time steps from the test data to the plot_val_targets
            additional_seqs = self.get_prev_batch_time_steps(seq_index)
            for seq in additional_seqs:
                seq = self.dataset_manager.inverse_targets(seq)[:,column_idx]
                self.plot_val_targets = torch.cat((self.plot_val_targets, seq), dim=0)

            plot_test_data = torch.cat((self.test_eq_target_seqs[seq_index], self.test_target_seqs[seq_index]), dim=0)
            self.plot_test_data = self.dataset_manager.inverse_targets(plot_test_data)[:,column_idx]

        else:
            self.plot_test_data = self.dataset_manager.inverse_targets(self.test_data)[:,column_idx]
        # preds for the column of column index column_idx are the ones provided in the preds parameter
        self.plot_pred_data = self.dataset_manager.inverse_targets(preds)

    def get_y_axes(self):
        self.train_y_axes = self.plot_train_targets 
        self.val_y_axes = self.plot_val_targets

        # length only affects the test data and predictions when not autoregressive
        if not self.autoreg_batch_plots:    
            if self.length is None:
                self.test_y_axes = self.plot_test_data
                self.pred_y_axes = self.plot_pred_data
            else:
                if self.length > len(self.plot_test_data):
                    self.length = len(self.plot_test_data)
                self.test_y_axes = self.plot_test_data[:self.length]
                self.pred_y_axes = self.plot_pred_data[self.dataset_manager.sequenceLength:self.length]
        else:
            # We want to see the whole autoregressive prediction vs the test curve
            self.test_y_axes = self.plot_test_data
            self.pred_y_axes = self.plot_pred_data

    def get_plot_indices(self, seq_idx = 0):
        self.val_start_index = len(self.train_y_axes)
        self.val_end_index = len(self.train_y_axes)+len(self.val_y_axes)
        if self.autoreg_batch_plots:
            self.test_start_index = self.val_end_index
            if self.is_production:
                self.test_end_index = self.val_end_index+len(self.test_eq_target_seqs[seq_idx])
                self.pred_start_index = self.test_end_index
                self.pred_end_index = self.pred_start_index+self.preds[seq_idx].shape[1] # We add on the length of the future predicted points
            else:
                self.test_end_index = self.test_start_index+len(self.test_eq_target_seqs[seq_idx])+self.preds[seq_idx].shape[1]
                self.pred_start_index = self.val_end_index+len(self.test_eq_target_seqs[seq_idx])
                self.pred_end_index = self.test_end_index
            # Here the test_data is each test_seq in the test_seqs
        else:
            self.test_start_index = self.val_end_index
            self.test_end_index = self.val_end_index+len(self.test_y_axes)
            self.pred_start_index = self.test_start_index + self.dataset_manager.sequenceLength

    def get_x_axes(self):
        self.train_x_axes = range(len(self.train_y_axes))
        self.val_x_axes = range(self.val_start_index, self.val_end_index)
        if not self.test_only:
            self.test_x_axes = range(self.val_end_index, self.test_end_index)
            self.pred_x_axes = range(self.pred_start_index, self.test_end_index)
        else:
            self.test_x_axes = range(self.test_start_index, self.test_end_index)
            self.pred_x_axes = range(self.pred_start_index, self.test_end_index)

    def plotColumnPreds(self, preds:torch.Tensor, seq_index:int = None,
                        column_idx:int = 0, seq_idx = 0):
        self.get_plot_data(preds, seq_index, column_idx)
        self.get_y_axes()
        self.get_plot_indices(seq_idx)
        self.get_x_axes()

        if isinstance(self.preds, torch.Tensor):
            num_columns = self.preds.shape[-1]
        else:
            num_columns = self.preds[seq_idx].shape[-1]
        self.idx_count += 1
        # Plotting
        # fig = plt.figure(figsize = figsize)
        axs = self.figure.add_subplot(self.num_rows, num_columns, self.idx_count)
        # axs.set_title(f"Predictions for column {self.dataset_manager.df.columns[column_idx]}")
        
        if self.autoreg_batch_plots:
            test_x_axes = self.test_x_axes[:(len(self.test_x_axes)-len(self.pred_x_axes))]
            test_labels_x_axes = self.test_x_axes[-(len(self.pred_x_axes)):]

            test_y_axes = self.test_y_axes[:(len(self.test_x_axes)-len(self.pred_x_axes))]
            test_labels_y_axes = self.test_y_axes[-(len(self.pred_x_axes)):]
        else:
            test_x_axes = self.test_x_axes
            test_y_axes = self.test_y_axes
            test_labels_x_axes = None 
            test_labels_y_axes = None

        if not self.test_only:
            axs.plot(self.train_x_axes, self.train_y_axes, c = "black", label = "train")
            axs.plot(self.val_x_axes, self.val_y_axes, c = "green", label = "val")
        axs.plot(test_x_axes, test_y_axes, c = "yellow", label = "test")
        if self.autoreg_batch_plots:
            axs.plot(test_labels_x_axes, test_labels_y_axes, c = "green", label = "true_preds")
        axs.plot(self.pred_x_axes, self.pred_y_axes, c = "red", label = "preds")
        axs.set_title(f"{self.dataset_manager.target_column_names[column_idx]}")
        axs.legend()

        if self.interactive_cursor:
            cursor = Cursor(axs, useblit=True, color='red', linewidth=1)
        if self.show_gridlines:
            axs.grid(True)

    def ColumnsPlot(self, future_preds):
        main_fig = plt.figure(figsize=self.figsize)
        figs = []
        for t in range(future_preds.shape[-1]):
            feature_future_preds = future_preds[:,t]
            figs.append(self.plotColumnPreds(feature_future_preds))

        # for index, fig in enumerate(figs):
        #     main_fig.add_subfigure(fig) # More to be done here


    def plotAutoRegPreds(self):
        if isinstance(self.preds, list): # We have an autogressive prediction model

            # handle each autoregressive prediction
            for seq_idx, future_preds in enumerate(self.preds):
                if seq_idx >= self.test_plots:
                    break
                # Note: batch dim is at index 0
                future_preds = future_preds.squeeze(0) # remove the batch dimension

                # handle multiple columns
                if future_preds.shape[-1] > 1:
                    for t in range(future_preds.shape[-1]):
                        feature_future_preds = future_preds[:,t].unsqueeze(1)

                        self.plotColumnPreds(feature_future_preds, seq_index = seq_idx,
                                             column_idx = t, seq_idx = seq_idx)
                else:
                    self.plotColumnPreds(future_preds, seq_index=seq_idx)
            plt.show()

    def plotTimeStepPreds(self):
        future_preds = self.preds
        # handle multiple columns
        if future_preds.shape[-1] > 1:
            future_preds = future_preds.squeeze(1)
            for t in range(future_preds.shape[-1]):
                feature_future_preds = future_preds[:,t].unsqueeze(1)
                self.plotColumnPreds(feature_future_preds, column_idx=t)
        else:
            self.plotColumnPreds(future_preds)
        plt.show()

    def plotPredictions(self):
        if isinstance(self.preds, list):
            self.autoreg_batch_plots = True
            self.plotAutoRegPreds()
        else:
            self.autoreg_batch_plots = False
            self.plotTimeStepPreds()