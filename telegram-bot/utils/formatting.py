from datetime import datetime


def request_to_json(request: str) -> dict:
    pairs = request.split(';')
    json_dict = {
        key: value
        for key, value in (pair.split(':') for pair in pairs)
    }
    json_dict['Budget'] = int(json_dict['Budget'])
    return json_dict


def format_route_info(self, routes):

    def format_datetime(dt_str):
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    formatted_routes = []
    for route in routes:
        ticket = route.get('ticket', {})
        hotel = route.get('hotel', {})

        flight_number = ticket.get('flight_number', 'N/A')
        departure = format_datetime(ticket.get('departure_at', 'N/A'))
        return_date = format_datetime(ticket.get('return_at', 'N/A'))
        origin = ticket.get('origin', 'N/A')
        destination = ticket.get('destination', 'N/A')
        price = ticket.get('price', 'N/A')

        hotel_name = hotel.get('hotelName', 'N/A')
        hotel_price = hotel.get('priceFrom', 'N/A')

        formatted_route = (f"Flight:\n"
                           f"  - Flight Number: {flight_number}\n"
                           f"  - From: {origin} to {destination}\n"
                           f"  - Departure: {departure}\n"
                           f"  - Return: {return_date}\n"
                           f"  - Price: {price} RUB\n"
                           f"Hotel:\n"
                           f"  - Name: {hotel_name}\n"
                           f"  - Price: {hotel_price:.2f} RUB\n")

        formatted_routes.append(formatted_route)

    return "\n---\n".join(formatted_routes)
