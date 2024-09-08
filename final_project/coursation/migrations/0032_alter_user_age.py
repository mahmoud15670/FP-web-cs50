# Generated by Django 4.2.15 on 2024-09-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coursation", "0031_alter_user_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="age",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                    (11, 11),
                    (12, 12),
                    (13, 13),
                    (14, 14),
                    (15, 15),
                    (16, 16),
                    (17, 17),
                    (18, 18),
                    (19, 19),
                    (20, 20),
                    (21, 21),
                    (22, 22),
                    (23, 23),
                    (24, 24),
                    (25, 25),
                    (26, 26),
                    (27, 27),
                    (28, 28),
                    (29, 29),
                    (30, 30),
                    (31, 31),
                    (32, 32),
                    (33, 33),
                    (34, 34),
                    (35, 35),
                    (36, 36),
                    (37, 37),
                    (38, 38),
                    (39, 39),
                    (40, 40),
                    (41, 41),
                    (42, 42),
                    (43, 43),
                    (44, 44),
                    (45, 45),
                    (46, 46),
                    (47, 47),
                    (48, 48),
                    (49, 49),
                    (50, 50),
                    (51, 51),
                    (52, 52),
                    (53, 53),
                    (54, 54),
                    (55, 55),
                    (56, 56),
                    (57, 57),
                    (58, 58),
                    (59, 59),
                    (60, 60),
                    (61, 61),
                    (62, 62),
                    (63, 63),
                    (64, 64),
                    (65, 65),
                    (66, 66),
                    (67, 67),
                    (68, 68),
                    (69, 69),
                    (70, 70),
                    (71, 71),
                    (72, 72),
                    (73, 73),
                    (74, 74),
                    (75, 75),
                    (76, 76),
                    (77, 77),
                    (78, 78),
                    (79, 79),
                    (80, 80),
                ],
                help_text="age 7 to 80 years",
                null=True,
            ),
        ),
    ]
