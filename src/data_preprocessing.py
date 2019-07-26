import numpy as np
import os
import random
import copy

def define_actions(data_dir_train,num_actions):
		actions_candidate = []
		for fn in os.listdir(data_dir_train):
			actions_candidate.append(fn)
		if unique:
			return random.sample(actions_candidate,k=num_actions)
		else:
			return random.choices(actions_candidate,k=num_actions)

def readCSVasFloat(filename):
    returnArray = []
    lines = open(filename).readlines()
    for line in lines:
        line = line.strip().split(',')
        if len(line) > 0:
            returnArray.append(np.array([np.float32(x) for x in line]))
    returnArray = np.array(returnArray)
    return returnArray

def normalization_stats(all_data):
	    data_mean = np.mean(all_data,axis=0)
	    data_std = np.std(all_data,axis=0)
	    dimensions_to_ignore = []
	    dimensions_to_use = []
	    dimensions_to_ignore.extend(list(np.where(data_std<1e-4)[0]))
	    dimensions_to_use.extend(list(np.where(data_std>=1e-4)[0]))
	    data_std[dimensions_to_ignore] = 1.0
	    return data_mean, data_std, dimensions_to_ignore, dimensions_to_use

class data_prep(object):
	"""docstring for data_preprocessing"""
	def __init__(self, dataset,num_actions,unique):
		if dataset=="cmu":
			data_dir = ("./data/cmu_mocap")
		
		data_dir_train = os.path.normpath(os.path.join(data_dir,"train"))
		print("the training directory is: {0}".format(data_dir_train))
		self.norm_trainData = {}
		self.norm_testData = {}
		self.actions = define_actions(data_dir_train,num_actions,unique)
		print("the actions sequences are the following: {0}".format(self.actions))
		self.complete_train,self.trainData = self.load_data(data_dir_train)
		self.data_mean,self.data_std,self.dim_ignore,self.dim_use = normalization_stats(self.complete_train)
		self.norm_complete_train = self.normalize_data()

	def load_data(self,path_to_dataset):
		complete = []
		Data = {}
		nactions = len(self.actions)
		print("load the following action data:")
		for i in range(nactions):
			action = self.actions[i]
			sub_path = '{}/{}'.format(path_to_dataset,action)
			count = 0
			for fn in os.listdir(sub_path):
				count = count+1
			if action=='walking_extra':
				j = np.random.randint(13,53)
				filename = '{0}/{1}_{2}.txt'.format(sub_path,'walking',j)
			else:
				j = np.random.randint(1,count+1)
				filename = '{0}/{1}_{2}.txt'.format(sub_path,action,j)
			print(filename)
			action_sequence = readCSVasFloat(filename)
			r,c = action_sequence.shape
			Data[(action,j)]=action_sequence

			if len(complete)==0:
				complete = copy.deepcopy(action_sequence)
			else:
				complete = np.append(complete,action_sequence,axis=0)
		return complete,Data

	def normalize_data(self):
		norm_complete_train = np.divide((self.complete_train-self.data_mean),self.data_std)
		norm_complete_train = norm_complete_train[:,self.dim_use]
		return norm_complete_train

	def mini_batch(self,model,batch_size):
		total_frames = model.source_seq_len + model.target_seq_len
		encoder_inputs = np.zeros((model.batch_size, model.source_seq_len, model.features),dtype=float)
		decoder_inputs = np.zeros((model.batch_size, model.target_seq_len, model.features),dtype=float)
		decoder_outputs = np.zeros((model.batch_size, model.target_seq_len, model.features),dtype=float)

		for i in range(batch_size):
			r, c = self.norm_complete_train.shape
			idx = np.random.randint(0, r-total_frames)
			data_sel = self.norm_complete_train[idx:idx+total_frames, :]

			encoder_inputs[i,:,:] = data_sel[0:model.source_seq_len,:]
			decoder_inputs[i,:,:] = data_sel[model.source_seq_len-1:model.source_seq_len+model.target_seq_len-1, :]
			decoder_outputs[i,:,:] = data_sel[model.source_seq_len:,:]
		return encoder_inputs, decoder_inputs, decoder_outputs