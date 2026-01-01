from django.contrib import admin
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from common.admin import BaseAuditAdmin
from common.export import BaseModelResource

from .models import Ticket, TicketDetail

class TicketResource(BaseModelResource):
    id = fields.Field(attribute='id', column_name='id')
    number = fields.Field(attribute='number', column_name='number')
    title = fields.Field(attribute='title', column_name='title')
    status = fields.Field(attribute='status', column_name='status')
    priority = fields.Field(attribute='priority', column_name='priority')
    type = fields.Field(attribute='type', column_name='type')
    is_active = fields.Field(attribute='is_active', column_name='is_active')
    is_resolved = fields.Field(attribute='is_resolved', column_name='is_resolved')

    class Meta:
        model = Ticket
        fields = (
            'id',
            'number',
            'title',
            'status',
            'priority',
            'type',
            'is_active',
            'is_resolved',
        )
        import_id_fields = ('id',)
        export_order = fields

class TicketDetailInline(admin.TabularInline):
    model = TicketDetail
    extra = 0
    fields = ('message', 'attachment', 'created_by', '_created_at')
    readonly_fields = ('created_by', '_created_at')


@admin.register(Ticket)
class TicketAdmin(BaseAuditAdmin):
    resource_class = TicketResource

    list_display = (
        'number',
        'title',
        'status',
        'priority',
        'type',
        'is_active',
        'is_resolved',
        'created_by',
        '_created_at',
    )

    search_fields = (
        'number',
        'title',
        'description',
    )

    list_filter = (
        'status',
        'priority',
        'type',
        'is_active',
        'is_resolved',
    )

    ordering = ('-order', '-_created_at')

    filter_horizontal = ('user',)

    inlines = [TicketDetailInline]

    readonly_fields = (
        'number',
        'order',
        '_created_at',
        '_updated_at',
        'created_by',
        'updated_by',
    )

class TicketDetailResource(BaseModelResource):
    id = fields.Field(attribute='id', column_name='id')
    message = fields.Field(attribute='message', column_name='message')

    class Meta:
        model = TicketDetail
        fields = ('id', 'message')
        import_id_fields = ('id',)


class TicketDetailResource(BaseModelResource):
    id = fields.Field(attribute='id', column_name='id')
    message = fields.Field(attribute='message', column_name='message')

    class Meta:
        model = TicketDetail
        fields = ('id', 'message')
        import_id_fields = ('id',)


@admin.register(TicketDetail)
class TicketDetailAdmin(BaseAuditAdmin):
    resource_class = TicketDetailResource

    list_display = (
        'ticket',
        'message',
        'created_by',
        '_created_at',
    )

    search_fields = (
        'message',
        'ticket__number',
    )

    ordering = ('-_created_at',)


