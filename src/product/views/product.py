from django.views import generic

from product.models import Variant, Product, ProductVariantPrice, ProductVariant
from django.db.models import Q
from datetime import datetime


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ListProductView(generic.list.ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()
    ordering = ['id']
    paginate_by = 2

    def get_query_strings(self):
        title = self.request.GET.get('title','')
        varient = self.request.GET.get('variant','')
        price_from = self.request.GET.get('price_from','')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date','')
        return (title, varient, price_from, price_to, date)

    def get_filtered_data(self):
        title, varient, price_from, price_to, date = self.get_query_strings()
        q = ProductVariantPrice.objects.all()
        p = []
        if not title and not varient and not price_from and not price_to and not date:
            pass
        else:
            if title:
                q = q.filter(product__title__icontains = title)
            if varient:
                q = q.filter(Q(product_variant_one__variant_title__icontains = varient) | Q(product_variant_two__variant_title__icontains = varient) | Q(product_variant_three__variant_title__icontains = varient))
            if price_from:
                q = q.filter(price__gte = price_from)
            if price_to:
                q = q.filter(price__lte = price_to)
            if date:
                date = "/".join(date.split("-"))
                date = datetime.strptime(date, '%Y/%m/%d')
                q = q.filter(updated_at__gte = date)

            p = set()
            for obj in q:
                p.add(obj.product.id)
            p = list(p)
        return q, p


    def get_queryset(self):
        if self.request.method == "GET":
            title, varient, price_from, price_to, date = self.get_query_strings()
            q, p = self.get_filtered_data()
            if p:
                queryset = Product.objects.filter(pk__in=p)
            else:
                queryset = Product.objects.all()
            return queryset

    def get_context_data(self, **kwargs):
        if self.request.method == "GET":
            title, varient, price_from, price_to, date = self.get_query_strings()
            q, p = self.get_filtered_data()


        context = super(ListProductView,self).get_context_data(**kwargs)
        context['variants'] = q
        context['pageContentCount'] = 2
        context['totalObjects'] = len(p) if p else len(Product.objects.all())
        context['allVariants'] = Variant.objects.all()
        context['allProductVariants'] = ProductVariant.objects.order_by().values('variant_title').distinct()
        return context