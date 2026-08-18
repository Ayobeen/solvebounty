from django.core.management.base import BaseCommand
from apps.skills.models import Skill

class Command(BaseCommand):
    help = 'Seed the skills catalogue with initial skills for SolveBounty'

    def handle(self, *args, **options):
        initial_skills = [
            ("Python", "Software Engineering"),
            ("Django", "Software Engineering"),
            ("FastAPI", "Software Engineering"),
            ("JavaScript", "Software Engineering"),
            ("TypeScript", "Software Engineering"),
            ("React", "Frontend"),
            ("Next.js", "Frontend"),
            ("Tailwind CSS", "Frontend"),
            ("SQL", "Data & Databases"),
            ("PostgreSQL", "Data & Databases"),
            ("Power BI", "Data Analytics"),
            ("Data Analysis", "Data Analytics"),
            ("Data Visualization", "Data Analytics"),
            ("Machine Learning", "AI & ML"),
            ("AI Prompt Engineering", "AI & ML"),
            ("UI/UX Design", "Design"),
            ("Graphic Design", "Design"),
            ("Logo Design", "Design"),
            ("Content Writing", "Content & Marketing"),
            ("Copywriting", "Content & Marketing"),
            ("Digital Marketing", "Marketing"),
            ("Research", "General"),
            ("Financial Modeling", "Finance"),
            ("Blockchain / Web3", "Specialized"),
        ]

        count = 0
        for name, category in initial_skills:
            skill, created = Skill.objects.get_or_create(
                name=name,
                defaults={'category': category}
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} skills."))
