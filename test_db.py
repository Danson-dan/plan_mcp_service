from src.plan_mcp_service import db
import json
import os

def test_database_operations():
    print("Running database tests...")
    
    # Clean up previous test db if exists (optional, but good for clean slate)
    if os.path.exists("plans.db"):
        pass # We'll just append for now, or we could delete it. 
             # For this test let's keep it simple and just run operations.

    # 1. Create a parent plan (Travel)
    print("\n1. Creating 'Japan Trip' plan...")
    travel_id = db.create_item(
        name="Japan Trip",
        category="travel",
        description="A week in Tokyo and Kyoto",
        metadata={"budget": 3000}
    )
    print(f"   -> Created Plan ID: {travel_id}")

    # 2. Add sub-tasks
    print("\n2. Adding steps to 'Japan Trip'...")
    step1 = db.create_item(name="Book Flight", parent_id=travel_id, category="travel")
    step2 = db.create_item(name="Book Hotel", parent_id=travel_id, category="travel")
    print(f"   -> Created Steps: {step1}, {step2}")

    # 3. Create a batch plan (Study)
    print("\n3. Creating 'Python Study' batch plan...")
    # Manually simulating batch creation logic here
    study_id = db.create_item(name="Python Study Week", category="study")
    db.create_item(name="Day 1: Syntax", parent_id=study_id, category="study", scheduled_at="2025-01-01")
    db.create_item(name="Day 2: Loops", parent_id=study_id, category="study", scheduled_at="2025-01-02")
    print(f"   -> Created Study Plan ID: {study_id}")

    # 4. Query Items
    print("\n4. Querying all 'travel' items...")
    travel_items = db.query_items(category="travel")
    for item in travel_items:
        print(f"   - [{item['id']}] {item['name']} (Parent: {item['parent_id']})")

    # 5. Get Tree View
    print(f"\n5. Getting Tree View for Plan {travel_id}...")
    tree = db.get_tree(travel_id)
    print(json.dumps(tree, indent=2))

    # 6. Update Item
    print(f"\n6. Updating Step {step1} to 'completed'...")
    db.update_item(step1, status="completed")
    updated_step = db.get_item(step1)
    print(f"   -> Step {step1} status: {updated_step['status']}")

    # 7. Delete Item
    print(f"\n7. Deleting Study Plan {study_id}...")
    db.delete_item(study_id)
    deleted_plan = db.get_item(study_id)
    if not deleted_plan:
        print("   -> Study Plan deleted successfully.")
    else:
        print("   -> Error: Study Plan still exists.")

    print("\nTests completed!")

if __name__ == "__main__":
    test_database_operations()
