//
//  RecipeFormView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//
import SwiftUI
import SwiftData

struct RecipeFormView: View {
    @State private var title: String = ""
    @State private var description: String = ""
    @State private var ingredients: [String]  = [""]
    @State private var steps: [String]  = [""]

    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(spacing: 16) {
            Text(title.isEmpty ? "New Recipe" : title)
                .padding(.horizontal, 16)
                .font(.title)
                .bold()

            Form {
                Section(header: Text("Title")) {
                    TextField("Grandma's classic ra...", text: $title)
                }

                Section(header: Text("Description")) {
                    TextField("The best ting ever!", text: $description)
                }

                Section(header: Text("Ingredients")) {
                    ForEach(0..<ingredients.count, id: \.self) { index in
                        TextField("Ingredient \(index + 1)", text: $ingredients[index])
                    }
                    Button("Add Ingredient") {
                        ingredients.append("")
                    }
                }

                Section(header: Text("Steps")) {
                    ForEach(0..<steps.count, id: \.self) { index in
                        TextField("Step \(index + 1)", text: $steps[index])
                    }
                    Button("Add Step") {
                        steps.append("")
                    }
                }
            }

            Button("Create Recipe") {
                createRecipe()
            }
            .buttonStyle(.glassProminent)
            .disabled(title.isEmpty || description.isEmpty || ingredients.isEmpty || steps.isEmpty)
        }
        .padding(.top, 16)
    }

    func createRecipe() {
        let recipe = Recipe(title: title, desc: description, ingredients: ingredients, steps: steps)
        modelContext.insert(recipe)

        title = ""
        description = ""
        ingredients = [""]
        steps = [""]

        dismiss()
    }
}
