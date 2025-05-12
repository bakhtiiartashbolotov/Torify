from rest_framework import permissions

class IsTourOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'touroperator'
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'touroperator' and 
            obj.tour_operator == request.user
        )

class IsBookingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user

class IsTourOperatorForBooking(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'touroperator' and
            obj.tour.tour_operator == request.user
        )