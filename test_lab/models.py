from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField


GENDER_CHOICES: list[tuple[str, str]] = [
    ("M", "Male"),
    ("F", "Female"),
]


class YearInSchool(models.TextChoices):
    FRESHMAN = "FR", "Freshman"
    SOPHOMORE = "SO", "Sophomore"
    JUNIOR = "JR", "Junior"
    SENIOR = "SR", "Senior"
    GRADUATE = "GR", "Graduate"


class BaseModelTest(models.Model):
    pass


class ModelTest(BaseModelTest):
    choices: "models.CharField[str, str]" = models.CharField(max_length=3, choices=GENDER_CHOICES)
    year_in_school: "models.CharField[str, str]" = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
    )

    @property
    def property_none(self) -> None:
        return None

    @property
    def full_name(self) -> str | None:
        return self._meta.model_name

    full_name.fget.short_description = "полное имя класса"  # type: ignore[attr-defined, misc]


class SubClassesModelTest(ModelTest):
    pass


class SubClassesSecondModelTest(ModelTest):
    pass


class SubClassForSubClasses(SubClassesModelTest):
    pass


class ExternalClassForModelTest(models.Model):
    external_key: "ForeignKey['ModelTest', 'ModelTest']" = ForeignKey(
        on_delete=models.PROTECT, to=ModelTest  # type: ignore[misc]
    )


class DependentClassForModelTestCascade(models.Model):
    external_key: "ForeignKey['ModelTest', 'ModelTest']" = ForeignKey(
        on_delete=models.CASCADE, to=ModelTest, related_name="_TEXT_TEST+"  # type: ignore[misc]
    )


class DependentClassForModelTestOneToOne(models.Model):
    external_key: "OneToOneField['ModelTest', 'ModelTest']" = OneToOneField(
        on_delete=models.PROTECT, to=ModelTest  # type: ignore[misc]
    )


class DependentClassForModelTestManyToMany(models.Model):
    external_key: "ManyToManyField['ModelTest', 'ModelTest']" = ManyToManyField(
        to=ModelTest, related_name="+", blank=True  # type: ignore[misc]
    )
