import ifcopenshell

ifc_path = "data/ifc/sample_model.ifc"

model = ifcopenshell.open(ifc_path)

print("IFC loaded successfully")
print("File:", ifc_path)

doors = model.by_type("IfcDoor")
spaces = model.by_type("IfcSpace")
walls = model.by_type("IfcWall")
slabs = model.by_type("IfcSlab")
sanitary = model.by_type("IfcSanitaryTerminal")

print("Doors:", len(doors))
print("Spaces:", len(spaces))
print("Walls:", len(walls))
print("Slabs:", len(slabs))
print("Sanitary terminals:", len(sanitary))

print("\nFirst 5 doors:")
for door in doors[:5]:
    print("-", door.Name)

print("\nFirst 10 spaces:")
for space in spaces[:10]:
    print("-", space.Name)