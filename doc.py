responses_delete = {
    200: {"description": "Car deleted successfully",
          "content": {"application/json": {"example": {"message": "Car deleted"}}}},

    404: {"description": "Car not found",
          "content": {"application/json": {"example": {"detail": "Car not found"}}}}
}

responses_get_by_num = {
    200: {"description": "Car found successfully"},
    404: {"description": "Car not found",
          "content": {"application/json": {"example": {"detail": "Car not found"}}}}
}

responses_update = {
    200: {"description": "Car updated successfully",
          "content": {"application/json": {
              "example": {"message": "Car updated successfully",
                          "updated_car": {
                              "brand": "Toyota",
                              "owner_surname": "Іваненко",
                              "car_number": "AA1234BB",
                              "status": "Викрадений"
                          }}}}},
    400: {"description": "No changes were made to the car",
          "content": {"application/json": {"example": {"detail": "No changes were made to the car"}}}},
    404: {"description": "Car not found",
          "content": {"application/json": {"example": {"detail": "Car not found"}}}}
}

response_paginate = {
    200: {"content": {"application/json": {"example": {
        "cars": [
            {
                "car_number": "24254234",
                "brand": "аикп",
                "status": "Викрадений",
                "owner_surname": "кпи"
            },
            {
                "car_number": "3",
                "brand": "Toyota",
                "status": "Викрадений",
                "owner_surname": "Іваненко"
            },
            {
                "car_number": "45",
                "brand": "566",
                "status": "Викрадений",
                "owner_surname": "5675"
            }
        ],
        "totalPages": 37
    }}}}
}
examples_update = {
    "update_full": {
        "summary": "Update all fields",
        "description": "This example updates the car number, status, brand, and model.",
        "value": {
            "car_number": "AA1234BB",
            "status": "Викрадений",
            "brand": "Toyota",
            "model": "Corolla"
        }
    },
    "update_without_number": {
        "summary": "Update status, brand, and model",
        "description": "This example updates only the status, brand, and model (without car_number).",
        "value": {
            "status": "Викрадений",
            "brand": "Toyota",
            "model": "Corolla"
        }
    },
    "update_status_only": {
        "summary": "Update only status",
        "description": "This example updates only the status of the car.",
        "value": {
            "status": "Викрадений"
        }
    }
}
