from django import template
from users.models import listing_affilies

register = template.Library()

@register.inclusion_tag('users/team.html')
def show_teams(sbfmember):
    team = listing_affilies(sbfmember)
    print(team, sbfmember)
    return { 'team': team, 'affilie': sbfmember }