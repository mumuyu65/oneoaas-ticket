# coding: utf-8
from mako import template


class DMTemplate(template.Template):
    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        return super(DMTemplate, self).render(**context_dict)


setattr(template, 'Template', DMTemplate)
