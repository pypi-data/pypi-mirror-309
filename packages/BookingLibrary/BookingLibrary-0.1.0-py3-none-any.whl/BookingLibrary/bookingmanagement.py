import random
import string

class BookingManagement:
    def __init__(self):
        self.bookings = {}
    
    def generate_booking_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def book_room(self, booking_data):
        booking_id = self.generate_booking_id()  
        self.bookings[booking_id] = booking_data
        
        return {
            'status': 'success',
            'message': 'Room booked successfully',
            'booking_id': booking_id,
            'details': booking_data
        }

    def cancel_booking(self, booking_id):
        if booking_id in self.bookings:
            del self.bookings[booking_id]
            return {'status': 'success', 'message': 'Booking canceled successfully'}
        else:
            return {'status': 'error', 'message': 'Booking ID not found'}

    def get_booking(self, booking_id):
        if booking_id in self.bookings:
            return {
                'status': 'success',
                'booking_id': booking_id,
                'details': self.bookings[booking_id]
            }
        else:
            return {'status': 'error', 'message': 'Booking ID not found'}
