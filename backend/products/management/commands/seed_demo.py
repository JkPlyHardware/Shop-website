from django.core.management.base import BaseCommand
from products.models import Category, Product
from chatbot.models import ChatFAQ

class Command(BaseCommand):
    help = "Create safe sample catalogue categories, sample catalogue entries and FAQ responses. No prices or customer reviews are added."
    def handle(self, *args, **options):
        items = [
            ("Wooden Doors", "wooden-doors", "Door designs and made-to-measure enquiries."),
            ("Beds", "beds", "Bed styles and custom size enquiries."),
            ("Tables", "tables", "Tables made for your space."),
            ("Bed Tables", "bed-tables", "Bedside table options."),
            ("Plywood & Laminates", "plywood-laminates", "Plywood and laminate product enquiries."),
            ("Hardware", "hardware", "Furniture and fitting hardware enquiries."),
            ("Custom Furniture", "custom-furniture", "Discuss a made-to-measure furniture project."),
        ]
        for name, slug, description in items:
            category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": description})
            # Catalogue sample labels are not claims of stock; the item is an enquiry category card.
            Product.objects.get_or_create(slug=f"enquire-{slug}", defaults={"name": f"{name} – Enquire", "category": category, "description": description, "availability": "made_to_order", "is_published": True})
        faqs = [
            ("Where is JK Ply located?", "JK Ply Hardware & Furniture Workshop is in Patna, Bihar. Please contact +91 96613 82988 for directions and the exact shop location.", "address,location,where are you,directions,patna"),
            ("How can I contact the workshop?", "You can call +91 96613 82988 or submit the contact form on this website.", "contact,phone,call,mobile,number"),
            ("What furniture do you make?", "The workshop information lists wooden doors, tables, beds, bed tables and custom furniture. Contact the workshop to discuss your requirements.", "furniture,doors,bed,table,custom"),
            ("Do you sell plywood and laminates?", "Plywood, laminates and hardware are among the listed product categories. Please contact the workshop for current options and availability.", "plywood,laminate,hardware"),
            ("How do I get a quote?", "Use the Get a quote form and share the item or measurements you need. The workshop states that prices are confirmed in writing before work starts.", "quote,price,cost,estimate,measurement"),
        ]
        for question, answer, keywords in faqs:
            ChatFAQ.objects.get_or_create(question=question, defaults={"answer": answer, "keywords": keywords})
        self.stdout.write(self.style.SUCCESS("Demo catalogue and FAQ data are ready. No prices or reviews were generated."))
