from auditlog.mixins import AuditlogHistoryAdminMixin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin


class BaseAuditAdmin(AuditlogHistoryAdminMixin, ImportExportModelAdmin, UnfoldModelAdmin):
    show_auditlog_history_link = True
