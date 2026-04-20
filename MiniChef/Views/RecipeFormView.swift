//
//  RecipeFormView.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//
import SwiftUI
import SwiftData

struct RecipeFormView: View {
    @State private var recipeID: UUID?
    @State private var title: String
    @State private var description: String
    @State private var ingredients: [String]
    @State private var steps: [String]

    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    init(recipe: Recipe? = nil) {
        _recipeID = State(initialValue: recipe?.id ?? nil)
        _title = State(initialValue: recipe?.title ?? "")
        _description = State(initialValue: recipe?.desc ?? "")
        _ingredients = State(initialValue: recipe?.ingredients ?? [])
        _steps = State(initialValue: recipe?.steps ?? [])
    }

    var body: some View {
        VStack(spacing: 16) {
            Text(!title.isEmpty ? title : "New Recipe")
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

            Button("Save Recipe") { saveRecipe() } .buttonStyle(.glassProminent)
            .disabled(title.isEmpty || description.isEmpty || ingredients.isEmpty || steps.isEmpty)
        }
        .padding(.top, 16)
    }

    func saveRecipe() {
        if recipeID == nil {
            let recipe = Recipe(title: title, desc: description, ingredients: ingredients, steps: steps)
            modelContext.insert(recipe)

        } else {
            guard let recipeID else {
                dismiss()
                return
            }

            let descriptor = FetchDescriptor<Recipe>(predicate: #Predicate { $0.id == recipeID })
            if let recipe = try? modelContext.fetch(descriptor).first {
                recipe.title = title
                recipe.desc = description
                recipe.ingredients = ingredients
                recipe.steps = steps
            }
        }

        dismiss()
    }
}
