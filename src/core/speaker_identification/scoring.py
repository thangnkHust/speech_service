import os
import numpy as np
from scipy.spatial.distance import euclidean, cosine
import math
from .model import vggvox_model
from .wav_reader import get_fft_spectrum
from . import constants as c


class SpeakerIdentificationModel:
	__model = None
	@staticmethod 
	def getModel():
		""" Static access method. """
		if SpeakerIdentificationModel.__model == None:
			SpeakerIdentificationModel()
		return SpeakerIdentificationModel.__model

	def __init__(self):
		""" Virtually private constructor. """
		if SpeakerIdentificationModel.__model == None:
			SpeakerIdentificationModel.__model = vggvox_model()
			SpeakerIdentificationModel.__model.load_weights(c.WEIGHTS_FILE)
			SpeakerIdentificationModel.__model.summary()
		else:
			SpeakerIdentificationModel.__model = self.__model

	@staticmethod
	def get_speaker_result(enroll_list, feature_test):
		'''
		Description: Get speaker in speaker identification
		Input: <list> speaker registered
				<numpy> feature data of audio test
		Output: <speaker> speaker detected
				<float> confidence of speaker test compare with speaker enroll
		'''
		min_dist, min_spk = math.pi, None

		for item in enroll_list:
			if c.COST_METRIC == "euclidean":
				dist = euclidean(feature_test, np.frombuffer(item['audio_data'], dtype=np.float32))
			elif c.COST_METRIC == "cosine":
				dist = cosine(feature_test, np.frombuffer(item['audio_data'], dtype=np.float32))
			else:
				return None
			# Compare distinct
			if dist < min_dist:
				min_dist, min_spk = dist, item['speaker']

		return min_spk, math.cos(min_dist)
	
	@staticmethod
	def get_feature_data(file_path):
		'''
		Description: Get feature from audio file
		Input: <string> Path of file
		Output: <numpy> Data
		'''
		buckets = SpeakerIdentificationModel.build_buckets(c.MAX_SEC, c.BUCKET_STEP, c.FRAME_STEP)
		signal = get_fft_spectrum(file_path, buckets)
		embedding = np.squeeze(SpeakerIdentificationModel.__model.predict(signal.reshape(1,*signal.shape,1)))

		return embedding

	@staticmethod
	def build_buckets(max_sec, step_sec, frame_step):
		buckets = {}
		frames_per_sec = int(1/frame_step)
		end_frame = int(max_sec*frames_per_sec)
		step_frame = int(step_sec*frames_per_sec)
		for i in range(0, end_frame+1, step_frame):
			s = i
			s = np.floor((s-7+2)/2) + 1  # conv1
			s = np.floor((s-3)/2) + 1  # mpool1
			s = np.floor((s-5+2)/2) + 1  # conv2
			s = np.floor((s-3)/2) + 1  # mpool2
			s = np.floor((s-3+2)/1) + 1  # conv3
			s = np.floor((s-3+2)/1) + 1  # conv4
			s = np.floor((s-3+2)/1) + 1  # conv5
			s = np.floor((s-3)/2) + 1  # mpool5
			s = np.floor((s-1)/1) + 1  # fc6
			if s > 0:
				buckets[i] = int(s)
		return buckets

	@staticmethod
	def speaker_identification(enroll_list, input_data):
		feature_data = SpeakerIdentificationModel.get_feature_data(input_data)
		correct_speaker, confidence = SpeakerIdentificationModel.get_speaker_result(enroll_list, feature_data)

		return {
			'name': correct_speaker.name,
			'reliability_speaker': confidence
		}