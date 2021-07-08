from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        handle a generic/unknown/unexpected http response
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
