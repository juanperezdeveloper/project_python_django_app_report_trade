from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

PICKLIST_THRESHOLDS = (1, 2, 3, 4, 5, 6, 11, 16, 21, 31, 46, 61, 91, 121, 151,
                            181, 211, 241, 271, 301, 451, 601, 751, 901, 1051,
                            1201)  # Lower Bounds

MLB_AVERAGE = (4.12,) * 12  # Rounds 1-3, Cells 1-12
MLB_AVERAGE += (3.745,) * 3  # Rounds 4-6, Cells 13-15
MLB_AVERAGE += (3.45,) * 4  # Rounds 7-10, Cells 16-19
MLB_AVERAGE += (3.42,) * 2  # Rounds 11-20, Cells 20-21
MLB_AVERAGE += (3.71,) * 2  # Rounds 21-30, Cells 22-23
MLB_AVERAGE += (4.52,) * 3  # Rounds 30+, Cells 24-26

MiLB_AVERAGE = (4,) * 12  # Rounds 1-3, Cells 1-12
MiLB_AVERAGE += (5,) * 14  # Rounds 1-3, Cells 1-12

PR_MAJORS = 4

R2_POSITION = [0.5225, 0.1909, 0.5877, 0.4806, 0.6212, 0.863, 0.9007, 0.7654, 0]
R2_STATUS = [0.667, 0.8304, 0.7963]

POSITION_CHOICES = (
    (0, 'C'),
    (1, '1B-DH'),
    (2, '2B'),
    (3, '3B'),
    (4, 'SS'),
    (5, 'OF'),
    (6, 'LHP'),
    (7, 'RHP'),
    (8, 'ALL')
)

STATUS_CHOICES = (
    (0, 'HS'),
    (1, 'JC'),
    (2, '4YR')
)

TRAVEL_TIME = (
    5.2,  # HS
    4.9,  # JC
    4.07  # 4YR
)   # In the spreadsheet, this is derived from a table listing college years
    # separately. Simplified here.


def get_idx(choices, string):
    """Given a string, finds the corresponding int index in a *_CHOICES list"""
    for pair in choices:
        if pair[1] == string.strip():
            return pair[0]


class PrMajorsData(models.Model):
    """
    Statistics on the probability of a player with a given position, status,
    and draft cell making it to the majors.
    """
    position = models.IntegerField(
        choices=POSITION_CHOICES,
        validators = [
            MinValueValidator(POSITION_CHOICES[0][0]),
            MaxValueValidator(POSITION_CHOICES[-1][0])
            ]
        )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        validators = [
            MinValueValidator(STATUS_CHOICES[0][0]),
            MaxValueValidator(STATUS_CHOICES[-1][0])
            ]
        )

    draft_cell = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(len(PICKLIST_THRESHOLDS))
            ]
        )

    value = models.FloatField(
        validators = [
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
            ]
        )

    class Meta:
        verbose_name_plural = "PrMajorsData"

    def __unicode__(self):
        return ("%s %s cell %d: %d" % (POSITION_CHOICES[self.position][1],
                                       STATUS_CHOICES[self.status][1],
                                       self.draft_cell,
                                       self.value))


class MLBData(models.Model):
    """
    MLD Salary data arranged by position, status, draft cell, and years of play
    """

    position = models.IntegerField(
        choices=POSITION_CHOICES,
        validators = [
            MinValueValidator(POSITION_CHOICES[0][0]),
            MaxValueValidator(POSITION_CHOICES[-1][0])
            ]
        )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        validators = [
            MinValueValidator(STATUS_CHOICES[0][0]),
            MaxValueValidator(STATUS_CHOICES[-1][0])
            ]
        )

    draft_cell = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(len(PICKLIST_THRESHOLDS))
            ]
        )

    year = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(19)
            ]
        )

    value = models.FloatField(
        validators = [
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
            ],
        null=True
        )

    class Meta:
        verbose_name_plural = "MLBData"

    def __unicode__(self):
        return ("%s %s cell %d year %d: %s"
                % (POSITION_CHOICES[self.position][1],
                   STATUS_CHOICES[self.status][1],
                   self.draft_cell,
                   self.year,
                   self.value))


class DOLSalary(models.Model):
    """
    Department of Labor salary statistics for a wide variety of occupations

    """

    occupation = models.CharField(max_length=255)

    sal10 = models.IntegerField()
    sal25 = models.IntegerField()
    sal50 = models.IntegerField()
    sal75 = models.IntegerField()
    sal90 = models.IntegerField()

    class Meta:
        verbose_name_plural = "DOLSalaries"

    def __unicode__(self):
        return self.occupation

    def mean(self):
        return self.sal50

    def deviation(self):
        return (1.1 * self.sal90 - self.sal50) / 2


class College(models.Model):
    """
    Statistics on the effect of college on career earnings.
    
    """
    school = models.CharField(max_length=255)
    
    # I'm using a string here because I'm not sure there is any benefit to
    # normalizing this data. It can be normalized with a FK or M2M later
    # if needed.
    type = models.CharField(max_length=255)

    starting = models.IntegerField()
    mid_career = models.IntegerField()
    start_fx = models.FloatField()
    mid_fx = models.FloatField()

    class Meta:
        verbose_name_plural = "Colleges"

    def __unicode__(self):
        return self.school


class SlotBonus(models.Model):
    """
    Bonus earned by draft slot.
    
    """

    pick = models.IntegerField()
    amount = models.IntegerField()
    draft_cell = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(len(PICKLIST_THRESHOLDS))
            ]
        )

    class Meta:
        verbose_name_plural = "SlotBonuses"

    def __unicode__(self):
        return "Pick %d ($%d, cell %d) " % (self.pick, self.amount,
                                            self.draft_cell)

class SigningBonus(models.Model):
    """
    Expected Signing Bonus

    This data is the same things as SlotBonus, but takes more inputs for
    greater accuracy.

    """

    draft_cell = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(len(PICKLIST_THRESHOLDS))
            ]
        )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        validators = [
            MinValueValidator(STATUS_CHOICES[0][0]),
            MaxValueValidator(STATUS_CHOICES[-1][0])
            ]
        )

    amount = models.IntegerField()
        
    class Meta:
        verbose_name_plural = "SigningBonuses"

    def __unicode__(self):
        return ("Cell %d, status %s: $%d"
                % (self.draft_cell,
                   STATUS_CHOICES[self.status][1],
                   self.amount))


class PrOutPosition(models.Model):

    position = models.IntegerField(
        choices=POSITION_CHOICES,
        validators = [
            MinValueValidator(POSITION_CHOICES[0][0]),
            MaxValueValidator(POSITION_CHOICES[-1][0])
            ]
        )

    year = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(18)
            ]
        )

    value = models.FloatField(
        validators = [
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
            ],
        null=True
        )

    class Meta:
        verbose_name_plural = "PrOutPositions"

    def __unicode__(self):
        return ("Position %s, year %d: %s"
                % (POSITION_CHOICES[self.position][1], self.year, self.value))

class PrOutStatus(models.Model):

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        validators = [
            MinValueValidator(STATUS_CHOICES[0][0]),
            MaxValueValidator(STATUS_CHOICES[-1][0])
            ]
        )

    year = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(18)
            ]
        )

    value = models.FloatField(
        validators = [
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
            ],
        null=True
        )

    class Meta:
        verbose_name_plural = "PrOutStatuses"

    def __unicode__(self):
        return "Status %s, year %d: %s" % (STATUS_CHOICES[self.status][1],
                                           self.year,
                                           self.value)


class Visitor(models.Model):

    modx_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    fullname = models.CharField(max_length=64, null=True, blank=True)

    ip = models.CharField(max_length=15)
    user_agent = models.CharField(max_length=255)

    # Reverse: scenarios

    def __unicode__(self):
        if self.fullname:
            return self.fullname
        else:
            return '(%s)' % (self.ip, )

class Scenario(models.Model):

    visitor = models.ForeignKey(Visitor)
    timestamp = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=True)

    college = models.ForeignKey(College)
    alt = models.ForeignKey(DOLSalary, related_name="alt_scenario_set")
    sec = models.ForeignKey(DOLSalary, related_name="sec_scenario_set")
    pick = models.IntegerField()
    pos = models.IntegerField()
    status = models.IntegerField()

    def get_draft_cell(self):
        from django_mlds.acefs.acefs import DraftCell
        return DraftCell(self.pick)

    def get_position(self):
        from django_mlds.acefs.acefs import Position
        return Position(self.pos)

    def get_status(self):
        from django_mlds.acefs.acefs import Status
        return Status(self.status)

    def get_modx_url(self):
        return 'http://example.com'
    

    def __unicode__(self):
        fullname = self.visitor.fullname
        if not fullname:
            fullname = '(Anonymous)'
        return "%s %s" % (fullname, self.timestamp)