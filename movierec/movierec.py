import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def movie_recommendation(movie_name):

    movies_df = pd.read_csv('movies.csv', usecols=['movieId', 'title'], dtype={'movieId': 'int32', 'title': 'str'})
    rating_df = pd.read_csv('ratings.csv', usecols=['userId', 'movieId', 'rating'],
                            dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

    # movies_df.head()
    # rating_df.head()

    df = pd.merge(rating_df, movies_df, on='movieId')
    # df.head()

    combine_movie_rating = df.dropna(axis=0, subset=['title'])

    movie_ratingCount = (combine_movie_rating.
    groupby(by=['title'])['rating'].
    count().
    reset_index().
    rename(columns={'rating': 'totalRatingCount'})
    [['title', 'totalRatingCount']]
    )
    # movie_ratingCount.head()

    rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on='title', right_on='title',
                                                              how='left')
    # rating_with_totalRatingCount.head()

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    # print(movie_ratingCount['totalRatingCount'].describe())

    popularity_threshold = 50
    rating_popular_movie = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
    # rating_popular_movie.head()

    rating_popular_movie.shape

    ## create a Pivot matrix
    movie_features_df = rating_popular_movie.pivot_table(index='title', columns='userId', values='rating').fillna(0)
    # movie_features_df.head()

    movie_features_df_matrix = csr_matrix(movie_features_df.values)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')

    # fit dataframe to model

    model_knn.fit(movie_features_df_matrix)

    movie_features_df.shape

    movie_features_df.head()
    #movie_features_df.to_csv("Movie features.csv")

    # pass the index of the movie
    #user_choice = "I, Robot (2004)"

    input_movie = movie_name
    ind = 0
    for i in movie_features_df.index:
        if i == input_movie:
            print(i)
            # movie_features_df.index[i]
            break
        else:
            ind += 1

    print(ind)

    query_index = ind  # I Robot
    # query_index = 75 # Bruce Almighty
   # print(" 207", movie_features_df.index[query_index])
    try:
        distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index, :].values.reshape(1, -1),
                                                  n_neighbors=6)
        lists=[]
        for i in range(0, len(distances.flatten())):
            if i == 0:
                print('Recommendations for {0}:\n'.format(movie_features_df.index[query_index]))
                lists.append('Recommendations for {0}:\n'.format(movie_features_df.index[query_index]))
                lists.append('<br><br>')
            else:
                print('{0}: {1}, with distance of {2}'.format(i, movie_features_df.index[indices.flatten()[i]],distances.flatten()[i]))
                lists.append('{0}: {1}\n'.format(i, movie_features_df.index[indices.flatten()[i]]))
                lists.append('<br>')

        return lists
    except:
        return "Recommendation Not available. Please check the spelling"
