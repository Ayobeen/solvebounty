from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.challenges.models import Challenge, ChallengeRequirement, PrizeAllocation
from apps.skills.models import Skill
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed initial demo users and challenges'

    def handle(self, *args, **options):
        # Demo poster
        poster, _ = User.objects.get_or_create(
            email='demo.poster@solvebounty.ng',
            defaults={
                'first_name': 'Kola',
                'last_name': 'Bakare',
                'role': User.Role.POSTER,
            }
        )
        if _:
            poster.set_password('Password123!')
            poster.save()

        # Demo solver
        solver, _ = User.objects.get_or_create(
            email='demo.solver@solvebounty.ng',
            defaults={
                'first_name': 'Ngozi',
                'last_name': 'Eze',
                'role': User.Role.SOLVER,
            }
        )
        if _:
            solver.set_password('Password123!')
            solver.save()

        # Demo challenges
        demos = [
            {
                'title': 'Build a Monthly Sales & Customer Performance Dashboard',
                'category': 'Data Analytics',
                'budget': 125000.00,
                'description': 'We need a complete interactive executive dashboard in Power BI or React/Recharts showing monthly revenue breakdown, customer acquisition cost, retention cohorts, and region-by-region metrics for Nigerian retail distribution.\n\nDeliverables:\n1. Interactive Dashboard (Power BI / web app)\n2. Clean SQL queries for data aggregation\n3. Walkthrough documentation',
                'requirements': [
                    'Interactive drill-down filters by state/region in Nigeria',
                    'Monthly revenue vs target comparison charts',
                    'Customer retention cohort matrix',
                    'Export to PDF / CSV summary report'
                ],
                'skills': ['Power BI', 'SQL', 'Data Analytics', 'Data Visualization']
            },
            {
                'title': 'React Native Cross-Platform Logistics Delivery Tracker',
                'category': 'Mobile Development',
                'budget': 250000.00,
                'description': 'Develop a clean React Native mobile app for riders in Lagos with real-time route optimization, offline order state caching, and customer delivery receipt verification.',
                'requirements': [
                    'Interactive map view with live route display',
                    'Offline caching using SQLite/AsyncStorage',
                    'Photo proof of delivery capture modal',
                    'Clean TypeScript source repository'
                ],
                'skills': ['React', 'TypeScript', 'JavaScript']
            },
            {
                'title': 'Fintech Mobile App UI/UX Design System in Figma',
                'category': 'Design',
                'budget': 85000.00,
                'description': 'Design a high-converting 12-screen mobile wallet onboarding and savings flow tailored for young Nigerian professionals. Must include a full Figma token library.',
                'requirements': [
                    '12 high-fidelity mobile screens in Figma',
                    'Complete typography and color token system',
                    'Interactive prototype showing savings goal creation'
                ],
                'skills': ['UI/UX Design', 'Graphic Design']
            }
        ]

        for d in demos:
            c, created = Challenge.objects.get_or_create(
                title=d['title'],
                defaults={
                    'poster': poster,
                    'category': d['category'],
                    'budget': d['budget'],
                    'platform_fee': d['budget'] * 0.10,
                    'description': d['description'],
                    'deadline': timezone.now() + timedelta(days=14),
                    'status': Challenge.Status.OPEN,
                    'currency': 'NGN',
                    'ip_terms': 'Full IP ownership transfers to poster upon bounty disbursement.',
                    'rules': 'Original solutions only. Proof of work required.'
                }
            )
            if created:
                for idx, r in enumerate(d['requirements']):
                    ChallengeRequirement.objects.create(
                        challenge=c,
                        description=r,
                        priority=idx + 1
                    )
                skills = Skill.objects.filter(name__in=d['skills'])
                c.skills.set(skills)
                PrizeAllocation.objects.create(challenge=c, rank=1, amount=c.budget)

        self.stdout.write(self.style.SUCCESS("Seeded demo poster, solver, and 3 active bounties successfully!"))
