# from rest_framework import generics
from scipy.stats import pearsonr
from api.models import Hostel
from api.serializers import SearchSerializer
import pandas as pd
from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame
from sklearn.metrics import jaccard_score

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from api.models import Hostel
from api.serializers import SearchSerializer
from sklearn.preprocessing import MultiLabelBinarizer

class SearchHostel(generics.ListCreateAPIView):
    queryset = Hostel.objects.all()
    serializer_class = SearchSerializer

    vectorizer = CountVectorizer()
    all_features = []
    for hostel in queryset:
        features = [hostel.hostel_name, hostel.district, hostel.place, hostel.hostel_type, hostel.single_seater, hostel.two_seater, hostel.three_seater, hostel.four_seater, hostel.wifi, hostel.hot_water, hostel.parking, hostel.laundry, hostel.cctv, hostel.fan]
        features = [str(feature) for feature in features]
        all_features.append(" ".join(features))
    feature_matrix = vectorizer.fit_transform(all_features)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
# -----------------------------------------------------

        # input_features = [str(serializer.validated_data['hostel_name']),str(serializer.validated_data['district']), str(serializer.validated_data['place']), str(serializer.validated_data['hostel_type']), str(serializer.validated_data['single_seater']), str(serializer.validated_data['two_seater']), str(serializer.validated_data['three_seater']), str(serializer.validated_data['four_seater']), str(serializer.validated_data['wifi']), str(serializer.validated_data['hot_water']), str(serializer.validated_data['parking']), str(serializer.validated_data['laundry']), str(serializer.validated_data['cctv']), str(serializer.validated_data['fan'])]

        # input_matrix = self.vectorizer.transform([" ".join(input_features)])
# --------------------------------------------
        # similarity = cosine_similarity(input_matrix, self.feature_matrix)

        # ---------------------
        
        # Define the list of features
        features_list = ['hostel_name', 'district', 'place', 'hostel_type', 'single_seater', 'two_seater', 'three_seater', 'four_seater', 'wifi', 'hot_water', 'parking', 'laundry', 'cctv', 'fan']

        # Convert the input features into a binary vector
        input_features = [str(serializer.validated_data[feature]) for feature in features_list]
        input_vector = []
        for feature in input_features:
            
            if feature:
                if isinstance(feature, bool):
                    input_vector.append(int(feature))
                else:
                    input_vector.append(feature)
            else:
                input_vector.append(0)

        # Convert the hostel features into binary vectors
        hostel_vectors = []
        for hostel in self.get_queryset():
            hostel_features = [getattr(hostel, feature) for feature in features_list]
            hostel_vector = []
            for feature in hostel_features:
                if feature:
                    if isinstance(feature, bool):
                        hostel_vector.append(int(feature))
                    else:
                        hostel_vector.append(feature)
                else:
                    hostel_vector.append(0)
            hostel_vectors.append(hostel_vector)
       

        # Convert the input and hostel vectors into arrays and apply one-hot encoding
        mlb = MultiLabelBinarizer()
        input_matrix = mlb.fit_transform([input_vector])
        hostel_matrix = mlb.transform(hostel_vectors)

    #     weights = {
    #         'hostel_name': 0.5,
    #         'district': 0.15,
    #         'place': 0.4,
    #         'hostel_type': 0.2,
    #         'single_seater': 0.05,
    #         'two_seater': 0.05,
    #         'three_seater': 0.05,
    #         'four_seater': 0.05,
    #         'wifi': 0.1,
    #         'hot_water': 0.1,
    #         'parking': 0.05,
    #         'laundry': 0.05,
    #         'cctv': 0.05,
    #         'fan': 0.05,
        
    # }
        weights = {
            'hostel_name': 0.5,
            'district': 0.2,
            'place': 0.4,
            'hostel_type': 0.2,
            'single_seater': 0.05,
            'two_seater': 0.05,
            'three_seater': 0.05,
            'four_seater': 0.05,
            'wifi': 0.1,
            'hot_water': 0.1,
            'parking': 0.05,
            'laundry': 0.05,
            'cctv': 0.05,
            'fan': 0.05,
        }
        
                
        # scores = []
        # for i, hostel in enumerate(self.get_queryset()):
        #     features = [hostel.hostel_name, hostel.district, hostel.place, hostel.hostel_type, hostel.single_seater, hostel.two_seater, hostel.three_seater, hostel.four_seater, hostel.wifi, hostel.hot_water, hostel.parking, hostel.laundry, hostel.cctv, hostel.fan]
        #     features = [str(feature) for feature in features]
        #     hostel_matrix = self.vectorizer.transform([" ".join(features)])
        #     similarity_score, _ = pearsonr(input_matrix.toarray()[0], hostel_matrix.toarray()[0])
        #     weighted_score = sum([similarity_score * weights[key] for key in weights])
        #     scores.append((i, weighted_score))

        # ranked_hostels = sorted(scores, key=lambda x: x[1], reverse=True)

        # # Get top 10 hostels
        # top_hostels = ranked_hostels[:20]

# --------------------------------------------------------------------------------------------------------------------------
        # scores = []
        # for i, hostel in enumerate(self.get_queryset()):
        #     features = [hostel.hostel_name, hostel.district, hostel.place, hostel.hostel_type, hostel.single_seater, hostel.two_seater, hostel.three_seater, hostel.four_seater, hostel.wifi, hostel.hot_water, hostel.parking, hostel.laundry, hostel.cctv, hostel.fan]
        #     features = [str(feature) for feature in features]
        #     hostel_matrix = self.vectorizer.transform([" ".join(features)])
        #     similarity_score = cosine_similarity(input_matrix, hostel_matrix)[0][0]
        #     weighted_score = sum([similarity_score * weights[key] for key in weights])
        #     scores.append((i, weighted_score))

# ----------------------------------------------------------------------------------------------------------------------
        scores = []
        for i, hostel in enumerate(self.get_queryset()):
            features = [hostel.hostel_name, hostel.district, hostel.place, hostel.hostel_type, hostel.single_seater, hostel.two_seater, hostel.three_seater, hostel.four_seater, hostel.wifi, hostel.hot_water, hostel.parking, hostel.laundry, hostel.cctv, hostel.fan]
            features = [str(feature) for feature in features]
            hostel_matrix = self.vectorizer.transform([" ".join(features)])
            similarity_score = jaccard_score(input_matrix[0], hostel_matrix[i])
            weighted_score = sum([similarity_score * weights[key] for key in weights])
            scores.append((i, weighted_score))

        ranked_hostels = sorted(scores, key=lambda x: x[1], reverse=True)

        # # Get top 10 hostels
        top_hostels = ranked_hostels[:10]

        # Get details of top hostels
        top_hostels_details = []
        for hostel in top_hostels:
            hostel_details = self.queryset[hostel[0]]
            hostel_serializer = self.get_serializer(hostel_details)
            top_hostels_details.append(hostel_serializer.data)

        # Check if there's a hostel with exact name match, move it to the top
        for i, hostel in enumerate(top_hostels_details):
            if hostel['hostel_name'] == input_features[0]:
                top_hostels_details.pop(i)
                top_hostels_details.insert(0, hostel)
                break

        return Response(top_hostels_details)
        # most_similar = similarity.argsort()[:, ::-1]
        # recommended_hostels = Hostel.objects.filter(hostel_id__in=[most_similar[0][i]+1 for i in range(5)])
        # recommended_serializer = SearchSerializer(recommended_hostels, many=True)

        # headers = self.get_success_headers(serializer.data)
        # return Response(recommended_serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# def get_recommendations(self,district, place, hostel_type, single_seater, two_seater, three_seater, four_seater, wifi, hot_water, parking, laundry, cctv, fan):
            
#         # Convert the booleans to strings
#             wifi = str(wifi)
#             hot_water = str(hot_water)
#             parking = str(parking)
#             laundry = str(laundry)
#             cctv = str(cctv)
#             fan = str(fan)

#             # Create a list of the user's input
#             input_features = [district, place, hostel_type, single_seater, two_seater, three_seater, four_seater, wifi, hot_water, parking, laundry, cctv, fan]
#             # Use CountVectorizer to convert the input into a matrix of token counts
#             input_matrix = self.vectorizer.transform([" ".join(input_features)])
#             # Calculate the cosine similarity between the input and all hostels
#             similarity = cosine_similarity(input_matrix, self.feature_matrix)
#             # Get the indices of the most similar hostels
#             most_similar = similarity.argsort()[:, ::-1]
#             # Return a list of the most similar hostels
#             return df.iloc[most_similar[0][:5]].index.tolist()

# class SearchHostel(generics.ListAPIView):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         global df
#         data=Hostel.objects.all()
#         df = read_frame(data)
#         print(df)
        



    
