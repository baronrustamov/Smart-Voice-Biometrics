import cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM
from featureextraction import extract_features
import warnings
warnings.simplefilter('ignore')


def addUser(username):
    try:
        source = 'new_train/'
        destination = 'Speaker_models/'

        file_paths = open("{}_datapath.txt".format(username), 'r')

        features = np.asarray(())
        for path in file_paths:
            path = path.strip()
            print path

            # Read the audio
            sr, audio = read(source + path)

            # Extract 40 dimesnional MFCC & Delta features
            vector = extract_features(audio, sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))

        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        pklFile = "{}.gmm".format(username)
        cPickle.dump(gmm, open(destintation + pklFile, "w"))
        print "+ modelling completed for speaker: ", pklFile, " with data point = ", features.shape

        return 1
    except:
        return 0
