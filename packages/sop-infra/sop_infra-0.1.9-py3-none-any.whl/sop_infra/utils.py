from django.contrib import messages

from sop_infra.models import SopInfra


__all__ = (
    'SopInfraRefreshMixin',
    'SopInfraRelatedModelsMixin'
)


class SopInfraRefreshMixin:

    def update_master_instance(self, request, instance, ad):

        if instance.ad_cumulative_users == ad:
            messages.success(request, f'{instance} has already been updated !')
            return

        instance.snapshot()
        instance.full_clean()
        instance.save()
        messages.success(request, f'{instance} successfully updated !')


    def update_child_instance(self, request, instance, ad):

        if instance.ad_cumulative_users == ad:
            messages.success(request, f'{instance} has already been updated !')
            return

        instance.snapshot()
        instance.save()
        messages.success(request, f'{instance} successfully updated !')


    def pre_compute_queryset(self, request, queryset, parent=False):

        for instance in queryset:

            if parent is False:
                self.update_child_instance(
                    request,
                    instance,
                    instance.compute_ad_cumulative_users(instance)
                )
                continue

            self.update_master_instance(
                request,
                instance,
                instance.compute_ad_cumulative_users(instance)
            )


    def refresh_infra(self, request, queryset):

        # cannot select DC because 
        queryset = queryset.exclude(site__status='dc')
        if queryset.first() is None:
            messages.error(request, 'You cannot refresh -DC- status sites.')
            return

        slave = queryset.filter(master_site__isnull=False)
        maybe_master = queryset.filter(master_site__isnull=True)

        self.pre_compute_queryset(request, slave, False)
        self.pre_compute_queryset(request, maybe_master, True)



class SopInfraRelatedModelsMixin:


    def normalize_queryset(self, obj):

        qs = [str(item) for item in obj]
        if qs == []:
            return None

        return f'id=' + '&id='.join(qs)


    def get_slave_sites(self, infra):
        '''
        look for slaves sites and join their id
        '''
        if not infra.exists():
            return None, None

        # get every SopInfra instances with master_site = current site
        # and prefetch the only attribute that matters to optimize the request
        sites = SopInfra.objects.filter(master_site=(infra.first()).site).prefetch_related('site')
        count = sites.count()

        target = sites.values_list('site__pk', flat=True)
        if not target:
            return None, None
        
        return self.normalize_queryset(target), count


    def get_slave_infra(self, infra):

        if not infra.exists():
            return None

        infras = SopInfra.objects.filter(master_site=(infra.first().site))
        count = infras.count()

        target = infras.values_list('id', flat=True)
        if not target:
            return None, None

        return self.normalize_queryset(target), count

