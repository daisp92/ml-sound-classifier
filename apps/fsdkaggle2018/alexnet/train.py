# Train FSDKaggle2018 model
#
import sys
sys.path.append('../../..')
from lib_train import *

X_TRAIN = '../X_train.npy'
Y_TRAIN = '../y_train.npy'
Y_TEST  = '../y_test.npy'
X_TEST  = '../X_test.npy'

# 1. Load Meta data
DATAROOT = Path.home() / '.kaggle/competitions/freesound-audio-tagging'
#Data frame for training dataset
df_train = pd.read_csv(DATAROOT / 'train.csv')
#Plain y_train label
plain_y_train = np.array([conf.label2int[l] for l in df_train.label])

# 2. Preprocess data if it's not ready
def fsdkaggle2018_map_y_train(idx_train, plain_y_train):
    return np.array([plain_y_train[i] for i in idx_train])
def fsdkaggle2018_make_preprocessed_train_data():
    conf.folder.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(X_TRAIN):
        XX = mels_build_multiplexed_X(conf, [DATAROOT/'audio_train'/fname for fname in df_train.fname])
        X_train, y_train, X_test, y_test = \
            train_valid_split_multiplexed(conf, XX, plain_y_train, demux=True)
        np.save(X_TRAIN, X_train)
        np.save(Y_TRAIN, y_train)
        np.save(X_TEST, X_test)
        np.save(Y_TEST, y_test)

fsdkaggle2018_make_preprocessed_train_data()

# 3. Load all dataset & normalize
X_train, y_train = load_dataset(conf, X_TRAIN, Y_TRAIN, normalize=True)
X_test, y_test = load_dataset(conf, X_TEST, Y_TEST, normalize=True)
print('Loaded train:test = {}:{} samples.'.format(len(X_train), len(X_test)))

# 4. Train folds
history, model, plain_datagen = train_model(conf, fold=0,
                                            dataset=[X_train, y_train],
                                            model=None,
                                            init_weights=None, # from scratch
                                            #init_weights='../../model/mobilenetv2_fsd2018_41cls.h5'
)
acc = evaluate_model(conf, model, plain_datagen, X_test, y_test)

print('___ training finished ___')
