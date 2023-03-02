#features to be added on views
input_data = serializer.validated_data
input_features = []
for key in weights.keys():
    if key in input_data:
        input_features.append(str(input_data[key]))
    else:
        input_features.append('')

input_matrix = self.vectorizer.transform([" ".join(input_features)])
