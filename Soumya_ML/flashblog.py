from flask import Flask
from training import *
from preprocess import *
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import re
import numpy as np

# Supress unnecessary warnings so that presentation looks clean
import warnings

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/predict')
def predict():

	warnings.filterwarnings('ignore')

	######################################### DISCLAIMER ###################################################################

	# This class is the final pipeline. It trains various classifiers and finally trains 2 meta classifiers on the predicted
	# probabilities of the first level classifiers. It incorporates all methods of the other classes and is the final
	# product of our project.

	######################################### DATA LOADING #################################################################

	# Print all columns. Dont hide any.
	pd.set_option('display.max_columns', None)

	# NOTE: Adjust relative file path to your file system
	data = pd.read_html("https://www2.morgenweb.de/austausch/vk_abfrage.php?out=html")
	mannheimdata = data[0]
	mannheimdata.columns = ['row', 'rubrik_id', 'latest_update', 'category', 'veranstaltung_id', 'starts', 'ends', 'veranstaltungsort_id', 'veranstalter_id', 'ort_id','name_titel','titel_kurz','titel_lang','priority','reihe_kurz','reihe_lang','ergaenzung_kurz','ergaenzung_lang','description','comment','print message','kurzinfo','phone','fax','Internet','z', 'a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','terminkalenderflag','client','text editor','picture editor','notes','organizer','Postcode','city','district','Street','House number','veranstalter_bild_link','venue','room','location info','veranstaltungsort_bild_link']

	print('Full dataset shape: ')
	print(mannheimdata.shape)

	mannheimdata = mannheimdata.dropna(subset = ['description'])
	print('Full dataset shape after dropping NAN: ')
	print(mannheimdata.shape)

	mannheimdata = mannheimdata[~mannheimdata['description'].str.contains('FSK: k.A')]

	searchfor = ['Alita: Battle Angel', '(OV)', 'Happy Deathday 2U', 'The Lego Movie', 'Die Rückkehr des Pokals - Der Film', 'Blue Planet - Ein Portrait unserer Erde', 'Drachenzähmen leicht gemacht 3: Die geheime Welt 3D', 'Chaos im Netz 3D', 'Delfine', 'Colette', 'Manhattan Queen', 'Ben is back', 'Verschwörung', 'Aquaman 3D']
	mannheimdata = mannheimdata[~mannheimdata['name_titel'].str.contains('|'.join(searchfor))]
	print('Full dataset shape after dropping fsk: ')
	print(mannheimdata.shape)
	#########################################Get rating ##################
	rating_list = []
	movie_new = []
	#ia = IMDb()
	movie_names = mannheimdata['name_titel']
	descriptions = mannheimdata['description']
	test_movie_names = mannheimdata['name_titel'].tail(96)

	print('Movies to test')
	print(test_movie_names)

	fields = {
	    'movie_names': movie_names.tolist(),
	    'descriptions': descriptions.tolist(),
	}

	# for enum in range(len(fields["movie_names"])):
	#
	#     movie = fields["movie_names"][enum]
	#     describe = fields["descriptions"][enum]
	#     des_str = str(describe)
	#     year = des_str[des_str.index("jahr: ")+6: des_str.index(" Land")]
	#     movie_new.append(movie + ' (' + year + ')')
	#
	# print(movie_new)

	# for movie_name in movie_new:
	#     imdb_id = ia.title2imdbID(movie_name)
	#     print('movie id is------')
	#     print(imdb_id)
	#     movie = ia.get_movie(imdb_id)
	#     print('movie name is------')
	#     print(movie)
	#     imdb_rate = movie['rating']
	#     print('movie rate is------')
	#     print(imdb_rate)
	#     rating_list.append(imdb_rate)
	#     print('movie rate_list is------')
	#     print(rating_list)
	#
	# print(rating_list)
	######################################### PREPROCESSING ################################################################

	# create preprocessed datasets (one-hot, dummy and label encoded)
	X_preprocessed_label = data_preprocessing(data_set=mannheimdata,
	                                            columns_to_drop=['description','row', 'rubrik_id','latest_update','ends','veranstaltung_id', 'veranstaltungsort_id', 'veranstalter_id', 'ort_id','titel_kurz','titel_lang','reihe_kurz','reihe_lang','ergaenzung_kurz','ergaenzung_lang','comment','print message','fax','z', 'a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','text editor','picture editor','notes','veranstalter_bild_link','location info','veranstaltungsort_bild_link'],
	                                            columns_to_onehot=[],
	                                            columns_to_dummy=[],
	                                            columns_to_label=['category','name_titel','priority','kurzinfo','phone','Internet','terminkalenderflag','client','organizer','Postcode','city','Street','House number','venue','room'],
	                                            normalise=False)



	y_full_continuous = [1.2, 7.1, 5.8, 5.8, 8.0, 8.0, 6.1, 6.1, 6.5, 8.0, 6.9, 7.2, 6.1, 7.2, 7.1, 8.0, 8.0, 7.3, 7.2, 7.1, 7.1, 7.1, 5.8, 7.8, 5.4, 1.5, 6.5, 8.0, 8.0, 5.6, 5.6, 5.6, 5.6, 6.3, 7.3, 7.1, 6.5, 7.3, 7.1, 7.2, 7.2, 7.2, 7.8, 8.0, 8.0, 8.0, 5.6, 6.1, 6.5, 6.5, 7.3, 8.0, 6.1, 5.3, 6.1, 6.5, 7.3, 8.2, 7.2, 7.2, 7.2, 7.1, 6.5, 6.2, 6.3, 5.8, 7.6, 7.3, 5.8, 7.6, 7.2, 7.1, 7.1, 5.8, 8.3, 6.1, 6.1, 8.0, 7.3, 7.3, 7.2, 5.8, 5.8, 5.8, 7.8, 7.8, 8.0, 8.0, 8.0, 8.0, 5.6, 6.1, 6.5, 6.3, 8.0, 6.5, 7.2, 7.2, 7.2, 7.1, 5.8, 8.0, 6.5, 6.0, 7.3, 6.5, 6.5, 7.2, 7.2, 7.2, 7.2, 7.2, 7.2, 7.2, 7.1, 7.1, 5.8, 5.8, 5.8, 7.8, 5.4, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 6.1, 7.2, 6.5, 6.5, 6.5, 5.8, 8.0, 7.1, 8.0, 6.4, 7.3, 7.2, 7.2, 5.8, 5.8, 8.0, 8.3, 8.3, 6.3, 7.1, 7.2, 5.8, 8.0, 5.6, 6.5, 7.1, 5.8, 7.3, 8.0, 5.8, 6.1, 6.9, 6.5, 7.6, 7.8, 7.2, 8.3, 6.5, 6.5, 7.5, 7.3, 7.3, 7.3, 8.3, 7.3, 6.5, 6.5, 5.8, 8.0, 7.2, 7.2, 5.8, 5.8, 7.2, 7.6, 5.8, 7.6, 6.3, 7.8, 7.8, 6.3, 8.2, 8.2, 7.2, 7.5, 5.8, 7.8, 7.8, 8.0, 8.3, 6.9, 6.5, 6.5, 6.3, 6.3, 7.2, 8.0, 8.0, 7.1, 7.8, 8.0, 8.0, 8.3, 6.3, 7.2, 7.2, 7.2, 7.8, 7.8, 8.0, 8.0, 6.5, 6.5, 6.3, 6.3, 7.8, 7.8, 8.0, 6.5, 6.3, 6.3, 7.2, 7.2, 7.2, 7.2, 5.8, 5.8, 5.8, 8.0, 8.0, 8.0, 8.0, 7.3, 8.3, 8.3, 8.3, 6.6, 6.5, 7.6, 5.8, 7.8, 8.0, 8.0, 8.3, 8.3, 7.2, 5.8, 5.8, 5.8, 7.6, 7.8, 6.4, 7.2, 5.8, 5.8, 7.8, 8.0, 8.3, 7.6, 6.3, 7.8, 7.2, 8.3, 7.3, 8.3, 5.8, 7.8, 8.0, 7.3, 6.5, 7.3, 8.2, 7.8, 7.8, 5.3, 8.3, 6.5, 7.8, 7.8, 7.5, 5.8, 7.8, 7.8, 8.2, 5.8, 7.8, 7.8, 7.8, 6.3, 6.3, 6.3, 6.1, 7.4, 7.8, 6.3, 5.8, 8.2, 8.2, 5.8, 7.8, 7.8, 7.3, 8.0, 8.0, 7.0, 6.3, 8.3, 7.4, 8.2, 5.8, 8.2, 7.5, 5.8, 7.0, 7.0, 7.6, 6.3, 6.3, 7.5, 8.0, 8.3, 7.6, 7.5, 6.3, 8.2, 8.2, 7.5, 5.8, 5.8, 7.8, 7.3, 7.0, 8.3, 8.3, 6.5, 7.6, 7.6, 7.6, 6.3, 6.3, 7.2, 5.0, 7.5, 6.5, 7.8, 7.0, 8.3, 7.6, 5.8, 5.8, 5.8, 7.3, 8.3, 8.3, 6.5, 7.6, 7.6, 6.3, 7.6, 7.2, 5.0, 7.5, 5.8, 5.8, 5.8, 5.8, 5.3, 5.3, 8.3, 8.3, 8.3, 6.3, 7.2, 5.0, 8.2, 5.8, 7.3, 5.0, 7.4, 8.2, 8.3, 7.5, 7.5, 5.3, 7.0, 7.0, 6.3, 6.3, 7.2, 6.3, 7.4, 7.5, 7.5, 5.8, 7.0, 8.3, 8.3, 7.8, 7.4, 7.4, 8.2, 7.5, 7.5, 7.5, 7.0, 7.0, 5.0, 5.0, 6.1, 5.0, 6.3, 5.8, 8.2, 5.8, 5.0, 7.0, 5.8, 6.3, 8.2, 7.5, 7.5, 5.8, 5.8, 6.3, 5.0, 6.4, 7.6, 7.2, 7.5, 5.8, 5.8, 5.8, 7.0, 6.4, 6.3, 6.1, 6.1, 5.8, 6.3, 7.4, 4.4, 7.5, 7.5, 5.8, 5.8, 5.8, 7.0, 7.0, 5.0, 5.0, 5.0, 6.1, 6.1, 6.1, 6.3, 7.5, 8.3, 6.1, 6.1, 5.0, 7.5, 5.8, 7.0, 6.3, 5.0, 5.0]
	print("Target as continuous variable")
	print(y_full_continuous)

	# bins = np.linspace(0, 10, 0.5)
	# y_binned = np.digitize(y_full, bins)

	bins = [0, 3, 7, 10]
	y_multi_class = pd.cut(y_full_continuous, bins, labels=['Bad', 'Good', 'Excellent'])
	print('Target as multi class')
	print(y_multi_class)

	#y_full_cat = y_multi_class.cat.codes
	#y_full_cat = y_multi_class.replace(('Bad', 'Good', 'Excellent'), (0, 1, 2), inplace=True)

	lbl = preprocessing.LabelEncoder()
	y_full_cat = lbl.fit_transform(y_multi_class)
	print('Target as numerical values')
	print(y_full_cat)

	# perform 80/20 train-test-split for each
	X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(X_preprocessed_label, y_full_cat,
	                                                            test_size=0.20, random_state=42, stratify=y_full_cat)


	print()
	print("LABEL ENCODED: \n")
	print(X_train_l.shape)
	print(X_test_l.shape)
	print(y_train_l.shape)
	print(y_test_l.shape)
	print()
	# print("TARGET LABEL DISTRIBUTION: \n")
	# print(y_full_cat.value_counts())
	# print()
	y_pred_test = []
	new_data = []
	######################################### 1ST LEVEL TRAINING ###########################################################

	# Dictionary to decide which ones to run; set value to False if you want the algorithm to be skipped
	classifiers = {
	    'g_naive_bayes': False,
	    'b_naive_bayes': False,
	    'c_naive_bayes': False,
	    'nearest_centroid': False,
	    'knn': False,
	    'decision_tree': True,
	    'logistic': False,
	    'random_forest': False,
	    'svm': False,
	   # 'xgboost': True
	}


	if classifiers['decision_tree']:
	    print('\n Training Decision Tree \n')

	    params_dt = {'criterion': 'gini',
	                 'max_depth': 2,
	                 'min_impurity_decrease': 0.0,
	                 'min_samples_leaf': 15,
	                 'min_samples_split': 2,
	                 'min_weight_fraction_leaf': 0.15,
	                 'random_state': 123,
	                 'splitter': 'best'
	                 }

	    decision_tree_model = train_decision_tree(params_dt,
	                                              x_train=X_train_l,
	                                              y_train=y_train_l,
	                                              n_folds=10,
	                                              random_state=123,
	                                              stratified=True,
	                                              shuffle=True
	                                              )

	    dt_x_train_probas = decision_tree_model.predict_proba(X_train_l)
	    dt_x_test_probas = decision_tree_model.predict_proba(X_test_l)

	    y_pred_full = decision_tree_model.predict(X_preprocessed_label)
	    y_pred_test = decision_tree_model.predict(X_test_l)

	    print("Confusion")
	    confusion_matrix_report(y_full_cat, y_pred_full)
	    print("Acc")
	    print(accuracy_score(y_full_cat, y_pred_full))
	    print("Precision")
	    print(precision_score(y_full_cat, y_pred_full))
	    print("Recall")
	    print(recall_score(y_full_cat, y_pred_full))
	    print("F1")
	    print(f1_score(y_full_cat, y_pred_full))


	    print("Confusion")
	    confusion_matrix_report(y_test_l, y_pred_test)
	    print("Acc")
	    print(accuracy_score(y_test_l, y_pred_test))
	    print("Precision")
	    print(precision_score(y_test_l, y_pred_test))
	    print("Recall")
	    print(recall_score(y_test_l, y_pred_test))
	    print("F1")
	    print(f1_score(y_test_l, y_pred_test))

	    print('actual label')
	    print(y_test_l)
	    print(y_test_l.dtype)
	    print('predicted label')
	    print(y_pred_test)
	    print(y_pred_test.shape)
	    print(test_movie_names.shape)
	    # print('Movies are --')
	    # print(X_test_l['name_titel'].astype(str))


	    new_data = test_movie_names + "  " + y_pred_test.astype(str)

	    print(new_data)
	    print(new_data.shape)
	    best_movies = new_data[new_data.str.contains('  2')]
	    best_movies = best_movies.astype(str).str[:-2]
	    best_movies = best_movies.astype(str)
	return str(best_movies)
if __name__ == '__main__':
	app.run(debug=True)
