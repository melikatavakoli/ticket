from random import randint
from django.contrib.auth import get_user_model
from django.db import models
import jdatetime
from core.models import GenericModel
from ticket.type import PriorityType, TicketStatus, TicketType
from django.core.exceptions import ValidationError
User = get_user_model()

# ========================================================================================
# ================== Helper Function
# ========================================================================================
def ticket_attachment_path(instance, filename):
    return f'tickets/{instance.sender.mobile}/{filename}'

def validate_attachment_file(value):
    valid_mime_types = [
        'image/jpeg', 'image/png', 'image/gif',  # تصاویر
        'text/plain',  # فایل تکست
    ]
    file_mime_type = value.file.content_type
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type. Only images and text files are allowed.')

# ========================================================================================
# ================== Ticket Model
# ========================================================================================-
class Ticket(GenericModel):
    user = models.ManyToManyField(
        User,
        related_name="ticket_user",
        verbose_name="user",
    )
    status = models.CharField(
        'status',
        max_length=30,
        choices=TicketStatus.choices,
        default=TicketStatus.open,
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(
        'order',
        null=True,
        blank=True
    )
    number = models.CharField(
        'number',
        max_length=256,
        null=True,
        blank=True,
        default=''
    )
    description = models.CharField(
        'description',
        max_length=500,
        null=True,
        blank=True,
        default=''
    )
    title = models.CharField(
        'title',
        max_length=500,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_resolved = models.BooleanField(
        default=False
    )
    can_reply = models.BooleanField(
        default=True
    )
    can_upload_attachment = models.BooleanField(
        default=True
    )
    reviewer = models.ForeignKey(
        User,
        related_name="ticket_reviewer",
        verbose_name="reviewer",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    type = models.CharField(
        "type",
        choices=TicketType.choices,
        max_length=400,
        null=True,
        blank=True
    )
    priority = models.CharField(
        "priority",
        choices=PriorityType.choices,
        max_length=400,
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        # تولید شماره تیکت
        if not self.number:
            # گرفتن سال شمسی فعلی
            year = jdatetime.date.today().year  # مثال: 1404
            # اضافه کردن عدد تصادفی 5 رقمی
            random_number = randint(10000, 99999)
            self.number = f"{year}-{random_number}"
            
        # تولید order ترتیبی از ۱
        if self.order is None:
            last_order = Ticket.objects.aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0
            self.order = last_order + 1
            
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "3-ticket"
        verbose_name_plural = "3-tickets"
        db_table = 'ticket'
        indexes = [
            models.Index(fields=(
                'id',
            )),
        ]

    def __str__(self):
        return self.title or f"Ticket {self.number}" or "Unnamed Ticket"

# ========================================================================================
# ================== Ticket-Detail Model
# ========================================================================================-
class TicketDetail(GenericModel):
    ticket = models.ForeignKey(
        Ticket,
        related_name='ticket',
        verbose_name='detail_ticket',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    message = models.CharField(
        'message',
        max_length=1000,
    blank=True,
    null=True
    )
    attachment = models.FileField(
        upload_to=ticket_attachment_path,
        validators=[validate_attachment_file],
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "4-ticket_detail"
        verbose_name_plural = "4-ticket_details"
        db_table = 'ticket_detail'
        indexes = [
            models.Index(fields=('id',)),
        ]

    def __str__(self):
        return f"Message for Ticket {self.ticket.number}" if self.ticket else "TicketDetail"
