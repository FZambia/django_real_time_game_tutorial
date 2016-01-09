# coding: utf-8
from django.contrib import admin
from core.models import Game, Team, Player, Question, Choice, Answer


class GameAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'stage', 'status')
    list_editable = ('status',)
    list_filter = ('name',)
    search_fields = ('name',)

    class Meta:
        model = Game


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'team', 'is_active')
    list_editable = ('is_active', )
    list_filter = ('team', 'team__game', 'is_active')
    search_fields = ('user__username',)
    raw_id_fields = ("user", )

    class Meta:
        model = Player


class TeamAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'game', 'priority', 'is_active')
    list_filter = ('game',)
    list_editable = ('priority', 'is_active')
    search_fields = ('name',)
    list_select_related = True

    class Meta:
        model = Team


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline, )
    list_display = ('__unicode__', 'priority', 'game')
    list_filter = ('game',)
    search_fields = ('text',)
    list_editable = ('priority', )

    class Meta:
        model = Question


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'priority', 'factor', 'question')
    list_filter = ('question__game', 'question',)
    search_fields = ('text',)
    list_editable = ('priority', 'factor')

    class Meta:
        model = Choice


class AnswerAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'pk', 'player', 'choice', 'stage', 'created_at')
    list_filter = ('choice__question__game', 'choice__question', 'stage')
    search_fields = ('player__user__username',)
    list_select_related = ("player", "player__user", "choice", "choice__question")

    class Meta:
        model = Answer


admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
