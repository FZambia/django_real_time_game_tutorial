# coding: utf-8
from __future__ import unicode_literals
import logging

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator


logger = logging.getLogger('django_real_time_game')


class Game(models.Model):

    GAME_TITLE = _("quiz")
    GAME_SLOGAN = _("real-time quiz-like game in Django")

    STATUS_DRAFT = 0
    STATUS_NEW = 1
    STATUS_IN_PROGRESS = 2
    STATUS_FINISHED = 3

    STATUS_CHOICES = (
        (STATUS_DRAFT, _("draft")),
        (STATUS_NEW, _("new game")),
        (STATUS_IN_PROGRESS, _("game in progress")),
        (STATUS_FINISHED, _("game completed"))
    )

    STAGE_DEFAULT = 0
    STAGE_PERSONAL = 1
    STAGE_TEAM = 2
    STAGE_RESULTS = 3

    STAGE_CHOICES = (
        (STAGE_DEFAULT, _("stage default")),
        (STAGE_PERSONAL, _('stage 1: personal')),
        (STAGE_TEAM, _('stage 2: team')),
        (STAGE_RESULTS, _('stage 3: results'))
    )

    name = models.CharField(max_length=50, verbose_name=_("name of game"))
    status = models.SmallIntegerField(
        _('game status'), choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    stage = models.SmallIntegerField(
        _('game stage'), choices=STAGE_CHOICES, default=STAGE_DEFAULT
    )
    current_question = models.ForeignKey(
        "Question", verbose_name=_("current question"),
        blank=True, null=True, on_delete=models.SET_NULL, related_name="with_questions"
    )
    password = models.CharField(_("password to join"), max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = _("game")
        verbose_name_plural = _("games")

    def __unicode__(self):
        return self.name


class Team(models.Model):
    game = models.ForeignKey(Game, verbose_name=_("game"), blank=False, null=True)
    name = models.CharField(max_length=50, verbose_name=_("team name"))
    priority = models.PositiveIntegerField(_("priority"), default=0)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ('game', 'priority', 'name')

    def __unicode__(self):
        return self.name


class Player(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"),
        related_name="players", blank=True, null=True
    )
    team = models.ForeignKey(Team, verbose_name=_("team"), blank=False, null=True)
    is_active = models.BooleanField(u"активен", default=True)

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")
        ordering = ('team',)
        unique_together = ('team', 'user')

    def __unicode__(self):
        return self.user.__unicode__()


class Question(models.Model):
    game = models.ForeignKey(Game, verbose_name=_("game"), related_name="questions")
    text = models.TextField(_("question text"), blank=False, null=False)
    priority = models.PositiveIntegerField(_("priority"), default=0)

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ['game', 'priority', 'id']

    def __unicode__(self):
        if len(self.text) > 50:
            return self.text[:50] + "..."
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("question"), related_name="choices")
    text = models.CharField(_("choice text"), max_length=255, blank=False, null=False)
    priority = models.PositiveIntegerField(_("priority"), default=0)
    factor = models.FloatField(
        _("correctness factor from 0 to 1"), default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )

    class Meta:
        verbose_name = _("question answer choice")
        verbose_name_plural = _("question answer choices")
        ordering = ['question', 'priority', 'id']

    def __unicode__(self):
        return self.text


class Answer(models.Model):
    choice = models.ForeignKey(Choice)
    player = models.ForeignKey(Player)
    stage = models.SmallIntegerField(choices=Game.STAGE_CHOICES, default=Game.STAGE_DEFAULT)
    created_at = models.DateTimeField(_("answer time"), auto_now=True)

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    def __unicode__(self):
        return self.choice.text

