# import and ensure we have python ≥3.5
import sys

assert sys.version_info >= (3, 5)

# import and ensure we have scikit-Learn ≥0.20
import sklearn
assert sklearn.__version__ >= "0.20"

# import and ensure we have tensorflow ≥2.0
import tensorflow as tf
assert tf.__version__ >= "2.0"

# import commonly used modules
import numpy as np
import os

# settings for plotting figures
# -> % matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

# create and set directory to save images
PROJECT_ROOT_DIR = "."
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images")
os.makedirs(IMAGES_PATH, exist_ok=True)


# *************helper function to save images *************************
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


# get data using fetch_var_data(var_url=CONST, var_path=CONST) function

#-> use pandas to check data is downloaded
# def load_housing_data(housing_path=HOUSING_PATH):
#     csv_path = os.path.join(housing_path, "housing.csv")
#     return pd.read_csv(csv_path)
#
# housing = load_housing_data()
# housing.head()
# housing.info()
# housing["ocean_proximity"].value_counts()
# housing.describe()

#-> explore attribute histograms and save the figures
# %matplotlib inline
# import matplotlib.pyplot as plt
# housing.hist(bins=50, figsize=(20,15))
# save_fig("attribute_histogram_plots")
# plt.show()

#-> split data into training and testing with sklearn.model_selection instead of writing our own
# from sklearn.model_selection import train_test_split
#
# train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
test_set.head()