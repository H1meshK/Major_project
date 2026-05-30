import pandas as pd
import random

random.seed(42)

supplier_categories = {
    "Steel": [
        "Punjab Steel Works",
        "North India Alloys",
        "Reliable Alloy Works",
        "Steel Forge Solutions",
        "Prime Metal Fabricators"
    ],
    "Fasteners": [
        "Doaba Fasteners",
        "Titan Fastening Systems",
        "FastenPro Industries",
        "Industrial Bolt Works",
        "Precision Fasteners"
    ],
    "Castings": [
        "Guru Nanak Castings",
        "Precision Casting Works",
        "Elite Cast Products",
        "FoundryTech Castings",
        "Northern Cast Components"
    ],
    "Rubber": [
        "Punjab Rubber Industries",
        "RubberTech Solutions",
        "Industrial Elastomers",
        "Prime Rubber Components",
        "FlexiRubber Products"
    ],
    "Bearings": [
        "Industrial Bearings Co",
        "BearingTech Industries",
        "Precision Bearings Ltd",
        "Motion Bearing Systems",
        "North Bearings"
    ],
    "Auto Components": [
        "Velocity Auto Parts",
        "AutoTech Components",
        "DriveLine Products",
        "Precision Auto Systems",
        "Metro Auto Industries"
    ],
    "Engineering": [
        "Shakti Engineering Supplies",
        "Northern Engineering Ltd",
        "JMD Manufacturing Support",
        "Industrial Engineering Works",
        "Apex Engineering Systems"
    ],
    "Tools": [
        "Apex Industrial Tools",
        "ToolCraft Industries",
        "ProTool Manufacturing",
        "Industrial Tool Works",
        "Titan Tooling Solutions"
    ]
}

suppliers = []

for i in range(1, 1001):

    supplier_type = random.choice(list(supplier_categories.keys()))

    supplier_name = (
        random.choice(supplier_categories[supplier_type])
        + f" Vendor-{i}"
    )

    suppliers.append({
        "Supplier": supplier_name,
        "SupplierType": supplier_type,

        "OnTimeDelivery": random.randint(70, 99),

        "DefectRate": random.randint(1, 12),

        "CostVariance": random.randint(2, 15),

        "ComplianceScore": random.randint(75, 100),

        "LeadTime": random.randint(2, 12),

        "FulfillmentRate": random.randint(85, 100),

        "ResponseTime": random.randint(1, 6)
    })

df = pd.DataFrame(suppliers)

df.to_csv("suppliers.csv", index=False)

print(f"{len(df)} suppliers generated successfully.")