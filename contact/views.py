from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer

@api_view(['POST'])
def contact_message_create(request):
    """
    Handle POST requests to create a new contact message.

    Validates input data using the ContactSerializer.
    Returns a success message with 201 status if valid,
    otherwise returns detailed validation errors with 400 status.
    """
    # Deserialize and validate the request data
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        # Save the validated contact message to the database
        serializer.save()
        return Response({"message": "Message reçu avec succès."}, status=status.HTTP_201_CREATED)
    
    # Return validation errors if input is invalid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
