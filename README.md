# Temporal segmentation on CMU Mocap Dataset

## Introduction
This repository contains the code to use Sequence to Sequence model (Seq2Seq) for unsupervised temporal segmentation tested on CMU Mocap Dataset.

## Abstract
We present that Seq2Seq model has capability to learn temporal embedding automatically. Given skeleton-based dataset, although we train the network to do regression,
at the same time, the network itself is able to learn a embedding space that can be used to separate different type of actions. 
To demonstrate our method, we first concatenate multiple different actions together manually and use Seq2Seq to learn the representation. During testing,
we will perform motion prediction task and utilize the internal states in Recurrent Neural Network to do clustering. We only provide the total number of 
possible actions happening in the whole sequence and don't provide any label during training and testing.

## Datasets
We do expermients on two human motion datasets: H3.6M dataset and CMU Mocap Dataset.

We follow the work done by 
[Julieta Martinez](https://github.com/una-dinosauria/human-motion-prediction) and [Chen Li](https://github.com/chaneyddtt/Convolutional-Sequence-to-Sequence-Model-for-Human-Dynamics) to
use H3.6M dataset and CMU Mocap dataset which are two standard datasets for human motion prediction. Both datasets are preprocessed on exponential map format. You can download the data from their Github webpage.
H3.6M contains 15 different type of actions and for CMU Mocap we select 8 unique actions (walking, running, jumping, basketball, soccer, washwindow, basketball signal, and directing traffic).
For both datasets, each sequence only contains one action. As a result, we manually concatenate multiple actions together to demonstrate the temporal segmentation. 
To avoid biases on selecting data, we only mandatory choose the number of possible actions and then randomly select the sequences and orders of data. Each unique type of action can also be repeated. 

## Requirements
1. Tensorflow 1.13
2. Python 3

## Getting Started
For a quick demo, you can use pre-trained models and reproduce the videos shown above.

To train a new model from scratch, run
```bash
python src/main.py --dataset CMU --actions_number 8
```

## Argument
`--dataset`: a string that is either `CMU` or `H3.6M`.

`--actions_number`: unique number of actions specified for tested sequence (2 to 8 for CMU, 2 to 15 for H3.6M).

`--specific_actions`: instead of randomly choose actions, you can specify a list that contains names of actions you want to show in the testing video. For CMU dataset, you can choose
any action from `['walking', 'running', 'jumping', 'soccer', 'basketball', 'directing_traffic', 'washwindow', 'basketball_signal']
`. For H3.6M dataset, you can choose any action from `['walking', 'directions', 'discussion', 'eating', 'greeting', 'phoning', 'posing', 'purchases', 'sitting', 'sittingdown', 'smoking', 'takingphoto',
'waiting', 'walkingdog','walkingtogether']`.

## Files and functions
* Seq2Seq model (class)
* data_utils
  * readCSV
  * normalize data
  * unormalize data
  * expmap to rotation matrix
  * get mini batch
* Datasets
  * CMU Mocap dataset
  * H3.6M dataset
* experiments (checkpoint files)
* forward kinematics
  * some variables
  * revert coordinate space
  * fkl
* visualize (class)
  * axes
  * update
* clustering
* main file
  * get data (readCSV)
  * preprocess data (normalization)
  * train (seq2seq model, mini_batch)
  * get checkpoint (save)
  * forward propagation (Seq2Seq model)
  * temporal cuts (for loop)
  * clustering
  * generate videos
