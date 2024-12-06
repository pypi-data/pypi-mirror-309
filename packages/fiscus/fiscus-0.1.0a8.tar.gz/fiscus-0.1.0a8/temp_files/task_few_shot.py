import json

task_few_shot_examples = [
    # Single-task example: Plaid for balance checking
    {
        "user": json.dumps({"user_input": "Check my bank account balance at Plaid."}),
        "assistant": json.dumps({"tasks": [{"connector": "plaid", "operation": "get_balance", "params": {}}]})
    },
    
    # Single-task example: Weather forecast from a weather service
    {
        "user": json.dumps({"user_input": "What’s the weather forecast for tomorrow in New York?"}),
        "assistant": json.dumps({"tasks": [{"connector": "weather", "operation": "get_forecast", "params": {"location": "New York", "date": "2023-10-11"}}]})
    },
    
    # Single-task example: Booking a Lyft ride
    {
        "user": json.dumps({"user_input": "Book a Lyft ride from my home to the airport at 7 AM tomorrow."}),
        "assistant": json.dumps({"tasks": [{"connector": "lyft", "operation": "schedule_ride", "params": {"pickup_location": "home", "dropoff_location": "airport", "pickup_time": "2023-10-11T07:00:00Z"}}]})
    },

    # Two-task example: Get top headlines from news API and send summary via email
    {
        "user": json.dumps({"user_input": "Get today’s top headlines and email me a summary."}),
        "assistant": json.dumps({
            "tasks": [
                {"connector": "news_api", "operation": "get_top_headlines", "params": {"country": "us"}},
                {"connector": "gmail", "operation": "send_email", "params": {"to": "user@example.com", "subject": "Today’s Top Headlines", "body": "Here’s a summary of today’s news headlines."}}
            ]
        })
    },

    # Four-task example: Creating a trip itinerary with travel-related services
    {
        "user": json.dumps({"user_input": "Plan my trip itinerary for next month: book flights, reserve a hotel, get travel insurance, and send me the details."}),
        "assistant": json.dumps({
            "tasks": [
                {"connector": "expedia", "operation": "book_flight", "params": {"destination": "Paris", "departure_date": "2023-11-01", "return_date": "2023-11-15"}},
                {"connector": "booking", "operation": "reserve_hotel", "params": {"location": "Paris", "check_in": "2023-11-01", "check_out": "2023-11-15"}},
                {"connector": "insurance_api", "operation": "purchase_travel_insurance", "params": {"destination": "Paris", "start_date": "2023-11-01", "end_date": "2023-11-15"}},
                {"connector": "gmail", "operation": "send_email", "params": {"to": "user@example.com", "subject": "Trip Itinerary", "body": "Your trip details to Paris are confirmed!"}}
            ]
        })
    }
]
