#!/usr/bin/env python3
"""
OpenCog Basic Example - Reasoning with AtomSpace

This example demonstrates basic OpenCog functionality including:
- Creating concepts and relationships
- Building knowledge graphs
- Simple reasoning operations
- Pattern matching
"""

from opencog.atomspace import AtomSpace, types
from opencog.utilities import initialize_opencog
from opencog.type_constructors import *


def create_simple_knowledge_base(atomspace):
    """Create a simple knowledge base about animals and their properties."""
    
    print("=== Creating Knowledge Base ===")
    
    # Create concepts
    cat = ConceptNode('cat')
    dog = ConceptNode('dog')
    animal = ConceptNode('animal')
    mammal = ConceptNode('mammal')
    pet = ConceptNode('pet')
    
    # Create properties
    has_fur = ConceptNode('has_fur')
    makes_sound = ConceptNode('makes_sound')
    
    # Create inheritance relationships
    cat_is_animal = InheritanceLink(cat, animal)
    dog_is_animal = InheritanceLink(dog, animal)
    cat_is_mammal = InheritanceLink(cat, mammal)
    dog_is_mammal = InheritanceLink(dog, mammal)
    cat_is_pet = InheritanceLink(cat, pet)
    dog_is_pet = InheritanceLink(dog, pet)
    mammal_is_animal = InheritanceLink(mammal, animal)
    
    # Create property relationships
    cat_has_fur = InheritanceLink(cat, has_fur)
    dog_has_fur = InheritanceLink(dog, has_fur)
    
    # Add all atoms to atomspace
    atoms = [
        cat_is_animal, dog_is_animal, cat_is_mammal, dog_is_mammal,
        cat_is_pet, dog_is_pet, mammal_is_animal, cat_has_fur, dog_has_fur
    ]
    
    for atom in atoms:
        atomspace.add_atom(atom)
    
    print(f"Added {len(atoms)} relationships to the knowledge base")
    print(f"Total atoms in AtomSpace: {len(atomspace)}")
    return atomspace


def demonstrate_queries(atomspace):
    """Demonstrate basic queries on the knowledge base."""
    
    print("\n=== Demonstrating Queries ===")
    
    # Find all animals
    print("\nFinding all animals:")
    animal_concept = ConceptNode('animal')
    
    # Find all concepts that inherit from 'animal'
    for atom in atomspace:
        if (atom.type == types.InheritanceLink and 
            len(atom.out) == 2 and 
            atom.out[1] == animal_concept):
            print(f"  {atom.out[0].name} is an animal")
    
    # Find all mammals
    print("\nFinding all mammals:")
    mammal_concept = ConceptNode('mammal')
    
    for atom in atomspace:
        if (atom.type == types.InheritanceLink and 
            len(atom.out) == 2 and 
            atom.out[1] == mammal_concept):
            print(f"  {atom.out[0].name} is a mammal")


def demonstrate_reasoning(atomspace):
    """Demonstrate simple reasoning through inheritance."""
    
    print("\n=== Demonstrating Reasoning ===")
    
    # Reasoning: if X is a mammal, and mammal is an animal, then X is an animal
    print("\nReasoning about inheritance:")
    
    mammal = ConceptNode('mammal')
    animal = ConceptNode('animal')
    
    # Find what inherits from mammal
    mammals = []
    for atom in atomspace:
        if (atom.type == types.InheritanceLink and 
            len(atom.out) == 2 and 
            atom.out[1] == mammal):
            mammals.append(atom.out[0])
    
    # Check if mammal inherits from animal
    mammal_is_animal = False
    for atom in atomspace:
        if (atom.type == types.InheritanceLink and 
            len(atom.out) == 2 and 
            atom.out[0] == mammal and 
            atom.out[1] == animal):
            mammal_is_animal = True
            break
    
    if mammal_is_animal:
        print("Since mammals are animals, we can infer:")
        for m in mammals:
            print(f"  {m.name} is an animal (by transitivity)")


def main():
    """Main function to run the OpenCog example."""
    
    print("OpenCog Basic Example - AGI Reasoning")
    print("=====================================")
    
    # Initialize AtomSpace
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    print(f"Initialized AtomSpace with {len(atomspace)} atoms")
    
    # Create knowledge base
    create_simple_knowledge_base(atomspace)
    
    # Demonstrate queries
    demonstrate_queries(atomspace)
    
    # Demonstrate reasoning
    demonstrate_reasoning(atomspace)
    
    print("\n=== Summary ===")
    print(f"Final AtomSpace contains {len(atomspace)} atoms")
    print("Example completed successfully!")
    
    # Print all atoms for inspection
    print("\nAll atoms in AtomSpace:")
    for i, atom in enumerate(atomspace):
        print(f"  {i+1}. {atom}")


if __name__ == "__main__":
    main()