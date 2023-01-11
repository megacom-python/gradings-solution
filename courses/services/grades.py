from django.db.models import F, Avg

class GradeService:

    def execute(self, user):
        return user.student.submissions.annotate(
            percent=F("grade") * 100 / F("assignment__points")
        ).aggregate(
            avg=Avg("percent")
        )