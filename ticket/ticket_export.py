# from ticket.models import (
#     Ticket,
#     TicketUserGroup,
#     TicketMessage,
#     TicketDetail,
# )

# EXPORT_FIELDS = {
#     # =========================
#     # Ticket
#     # =========================
#     "ticket.id": lambda t, d, m: t.id,
#     "ticket.number": lambda t, d, m: t.number,
#     "ticket.title": lambda t, d, m: t.title,
#     "ticket.status": lambda t, d, m: t.status,
#     "ticket.priority": lambda t, d, m: t.priority,
#     "ticket.type": lambda t, d, m: t.type,
#     "ticket.is_active": lambda t, d, m: t.is_active,
#     "ticket.is_resolved": lambda t, d, m: t.is_resolved,
#     "ticket.order": lambda t, d, m: t.order,
#     "ticket.created_at": lambda t, d, m: t.created_at,

#     # =========================
#     # Ticket User
#     # =========================
#     "user.id": lambda t, d, m: t.user.id if t.user else None,
#     "user.name": lambda t, d, m: str(t.user) if t.user else None,

#     # =========================
#     # Reviewer
#     # =========================
#     "reviewer.id": lambda t, d, m: t.reviewer.id if t.reviewer else None,
#     "reviewer.name": lambda t, d, m: str(t.reviewer) if t.reviewer else None,

#     # =========================
#     # Ticket Group
#     # =========================
#     "group.id": lambda t, d, m: t.users_group.id if t.users_group else None,
#     "group.name": lambda t, d, m: t.users_group.name if t.users_group else None,

#     # =========================
#     # Ticket Detail
#     # =========================
#     "detail.id": lambda t, d, m: d.id if d else None,
#     "detail.user": lambda t, d, m: str(d.user) if d and d.user else None,

#     # =========================
#     # Ticket Message
#     # =========================
#     "message.id": lambda t, d, m: m.id if m else None,
#     "message.sender": lambda t, d, m: str(m.sender) if m else None,
#     "message.content": lambda t, d, m: m.content if m else None,
#     "message.has_attachment": lambda t, d, m: bool(m.attachment) if m else False,
# }

# def export_ticket_data(ticket_id=None, selected_fields=None):
#     queryset = (
#         Ticket.objects
#         .select_related(
#             "user",
#             "reviewer",
#             "users_group",
#         )
#         .prefetch_related(
#             "ticket__message",
#             "ticket__message__sender",
#         )
#     )

#     if ticket_id:
#         queryset = queryset.filter(id=ticket_id)

#     fields = selected_fields or EXPORT_FIELDS.keys()
#     result = []

#     for ticket in queryset:
#         details = ticket.ticket.all()  # related_name='ticket'

#         if not details.exists():
#             row = {}
#             for field in fields:
#                 extractor = EXPORT_FIELDS.get(field)
#                 if extractor:
#                     row[field] = extractor(ticket, None, None)
#             result.append(row)
#             continue

#         for detail in details:
#             messages = detail.message.all()

#             if not messages.exists():
#                 row = {}
#                 for field in fields:
#                     extractor = EXPORT_FIELDS.get(field)
#                     if extractor:
#                         row[field] = extractor(ticket, detail, None)
#                 result.append(row)
#                 continue

#             for msg in messages:
#                 row = {}
#                 for field in fields:
#                     extractor = EXPORT_FIELDS.get(field)
#                     if extractor:
#                         row[field] = extractor(ticket, detail, msg)
#                 result.append(row)

#     return result

# TICKET_GROUP_EXPORT_FIELDS = {
#     "group.id": lambda g: g.id,
#     "group.name": lambda g: g.name,

#     "creator.id": lambda g: g.creator.id if g.creator else None,
#     "creator.name": lambda g: str(g.creator) if g.creator else None,

#     "members.count": lambda g: g.members.count(),
#     "members.list": lambda g: ", ".join(str(u) for u in g.members.all()),

#     "group.created_at": lambda g: g.created_at,
# }

# def export_ticket_groups(selected_fields=None):
#     queryset = (
#         TicketUserGroup.objects
#         .select_related("creator")
#         .prefetch_related("members")
#     )

#     fields = selected_fields or TICKET_GROUP_EXPORT_FIELDS.keys()
#     result = []

#     for group in queryset:
#         row = {}
#         for field in fields:
#             extractor = TICKET_GROUP_EXPORT_FIELDS.get(field)
#             if extractor:
#                 row[field] = extractor(group)
#         result.append(row)

#     return result


# TICKET_MESSAGE_EXPORT_FIELDS = {
#     "message.id": lambda m: m.id,
#     "message.content": lambda m: m.content,
#     "message.has_attachment": lambda m: bool(m.attachment),

#     "sender.id": lambda m: m.sender.id if m.sender else None,
#     "sender.name": lambda m: str(m.sender) if m.sender else None,

#     "message.created_at": lambda m: m.created_at,
# }

# def export_ticket_messages(ticket_id=None, selected_fields=None):
#     queryset = (
#         TicketMessage.objects
#         .select_related("sender")
#     )

#     if ticket_id:
#         queryset = queryset.filter(ticket_details__ticket_id=ticket_id)

#     fields = selected_fields or TICKET_MESSAGE_EXPORT_FIELDS.keys()
#     result = []

#     for message in queryset.distinct():
#         row = {}
#         for field in fields:
#             extractor = TICKET_MESSAGE_EXPORT_FIELDS.get(field)
#             if extractor:
#                 row[field] = extractor(message)
#         result.append(row)

#     return result


# TICKET_DETAIL_EXPORT_FIELDS = {
#     "detail.id": lambda d: d.id,

#     "ticket.id": lambda d: d.ticket.id if d.ticket else None,
#     "ticket.number": lambda d: d.ticket.number if d.ticket else None,

#     "user.id": lambda d: d.user.id if d.user else None,
#     "user.name": lambda d: str(d.user) if d.user else None,

#     "messages.count": lambda d: d.message.count(),
#     "messages.ids": lambda d: list(d.message.values_list("id", flat=True)),

#     "detail.created_at": lambda d: d.created_at,
# }

# def export_ticket_details(ticket_id=None, selected_fields=None):
#     queryset = (
#         TicketDetail.objects
#         .select_related("ticket", "user")
#         .prefetch_related("message")
#     )

#     if ticket_id:
#         queryset = queryset.filter(ticket_id=ticket_id)

#     fields = selected_fields or TICKET_DETAIL_EXPORT_FIELDS.keys()
#     result = []

#     for detail in queryset:
#         row = {}
#         for field in fields:
#             extractor = TICKET_DETAIL_EXPORT_FIELDS.get(field)
#             if extractor:
#                 row[field] = extractor(detail)
#         result.append(row)

#     return result
