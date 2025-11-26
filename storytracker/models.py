from django.db import models


class Story(models.Model):
    """A single story/novel being tracked in StoryTracker."""
    title = models.CharField(max_length=200)
    genre = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Dark fantasy, psychological horror"
    )
    tags = models.CharField(
        max_length=250,
        blank=True,
        help_text="Comma-separated tags, e.g. 'dark fantasy, cult, catacombs'"
    )
    summary = models.TextField(
        blank=True,
        help_text="Short description of the story."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # This is how the story will show up in the admin/shell
        return self.title


class Update(models.Model):
    """A progress/update entry for a specific story."""
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='updates'
    )
    note = models.TextField(
        help_text="What you did for this story in this update."
    )

    # Optional: track 'how much I uploaded' for this update
    words_added = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="How many words you added in this update (optional)."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Newest updates first when you do story.updates.all()
        ordering = ['-created_at']

    def __str__(self):
        return f"Update for {self.story.title} on {self.created_at:%Y-%m-%d}"
