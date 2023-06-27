import os
import pandas as pd
from tensorflow.keras.models import load_model
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm



MODEL_PATH = 'C:/Users/soura/cowhealthprediction/static/model/CNN_model_Capstone.h5'

# Function to load the trained model
def load_trained_model():
    model = load_model(MODEL_PATH)
    # Add any additional preprocessing or configuration if needed
    return model


# Function to perform the prediction
def predict_cow_health(file_path):
    # Load the trained model
    model = load_trained_model()
    # Read the uploaded file using pandas or any other library
    df = pd.read_excel(file_path)
    # Perform any necessary preprocessing on the data
    # Make predictions using the loaded model
    predictions = model.predict(df)
    # Process the predictions and obtain the final result
    # Return the prediction result
    return predictions

def home(request):
    return render(request, 'index.html')

def predict(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']

        if file.name.endswith(('.xls', '.xlsx')):
            try:
                # Save the uploaded file temporarily
                file_path = 'C:/Users/soura/cowhealthprediction/uploadedFiles' + file.name
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Call the predict_cow_health function
                prediction = predict_cow_health(file_path)

                # Delete the temporary file
                os.remove(file_path)

                return HttpResponse(f"The cow is predicted to be: {prediction}")
            except Exception as e:
                return HttpResponse(f"Error processing the file: {str(e)}")
        else:
            return HttpResponse('Invalid file format. Only Excel files (.xls, .xlsx) are allowed.')
    else:
        return HttpResponse('No file uploaded')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            # Save the uploaded file to a temporary location
            with open('C:/Users/soura/cowhealthprediction/uploadedFiles/testingdata.xlsx', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Process the uploaded file
            # Modify the code here to process the file as you desire
            # Example: Read the file using pandas
            import pandas as pd
            df = pd.read_excel('C:/Users/soura/cowhealthprediction/uploadedFiles/testingdata.xlsx')
            # Perform further processing or analysis

            # Pass the processed data to the template for rendering
            context = {'data': df.to_html()}
            return render(request, 'file_upload_app/result.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'file_upload_app/upload.html', {'form': form})
