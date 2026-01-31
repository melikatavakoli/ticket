from django.db import models


class TicketCategory(models.TextChoices):
    technical = "technical", "Technical"
    order = "order", "Order"
    question = "question", "Question"
    others = "others", "Others"

class TicketType(models.TextChoices):
    chat = "chat", "Chat"
    ticket = "ticket", "Ticket"

class TicketStatus(models.TextChoices):
    open = "open", "Open"
    close = "close", "Close"

class PriorityType(models.TextChoices):
    low = "low", "Low"
    high = "high", "High"
    force = "force", "Force"