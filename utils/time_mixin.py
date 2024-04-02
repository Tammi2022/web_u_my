from django.db import models
import time


class TimeMixin(models.Model):
    """ Add creation and update times to a model. """

    creationTime = models.IntegerField(
        verbose_name="creationTime",
        null=True,
        blank=True,
        default=time.time,
    )

    lastUpdateTime = models.IntegerField(
        verbose_name="lastUpdateTime",
        null=True,
        blank=True,
        default=time.time,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            # 对象还未保存，因此设置 creationTime 和 lastUpdateTime
            self.creationTime = time.time()
            self.lastUpdateTime = time.time()
        else:
            # 对象已存在，只更新 lastUpdateTime
            self.lastUpdateTime = time.time()
        super().save(*args, **kwargs)

    # def save_times(self):
    #     """ Saves the time fields. Must be called when the subclassing model
    #     saves. """
    #     if self.creationTime is None:
    #         self.creationTime = time.time()
    #
    #     if self.lastUpdateTime is None:
    #         self.lastUpdateTime = time.time()

    class Meta:
        abstract = True
