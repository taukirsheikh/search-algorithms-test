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
